"""Preprocessing phase 1: integrity re-check (batches 1-7) and sensor-block reconstruction.

Usage: python scripts/pp1_quality_imputation.py --config configs/preprocessing.yaml      (temporal protocol)
       python scripts/pp1_quality_imputation.py --config configs/reference_iid.yaml      (no-drift reference)
Outputs: results/preprocessing/phase1/<protocol>/
  integrity.json, reconstruction_errors.csv (per feature), reconstruction_per_sensor.csv,
  reconstruction_summary.csv, reconstruction_{rmse,r2}_table.csv

Protocol: imputers are fitted on the Train rows of the protocol only. On the clean evaluation rows
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
from joblib import Parallel, delayed
from sklearn.exceptions import ConvergenceWarning

from src.data import FEATURE_KINDS, FEATURES, N_SENSORS, xy
from src.imputation import BlockImputer, block_errors
from src.splits import get_protocol_data, load_config


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


METRICS = ("rmse", "mae", "medae", "r2")


def evaluate_sensor(imp, X_val, sensor, exclude_twin, folds, mu, sd):
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    X_hat = imp.reconstruct(X_val, sensor, exclude_twin, folds)
    err = block_errors(X_val, X_hat, mu, sd, sensor)
    alpha = imp.ridge_alpha(sensor, exclude_twin) if imp.method == "ridge" else np.nan
    return [{"sensor": f"S{sensor + 1:02d}", "exclude_twin": exclude_twin, "feature_kind": k,
             **{m: err[m][i] for m in METRICS}, "ridge_alpha": alpha} for i, k in enumerate(FEATURE_KINDS)]


def main(cfg_path):
    cfg = load_config(cfg_path)
    p1 = cfg["phase1"]
    proto = get_protocol_data(cfg)
    out = Path("results/preprocessing/phase1") / cfg.get("run_name", proto.name)
    out.mkdir(parents=True, exist_ok=True)

    report = integrity(pd.concat([proto.train, proto.eval], ignore_index=True),
                       expected_rows=9546 - len(proto.dropped_train))
    report["protocol"] = proto.name
    report["train_rows"], report["eval_rows"] = len(proto.train), len(proto.eval)
    report["cleaning_dropped_train"] = proto.dropped_train.to_dict("records")
    report["cleaning_flagged_eval_kept"] = proto.flagged_eval.to_dict("records")
    json.dump(report, open(out / "integrity.json", "w"), indent=1)
    print("integrity:", json.dumps({k: v for k, v in report.items() if k != "records_per_batch"}))
    assert report["passed"], "integrity check failed"

    X_tr, _ = xy(proto.train)
    # A record the cleaning rule flags in the evaluation rows has a corrupt "true" value, so it cannot be a
    # reconstruction target: it is left out of the reconstruction errors (it stays in classification).
    flagged = set(map(tuple, proto.flagged_eval[["batch", "line"]].to_numpy()))
    usable = np.array([(b, l) not in flagged for b, l in zip(proto.eval["batch"], proto.eval["line"])])
    X_va, _ = xy(proto.eval[usable])
    report["reconstruction_eval_rows_excluded"] = int((~usable).sum())
    json.dump(report, open(out / "integrity.json", "w"), indent=1)
    print(f"reconstruction metrics: {int((~usable).sum())} flagged evaluation record(s) excluded of {len(usable)}")
    mu, sd = X_tr.mean(0), X_tr.std(0)
    folds = proto.inner_folds

    rows = []
    for space in p1["spaces"]:
        for method in p1["methods"]:
            t0 = time.time()
            imp = BlockImputer(method, space, p1["knn_neighbors"], p1["ridge_alphas"],
                               p1["iterative"], cfg["seed"]).fit(X_tr, proto.groups)
            res = Parallel(n_jobs=6)(delayed(evaluate_sensor)(imp, X_va, s, tw, folds, mu, sd)
                                     for s in range(N_SENSORS) for tw in (False, True))
            for r in res:
                rows += [{"method": method, "space": space, **x} for x in r]
            print(f"{method:9s} {space:4s} done in {time.time() - t0:5.1f}s")

    err = pd.DataFrame(rows)
    err.to_csv(out / "reconstruction_errors.csv", index=False)

    keys = ["method", "space", "exclude_twin", "sensor"]
    per_sensor = err.groupby(keys, as_index=False)[list(METRICS)].mean()
    per_sensor.to_csv(out / "reconstruction_per_sensor.csv", index=False)
    summary = (per_sensor.groupby(["method", "space", "exclude_twin"])
               .agg(rmse_mean=("rmse", "mean"), rmse_std=("rmse", "std"),
                    mae_mean=("mae", "mean"), medae_mean=("medae", "mean"),
                    r2_mean=("r2", "mean"), r2_median=("r2", "median"), r2_min=("r2", "min"),
                    sensors_r2_below_0=("r2", lambda v: int((v < 0).sum())))
               .reset_index().sort_values(["exclude_twin", "rmse_mean"]))
    summary.to_csv(out / "reconstruction_summary.csv", index=False)
    for metric in METRICS:
        table = per_sensor.pivot_table(index="sensor", values=metric,
                                       columns=["method", "space", "exclude_twin"])
        table.round(3).to_csv(out / f"reconstruction_{metric}_table.csv")
    print(summary.round(3).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
