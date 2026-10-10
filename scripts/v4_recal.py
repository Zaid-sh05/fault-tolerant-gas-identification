"""Carrying a calibration forward in time (v4; POST-HOC, EXPLORATORY; decisions_log Q9 and R).

Usage (worktree root, with PYTHONPATH=<worktree> so that `src` is the worktree copy):
  python scripts/v4_recal.py part1 [--jobs 3]   # Q9: secondary v3 analyses + arm (e) = v2 model b8_s{s} on batch 10 (calibration shelf life)
The v2 fitted models and the v3 per-scenario predictions exist only in the main checkout; they are read READ-ONLY through the absolute
path in configs/v4_recal.yaml. Everything is written under results/v4_recal/ of this worktree.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from functools import lru_cache  # noqa: E402
from pathlib import Path, PureWindowsPath  # noqa: E402
from types import SimpleNamespace  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

sys.path.insert(0, "scripts")
from ft_v2_recal import keep_mask, scenario_list as test_scenarios  # noqa: E402
from paper_corrections import seed_t, shared_boot  # noqa: E402
from v2_arbiter import atomic, scenario_info, scenario_list as dev_scenarios  # noqa: E402
from v2_recal import CAL_GROUP, calib_rows  # noqa: E402
from src.data import load_batches, xy  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.preprocessing import fit_preprocessor  # noqa: E402
from src.scenarios import FaultStats, apply_scenario  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402
from src.strategies import StrategyKit, acted_sets, group_by_set  # noqa: E402
from src.study import OVERNIGHT  # noqa: E402

CFG = load_config("configs/v4_recal.yaml")
MAIN = Path(CFG["main_checkout"])
V2 = MAIN / CFG["v2_models"]                      # read-only
V3_PREDS = MAIN / CFG["v3_preds"]                 # read-only
V3_SCORES = Path("results/v3_prevbatch/scores.csv")
OUT = Path(CFG["output_root"])
SEEDS = tuple(CFG["seeds"])
V3_CHUNK = 40
N_CAL = CFG["n_per_gas"]
MEMORY = {int(k): tuple(v) for k, v in CFG["memory"].items()}
CANDS = CFG["candidates"]                          # insertion order = the R3 tie-break order
DEV_TARGETS, TEST_TARGETS = tuple(CFG["dev_targets"]), tuple(CFG["test_targets"])
PSEUDO_GROUP = 2000                                # group id of pseudo-labelled rows (scaler/SVM only; the detector is not refitted)
GO_DELTA, CLEAN_TOL, TIE = 0.010, 0.005, 0.002     # R3
ARM_NAMES = {"a": "(a) uncalibrated", "b": "(b) same-period", "c": "(c) previous-period", "e": "(e) two periods back (b8 on b10)"}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def worker(name):
    """A module-level function of the IMPORTED module: pickled by reference, so the lru_cache globals of __main__ never reach loky."""
    import v4_recal
    return getattr(v4_recal, name)


# ---- Test-side data, models and predictions -------------------------------------------------------------------
@lru_cache(maxsize=1)
def test_data():
    """(Xtr, ytr, btr, {8, 9, 10: (X, y)}) exactly as ft_v2_recal / v3 build them (Train 1-7 cleaned)."""
    proto = get_protocol_data(CFG)
    Xtr, ytr = xy(proto.train)
    return Xtr, ytr, proto.train["batch"].to_numpy(), {b: xy(proto.eval[proto.eval["batch"] == b]) for b in (8, 9, 10)}


@lru_cache(maxsize=1)
def test_stats():
    return FaultStats.fit(test_data()[0])


def test_rows(t, s):
    """Scored rows of batch t, seed s: the v3 / v2 kept rows."""
    return np.flatnonzero(keep_mask(test_data()[3][t][1], s, t))


def load_v2(prefix, s):
    return joblib.load(V2 / ("uncalibrated" if prefix == "uncal" else f"{prefix}_s{s}") / "fitted.joblib")


def as_model(f, V=None):
    return {"pre": f["pre"], "svm": f["svm"], "det": f["det"], "V": V}


def classify(m, X):
    """SVM labels of raw rows X; with V (CAND-C) the drift directions are projected out of the standardized input."""
    Z = fill_nan_zero(m["pre"].transform(X))
    if m["V"] is not None:
        Z = Z - (Z @ m["V"]) @ m["V"].T
    return fast_svm_predict(m["svm"], Z)


def predict(m, X, stats, scen, sids):
    """SVM and A labels on the FULL batch X for the scenarios `sids` (as v2/v3: faults with the raw Train statistics, cap 4, twin allowed)."""
    shim = SimpleNamespace(det=m["det"])                       # StrategyKit.reconstruct only uses .det
    out = {"svm": [], "A": []}
    for sid in sids:
        sc = scen[sid]
        Xf = X if sc is None else apply_scenario(X, sc, stats)[0]
        R = m["det"].ratio(Xf)
        Xr = StrategyKit.reconstruct(shim, Xf, group_by_set(acted_sets(R, R > 1.0)), False)
        out["svm"].append(classify(m, Xf))
        out["A"].append(classify(m, Xr))
    return {k: np.array(v, dtype=np.int8) for k, v in out.items()}


def load_v3_preds(arm, t, s, root=None):
    """v3 labels (svm, A, B; all 1081 scenarios, all rows of batch t), with a provenance check of every chunk."""
    d = Path(root or V3_PREDS) / (f"a_b{t}" if arm == "a" else f"{arm}_b{t}_s{s}")
    expect = {"a": ("uncalibrated", 0), "b": (f"b{t}_s{s}", s), "c": (f"b{t - 1}_s{s}", s)}[arm]
    n = len(test_scenarios())
    starts = list(range(0, n, V3_CHUNK))
    parts = [pickle.load(open(d / f"chunk_{i:03d}.pkl", "rb")) for i in range(len(starts))]
    for p, a in zip(parts, starts):
        got = (p["arm"], p["target"], PureWindowsPath(p["model"]).name, p["seed"], p["sids"])
        assert got == (arm, t, *expect, list(range(a, min(a + V3_CHUNK, n)))), f"bad v3 chunk in {d}"
    return {m: np.concatenate([p["preds"][m] for p in parts]) for m in ("svm", "A", "B")}


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic(path, lambda p: pickle.dump(obj, open(p, "wb")))


def load_parts(paths, expect):
    """Concatenate prediction parts after checking each part's provenance fields against `expect` (dict of field -> value)."""
    parts = [pickle.load(open(p, "rb")) for p in paths]
    for p in parts:
        assert all(p[k] == v for k, v in expect.items()), f"bad part {p.get('key')}"
    sids = [i for p in parts for i in p["sids"]]
    return {m: np.concatenate([p["preds"][m] for p in parts]) for m in parts[0]["preds"]}, sids


# ---- Part 1 (Q9) ------------------------------------------------------------------------------------------------
def job_e(s, index, sids):
    """Arm (e): the v2 model b8_s{s} applied unchanged to batch 10 (no refit)."""
    path = OUT / "preds" / "part1" / f"e_b10_s{s}" / f"chunk_{index:03d}.pkl"
    if not path.exists():
        preds = predict(as_model(load_v2("b8", s)), test_data()[3][10][0], test_stats(), test_scenarios(), sids)
        save(path, {"arm": "e", "target": 10, "seed": s, "model": f"b8_s{s}", "sids": list(sids), "preds": preds})
    return str(path)


def score_frame(rows):
    df = pd.DataFrame(rows, columns=["subset", "cal_seed", "arm", "method", "sid", "f1"])
    info = pd.DataFrame([{"sid": i, **scenario_info(sc), "level": (np.nan if sc is None else sc.level)} for i, sc in enumerate(test_scenarios())])
    return df.merge(info, on="sid")


def per_seed(df, sub, arm, m):
    """(5, n_fault_scenarios) Macro-F1 under faults, the k labels and the sids, with an alignment check across seeds."""
    g = df[(df.subset == sub) & (df.arm == arm) & (df.method == m) & (df.setting != "clean")].sort_values(["cal_seed", "sid"])
    mats = [g[g.cal_seed == s] for s in SEEDS]
    assert all(np.array_equal(x.sid.to_numpy(), mats[0].sid.to_numpy()) for x in mats) and len(mats[0]), (sub, arm, m)
    return np.stack([x.f1.to_numpy() for x in mats]), mats[0].setting.to_numpy(), mats[0].sid.to_numpy()


def clean(df, sub, arm, m):
    g = df[(df.subset == sub) & (df.arm == arm) & (df.method == m) & (df.setting == "clean")].sort_values("cal_seed")
    assert list(g.cal_seed) == list(SEEDS), (sub, arm, m)
    return g.f1.to_numpy()


def diff_boot(df, sub, x, y):
    """k-balanced Macro-F1 under faults, x - y, paired by scenario; x and y are (arm, method); v2 shared-index bootstrap."""
    (X, k, sx), (Y, _, sy) = per_seed(df, sub, *x), per_seed(df, sub, *y)
    assert np.array_equal(sx, sy)
    return dict(zip(("value", "ci_low", "ci_high"), shared_boot(X - Y, k)))


def level_boot(df, sub, arm, m):
    X, k, _ = per_seed(df, sub, arm, m)
    return dict(zip(("value", "ci_low", "ci_high"), shared_boot(X, k)))


def retention(df, sub, arm, m):
    """J6: per scenario Macro-F1 / clean (same method, arm, subset, seed), k1 and k2 weighted equally; worst as ft_v2_tables."""
    X, k, _ = per_seed(df, sub, arm, m)
    c = clean(df, sub, arm, m)
    r = X / c[:, None]
    ret = np.mean([np.mean([r[i][k == kk].mean() for kk in ("k1", "k2")]) for i in range(len(SEEDS))])
    worst = np.mean([min(X[i].min(), c[i]) for i in range(len(SEEDS))])
    return ret, worst


def stage_part1(jobs):
    n = len(test_scenarios())
    tasks = [(s, i, list(range(a, min(a + V3_CHUNK, n)))) for s in SEEDS for i, a in enumerate(range(0, n, V3_CHUNK))]
    log(f"part1: arm (e) = b8_s* on batch 10, {len(tasks)} chunks")
    Parallel(n_jobs=jobs, verbose=5)(delayed(worker("job_e"))(*task) for task in tasks)
    y10 = test_data()[3][10][1]
    rows = []
    for s in SEEDS:
        d = OUT / "preds" / "part1" / f"e_b10_s{s}"
        P, sids = load_parts(sorted(d.glob("chunk_*.pkl")), {"arm": "e", "target": 10, "seed": s, "model": f"b8_s{s}"})
        assert sids == list(range(n))
        keep = test_rows(10, s)
        rows += [("b10", s, "e", m, sid, scores(y10[keep], P[m][sid][keep])["macro_f1"]) for m in ("svm", "A") for sid in range(n)]
    e = score_frame(rows)
    e.to_csv(OUT / "part1_arm_e_scores.csv", index=False)
    df = pd.concat([pd.read_csv(V3_SCORES), e], ignore_index=True)

    levels = [{"subset": sub, "arm": ARM_NAMES[a], "method": m, **level_boot(df, sub, a, m)}
              for sub in ("b9", "b10", "pooled") for a in "abc" for m in ("svm", "A", "B")]
    levels += [{"subset": "b10", "arm": ARM_NAMES["e"], "method": m, **level_boot(df, "b10", "e", m)} for m in ("svm", "A")]
    full = [{"subset": sub, "comparison": f"{m} in arm (c) - SVM in arm (a), under faults", **diff_boot(df, sub, ("c", m), ("a", "svm"))}
            for sub in ("b9", "b10", "pooled") for m in ("A", "B")]
    ret = [{"subset": sub, "arm": ARM_NAMES[a], "method": m, **dict(zip(("retention_j6", "worst"), retention(df, sub, a, m)))}
           for sub in ("b9", "b10", "pooled") for a in "abc" for m in ("svm", "A", "B")]
    ret += [{"subset": "b10", "arm": ARM_NAMES["e"], "method": m, **dict(zip(("retention_j6", "worst"), retention(df, "b10", "e", m)))}
            for m in ("svm", "A")]
    shelf = []
    for label, age, sub, arm in (("same period (b)", "0 (rows interleaved, N9)", "b9", "b"), ("same period (b)", "0 (rows interleaved, N9)", "b10", "b"),
                                 ("8 -> 9 (c)", "1-8 months", "b9", "c"), ("9 -> 10 (c)", "6-12 months", "b10", "c"),
                                 ("8 -> 10 (e)", "13-14 months", "b10", "e")):
        g = diff_boot(df, sub, (arm, "A"), ("a", "A"))
        same = diff_boot(df, sub, ("b", "A"), ("a", "A"))["value"]
        cg = seed_t(clean(df, sub, arm, "svm") - clean(df, sub, "a", "svm"))
        shelf.append({"calibration": label, "age": age, "target": sub, "A_faults_gain_vs_a": g["value"], "A_ci_low": g["ci_low"],
                      "A_ci_high": g["ci_high"], "share_of_same_period_gain": g["value"] / same, "clean_svm_gain_vs_a": cg[0],
                      "clean_ci_low": cg[1], "clean_ci_high": cg[2]})
    ec = diff_boot(df, "b10", ("e", "A"), ("c", "A"))
    shelf.append({"calibration": "8 -> 10 (e) minus 9 -> 10 (c)", "age": "13-14 vs 6-12 months", "target": "b10", "A_faults_gain_vs_a": ec["value"],
                  "A_ci_low": ec["ci_low"], "A_ci_high": ec["ci_high"]})
    out = {"part1_levels": levels, "part1_full_pipeline": full, "part1_retention": ret, "part1_shelf_life": shelf}
    md = ["# Part 1 (decisions_log Q9; secondary, defined after the Q results, not pre-registered)", "",
          "From the saved v3 predictions and one extra arm (e) = v2 model b8_s{s} applied unchanged to batch 10. Under faults = k1/k2 equal "
          "weight, mean over 5 calibration seeds; 95% v2 shared-index scenario bootstrap (faults), 95% t over seeds (clean).", ""]
    for name, tab in out.items():
        tab = pd.DataFrame(tab)
        tab.round(6).to_csv(OUT / f"{name}.csv", index=False)
        md += [f"## {name}", "", tab.round(4).to_markdown(index=False), ""]
    (OUT / "PART1.md").write_text("\n".join(md), encoding="utf-8")
    log("part1: written " + ", ".join(out))


# ---- Part 2 (decisions_log R): development data, candidates and models ---------------------------------------------
@lru_cache(maxsize=1)
def dev_data():
    """Drift-Dev (R1): Train 1-3 cleaned as v2, evaluation batches 6 and 7, and batch 5 (raw) for its calibration rows. Never 8-10."""
    cfg = load_config(CFG["dev_config"])
    proto = get_protocol_data(cfg)                                    # temporal protocol: asserts that no Test batch is loaded
    Xtr, ytr = xy(proto.train)
    ev = {int(b): xy(proto.eval[proto.eval["batch"] == b]) for b in DEV_TARGETS}
    for b in CFG["dev_extra_batches"]:
        assert b not in (8, 9, 10), "development steps never read batches 8-10"
        ev[b] = xy(load_batches(cfg["data"]["raw_dir"], [b]))
    return Xtr, ytr, proto.train["batch"].to_numpy(), ev


@lru_cache(maxsize=1)
def dev_stats():
    return FaultStats.fit(dev_data()[0])


def dev_rows(t, s):
    return np.flatnonzero(keep_mask(dev_data()[3][t][1], s, t))


def data(domain):
    return dev_data() if domain == "dev" else test_data()


def kept(domain, t, s):
    return dev_rows(t, s) if domain == "dev" else test_rows(t, s)


def halves(domain, t, s):
    """CAND-S: fixed disjoint halves H1/H2 of the kept rows of batch t (generator keyed by seed and batch)."""
    k = kept(domain, t, s)
    perm = np.random.default_rng([s, t]).permutation(k)
    return np.sort(perm[: len(k) // 2]), np.sort(perm[len(k) // 2:])


def comparison_rows(domain, key, t, s):
    """Rows on which `key` and every arm it is compared with are scored: H2 for CAND-S, otherwise the kept rows."""
    return halves(domain, t, s)[1] if key in CANDS and CANDS[key]["family"] == "S" else kept(domain, t, s)


def train_set(domain, batches, s, w=1.0):
    """Train rows + the seed-s calibration rows of each batch in `batches` (each its own detector group); weights 1 / w."""
    Xtr, ytr, btr, ev = data(domain)
    Xs, ys, gs, ws = [Xtr], [ytr], [btr], [np.ones(len(ytr))]
    for b in batches:
        c = calib_rows(ev[b][1], N_CAL, s, b)
        Xs.append(ev[b][0][c])
        ys.append(ev[b][1][c])
        gs.append(np.full(len(c), CAL_GROUP + b))
        ws.append(np.full(len(c), float(w)))
    return np.vstack(Xs), np.concatenate(ys), np.concatenate(gs), np.concatenate(ws)


def standardize(pre, X):
    return fill_nan_zero(pre.transform(X))


def svm_params():
    return json.load(open(OVERNIGHT / "final_pipeline.json"))["svm_params"]


def fit_recipe(X, y, groups, weight=None, detector=True):
    """The N2 recipe of ft_v2_recal.fit_model (StandardScaler, SVC C=10 gamma=0.01, median detector), optional SVM sample weights."""
    pre = fit_preprocessor(json.load(open(OVERNIGHT / "final_pipeline.json"))["spec"], X, y, groups, fill_nan=False)
    svm = SVC(kernel="rbf", random_state=0, **svm_params()).fit(standardize(pre, X), y, sample_weight=weight)
    det = ReliabilityDetector(normalization="median").fit(X, groups) if detector else None
    return {"pre": pre, "svm": svm, "det": det, "V": None}


def drift_directions(Z, y, is_cal, r):
    """Top-r right singular vectors (uncentered) of the per-gas drift vectors mean(calibration, gas) - mean(Train, gas)."""
    D = np.stack([Z[is_cal & (y == g)].mean(0) - Z[~is_cal & (y == g)].mean(0)
                  for g in np.unique(y[is_cal]) if (~is_cal & (y == g)).any()])
    return np.linalg.svd(D, full_matrices=False)[2][:r].T


def prev_model(domain, t, s):
    """prev = Train + calibration rows of batch t-1: fitted by the recipe on dev; the identical v2 model b{t-1}_s{s} on Test."""
    X, y, g, _ = train_set(domain, (t - 1,), s)
    if domain == "dev":
        return fit_recipe(X, y, g), X, y, g
    f = load_v2(f"b{t - 1}", s)
    assert np.array_equal(f["Xtr"], X) and np.array_equal(f["ytr"], y)
    return as_model(f), X, y, g


def build(domain, key, t, s):
    """(model, info) of a reference arm (dev only) or a candidate (R2). No label of batch t enters any fit."""
    if key in ("uncal", "same", "prev"):
        assert domain == "dev", "on Test the reference arms are the saved v3 predictions"
        X, y, g, _ = train_set(domain, {"uncal": (), "same": (t,), "prev": (t - 1,)}[key], s)
        return fit_recipe(X, y, g), {"n_fit": len(y)}
    c = CANDS[key]
    if c["family"] == "W":
        X, y, g, w = train_set(domain, MEMORY[t], s, c["w"])
        return fit_recipe(X, y, g, None if c["w"] == 1 else w), {"n_fit": len(y), "n_cal": int((g >= CAL_GROUP).sum())}
    prev, Xp, yp, gp = prev_model(domain, t, s)
    if c["family"] == "C":
        X, y, g, _ = train_set(domain, MEMORY[t], s)
        pre = fit_preprocessor(json.load(open(OVERNIGHT / "final_pipeline.json"))["spec"], X, y, g, fill_nan=False)
        Z = standardize(pre, X)
        V = drift_directions(Z, y, g >= CAL_GROUP, c["r"])
        svm = SVC(kernel="rbf", random_state=0, **svm_params()).fit(Z - (Z @ V) @ V.T, y)
        return {"pre": pre, "svm": svm, "det": prev["det"], "V": V}, {"n_fit": len(y), "V": V}
    h1, _ = halves(domain, t, s)
    Xh = data(domain)[3][t][0][h1]                                    # CLEAN, UNLABELED readings of H1
    Z = standardize(prev["pre"], Xh)
    lab = fast_svm_predict(prev["svm"], Z)
    dec = np.sort(prev["svm"].decision_function(Z), axis=1)
    margin = dec[:, -1] - dec[:, -2]
    sel = np.sort(np.concatenate([idx[np.argsort(-margin[idx], kind="stable")[: int(np.ceil(c["q"] * len(idx)))]]
                                  for idx in (np.flatnonzero(lab == g) for g in np.unique(lab))]))
    m = fit_recipe(np.vstack([Xp, Xh[sel]]), np.r_[yp, lab[sel]], np.r_[gp, np.full(len(sel), PSEUDO_GROUP + t)], detector=False)
    m["det"] = prev["det"]
    return m, {"n_fit": len(yp) + len(sel), "pseudo_rows": h1[sel], "pseudo_labels": lab[sel]}


# ---- Part 2: development runs, dev gate, tournament and the R3 decision -----------------------------------------------
def dev_pred_path(key, t, s):
    return OUT / "preds" / "dev" / f"{key}_b{t}_s{s}.pkl"


def job_dev(key, t, s):
    path = dev_pred_path(key, t, s)
    if not path.exists():
        m, info = build("dev", key, t, s)
        n = len(dev_scenarios())
        preds = predict(m, dev_data()[3][t][0], dev_stats(), dev_scenarios(), range(n))
        save(path, {"domain": "dev", "key": key, "target": t, "seed": s, "sids": list(range(n)), "preds": preds, "info": info})
    return str(path)


def load_dev_preds(key, t, s):
    s0 = 0 if key == "uncal" else s                                   # the uncalibrated model does not depend on the seed
    p = pickle.load(open(dev_pred_path(key, t, s0), "rb"))
    assert (p["domain"], p["key"], p["target"], p["seed"], p["sids"]) == ("dev", key, t, s0, list(range(len(dev_scenarios())))), key
    return p["preds"]


def dev_score_frame(keys_by_rows):
    """Macro-F1 per (rows kind, key, target, seed, method, sid); rows kind 'keep' = kept rows, 'H2' = the CAND-S scoring half."""
    rows = []
    for t in DEV_TARGETS:
        y = dev_data()[3][t][1]
        for s in SEEDS:
            idx = {"keep": dev_rows(t, s), "H2": halves("dev", t, s)[1]}
            for kind, keys in keys_by_rows.items():
                for key in keys:
                    P = load_dev_preds(key, t, s)
                    r = idx[kind]
                    rows += [(kind, key, t, s, m, sid, scores(y[r], P[m][sid][r])["macro_f1"]) for m in ("svm", "A") for sid in range(len(P[m]))]
    df = pd.DataFrame(rows, columns=["rows", "key", "target", "cal_seed", "method", "sid", "f1"])
    info = pd.DataFrame([{"sid": i, **scenario_info(sc)} for i, sc in enumerate(dev_scenarios())])
    return df.merge(info, on="sid")


def stage_devgate(jobs):
    tasks = [("uncal", t, 0) for t in DEV_TARGETS] + [("same", t, s) for t in DEV_TARGETS for s in SEEDS]
    log(f"devgate: {len(tasks)} reference models (uncal, same) on Drift-Dev")
    Parallel(n_jobs=jobs, verbose=5)(delayed(worker("job_dev"))(*task) for task in tasks)
    df = dev_score_frame({"keep": ["uncal", "same"]})
    v2 = pd.read_csv("results/v2/recal/scenarios.csv")
    v2 = v2[v2.protocol == "drift_dev"].replace({"model": {"uncalibrated": "uncal", "calibrated": "same"}})
    m = df.merge(v2.rename(columns={"model": "key", "batch": "target"})[["key", "target", "cal_seed", "sid", "svm", "A"]]
                 .melt(id_vars=["key", "target", "cal_seed", "sid"], var_name="method", value_name="f1_v2"),
                 on=["key", "target", "cal_seed", "sid", "method"])
    diff = float((m.f1 - m.f1_v2).abs().max())
    ok = len(m) == len(df) and diff <= 5.1e-6                          # results/v2/recal/scenarios.csv has 5 decimals
    json.dump({"rows_compared": len(m), "rows_ours": len(df), "max_abs_diff": diff, "tolerance": 5.1e-6, "passed": ok},
              open(OUT / "devgate.json", "w"), indent=1)
    log(f"devgate: {len(m)}/{len(df)} rows vs v2 stage 2, max |diff| {diff:.3g} -> {'PASSED' if ok else 'FAILED'}")
    if not ok:
        raise SystemExit(1)


def kbal(df, kind, key, method="A"):
    """Dev score: per (target, seed) the k1 and k2 means averaged equally, then the mean over seeds and the two targets."""
    g = df[(df.rows == kind) & (df.key == key) & (df.method == method) & (df.setting != "clean")]
    per = g.groupby(["target", "cal_seed", "setting"]).f1.mean().unstack("setting")
    return float(((per["k1"] + per["k2"]) / 2).mean()), ((per["k1"] + per["k2"]) / 2).groupby("target").mean().to_dict()


def clean_svm(df, kind, key):
    return float(df[(df.rows == kind) & (df.key == key) & (df.method == "svm") & (df.setting == "clean")].f1.mean())


def stage_tournament(jobs):
    assert json.load(open(OUT / "devgate.json"))["passed"], "the dev gate has not passed"
    (OUT / "DEV_STARTED").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
    tasks = [(k, t, s) for k in ["prev", *CANDS] for t in DEV_TARGETS for s in SEEDS]
    log(f"tournament: {len(tasks)} models (prev + 7 candidates) on Drift-Dev")
    t0 = time.time()
    Parallel(n_jobs=jobs, verbose=5)(delayed(worker("job_dev"))(*task) for task in tasks)
    s_keys = [k for k in CANDS if CANDS[k]["family"] == "S"]
    df = dev_score_frame({"keep": ["uncal", "same", "prev", *[k for k in CANDS if k not in s_keys]], "H2": ["uncal", "same", "prev", *s_keys]})
    df.to_csv(OUT / "dev_scores.csv", index=False)
    table = []
    for kind, key in [("keep", "uncal"), ("keep", "same"), ("keep", "prev"), ("H2", "prev")] + [("H2" if k in s_keys else "keep", k) for k in CANDS]:
        score, per_t = kbal(df, kind, key)
        ref, ref_t = kbal(df, kind, "prev")
        table.append({"config": key, "rows": kind, "dev_score_A_faults": score, "prev_same_rows": ref, "delta_vs_prev": score - ref,
                      "delta_t6": per_t[6] - ref_t[6], "delta_t7": per_t[7] - ref_t[7], "clean_svm": clean_svm(df, kind, key),
                      "clean_svm_minus_prev": clean_svm(df, kind, key) - clean_svm(df, kind, "prev"),
                      "candidate": key in CANDS})
    tab = pd.DataFrame(table)
    cand = tab[tab.candidate].set_index("config")
    elig = [k for k in CANDS if cand.loc[k, "clean_svm_minus_prev"] >= -CLEAN_TOL]
    winner = None
    if elig:
        best = max(cand.loc[k, "delta_vs_prev"] for k in elig)
        winner = next(k for k in CANDS if k in elig and cand.loc[k, "delta_vs_prev"] >= best - TIE)
    go = winner is not None and bool(cand.loc[winner, "delta_vs_prev"] >= GO_DELTA)
    w1_check = all(np.array_equal(load_dev_preds("W1", 6, s)[m], load_dev_preds("prev", 6, s)[m]) for s in SEEDS for m in ("svm", "A"))
    decision = {"rule": "decisions_log R3", "eligible": elig, "winner": winner, "go": go,
                "winner_delta_vs_prev": None if winner is None else float(cand.loc[winner, "delta_vs_prev"]),
                "winner_clean_svm_minus_prev": None if winner is None else float(cand.loc[winner, "clean_svm_minus_prev"]),
                "thresholds": {"go_delta": GO_DELTA, "clean_tol": CLEAN_TOL, "tie": TIE},
                "check_W1_equals_prev_on_target_6": w1_check, "tournament_seconds": round(time.time() - t0)}
    tab.round(6).to_csv(OUT / "tournament.csv", index=False)
    json.dump(decision, open(OUT / "r3_decision.json", "w"), indent=1)
    (OUT / "TOURNAMENT.md").write_text("\n".join([
        "# Dev tournament (decisions_log R1-R3; Drift-Dev targets 6 and 7, seeds 0-4, A under faults, k1/k2 equal)", "",
        tab.round(4).to_markdown(index=False), "", "```", json.dumps(decision, indent=1), "```", ""]), encoding="utf-8")
    log(f"tournament: winner {winner}, delta {decision['winner_delta_vs_prev']}, GO={go}")


# ---- R4: the single Test run (only on GO) -----------------------------------------------------------------------------
def test_pred_path(key, t, s):
    return OUT / "preds" / "test" / f"{key}_b{t}_s{s}.pkl"


def job_test(key, t, s):
    path = test_pred_path(key, t, s)
    if not path.exists():
        m, info = build("test", key, t, s)
        n = len(test_scenarios())
        preds = predict(m, test_data()[3][t][0], test_stats(), test_scenarios(), range(n))
        save(path, {"domain": "test", "key": key, "target": t, "seed": s, "sids": list(range(n)), "preds": preds,
                    "info": {k: v for k, v in info.items() if k != "V"}})
    return str(path)


def load_test_preds(key, t, s):
    p = pickle.load(open(test_pred_path(key, t, s), "rb"))
    assert (p["domain"], p["key"], p["target"], p["seed"], p["sids"]) == ("test", key, t, s, list(range(len(test_scenarios())))), key
    return p["preds"]


def test_gate():
    """R4 gate: saved v3 labels (provenance-checked) re-scored on the kept rows equal v3 scores.csv; v4 prediction code reproduces arm (c)."""
    v3 = pd.read_csv(V3_SCORES)
    v3 = v3[v3.subset.isin(["b9", "b10"])].set_index(["subset", "cal_seed", "arm", "method", "sid"])["f1"]
    worst, n = 0.0, 0
    for t in TEST_TARGETS:
        y = test_data()[3][t][1]
        for s in SEEDS:
            r = test_rows(t, s)
            for arm in "abc":
                P = load_v3_preds(arm, t, s)
                for m in ("svm", "A", "B"):
                    for sid in range(len(P[m])):
                        worst = max(worst, abs(scores(y[r], P[m][sid][r])["macro_f1"] - v3[(f"b{t}", s, arm, m, sid)]))
                        n += 1
    sids = [0, 1, 2, 100, 250, 400, 550, 700, 850, 950, 1000, 1080]
    label_mism = {}
    for t in TEST_TARGETS:
        got = predict(as_model(load_v2(f"b{t - 1}", 0)), test_data()[3][t][0], test_stats(), test_scenarios(), sids)
        ref = load_v3_preds("c", t, 0)
        label_mism[f"b{t}"] = {m: int((got[m] != ref[m][sids]).sum()) for m in ("svm", "A")}
    ok = worst <= 1e-9 and all(v == 0 for d in label_mism.values() for v in d.values())
    gate = {"v3_rescored_rows": n, "v3_max_abs_diff": worst, "arm_c_relabel_sids": sids, "arm_c_label_mismatches": label_mism, "passed": ok}
    json.dump(gate, open(OUT / "test" / "gate.json", "w"), indent=1)
    log(f"test gate: {n} v3 rows, max |diff| {worst:.3g}; arm (c) relabel mismatches {label_mism} -> {'PASSED' if ok else 'FAILED'}")
    return ok


def stage_test(jobs):
    marker = OUT / "test" / "RUN_STARTED"
    if marker.exists():
        raise SystemExit("refusing to run the Test stage again: RUN_STARTED exists (decisions_log R4: one run)")
    dpath = OUT / "r3_decision.json"
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(dpath)], capture_output=True).returncode == 0
    dirty = subprocess.run(["git", "status", "--porcelain", "--", str(dpath)], capture_output=True, text=True).stdout.strip()
    assert tracked and not dirty, "the R3 decision must be committed before the Test run"
    dec = json.load(open(dpath))
    if not dec["go"]:
        raise SystemExit("R3 decision is NO-GO: no Test run")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
    if not test_gate():
        raise SystemExit("R4 reproduction gate FAILED: hard stop")
    winner = dec["winner"]
    tasks = [(winner, t, s) for t in TEST_TARGETS for s in SEEDS]
    log(f"test: arm (d) = {winner}, {len(tasks)} models x {len(test_scenarios())} scenarios")
    Parallel(n_jobs=jobs, verbose=5)(delayed(worker("job_test"))(*task) for task in tasks)
    (OUT / "test" / "RUN_FINISHED").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
    test_tables(winner)


def test_tables(winner):
    rows = []
    n = len(test_scenarios())
    for s in SEEDS:
        r = {t: comparison_rows("test", winner, t, s) for t in TEST_TARGETS}
        y = {t: test_data()[3][t][1] for t in TEST_TARGETS}
        for arm in "abcd":
            P = {t: (load_test_preds(winner, t, s) if arm == "d" else load_v3_preds(arm, t, s)) for t in TEST_TARGETS}
            for m in ("svm", "A"):
                for sid in range(n):
                    for t in TEST_TARGETS:
                        rows.append((f"b{t}", s, arm, m, sid, scores(y[t][r[t]], P[t][m][sid][r[t]])["macro_f1"]))
                    rows.append(("pooled", s, arm, m, sid, scores(np.concatenate([y[t][r[t]] for t in TEST_TARGETS]),
                                                                  np.concatenate([P[t][m][sid][r[t]] for t in TEST_TARGETS]))["macro_f1"]))
    df = score_frame(rows)
    df.to_csv(OUT / "test" / "scores.csv", index=False)
    subs = ("b9", "b10", "pooled")
    primary = {"endpoint": "A under faults, (d) - (c), pooled b9+b10", **diff_boot(df, "pooled", ("d", "A"), ("c", "A")),
               "interval": "95% shared-index scenario bootstrap (k-stratified, 1000, seed 0)", "winner": winner}
    primary["verdict"] = "SUPPORTED" if primary["ci_low"] > 0 else "NOT SUPPORTED"
    levels = [{"subset": sub, "arm": a, "method": m, **level_boot(df, sub, a, m)} for sub in subs for a in "abcd" for m in ("svm", "A")]
    diffs = [{"subset": sub, "comparison": f"({x})-({y}) {m} under faults", **diff_boot(df, sub, (x, m), (y, m))}
             for sub in subs for m in ("svm", "A") for x, y in (("d", "c"), ("d", "a"), ("d", "b"), ("c", "a"))]
    diffs += [{"subset": sub, "comparison": f"A-SVM under faults, arm ({a})", **diff_boot(df, sub, (a, "A"), (a, "svm"))} for sub in subs for a in "cd"]
    clean_rows = [{"subset": sub, "comparison": f"({x})-({y}) {m} clean", **dict(zip(("value", "ci_low", "ci_high"),
                   seed_t(clean(df, sub, x, m) - clean(df, sub, y, m))))} for sub in subs for m in ("svm", "A") for x, y in (("d", "c"), ("d", "a"), ("d", "b"))]
    ret = [{"subset": sub, "arm": a, "method": m, **dict(zip(("retention_j6", "worst"), retention(df, sub, a, m)))}
           for sub in subs for a in "abcd" for m in ("svm", "A")]
    w = (df[(df.setting != "clean") & df.arm.isin(["c", "d"]) & (df.method == "A")]
         .groupby(["subset", "arm", "sid", "setting", "fault", "sensors", "level"], dropna=False).f1.mean().reset_index()
         .pivot_table(index=["subset", "sid", "setting", "fault", "sensors", "level"], columns="arm", values="f1").reset_index())
    w["d_minus_c"] = w["d"] - w["c"]
    worst = pd.concat([g.nsmallest(5, "d") for _, g in w.groupby("subset")])
    drops = pd.concat([g.nsmallest(5, "d_minus_c") for _, g in w.groupby("subset")])
    out = {"r5_primary": pd.DataFrame([primary]), "r5_levels": pd.DataFrame(levels), "r5_diffs": pd.DataFrame(diffs),
           "r5_clean": pd.DataFrame(clean_rows), "r5_retention": pd.DataFrame(ret), "r5_worst_d": worst, "r5_drops_d_vs_c": drops}
    md = [f"# R4/R5 Test run: arm (d) = {winner} (selected on Drift-Dev, evaluated once)", ""]
    for name, tab in out.items():
        tab.round(6).to_csv(OUT / "test" / f"{name}.csv", index=False)
        md += [f"## {name}", "", tab.round(4).to_markdown(index=False), ""]
    (OUT / "test" / "TABLES.md").write_text("\n".join(md), encoding="utf-8")
    log(f"test: R5 {primary['value']:+.4f} [{primary['ci_low']:+.4f}, {primary['ci_high']:+.4f}] -> {primary['verdict']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["part1", "devgate", "tournament", "test"])
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    {"part1": lambda: stage_part1(a.jobs), "devgate": lambda: stage_devgate(a.jobs), "tournament": lambda: stage_tournament(a.jobs),
     "test": lambda: stage_test(a.jobs)}[a.stage]()
