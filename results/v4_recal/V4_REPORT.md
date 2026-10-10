# v4: carrying a calibration forward in time — report

POST-HOC, EXPLORATORY. Part 1 is in decisions_log Q9 (secondary, not pre-registered). Part 2 is in section R, pre-registered and committed alone (`283f498`, 2026-10-10 03:27:44) before any R result. Branch `exp/prev-recal-v4`, worktree `../fti-v4`; the main checkout was only read.

## ملخص بالعربي

**القرار R3: NO-GO، يعني ما في تشغيل على Test.** جرّبنا سبع طرق لنقل المعايرة للأمام على بيانات التطوير بس (Drift-Dev: تدريب 1–3، والأزواج 5→6 و6→7)، وولا وحدة وصلت لعتبة +0.010.
- الفائز بالقاعدة هو W1 بـ **+0.0013**.
- أعلى مكسب كان لـ C1 (+0.0027)، بس هو ضمن هامش التعادل 0.002 مع W1، فراح التعادل للأبسط.
- الأوزان الأعلى (W5 وW20) والإسقاط على اتجاهين (C2) والتدريب الذاتي (S30 وS60) ما ساعدوا. C2 ساعد في 5→6 بـ +0.052 وضرّ 6→7 بنفس المقدار تقريبًا، وS30 طلع غير مؤهل لأنه نزّل الأداء النظيف.
- مرحلة Test رفضت تشتغل بسبب NO-GO، وما انفتحت بيانات Test لهالجزء. بتظل نتيجة v3 (القسم Q) هي النتيجة المعتمدة.

**الجزء الأول (Q9، وصفي) فيه أهم اكتشاف: عمر المعايرة بالكاد بيأثر.** مكسب A تحت الأعطال فوق النموذج بدون معايرة:

| المعايرة | عمرها | المكسب |
|---|---|---|
| 8→9 | 1–8 أشهر | +0.024 |
| 9→10 | 6–12 شهر | +0.024 |
| 8→10 (عمرها 13–14 شهر) | 13–14 شهر | **+0.021** |

- يعني خسرنا 0.004 بس مع ستة أشهر زيادة.
- مكسب نفس الفترة (+0.14 إلى +0.23) سببه المعايرة من الدفعة نفسها، وجزء منه متفائل لأنه صفوف المعايرة متداخلة زمنيًا مع الصفوف المقيَّمة (N9). مش سببه إنه المعايرة جديدة.
- **التأثير الكامل للسلسلة:** A في الذراع (c) أعلى من SVM بدون معايرة بـ **+0.132**، وفترة الثقة [0.124، 0.141].

**التحقق:**
- التسجيل المسبق R انعمله commit لحاله قبل أي رقم من R، وقرار R3 انعمله commit لحاله قبل أي محاولة تشغيل Test.
- بوابة التطوير طابقت المرحلة 2 من v2 على 19,240 صف، وأكبر فرق 5.0e-6، وهاد تقريب الملف لخمس خانات.
- 12 اختبار نجحوا، وكل اختبار تسرّب فشل لما زرعنا التسرّب عن قصد (11 تعديل).
- **التدقيق المستقل:** وكيل منفصل حسب نتائج البطولة بكوده الخاص قبل ما يقرأ ملفاتي.
  - طلعلّه نفس الفائز W1 (+0.00133) ونفس القرار NO-GO.
  - طابقت القيم كلها حتى 1e-16، وما لقى مشاكل حرجة.
  - أكد إنه ما صار أي تشغيل Test، وإنه النسخة الرئيسية من المشروع ما انلمست.
  - صحّح عبارة كتبتها عن تأثير الأوزان: هي صحيحة للبذرة 0 بس. سجّلت التصحيح (R8).

## 1. Shelf life of a calibration (Q9, Test batches, descriptive)

Gain over arm (a), uncalibrated. Rows are the v3 kept rows; 5 calibration seeds. Under faults, k1 and k2 are weighted equally, with a 95% shared-index scenario bootstrap; clean values use a 95% t interval over seeds. Source: `part1_shelf_life.csv`.

| calibration | age | target | A under faults, gain [95% CI] | share of same-period gain | clean SVM gain [95% CI] |
|---|---|---|---|---|---|
| same period (b) | 0 (rows interleaved, N9) | b9 | +0.2345 [0.2295, 0.2389] | 100% | +0.2446 [0.2398, 0.2495] |
| same period (b) | 0 (rows interleaved, N9) | b10 | +0.1441 [0.1413, 0.1469] | 100% | +0.1440 [0.1205, 0.1675] |
| 8 → 9 (c) | 1–8 months | b9 | +0.0238 [0.0211, 0.0265] | 10% | +0.0078 [0.0021, 0.0134] |
| 9 → 10 (c) | 6–12 months | b10 | +0.0244 [0.0231, 0.0256] | 17% | +0.0181 [0.0110, 0.0251] |
| **8 → 10 (e)** | **13–14 months** | b10 | **+0.0205 [0.0196, 0.0213]** | 14% | +0.0184 [0.0141, 0.0227] |
| (e) − (c) | 13–14 vs 6–12 months | b10 | −0.0039 [−0.0051, −0.0027] | | |

Batch months come from the UCI documentation: batch 8 = 22–23, batch 9 = 24 and 30, batch 10 = 36.

**Full pipeline, method in arm (c) − SVM in arm (a), under faults** (source: `part1_full_pipeline.csv`):

| | b9 | b10 | pooled |
|---|---|---|---|
| A(c) − SVM(a) | +0.120 [0.110, 0.130] | +0.133 [0.125, 0.142] | **+0.132 [0.124, 0.141]** |
| B(c) − SVM(a) | +0.128 [0.119, 0.137] | +0.145 [0.137, 0.153] | **+0.142 [0.135, 0.150]** |

## 2. Per-batch and pooled Macro-F1 under faults (arms a, b, c, e)

Source: `part1_levels.csv`.

| subset | method | (a) uncal | (b) same period | (c) previous period | (e) two periods back |
|---|---|---|---|---|---|
| b9 | SVM | 0.610 | 0.771 | 0.634 | — |
| b9 | A | 0.706 | 0.940 | 0.730 | — |
| b9 | B | 0.704 | 0.955 | 0.737 | — |
| b10 | SVM | 0.512 | 0.642 | 0.536 | 0.529 |
| b10 | A | 0.621 | 0.765 | 0.646 | 0.642 |
| b10 | B | 0.629 | 0.784 | 0.657 | — |
| pooled | SVM | 0.529 | 0.658 | 0.554 | — |
| pooled | A | 0.636 | 0.784 | 0.661 | — |
| pooled | B | 0.642 | 0.802 | 0.672 | — |

J6 retention (k1/k2 equal) and worst case (source: `part1_retention.csv`):
- Pooled A, retention: 0.946 (a), 0.955 (b), 0.959 (c).
- Pooled A, worst case: 0.118, 0.137, 0.102.
- b10 A for arm (e): retention 0.953, worst case 0.102.

**Worst scenarios of arm (e) on b10** (A, mean over seeds; source: `part1_arm_e_scores.csv`, arm e, method A, with v3 `scores.csv` b10 arms a and c):

| scenario | (a) | (c) | (e) |
|---|---|---|---|
| k2 stuck 1.0, S09–S10 | 0.060 | 0.068 | 0.104 |
| k2 bias 3σ, S01–S02 (twin masking) | 0.128 | 0.109 | 0.115 |
| k2 stuck 1.0, S09–S10 (another fault seed) | 0.138 | 0.151 | 0.139 |

The older calibration (e) falls furthest behind (c) on k2 bias 3σ of twin pairs: S09–S10 drops from 0.388 to 0.252, and S13–S14 from 0.374 to 0.247.

## 3. Dev tournament (R1–R3; Drift-Dev, targets 6 and 7, seeds 0–4, 481 scenarios)

Source: `tournament.csv`, `r3_decision.json`.

| configuration | rows | A under faults | prev-analog, same rows | Δ vs prev (t6 / t7) | clean SVM − prev | eligible |
|---|---|---|---|---|---|---|
| uncal (reference) | keep | 0.6297 | 0.7388 | −0.1091 (−0.020 / −0.198) | −0.128 | — |
| same period (reference) | keep | 0.9176 | 0.7388 | +0.1788 (+0.290 / +0.068) | +0.195 | — |
| **W1** memory, unweighted | keep | 0.7401 | 0.7388 | **+0.0013** (0.000 / +0.003) | +0.003 | yes |
| W5 | keep | 0.7370 | 0.7388 | −0.0018 (0.000 / −0.004) | +0.004 | yes |
| W20 | keep | 0.7351 | 0.7388 | −0.0036 (0.000 / −0.007) | +0.001 | yes |
| C1 drift direction removed | keep | 0.7415 | 0.7388 | +0.0027 (+0.006 / −0.000) | +0.007 | yes |
| C2 | keep | 0.7370 | 0.7388 | −0.0018 (+0.052 / −0.055) | +0.001 | yes |
| S30 self-training | H2 | 0.7220 | 0.7363 | −0.0143 (−0.011 / −0.018) | −0.007 | **no** |
| S60 | H2 | 0.7352 | 0.7363 | −0.0010 (−0.006 / +0.004) | +0.007 | yes |

**R3 decision: NO-GO.**
- Best Δ: C1, +0.0027.
- Tie set within 0.002 of the best: {W1, C1}. W1 comes first in the order, so it wins with +0.0013, below the 0.010 threshold.
- W1 equals prev on target 6 (built-in check: true).

The Test stage refused to start (`test_stage_refusal.log`): no marker was written and no Test data was opened for R. **R5: no number (no Test run).**

**Doubt checks:**
- *W5/W20 show exactly 0.0000 on target 6.* The weights do reach the SVM: at w=20 the support set changes and the dual coefficients move by up to 16.9; scikit-learn 1.8.0 documents `sample_weight` as "Rescale C per sample". For seeds 1, 3 and 4 the weighted SVM is identical to the unweighted one. Seeds 0 and 2 change a handful of labels; for seed 0, 5 of 2,300 clean batch-6 labels change, and only 1 of 13 batch-5 support vectors sits at the bound C. (The first version of this note generalized seed 0; the audit corrected it, decisions_log R8.)
- *C2 helps 5→6 by +0.052 and hurts 6→7 by −0.055.* The removed directions fit one drift step and not the next: unstable, rejected by the rule.
- *On dev, previous-period calibration helps target 7 a lot* (prev − uncal +0.198 on t7, +0.020 on t6), *unlike Test.* Batch 5 has no toluene rows, so 5→6 lacks a class.

## 4. Verification

- **Isolation.** New worktree `C:\Users\Admin\fti-v4` on branch `exp/prev-recal-v4`.
  - Imports resolve to the worktree (`PYTHONPATH`; bytecode writes disabled).
  - v2 models and v3 predictions are read through absolute paths, read-only.
- **Tests first** (`tests/test_v4_recal.py`, 12 pass):
  - Part 1: arm (e) is the b8 model without batch-10 rows; v3 rows; v4 prediction reproduces v3 arm (c) labels; stale v3 chunks are rejected.
  - Part 2: (1) no batch-t label in any candidate fit; (2) H1/H2 disjoint and no H2 row in any fit; (3) identical scored rows across compared arms, and saved dev scores rescore on them; (4) dev never reads batches 8–10, and the Test stage runs once; (5) drift directions come from Train + past calibration only; memory sets exclude the target.
  - All 11 injected defects are caught (`mutation_checks.md`).
- **Gates.**
  - Smoke test: 5 scenarios, max |diff| 4.5e-6.
  - Dev gate: 19,240 rows equal v2 stage 2, max |diff| 5.0e-6.
  - The R4 Test gate was not reached (NO-GO).
- **Commit order.**
  - `78ed276`: slice 1 code.
  - `dc0b85f`: Part 1 + Q9.
  - `283f498`: R, alone.
  - `f204166`: candidate code + tests.
  - `6eb03a6`: dev gate.
  - `8a397a1`: R3 decision, alone.
  - `c4d543d`: NEGATIVE_RESULTS + R7.
  - `67a7c6d`: PAPER_NUMBERS_v4.

## 5. Independent audit (`AUDIT_SUBAGENT.md`)

A fresh subagent on a different model tier audited the branch. It had not seen this analysis, and it computed its numbers before opening the author's files.

**Exposure it disclosed:** the required `git log` showed the subject of the decision commit, and a header grep showed fragments of R7. It opened no embargoed file early.

**Timeline and isolation hold:**
- R (`283f498`, 03:27:44) touches only `decisions_log.md` and precedes the first dev prediction (03:32:47), `devgate.json` and `DEV_STARTED`.
- R0–R6 were never edited later.
- The decision commit (04:39:41) precedes the only Test-stage call (04:39:50), which refused.
- There is no `test/` or `preds/test/` folder, and none was ever created.
- In the main checkout, nothing is newer than the start of v4 outside `.git`. Its status, branch tips and tags are unchanged.

**Tests:** 12 pass, and each guards what it claims. Minor gaps:
- test_4 could miss Test data read through an already-cached `test_data()`;
- no unit test checks that `job_e` loads b8 (the audit verified it from the labels);
- test_4b covers only the marker.

**Recomputation:**
- Its own R3 implementation gives winner W1 (+0.00133) and NO-GO.
- `tournament.csv` matches within 5e-7; all 125,060 values of `dev_scores.csv` match within 1e-16.
- Refits of prev, W1, W5, C1 and S60 from the R2 text reproduce the saved labels exactly.
- Part 1 (e) − (a) on b10 = +0.0205 [0.0196, 0.0213], identical to mine.

**Code review:** no Critical finding. One Important finding: saved predictions are reused if the file exists, with no check against the current code.
- Classified as a valid trade-off, not fixed. The run is complete and nothing will reuse these files, and the refits above show the cached labels equal fresh fits of the R2 recipe.
- Minor: `w1_check` is recorded but does not stop the run; `DEV_STARTED` is not checked; some small writes are not atomic.

**Doubts it raised:**
- W5/W20 near-identity: correct, but my explanation generalized seed 0; corrected in R8.
- C2 instability: real, not a bug.
- Timing of R (committed 33 s after the Part 1 numbers were written): the R text was drafted in the session scratchpad at 03:19:34, before Part 1 finished (03:27:11), and committed byte-identical. This is local file evidence, not git evidence; R0 already declares the design test-informed.

**Cross-model review:** skipped and announced; the brief said run without stopping to ask, and the audit subagent was the fresh-context reviewer.

**Verdict: the R3 decision (NO-GO) stands, and the "no Test run" claim is true.**

## 6. Paper-ready paragraph

The request asked for the clause "selected on development batches, evaluated once". No method qualified for Test, so the clause is adapted to say what happened.

Previous-period recalibration proved durable: in a post-hoc shelf-life analysis, a calibration taken 13–14 months before the evaluated batch still raised the Macro-F1 of the compensating classifier under simulated sensor faults by 0.021 (95% CI [0.020, 0.021]), against 0.024 for calibrations one to twelve months old. With that carried-forward calibration, the complete detect–compensate–recalibrate pipeline exceeded the uncalibrated, unprotected SVM by 0.132 Macro-F1 under faults (95% CI [0.124, 0.141]). Seven strategies for carrying the calibration forward more effectively (accumulated and up-weighted calibration memory, removal of estimated drift directions, and confidence-based self-training) were to be selected on development batches and evaluated once on Test, but none added the pre-registered 0.010 Macro-F1 on the development batches (best +0.003), so none reached Test. The remaining gap to same-period calibration, 0.12 to 0.21 Macro-F1, was not narrowed by any of these past-label or label-free strategies.
