"""v2 paper material + LaTeX tables of v1 and v2. Reads result files only (no experiment, Test data not read).

Usage: python scripts/v2_paper.py
1. results/paper/v2_figure_data.csv: level intervals of the v2 methods (pooled): clean = 95% t-interval over the 5 calibration seeds;
   under faults = scenario bootstrap (stratified by k, 1000, per seed then averaged), from results/final_test_v2/test/scores.csv.
2. Rewrites the "## v2 post-hoc" section of results/paper/PAPER_NUMBERS.md (one number per row, exact locators). The v1 part is not touched.
3. Figures fig4_v2_recalibration.png, fig5_v2_gain_per_batch.png and LaTeX tables results/paper/latex/*.tex. Every number they show is
   looked up by name in PAPER_NUMBERS.md (pn()), so it is listed there; scripts/check_paper_numbers.py verifies both directions.
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, "scripts")
from ft_v2_tables import boot_scen  # noqa: E402

P = Path("results/paper")
PN = P / "PAPER_NUMBERS.md"
V2 = "results/final_test_v2/test"
EDGE1, EDGE2 = "results/edge_cost/edge_cost.json", "results/edge_cost/edge_cost_v2.json"
HEADER = "## v2 post-hoc"
MNAME = {"svm": "SVM", "A": "A", "B": "B"}
SUBSETS = ("b8", "b9", "b10", "pooled")


# ---- 1. derived interval data ---------------------------------------------------------------------------------------------------
def figure_data():
    df = pd.read_csv(Path(V2) / "scores.csv")
    rng = np.random.default_rng(0)
    rows = []
    for (model, m), g in df[df.subset == "pooled"].groupby(["model", "method"]):
        c = g[g.setting == "clean"].groupby("cal_seed")["f1"].first()
        half = 2.776 * c.std(ddof=1) / np.sqrt(len(c))                     # t(0.975, 4)
        rows.append({"subset": "pooled", "model": model, "method": m, "kind": "clean", "value": c.mean(), "ci_low": c.mean() - half,
                     "ci_high": c.mean() + half, "interval": "95% t-interval over 5 calibration seeds"})
        f = g[g.setting != "clean"].sort_values(["cal_seed", "sid"])
        seeds = sorted(f.cal_seed.unique())
        v, lo, hi = boot_scen([f[f.cal_seed == s]["f1"].to_numpy() for s in seeds], [f[f.cal_seed == s]["setting"].to_numpy() for s in seeds], rng)
        rows.append({"subset": "pooled", "model": model, "method": m, "kind": "faults", "value": v, "ci_low": lo, "ci_high": hi,
                     "interval": "95% scenario bootstrap (k-stratified), averaged over seeds"})
    out = pd.DataFrame(rows)
    out.round(6).to_csv(P / "v2_figure_data.csv", index=False)
    return out


# ---- 2. v2 section of PAPER_NUMBERS --------------------------------------------------------------------------------------------
def v2_rows():
    R = []
    clean = pd.read_csv(Path(V2) / "clean.csv")
    for _, r in clean.iterrows():
        for col, lab in (("a", "(a) no calibration"), ("b", "(b) 10 per gas, mean of 5 seeds")):
            R.append((f"v2 clean Macro-F1 {MNAME[r.method]}, {r.subset}, {lab}", r[col], f"{V2}/clean.csv, subset={r.subset}, method={r.method}, column {col}"))
    cci = pd.read_csv(Path(V2) / "clean_ci.csv")
    for _, r in cci.iterrows():
        for col in ("diff", "ci_low", "ci_high"):
            R.append((f"v2 clean gain (b)-(a) {MNAME[r.method]}, {r.subset}, {col}", r[col], f"{V2}/clean_ci.csv, subset={r.subset}, method={r.method}, column {col}"))
    ft = pd.read_csv(Path(V2) / "faults.csv")
    for _, r in ft.iterrows():
        for col in ("mean_under_faults", "k1", "k2", "worst", "retained"):
            R.append((f"v2 {col} {MNAME[r.method]}, model ({r.model}), {r.subset}", r[col],
                      f"{V2}/faults.csv, subset={r.subset}, model={r.model}, method={r.method}, column {col}"))
    fci = pd.read_csv(Path(V2) / "faults_ci.csv")
    for _, r in fci.iterrows():
        for col in ("diff", "ci_low", "ci_high"):
            R.append((f"v2 {r.comparison}, {r.subset}, {col}", r[col], f"{V2}/faults_ci.csv, subset={r.subset}, comparison={r.comparison}, column {col}"))
    fd = pd.read_csv(P / "v2_figure_data.csv")
    for _, r in fd.iterrows():
        for col in ("value", "ci_low", "ci_high"):
            R.append((f"v2 level {r.kind} {MNAME[r.method]}, model ({r.model}), pooled, {col}", r[col],
                      f"results/paper/v2_figure_data.csv, model={r.model}, method={r.method}, kind={r.kind}, column {col}"))
    v = json.load(open(Path(V2) / "verdict.json"))
    R.append(("v2 verdict N8 success", v["success"], f"{V2}/verdict.json, success"))
    e = json.load(open(EDGE2))
    for k, val in e["size_kb"].items():
        R.append((f"v2 edge size (KB), {k}", val, f"{EDGE2}, size_kb.{k}"))
    for c in ("svm_only_fault_free", "A_fault_free", "A_bias_one_sensor", "B_fault_free", "B_bias_one_sensor"):
        for q in ("median_ms", "p95_ms"):
            R.append((f"v2 edge latency {q}, {c}", e[c][q], f"{EDGE2}, {c}.{q}"))
    for k in ("calibration_svm_s", "calibration_detector_s", "calibration_B_136_models_s", "calibration_total_s", "train_data_kb_float64",
              "memory_peak_mb", "calibration_rows", "train_rows_for_calibration"):
        R.append((f"v2 edge {k}", e[k], f"{EDGE2}, {k}"))
    return R


def fmt(v):
    if isinstance(v, (bool, np.bool_)):
        return str(bool(v))
    if float(v).is_integer() and abs(v) >= 1:
        return str(int(v))
    return f"{float(v):.4f}"


def write_v2_section():
    text = PN.read_text(encoding="utf-8")
    v1 = text.split("\n\n" + HEADER)[0].split("\n" + HEADER)[0].rstrip("\n")
    L = ["", "", HEADER, "",
         "SEPARATE SETTING: 'with 10 labeled calibration samples per gas' (few-shot recalibration). POST-HOC and test-informed design "
         "(decisions_log G0, J0, N0); single Test run at tag `frozen-before-test-v2`. Train = batches 1-7, so (a) is NOT the v1 model; do not "
         "compare these numbers with the v1 numbers above. Calibration rows are interleaved in time with the scored rows (optimistic, N9). "
         "Generated by scripts/v2_paper.py.", "", "| number | value | source |", "|---|---|---|"]
    L += [f"| {n} | {fmt(v)} | {s} |" for n, v, s in v2_rows()]
    PN.write_text(v1 + "\n" + "\n".join(L) + "\n", encoding="utf-8")
    assert PN.read_text(encoding="utf-8").startswith(v1)


# ---- lookup ------------------------------------------------------------------------------------------------------------------
def load_pn():
    d = {}
    for line in PN.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith(("| number", "| quantity")):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            d[parts[0]] = parts[1]
    return d


PNV = {}


def pn(name):
    return float(PNV[name])


# ---- 3a. figures -------------------------------------------------------------------------------------------------------------
def figures():
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2), sharey="row")
    for i, kind in enumerate(("clean", "faults")):
        for j, model in enumerate(("a", "b")):
            ax = axes[i, j]
            vals = [pn(f"v2 level {kind} {MNAME[m]}, model ({model}), pooled, value") for m in MNAME]
            lo = [pn(f"v2 level {kind} {MNAME[m]}, model ({model}), pooled, ci_low") for m in MNAME]
            hi = [pn(f"v2 level {kind} {MNAME[m]}, model ({model}), pooled, ci_high") for m in MNAME]
            ax.bar(range(3), vals, color=["#888888", "#1f77b4", "#2ca02c"],
                   yerr=[np.array(vals) - lo, np.array(hi) - vals], capsize=4)
            ax.set_xticks(range(3), list(MNAME.values()))
            ax.set_ylim(0.4, 1.0)
            ax.set_title(("without" if model == "a" else "with 10 labeled samples/gas") + (", clean" if kind == "clean" else ", under faults"),
                         fontsize=9)
            if j == 0:
                ax.set_ylabel("Macro-F1 (Test pooled)")
    fig.suptitle("v2 (post-hoc): few-shot recalibration, Test batches 8-10", fontsize=10)
    fig.text(0.5, 0.005, "clean: 95% interval over 5 calibration seeds; under faults: k=1,2 every type/severity, 95% scenario bootstrap",
             ha="center", fontsize=7)
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig.savefig(P / "fig4_v2_recalibration.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    w = 0.26
    for j, m in enumerate(MNAME.values()):
        v = [pn(f"v2 clean gain (b)-(a) {m}, {s}, diff") for s in SUBSETS]
        lo = [pn(f"v2 clean gain (b)-(a) {m}, {s}, ci_low") for s in SUBSETS]
        hi = [pn(f"v2 clean gain (b)-(a) {m}, {s}, ci_high") for s in SUBSETS]
        ax.bar(np.arange(4) + (j - 1) * w, v, w, label=m, yerr=[np.array(v) - lo, np.array(hi) - v], capsize=3)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(range(4), ["batch 8", "batch 9", "batch 10", "pooled"])
    ax.set_ylabel("clean Macro-F1 gain (b)-(a)")
    ax.legend(fontsize=8)
    ax.set_title("Gain of the recalibration per Test batch (95% paired row bootstrap)", fontsize=9)
    fig.tight_layout()
    fig.savefig(P / "fig5_v2_gain_per_batch.png", dpi=200)
    plt.close(fig)


# ---- 3b. LaTeX tables (IEEE, booktabs) -----------------------------------------------------------------------------------------
def tex_table(path, caption, label, colspec, header, body, source):
    L = [f"% Source: {source}", "% Every number is a row of results/paper/PAPER_NUMBERS.md; generated by scripts/v2_paper.py",
         "\\begin{table}[t]", "\\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\setlength{\\tabcolsep}{4pt}",
         f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", header + " \\\\", "\\midrule"] + [r + " \\\\" for r in body] + [
         "\\bottomrule", "\\end{tabular}", "\\end{table}"]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def f3(name):
    return f"{pn(name):.3f}"


def tables():
    T = P / "latex"
    T.mkdir(exist_ok=True)
    models = ["SVM", "SVM + fault augmentation", "LightGBM", "LightGBM + fault augmentation"]
    body = [f"{m} & {f3(f'Validation clean Macro-F1, {m}')} & " + " & ".join(f3(f"Test clean Macro-F1, {m}, {s}") for s in SUBSETS) for m in models]
    tex_table(T / "tab_v1_clean.tex", "Clean Macro-F1 of the baselines (v1, pre-registered). Train batches 1--6.", "tab:v1clean",
              "lccccc", "Model & Val.\\ 7 & B8 & B9 & B10 & Test pooled", body,
              "PAPER_NUMBERS.md rows 'Validation clean Macro-F1, *' and 'Test clean Macro-F1, *' (ft_clean_by_subset.csv, clean_eval.csv)")
    body = []
    for k in (1, 2, 4):
        for fault in ("dropout", "bias", "stuck", "random"):
            c = f"{fault}, k={k}, medium, Test pooled"
            body.append(f"{fault} & {k} & " + " & ".join(f3(f"Macro-F1 {x}, {c}") for x in
                        ("SVM", "best augmented baseline", "A", "B", "C", "Oracle A", "Oracle B")) +
                        f" & {pn(f'A minus best augmented baseline, {c}'):+.3f} & {pn(f'B minus best augmented baseline, {c}'):+.3f}")
    tex_table(T / "tab_v1_main.tex", "Macro-F1 under faults, medium severity, Test pooled (v1). $\\Delta$: difference to the best augmented "
              "baseline.", "tab:v1main", "llccccccccc",
              "Fault & $k$ & SVM & Aug. & A & B & C & Or.\\,A & Or.\\,B & $\\Delta$A & $\\Delta$B", body,
              "PAPER_NUMBERS.md rows 'Macro-F1 *, medium, Test pooled' and '* minus best augmented baseline' (ft_comparison.csv, ft_vs_best_aug.csv)")
    subs = [("Validation", "Validation"), ("Test b8", "Test b8"), ("Test b9", "Test b9"), ("Test b10", "Test b10"), ("Test pooled", "Test pooled")]
    body = [f"AUROC {fault} & " + " & ".join(f3(f"Detector isolation AUROC, {fault}, {s}") for _, s in subs) for fault in ("dropout", "bias", "stuck", "random")]
    body += ["FAR, all sensors & " + " & ".join(f3(f"False-alarm rate per sensor-row, all, all sensors, {s}") for _, s in subs),
             "FAR, w/o S01, S02 & " + " & ".join(f3(f"False-alarm rate per sensor-row, all, without S01,S02, {s}") for _, s in subs)]
    tex_table(T / "tab_v1_detector.tex", "Reliability detector (v1): isolation AUROC ($k=1$, medium) and false-alarm rate on clean rows.",
              "tab:v1det", "lccccc", "Metric & Val.\\ 7 & B8 & B9 & B10 & Test pooled", body,
              "PAPER_NUMBERS.md rows 'Detector isolation AUROC, *' and 'False-alarm rate per sensor-row, all, *'")
    body = []
    for m in MNAME.values():
        body.append(f"{m} & {f3(f'v2 clean Macro-F1 {m}, pooled, (a) no calibration')} & {f3(f'v2 clean Macro-F1 {m}, pooled, (b) 10 per gas, mean of 5 seeds')}"
                    f" & {pn(f'v2 clean gain (b)-(a) {m}, pooled, diff'):+.3f} [{f3(f'v2 clean gain (b)-(a) {m}, pooled, ci_low')}, "
                    f"{f3(f'v2 clean gain (b)-(a) {m}, pooled, ci_high')}]"
                    f" & {f3(f'v2 mean_under_faults {m}, model (a), pooled')} & {f3(f'v2 mean_under_faults {m}, model (b), pooled')}"
                    f" & {f3(f'v2 retained {m}, model (b), pooled')} & {f3(f'v2 worst {m}, model (b), pooled')}")
    tex_table(T / "tab_v2_recalibration.tex", "Post-hoc v2: few-shot recalibration with 10 labeled samples per gas, Test pooled, same rows for "
              "(a) without and (b) with calibration; Train batches 1--7; mean of 5 calibration seeds. Faults: $k=1,2$, every type and severity. "
              "Calibration rows are interleaved in time with the scored rows (optimistic).", "tab:v2recal", "lccccccc",
              "Method & Clean (a) & Clean (b) & Gain [95\\% CI] & Faults (a) & Faults (b) & Retained (b) & Worst (b)", body,
              "PAPER_NUMBERS.md section 'v2 post-hoc' (results/final_test_v2/test/clean.csv, clean_ci.csv, faults.csv)")
    body = [f"{s.replace('pooled', 'Test pooled').replace('b', 'B') if s != 'pooled' else 'Test pooled'} & "
            + " & ".join(f"{pn(f'v2 clean gain (b)-(a) {m}, {s}, diff'):+.3f} [{f3(f'v2 clean gain (b)-(a) {m}, {s}, ci_low')}, "
                         f"{f3(f'v2 clean gain (b)-(a) {m}, {s}, ci_high')}]" for m in MNAME.values()) for s in SUBSETS]
    tex_table(T / "tab_v2_gain_per_batch.tex", "Post-hoc v2: clean Macro-F1 gain of the recalibration per Test batch (95\\% paired row bootstrap).",
              "tab:v2gain", "lccc", "Batch & SVM & A & B", body, "PAPER_NUMBERS.md rows 'v2 clean gain (b)-(a) *' (clean_ci.csv)")
    body = [f"v1 A (SVM + detector + Ridge) & {pn('Bundle size of pipeline A (KB)'):.0f} & {f3('Latency median, fault_free (ms)')} & "
            f"{f3('Latency p95, fault_free (ms)')} & -- ",
            f"v2 SVM (calibrated) & {pn('v2 edge size (KB), svm_calibrated'):.0f} & {f3('v2 edge latency median_ms, svm_only_fault_free')} & "
            f"{f3('v2 edge latency p95_ms, svm_only_fault_free')} & {pn('v2 edge calibration_svm_s'):.1f}",
            f"v2 A & {pn('v2 edge size (KB), A_bundle_svm_pre_detector'):.0f} & {f3('v2 edge latency median_ms, A_fault_free')} & "
            f"{f3('v2 edge latency p95_ms, A_fault_free')} & {pn('v2 edge calibration_svm_s') + pn('v2 edge calibration_detector_s'):.1f}",
            f"v2 B (136 models, $k\\le2$) & {pn('v2 edge size (KB), B_bundle_pre_detector_136_models'):.0f} & {f3('v2 edge latency median_ms, B_fault_free')} & "
            f"{f3('v2 edge latency p95_ms, B_fault_free')} & {pn('v2 edge calibration_total_s'):.1f}"]
    tex_table(T / "tab_edge.tex", "Edge cost on one laptop CPU core (upper bound): bundle size, single-sample latency (1000 runs) and refit time "
              "of the calibration step. v2 refits on the Train rows plus 60 calibration rows.", "tab:edge", "lcccc",
              "Pipeline & Size (KB) & Median (ms) & p95 (ms) & Calib.\\ refit (s)", body,
              "PAPER_NUMBERS.md rows 'Bundle size of pipeline A (KB)', 'Latency * (ms)', 'v2 edge *' (edge_cost.json, edge_cost_v2.json)")


if __name__ == "__main__":
    figure_data()
    write_v2_section()
    PNV.update(load_pn())
    figures()
    tables()
    print("v2 section rows:", sum(1 for k in PNV if k.startswith("v2 ")), "; figures and tables written")
