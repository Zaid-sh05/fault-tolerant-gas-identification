"""Test report (facts only, every number read from result files): results/final_test/TEST_REPORT.md.

Usage: python scripts/ft_report.py [--test results/final_test/test] [--out results/final_test/TEST_REPORT.md]
Sections: 1 gates; 2 clean performance of the baselines and of A/B/C (do false alarms hurt?); 3 detector per batch;
4 did the ordering "A and B above the best augmented baseline" hold on Test (per fault type and per k, per batch);
5 per-batch tables of the main comparison; 6 caveats. Validation numbers come from results/overnight/temporal.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

VAL = Path("results/overnight/temporal")
MEDIUM = {"dropout": 0.5, "bias": 1.0, "stuck": 0.5, "random": 0.5}
CELL = ["kset", "fault", "level"]


def t(df, fmt=3):
    return df.to_markdown(index=False, floatfmt=f".{fmt}f")


def subsets_in(df):
    return [s for s in ("pooled", "b8", "b9", "b10", "b7") if s in set(df["subset"])]


def main(test, out):
    test = Path(test)
    ver = json.load(open(test / "ft_verdicts.json"))
    g2 = json.load(open(test / "ft_g2_by_subset.json"))
    primary = next(iter(g2.values()))["primary"]
    subs = list(ver)
    md = ["# Final test report (batches 8-10), facts only",
          "Frozen commit/manifest: `FREEZE_MANIFEST.md`, tag `frozen-before-test`. Every number below is read from files in "
          f"`{test}` (Test) or `{VAL}` (Validation). Interpretation is not part of this file.", ""]

    # 1 gates -----------------------------------------------------------------------------------------
    v1, v2, v3 = (json.load(open(VAL / f)) for f in ("g1_verdict.json", "g2_verdict.json", "g3_verdict.json"))
    rows = [{"subset": "Validation (b7)", "clean best baseline": v1["best_clean_baseline"], "clean Macro-F1": v1["clean_macro_f1"],
             "G1 types >= 0.03": f'{len(v1["types_with_drop_ge_0.03"])} of 4', "G1": v1["G1_passes"],
             "G2 median AUROC": v2["median_auroc"], "G2": v2["G2_passes"], "G3 cells": f'{v3["cells_passing"]} of {v3["comparisons"]}', "G3": v3["G3_passes"]}]
    for s in subs:
        v = ver[s]
        rows.append({"subset": f"Test {s}", "clean best baseline": v["G1"]["best_clean_baseline"], "clean Macro-F1": v["G1"]["clean_macro_f1"],
                     "G1 types >= 0.03": f'{len(v["G1"]["types_with_drop_ge_0.03"])} of 4', "G1": v["G1"]["G1_passes"],
                     "G2 median AUROC": g2[s]["detectors"][primary]["median_auroc"], "G2": g2[s]["G2_passes"],
                     "G3 cells": f'{v["cells_passing"]} of {v["comparisons"]}', "G3": v["G3_passes"]})
    md += ["## 1. Gates", t(pd.DataFrame(rows)), "",
           "G1 drop of the best clean baseline per fault type (k=1, medium severity):", t(pd.DataFrame(
               [{"subset": "Validation", **v1["k1_medium_mean_drop_by_fault"]}] + [{"subset": f"Test {s}", **ver[s]["G1"]["k1_medium_mean_drop_by_fault"]} for s in subs]), 3), "",
           "G3 passes if a single comparison passes (lenient); intervals resample rows only (optimistic).", ""]

    # 2 clean performance --------------------------------------------------------------------------------
    clean = pd.read_csv(test / "ft_clean_by_subset.csv")
    vclean = pd.read_csv(VAL / "strategy_clean_eval.csv").set_index("method")
    vbase = pd.read_csv(VAL / "clean_eval.csv", index_col=0)
    rows = []
    for m in ["svm", "lgbm", "A_det_twin", "A_det_notwin", "B_det", "C_det", "C_equal"]:
        r = {"method": m}
        v = vclean.loc["clean_svm_no_handling" if m == "svm" else m, "macro_f1"] if m not in ("lgbm",) else vbase.loc["lgbm", "macro_f1"]
        r["Validation"] = v
        for s in subs:
            r[f"Test {s}"] = clean[(clean.subset == s) & (clean.method == m)]["macro_f1"].iloc[0]
        rows.append(r)
    tab = pd.DataFrame(rows)
    md += ["## 2. Clean (no injected fault) Macro-F1: do false alarms hurt?", t(tab), ""]
    delta = tab.set_index("method")
    d = pd.DataFrame({c: [delta.loc["A_det_twin", c] - delta.loc["svm", c], delta.loc["A_det_notwin", c] - delta.loc["svm", c], delta.loc["B_det", c] - delta.loc["svm", c]]
                      for c in delta.columns}, index=["A (twin) - SVM", "A (no twin) - SVM", "B - SVM"]).reset_index(names="difference")
    md += ["Difference to the plain SVM on clean rows (negative = acting on false alarms costs accuracy):", t(d), "",
           "Share of clean rows on which at least one sensor is flagged, and mean flagged sensors per row (detector acting on clean data):"]
    flag = clean[clean.method.isin(["A_det_twin"])][["subset", "rows", "mean_flagged_per_row", "rows_with_any_flag"]]
    vf = pd.DataFrame([{"subset": "Validation", "rows": np.nan, "mean_flagged_per_row": vclean.loc["A_det_twin", "mean_flagged_per_row"],
                        "rows_with_any_flag": vclean.loc["A_det_twin", "rows_with_any_flag"]}])
    md += [t(pd.concat([vf, flag])), ""]
    acc = clean[clean.method.isin(["svm", "A_det_twin", "B_det"])].pivot(index="method", columns="subset", values="accuracy").reset_index()
    md += ["Clean accuracy (Test):", t(acc), ""]

    # 3 detector per batch ------------------------------------------------------------------------------
    far = pd.read_csv(test / "ft_far_by_gas.csv")
    far = far[far.detector == primary]
    vfar = pd.read_csv(VAL / "far_by_gas.csv")
    vfar = vfar[vfar.detector == primary]
    rows = []
    for label in ("all sensors", "without S01,S02"):
        r = {"sensors": label, "Validation": vfar[(vfar.gas == "all") & (vfar.sensors == label)]["alarm_rate_per_sensor_row"].iloc[0]}
        for s in subs:
            r[f"Test {s}"] = far[(far.subset == s) & (far.gas == "all") & (far.sensors == label)]["alarm_rate_per_sensor_row"].iloc[0]
        rows.append(r)
    md += ["## 3. Detector on clean data", f"Primary detector: `{primary}` (alarm threshold = Train out-of-fold 95th percentile, so about 5% is expected without drift).",
           "False-alarm rate per sensor-row, per batch:", t(pd.DataFrame(rows)), ""]
    pg = far[far.sensors == "all sensors"].pivot(index="gas", columns="subset", values="alarm_rate_per_sensor_row")[subs].reset_index()
    pg2 = far[far.sensors == "without S01,S02"].pivot(index="gas", columns="subset", values="alarm_rate_per_sensor_row")[subs].reset_index()
    md += ["Per gas, all sensors:", t(pg), "", "Per gas, without S01 and S02:", t(pg2), ""]
    rank = pd.read_csv(test / "ft_reliability_ranking.csv")
    rank = rank[rank.detector == primary]
    rk = rank.pivot(index="rank_from_least_reliable", columns="subset", values="sensor")[subs].reset_index()
    md += ["Sensors from least to most reliable on clean rows:", t(rk), ""]
    al = pd.read_csv(test / "sensor_alarm_rate_by_batch.csv")
    md += ["Detector alarm rate of S01 and S02 per batch (batches 1-6 out-of-fold, 7-10 evaluation):",
           t(al[al.sensor.isin(["S01", "S02"])].pivot(index="batch", columns="sensor", values="alarm_rate").reset_index()), ""]
    summ = pd.read_csv(test / "ft_detector_summary.csv")
    sel = summ[(summ.detector == primary) & (summ.kset == "k1")]
    sel = sel[[(r.level == MEDIUM[r.fault]) for r in sel.itertuples()]]
    md += ["Isolation AUROC per fault type (k=1, medium severity), per batch:",
           t(sel.pivot(index="fault", columns="subset", values="auroc_isolation")[subs].reset_index()), "",
           "Hit rate (share of faulty blocks flagged) and false-alarm rate on the healthy blocks of the same rows (k=1, medium):",
           t(sel.pivot(index="fault", columns="subset", values="tpr")[subs].reset_index()), "",
           t(sel.pivot(index="fault", columns="subset", values="fpr_healthy_same_rows")[subs].reset_index()), ""]

    # 4 ordering ----------------------------------------------------------------------------------------
    vs = pd.read_csv(test / "ft_vs_best_aug.csv")
    vv = pd.read_csv(VAL / "strategy_vs_best_aug.csv")
    vv["subset"] = "Validation"
    allv = pd.concat([vv[vs.columns.intersection(vv.columns)], vs[vs.columns]])
    md += ["## 4. Did A and B stay above the best augmented baseline?",
           "Per fault type and k, over every severity (levels) and the sensor sets: number of cells with a positive difference to the best augmented baseline "
           "and, in brackets, with an interval that excludes 0. Methods use the real detector.", ""]
    order = ["Validation"] + [s for s in subsets_in(vs)]
    for method in ("A_det_twin", "B_det"):
        rows = []
        for (fault, kset), g in allv[allv.method == method].groupby(["fault", "kset"]):
            r = {"fault": fault, "k": kset[1:]}
            for s in order:
                x = g[g.subset == s]
                if len(x):
                    r[s] = f"{int((x['diff'] > 0).sum())}/{len(x)} ({int((x['ci_low'] > 0).sum())})"
            rows.append(r)
        md += [f"{method}:", t(pd.DataFrame(rows)), ""]
    rows = []
    for method in ("A_det_twin", "B_det"):
        for s in order:
            x = allv[(allv.method == method) & (allv.subset == s)]
            rows.append({"method": method, "subset": s, "cells": len(x), "diff > 0": int((x["diff"] > 0).sum()), "CI excludes 0": int((x["ci_low"] > 0).sum()),
                         "mean diff": x["diff"].mean(), "min diff": x["diff"].min(), "max diff": x["diff"].max()})
    md += ["Totals:", t(pd.DataFrame(rows)), ""]
    flips = []
    for method in ("A_det_twin", "B_det"):
        v = vv[vv.method == method].set_index(CELL)["diff"]
        p = vs[(vs.subset == "pooled") & (vs.method == method)].set_index(CELL)["diff"]
        j = pd.concat([v.rename("val"), p.rename("test")], axis=1).dropna()
        for idx, r in j[(j.val > 0) != (j.test > 0)].iterrows():
            flips.append({"method": method, "kset": idx[0], "fault": idx[1], "level": idx[2], "Validation diff": r.val, "Test pooled diff": r.test})
    md += ["Cells where the sign of the difference to the best augmented baseline differs between Validation and Test (pooled):",
           t(pd.DataFrame(flips)) if flips else "none", ""]
    comp = pd.read_csv(test / "ft_comparison.csv")
    rows = []
    for s in subsets_in(comp):
        c = comp[(comp.subset == s)]
        for fault in MEDIUM:
            for k in ("k1", "k2", "k4"):
                x = c[(c.fault == fault) & (c.kset == k) & (c.level == MEDIUM[fault])].iloc[0]
                rows.append({"subset": s, "fault": fault, "k": k[1:], "SVM": x["svm"], "best aug": x[x["best_aug_baseline"]], "A": x["A_det_twin"], "B": x["B_det"],
                             "C": x["C_det"], "Oracle A": x["A_orc_twin"], "Oracle B": x["B_orc"]})
    md += ["## 5. Main comparison per batch (medium severity, Macro-F1)", t(pd.DataFrame(rows)), "",
           "All severities and sets: `ft_comparison.csv`, `ft_vs_best_aug.csv` (columns subset, kset, fault, level).", ""]

    md += ["## 6. Caveats",
           "- Intervals: paired bootstrap over evaluation rows only, so optimistic (fault draw, training set and batch are not resampled).",
           "- G3 passes on a single comparison (lenient); the tables above are the evidence, not the gate.",
           "- The number of Test records flagged by the invalid-value rule was not recorded (decision E1); Test files were read once.",
           "- k=4 sensor groups are a hypothesis. Per-batch rows use the faulted matrices drawn on the pooled Test rows (Stuck reference rows and "
           "Dropout/Random row choices are shared across batches).",
           "- Batch 8 has few rows; per-batch Macro-F1 over the classes present in that batch only."]
    Path(out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"written {out} ({len(md)} blocks)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", default="results/final_test/test")
    ap.add_argument("--out", default="results/final_test/TEST_REPORT.md")
    a = ap.parse_args()
    main(a.test, a.out)
