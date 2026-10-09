"""Final Test v2: few-shot recalibration, ONE run (POST-HOC design, decisions_log N0-N10).

Usage:
  python scripts/ft_v2_recal.py --config configs/final_test_v2.yaml [--jobs 3]           # the single Test run (needs tag frozen-before-test-v2)
  python scripts/ft_v2_recal.py --config configs/v2_drift_dev.yaml --smoke                # N6: Drift-Dev batch 6, seed 0, medium scenarios
Per evaluation batch: (a) M0 on the Train rows, (b) M0 on Train + the batch's calibration rows (seed); both scored on the SAME remaining rows.
SVM (no handling), A and B with the "median" detector (stage-2 recipe, J3/N2). Faults on the full raw batch, raw Train statistics.
Outputs in <output_root>/test (or results/v2/ft_smoke): fitted models, prediction chunks, scores.csv, detector.csv, tables, verdict.json.
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
from pathlib import Path  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

sys.path.insert(0, "scripts")
from ov3_detector import auc  # noqa: E402
from v2_arbiter import atomic, scenario_info  # noqa: E402
from v2_recal import CAL_GROUP, calib_rows  # noqa: E402
from src.data import xy  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.preprocessing import fit_preprocessor  # noqa: E402
from src.scenarios import MEDIUM, FaultStats, apply_scenario, build_scenarios  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402
from src.strategies import StrategyKit, acted_sets  # noqa: E402
from src.study import AUG_SEEDS, OVERNIGHT  # noqa: E402

N_CAL, CHUNK, B_BOOT = 10, 40, 1000
METHODS = ("svm", "A", "B")
TAG = "frozen-before-test-v2"


def scenario_list(medium_only=False):
    sc = build_scenarios(AUG_SEEDS, ("k1", "k2"))
    return [None] + [s for s in sc if not medium_only or s.level == MEDIUM[s.fault]]


def keep_mask(y, seed, batch):
    keep = np.ones(len(y), bool)
    keep[calib_rows(y, N_CAL, seed, batch)] = False
    return keep


def fit_model(Xtr, ytr, btr, path):
    """Stage-2 recipe (N2) without Platt probabilities: preprocessing, SVM, median detector."""
    if path.exists():
        return
    fin = json.load(open(OVERNIGHT / "final_pipeline.json"))
    pre = fit_preprocessor(fin["spec"], Xtr, ytr, btr, fill_nan=False)
    svm = SVC(kernel="rbf", random_state=0, **fin["svm_params"]).fit(fill_nan_zero(pre.transform(Xtr)), ytr)
    obj = {"pre": pre, "svm": svm, "det": ReliabilityDetector(normalization="median").fit(Xtr, btr), "Xtr": Xtr, "ytr": ytr,
           "params": fin["svm_params"]}
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic(path, lambda p: joblib.dump(obj, p))


def run_chunk(model_dir, batch, X, y, masks, raw_stats, index, sids, medium_only):
    """Per-row labels of SVM, A, B for the scenarios `sids` on the full batch X; detector metrics on each scoring mask.
    The reduced B models are cached once per model (model_dir/reduced); chunks per batch (model_dir/b<batch>_chunks)."""
    path = model_dir / f"b{batch}_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    f = joblib.load(model_dir / "fitted.joblib")
    kit = StrategyKit(f["pre"], f["svm"], f["Xtr"], f["ytr"], f["det"], f["params"], str(model_dir / "reduced"))
    scen = scenario_list(medium_only)
    preds, det_rows = {m: [] for m in METHODS}, []
    for sid in sids:
        sc = scen[sid]
        Xf, truth = (X, np.zeros((len(X), 16), bool)) if sc is None else apply_scenario(X, sc, raw_stats)
        R = f["det"].ratio(Xf)
        flags = R > 1.0
        sets = acted_sets(R, flags)
        preds["svm"].append(fast_svm_predict(f["svm"], fill_nan_zero(f["pre"].transform(Xf))))
        preds["A"].append(kit.predict_A(Xf, sets, False))
        preds["B"].append(kit.predict_B(Xf, sets))
        for mi, keep in enumerate(masks):
            t, h = truth & keep[:, None], (~truth & truth.any(1)[:, None]) & keep[:, None]
            det_rows.append({"sid": sid, "mask": mi, "auroc": auc(R[t], R[h]) if sc is not None else np.nan,
                             "tpr": float(flags[t].mean()) if sc is not None else np.nan,
                             "far_clean": float(flags[keep].mean()) if sc is None else np.nan,
                             "rows_with_alarm_clean": float(flags[keep].any(1).mean()) if sc is None else np.nan})
    out = {"sids": list(sids), "preds": {m: np.array(v, dtype=np.int8) for m, v in preds.items()}, "det": det_rows}
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic(path, lambda p: pickle.dump(out, open(p, "wb")))
    return str(path)


def load_preds(model_dir, batch, n_chunks):
    parts = [pickle.load(open(model_dir / f"b{batch}_chunks" / f"chunk_{i:03d}.pkl", "rb")) for i in range(n_chunks)]
    return ({m: np.concatenate([p["preds"][m] for p in parts]) for m in METHODS},
            pd.DataFrame([r for p in parts for r in p["det"]]))


def check_frozen(cfg_path):
    tags = subprocess.run(["git", "tag", "--points-at", "HEAD"], capture_output=True, text=True).stdout.split()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "scripts", "src", "configs"], capture_output=True, text=True).stdout.strip()
    assert TAG in tags, f"HEAD is not tagged {TAG}: the Test run needs the frozen commit (decisions_log N10)"
    assert not dirty, f"uncommitted changes in scripts/src/configs: {dirty[:200]}"


def main(cfg_path, jobs, smoke):
    cfg = load_config(cfg_path)
    is_test = cfg["split"].get("type") == "final_test"
    if is_test:
        assert not smoke
        check_frozen(cfg_path)
        out = Path(cfg["output_root"]) / "test"
        out.mkdir(parents=True, exist_ok=True)
        marker = out / "RUN_STARTED"
        if marker.exists() and not os.environ.get("FT_V2_RESUME"):
            raise SystemExit(f"refusing to start again: {marker} exists (resume after an interruption: FT_V2_RESUME=1, logged)")
        marker.write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
        seeds = tuple(cfg["recalibration"]["seeds"])
    else:
        assert smoke, "a non-Test config is only used for the smoke test"
        out, seeds = Path("results/v2/ft_smoke"), (0,)
    proto = get_protocol_data(cfg)                                                  # Test batches are read here, once (step 5)
    Xtr, ytr = xy(proto.train)
    btr = proto.train["batch"].to_numpy()
    batches = [6] if smoke else sorted(int(b) for b in proto.eval["batch"].unique())
    evals = {b: xy(proto.eval[proto.eval["batch"] == b]) for b in batches}
    raw_stats = FaultStats.fit(Xtr)
    medium_only = smoke
    n_sc = len(scenario_list(medium_only))
    chunks = [(i, list(range(a, min(a + CHUNK, n_sc)))) for i, a in enumerate(range(0, n_sc, CHUNK))]

    configs = [("uncal", None, None)] + [("cal", b, s) for b in batches for s in seeds]
    def model_dir(kind, b, s):                                                       # noqa: E306
        return out / ("uncalibrated" if kind == "uncal" else f"b{b}_s{s}")

    def train_rows(kind, b, s):
        if kind == "uncal":
            return Xtr, ytr, btr
        X, y = evals[b]
        cal = calib_rows(y, N_CAL, s, b)
        return np.vstack([Xtr, X[cal]]), np.r_[ytr, y[cal]], np.r_[btr, np.full(len(cal), CAL_GROUP + b)]
    Parallel(n_jobs=jobs, verbose=5)(delayed(fit_model)(*train_rows(k, b, s), model_dir(k, b, s) / "fitted.joblib") for k, b, s in configs)
    print("fitted", len(configs), "models", flush=True)

    tasks = []
    for b in batches:
        X, y = evals[b]
        tasks += [delayed(run_chunk)(model_dir("uncal", None, None), b, X, y, [keep_mask(y, s, b) for s in seeds], raw_stats, i, sids,
                                     medium_only) for i, sids in chunks]
        for s in seeds:
            tasks += [delayed(run_chunk)(model_dir("cal", b, s), b, X, y, [keep_mask(y, s, b)], raw_stats, i, sids, medium_only)
                      for i, sids in chunks]
    Parallel(n_jobs=jobs, verbose=5)(tasks)
    print("scenarios done", flush=True)
    score(out, batches, seeds, evals, n_sc, len(chunks), medium_only)


def score(out, batches, seeds, evals, n_sc, n_chunks, medium_only):
    scen = scenario_list(medium_only)
    info = pd.DataFrame([{"sid": i, **scenario_info(sc), "level": (np.nan if sc is None else sc.level)} for i, sc in enumerate(scen)])
    rows, det, clean_rows = [], [], {}                     # clean_rows[(subset, seed)] = (y, {(model, method): labels})
    unc = {b: load_preds(out / "uncalibrated", b, n_chunks) for b in batches}
    for si, s in enumerate(seeds):
        pooled = {model: {m: [] for m in METHODS} for model in ("a", "b")}
        pooled_y = []
        for b in batches:
            X, y = evals[b]
            keep = keep_mask(y, s, b)
            cal_preds, cal_det = load_preds(out / f"b{b}_s{s}", b, n_chunks)
            for model, P in (("a", unc[b][0]), ("b", cal_preds)):
                for m in METHODS:
                    for sid in range(n_sc):
                        rows.append({"subset": f"b{b}", "cal_seed": s, "model": model, "method": m, "sid": sid,
                                     "f1": scores(y[keep], P[m][sid][keep])["macro_f1"]})
                    pooled[model][m].append(P[m][:, keep])
                    clean_rows.setdefault((f"b{b}", s), (y[keep], {}))[1][(model, m)] = P[m][0][keep]
            pooled_y.append(y[keep])
            for model, D in (("a", unc[b][1][unc[b][1]["mask"] == si]), ("b", cal_det)):
                det.append(D.assign(subset=f"b{b}", cal_seed=s, model=model))
        if len(batches) > 1:
            yp = np.concatenate(pooled_y)
            for model in ("a", "b"):
                for m in METHODS:
                    P = np.concatenate(pooled[model][m], axis=1)
                    for sid in range(n_sc):
                        rows.append({"subset": "pooled", "cal_seed": s, "model": model, "method": m, "sid": sid,
                                     "f1": scores(yp, P[sid])["macro_f1"]})
                    clean_rows.setdefault(("pooled", s), (yp, {}))[1][(model, m)] = P[0]
    df = pd.DataFrame(rows).merge(info, on="sid")
    df.to_csv(out / "scores.csv", index=False)
    pd.concat(det).merge(info, on="sid").to_csv(out / "detector.csv", index=False)
    print("scored", len(df), "rows", flush=True)
    ci = []                                                                          # N5: paired row bootstrap of (b)-(a), clean rows
    for sub in sorted({k[0] for k in clean_rows}):
        for m in METHODS:
            boots, points = [], []
            for s in seeds:
                yk, P = clean_rows[(sub, s)]
                rng = np.random.default_rng(s)
                f = lambda idx, mod: scores(yk[idx], P[(mod, m)][idx])["macro_f1"]  # noqa: E731
                allr = np.arange(len(yk))
                points.append(f(allr, "b") - f(allr, "a"))
                boots.append([f(i, "b") - f(i, "a") for i in (rng.integers(0, len(yk), len(yk)) for _ in range(B_BOOT))])
            bm = np.mean(boots, axis=0)
            ci.append({"subset": sub, "method": m, "diff": float(np.mean(points)), "ci_low": float(np.percentile(bm, 2.5)),
                       "ci_high": float(np.percentile(bm, 97.5))})
    pd.DataFrame(ci).to_csv(out / "clean_ci.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    main(a.config, a.jobs, a.smoke)
