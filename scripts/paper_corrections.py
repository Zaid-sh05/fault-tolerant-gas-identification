"""Post-audit corrections of the paper numbers (decisions_log O). Reads result files only: no Test data, no Test labels, no model.

Usage: python scripts/paper_corrections.py ci      # step 2: corrected v2 intervals -> results/paper/v2_corrected_ci.csv + PN section
       python scripts/paper_corrections.py auroc   # step 3: detector AUROC without Dropout -> results/paper/auroc_no_dropout.csv + PN section
Corrected v2 intervals (the audit found that the old ones averaged INDEPENDENT bootstrap replicates of the 5 calibration seeds):
  under faults : scenario bootstrap, k-stratified, 1000 replicates, ONE resample index per replicate shared by all seeds (seed 0)
  clean        : 95% t-interval over the 5 per-seed values (calibration-draw variance only; the row-sampling part would need the Test
                 labels, which are not read again)
Old PAPER_NUMBERS rows that these replace are kept and their names marked "[superseded: v2 corrected CIs]".
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t

PN = Path("results/paper/PAPER_NUMBERS.md")
V2 = Path("results/final_test_v2/test")
CI_CSV = Path("results/paper/v2_corrected_ci.csv")
AUC_CSV = Path("results/paper/auroc_no_dropout.csv")
SEC_CI, SEC_AUC = "## v2 corrected CIs", "## Detector AUROC without Dropout"
MARK = " [superseded: v2 corrected CIs]"
M = {"svm": "SVM", "A": "A", "B": "B"}


def seed_t(x):
    x = np.asarray(x, float)
    h = t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return x.mean(), x.mean() - h, x.mean() + h


def shared_boot(per_seed, ksets, b=1000):
    """per_seed: (n_seeds, n_scen) per-scenario values; mean over seeds of the k-balanced mean; one index per replicate for every seed."""
    groups = [np.flatnonzero(ksets == k) for k in ("k1", "k2")]
    point = float(np.mean([np.mean([s[g].mean() for g in groups]) for s in per_seed]))
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(b):
        idx = [rng.choice(g, len(g)) for g in groups]
        bs.append(np.mean([np.mean([s[i].mean() for i in idx]) for s in per_seed]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return point, float(lo), float(hi)


def corrected_ci():
    df = pd.read_csv(V2 / "scores.csv")
    clean = df[df.setting == "clean"].pivot_table(index=["subset", "cal_seed", "method"], columns="model", values="f1").reset_index()
    f = df[df.setting != "clean"]
    rows = []
    for (sub, m), g in clean.groupby(["subset", "method"]):
        v, lo, hi = seed_t(g["b"] - g["a"])
        rows.append({"kind": "clean_gain", "subset": sub, "comparison": f"(b)-(a) {m} clean", "value": v, "ci_low": lo, "ci_high": hi,
                     "interval": "95% t over 5 calibration seeds"})
        v, lo, hi = seed_t(g["b"])
        rows.append({"kind": "clean_level", "subset": sub, "comparison": f"{m} model (b) clean", "value": v, "ci_low": lo, "ci_high": hi,
                     "interval": "95% t over 5 calibration seeds"})
        rows.append({"kind": "clean_level", "subset": sub, "comparison": f"{m} model (a) clean", "value": g["a"].mean(), "ci_low": np.nan,
                     "ci_high": np.nan, "interval": "single model: no seed interval"})

    def per_seed(sub, mod, meth):
        s = f[(f.subset == sub) & (f.model == mod) & (f.method == meth)].sort_values(["cal_seed", "sid"])
        seeds = sorted(s.cal_seed.unique())
        return np.stack([s[s.cal_seed == x]["f1"].to_numpy() for x in seeds]), s[s.cal_seed == seeds[0]]["setting"].to_numpy()

    for sub in sorted(f.subset.unique()):
        for m in M:
            (yb, k), (ya, _) = per_seed(sub, "b", m), per_seed(sub, "a", m)
            rows.append({"kind": "faults_diff", "subset": sub, "comparison": f"(b)-(a) {m} under faults", **dict(zip(("value", "ci_low", "ci_high"), shared_boot(yb - ya, k))),
                         "interval": "95% shared-index scenario bootstrap"})
            for mod, y in (("a", ya), ("b", yb)):
                rows.append({"kind": "faults_level", "subset": sub, "comparison": f"{m} model ({mod}) under faults",
                             **dict(zip(("value", "ci_low", "ci_high"), shared_boot(y, k))), "interval": "95% shared-index scenario bootstrap"})
        for mod in ("a", "b"):
            (A, k), (S, _) = per_seed(sub, mod, "A"), per_seed(sub, mod, "svm")
            rows.append({"kind": "faults_diff", "subset": sub, "comparison": f"A-SVM under faults, model ({mod})",
                         **dict(zip(("value", "ci_low", "ci_high"), shared_boot(A - S, k))), "interval": "95% shared-index scenario bootstrap"})
    out = pd.DataFrame(rows)
    out.round(6).to_csv(CI_CSV, index=False)
    check_against_audit(out)
    return out


def check_against_audit(out):
    """The corrected values must reproduce results/audit/ci_impact.md (the audit estimate) at its 4 printed decimals."""
    text = Path("results/audit/ci_impact.md").read_text(encoding="utf-8")
    n = 0
    for line in text.splitlines():
        p = [x.strip() for x in line.strip("|").split("|")]
        if len(p) == 6 and p[1] in M:                                                # clean table: subset, method, diff, reported, t, range
            lo, hi = map(float, re.findall(r"-?\d+\.\d+", p[4]))
            r = out[(out.kind == "clean_gain") & (out.subset == p[0]) & (out.comparison == f"(b)-(a) {p[1]} clean")].iloc[0]
        elif len(p) == 5 and p[0] in ("b8", "b9", "b10", "pooled"):                  # faults table: subset, comparison, diff, reported, shared
            lo, hi = map(float, re.findall(r"-?\d+\.\d+", p[4]))
            r = out[(out.kind == "faults_diff") & (out.subset == p[0]) & (out.comparison == p[1])].iloc[0]
        else:
            continue
        assert abs(r.ci_low - lo) < 6e-5 and abs(r.ci_high - hi) < 6e-5, f"does not reproduce ci_impact.md: {p}"
        n += 1
    assert n == 32, f"expected 32 audit intervals, matched {n}"
    print(f"corrected intervals reproduce all {n} intervals of results/audit/ci_impact.md")


def auroc_no_dropout():
    rows = []
    v1 = pd.read_csv("results/final_test/test/ft_detector_summary.csv")
    v1 = v1[(v1.detector == "median") & v1.kset.isin(["k1", "k2"])]
    val = pd.read_csv("results/overnight/temporal/detector_summary.csv")
    val = val[(val.detector == "median") & val.kset.isin(["k1", "k2"])].assign(subset="Validation")
    for src, d in (("results/overnight/temporal/detector_summary.csv", val), ("results/final_test/test/ft_detector_summary.csv", v1)):
        for (sub, k), g in d.groupby(["subset", "kset"]):
            per_fault = g.groupby("fault")["auroc_isolation"].mean()                # mean over severities, then over fault types
            rows.append({"version": "v1", "subset": sub, "model": "-", "k": k, "with_dropout": per_fault.mean(),
                         "without_dropout": per_fault.drop("dropout").mean(), "source": src})
    v2 = pd.read_csv(V2 / "detector_summary.csv")
    v2 = v2[v2.setting.isin(["k1", "k2"])]
    for (sub, mod, k), g in v2.groupby(["subset", "model", "setting"]):
        per_fault = g.set_index("fault")["auroc"]
        rows.append({"version": "v2", "subset": sub, "model": mod, "k": k, "with_dropout": per_fault.mean(),
                     "without_dropout": per_fault.drop("dropout").mean(), "source": str(V2 / "detector_summary.csv")})
    out = pd.DataFrame(rows)
    out.round(6).to_csv(AUC_CSV, index=False)
    return out


def fmt(v):
    return f"{float(v):.4f}"


def write_section(header, lines):
    text = PN.read_text(encoding="utf-8")
    if header in text:                                                               # idempotent: replace the section
        before, rest = text.split("\n" + header, 1)
        nxt = rest.find("\n## ")
        text = before.rstrip("\n") + ("\n" + rest[nxt:].lstrip("\n") if nxt >= 0 else "")
    PN.write_text(text.rstrip("\n") + "\n\n\n" + header + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def mark_superseded():
    """Mark the old v2 interval rows (kept, not deleted)."""
    lines = PN.read_text(encoding="utf-8").splitlines()
    pat = re.compile(r"^\| (v2 clean gain \(b\)-\(a\) .*, ci_(low|high)|v2 \(b\)-\(a\) .* under faults, .*, ci_(low|high)|"
                     r"v2 A-SVM under faults, model \(.\), .*, ci_(low|high)|v2 level .*, ci_(low|high))( \|)")
    n = 0
    for i, line in enumerate(lines):
        if MARK not in line and pat.match(line):
            lines[i] = pat.sub(lambda m: m.group(0)[:-2] + MARK + " |", line, count=1)
            n += 1
    PN.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return n


def step_ci():
    out = corrected_ci()
    src = lambda r: f"{CI_CSV.as_posix()}, kind={r.kind}, subset={r.subset}, comparison={r.comparison}"  # noqa: E731
    L = ["Post-audit correction (decisions_log O). Replaces the v2 intervals marked '[superseded: v2 corrected CIs]' above (kept, not deleted). "
         "Under faults: shared-index scenario bootstrap over the 5 calibration seeds; clean: 95% t-interval over the 5 seeds "
         "(calibration-draw variance only; row sampling would need the Test labels, not read again). Point estimates are unchanged.",
         "", "| number | value | source |", "|---|---|---|"]
    for r in out.itertuples():
        L.append(f"| v2c {r.comparison}, {r.subset}, value | {fmt(r.value)} | {src(r)}, column value |")
        if not np.isnan(r.ci_low):
            L.append(f"| v2c {r.comparison}, {r.subset}, ci_low | {fmt(r.ci_low)} | {src(r)}, column ci_low |")
            L.append(f"| v2c {r.comparison}, {r.subset}, ci_high | {fmt(r.ci_high)} | {src(r)}, column ci_high |")
    write_section(SEC_CI, L)
    print("superseded rows marked:", mark_superseded(), "; corrected rows:", sum(1 for x in L if x.startswith("| v2c")))


def step_auroc():
    out = auroc_no_dropout()
    L = ["Mean isolation AUROC over the fault types (each type first averaged over its severities), primary 'median' detector. Dropout scores "
         "1.0 by construction (a missing block is +inf), so it is shown with and without it (decisions_log O). v2 has no pooled detector value "
         "(each Test batch has its own model).", "", "| number | value | source |", "|---|---|---|"]
    for r in out.itertuples():
        tag = f"{r.version} {r.subset}" + ("" if r.model == "-" else f" model ({r.model})") + f" {r.k}"
        loc = f"{AUC_CSV.as_posix()}, version={r.version}, subset={r.subset}, model={r.model}, k={r.k}"
        L.append(f"| AUROC {tag}, with Dropout | {fmt(r.with_dropout)} | {loc}, column with_dropout |")
        L.append(f"| AUROC {tag}, without Dropout | {fmt(r.without_dropout)} | {loc}, column without_dropout |")
    write_section(SEC_AUC, L)
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    {"ci": step_ci, "auroc": step_auroc}[sys.argv[1]]()
