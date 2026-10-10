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
import pickle  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from functools import lru_cache  # noqa: E402
from pathlib import Path, PureWindowsPath  # noqa: E402
from types import SimpleNamespace  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

sys.path.insert(0, "scripts")
from ft_v2_recal import keep_mask, scenario_list as test_scenarios  # noqa: E402
from paper_corrections import seed_t, shared_boot  # noqa: E402
from v2_arbiter import atomic, scenario_info  # noqa: E402
from src.data import xy  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.scenarios import FaultStats, apply_scenario  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402
from src.strategies import StrategyKit, acted_sets, group_by_set  # noqa: E402

CFG = load_config("configs/v4_recal.yaml")
MAIN = Path(CFG["main_checkout"])
V2 = MAIN / CFG["v2_models"]                      # read-only
V3_PREDS = MAIN / CFG["v3_preds"]                 # read-only
V3_SCORES = Path("results/v3_prevbatch/scores.csv")
OUT = Path(CFG["output_root"])
SEEDS = tuple(CFG["seeds"])
V3_CHUNK = 40
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["part1"])
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    {"part1": lambda: stage_part1(a.jobs)}[a.stage]()
