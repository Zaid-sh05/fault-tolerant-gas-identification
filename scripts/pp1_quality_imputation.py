"""Preprocessing phase 1: integrity re-check (batches 1-7) and sensor-block reconstruction.

Usage: python scripts/pp1_quality_imputation.py --config configs/preprocessing.yaml
Outputs: results/preprocessing/phase1/
  integrity.json, reconstruction_errors.csv (per feature), reconstruction_per_sensor.csv,
  reconstruction_summary.csv, reconstruction_{rmse,r2}_table.csv

Protocol: imputers are fitted on Train (batches 1-6) only. On Validation (batch 7, clean)
one whole sensor block is hidden at a time, rebuilt, and compared with the truth, once with
the replicate twin available and once without it (leave-pair-out).
Errors are on the raw standardised scale: (x - Train mean) / Train std.
"""
import argparse
import json
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from joblib import Parallel, delayed
from sklearn.exceptions import ConvergenceWarning

from src.data import FEATURE_KINDS, FEATURES, N_SENSORS, load_batches, split_by_batches, xy
from src.imputation import BlockImputer, block_errors


def integrity(df, expected_rows):
    X = df[FEATURES].to_numpy()
    report = {
        "records": len(df), "expected_records": expected_rows,
        "features": X.shape[1],
        "nan": int(np.isnan(X).sum()), "inf": int(np.isinf(X).sum()),
        "constant_features": int((X.std(0) == 0).sum()),
        "duplicate_rows": int(df[FEATURES].duplicated().sum()),
        "records_per_batch": {int(b): int(n) for b, n in df.batch.value_counts().sort_index().items()},
        "gas_codes": sorted(int(g) for g in df.gas.unique()),
    }
    report["passed"] = bool(report["records"] == expected_rows and report["nan"] == 0 and report["inf"] == 0
                            and report["constant_features"] == 0)
    return report


def evaluate_sensor(imp, X_val, sensor, exclude_twin, folds, mu, sd):
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    X_hat = imp.reconstruct(X_val, sensor, exclude_twin, folds)
    rmse, r2 = block_errors(X_val, X_hat, mu, sd, sensor)
    alpha = imp.ridge_alpha(sensor, exclude_twin) if imp.method == "ridge" else np.nan
    return [{"sensor": f"S{sensor + 1:02d}", "exclude_twin": exclude_twin, "feature_kind": k,
             "rmse": rmse[i], "r2": r2[i], "ridge_alpha": alpha} for i, k in enumerate(FEATURE_KINDS)]


def main(cfg_path):
    cfg = yaml.safe_load(open(cfg_path))
    sp, p1 = cfg["split"], cfg["phase1"]
    out = Path("results/preprocessing/phase1")
    out.mkdir(parents=True, exist_ok=True)

    df = load_batches(cfg["data"]["raw_dir"], sp["train_batches"] + sp["val_batches"])
    report = integrity(df, expected_rows=9546)
    json.dump(report, open(out / "integrity.json", "w"), indent=1)
    print("integrity:", json.dumps({k: v for k, v in report.items() if k != "records_per_batch"}))
    assert report["passed"], "integrity check failed"

    tr, va = split_by_batches(df, sp["train_batches"]), split_by_batches(df, sp["val_batches"])
    X_tr, _ = xy(tr)
    X_va, _ = xy(va)
    mu, sd = X_tr.mean(0), X_tr.std(0)
    folds = [tuple(f) for f in sp["inner_folds"]]

    rows = []
    for space in p1["spaces"]:
        for method in p1["methods"]:
            t0 = time.time()
            imp = BlockImputer(method, space, p1["knn_neighbors"], p1["ridge_alphas"],
                               p1["iterative"], cfg["seed"]).fit(X_tr, tr["batch"].to_numpy())
            res = Parallel(n_jobs=6)(delayed(evaluate_sensor)(imp, X_va, s, tw, folds, mu, sd)
                                     for s in range(N_SENSORS) for tw in (False, True))
            for r in res:
                rows += [{"method": method, "space": space, **x} for x in r]
            print(f"{method:9s} {space:4s} done in {time.time() - t0:5.1f}s")

    err = pd.DataFrame(rows)
    err.to_csv(out / "reconstruction_errors.csv", index=False)

    keys = ["method", "space", "exclude_twin", "sensor"]
    per_sensor = err.groupby(keys, as_index=False).agg(rmse=("rmse", "mean"), r2=("r2", "mean"))
    per_sensor.to_csv(out / "reconstruction_per_sensor.csv", index=False)
    summary = (per_sensor.groupby(["method", "space", "exclude_twin"])
               .agg(rmse_mean=("rmse", "mean"), rmse_std=("rmse", "std"),
                    r2_mean=("r2", "mean"), r2_median=("r2", "median"), r2_min=("r2", "min"),
                    sensors_r2_below_0=("r2", lambda v: int((v < 0).sum())))
               .reset_index().sort_values(["exclude_twin", "rmse_mean"]))
    summary.to_csv(out / "reconstruction_summary.csv", index=False)
    for metric in ("rmse", "r2"):
        table = per_sensor.pivot_table(index="sensor", values=metric,
                                       columns=["method", "space", "exclude_twin"])
        table.round(3).to_csv(out / f"reconstruction_{metric}_table.csv")
    print(summary.round(3).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
