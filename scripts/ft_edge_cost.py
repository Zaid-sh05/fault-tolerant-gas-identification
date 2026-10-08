"""Edge cost of the full pipeline A: reliability detector + reconstruction of the flagged blocks + SVM.

Usage: python scripts/ft_edge_cost.py            (run it on an otherwise idle machine; takes about a minute)
Outputs: results/edge_cost/edge_cost.json and edge_cost.md
What is measured
  * size: the deployable bundle (SVM, preprocessing, detector WITHOUT its training-only arrays: per-batch Gram matrices and
    the out-of-fold scores) pickled, in KB, with the size of each part;
  * latency of one sample (detector -> flags -> reconstruction of the flagged blocks -> preprocessing -> SVM) in a FRESH process
    pinned to one CPU core with one BLAS thread: median and 95th percentile over 1000 runs (after 50 warm-up runs), for
    (1) fault-free samples, (2) samples with a Bias fault on one sensor, (3) the same with the reconstruction weights solved on
    demand (cache emptied before each run: worst case);
  * memory: peak working set of that process (Windows PeakWorkingSetSize) and the working set before the model is loaded.
The samples are random rows of Validation batch 7 (latency does not depend on the labels), so the Test rows are not read again.
This is a laptop CPU, not an edge device: the numbers are an upper bound on the algorithmic work, not a board benchmark.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import copy  # noqa: E402
import ctypes  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
from ctypes import wintypes  # noqa: E402
from pathlib import Path  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402

RUNS, WARMUP = 1000, 50
OUT = Path("results/edge_cost")


class Counters(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t), ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t)]


def memory_mb():
    """(current, peak) working set of this process in MB."""
    c = Counters()
    c.cb = ctypes.sizeof(Counters)
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(c), c.cb)
    return c.WorkingSetSize / 2**20, c.PeakWorkingSetSize / 2**20


def child(bundle_path, data_path, out_path):
    ctypes.windll.kernel32.SetProcessAffinityMask(ctypes.windll.kernel32.GetCurrentProcess(), 1)       # one core
    from src.strategies import StrategyKit, acted_sets                    # noqa: E402  (imports counted in the baseline)
    before = memory_mb()[0]
    with open(bundle_path, "rb") as f:
        b = pickle.load(f)
    kit = object.__new__(StrategyKit)                                      # A needs only pre, svm and the detector
    kit.pre, kit.svm, kit.det = b["pre"], b["svm"], b["det"]
    data = np.load(data_path)

    def one(x, cold):
        if cold:
            kit.det._w_cache.clear()
        t = time.perf_counter_ns()
        R = kit.det.ratio(x)
        y = kit.predict_A(x, acted_sets(R, R > 1.0), False)
        return (time.perf_counter_ns() - t) / 1e6, int(y[0]), int((R > 1.0).sum())

    out = {"memory_after_imports_mb": before}
    for case, cold in (("fault_free", False), ("bias_one_sensor", False), ("bias_one_sensor_cold_weights", True)):
        X = data["clean" if case == "fault_free" else "bias"]
        for i in range(WARMUP):
            one(X[i:i + 1], cold)
        res = [one(X[i:i + 1], cold) for i in range(RUNS)]
        ms = np.array([r[0] for r in res])
        out[case] = {"runs": RUNS, "median_ms": float(np.median(ms)), "p95_ms": float(np.percentile(ms, 95)),
                     "mean_flagged_sensors": float(np.mean([r[2] for r in res]))}
    out["memory_final_mb"], out["memory_peak_mb"] = memory_mb()
    json.dump(out, open(out_path, "w"))


def parent():
    from src.scenarios import Scenario, apply_scenario
    from src.study import Study
    study = Study("configs/preprocessing.yaml", "temporal")                  # Train 1-6 and Validation 7 only
    det = joblib.load(study.dir / "detectors" / "median.joblib")
    svm = joblib.load(study.dir / "models" / "svm.joblib")
    slim = copy.copy(det)
    for attr in ("Gb_", "nb_", "batch_ids_", "E_oof_"):                      # training-only arrays
        delattr(slim, attr)
    parts = {"svm": svm, "pre": study.pre, "det": slim}
    sizes = {k: len(pickle.dumps(v, protocol=pickle.HIGHEST_PROTOCOL)) / 1024 for k, v in parts.items()}
    sizes["det_full_with_training_arrays"] = len(pickle.dumps(det, protocol=pickle.HIGHEST_PROTOCOL)) / 1024
    rng = np.random.default_rng(0)
    rows = rng.choice(len(study.Xev), RUNS + WARMUP, replace=False)
    sensors = np.arange(len(rows)) % 16
    bias = np.empty((len(rows), 128))
    for s in range(16):                                                      # Bias fault, medium severity, one sensor per row
        Xf, _ = apply_scenario(study.Xev, Scenario(0, "k1", (s,), "bias", 1.0, 0), study.stats)
        bias[sensors == s] = Xf[rows[sensors == s]]
    with tempfile.TemporaryDirectory() as tmp:
        bundle, data, res = Path(tmp) / "bundle.pkl", Path(tmp) / "data.npz", Path(tmp) / "res.json"
        pickle.dump(parts, open(bundle, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
        np.savez(data, clean=study.Xev[rows], bias=bias)
        subprocess.run([sys.executable, __file__, "--child", str(bundle), str(data), str(res)], check=True)
        result = json.load(open(res))
    result["bundle_kb"] = len(pickle.dumps(parts, protocol=pickle.HIGHEST_PROTOCOL)) / 1024
    result["part_sizes_kb"] = sizes
    result["note"] = ("Validation rows, one core, one BLAS thread, laptop CPU; sizes are pickles (float64). "
                      "The bundle holds the SVM, the preprocessing and the detector without its training-only arrays.")
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(result, open(OUT / "edge_cost.json", "w"), indent=1)
    md = ["# Edge cost of pipeline A (detector + reconstruction + SVM)", "",
          f"Bundle size: **{result['bundle_kb']:.0f} KB** ("
          + ", ".join(f"{k} {v:.0f} KB" for k, v in sizes.items()) + ")", "",
          "| case | median (ms) | p95 (ms) | mean flagged sensors |", "|---|---|---|---|"]
    for case in ("fault_free", "bias_one_sensor", "bias_one_sensor_cold_weights"):
        c = result[case]
        md.append(f"| {case} | {c['median_ms']:.3f} | {c['p95_ms']:.3f} | {c['mean_flagged_sensors']:.2f} |")
    md += ["", f"Memory: {result['memory_after_imports_mb']:.0f} MB after imports, {result['memory_peak_mb']:.0f} MB peak "
           f"(working set of the measuring process, {RUNS} runs per case).", "", result["note"]]
    (OUT / "edge_cost.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--child", nargs=3)
    a = ap.parse_args()
    child(*a.child) if a.child else parent()
