# Previous-period recalibration (v3): report

POST-HOC, EXPLORATORY. The design is in `results/decisions_log.md`, section Q. The pre-registration was committed alone before any result (`fe127f5`, 2026-10-10 00:56:59).

## ملخص بالعربي

**السؤال:** هل المعايرة بعيّنات قليلة بتظل مفيدة إذا أخذنا عيّناتها من **الفترة السابقة** بس، بدون ولا عيّنة معلَّمة من الفترة اللي بنقيّمها؟
- الإعداد: النموذج مدرّب على الدفعات 1–7.
- لتقييم الدفعة 9 بنعايره بعيّنات من الدفعة 8، ولتقييم الدفعة 10 بنعايره بعيّنات من الدفعة 9.

**النتيجة (المعيار الأساسي Q3): مدعومة (SUPPORTED).**
- A تحت الأعطال، الذراع (c) ناقص الذراع (a)، الدفعتان 9 و10 معًا: **+0.0248**، وفترة الثقة 95% **[0.0235، 0.0260]** كلها فوق الصفر.
- الأداء ارتفع من 0.636 إلى 0.661.
- المكسب موجب في كل بذرة معايرة، وفي كل دفعة، ولكل طريقة (SVM وA وB).

**بس المكسب صغير:**
- المعايرة من الفترة السابقة بتحتفظ بحوالي **17%** بس من مكسب المعايرة من نفس الفترة.
  - للطريقة A: +0.025 مقابل +0.147.
  - على البيانات النظيفة: +0.018 مقابل +0.148 لـ SVM.
- على الدفعة 9، الغاز 6 بيضل F1 = 0 بالذراعين (a) و(c). الدفعة 8 فيها 18 عيّنة بس من هالغاز، و9 منها انسحبت للمعايرة.

**طبقة الأعطال بتظل ضرورية فوق المعايرة المنقولة:**
- A أعلى من SVM بـ **+0.107**، وB أعلى منه بـ **+0.118**، والفترتين فوق الصفر.

**وين بتنكسر الذراع (c):**
- بأقل من 4% من السيناريوهات للطريقة A، وأوضحها Bias بشدة 3σ على زوج توأم (S15–S16 على b9: من 0.435 إلى 0.258).
- أسوأ الحالات المطلقة هي نفسها أسوأ حالات v2: إخفاء التوأم S01–S02 وStuck على S09–S10.

**التحقق:**
- **بوابة إعادة الإنتاج نجحت:** الذراعان (a) و(b) طلعوا مطابقين لتشغيل v2 بالضبط، بتسميات متطابقة وفرق F1 أقصاه 1.1e-16.
- **التدقيق المستقل نجح:** وكيل منفصل أعاد حساب المعيار بكوده الخاص وطلعلّه +0.024814 [0.023543، 0.026007]، يعني نفس النتيجة. ما لقى أي مشكلة حرجة، والمشاكل المهمة الثلاث انصلحت.
- **فحص التسرّب:** ولا صف من الدفعة t موجود في تدريب نموذج الذراع (c).

## 1. Primary endpoint (Q3)

| endpoint | value | 95% CI | verdict |
|---|---|---|---|
| A, Macro-F1 under faults, arm (c) − arm (a), pooled b9+b10 | **+0.0248** | **[+0.0235, +0.0260]** | **SUPPORTED** |

The interval is a shared-index scenario bootstrap (k-stratified, 1000 replicates, seed 0). It resamples scenarios only; this is the O2 limitation, registered in Q6. A t-interval over the 5 calibration seeds on the same difference gives about [+0.019, +0.030] (computed by the auditor), which is also above 0. Source: `q3_primary.csv`.

## 2. Three arms, per batch and pooled (Macro-F1; mean over 5 seeds)

(a) = uncalibrated (Train 1–7); (b) = calibrated on batch t; (c) = calibrated on batch t−1. All arms are scored on identical rows. "Under faults" weights k1 and k2 equally.

| subset | quantity | (a) uncal | (b) same period | (c) previous period | (c)−(a) [95% CI] | (c)−(b) [95% CI] |
|---|---|---|---|---|---|---|
| b9 (410 rows) | clean, SVM | 0.736 | 0.981 | 0.744 | +0.008 [0.002, 0.013] | −0.237 [−0.240, −0.234] |
| b9 | faults, SVM | 0.610 | 0.771 | 0.634 | +0.025 [0.021, 0.028] | −0.137 [−0.145, −0.130] |
| b9 | faults, A | 0.706 | 0.940 | 0.730 | +0.024 [0.021, 0.026] | −0.211 [−0.216, −0.206] |
| b9 | faults, B | 0.704 | 0.955 | 0.737 | +0.033 [0.030, 0.036] | −0.218 [−0.222, −0.214] |
| b10 (3540 rows) | clean, SVM | 0.674 | 0.818 | 0.692 | +0.018 [0.011, 0.025] | −0.126 [−0.153, −0.099] |
| b10 | faults, SVM | 0.512 | 0.642 | 0.536 | +0.024 [0.022, 0.025] | −0.106 [−0.108, −0.104] |
| b10 | faults, A | 0.621 | 0.765 | 0.646 | +0.024 [0.023, 0.026] | −0.120 [−0.122, −0.118] |
| b10 | faults, B | 0.629 | 0.784 | 0.657 | +0.028 [0.027, 0.029] | −0.128 [−0.129, −0.126] |
| **pooled** | clean, SVM | 0.686 | 0.834 | 0.704 | +0.018 [0.011, 0.025] | −0.130 [−0.154, −0.106] |
| **pooled** | faults, SVM | 0.529 | 0.658 | 0.554 | +0.025 [0.023, 0.026] | −0.104 [−0.106, −0.102] |
| **pooled** | faults, A | 0.636 | 0.784 | 0.661 | **+0.025 [0.023, 0.026]** | −0.122 [−0.125, −0.120] |
| **pooled** | faults, B | 0.642 | 0.802 | 0.672 | +0.029 [0.028, 0.030] | −0.130 [−0.132, −0.129] |

The arm (b) values equal the v2 Test report (e.g. b9 A 0.9404, b10 A 0.7653), as the reproduction gate requires. Sources: `q4_levels_faults.csv`, `q4_diffs_faults.csv`, `q4_clean.csv`.

**Fault layer on top of previous-period calibration (within arm (c), under faults):**

| subset | A − SVM | B − SVM |
|---|---|---|
| b9 | +0.096 [0.086, 0.106] | +0.103 [0.095, 0.112] |
| b10 | +0.110 [0.101, 0.119] | +0.121 [0.113, 0.130] |
| pooled | **+0.107 [0.099, 0.116]** | **+0.118 [0.110, 0.126]** |

**Share of the same-period gain kept**, ((c)−(a)) / ((b)−(a)) under faults:

| method | b9 | b10 | pooled |
|---|---|---|---|
| SVM | 15% | 18% | 19% |
| A | 10% | 17% | 17% |
| B | 13% | 18% | 18% |

Source: `q4_share_kept.csv`.

**Retention and worst case:**
- Retention follows J6 (k1 and k2 weighted equally). For pooled A it is 0.946 (a), 0.955 (b) and 0.959 (c); for pooled B, 0.944, 0.963 and 0.962.
- Worst case for pooled A is 0.118, 0.137 and 0.102; for pooled B, 0.232, 0.303 and 0.236. Worst case is, per seed, the lowest per-scenario Macro-F1 including clean, then the mean over seeds.
- Source: `q4_retention_worst.csv`, which also has the unweighted retention for comparison with v2.

## 3. Where arm (c) holds and where it breaks

**It holds almost everywhere:**
- The k-balanced (c)−(a) is positive in every seed, batch and method. For pooled A by seed: +0.028, +0.017, +0.028, +0.026 and +0.025.
- Arm (c) is below arm (a) in 3.5% of pooled A scenario–seed pairs (b9: 5.4%, b10: 4.5%) and in 2.4% for pooled B.
- By fault type (pooled A), the gain ranges from +0.021 (dropout, stuck) to +0.032 (k2 bias). Dropout and random are never below (a). Source: `q4_by_fault_c_vs_a.csv`.

**It breaks in strong two-sensor bias on twin pairs.** The largest drops against (a), mean over seeds (source: `q4_largest_drops_c_vs_a.csv`):

| batch | method | scenario | (a) | (c) | (c)−(a) |
|---|---|---|---|---|---|
| b9 | A | k2 bias 3σ, S15–S16 | 0.435 | 0.258 | −0.177 |
| b9 | B | k2 bias 3σ, S15–S16 | 0.561 | 0.432 | −0.129 |
| b9 | B | k2 bias 3σ, S13–S14 | 0.702 | 0.600 | −0.101 |
| b9 | A | k2 bias 3σ, S05–S06 | 0.464 | 0.393 | −0.071 |
| b10 | A | k2 bias 3σ, S15–S16 | 0.367 | 0.304 | −0.064 |

**The worst absolute scenarios of arm (c) are the known v2 failure modes, not new ones** (source: `q4_worst_scenarios_c.csv`):

| batch | method | scenario | (a) | (c) |
|---|---|---|---|---|
| b9 | A | k2 bias 3σ, S01–S02 (twin masking) | 0.037 | 0.048 |
| b10 | A | k2 stuck 1.0, S09–S10 | 0.060 | 0.068 |
| b9 | B | k2 bias 3σ, S01–S02 | 0.399 | 0.353 |
| b10 | B | k2 stuck 1.0, S09–S10 | 0.146 | 0.148 |

**Class-level caveat (from the audit):**
- On b9, gas 6 has F1 = 0 in both arms (a) and (c). Batch 8 has only 18 gas-6 rows, so its calibration uses 9 of them. Arm (b) reaches 0.995 on b9.
- On b10, arm (c) mostly improves gases 1 and 2, but confuses gas 4 with gas 6 more often.

## 4. Verification

**Readiness audit.** All four points were confirmed with file and line evidence (`PLAN.md`):
- Batch 8 gas 6 has 18 rows, so it gets 9 calibration rows; every other gas gets 10.
- The run uses 1081 scenarios.
- All v2 models are present.
- Scored rows come from `keep_mask`.

**Tests first** (`tests/test_v3_prevbatch.py`, 6 tests, all pass):
- No batch-t row is in the arm (c) training or calibration data.
- Saved scores of every arm reproduce on the shared rows.
- The arm (c) detector is the stored t−1 detector and is never refitted.
- Stale chunks are rejected.
- Each test was shown to fail on an injected defect: the same-period model, wrong rows, a detector refit, a stale chunk.

**Smoke test and reproduction gate:**
- Smoke test: 0 label mismatches.
- Arms (a) and (b), recomputed for b9 and b10 on all 1081 scenarios with SVM, A and B, gave labels identical to the saved v2 run.
- Macro-F1 against `results/final_test_v2/test/scores.csv`: 64,860 rows, max |diff| = 1.1e-16. `clean.csv` is equal at its 4 decimals. Source: `gate.json`.

**Run:**
- Arm (c) ran from 01:32:11 to 02:18:12 (`RUN_STARTED`, `RUN_FINISHED`, `run.log`).
- 4,003 reduced B models for acted sets missing from the v2 caches were fitted by the frozen routine into `results/v3_prevbatch/models/`.
- Sampled refits of v2-cached models with the same routine are bit-identical (8/8 here, 3/3 and 5 re-predicted scenarios by the auditor).
- No frozen file, config or v2 cache was modified: the auditor scanned 46,880 files.

**Independent audit** (`AUDIT_SUBAGENT.md`, a fresh subagent that had not seen this analysis):
- It recomputed Q3 with its own code: +0.024814 [0.023543, 0.026007].
- All Q4 tables matched within 5e-7 (rounding), and `scores.csv` matched within 1e-16.
- The timeline is clean: pre-registration, then gate, then run.
- No Critical finding. It raised three Important findings, all fixed after the results without changing any prediction (decisions_log Q8):
  - retention weighting is now J6's;
  - the row-identity test is now one that can fail;
  - chunk provenance is now checked.
- After the fixes, `scores.csv` and `q3_primary.csv` were recomputed byte-identical.
- Blindness caveat, stated by the auditor: it saw the Q3 value in `run.log` during the timeline check, before its own computation.

**Caveats:**
- Post-hoc and test-informed design: batches 8–10 were seen before this experiment, and they were re-opened for it by the user's decision (Q0).
- One calibration draw per seed.
- Batch 10 dominates the pooled rows.
- Intervals resample scenarios only.
- The N9 interleaving caveat applies to arm (b), not to (c): arm (c) has a real time gap.

**Skills.** Loaded and used:
- using-agent-skills, planning-and-task-breakdown, writing-plans, spec-driven-development, constraint-driven-development, constraints and documentation-and-adrs;
- using-git-worktrees: an in-place branch was chosen, because the 13 GB of v2 models are git-ignored;
- test-driven-development, systematic-debugging (the loky pickling failure), observability-and-instrumentation, performance-optimization, requesting-code-review and clean-user-facing-text.

Not loaded separately (their steps were done directly):
- executing-plans, incremental-implementation, debugging-and-error-recovery, dispatching-parallel-agents and subagent-driven-development: one auditor subagent was used;
- code-review:code-review and code-review-and-quality: the review was done by the auditor;
- doubt-driven-development: its checks are in §3 and the audit;
- source-driven-development and finishing-a-development-branch: local only, no merge.

Not created: a root `CONSTRAINTS.md`, because the request limited where new files may go. The floor is recorded in `PLAN.md`.

## 5. Paper-ready paragraph

In an exploratory previous-period evaluation, recalibrating the model with ten labelled samples per gas from the preceding batch alone, without a single label from the evaluated batch, raised the Macro-F1 of the compensating classifier under simulated sensor faults from 0.636 to 0.661 on batches 9 and 10 (+0.025, 95% CI [0.023, 0.026]), and the gain was positive for every calibration draw. Detection and compensation stayed indispensable on top of this carried-forward calibration, adding 0.107 (reconstruction) and 0.118 (exclusion) Macro-F1 over the unprotected SVM. The carried-forward calibration recovered only about one sixth of the gain of calibrating within the evaluated period (+0.147), so drift between consecutive batches erodes most of the benefit, and calibration labels must be refreshed each period to recover it.
