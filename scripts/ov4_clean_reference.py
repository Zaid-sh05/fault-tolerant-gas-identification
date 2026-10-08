"""What do the strategies cost when there is NO fault? (clean evaluation rows, same detector and thresholds)

Usage: python scripts/ov4_clean_reference.py --config configs/preprocessing.yaml --name temporal
Output: results/overnight/<name>/strategy_clean_eval.csv
Under drift the detector raises alarms on clean rows (S01 and S02 on almost every row of batch 7), so A/B/C act even
without a fault; this table measures the price of that.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import sys  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, "scripts")
from ov4_strategies import make_kit  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.strategies import acted_sets  # noqa: E402
from src.study import Study  # noqa: E402


def main(cfg_path, name):
    study = Study(cfg_path, name)
    kit, det = make_kit(study)
    X = study.Xev
    R = det.ratio(X)
    sets = acted_sets(R, R > 1.0)
    proba = kit.expert_proba(X)
    out = {"clean_svm_no_handling": fast_svm_predict(kit.svm, fill_nan_zero(study.pre.transform(X))),
           "A_det_twin": kit.predict_A(X, sets, False), "A_det_notwin": kit.predict_A(X, sets, True),
           "B_det": kit.predict_B(X, sets), "C_det": kit.combine(proba, R), "C_equal": kit.combine(proba, None)}
    n_flag = np.array([len(s) for s in sets])
    rows = [{"method": m, **scores(study.yev, p), "mean_flagged_per_row": float(n_flag.mean()) if m != "clean_svm_no_handling" else 0.0,
             "rows_with_any_flag": float((n_flag > 0).mean()) if m != "clean_svm_no_handling" else 0.0} for m, p in out.items()]
    df = pd.DataFrame(rows)
    df.round(4).to_csv(study.dir / "strategy_clean_eval.csv", index=False)
    print(df.round(4).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    ap.add_argument("--name", default="temporal")
    a = ap.parse_args()
    main(a.config, a.name)
