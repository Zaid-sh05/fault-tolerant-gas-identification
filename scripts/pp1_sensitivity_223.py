"""Sensitivity of the results to the borderline record (batch 2, line 223, S05_EMAd0.1 = -880).

Usage: python scripts/pp1_sensitivity_223.py
The rule keeps threshold 1000 MAD (not tuned). The record sits at ~1085 MAD in the reference protocol
(dropped there) and below the threshold in the temporal protocol (kept there). Each protocol is rerun with
the record forced the other way and the largest change is reported.
"""
from pathlib import Path

import numpy as np
import pandas as pd

R = Path("results")
P1 = R / "preprocessing" / "phase1"
THRESHOLD = 0.005


def main():
    rows = []
    base = pd.read_csv(R / "main_cleaned/02_baselines/clean_val.csv").set_index("model")
    alt = pd.read_csv(R / "main_cleaned_drop223/02_baselines/clean_val.csv").set_index("model")
    for model in base.index:
        rows.append({"what": f"temporal baseline {model} Macro-F1", "kept_223": base.loc[model, "macro_f1"],
                     "dropped_223": alt.loc[model, "macro_f1"]})
    for proto, other in (("temporal", "temporal_drop223"), ("reference_iid", "reference_iid_keep223")):
        a = pd.read_csv(P1 / proto / "reconstruction_summary.csv")
        b = pd.read_csv(P1 / other / "reconstruction_summary.csv")
        m = a.merge(b, on=["method", "space", "exclude_twin"], suffixes=("_a", "_b"))
        for metric in ("rmse_mean", "mae_mean", "medae_mean", "r2_median"):
            d = (m[f"{metric}_a"] - m[f"{metric}_b"]).abs()
            worst = m.loc[d.idxmax()]
            rows.append({"what": f"{proto} reconstruction {metric} (largest change, {worst['method']}/{worst['space']}"
                                 f"/twin_excluded={worst['exclude_twin']})",
                         "kept_223": worst[f"{metric}_a"], "dropped_223": worst[f"{metric}_b"]})
    t = pd.DataFrame(rows)
    t["abs_change"] = (t["kept_223"] - t["dropped_223"]).abs()
    t.round(4).to_csv(P1 / "sensitivity_line223.csv", index=False)
    pd.set_option("display.width", 250, "display.max_colwidth", 120)
    print(t.round(4).to_string(index=False))
    print(f"\nlargest change: {t['abs_change'].max():.4f}  (threshold {THRESHOLD}) ->",
          "below threshold" if t["abs_change"].max() < THRESHOLD else "ABOVE threshold")


if __name__ == "__main__":
    main()
