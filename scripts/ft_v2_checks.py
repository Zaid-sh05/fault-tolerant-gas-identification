"""Checks before the Test v2 run (decisions_log N6, N7). No Test data are read.

Usage: python scripts/ft_v2_checks.py smoke      # compare results/v2/ft_smoke/scores.csv with stage 2 (drift_dev_b6_n10_s0, seed 0)
       python scripts/ft_v2_checks.py estimate   # time the fits on the Train rows of batches 1-7 and estimate the run time
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

sys.path.insert(0, "scripts")
from src.data import xy  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.preprocessing import fit_preprocessor  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402
from src.strategies import StrategyKit  # noqa: E402
from src.study import OVERNIGHT  # noqa: E402

REC = Path("results/v2/recal")


def smoke():
    mine = pd.read_csv("results/v2/ft_smoke/scores.csv")
    mine = mine[(mine.subset == "b6") & (mine.cal_seed == 0)]
    cal = [r for f in sorted((REC / "drift_dev_b6_n10_s0" / "chunks").glob("chunk_*.pkl")) for r in pickle.load(open(f, "rb"))]
    unc = [r for f in sorted((REC / "uncal_drift_dev_b6_n10").glob("chunk_*.pkl")) for r in pickle.load(open(f, "rb")) if r["cal_seed"] == 0]
    worst = 0.0
    for model, ref in (("b", cal), ("a", unc)):
        ref = pd.DataFrame(ref).sort_values("sid")
        assert len(ref) == mine[mine.model == model].sid.nunique(), f"scenario count differs for model ({model})"
        for m in ("svm", "A", "B"):
            a = mine[(mine.model == model) & (mine.method == m)].sort_values("sid")["f1"].to_numpy()
            worst = max(worst, float(np.abs(a - ref[m].to_numpy()).max()))
    ok = worst < 1e-9
    print(f"smoke check vs stage 2 (drift_dev b6, seed 0, {len(cal)} scenarios): {'IDENTICAL' if ok else 'MISMATCH'} (max difference {worst:.2e})")
    return ok


def estimate():
    cfg = load_config("configs/preprocessing.yaml")
    cfg["split"] = {**cfg["split"], "train_batches": [1, 2, 3, 4, 5, 6, 7], "val_batches": [7]}   # only the Train rows are used
    proto = get_protocol_data(cfg)
    Xtr, ytr = xy(proto.train)
    btr = proto.train["batch"].to_numpy()
    fin = json.load(open(OVERNIGHT / "final_pipeline.json"))
    t = time.time()
    pre = fit_preprocessor(fin["spec"], Xtr, ytr, btr, fill_nan=False)
    svm = SVC(kernel="rbf", random_state=0, **fin["svm_params"]).fit(fill_nan_zero(pre.transform(Xtr)), ytr)
    t_svm = time.time() - t
    t = time.time()
    det = ReliabilityDetector(normalization="median").fit(Xtr, btr)
    t_det = time.time() - t
    kit = StrategyKit(pre, svm, Xtr, ytr, det, fin["svm_params"], "results/v2/ft_estimate_cache")
    t = time.time()
    for pattern in ((0,), (0, 1), (2, 5, 9), (1, 4, 8, 12)):
        kit.reduced_model(pattern)
    t_red = (time.time() - t) / 4
    X = Xtr[:3600]
    t = time.time()
    kit.predict_A(X, [()] * len(X), False)
    t_pred = time.time() - t
    sets_per_model = 1800                           # upper end of the stage-2 counts (960-1340 at medium severity) scaled to all severities
    n_scen, chunks_rows = 1081, 4364                # scenarios per batch; Test rows of 8-10 are about 4364 (v1 report)
    for seeds in (5, 3):
        models = 1 + 3 * seeds
        cpu = models * (t_svm + t_det + sets_per_model * t_red) + (3 * seeds + 3) * n_scen * 3 * t_pred * (chunks_rows / 3 / len(X))
        print(f"seeds {seeds}: {models} models; estimated wall time with 3 workers {cpu / 3 / 3600:.1f} h "
              f"(svm+pre {t_svm:.1f} s, detector {t_det:.1f} s, one reduced SVM {t_red:.1f} s, one predict on 3600 rows {t_pred:.2f} s)")


if __name__ == "__main__":
    {"smoke": lambda: sys.exit(0 if smoke() else 1), "estimate": estimate}[sys.argv[1]]()
