"""Paper material from the finished validation and final-test runs: tables, figures and the list of every number with its source.

Usage: python scripts/ft_paper.py [--test results/final_test/test] [--out results/paper]
Reads only result files (no data, no models). Writes into --out:
  table1_clean_baselines.md/.csv   clean baselines, Validation and Test (pooled and per batch)
  table2_main_comparison.md/.csv   strategies x fault type x k at medium severity, Test pooled, with 95% intervals;
  table2_full.csv                  every cell (fault x severity x k) for every subset (pooled, b8, b9, b10)
  table3_detector.md/.csv          detector isolation AUROC and false-alarm rates (Validation and Test)
  fig1_drift_cost_reconstruction.png, fig2_s01_s02_batches.png, fig3_f1_vs_k.png (Test), fig3_f1_vs_k_validation.png
  PAPER_NUMBERS.md                 every number quoted from these tables with its file and filter
Intervals come from a paired bootstrap that resamples evaluation rows only (optimistic: they ignore the variation of the
fault draw, the training set and the batch); G3 needs a single passing comparison (lenient). Both caveats are repeated in
the tables, and the full comparison is shown rather than the gate result alone.
"""
import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

VAL = Path("results/overnight/temporal")
MEDIUM = {"dropout": 0.5, "bias": 1.0, "stuck": 0.5, "random": 0.5}
FAULTS = list(MEDIUM)
KSETS = ["k1", "k2", "k4"]
STRAT = {"A_det_twin": "A (reconstruct)", "B_det": "B (exclude)", "C_det": "C (pair experts)",
         "A_orc_twin": "Oracle A", "B_orc": "Oracle B"}
CAVEAT = ("Intervals: paired bootstrap over evaluation rows only (1000 resamples), so they are optimistic: they ignore the "
          "variation of the fault draw, of the training set and of the batch. Gate G3 passes if a single comparison passes (lenient).")
NUMBERS = []


def num(label, value, source):
    NUMBERS.append((label, value, source))
    return value


def md_table(df, floatfmt=3):
    return df.to_markdown(index=False, floatfmt=f".{floatfmt}f")


def subsets_in(df):
    return [s for s in ("pooled", "b8", "b9", "b10", "b7") if s in set(df["subset"])]


# ---------------------------------------------------------------------------------------------------------------------
def table1(test, out):
    val = pd.read_csv(VAL / "clean_eval.csv", index_col=0)
    t = pd.read_csv(test / "ft_clean_by_subset.csv")
    subs = subsets_in(t)
    rows = []
    for label, base in (("SVM", "svm"), ("SVM + fault augmentation", "svm_aug"), ("LightGBM", "lgbm"), ("LightGBM + fault augmentation", "lgbm_aug")):
        names = [base] if "aug" not in base else [f"{base[:-4]}_aug{s}" for s in range(5)]
        row = {"model": label}
        v = val.loc[names, "macro_f1"]
        row["Validation (batch 7)"] = f"{v.mean():.3f}" + (f" ± {v.std():.3f}" if len(v) > 1 else "")
        num(f"Validation clean Macro-F1, {label}", float(v.mean()), f"{VAL}/clean_eval.csv, rows {names}, column macro_f1 (mean over rows)")
        for s in subs:
            x = t[(t.subset == s) & t.method.isin(names)]["macro_f1"]
            row[f"Test {s}"] = f"{x.mean():.3f}" + (f" ± {x.std():.3f}" if len(x) > 1 else "")
            num(f"Test clean Macro-F1, {label}, {s}", float(x.mean()), f"{test}/ft_clean_by_subset.csv, subset={s}, methods {names}, column macro_f1 (mean)")
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(out / "table1_clean_baselines.csv", index=False)
    rows_n = t[(t.method == "svm")][["subset", "rows"]].set_index("subset")["rows"]
    for s, n in rows_n.items():
        num(f"Number of evaluation rows, {s}", int(n), f"{test}/ft_clean_by_subset.csv, method=svm, column rows")
    (out / "table1_clean_baselines.md").write_text(
        "**Table 1. Clean (fault-free) Macro-F1 of the reference models.** Augmented models: mean ± std over 5 augmentation seeds. "
        "Models are trained on batches 1-6 only.\n\n" + md_table(df) + "\n\nEvaluation rows: " +
        ", ".join(f"{s} = {n}" for s, n in rows_n.items()) + "\n", encoding="utf-8")
    return df


# ---------------------------------------------------------------------------------------------------------------------
def cell(df, **kw):
    m = np.ones(len(df), dtype=bool)
    for k, v in kw.items():
        m &= (df[k] == v).to_numpy()
    return df[m]


def table2(test, out):
    comp, vs = pd.read_csv(test / "ft_comparison.csv"), pd.read_csv(test / "ft_vs_best_aug.csv")
    comp.to_csv(out / "table2_full.csv", index=False)
    vs.to_csv(out / "table2_full_vs_best_aug.csv", index=False)
    rows = []
    for fault in FAULTS:
        for k in KSETS:
            c = cell(comp, subset="pooled", kset=k, fault=fault, level=MEDIUM[fault]).iloc[0]
            src = f"{test}/ft_comparison.csv, subset=pooled, kset={k}, fault={fault}, level={MEDIUM[fault]}"
            row = {"fault": fault, "k": k[1:], "SVM (no handling)": c["svm"], "best augmented": c[c["best_aug_baseline"]],
                   "best aug. is": c["best_aug_baseline"].replace("_aug", "+Aug").upper()}
            for m, label in STRAT.items():
                row[label] = c[m]
            for m, label in (("A_det_twin", "A"), ("B_det", "B")):
                d = cell(vs, subset="pooled", kset=k, fault=fault, level=MEDIUM[fault], method=m).iloc[0]
                row[f"{label} - best aug. [95% CI]"] = f"{d['diff']:+.3f} [{d['ci_low']:+.3f}, {d['ci_high']:+.3f}]"
                num(f"{label} minus best augmented baseline, {fault}, k={k[1:]}, medium, Test pooled", float(d["diff"]),
                    f"{test}/ft_vs_best_aug.csv, subset=pooled, kset={k}, fault={fault}, level={MEDIUM[fault]}, method={m}, column diff (CI: ci_low, ci_high)")
            for m, label in (("svm", "SVM"), ("A_det_twin", "A"), ("B_det", "B"), ("C_det", "C"), ("A_orc_twin", "Oracle A"), ("B_orc", "Oracle B")):
                num(f"Macro-F1 {label}, {fault}, k={k[1:]}, medium, Test pooled", float(c[m]), src + f", column {m}")
            num(f"Macro-F1 best augmented baseline, {fault}, k={k[1:]}, medium, Test pooled", float(c[c["best_aug_baseline"]]), src + f", column {c['best_aug_baseline']}")
            rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(out / "table2_main_comparison.csv", index=False)
    g3 = json.load(open(test / "ft_verdicts.json"))
    for s, v in g3.items():
        num(f"G3 comparisons passing, {s}", f'{v["cells_passing"]} of {v["comparisons"]}', f"{test}/ft_verdicts.json, {s}, cells_passing / comparisons")
        num(f"G3 passing after Bonferroni, {s}", v["passing_after_bonferroni"], f"{test}/ft_verdicts.json, {s}, passing_after_bonferroni")
        num(f"G1 passes, {s}", v["G1"]["G1_passes"], f"{test}/ft_verdicts.json, {s}, G1.G1_passes")
        for f, d in v["G1"]["k1_medium_mean_drop_by_fault"].items():
            num(f"G1 drop of the best clean baseline, {f}, k=1, medium, {s}", float(d), f"{test}/ft_verdicts.json, {s}, G1.k1_medium_mean_drop_by_fault.{f}")
    (out / "table2_main_comparison.md").write_text(
        "**Table 2. Macro-F1 under sensor faults, Test batches 8-10 pooled, medium severity (Dropout 50% of rows, Bias 1 sigma_robust, "
        "Stuck 50%, Random 50%), mean over sensor sets and 5 fault seeds.** k = number of simultaneously faulty sensors (k=4 groups are a "
        "hypothesis). A, B, C use the real detector; the Oracle rows know the true faulty sensors (upper bound). "
        "Every severity and every batch is in table2_full.csv.\n\n" + md_table(df) + "\n\n" + CAVEAT + "\n", encoding="utf-8")
    return df


# ---------------------------------------------------------------------------------------------------------------------
def table3(test, out):
    g2t = json.load(open(test / "ft_g2_by_subset.json"))
    g2v = json.load(open(VAL / "g2_verdict.json"))
    primary = next(iter(g2t.values()))["primary"]
    cols = {"Validation": g2v["isolation_auroc_by_fault_k1_medium"], **{s: v["detectors"][primary]["by_fault"] for s, v in g2t.items()}}
    rows = []
    for f in FAULTS:
        rows.append({"fault (k=1, medium)": f, **{c: cols[c][f] for c in cols}})
        num(f"Detector isolation AUROC, {f}, Validation", float(cols["Validation"][f]), f"{VAL}/g2_verdict.json, isolation_auroc_by_fault_k1_medium.{f}")
        for s in g2t:
            num(f"Detector isolation AUROC, {f}, Test {s}", float(cols[s][f]), f"{test}/ft_g2_by_subset.json, {s}, detectors.{primary}.by_fault.{f}")
    med = {"fault (k=1, medium)": "median (G2)", "Validation": g2v["median_auroc"], **{s: v["detectors"][primary]["median_auroc"] for s, v in g2t.items()}}
    rows.append(med)
    num("G2 median isolation AUROC, Validation", float(g2v["median_auroc"]), f"{VAL}/g2_verdict.json, median_auroc")
    for s, v in g2t.items():
        num(f"G2 median isolation AUROC, Test {s}", float(v["detectors"][primary]["median_auroc"]), f"{test}/ft_g2_by_subset.json, {s}, detectors.{primary}.median_auroc")
        num(f"G2 passes, Test {s}", v["G2_passes"], f"{test}/ft_g2_by_subset.json, {s}, G2_passes")
        for k, d in v["detectors"].items():
            if k != primary:
                num(f"G2 median AUROC of the sensitivity detector {k}, Test {s}", float(d["median_auroc"]), f"{test}/ft_g2_by_subset.json, {s}, detectors.{k}.median_auroc")
    auroc = pd.DataFrame(rows)
    auroc.to_csv(out / "table3_detector_auroc.csv", index=False)

    far_t = pd.read_csv(test / "ft_far_by_gas.csv")
    far_t = far_t[far_t.detector == primary]
    far_v = pd.read_csv(VAL / "far_by_gas.csv")
    far_v = far_v[far_v.detector == primary]
    rows = []
    for gas in ["all"] + sorted(set(far_t.gas) - {"all"}):
        row = {"gas": gas}
        v = far_v[far_v.gas == gas]
        for label in ("all sensors", "without S01,S02"):
            val = v[v.sensors == label].iloc[0]
            row[f"Val {label}"] = val["alarm_rate_per_sensor_row"]
            num(f"False-alarm rate per sensor-row, {gas}, {label}, Validation", float(val["alarm_rate_per_sensor_row"]),
                f"{VAL}/far_by_gas.csv, detector={primary}, gas={gas}, sensors={label}, column alarm_rate_per_sensor_row")
            for s in subsets_in(far_t):
                x = far_t[(far_t.subset == s) & (far_t.gas == gas) & (far_t.sensors == label)]
                if len(x):
                    row[f"Test {s} {label}"] = float(x.iloc[0]["alarm_rate_per_sensor_row"])
                    num(f"False-alarm rate per sensor-row, {gas}, {label}, Test {s}", float(x.iloc[0]["alarm_rate_per_sensor_row"]),
                        f"{test}/ft_far_by_gas.csv, detector={primary}, subset={s}, gas={gas}, sensors={label}, column alarm_rate_per_sensor_row")
        rows.append(row)
    far = pd.DataFrame(rows)
    far.to_csv(out / "table3_detector_false_alarms.csv", index=False)

    rank = pd.read_csv(test / "ft_reliability_ranking.csv")
    rank = rank[rank.detector == primary]
    rk = rank.pivot(index="rank_from_least_reliable", columns="subset", values="sensor")
    rk.to_csv(out / "table3_reliability_ranking_clean.csv")
    for s in subsets_in(rank):
        top = rank[(rank.subset == s) & (rank.rank_from_least_reliable <= 3)]
        for _, r in top.iterrows():
            num(f"Reliability rank {r.rank_from_least_reliable} (least reliable first), Test {s}: sensor {r.sensor} alarm rate", float(r.alarm_rate),
                f"{test}/ft_reliability_ranking.csv, detector={primary}, subset={s}, rank={r.rank_from_least_reliable}, column alarm_rate")
    (out / "table3_detector.md").write_text(
        f"**Table 3. Reliability detector ({primary} normalisation, thresholds fixed on Train).** (a) isolation AUROC: faulty vs healthy "
        "sensor blocks in the same rows, k=1, medium severity. (b) False-alarm rate on clean rows, per sensor-row, per gas, with and without "
        "the two replicate sensors S01/S02. (c) Sensors ordered from least to most reliable on clean rows.\n\n(a)\n\n" + md_table(auroc) +
        "\n\n(b)\n\n" + md_table(far) + "\n\n(c)\n\n" + rk.reset_index().to_markdown(index=False) + "\n\n" + CAVEAT + "\n", encoding="utf-8")
    return auroc, far


# ---------------------------------------------------------------------------------------------------------------------
def skill_table():
    """Per protocol, sensor, method: skill = 1 - MAE_method / MAE_median (median imputation, same protocol, same sensor, same space).
    Summary over the 16 sensors: median (the S05-S08 anomaly cannot dominate), with the interquartile range."""
    base = "results/preprocessing/phase1/{}/reconstruction_per_sensor.csv"
    rows = []
    for proto, name in (("temporal", "temporal"), ("reference_iid", "reference")):
        d = pd.read_csv(base.format(proto))
        ref = d[d.method == "median"].set_index(["space", "exclude_twin", "sensor"])["mae"]
        d = d.join(ref.rename("mae_median"), on=["space", "exclude_twin", "sensor"])
        d["skill"] = 1 - d["mae"] / d["mae_median"]
        for (m, sp, tw), g in d[d.method.isin(["ridge", "knn"])].groupby(["method", "space", "exclude_twin"]):
            rows.append({"protocol": name, "method": m, "space": sp, "exclude_twin": tw, "skill_median": g["skill"].median(),
                         "skill_q25": g["skill"].quantile(0.25), "skill_q75": g["skill"].quantile(0.75), "r2_median": g["r2"].median()})
    t = pd.DataFrame(rows)
    w = t.pivot(index=["method", "space", "exclude_twin"], columns="protocol", values=["skill_median", "skill_q25", "skill_q75", "r2_median"])
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w.reset_index()
    w["drift_cost_skill"] = w["skill_median_reference"] - w["skill_median_temporal"]
    w["drift_cost_r2"] = w["r2_median_reference"] - w["r2_median_temporal"]
    return w


def fig1(out):
    """Drift cost of reconstruction on a scale that is comparable between the protocols (decisions_log D9, post-hoc):
    skill score against median imputation inside each protocol, and the median R2 over sensors."""
    w = skill_table()
    w.round(4).to_csv(out / "fig1_drift_cost_reconstruction.csv", index=False)
    src = "results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table()"
    for r in w.itertuples():
        tag = f"{r.method}/{r.space}, twin {'missing' if r.exclude_twin else 'available'}"
        num(f"Reconstruction skill (1 - MAE/MAE_median, median over sensors), {tag}, reference protocol", float(r.skill_median_reference), src)
        num(f"Reconstruction skill (1 - MAE/MAE_median, median over sensors), {tag}, temporal protocol", float(r.skill_median_temporal), src)
        num(f"Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), {tag}",
            float(r.drift_cost_skill), src)
        num(f"Median R2 over sensors, {tag}, reference", float(r.r2_median_reference), src)
        num(f"Median R2 over sensors, {tag}, temporal", float(r.r2_median_temporal), src)
        num(f"Drift cost in R2 (R2_reference - R2_temporal), {tag}", float(r.drift_cost_r2), src)
    for twin, name in ((False, "fig1_drift_cost_reconstruction.png"), (True, "fig1_supp_twin_missing.png")):
        s = w[w.exclude_twin == twin].reset_index(drop=True)
        x = np.arange(len(s))
        fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
        for key, ax, ylabel in (("skill_median", axes[0], "skill = 1 - MAE / MAE(median imputation)"), ("r2_median", axes[1], "median R$^2$ over sensors")):
            ax.bar(x - 0.2, s[f"{key}_reference"], 0.4, label="reference (no drift)", color="0.6")
            ax.bar(x + 0.2, s[f"{key}_temporal"], 0.4, label="temporal (real drift)", color="C3")
            if key == "skill_median":
                for off, proto, col in ((-0.2, "reference", "k"), (0.2, "temporal", "k")):
                    ax.errorbar(x + off, s[f"skill_median_{proto}"], yerr=[s[f"skill_median_{proto}"] - s[f"skill_q25_{proto}"], s[f"skill_q75_{proto}"] - s[f"skill_median_{proto}"]],
                                fmt="none", ecolor=col, lw=0.8, capsize=2)
                ax.axhline(0, color="k", lw=0.8)
            ax.set_xticks(x, s["method"] + chr(10) + "(" + s["space"] + ")", fontsize=8)
            ax.set_ylabel(ylabel, fontsize=8)
        axes[0].set_title("skill vs median imputation (bars: median over sensors, whiskers: IQR)", fontsize=8)
        axes[1].set_title("R$^2$ (median over sensors)", fontsize=8)
        axes[0].set_ylim(min(0, axes[0].get_ylim()[0]), 1.25)
        axes[0].legend(fontsize=7, ncol=2, loc="upper center")
        fig.suptitle("twin sensor available" if not twin else "twin sensor also missing (leave-pair-out)", fontsize=9)
        fig.tight_layout()
        fig.savefig(out / name, dpi=200)
        plt.close(fig)


def fig2(test, out):
    pair = pd.read_csv(test / "pair_consistency_by_batch_all.csv")
    alarm = pd.read_csv(test / "sensor_alarm_rate_by_batch.csv")
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for col, k, label in ((0, "spearman", "Spearman correlation within batch"), (1, "median_offset", "median offset log1p|DR|(a) - log1p|DR|(b)")):
        for p, g in pair.groupby("pair"):
            hi = p == "S01-S02"
            ax[col].plot(g["batch"], g[k], color="C3" if hi else "0.75", lw=2.2 if hi else 1, marker="o" if hi else None, label=p if hi else "other replicate pairs" if p == "S03-S04" else None)
        ax[col].axvline(6.5, color="k", ls=":", lw=0.8)
        ax[col].set(xlabel="batch", ylabel=label)
        ax[col].set_xticks(sorted(set(pair["batch"])))
        ax[col].legend(fontsize=7)
    piv = alarm.pivot(index="batch", columns="sensor", values="alarm_rate")
    for s in piv.columns:
        hi = s in ("S01", "S02")
        ax[2].plot(piv.index, piv[s], color={"S01": "C3", "S02": "C0"}.get(s, "0.75"), lw=2.2 if hi else 1, marker="o" if hi else None,
                   label=s if hi else "other sensors" if s == "S03" else None)
    ax[2].axvline(6.5, color="k", ls=":", lw=0.8)
    ax[2].set(xlabel="batch", ylabel="detector alarm rate on clean rows")
    ax[2].set_xticks(sorted(set(alarm["batch"])))
    ax[2].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "fig2_s01_s02_batches.png", dpi=200)
    plt.close(fig)
    for s in ("S01", "S02"):
        for b, v in piv[s].items():
            num(f"Detector alarm rate of {s} on clean rows, batch {b}", float(v), f"{test}/sensor_alarm_rate_by_batch.csv, sensor={s}, batch={b}, column alarm_rate")
    for b, g in pair[pair.pair == "S01-S02"].set_index("batch").iterrows() if False else pair[pair.pair == "S01-S02"].set_index("batch").iterrows():
        num(f"S01-S02 Spearman correlation, batch {b}", float(g["spearman"]), f"{test}/pair_consistency_by_batch_all.csv, pair=S01-S02, batch={b}, column spearman")
        num(f"S01-S02 median offset, batch {b}", float(g["median_offset"]), f"{test}/pair_consistency_by_batch_all.csv, pair=S01-S02, batch={b}, column median_offset")


def fig3(comp, subset, path, source):
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.4), sharey=True)
    style = {"svm": ("SVM (no handling)", "k", "--"), "best_aug": ("best augmented", "0.5", "-."), "A_det_twin": ("A reconstruct", "C0", "-"),
             "B_det": ("B exclude", "C2", "-"), "C_det": ("C pair experts", "C1", "-"), "A_orc_twin": ("Oracle A", "C0", ":"), "B_orc": ("Oracle B", "C2", ":")}
    for ax, fault in zip(axes, FAULTS):
        c = comp[(comp.subset == subset) & (comp.fault == fault) & (comp.level == MEDIUM[fault])].set_index("kset").loc[KSETS]
        c = c.assign(best_aug=[r[r["best_aug_baseline"]] for _, r in c.iterrows()])
        for m, (label, color, ls) in style.items():
            ax.plot([1, 2, 4], c[m], color=color, ls=ls, marker="o", ms=3, label=label)
        ax.set(title=fault, xlabel="k (faulty sensors)")
        ax.set_xticks([1, 2, 4])
    axes[0].set_ylabel("Macro-F1")
    axes[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main(test, out):
    test, out = Path(test), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    table1(test, out)
    table2(test, out)
    table3(test, out)
    fig1(out)
    fig2(test, out)
    fig3(pd.read_csv(test / "ft_comparison.csv"), "pooled", out / "fig3_f1_vs_k.png", test)
    val = pd.read_csv(VAL / "strategy_comparison.csv").assign(subset="pooled")
    fig3(val, "pooled", out / "fig3_f1_vs_k_validation.png", VAL)
    edge = Path("results/edge_cost/edge_cost.json")
    if edge.exists():
        e = json.load(open(edge))
        num("Bundle size of pipeline A (KB)", e["bundle_kb"], f"{edge}, bundle_kb")
        for case in ("fault_free", "bias_one_sensor", "bias_one_sensor_cold_weights"):
            num(f"Latency median, {case} (ms)", e[case]["median_ms"], f"{edge}, {case}.median_ms")
            num(f"Latency p95, {case} (ms)", e[case]["p95_ms"], f"{edge}, {case}.p95_ms")
        num("Peak memory (MB)", e["memory_peak_mb"], f"{edge}, memory_peak_mb")
    lines = ["# Numbers used in the paper and where they come from", "",
             "Every value is read from a result file by `scripts/ft_paper.py`; nothing is typed by hand. " + CAVEAT, "",
             "| number | value | source |", "|---|---|---|"]
    for label, v, src in NUMBERS:
        lines.append(f"| {label} | {v:.4f} | {src} |" if isinstance(v, (float, np.floating)) else f"| {label} | {v} | {src} |")
    (out / "PAPER_NUMBERS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(NUMBERS)} numbers listed in {out / 'PAPER_NUMBERS.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", default="results/final_test/test")
    ap.add_argument("--out", default="results/paper")
    a = ap.parse_args()
    main(a.test, a.out)
