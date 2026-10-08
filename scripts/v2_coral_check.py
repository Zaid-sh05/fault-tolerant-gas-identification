"""CORAL correctness check (DIAGNOSTIC ONLY, decisions_log K1; changes no choice). Batches 1-7 only.

Usage: python scripts/v2_coral_check.py
Output: results/v2/coral_check.csv and coral_check.md
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import sys  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.linalg import inv, sqrtm  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

sys.path.insert(0, "scripts")
from v2_dev import OUT, PROTOCOLS, build, load  # noqa: E402
from src.drift import Coral  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.study import OVERNIGHT  # noqa: E402


def gap(C, ref):
    return float(np.linalg.norm(C - ref) / np.linalg.norm(ref))


def main():
    svm_params = json.load(open(OVERNIGHT / "final_pipeline.json"))["svm_params"]
    ref = pd.read_csv(OUT / "candidates.csv").set_index("candidate")
    rows = []
    for proto, cfg in PROTOCOLS.items():
        Xtr, ytr, btr, evals = load(cfg)
        coral = Coral().fit(Xtr, btr)
        I = np.eye(Xtr.shape[1])
        Zs = (Xtr - coral.mu_) / coral.sd_
        Cs = np.cov(Zs, rowvar=False) + I
        _, _, m2 = build("M2", Xtr, ytr, btr)
        _, _, m0 = build("M0", Xtr, ytr, btr)
        for b, (X, y) in evals.items():
            Zt = (X - coral.mu_) / coral.sd_
            Ct = np.cov(Zt, rowvar=False) + I
            ours = (coral.transform(X) - coral.mu_) / coral.sd_
            independent = np.real(Zt @ inv(sqrtm(Ct)) @ sqrtm(Cs))
            # paper direction: Train mapped to the new batch's covariance, SVM retrained there (standardised space)
            Ds = np.real(Zs @ inv(sqrtm(Cs)) @ sqrtm(Ct))
            paper = fast_svm_predict(SVC(kernel="rbf", random_state=0, **svm_params).fit(Ds, ytr), Zt)
            f1_m2 = scores(y, m2(X))["macro_f1"]
            col = f"drift_dev_b{b}" if proto == "drift_dev" else "original_b7"
            rows.append({"protocol": proto, "batch": b,
                         "max_abs_diff_vs_independent": float(np.abs(ours - independent).max()),
                         "cov_gap_before": gap(np.cov(Zt, rowvar=False) + I, Cs),
                         "cov_gap_after": gap(np.cov(ours, rowvar=False) + I, Cs),
                         "mean_norm_train": float(np.linalg.norm(Zs.mean(0))),
                         "mean_norm_batch_before": float(np.linalg.norm(Zt.mean(0))),
                         "mean_norm_batch_after": float(np.linalg.norm(ours.mean(0))),
                         "f1_M0": scores(y, m0(X))["macro_f1"], "f1_M2_ours": f1_m2,
                         "M2_reproduces_candidates": abs(f1_m2 - ref.loc["M2", col]) < 5e-4,
                         "f1_coral_paper_direction": scores(y, paper)["macro_f1"]})
            print(rows[-1], flush=True)
    tab = pd.DataFrame(rows)
    tab.round(4).to_csv(OUT / "coral_check.csv", index=False)
    (OUT / "coral_check.md").write_text("# CORAL check (DIAGNOSTIC ONLY, decisions_log K1)" + chr(10) + chr(10)
                                        + tab.round(4).to_markdown(index=False) + chr(10), encoding="utf-8")
    print(tab.round(4).to_markdown(index=False))


if __name__ == "__main__":
    main()
