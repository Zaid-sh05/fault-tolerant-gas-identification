"""Previous-period recalibration (POST-HOC, EXPLORATORY; decisions_log Q). Batches 8-10 via configs/v3_prevbatch.yaml.

Usage (repository root):
  python scripts/v3_prevbatch.py smoke             # arms a, b on batch 9, seed 0, 12 scenarios, against the saved v2 labels
  python scripts/v3_prevbatch.py gate  [--jobs 3]  # Q5(2): arms a, b recomputed on batches 9, 10 (all scenarios) == v2 labels and scores.csv
  python scripts/v3_prevbatch.py run   [--jobs 3]  # Q5(3): arm c = v2 model b{t-1}_s{s} applied unchanged to batch t (needs a passed gate)
  python scripts/v3_prevbatch.py score             # scores.csv (b9, b10, pooled) for arms a, b, c
  python scripts/v3_prevbatch.py tables            # Q3 / Q4 tables -> results/v3_prevbatch/{q3_primary.csv, q4_*.csv, TABLES.md}
The fitted v2 models are only read. A reduced B model missing from a v2 cache is fitted by the frozen routine into results/v3_prevbatch/models.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from functools import lru_cache  # noqa: E402
from pathlib import Path  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

sys.path.insert(0, "scripts")
from ft_v2_recal import CHUNK, METHODS, SafeKit, keep_mask, scenario_list  # noqa: E402
from paper_corrections import seed_t, shared_boot  # noqa: E402
from v2_arbiter import atomic, scenario_info  # noqa: E402
from src.data import xy  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.scenarios import FaultStats, apply_scenario  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402
from src.strategies import acted_sets  # noqa: E402

CONFIG = "configs/v3_prevbatch.yaml"
V2 = Path("results/final_test_v2/test")
OUT = Path("results/v3_prevbatch")
TARGETS, SEEDS = (9, 10), (0, 1, 2, 3, 4)
SMOKE_SIDS = [0, 1, 2, 3, 4, 5, 100, 400, 700, 900, 1000, 1080]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---- data, arms, rows ------------------------------------------------------------------------------
@lru_cache(maxsize=1)
def load_data():
    """(Xtr, ytr, btr, {batch: (X, y)}) exactly as ft_v2_recal.main builds them (Train 1-7 cleaned; batches 8, 9, 10)."""
    proto = get_protocol_data(load_config(CONFIG))
    Xtr, ytr = xy(proto.train)
    return Xtr, ytr, proto.train["batch"].to_numpy(), {b: xy(proto.eval[proto.eval["batch"] == b]) for b in (8, 9, 10)}


@lru_cache(maxsize=1)
def raw_stats():
    return FaultStats.fit(load_data()[0])


def model_dir(arm, t, s):
    """(a) uncalibrated, (b) calibrated on batch t, (c) calibrated on batch t-1 (decisions_log Q2)."""
    return {"a": V2 / "uncalibrated", "b": V2 / f"b{t}_s{s}", "c": V2 / f"b{t - 1}_s{s}"}[arm]


def cache_dir(arm, t, s):
    return OUT / "models" / model_dir(arm, t, s).name / "reduced"


def scored_rows(arm, t, s, y):
    """Identical in every arm: batch t minus its seed-s calibration rows of the v2 run."""
    return np.flatnonzero(keep_mask(y, s, t))


def load_fitted(arm, t, s):
    return joblib.load(model_dir(arm, t, s) / "fitted.joblib")


def pred_dir(arm, t, s):
    return OUT / "preds" / (f"a_b{t}" if arm == "a" else f"{arm}_b{t}_s{s}")       # the uncalibrated model is the same for every seed


# ---- prediction --------------------------------------------------------------------------------------
class PrevKit(SafeKit):
    """Reduced B models: first the v2 cache of the same model (read-only), else the frozen fit routine into our own cache."""

    def __init__(self, f, cache, v2_cache):
        super().__init__(f["pre"], f["svm"], f["Xtr"], f["ytr"], f["det"], f["params"], str(cache))
        self.v2_cache = Path(v2_cache)

    def reduced_model(self, pattern):
        if pattern not in self._reduced:
            v2_path = self.v2_cache / ("B_" + ("none" if not pattern else "_".join(map(str, pattern))) + ".joblib")
            if v2_path.exists():
                self._reduced[pattern] = joblib.load(v2_path)
        return super().reduced_model(pattern)


def predict_scenarios(f, cache, X, Xtr, sids):
    """Labels of SVM, A, B on the FULL batch X for the scenarios `sids` (as ft_v2_recal.run_chunk; faults with the raw Train statistics)."""
    assert Xtr is load_data()[0], "faults must use the raw Train 1-7 statistics"
    kit = PrevKit(f, cache, V2 / Path(cache).parent.name / "reduced")
    scen = scenario_list()
    preds = {m: [] for m in METHODS}
    for sid in sids:
        sc = scen[sid]
        Xf = X if sc is None else apply_scenario(X, sc, raw_stats())[0]
        R = f["det"].ratio(Xf)
        sets = acted_sets(R, R > 1.0)
        preds["svm"].append(fast_svm_predict(f["svm"], fill_nan_zero(f["pre"].transform(Xf))))
        preds["A"].append(kit.predict_A(Xf, sets, False))
        preds["B"].append(kit.predict_B(Xf, sets))
    return {m: np.array(v, dtype=np.int8) for m, v in preds.items()}


def run_chunk(arm, t, s, index, sids):
    path = pred_dir(arm, t, s) / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    Xtr, _, _, evals = load_data()
    f = load_fitted(arm, t, s)
    out = {"arm": arm, "target": t, "seed": s, "model": str(model_dir(arm, t, s)), "sids": list(sids),
           "preds": predict_scenarios(f, cache_dir(arm, t, s), evals[t][0], Xtr, sids)}
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic(path, lambda p: pickle.dump(out, open(p, "wb")))
    return str(path)


def worker():
    """run_chunk of the imported module: pickled by reference, because the lru_cache globals of __main__ do not reach loky workers."""
    import v3_prevbatch
    return v3_prevbatch.run_chunk


def chunks():
    n = len(scenario_list())
    return [(i, list(range(a, min(a + CHUNK, n)))) for i, a in enumerate(range(0, n, CHUNK))]


def jobs_for(arms):
    keys = {(arm, t, 0 if arm == "a" else s) for arm in arms for t in TARGETS for s in SEEDS}
    return [(arm, t, s, i, sids) for arm, t, s in sorted(keys) for i, sids in chunks()]


def load_preds(arm, t, s):
    d = pred_dir(arm, t, s)
    parts = [pickle.load(open(d / f"chunk_{i:03d}.pkl", "rb")) for i, _ in chunks()]
    for p, (_, sids) in zip(parts, chunks()):                                    # provenance: a stale chunk is never reused silently
        assert (p["arm"], p["target"], p["model"], p["sids"]) == (arm, t, str(model_dir(arm, t, s)), sids), f"bad chunk in {d}"
    return {m: np.concatenate([p["preds"][m] for p in parts]) for m in METHODS}


def v2_preds(arm, t, s, index=None):
    d = model_dir(arm, t, s) / f"b{t}_chunks"
    idx = [i for i, _ in chunks()] if index is None else [index]
    parts = [pickle.load(open(d / f"chunk_{i:03d}.pkl", "rb")) for i in idx]
    return {m: np.concatenate([p["preds"][m] for p in parts]) for m in METHODS}


# ---- stages ------------------------------------------------------------------------------------------
def stage_smoke():
    Xtr, _, _, evals = load_data()
    res = {}
    for arm in ("a", "b"):
        got = predict_scenarios(load_fitted(arm, 9, 0), cache_dir(arm, 9, 0), evals[9][0], Xtr, SMOKE_SIDS)
        ref = v2_preds(arm, 9, 0)
        res[arm] = {m: int((got[m] != ref[m][SMOKE_SIDS]).sum()) for m in METHODS}
    ok = all(v == 0 for r in res.values() for v in r.values())
    json.dump({"sids": SMOKE_SIDS, "label_mismatches": res, "passed": ok}, open(OUT / "smoke.json", "w"), indent=1)
    log(f"smoke: label mismatches {res} -> {'PASSED' if ok else 'FAILED'}")
    if not ok:
        raise SystemExit(1)


def score_rows(arms):
    """Macro-F1 per (subset, seed, arm, method, sid) on the scored rows; pooled = union of the scored rows of batches 9 and 10."""
    evals = load_data()[3]
    rows = []
    for s in SEEDS:
        keep = {t: scored_rows("a", t, s, evals[t][1]) for t in TARGETS}
        y_pool = np.concatenate([evals[t][1][keep[t]] for t in TARGETS])
        for arm in arms:
            P = {t: load_preds(arm, t, s) for t in TARGETS}
            for m in METHODS:
                for sid in range(len(scenario_list())):
                    for t in TARGETS:
                        rows.append((f"b{t}", s, arm, m, sid, scores(evals[t][1][keep[t]], P[t][m][sid][keep[t]])["macro_f1"]))
                    yp = np.concatenate([P[t][m][sid][keep[t]] for t in TARGETS])
                    rows.append(("pooled", s, arm, m, sid, scores(y_pool, yp)["macro_f1"]))
    df = pd.DataFrame(rows, columns=["subset", "cal_seed", "arm", "method", "sid", "f1"])
    info = pd.DataFrame([{"sid": i, **scenario_info(sc), "level": (np.nan if sc is None else sc.level)} for i, sc in enumerate(scenario_list())])
    return df.merge(info, on="sid")


def stage_gate(jobs):
    tasks = jobs_for(("a", "b"))
    log(f"gate: {len(tasks)} chunks (arms a, b; batches 9, 10)")
    Parallel(n_jobs=jobs, verbose=5)(delayed(worker())(*task) for task in tasks)
    mism = {}
    for arm, t, s in sorted({(a, t, s) for a, t, s, _, _ in tasks}):
        got, ref = load_preds(arm, t, s), v2_preds(arm, t, s)
        mism[f"{arm}_b{t}_s{s}"] = {m: int((got[m] != ref[m]).sum()) for m in METHODS}
    labels_ok = all(v == 0 for r in mism.values() for v in r.values())
    df = score_rows(("a", "b"))
    df = df[df.subset != "pooled"]
    v2 = pd.read_csv(V2 / "scores.csv")
    v2 = v2[v2.subset.isin(["b9", "b10"])].rename(columns={"model": "arm"})
    m = df.merge(v2[["subset", "cal_seed", "arm", "method", "sid", "f1"]], on=["subset", "cal_seed", "arm", "method", "sid"], suffixes=("", "_v2"))
    f1_diff = float((m.f1 - m.f1_v2).abs().max())
    clean = pd.read_csv(V2 / "clean.csv")
    ours = df[df.setting == "clean"].groupby(["subset", "arm", "method"]).f1.mean().unstack("arm").reset_index()
    cm = ours.merge(clean, on=["subset", "method"], suffixes=("", "_v2"))
    clean_diff = float(max((cm["a"].round(4) - cm["a_v2"]).abs().max(), (cm["b"].round(4) - cm["b_v2"]).abs().max()))  # clean.csv has 4 decimals
    ok = labels_ok and len(m) == len(df) and f1_diff <= 1e-9 and clean_diff == 0 and len(cm) == 6
    gate = {"label_mismatches": mism, "labels_identical": labels_ok, "f1_rows_compared": len(m), "f1_rows_ours": len(df),
            "f1_max_abs_diff": f1_diff, "clean_csv_rows_compared": len(cm), "clean_max_abs_diff_at_4_decimals": clean_diff, "passed": ok}
    json.dump(gate, open(OUT / "gate.json", "w"), indent=1)
    log(f"gate: labels identical={labels_ok}, F1 rows {len(m)}/{len(df)}, max |dF1|={f1_diff:.3g}, clean max |d|={clean_diff:.3g} -> "
        f"{'PASSED' if ok else 'FAILED'}")
    if not ok:
        raise SystemExit(1)


def stage_run(jobs):
    gate = json.load(open(OUT / "gate.json"))
    assert gate["passed"], "the reproduction gate has not passed (decisions_log Q5)"
    if (OUT / "RUN_STARTED").exists() and not os.environ.get("V3_RESUME"):
        raise SystemExit("refusing to start again: RUN_STARTED exists (resume after an interruption: V3_RESUME=1, logged)")
    (OUT / "RUN_STARTED").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
    tasks = jobs_for(("c",))
    log(f"run: arm c, {len(tasks)} chunks")
    t0 = time.time()
    Parallel(n_jobs=jobs, verbose=5)(delayed(worker())(*task) for task in tasks)
    new_fits = {d.parent.name: len(list(d.glob("B_*.joblib"))) for d in sorted((OUT / "models").glob("*/reduced"))}
    (OUT / "RUN_FINISHED").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
    json.dump({"seconds": round(time.time() - t0), "new_reduced_models": new_fits}, open(OUT / "run_info.json", "w"), indent=1)
    log(f"run: finished in {time.time() - t0:.0f} s; new reduced B models fitted (frozen routine): {new_fits}")


def stage_score():
    df = score_rows(("a", "b", "c"))
    df.to_csv(OUT / "scores.csv", index=False)
    log(f"score: {len(df)} rows")


# ---- tables (decisions_log Q3, Q4) -------------------------------------------------------------------------
SUBSETS = ("b9", "b10", "pooled")


def tables():
    df = pd.read_csv(OUT / "scores.csv")
    clean = df[df.setting == "clean"].pivot_table(index=["subset", "cal_seed", "method"], columns="arm", values="f1").reset_index()
    f = df[df.setting != "clean"].sort_values(["subset", "arm", "method", "cal_seed", "sid"])

    def ps(sub, arm, m):
        g = f[(f.subset == sub) & (f.arm == arm) & (f.method == m)]
        assert all(np.array_equal(g[g.cal_seed == s]["sid"].to_numpy(), np.arange(1, len(scenario_list()))) for s in SEEDS), (sub, arm, m)
        return np.stack([g[g.cal_seed == s]["f1"].to_numpy() for s in SEEDS]), g[g.cal_seed == 0]["setting"].to_numpy()

    def boot(x, k):
        return dict(zip(("value", "ci_low", "ci_high"), shared_boot(x, k)))

    k = ps("pooled", "a", "A")[1]
    q3 = {"endpoint": "A under faults, arm (c) - arm (a), pooled b9+b10", **boot(ps("pooled", "c", "A")[0] - ps("pooled", "a", "A")[0], k),
          "interval": "95% shared-index scenario bootstrap (k-stratified, 1000, seed 0)"}
    q3["verdict"] = "SUPPORTED" if q3["ci_low"] > 0 else "NOT SUPPORTED"

    lev, diff, cln, ret = [], [], [], []
    for sub in SUBSETS:
        for m in METHODS:
            for arm in ("a", "b", "c"):
                lev.append({"subset": sub, "method": m, "arm": arm, **boot(ps(sub, arm, m)[0], k)})
            for x, y in (("c", "a"), ("b", "a"), ("c", "b")):
                diff.append({"subset": sub, "comparison": f"({x})-({y}) {m} under faults", **boot(ps(sub, x, m)[0] - ps(sub, y, m)[0], k)})
                g = clean[(clean.subset == sub) & (clean.method == m)]
                cln.append({"subset": sub, "comparison": f"({x})-({y}) {m} clean", **dict(zip(("value", "ci_low", "ci_high"), seed_t(g[x] - g[y])))})
            for arm in ("a", "b", "c"):
                g = clean[(clean.subset == sub) & (clean.method == m)]
                cln.append({"subset": sub, "comparison": f"({arm}) {m} clean", **dict(zip(("value", "ci_low", "ci_high"), seed_t(g[arm])))})
                per_seed = []
                for s in SEEDS:
                    gs = f[(f.subset == sub) & (f.arm == arm) & (f.method == m) & (f.cal_seed == s)]
                    c = clean[(clean.subset == sub) & (clean.cal_seed == s) & (clean.method == m)][arm].iloc[0]
                    r = gs["f1"] / c
                    per_seed.append((np.mean([r[gs.setting == kk].mean() for kk in ("k1", "k2")]), r.mean(), min(gs["f1"].min(), c)))
                ret.append({"subset": sub, "method": m, "arm": arm, "retention": np.mean([x[0] for x in per_seed]),    # J6: k1, k2 equal
                            "retention_unweighted_v2_tables": np.mean([x[1] for x in per_seed]),                    # as ft_v2_tables
                            "worst": np.mean([x[2] for x in per_seed])})
        for arm in ("a", "b", "c"):
            for m in ("A", "B"):
                diff.append({"subset": sub, "comparison": f"{m}-SVM under faults, arm ({arm})", **boot(ps(sub, arm, m)[0] - ps(sub, arm, "svm")[0], k)})
    lev, diff, cln, ret = (pd.DataFrame(x) for x in (lev, diff, cln, ret))
    share = []
    for sub in SUBSETS:
        for m in METHODS:
            v = {x: lev[(lev.subset == sub) & (lev.method == m) & (lev.arm == x)]["value"].iloc[0] for x in "abc"}
            share.append({"subset": sub, "method": m, "c_minus_a": v["c"] - v["a"], "b_minus_a": v["b"] - v["a"],
                          "share_of_same_period_gain_kept": (v["c"] - v["a"]) / (v["b"] - v["a"]) if v["b"] != v["a"] else np.nan})
    share = pd.DataFrame(share)
    worst = (f[f.arm.isin(["a", "c"]) & f.method.isin(["A", "B"])]
             .groupby(["subset", "arm", "method", "sid", "setting", "fault", "sensors", "level"], dropna=False).f1.mean().reset_index())
    w = worst.pivot_table(index=["subset", "method", "sid", "setting", "fault", "sensors", "level"], columns="arm", values="f1").reset_index()
    w["c_minus_a"] = w["c"] - w["a"]
    worst_c = pd.concat([g.nsmallest(5, "c") for _, g in w.groupby(["subset", "method"])])
    breaks = pd.concat([g.nsmallest(5, "c_minus_a") for _, g in w.groupby(["subset", "method"])])
    by_fault = (w.groupby(["subset", "method", "setting", "fault"]).agg(a=("a", "mean"), c=("c", "mean"), c_minus_a=("c_minus_a", "mean"),
                                                                     frac_c_below_a=("c_minus_a", lambda x: float((x < 0).mean())))
                .reset_index())
    out = {"q3_primary": pd.DataFrame([q3]), "q4_levels_faults": lev, "q4_diffs_faults": diff, "q4_clean": cln, "q4_retention_worst": ret,
           "q4_share_kept": share, "q4_worst_scenarios_c": worst_c, "q4_largest_drops_c_vs_a": breaks, "q4_by_fault_c_vs_a": by_fault}
    for name, tab in out.items():
        tab.round(6).to_csv(OUT / f"{name}.csv", index=False)
    md = ["# Previous-period recalibration: tables (POST-HOC, EXPLORATORY; decisions_log Q)", "",
          "Arms on identical rows: (a) uncalibrated, (b) calibrated on batch t, (c) calibrated on batch t-1. Under faults = k1/k2 weighted "
          "equally, mean over 5 calibration seeds; intervals: 95% shared-index scenario bootstrap (faults), 95% t over seeds (clean).", ""]
    for name, tab in out.items():
        md += [f"## {name}", "", tab.round(4).to_markdown(index=False), ""]
    (OUT / "TABLES.md").write_text("\n".join(md), encoding="utf-8")
    log(f"tables: Q3 {q3['value']:+.4f} [{q3['ci_low']:+.4f}, {q3['ci_high']:+.4f}] -> {q3['verdict']}")


def paper_numbers():
    """results/paper/PAPER_NUMBERS_v3.md: every v3 number with its file, filter and column (read from the CSVs, never typed)."""
    rows = []

    def add(name, path, filt, col):
        tab = pd.read_csv(OUT / path)
        sel = tab
        for k, v in filt.items():
            sel = sel[sel[k] == v]
        assert len(sel) == 1, (path, filt)
        rows.append(f"| {name} | {sel[col].iloc[0]:.4f} | results/v3_prevbatch/{path}, "
                    + (", ".join(f"{k}={v}" for k, v in filt.items()) or "single row") + f", column {col} |")

    for col in ("value", "ci_low", "ci_high"):
        add(f"v3 primary (Q3): A under faults (c)-(a), pooled b9+b10, {col}", "q3_primary.csv", {}, col)
    for path, key in (("q4_levels_faults.csv", ("subset", "method", "arm")), ("q4_diffs_faults.csv", ("subset", "comparison")),
                      ("q4_clean.csv", ("subset", "comparison"))):
        tab = pd.read_csv(OUT / path)
        for _, r in tab.iterrows():
            filt = {k: r[k] for k in key}
            label = ("Macro-F1 under faults, " if path.startswith("q4_levels") else "") + ", ".join(str(r[k]) for k in key)
            for col in ("value", "ci_low", "ci_high"):
                add(f"v3 {label}, {col}", path, filt, col)
    for _, r in pd.read_csv(OUT / "q4_share_kept.csv").iterrows():
        for col in ("c_minus_a", "b_minus_a", "share_of_same_period_gain_kept"):
            add(f"v3 under faults {r.method}, {r.subset}, {col}", "q4_share_kept.csv", {"subset": r.subset, "method": r.method}, col)
    for _, r in pd.read_csv(OUT / "q4_retention_worst.csv").iterrows():
        for col in ("retention", "retention_unweighted_v2_tables", "worst"):
            add(f"v3 {col}, {r.method}, arm ({r.arm}), {r.subset}", "q4_retention_worst.csv",
                {"subset": r.subset, "method": r.method, "arm": r.arm}, col)
    md = ["# Numbers of the previous-period recalibration (v3; POST-HOC, EXPLORATORY; decisions_log Q)", "",
          "Every value is read from a result file by `python scripts/v3_prevbatch.py paper`; nothing is typed by hand. Arms on identical rows: "
          "(a) uncalibrated, (b) calibrated on batch t, (c) calibrated on batch t-1, scored on batch t in {9, 10}. Under faults = k1/k2 weighted "
          "equally, mean over 5 calibration seeds. Intervals: 95% shared-index scenario bootstrap (faults; resamples scenarios only, O2) and 95% "
          "t over the 5 seeds (clean).", "", "| number | value | source |", "|---|---|---|"] + rows
    Path("results/paper/PAPER_NUMBERS_v3.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    log(f"paper: {len(rows)} numbers -> results/paper/PAPER_NUMBERS_v3.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["smoke", "gate", "run", "score", "tables", "paper"])
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    {"smoke": stage_smoke, "gate": lambda: stage_gate(a.jobs), "run": lambda: stage_run(a.jobs), "score": stage_score, "tables": tables, "paper": paper_numbers}[a.stage]()
