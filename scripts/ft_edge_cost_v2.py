"""Edge cost of v2 (few-shot recalibration), same method as scripts/ft_edge_cost.py. Train 1-6 and Validation 7 only (no Test data).

Usage: python scripts/ft_edge_cost_v2.py            (run on an otherwise idle machine; a few minutes)
Outputs: results/edge_cost/edge_cost_v2.json and edge_cost_v2.md
The deployment is simulated on Validation batch 7: 10 labeled rows per gas (calibration seed 0, the v2 sampling function) are added to the
Train rows and everything is refitted, exactly the v2 recipe. Measured in a FRESH process pinned to one CPU core with one BLAS thread:
  * calibration step: refit of preprocessing + SVM, of the detector, and of the 136 reduced B models that cover every k=1 and k=2 exclusion set
    (16 single sensors + 120 pairs); the Train rows must be available for this (their size is reported);
  * size (pickles, float64) of the calibrated SVM, of A's extra parts (detector without training-only arrays), of the 136 B models;
  * single-sample latency, median and 95th percentile over 1000 runs after 50 warm-up runs, on non-calibration rows of batch 7:
    SVM only; A (detector -> flags -> reconstruction -> SVM) fault-free and with a Bias fault on one sensor; B (detector -> reduced SVM of the
    flagged set; the set is limited to its two highest-ratio sensors so that it is one of the 136 covered sets);
  * peak working set of that process.
This is a laptop CPU, not an edge board: the numbers are an upper bound on the algorithmic work.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import ctypes  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, "scripts")
from ft_edge_cost import RUNS, WARMUP, memory_mb  # noqa: E402

OUT = Path("results/edge_cost")


def kb(obj):
    return len(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)) / 1024


def child(data_path, out_path):
    ctypes.windll.kernel32.SetProcessAffinityMask(ctypes.windll.kernel32.GetCurrentProcess(), 1)       # one core
    from sklearn.svm import SVC  # noqa: E402
    from src.detector import ReliabilityDetector  # noqa: E402
    from src.evaluate import fill_nan_zero  # noqa: E402
    from src.fastsvm import fast_svm_predict  # noqa: E402
    from src.preprocessing import fit_preprocessor  # noqa: E402
    from src.strategies import StrategyKit, acted_sets  # noqa: E402
    before = memory_mb()[0]
    d = np.load(data_path, allow_pickle=True)
    spec, params = json.loads(str(d["spec"])), json.loads(str(d["params"]))
    X, y, g = d["Xc"], d["yc"], d["gc"]
    out = {"memory_after_imports_mb": before, "train_rows_for_calibration": int(len(X)),
           "train_data_kb_float64": X.nbytes / 1024}

    # ---- calibration step (one core) ---------------------------------------------------------------------------------------
    t = time.perf_counter()
    pre = fit_preprocessor(spec, X, y, g, fill_nan=False)
    svm = SVC(kernel="rbf", random_state=0, **params).fit(fill_nan_zero(pre.transform(X)), y)
    out["calibration_svm_s"] = time.perf_counter() - t
    t = time.perf_counter()
    det = ReliabilityDetector(normalization="median").fit(X, g)
    out["calibration_detector_s"] = time.perf_counter() - t
    with tempfile.TemporaryDirectory() as cache:
        kit = StrategyKit(pre, svm, X, y, det, params, cache)
        sets = [(s,) for s in range(16)] + list(itertools.combinations(range(16), 2))
        t = time.perf_counter()
        reduced = {s: kit.reduced_model(s) for s in sets}
        out["calibration_B_136_models_s"] = time.perf_counter() - t
    out["calibration_total_s"] = out["calibration_svm_s"] + out["calibration_detector_s"] + out["calibration_B_136_models_s"]

    # ---- sizes ------------------------------------------------------------------------------------------------------------------
    slim = __import__("copy").copy(det)
    for attr in ("Gb_", "nb_", "batch_ids_", "E_oof_"):
        delattr(slim, attr)
    out["size_kb"] = {"svm_calibrated": kb(svm), "preprocessing": kb(pre), "detector_for_A": kb(slim),
                      "B_136_reduced_models": sum(kb(m) for m in reduced.values())}
    out["size_kb"]["A_bundle_svm_pre_detector"] = out["size_kb"]["svm_calibrated"] + out["size_kb"]["preprocessing"] + out["size_kb"]["detector_for_A"]
    out["size_kb"]["B_bundle_pre_detector_136_models"] = (out["size_kb"]["preprocessing"] + out["size_kb"]["detector_for_A"]
                                                          + out["size_kb"]["B_136_reduced_models"])

    # ---- latency ----------------------------------------------------------------------------------------------------------------
    kit.det = slim
    keep_cols = {s: kit.keep_columns(s) for s in sets}

    def svm_only(x):
        return fast_svm_predict(svm, fill_nan_zero(pre.transform(x)))

    def pipeline_a(x):
        R = slim.ratio(x)
        return kit.predict_A(x, acted_sets(R, R > 1.0), False)

    def pipeline_b(x):
        R = slim.ratio(x)[0]
        f = np.flatnonzero(R > 1.0)
        z = fill_nan_zero(pre.transform(x))
        if not len(f):
            return fast_svm_predict(svm, z)
        s = tuple(sorted(f[np.argsort(-R[f])[:2]].tolist()))
        return fast_svm_predict(reduced[s], z[:, keep_cols[s]])

    cases = [("svm_only_fault_free", svm_only, "clean"), ("A_fault_free", pipeline_a, "clean"), ("A_bias_one_sensor", pipeline_a, "bias"),
             ("B_fault_free", pipeline_b, "clean"), ("B_bias_one_sensor", pipeline_b, "bias")]
    for name, fn, kind in cases:
        Xs = d[kind]
        for i in range(WARMUP):
            fn(Xs[i:i + 1])
        ms = []
        for i in range(RUNS):
            t = time.perf_counter_ns()
            fn(Xs[i:i + 1])
            ms.append((time.perf_counter_ns() - t) / 1e6)
        out[name] = {"runs": RUNS, "median_ms": float(np.median(ms)), "p95_ms": float(np.percentile(ms, 95))}
    out["memory_final_mb"], out["memory_peak_mb"] = memory_mb()
    json.dump(out, open(out_path, "w"))


def parent():
    from src.scenarios import Scenario, apply_scenario
    from src.study import Study
    from v2_recal import CAL_GROUP, calib_rows
    study = Study("configs/preprocessing.yaml", "temporal")                    # Train 1-6 and Validation 7 only
    cal = calib_rows(study.yev, 10, 0, 7)
    rest = np.setdiff1d(np.arange(len(study.Xev)), cal)
    rows = np.random.default_rng(0).choice(rest, RUNS + WARMUP, replace=False)
    sensors = np.arange(len(rows)) % 16
    bias = np.empty((len(rows), 128))
    for s in range(16):                                                      # Bias, medium severity, one sensor per row
        Xf, _ = apply_scenario(study.Xev, Scenario(0, "k1", (s,), "bias", 1.0, 0), study.stats)
        bias[sensors == s] = Xf[rows[sensors == s]]
    with tempfile.TemporaryDirectory() as tmp:
        data, res = Path(tmp) / "data.npz", Path(tmp) / "res.json"
        np.savez(data, Xc=np.vstack([study.Xtr, study.Xev[cal]]), yc=np.r_[study.ytr, study.yev[cal]],
                 gc=np.r_[study.proto.groups, np.full(len(cal), CAL_GROUP + 7)], clean=study.Xev[rows], bias=bias,
                 spec=json.dumps(study.spec), params=json.dumps({k: study.svm_params[k] for k in ("C", "gamma")}))
        subprocess.run([sys.executable, __file__, "--child", str(data), str(res)], check=True)
        r = json.load(open(res))
    r["calibration_rows"] = int(len(cal))
    r["note"] = ("v2 deployment simulated on Validation batch 7 (calibration seed 0, 10 rows per gas); one core, one BLAS thread, laptop CPU; "
                 "pickled float64 sizes. B covers every k=1 and k=2 exclusion set (136 models); its latency uses the two highest-ratio flagged sensors.")
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(r, open(OUT / "edge_cost_v2.json", "w"), indent=1)
    s = r["size_kb"]
    md = ["# Edge cost of v2 (few-shot recalibration)", "",
          "| part | size (KB) |", "|---|---|"] + [f"| {k} | {v:.0f} |" for k, v in s.items()] + [
          f"| Train rows needed on the device (or server) for the calibration refit, float64 | {r['train_data_kb_float64']:.0f} |", "",
          "| single-sample case | median (ms) | p95 (ms) |", "|---|---|---|"] + [
          f"| {c} | {r[c]['median_ms']:.3f} | {r[c]['p95_ms']:.3f} |" for c in
          ("svm_only_fault_free", "A_fault_free", "A_bias_one_sensor", "B_fault_free", "B_bias_one_sensor")] + [
          "", "| calibration step (one core) | seconds |", "|---|---|",
          f"| preprocessing + SVM refit | {r['calibration_svm_s']:.2f} |", f"| detector refit | {r['calibration_detector_s']:.2f} |",
          f"| 136 reduced B models | {r['calibration_B_136_models_s']:.2f} |", f"| total | {r['calibration_total_s']:.2f} |", "",
          f"Calibration rows: {r['calibration_rows']}; refit on {r['train_rows_for_calibration']} rows. Memory: {r['memory_after_imports_mb']:.0f} MB "
          f"after imports, {r['memory_peak_mb']:.0f} MB peak.", "", r["note"]]
    (OUT / "edge_cost_v2.md").write_text(chr(10).join(md), encoding="utf-8")
    print(chr(10).join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--child", nargs=2)
    a = ap.parse_args()
    child(*a.child) if a.child else parent()
