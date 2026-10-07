"""Side-by-side reconstruction errors of the temporal and the reference_iid protocols.

Usage: python scripts/pp1_compare_protocols.py
Reads  results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv
Writes results/preprocessing/phase1/protocol_comparison_{sensor,summary}.csv

Flagged (invalid) evaluation records are already excluded from these errors (see pp1_quality_imputation.py).
drift cost = metric_temporal - metric_iid        for the errors (rmse, mae, medae): positive = drift hurts
drift cost = r2_iid - r2_temporal                 for R2:                           positive = drift hurts
"""
from pathlib import Path

import pandas as pd

ROOT = Path("results/preprocessing/phase1")
KEYS = ["method", "space", "exclude_twin", "sensor"]
ERRORS = ("rmse", "mae", "medae")


def main():
    t = pd.read_csv(ROOT / "temporal" / "reconstruction_per_sensor.csv")
    i = pd.read_csv(ROOT / "reference_iid" / "reconstruction_per_sensor.csv")
    m = t.merge(i, on=KEYS, suffixes=("_temporal", "_iid"))
    for e in ERRORS:
        m[f"drift_cost_{e}"] = m[f"{e}_temporal"] - m[f"{e}_iid"]
    m["drift_cost_r2"] = m["r2_iid"] - m["r2_temporal"]
    m.round(4).to_csv(ROOT / "protocol_comparison_sensor.csv", index=False)

    agg = {f"{e}_{p}": (f"{e}_{p}", "mean") for e in ERRORS for p in ("temporal", "iid")}
    agg.update(r2_median_temporal=("r2_temporal", "median"), r2_median_iid=("r2_iid", "median"),
               neg_r2_temporal=("r2_temporal", lambda v: int((v < 0).sum())),
               neg_r2_iid=("r2_iid", lambda v: int((v < 0).sum())))
    s = m.groupby(["method", "space", "exclude_twin"]).agg(**agg).reset_index()
    for e in ERRORS:
        s[f"drift_cost_{e}"] = s[f"{e}_temporal"] - s[f"{e}_iid"]
    s["drift_cost_r2_median"] = s["r2_median_iid"] - s["r2_median_temporal"]
    s = s.sort_values(["exclude_twin", "mae_iid"])
    s.round(4).to_csv(ROOT / "protocol_comparison_summary.csv", index=False)

    pd.set_option("display.width", 250)
    cols = ["method", "space", "exclude_twin", "mae_temporal", "mae_iid", "drift_cost_mae", "medae_temporal",
            "medae_iid", "rmse_temporal", "rmse_iid", "r2_median_temporal", "r2_median_iid",
            "neg_r2_temporal", "neg_r2_iid"]
    print("\nSUMMARY: mean over the 16 sensors (neg_r2 = sensors with R2 < 0)")
    print(s[cols].round(3).to_string(index=False))
    for method, space in (("ridge", "slog"), ("knn", "raw")):
        d = m[(m.method == method) & (m.space == space)]
        wide = d.pivot(index="sensor", columns="exclude_twin",
                       values=["mae_temporal", "mae_iid", "drift_cost_mae"]).round(3)
        wide.columns = [f"{a}|{'no_twin' if b else 'twin'}" for a, b in wide.columns]
        print(f"\nPER SENSOR MAE, {method}/{space}")
        print(wide.to_string())


if __name__ == "__main__":
    main()
