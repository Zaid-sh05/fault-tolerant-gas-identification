"""Detector numbers of the v1 final test in one place. READS EXISTING RESULT FILES ONLY (no experiment, Test data not read).

Usage: python scripts/detector_breakdown.py   ->  results/paper/detector_breakdown.md (also printed)
Sources: results/final_test/test/{ft_detector_summary.csv, ft_g2_by_subset.json, ft_far_by_gas.csv, ft_reliability_ranking.csv}.
Only the primary detector ("median") is shown. A number absent from these files is written "غير محسوب" (not computed) and is not derived.
"""
import json
from pathlib import Path

import pandas as pd

SRC = Path("results/final_test/test")
OUT = Path("results/paper/detector_breakdown.md")
NA = "غير محسوب"
DET = "median"


def main():
    summ = pd.read_csv(SRC / "ft_detector_summary.csv")
    summ = summ[summ.detector == DET]
    g2 = json.load(open(SRC / "ft_g2_by_subset.json"))
    far = pd.read_csv(SRC / "ft_far_by_gas.csv")
    far = far[(far.detector == DET) & (far.gas == "all")]
    rank = pd.read_csv(SRC / "ft_reliability_ranking.csv")
    rank = rank[rank.detector == DET]

    md = ["# Detector breakdown, v1 final test (batches 8-10), primary detector `median`", "",
          "Read from existing result files only (`results/final_test/test/`); no experiment was run and the Test data were not read again. "
          "Threshold = the frozen alarm threshold (95th percentile of the Train out-of-fold scores). "
          f"'{NA}' = not present in the result files, deliberately not derived.", "",
          "Definitions: AUROC = isolation AUROC (faulty blocks vs healthy blocks of the same rows), mean over the scenarios of the cell; "
          "TPR = share of faulty blocks flagged; FPR(healthy, same rows) = share of healthy blocks flagged in the faulted rows; "
          "FAR(clean) = share of sensor-rows flagged on the clean (no injected fault) Test rows.", ""]

    # 1. fault type x severity x k, pooled Test
    p = summ[summ.subset == "pooled"].sort_values(["kset", "fault", "level"])
    t1 = p[["kset", "fault", "level", "n", "auroc_isolation", "tpr", "fpr_healthy_same_rows"]].rename(columns={
        "kset": "k", "level": "severity", "n": "scenarios", "auroc_isolation": "AUROC", "tpr": "TPR", "fpr_healthy_same_rows": "FPR (healthy, same rows)"})
    md += ["## 1. AUROC and TPR at the frozen threshold, per fault type x severity x k (Test pooled)", "",
           t1.round(4).to_markdown(index=False), ""]

    # 2. per batch
    rows = []
    for sub in ("b8", "b9", "b10", "pooled"):
        d = g2[sub]["detectors"][DET]
        f_all = far[(far.subset == sub) & (far.sensors == "all sensors")]
        f_wo = far[(far.subset == sub) & (far.sensors == "without S01,S02")]
        rows.append({"subset": sub, "AUROC over all scenarios": NA,
                     "G2 statistic (median over fault types, k=1 medium)": round(d["median_auroc"], 4),
                     **{f"AUROC k=1 medium {k}": round(v, 4) for k, v in d["by_fault"].items()},
                     "FAR clean, all sensors": f_all["alarm_rate_per_sensor_row"].iloc[0] if len(f_all) else NA,
                     "FAR clean, without S01,S02": f_wo["alarm_rate_per_sensor_row"].iloc[0] if len(f_wo) else NA,
                     "clean rows with any alarm": f_all["rows_with_any_alarm"].iloc[0] if len(f_all) else NA})
    md += ["## 2. AUROC and FAR per Test batch", "",
           "An AUROC pooled over all scenarios of a batch is not in the files; the per-cell values of every batch are in "
           "`ft_detector_summary.csv` (and the per-batch k=1 medium values below).", "",
           pd.DataFrame(rows).to_markdown(index=False), ""]

    # 3. FAR per sensor on clean Test rows
    t3 = rank.pivot(index="sensor", columns="subset", values="alarm_rate").reindex([f"S{i:02d}" for i in range(1, 17)])
    t3 = t3[[c for c in ("pooled", "b8", "b9", "b10") if c in t3.columns]].astype(object).where(t3.notna(), NA)
    md += ["## 3. FAR per sensor on the clean Test rows (alarm rate of the sensor at the frozen threshold)", "",
           t3.reset_index().to_markdown(index=False), "",
           "Expected without drift: about 0.05 per sensor (the threshold is the 95th percentile of the Train out-of-fold scores)."]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
