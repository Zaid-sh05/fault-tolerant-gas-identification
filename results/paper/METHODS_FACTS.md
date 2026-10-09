# Methods facts (for the paper's Methods section)

Read-only extraction from the code, configs and result files (2026-10-09). No experiment was run and no Test data or label was read.
Every fact gives its source as `file:line` or `file, key`. "NOT FOUND" = not recorded anywhere in the repository; nothing is guessed.
"v1" = pre-registered study (Train 1-6, Validation 7, Test 8-10); "v2" = few-shot recalibration (Train 1-7 + calibration rows of each Test batch).

---

## 1. Preprocessing (classifier path)

| fact | value | source |
|---|---|---|
| Final pipeline spec | `{clip: none, slog: false, scaler: standard, groups: [], select: none}` | `results/overnight/final_pipeline.json:2-8`; `results/preprocessing/decisions.json, final_pipeline.spec` |
| Order of the steps (general pipeline) | raw 128 -> clip -> build features (optional slog of the raw block + engineered groups) -> scale -> select -> NaN fill | `src/preprocessing.py:1`, `src/preprocessing.py:212-223`; `configs/preprocessing.yaml:48` |
| Steps actually active with the final spec | (1) StandardScaler on the raw 128 features (mean/std of the cleaned Train rows); (2) NaN -> 0 (= Train mean after standardisation) before the SVM | `src/preprocessing.py:215-223`, `src/preprocessing.py:51-53`; `src/study.py:37` (fit on Train), `src/study.py:51`, `src/study.py:75` (fill before SVM) |
| Is slog used in the classifier path? | **No** (`slog: false`). Clip, engineered groups and drift selection are also off | `results/overnight/final_pipeline.json:3-7` |
| Definition of slog (where it is used) | `slog(x) = sign(x) * log1p(|x|)` | `src/models.py:12-13` |
| Where slog IS used | detector space and strategy-A reconstruction: `z = (slog(x) - mu) / sd`, mu/sd of slog(Train) per feature; inverse `sign(y) * expm1(|y|)` with `y = z*sd + mu` | `src/detector.py:30-31`, `src/detector.py:43-45`, `src/detector.py:127-130` |
| How the spec was chosen | pre-registered phases on Validation 7: Phase 2 keep_all (no clipping), Phase 3 MinMax won but the stress check re-selected StandardScaler, Phase 4 no group adopted, Phase 5 no drift filter | `results/preprocessing/decisions.json, history`; `results/decisions_log.md:16-18` (A6-A8) |
| Data cleaning before any fit | invalid-value rule, see item 7 | `src/splits.py:55-68` |
| LightGBM path | same preprocessing without the NaN fill (LightGBM handles NaN) | `src/study.py:49-51` |

## 2. SVM

| fact | value | source |
|---|---|---|
| Kernel | RBF | `src/study.py:44`; `src/evaluate.py:36` |
| C | 10 | `results/overnight/final_pipeline.json:10`; `results/preprocessing/decisions.json, new_baseline.svm_tuned.params` |
| gamma | 0.01 (numeric, not "scale") | `results/overnight/final_pipeline.json:11` |
| Other settings | `random_state=0` (config `seed: 0`), sklearn defaults otherwise (no class weights, no probabilities) | `src/study.py:33`, `src/study.py:44`; `configs/preprocessing.yaml:12` |
| Grid searched | C in {1, 10, 100} x gamma in {scale, 0.01} (6 points) | `configs/preprocessing.yaml:37` |
| Selection data | Macro-F1 on **Validation batch 7** (Train 1-6, cleaned), one preprocessor fit shared by all grid points; best = highest Validation Macro-F1 (0.8590) | `src/evaluate.py:92-108`; `scripts/pp3b_minmax_stress.py:86-91`; `results/preprocessing/decisions.json, new_baseline.svm_tuned` |
| Setting used during the pipeline comparison (before tuning) | C=10, gamma=scale | `configs/preprocessing.yaml:35` |
| v2 | same C and gamma, not re-tuned | `scripts/ft_v2_recal.py:85-87`; `results/decisions_log.md` N2 (line 380) |
| Prediction implementation | `fast_svm_predict` (BLAS kernel + libsvm one-vs-one voting, tested equal to `SVC.predict`) | `src/fastsvm.py:1-29` |

## 3. Reliability detector

| fact | value | source |
|---|---|---|
| Model | per sensor, Ridge regression **without intercept** in the slog-standardised space; target = the sensor's 8 features; predictors = the 120 features of the other 15 sensors | `src/detector.py:1-12`, `src/detector.py:33-39`, `src/detector.py:79-85` |
| Alpha grid | {0.01, 0.1, 1, 10, 100, 1000} | `src/detector.py:20` |
| Alpha choice | per sensor, lowest mean held-out MSE over the leave-one-group-out folds of Train (computed from Gram matrices) | `src/detector.py:52-66` |
| Selected alpha (v1, S01..S16) | 100, 100, 100, 100, 100, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 1 | `results/overnight/ov3_temporal.log:1`; `results/final_test/run.log:49` (same) |
| Selected alpha (v2 Test models) | NOT FOUND (not printed or stored outside the fitted joblib files) | - |
| Residual score of a sensor in a row | mean over its 8 features of `|prediction - value|` (z space); NaN predictors are set to 0; a block with any NaN scores +inf | `src/detector.py:88-98` |
| Normalisation used ("median") | score / median of the 16 sensor scores of the same row | `src/detector.py:100-104`; chosen on Validation: `results/overnight/temporal/g2_verdict.json, chosen_normalisation` = median; rule `scripts/ov3_detector.py:106-113` |
| Threshold | per sensor, **95th percentile** of its OOF normalised scores; alarm if score/threshold > 1 | `src/detector.py:26` (`pct=95.0`), `src/detector.py:73-75`, `src/detector.py:113-118` |
| OOF folds (v1) | leave-one-**batch**-out over Train batches 1, 2, 3, 4, 5, 6 (6 folds): the detector is fitted with `groups = Train batch id` | `scripts/ov3_detector.py:84`; `src/splits.py:81` and `src/splits.py:107` (groups = `tr["batch"]`) |
| Discrepancy to note | `decisions_log` B5 says alpha by "leave-batch-group-out" and the config lists inner folds `[[1],[2],[3],[4,5],[6]]`, but the detector receives the batch ids, so batches 4 and 5 are separate folds (6 folds, not 5) | `results/decisions_log.md:42`; `configs/preprocessing.yaml:10` vs `scripts/ov3_detector.py:84` |
| OOF folds (v2) | batches 1..7 each one fold + the calibration rows as one extra group (`1000 + batch`): 8 folds | `scripts/ft_v2_recal.py:173`, `scripts/v2_recal.py:33` |
| Final weights | refitted on all Train rows with the chosen alpha | `src/detector.py:76`, `src/detector.py:79-85` |
| v1 Test | detectors not refitted (Validation-time objects, hash-checked copies) | `results/decisions_log.md:86-89` (D1) |

## 4. Fault scenarios

| fact | value | source |
|---|---|---|
| Injection point | RAW 128 features of a clean copy of the evaluation rows, whole 8-feature sensor blocks, after the split; same faulted matrix for every method | `src/scenarios.py:1-14`; `results/decisions_log.md:30-37` (B3) |
| Severity levels | dropout {0.5, 1.0}; bias {0.5, 1.0, 3.0}; stuck {0.5, 1.0}; random {0.5, 1.0} | `src/scenarios.py:30` |
| Meaning of fraction 0.5 / 1.0 (dropout, stuck, random) | each evaluation row is affected independently with probability = level (`rng.random(n) < level`); 0.5 = about half the rows (random count), 1.0 = every row | `src/scenarios.py:89` |
| Dropout | affected rows: block -> NaN | `src/scenarios.py:93-94` |
| Stuck | affected rows: block frozen to the raw values of ONE evaluation row drawn at random per scenario (`ref = rng.integers(n)`) from the same clean evaluation matrix | `src/scenarios.py:90-91`, `src/scenarios.py:95-96` |
| Stuck reference row pool | v1 Validation: all 3613 rows of batch 7; v1 Test: the pooled Test matrix (batches 8-10 together, 4364 rows); v2: the full batch being evaluated (incl. its calibration rows) | `src/study.py:36`; `results/final_test/run.log:4` (eval 4364); `scripts/ft_v2_recal.py:106` |
| Random | affected rows: independent uniform draws per cell in [p1, p99] of the cleaned Train feature | `src/scenarios.py:97-98`, `src/scenarios.py:57` |
| Bias | ALL rows: `x + sign * delta * sigma_robust`; delta in {0.5, 1, 3}; ONE random sign per scenario shared by the sensors of the set | `src/scenarios.py:83-87` |
| sigma_robust | IQR / 1.349 per feature from the cleaned Train rows (plain std if IQR = 0) | `src/scenarios.py:52-58`; `configs/preprocessing.yaml:20-24` |
| "Medium" severity | dropout 0.5, bias 1.0 sigma, stuck 0.5, random 0.5 | `src/scenarios.py:31`; `results/decisions_log.md:26` (B1) |
| shared_rows | the affected rows are drawn once per scenario and are the same for every sensor of the set | `src/scenarios.py:11`, `src/scenarios.py:89` (rows drawn before the sensor loop) |
| Sensor sets | k=1: the 16 sensors; k=2: the 8 replicate pairs (S1-S2, ..., S15-S16); k=4: {1,2,9,10}, {3,4,11,12}, {5,6,13,14}, {7,8,15,16} (hypothesis) | `src/scenarios.py:25-29` |
| Fault seeds | 0-4 | `src/study.py:23` (`AUG_SEEDS`, passed to `build_scenarios`) ; `scripts/ov3_detector.py:88` |
| Total scenarios v1 | 28 sets x 9 levels x 5 seeds = **1260** (Validation and Test each) | `results/overnight/temporal/scenarios.csv` (1260 rows); `results/final_test/run.log:4` |
| Reference (IID) protocol | 480 (medium only, k=1 and k=2) | `results/decisions_log.md:75` (C2) |
| v2 per batch | 1 clean + 720 (k=1) + 360 (k=2) = 1081 | `results/decisions_log.md:391` (N5); `scripts/ft_v2_recal.py:70-72` |

## 5. Strategies

| fact | value | source |
|---|---|---|
| Which variant is "Strategy A" in the paper | `A_det_twin`: real detector, twin sensor allowed as a predictor | `scripts/ft_paper.py:30` |
| Strategy A, what is replaced | in every row, the 8 raw features of each flagged sensor (at most 4 per row, the 4 with the highest score/threshold ratio) are replaced | `src/strategies.py:3-5`, `src/strategies.py:24`, `src/strategies.py:28-36`, `src/strategies.py:56-64` |
| Strategy A, by which model | the detector's own Ridge in slog-standardised space, refitted on all Train rows with that sensor's alpha, using only the sensors NOT flagged in that row (NaN set to 0); prediction mapped back to raw scale; then the unchanged preprocessing and the clean SVM | `src/detector.py:121-130`; `src/strategies.py:57-68` |
| Strategy B | one RBF SVC per distinct excluded set (same C=10, gamma=0.01, random_state), trained on the Train rows **after** the full StandardScaler (fitted on all 128 features) with the excluded sensors' 8 columns removed; scaler not refitted; cached per set; same cap of 4 sensors | `src/strategies.py:71-98`; `results/decisions_log.md:76-78` (C3) |
| Oracle | the same A and B, but the acted-on sensors per row are the TRUE faulty ones from the scenario truth mask (analysis bound only) | `scripts/ov4_strategies.py:8`, `scripts/ov4_strategies.py:53-57`; `src/scenarios.py:13-14` |
| Strategy C (negative result) | 8 pair experts (SVC, C=10, gamma=scale, probabilities), weights `1/max(1, ratio)^2`, minimum over the pair | `src/strategies.py:101-135`; `results/decisions_log.md:76-78` (C3) |

## 6. Fault-augmented baselines

| fact | value | source |
|---|---|---|
| Amount | `copies: 1`: Train + one augmented copy of every Train row (augmented set = 2 x Train; half of it faulty) | `configs/preprocessing.yaml:28-30`; `src/faults.py:72-89`; `src/study.py:65` |
| Faults in the augmented copy | each row: ONE sensor drawn uniformly from 16, fault type drawn uniformly from {dropout, bias, stuck} (1/3 each; "random" not used); bias `+- U(0.5, 3.0) * sigma_robust`; stuck = that sensor's block from a random Train row | `src/faults.py:72-89`; sigma passed: `src/study.py:57`, `src/study.py:65` |
| aug0 ... aug4 | **five** models per classifier (not four): identical except the augmentation random seed (0-4); reported as their mean (+- std) | `src/study.py:23`, `src/study.py:60-66`; `configs/preprocessing.yaml:26-29` |
| Classifiers | SVM+Aug and LGBM+Aug (LightGBM 31 leaves, 400 trees, lr 0.05) | `src/study.py:59-66`; `results/overnight/final_pipeline.json:13-18` |
| "Best augmented baseline" | per setting (k x fault x level): whichever of SVM+Aug and LGBM+Aug (mean over the 5 seeds) has the higher mean Macro-F1 **on the evaluation rows of that setting** (not chosen in advance) | `scripts/ov4_analysis.py:92-95`; `results/decisions_log.md:61` (B10) |

## 7. Invalid-record rule

| fact | value | source |
|---|---|---|
| Condition | cell invalid if `|x - median_f| / MAD_f > 1000` (median and unscaled MAD of the Train rows of the protocol); record invalid if any of its 128 cells is; MAD = 0 features never flagged (none occur) | `src/cleaning.py:8-12`, `src/cleaning.py:20-43`; `configs/preprocessing.yaml:17-18` |
| Action | flagged Train records dropped before any fit; evaluation records never dropped (only counted) | `src/splits.py:55-68`; `src/cleaning.py:14-16` |
| Dropped, v1 (Train 1-6) | **2** of 5933 (batch 2 line 222 Ethanol; batch 2 line 380 Ethylene) -> 5931 Train rows | `results/preprocessing/cleaning/invalid_summary.json, temporal`; `results/preprocessing/DATA_CLEANING_RULE.md:20`; `results/final_test/run.log:4` |
| Flagged in Validation 7 | 0 | `results/preprocessing/cleaning/invalid_summary.json, temporal.flagged.eval` |
| Flagged in Test 8-10 | NOT FOUND (not recorded; decision not to re-read) | `results/decisions_log.md:108` (E1) |
| Dropped, v2 (Train 1-7) | NOT FOUND (rule applied, count not recorded) | rule: `results/decisions_log.md:382-383` (N2) |
| Reference IID protocol | 2 dropped (b2 l223, b2 l380), 1 evaluation record flagged and kept | `results/preprocessing/DATA_CLEANING_RULE.md:21` |

## 8. v2 recalibration

| fact | value | source |
|---|---|---|
| Preprocessing refitted with the calibration rows? | **Yes**: StandardScaler refitted on Train 1-7 + calibration rows | `scripts/ft_v2_recal.py:81-91`, `scripts/ft_v2_recal.py:168-174` |
| SVM refitted? | Yes, on the same rows | `scripts/ft_v2_recal.py:87` |
| Detector refitted? | **Yes** (alpha, weights, OOF thresholds); the calibration rows form one extra OOF group | `scripts/ft_v2_recal.py:88`, `scripts/ft_v2_recal.py:173` |
| Strategy B reduced models | refitted per calibrated model (own cache folder) | `scripts/ft_v2_recal.py:101`, `scripts/ft_v2_recal.py:165-166` |
| Fault statistics (sigma, p1, p99) | from Train 1-7 only (NOT refitted with calibration rows) | `scripts/ft_v2_recal.py:159` |
| Cleaning rule | fitted on Train 1-7; calibration rows are not screened by it | `src/splits.py:106`; `scripts/ft_v2_recal.py:154`, `scripts/ft_v2_recal.py:171-173` |
| Special weight for calibration rows? | **No** (plain `fit`, no `sample_weight`; each row counts once) | `scripts/ft_v2_recal.py:86-88` |
| n per gas | `min(n, count_gas // 2)` with n = 10, drawn without replacement, generator keyed by (seed, n, batch); count_gas = rows of that gas in the batch | `scripts/v2_recal.py:36-40`; `configs/final_test_v2.yaml:11`; `results/decisions_log.md:385-386` (N3) |
| Calibration rows in scoring | removed from scoring for both (a) and (b) | `scripts/ft_v2_recal.py:75-78`, `scripts/ft_v2_recal.py:200-206` |
| Calibration seeds | 0-4 | `configs/final_test_v2.yaml:12` |
| Number of calibration rows per Test batch | NOT FOUND (not written to any output; counting would need the Test labels) | - |
| Caveat | calibration rows are drawn from the whole batch (time order unknown): gain is optimistic | `results/decisions_log.md:404` (N9) |

## 9. Bootstrap

| interval | replicates | resampling unit | source |
|---|---|---|---|
| v1 Validation and Test, strategy vs best augmented (and all v1 F1 intervals) | 1000, seed 0 | **rows** of the evaluation set; ONE weight matrix shared by every method and scenario; setting value = mean over its scenarios; aug baselines averaged over seeds first. Reflects row sampling only | `scripts/ov4_analysis.py:6-9`, `scripts/ov4_analysis.py:61-63`, `scripts/ov4_analysis.py:95-98`; `scripts/ft_analysis.py:7`, `scripts/ft_analysis.py:72-81` |
| Preprocessing decision rule (Phase 3 stress, Part-1 rule) | 1000, seed 0 | rows (paired) | `src/evaluate.py:76-84`; `configs/preprocessing.yaml:81` |
| v2 clean (b)-(a), ORIGINAL (superseded) | 1000 per seed, seed = cal seed | rows, paired; the 5 per-seed replicate vectors averaged element-wise (independent indices) | `scripts/ft_v2_recal.py:225-238` |
| v2 under faults, ORIGINAL (superseded) | 1000 | scenarios, stratified by k, independent per seed, averaged | `scripts/ft_v2_tables.py:16-23` |
| v2 under faults, CORRECTED (paper) | 1000, seed 0 | **scenarios**, stratified by k (k1, k2), ONE index per replicate shared by all 5 seeds | `scripts/paper_corrections.py:34-44`; `results/decisions_log.md` O2 |
| v2 clean, CORRECTED (paper) | none (no resampling) | 95% t-interval over the 5 calibration **seeds** (calibration-draw variance only) | `scripts/paper_corrections.py:28-31`, `scripts/paper_corrections.py:52-58` |

## 10. Edge cost

| fact | value | source |
|---|---|---|
| CPU model | NOT FOUND in the edge-cost outputs (they say "laptop CPU"). The machine holding this repository reports `13th Gen Intel(R) Core(TM) i5-13420H` (queried 2026-10-09 with `Get-CimInstance Win32_Processor`), but the measurement itself did not record it | `results/edge_cost/edge_cost.json, note`; `results/edge_cost/edge_cost_v2.json, note` |
| OS | NOT FOUND in the outputs; same machine reports `Microsoft Windows 11 Pro 10.0.26300` (queried 2026-10-09) | - |
| Python / scikit-learn / numpy | 3.11.9 / 1.8.0 / 2.4.6 (also LightGBM 4.7.0, pandas 3.0.6) | `FREEZE_MANIFEST.md:3`; `requirements.txt:12`, `requirements.txt:22`; `pyproject.toml:4` |
| Threads | one BLAS/OpenMP thread (`*_NUM_THREADS=1`); the process is NOT pinned to a core (no affinity call) | `scripts/ft_edge_cost_v2.py:18-19`; `results/edge_cost/edge_cost_v2.json, note` |
| Latency protocol | single sample, median and p95 over 1000 runs after 50 warm-up runs, Validation rows | `scripts/ft_edge_cost_v2.py:10`; `results/edge_cost/edge_cost.json, fault_free.runs` |
| Size method | pickle size (float64), `len(pickle.dumps(obj)) / 1024` | `scripts/ft_edge_cost_v2.py:41` |
| "SVM only" = svm_calibrated + preprocessing | 511.4727 + 3.5791 = **515.05 KB -> "515 KB" is correct**, for the v2 calibrated SVM (simulated on Validation 7: Train 1-6 + 60 calibration rows = 5991 rows) | `results/edge_cost/edge_cost_v2.json, size_kb.svm_calibrated`, `size_kb.preprocessing`, `train_rows_for_calibration` |
| v1 SVM only (for comparison) | 527.4326 + 3.5791 = 531.01 KB | `results/edge_cost/edge_cost.json, part_sizes_kb.svm`, `part_sizes_kb.pre` |
| Caveat | the size is dominated by the support vectors, so it depends on the training rows; the v2 Test models (Train 1-7 + calibration rows) were not measured | `results/edge_cost/edge_cost_v2.json, note` |

## 11. Numbers added to PAPER_NUMBERS.md

New section "## Sanity checks and per-sensor false alarms" (checked by `scripts/check_paper_numbers.py`):
* Batch-identity accuracy: logistic regression, 5-fold stratified CV, predicting the batch id from the preprocessed Train features
  (`results/audit/sanity_checks.py:50-53`). Chance = share of the largest batch in that Train set.
* Per-sensor false-alarm rate on Test: share of clean Test rows in which the sensor is flagged by the frozen v1 "median" detector
  (`scripts/ft_detector.py:88-101`, column `alarm_rate` of `results/final_test/test/ft_reliability_ranking.csv`); OOF design rate is 5%.
