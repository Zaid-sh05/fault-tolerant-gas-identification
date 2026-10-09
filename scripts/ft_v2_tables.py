"""Tables and verdict of the Test v2 recalibration run (decisions_log N5, N8). Reads scores.csv and detector.csv only.

Usage: python scripts/ft_v2_tables.py [--dir results/final_test_v2/test]
Outputs in the same folder: clean.csv, faults.csv, detector_summary.csv, verdict.json, TABLES.md
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

B_BOOT = 1000


def boot_scen(diff_by_seed, kset_by_seed, rng):
    """Mean over seeds of the k-balanced mean difference; bootstrap resamples scenarios within each k, per seed."""
    pts, boots = [], []
    for d, k in zip(diff_by_seed, kset_by_seed):
        groups = [np.flatnonzero(k == g) for g in ("k1", "k2")]
        pts.append(np.mean([d[g].mean() for g in groups]))
        boots.append([np.mean([d[rng.choice(g, len(g))].mean() for g in groups]) for _ in range(B_BOOT)])
    b = np.mean(boots, axis=0)
    return float(np.mean(pts)), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def main(d):
    df = pd.read_csv(d / "scores.csv")
    det = pd.read_csv(d / "detector.csv")
    clean = df[df.setting == "clean"].pivot_table(index=["subset", "cal_seed", "method"], columns="model", values="f1").reset_index()
    faults = df[df.setting != "clean"]
    rng = np.random.default_rng(0)

    # clean: mean +- std over seeds; (b)-(a) with the per-seed differences (row bootstrap is in clean_ci.csv when computed by ft_v2_recal)
    ct = clean.groupby(["subset", "method"]).agg(a=("a", "mean"), a_std=("a", "std"), b=("b", "mean"), b_std=("b", "std")).reset_index()
    ct["b_minus_a"] = ct["b"] - ct["a"]
    rows = []
    for (sub, model, m), g in faults.groupby(["subset", "model", "method"]):
        per_seed = []
        for s, gs in g.groupby("cal_seed"):
            c = clean[(clean.subset == sub) & (clean.cal_seed == s) & (clean.method == m)][model].iloc[0]
            k_means = [gs[gs.setting == k]["f1"].mean() for k in ("k1", "k2")]
            per_seed.append({"mean_under_faults": np.mean(k_means), "k1": k_means[0], "k2": k_means[1],
                             "worst": min(gs["f1"].min(), c), "retained": float((gs["f1"] / c).mean())})
        ps = pd.DataFrame(per_seed)
        rows.append({"subset": sub, "model": model, "method": m, **{c: ps[c].mean() for c in ps.columns},
                     "mean_under_faults_std": ps["mean_under_faults"].std()})
    ft = pd.DataFrame(rows)

    def scen_diff(sub, x, y):
        diffs, ks = [], []
        for s, gs in faults[faults.subset == sub].groupby("cal_seed"):
            a = gs[(gs.model == x[0]) & (gs.method == x[1])].sort_values("sid")
            b = gs[(gs.model == y[0]) & (gs.method == y[1])].sort_values("sid")
            diffs.append(a["f1"].to_numpy() - b["f1"].to_numpy())
            ks.append(a["setting"].to_numpy())
        return boot_scen(diffs, ks, rng)

    ci = []
    for sub in sorted(df.subset.unique()):
        for m in ("svm", "A", "B"):
            ci.append({"subset": sub, "comparison": f"(b)-(a) {m} under faults", **dict(zip(("diff", "ci_low", "ci_high"), scen_diff(sub, ("b", m), ("a", m))))})
        for model in ("a", "b"):
            ci.append({"subset": sub, "comparison": f"A-SVM under faults, model ({model})",
                       **dict(zip(("diff", "ci_low", "ci_high"), scen_diff(sub, (model, "A"), (model, "svm"))))})
    ci = pd.DataFrame(ci)
    dsum = (det.groupby(["subset", "model", "setting", "fault"])[["auroc", "tpr", "far_clean", "rows_with_alarm_clean"]].mean()
            .reset_index())

    cci = pd.read_csv(d / "clean_ci.csv") if (d / "clean_ci.csv").exists() else None
    pooled = "pooled" if "pooled" in set(df.subset) else sorted(df.subset.unique())[0]
    b_clean = cci[(cci.subset == pooled) & (cci.method == "svm")].iloc[0] if cci is not None else None
    a_vs_svm = ft[(ft.subset == pooled) & (ft.model == "b")].set_index("method")["mean_under_faults"]
    verdict = {"rule": "decisions_log N8", "post_hoc": True, "subset": pooled,
               "clean_b_minus_a_svm": None if b_clean is None else [float(b_clean["diff"]), float(b_clean["ci_low"]), float(b_clean["ci_high"])],
               "calibrated_A_minus_SVM_under_faults": float(a_vs_svm["A"] - a_vs_svm["svm"])}
    verdict["success"] = bool(b_clean is not None and b_clean["ci_low"] > 0 and verdict["calibrated_A_minus_SVM_under_faults"] >= 0)

    ct.round(4).to_csv(d / "clean.csv", index=False)
    ft.round(4).to_csv(d / "faults.csv", index=False)
    ci.round(4).to_csv(d / "faults_ci.csv", index=False)
    dsum.round(4).to_csv(d / "detector_summary.csv", index=False)
    json.dump(verdict, open(d / "verdict.json", "w"), indent=1)
    md = ["# Test v2 tables (POST-HOC; decisions_log N)", "", "## Clean Macro-F1, (a) without and (b) with calibration, same rows", "",
          ct.round(4).to_markdown(index=False), ""]
    if cci is not None:
        md += ["Row-bootstrap intervals of (b)-(a) on clean rows:", "", cci.round(4).to_markdown(index=False), ""]
    md += ["## Under faults (k1, k2; every type and severity; k weighted equally)", "", ft.round(4).to_markdown(index=False), "",
           "Scenario-bootstrap intervals:", "", ci.round(4).to_markdown(index=False), "", "## Detector", "",
           dsum.round(4).to_markdown(index=False), "", "```", json.dumps(verdict, indent=1), "```"]
    (d / "TABLES.md").write_text(chr(10).join(md), encoding="utf-8")
    print(chr(10).join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="results/final_test_v2/test")
    main(Path(ap.parse_args().dir))
