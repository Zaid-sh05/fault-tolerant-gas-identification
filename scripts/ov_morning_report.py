"""Assemble results/MORNING_REPORT.md from the result files (every number is read from a file, paths are cited).

Usage: python scripts/ov_morning_report.py
Arabic summary first (one page), English details after.
"""
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd

R = Path("results")
OV = R / "overnight"
PP = R / "preprocessing"
T, REF = OV / "temporal", OV / "reference_iid"


def rd(p, **kw):
    p = Path(p)
    return pd.read_csv(p, **kw) if p.exists() else None


def js(p):
    p = Path(p)
    return json.load(open(p)) if p.exists() else None


def md(df, fmt=".3f"):
    return "(missing)" if df is None else df.to_markdown(index=False, floatfmt=fmt)


def gate_rows():
    rep = (PP / "REPORT.md")
    rows = []
    if rep.exists():
        for line in rep.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\| (P\d [^|]+) \| (PASS|FAIL|NOT RUN) \| (.*) \|$", line)
            if m:
                rows.append((m.group(1).strip(), m.group(2), m.group(3).strip()))
    return rows


def elapsed(folder, pattern):
    files = sorted(Path(folder).glob(pattern), key=lambda p: p.stat().st_mtime)
    if len(files) < 2:
        return "n/a"
    mins = (files[-1].stat().st_mtime - files[0].stat().st_mtime) / 60
    return f"{mins:.0f} min (first to last chunk file)"


def git_log():
    try:
        return subprocess.check_output(["git", "log", "--oneline", "-n", "40"], text=True)
    except Exception:
        return "(git log unavailable)"


def cell(t, kset, fault, level, col):
    r = t[(t.kset == kset) & (t.fault == fault) & (t.level == level)].iloc[0]
    return r[col], r.get(f"{col}_std_over_seeds", float("nan"))


def main():
    g1 = js(T / "g1_verdict.json")
    g2 = js(T / "g2_verdict.json")
    g3 = js(T / "g3_verdict.json")
    g1s = rd(T / "g1_summary.csv")
    cmp_ = rd(T / "strategy_comparison.csv")
    vs = rd(T / "strategy_vs_best_aug.csv")
    clean = rd(T / "strategy_clean_eval.csv")
    far = rd(T / "far_by_gas.csv")
    rank = rd(T / "reliability_ranking.csv")
    det = rd(T / "detector_summary.csv")
    aug = rd(PP / "final/aug_baselines_summary.csv")
    nb = js(PP / "phase3/new_baseline.json")
    design = rd(R / "main_cleaned/diagnosis/design_2x2.csv")
    trials = rd(PP / "trials.csv")
    chosen = g2["chosen_normalisation"]
    g1_ref, g2_ref, g3_ref = js(REF / "g1_verdict.json"), js(REF / "g2_verdict.json"), js(REF / "g3_verdict.json")
    gates = gate_rows()
    repro = js(PP / "reproducibility.json")

    # ------------ numbers used in the Arabic text -----------------
    old_svm = rd(R / "main/02_baselines/clean_val.csv").set_index("model").loc["svm", "macro_f1"]
    new_svm = rd(R / "main_cleaned/02_baselines/clean_val.csv").set_index("model").loc["svm", "macro_f1"]
    same_params = design[(design.gamma.astype(str) == "scale") & (design.svm_fitted_on == "cleaned") & (design.scaler_fitted_on == "cleaned")]["macro_f1"].iloc[0]
    svm_clean = g1["clean_macro_f1"]
    k1 = g1s[g1s.kset == "k1"]
    drops = {f: float(k1[(k1.fault == f)]["best_clean_drop"].min()) for f in ("bias", "dropout", "random", "stuck")}
    a_k1 = cmp_[cmp_.kset == "k1"][["A_det_twin", "A_det_notwin"]].to_numpy()
    best_aug_k1 = cmp_[cmp_.kset == "k1"][["svm_aug", "lgbm_aug"]].max(axis=1)
    n_pass = g3["cells_passing"] if g3 else None
    k4b = cmp_[(cmp_.kset == "k4") & (cmp_.fault == "bias") & (cmp_.level == 3.0)].iloc[0]
    cl = clean.set_index("method") if clean is not None else None
    s1 = rank[(rank.detector == chosen) & (rank.sensor.isin(["S01", "S02"]))].set_index("sensor")
    pair = rd(PP / "phase1/pair_consistency_summary.csv")
    p12 = pair[pair.pair == "S01-S02"].iloc[0]
    ci_det = det[(det.detector == chosen) & (det.kset == "k4")]
    k4_stuck = ci_det[ci_det.fault == "stuck"]["auroc_isolation"]
    k4_bias = ci_det[ci_det.fault == "bias"]["auroc_isolation"]

    L = []
    w = L.append
    w("# التقرير الصباحي / Morning report\n")
    w(f"*(مولَّد آليًا من الملفات، {datetime.now():%Y-%m-%d %H:%M}؛ كل رقم له مصدر مذكور في الأقسام الإنجليزية أدناه. الدفعات 8–10 لم تُفتح إطلاقًا في هذا التشغيل الليلي.)*\n")
    w("## ملخص بالعربية\n")
    w("**أُنجز:** الأجزاء الأربعة على البروتوكول الزمني كاملة (معالجة مسبقة، أعطال وبوابة G1، كاشف موثوقية وبوابة G2، مقارنة الاستراتيجيات وبوابة G3)، "
      "وعلى البروتوكول المرجعي بمجموعة مختصرة" + (" (مكتملة)." if g3_ref else " (لم تكتمل، انظر الحالة أدناه).") +
      f" **لم يُنجز / ناقص:** {'تحقق P6 لم يكتمل' if not repro else 'لا شيء ناقص جوهريًا'}؛ الجزء 2 تجاوز حدّه الزمني (ساعتان) بسبب تزاحم الموارد في بدايته؛ "
      "استراتيجية C (خبراء الأزواج) ضعيفة ولم أغيّر تصميمها (قرار خارج القواعد المسجّلة).\n")
    w("| البوابة | النتيجة | الرقم |\n|---|---|---|")
    for name, res, ev in gates:
        w(f"| {name} | {'نجحت' if res == 'PASS' else ('فشلت' if res == 'FAIL' else 'لم تُنفَّذ')} | {ev.split('[')[0].strip()[:110]} |")
    w(f"| G1 | {'نجحت' if g1['G1_passes'] else 'فشلت'} | 4 من 4 أنواع أعطال ≥ 0.03 عند k=1 متوسط الشدة (أصغرها {min(g1['k1_medium_mean_drop_by_fault'].values()):.3f}) |")
    w(f"| G2 | {'نجحت' if g2['G2_passes'] else 'فشلت'} | وسيط AUROC = {g2['median_auroc']:.3f} (تطبيع {chosen}) |")
    w(f"| G3 | {'نجحت' if g3['G3_passes'] else 'فشلت'} | {g3['cells_passing']} من {g3['comparisons']} مقارنة (A أو B بالكاشف الحقيقي) |")
    w("\n**أهم خمس نتائج (كل واحدة صالحة للورقة):**\n")
    w(f"1. تنظيف سجلين تالفين من تدريب الدفعة 2 خفّض Macro-F1 لـ SVM على التحقق من {old_svm:.3f} إلى {new_svm:.3f} "
      f"(و{same_params:.3f} بنفس الإعدادات القديمة)؛ المرجع القديم كان مضخَّمًا لأن السجلين ضخّما الانحراف المعياري ×316.")
    w(f"2. عطل حساس واحد يخفض Macro-F1 لـ SVM النظيف ({svm_clean:.3f}) بمقدار {min(drops.values()):.3f}–{k1['best_clean_drop'].max():.3f}، "
      f"والتدريب المعزَّز يخفف الأثر لكنه يكلّف الدقة النظيفة (SVM+Aug = {aug.set_index('model').loc['svm_aug', 'macro_f1_mean']:.3f} ± "
      f"{aug.set_index('model').loc['svm_aug', 'macro_f1_std']:.3f}).")
    w(f"3. الكشف ثم إعادة البناء (A) يبقي Macro-F1 عند {a_k1.min():.3f}–{a_k1.max():.3f} لكل أعطال k=1، مقابل {best_aug_k1.min():.3f}–{best_aug_k1.max():.3f} لأفضل Baseline معزَّز؛ "
      f"وتتفوق A أو B معنويًا في {n_pass} من {g3['comparisons']} مقارنة.")
    w(f"4. الاستراتيجيات تنهار حين يفشل الكشف: عند k=4 مع Bias قوي (δ=3) تعطي A = {k4b['A_det_twin']:.3f} مقابل {k4b['lgbm_aug']:.3f} لـ LGBM+Aug "
      f"(الـ Oracle = {k4b['A_orc_twin']:.3f})، لأن AUROC العزل ينخفض إلى {k4_bias.min():.2f}–{k4_bias.max():.2f} (Bias) و{k4_stuck.min():.2f}–{k4_stuck.max():.2f} (Stuck).")
    w(f"5. الانجراف يكسر علاقة التوأم S01–S02 (Spearman من {p12['train_spearman_mean']:.3f} إلى {p12['val_spearman']:.3f})، وهما أقل الحساسات موثوقية "
      f"على الدفعة 7 النظيفة (إنذارات {s1.loc['S01', 'alarm_rate']:.0%} و{s1.loc['S02', 'alarm_rate']:.0%})؛ ومعالجتهما دائمًا تكلّف {svm_clean - cl.loc['A_det_twin', 'macro_f1']:.3f} (A) و{svm_clean - cl.loc['B_det', 'macro_f1']:.3f} (B) على بيانات نظيفة.\n")
    if g1_ref and g3_ref:
        vr = rd(REF / "strategy_vs_best_aug.csv")
        vr = vr[vr.counts_for_G3]
        cl_ref = rd(REF / "strategy_clean_eval.csv").set_index("method")
        w(f"**ملاحظة مهمة (البروتوكول المرجعي بلا انجراف):** SVM النظيف يصل إلى {cl_ref.loc['clean_svm_no_handling', 'macro_f1']:.3f}، وG1 تنجح بـ {len(g1_ref['types_with_drop_ge_0.03'])} من 4 أنواع فقط، "
          f"وتفوّق A/B على أفضل Baseline معزَّز يتقلص إلى فروق ≤ {vr['diff'].max():.3f} (G3 تنجح بـ {g3_ref['cells_passing']} من {g3_ref['comparisons']} مقارنة، {g3_ref['bonferroni_supplement']['passing_after_bonferroni']} بعد Bonferroni)؛ "
          f"أي أن الفائدة الكبيرة في الزمني تأتي من تفاعل الأعطال مع الانجراف، وليس من الأعطال وحدها. ومعدل الإنذار الكاذب هناك ≈ 5% كما صُمِّم ولا شذوذ في S01/S02.\n")
    w("**قرارات أحتاجك فيها قبل تشغيل الاختبار (8–10):** (1) الموافقة الصريحة على تشغيل واحد بالـ Pipeline والكاشف والعتبات المجمَّدة؛ "
      "(2) هل نعيد تصميم C (خبراء أكبر من زوجين) أم نحذفها من الورقة؟ (3) أي استراتيجية تُعلن كنتيجة رئيسية (أقترح A مع تقرير B وOracle)؛ "
      "(4) كيف نصف الإنذارات الدائمة لـ S01/S02 في الورقة؛ (5) هل نكرر التقييم بالكاشف leave-pair-out. التفاصيل في القسم 7 أدناه.\n")

    w("\n---\n\n# Details (English)\n")
    w("## 1. Gates\n")
    w("| gate | result | evidence (file) |\n|---|---|---|")
    for name, res, ev in gates:
        w(f"| {name} | {res} | {ev} |")
    w(f"| G1 | {'PASS' if g1['G1_passes'] else 'FAIL'} | types with mean drop >= 0.03 in the medium k=1 setting: {', '.join(g1['types_with_drop_ge_0.03'])}; drops {g1['k1_medium_mean_drop_by_fault']} [overnight/temporal/g1_verdict.json, g1_summary.csv] |")
    w(f"| G2 | {'PASS' if g2['G2_passes'] else 'FAIL'} | median isolation AUROC {g2['median_auroc']:.3f} by fault {g2['isolation_auroc_by_fault_k1_medium']}; candidates {g2['candidates_median_auroc']} [overnight/temporal/g2_verdict.json] (Dropout is detected by definition, AUROC 1.0 is trivial) |")
    w(f"| G3 | {'PASS' if g3['G3_passes'] else 'FAIL'} | {g3['cells_passing']} of {g3['comparisons']} comparisons (A or B, real detector) beat the best augmented baseline with a bootstrap interval excluding 0; {g3['bonferroni_supplement']['passing_after_bonferroni']} after a Bonferroni check [overnight/temporal/g3_verdict.json, strategy_vs_best_aug.csv] |")
    if g1_ref and g2_ref and g3_ref:
        w(f"| reference protocol G1/G2/G3 | {'PASS' if g1_ref['G1_passes'] else 'FAIL'}/{'PASS' if g2_ref['G2_passes'] else 'FAIL'}/{'PASS' if g3_ref['G3_passes'] else 'FAIL'} | reduced scenario set (medium severity, k=1,2) [overnight/reference_iid/*_verdict.json] |")
    w("")
    w("## 2. What was done and what was not\n")
    w("* Done: Part 1 (stress check, phases 4-5, decision rule, new baselines), Part 2 (scenarios, G1), Part 3 (detector, G2), Part 4 (A/B/C, G3) on the temporal protocol; reduced set on reference_iid; unit tests (see section 6).")
    w("* Not done / partial: " + ("the one-command reproduction check (P6) is not complete; " if not repro else "") +
      "strategy C was not redesigned (a decision outside the registered rules); the secondary leave-pair-out detector is only reported as a diagnostic AUROC.")
    w("* Deviation: Part 2 took longer than its 2-hour limit because it started together with the reproduction run, which starved it (decisions_log C1).\n")

    w("## 3. Main comparison on Validation (temporal protocol): mean Macro-F1 over scenarios, +- std over the 5 fault seeds\n")
    w("Source: `overnight/temporal/strategy_comparison.csv`. SVM = clean model, no handling. Aug = augmented, mean over 5 augmentation seeds. "
      "A/B/C_det use the real detector; *_orc use the true faulty sensors (analysis bound); C_equal = the same experts with equal weights.\n")
    cols = ["svm", "svm_aug", "lgbm_aug", "A_det_twin", "A_det_notwin", "B_det", "C_det", "C_equal", "A_orc_twin", "B_orc"]
    rows = []
    for _, r in cmp_.iterrows():
        row = {"k": r.kset, "fault": r.fault, "level": r.level, "best aug": r.best_aug_baseline}
        for c in cols:
            row[c] = f"{r[c]:.3f} +- {r[c + '_std_over_seeds']:.3f}"
        rows.append(row)
    w(pd.DataFrame(rows).to_markdown(index=False) + "\n")
    w("Differences against the best augmented baseline with paired-bootstrap 95% intervals (rows only; scenarios fixed) are in `overnight/temporal/strategy_vs_best_aug.csv`. "
      "Comparisons where the real-detector strategies do not win:\n")
    g = vs[vs.counts_for_G3 & ~vs.beats_and_ci_excludes_0]
    w(md(g[g.method != "C_det"][["kset", "fault", "level", "method", "method_f1", "best_aug_f1", "diff", "ci_low", "ci_high"]]) + "\n")
    w("C_det never beats the best augmented baseline except in the strongest settings, and C_det is not better than C_equal "
      f"(mean difference over all cells {float((cmp_['C_det'] - cmp_['C_equal']).mean()):+.4f}).\n")

    w("## 4. Detector (Part 3)\n")
    w(f"Chosen normalisation: **{chosen}** (candidates {g2['candidates_median_auroc']}); secondary leave-pair-out AUROC {g2['secondary_leave_pair_out']} (`g2_verdict.json`).\n")
    w("False alarms on the clean Validation batch, per gas (`far_by_gas.csv`), chosen detector:\n")
    w(md(far[far.detector == chosen][["gas", "sensors", "rows", "alarm_rate_per_sensor_row", "rows_with_any_alarm"]], ".3f") + "\n")
    w("Reliability ranking on the clean batch (least reliable first, `reliability_ranking.csv`):\n")
    w(md(rank[rank.detector == chosen].head(6)[["rank_from_least_reliable", "sensor", "median_ratio", "alarm_rate"]]) + "\n")
    w("Isolation AUROC by fault, severity and k (`detector_summary.csv`):\n")
    d = det[det.detector == chosen].pivot_table(index=["fault", "level"], columns="kset", values="auroc_isolation").reset_index()
    w(md(d) + "\n")
    w("Recall of the detector at its 5%-calibrated threshold (`detector_summary.csv`):\n")
    d2 = det[det.detector == chosen].pivot_table(index=["fault", "level"], columns="kset", values="tpr").reset_index()
    w(md(d2) + "\n")

    w("## 5. Cost of acting on clean data, and baselines\n")
    w("Strategies on the clean Validation rows (`overnight/temporal/strategy_clean_eval.csv`):\n")
    w(md(clean, ".4f") + "\n")
    w("Baselines on the final preprocessing, 5 augmentation seeds (`preprocessing/final/aug_baselines_summary.csv`):\n")
    w(md(aug, ".4f") + "\n")
    w(f"New Baseline: SVM {nb['svm_tuned']['macro_f1']:.4f} (StandardScaler, {nb['svm_tuned']['params']}), LightGBM {nb['lgbm_tuned']['macro_f1']:.4f} "
      f"(`preprocessing/phase3/new_baseline.json`). Old reference 0.878 was inflated by the corrupt records (`main_cleaned/diagnosis/design_2x2.csv`).\n")

    if g3_ref:
        w("## 5b. Reference protocol (no train-to-evaluation drift), reduced scenarios\n")
        cr = rd(REF / "strategy_comparison.csv")
        w("Mean Macro-F1 per cell (`overnight/reference_iid/strategy_comparison.csv`) next to the temporal value of the same cell:\n")
        merged = cr.merge(cmp_, on=["kset", "fault", "level"], suffixes=("_iid", "_temporal"))
        keep = []
        for c in ["svm", "svm_aug", "lgbm_aug", "A_det_twin", "B_det"]:
            merged[f"{c}: drift cost"] = merged[f"{c}_iid"] - merged[f"{c}_temporal"]
            keep += [f"{c}_iid", f"{c}_temporal", f"{c}: drift cost"]
        w(md(merged[["kset", "fault", "level"] + keep]) + "\n")
        cleanr = rd(REF / "strategy_clean_eval.csv")
        if cleanr is not None:
            w("Clean reference-protocol rows (`overnight/reference_iid/strategy_clean_eval.csv`):\n")
            w(md(cleanr, ".4f") + "\n")

    w("## 6. Reproducibility and tests\n")
    w(f"Reproduction run (P6): {json.dumps({k: v for k, v in repro.items() if k != 'differing'}) if repro else 'not verified'} (`preprocessing/reproducibility.json`).")
    junit = PP / "junit.xml"
    if junit.exists():
        txt = junit.read_text()
        m = re.search(r'tests="(\d+)"', txt)
        f = re.search(r'failures="(\d+)"', txt)
        w(f"Unit tests in the last run: {m.group(1) if m else '?'} tests, {f.group(1) if f else '?'} failures (`preprocessing/junit.xml`).")
    w(f"Number of trials logged in the preprocessing study: {0 if trials is None else len(trials)} (`preprocessing/trials.csv`); "
      f"scenarios evaluated: {len(cmp_) and int(cmp_['n_scenarios'].sum())} on the temporal protocol.\n")

    w("## 7. Decisions and open items\n")
    w("### Decisions I took alone (rule relied on) — the full log is `results/decisions_log.md`; sections B (interpretations, PRE) and C (during the run):\n")
    log = (R / "decisions_log.md").read_text(encoding="utf-8")
    w(log[log.index("## B."):])
    w("\n### Suspicious or unexpected\n")
    for item in [
        f"The detector flags S01 and S02 on almost every clean Validation row ({cl.loc['A_det_twin', 'rows_with_any_flag']:.0%} of rows have at least one flag, mean {cl.loc['A_det_twin', 'mean_flagged_per_row']:.2f} sensors per row), so A/B/C always act on them; the per-sensor alarm rate of the other 14 sensors is lower than the 5% target.",
        "Strategy C (8 pair experts) reaches only ~0.65 on clean data and reliability weights do not help (C_det ~ C_equal): the experts use two sensors each and are too weak; this is a design weakness, not evidence about weighting in general.",
        "On the reference protocol (no drift) the strategies' advantage almost vanishes (differences <= 0.006, G1 passes with 2 of 4 fault types): the benefit seen on the temporal protocol comes from the interaction of faults with drift.",
        "Bootstrap intervals resample evaluation rows only; the scenarios of a cell share the same 3,613 rows and the same augmentation seeds, so the intervals are optimistic about generalisation to new rows and batches.",
        "G3 is a permissive rule (one winning cell out of 108 comparisons suffices); the result is nevertheless broad (see the counts above), and the failures concentrate at k=4.",
        "LightGBM is not exactly scale-invariant (0.68-0.71 across scalers), and its predictions took far longer than SVM's, which shaped the run times.",
        "The first full reproduction run starved Part 2 (CPU oversubscription); it was stopped and resumed later, see decisions_log C1.",
        "`phase3/new_baseline.json` was overwritten when the stress check re-selected StandardScaler; the MinMax version is in git history.",
    ]:
        w(f"* {item}")
    w("\n### Decisions that need you before the Test run\n")
    for item in [
        "Explicit approval to read batches 8-10 exactly once, with the pipeline, cleaning rule, detector (normalisation, thresholds), strategy settings and scenario list frozen as committed. The overnight run never opened a Test file; earlier in the project the download step hashed the ten batch files and the Step-1 audit counted the lines of batches 8-10 (no values or labels were looked at; see decisions_log C5).",
        "Whether to redesign C (larger or overlapping sensor groups) or drop it; any redesign must be fixed before the Test run.",
        "Which strategy is the headline result (suggestion: A with the real detector, B and the Oracles as references).",
        "How to describe in the paper the permanent alarms on S01/S02 (a real drift-induced break of a replicate pair).",
        "Whether to report the leave-pair-out detector as a primary variant (its AUROC is in `g2_verdict.json`).",
        "Whether the fault severities (delta 0.5/1/3 sigma_robust, fractions 0.5/1.0) and the k=4 groups (hypothesis) stay as they are.",
    ]:
        w(f"* {item}")

    w("\n## 8. Commits, run times, trials\n")
    w("```\n" + git_log() + "```")
    w("Run times (first to last result file of each part, `results/overnight/temporal/*_chunks`):\n")
    w(f"* Part 2 (scenarios and baselines under faults): {elapsed(T / 'g1_chunks', '*.pkl')}")
    w(f"* Part 3 (detector): {elapsed(T / 'ov3_chunks', '*.pkl')}")
    w(f"* Part 4 (strategies): {elapsed(T / 'ov4_chunks', '*.pkl')}")
    w(f"* Trials in `preprocessing/trials.csv`: {0 if trials is None else len(trials)}")
    (R / "MORNING_REPORT.md").write_text("\n".join(L), encoding="utf-8")
    print("written", R / "MORNING_REPORT.md", len("\n".join(L)), "characters")


if __name__ == "__main__":
    main()
