# Decisions log

Labels: **USER** = given by the user. **PRE** = registered here before the result it governs was seen.
**POST-HOC** = decided after validation results were seen (kept visible on purpose).
Hard rule of the overnight run: batches 8-10 are never read; everything is fitted on Train only; choices are made on
Validation (batch 7) or inner folds only.

## A. Decisions taken before the overnight run (from the conversation)
| # | decision | label | note |
|---|---|---|---|
| A1 | split Train 1-6 / Validation 7 / Test 8-10; Test needs explicit approval | USER | |
| A2 | statistical outliers (IQR) are real drift and are kept | USER, after Phase 2 | winsorising -0.021 SVM Macro-F1 |
| A3 | invalid-value rule `|x-median|/MAD > 1000`, fitted on Train, drops Train rows only, evaluation rows only counted | USER (rule) / POST-HOC (the need for it was found after seeing the Train std inflation) | threshold not tuned |
| A4 | the reconstruction errors exclude evaluation records flagged by A3; classification keeps them | USER | |
| A5 | reference_iid protocol (batches 1-7, stratified 80/20, 5-fold inside) | USER | |
| A6 | bias unit sigma_robust = IQR/1.349 from cleaned Train | USER | old G1 used an inflated plain std (x316 for S06 `|DR|`) |
| A7 | MinMax adoption rule (CI excludes 0 AND percentile-bounded MinMax still beats Standard by > 0.005) registered before the stress check; result: StandardScaler adopted | PRE | `results/preprocessing/phase3/stress_check.json` |
| A8 | Phase 4: sensor-local groups only; Phase 5: drift options none/top10/top20 | PRE | |
| A9 | first-run IterativeImputer diverged; imputed values bounded to the Train range afterwards | POST-HOC | first run kept in `phase1/temporal_first_run` |
| A10 | kNN reconstruction uses NearestNeighbors (equivalent to KNNImputer, tested) for speed | POST-HOC (speed only) | |
| A11 | `phase3/new_baseline.json` and `new_baseline_grid_val.csv` were overwritten when the stress check re-selected StandardScaler; the MinMax version is in commit `d7a91c9` | note | |
| A12 | the old line-223 record is borderline for the rule; rule unchanged, sensitivity reported | USER | not below 0.005 everywhere |

## B. Interpretations registered before running Parts 2-4 (2026-10-08, PRE)
The overnight text leaves these open. They are fixed here and will not be changed after seeing results.
1. **Medium severity** = Bias delta 1.0; Dropout/Stuck/Random fraction 0.5 (the milder of the two levels).
2. **Part-1 decision rule** compares each candidate (Phase 4 eligible groups, Phase 5 options) with the clean Baseline
   (StandardScaler, SVM C=10 gamma=0.01, Macro-F1 0.8590) using the baseline's tuned SVM settings; adopt only if
   gain > 0.005 AND the paired-bootstrap (1000) 95% interval of the Macro-F1 difference excludes 0. SVM is primary.
3. **Faults** are injected on the evaluation rows, on the RAW 128 features, on whole 8-feature sensor blocks:
   * shared_rows = true: the affected rows are drawn once per scenario and are the same for every sensor of the set;
   * Bias: delta x sigma_robust, ONE random sign per scenario shared by the sensors of the set, applied to all rows;
   * Stuck: each affected sensor block is frozen to the values of ONE random row of the evaluation set (per scenario);
   * Random: independent uniform draws per cell in [p1, p99] of the cleaned Train feature;
   * Dropout: block set to NaN.
   Sets: k=1 the 16 sensors; k=2 the 8 replicate pairs; k=4 the four candidate groups {1,2,9,10},{3,4,11,12},{5,6,13,14},{7,8,15,16}
   (hypothesis, as in the old study). Seeds 0-4. Scenarios are generated once, saved, and applied identically to every method.
4. **G1**: a fault type counts if, in its medium-severity k=1 setting, the mean Macro-F1 drop (16 sensors x 5 seeds) of the
   better clean baseline (SVM or LightGBM, higher clean Validation Macro-F1) is >= 0.03. G1 passes if >= 2 of the 4 types count.
5. **Detector** (Part 3): per sensor, Ridge in the signed-log standardised space predicts its 8 features from ALL other 15
   sensors (as specified; the leave-pair-out variant is reported as a secondary diagnostic). Score = mean over the 8 features
   of |prediction - value|. Alpha: leave-batch-group-out on Train. Out-of-fold (OOF) scores: leave-one-batch-out inside batches 1-6.
   Normalisation (a): score / the sensor's own OOF median; (b): score / the median over the 16 sensors of the same row.
   Alarm threshold per sensor = 95th percentile of its OOF normalised score (5% false alarms on OOF Train).
   A sensor block containing NaN is flagged by definition (score = +inf); NaN predictors are filled with 0 (the Train mean),
   so Dropout detection is trivial by construction and is reported as such.
6. **Choice (a) vs (b)**: higher median AUROC over the four fault types at k=1 medium severity on Validation.
7. **AUROC (primary, "isolation")**: in the affected rows of a scenario, scores of the faulty sensors (positives) against the
   scores of the healthy sensors in the same rows (negatives). Secondary: faulty blocks against the same blocks on the clean copy.
8. **G2**: median over the four fault types of the isolation AUROC (mean over sensors and seeds) at k=1, medium severity >= 0.80.
9. **False alarms**: alarm rate per (row, sensor) on the clean Validation batch, per gas, with all sensors and without S01, S02;
   also the share of rows with any alarm.
10. **Part 4 methods** (temporal protocol, SVM C=10 gamma=0.01 on StandardScaler features unless stated):
    * references: clean SVM without handling, SVM+Aug and LGBM+Aug (5 augmentation seeds, mean +- std);
    * A: flagged blocks (per row) are replaced by the Ridge prediction in slog space from the sensors not flagged in that row
      (with the twin, and without it), then the clean SVM; Oracle-A uses the true faulty sensors per row;
    * B: SVM trained without the flagged sensors (cached by excluded set; at most the 4 highest-scoring flagged sensors are
      excluded in a row); Oracle-B uses the true set;
    * C: 8 replicate-pair experts (SVM with probabilities, 16 features each), weights w = 1 / max(1, z/threshold)^2 per sensor,
      expert weight = minimum over its two sensors, compared with the same experts at equal weights;
    * best augmented baseline per setting = the better of SVM+Aug and LGBM+Aug (mean over aug seeds).
11. **G3**: A or B or C with the REAL detector beats the best augmented baseline in absolute Macro-F1 in at least one setting
    (fault type x severity x k) with a paired-bootstrap interval of the difference that excludes 0. A Bonferroni note over the
    number of comparisons is added as a supplement; it does not change the gate.
12. Reference protocol: reduced scenario set (medium severity per fault, k=1 and k=2 only), run after the temporal protocol is complete.

## C. Decisions taken during the overnight run (filled in as they happen)
* C1 (2026-10-08 ~02:15, operational, not a scientific decision): the full reproduction run (`scripts/run_preprocessing.py`, gate P6) and the Part-2 run were
  started together and starved each other (BLAS oversubscription: one SVM prediction took 4 s instead of 0.05 s). The
  reproduction run was stopped after 7 of 21 steps (markers in `results/preprocessing/_done`); it resumes with `--resume`
  once the CPU is free. Nothing was changed in the methods. Backup of the earlier results: `results/_backup_*`.
* C2 (PRE for the reference protocol, written before it was run): reference_iid uses the same classifier settings as the temporal
  protocol (SVM C=10 gamma=0.01, LightGBM 31 leaves, StandardScaler) instead of re-tuning them with the inner 5-fold, to save time;
  its detector and strategies are fitted on its own Train part (7,634 rows after cleaning) with the inner folds as the groups.
  Reduced scenario set (medium severity per fault, k=1 and k=2, 5 seeds = 480 scenarios).
* C3 (PRE, before the Part-4 results): the cap of 4 acted-on sensors per row (decisions_log B10) applies to A as well as B,
  so A and B always act on the same sets; C uses all reliability weights without a cap. C experts use gamma='scale' (16 features each)
  with C=10. Weight per sensor w = 1 / max(1, ratio)^2 and per expert the minimum over its two sensors.
* C4 (PRE): the Part-4 chunks are processed in the order k=4, k=2, k=1 (the user's rule if time runs out); the analysis accepts a subset.
* C5 (operational): `scripts/01_audit.py` used to open the Test files to count their lines (done once, in Step 1, before the
  overnight rule). It no longer opens them; the Test row of its split table now says "not read". The overnight run never opened
  batches 8-10 (the loaders refuse them and unit tests prove it). Earlier in the project, the dataset download step hashed the ten
  files (`data/raw/SHA256SUMS.txt`) and the Step-1 audit counted the lines of batches 8-10; no values or labels were looked at.

## D. Final-test decisions (user, 2026-10-08, all PRE: written before batches 8-10 were opened)
* D1: batches 8-10 are opened once, by `scripts/run_final_test.sh configs/final_test.yaml`, after the tag `frozen-before-test` and
  `FREEZE_MANIFEST.md`. Same code and configs verbatim; no change afterwards whatever the outcome; a programming error stops the run
  and is reported to the user (no silent fix-and-rerun). Nothing is refitted: the Validation-time models, detectors, thresholds and
  reduced SVMs are copied (hash-checked) from `results/overnight/temporal`.
* D2: results per evaluation batch (8, 9, 10) and pooled, with the Validation tables: baselines, A/B/C and the Oracles, G1-G3, detector
  AUROC, false alarms per gas (with and without S01/S02), sensor reliability ranking on clean rows, and the S01-S02 plot over batches 1-10.
  The per-batch and pooled analysis scripts (`ft_analysis.py`, `ft_detector.py`, `ft_s01s02.py`) were written and dry-run (on a 250-row
  sample of Validation, `configs/final_test_dryrun.yaml`) before the freeze; the pooled tables are cross-checked against `ov4_analysis.py`.
* D3: strategy C is not redesigned; it is reported as a negative result ("reliability weighting of the pair experts did not improve
  performance"; C_det ~ C_equal ~ 0.65 on Validation).
* D4: headline strategy = A, with B and the Oracle as references. The primary detector is the frozen "median" normalisation
  (Validation median AUROC 0.977); leave-pair-out is a sensitivity analysis.
* D5: S01/S02 are described as "naturally occurring replica divergence, flagged by the unsupervised reliability estimator on clean data;
  not flagged under the reference (no-drift) protocol, hence attributable to drift". They are not called faults.
* D6: fault severities and the k=4 groups stay as they are; k=4 is described as a hypothesis.
* D7: after the test: edge cost of the full pipeline A (detector + reconstruction + SVM) = size in KB, single-sample latency on one
  CPU core (median and 95th percentile over 1000 runs), peak memory; then the paper material in `results/paper/`. The report must say
  that the confidence intervals are optimistic (row resampling only) and that G3 is lenient, so the full tables are shown, not the gate result alone.
* D8 (operational): the test-time `ov3_detector.py` keeps the Validation choice of the normalisation (`--frozen-choice`); the run folder
  is `results/final_test/test` (`output_root` in the config).

## E. Decisions after the final-test launch (user, 2026-10-08)
* E1 (reporting, PRE of the test report): the number of Test records flagged by the invalid-value rule was not recorded during the run
  and the Test files are NOT read a second time to count them. The paper says it was not recorded.
* E2 / D9 (POST-HOC, made after the Figure-1 draft was seen; affects Phase-1 reporting only, no number of any result changes): Figure 1 originally
  compared the MAE in standardised units of the two protocols. That is not comparable: each protocol has its own Scaler and its own evaluation set
  (temporal = one homogeneous batch, reference = a mix of 7 batches), which made median/mean imputation look better under drift. Replaced by
  scale-free measures inside each protocol: skill = 1 - MAE_method / MAE_median (same protocol, same sensor, same space; median imputation is the
  zero reference), summarised by the median over the 16 sensors (whiskers: IQR), plus the median R2 over sensors as the second panel. Only ridge and
  knn (raw and slog) are in the main figure; iterative and mean are dropped from it (their rows remain in the CSV files of Phase 1). The leave-pair-out
  variant is in `fig1_supp_twin_missing.png`. Drift cost = skill_reference - skill_temporal (R2: R2_reference - R2_temporal); positive means the method
  loses its advantage over median imputation under drift. Generated by `scripts/ft_paper.py` (skill_table), listed in PAPER_NUMBERS.md.
* E3 (PRE of the test report): the report adds, per batch 8/9/10 and pooled: the results of every table; the false-alarm rate of the detector on
  clean Test rows; A and B on clean rows against the plain SVM (do the false alarms hurt the clean score under heavy drift); and whether the ordering
  "A and B above augmentation" held on Test, per fault type and per k.

## F. Operational incident during the final-test run (2026-10-08)
* F1: the final-test shell run (`scripts/run_final_test.sh`, started 10:39) was stopped by Claude Code at about 11:3x because the machine was critically
  low on memory (an automatic reaper, not a programming error). State: step `ov2_faults_g1.py` of 9, 12 of 42 chunks finished (`results/final_test/test/g1_chunks`,
  last written 11:27); no result file of any step exists yet; no code or config was changed. The run was NOT restarted; the `RUN_STARTED` marker still
  blocks a second start. Resuming would reuse the finished chunks (deterministic, checkpointed), but that needs the user's decision.
* F2 (correction and decisions, 2026-10-08, user approved the resume): the first entry above said the run had stopped with 12 of 42 chunks. In fact the
  orchestrating shell was killed but its python process (`ov2_faults_g1.py`) and its six workers survived as orphans and kept writing chunks; the
  count was 18 of 42 when they were ended (taskkill of the process tree, no python process left afterwards). Cause: system memory exhaustion (an
  infrastructure event, not a decision based on results). Resume conditions set by the user: (1) no old worker left; (2) the only change is the number of
  workers (`--jobs`, 3 for the resume), which does not touch the computation; (3) the change is a separate commit and is documented in section 4 of
  `FREEZE_MANIFEST.md`; (4) determinism is demonstrated first by recomputing one finished chunk with the new worker count and comparing it with the original
  (identical or difference < 1e-9, otherwise stop); (5) a memory guard at 85% stops the run safely instead of letting the system kill it; (6) the
  `RUN_STARTED` marker is moved aside after the check and the run resumes (finished chunks are reused); (7) partial results are not looked at or shown
  until the whole run has finished.
* F3 (2026-10-08, integrity check of the chunks written by the orphaned process, requested by the user): all 18 inherited Part-2 chunks
  (`chunk_000`..`chunk_017`; the user's "chunk 18" is the 18th file, index 17, the last one the orphan wrote) were checked with `scripts/ft_ops.py recheck`:
  every file reads completely; each has the expected 30 scenarios (sids in order), predictions of shape (30, 4364) for each of the 12 models
  (int8) and finite scores. Chunk 17 was then recomputed in a separate folder (`results/final_test_check`, same frozen models, same data) and compared
  with the original: IDENTICAL (predictions equal, maximum difference of the row values 0.0). Together with the earlier recomputation of chunk 5
  (3 workers, identical), no inherited chunk had to be recomputed. The pipeline kept running during the check (it touches nothing in the run folder).

## G. Version 2 (drift-robust base model + hybrid arbiter). ALL POST-HOC (user, 2026-10-08, after the v1 Test results were seen)
Written before any v2 code was run or any v2 number was computed.
* G0 (status and integrity). v2 is designed AFTER the v1 Test results were seen, and its motivation comes from them (clean Test score 0.859 -> 0.535;
  the per-domain ordering of the methods). Test batches 8-10 are therefore NOT an independent hold-out for v2: a v2 Test number is a post-hoc,
  test-informed result, labelled "post-hoc" wherever it appears, and it never replaces v1. The v1 results (tag `frozen-before-test`) stay unchanged,
  remain the pre-registered results of the paper and are shown in it. Everything of v2 lives in `results/v2/`.
* G1 (motivation, base model). On Test the clean score collapsed because of long-term drift, not faults. v2 develops a more drift-robust base model;
  the fault layer (detector, A, B) stays as it is and sits on top of it.
* G2 (motivation, arbiter = the main contribution of v2). v1 showed a domain where each method is best: the plain SVM without faults, A with one faulty
  sensor, augmentation with several Bias/Stuck sensors (Test pooled k=4; partly visible on Validation already, where A beat the best augmented
  baseline in only 1 of 3 Bias k=4 cells). The arbiter routes each row by the number of sensors the detector flags (n_flag); it never sees the truth
  or the labels.
* G3 (rules). (1) Batches 8-10 are not used for any development, choice or tuning; they are read once, at the end, after the tag `frozen-v2` and
  `FREEZE_MANIFEST_v2.md`. (2) Every adaptation is unsupervised on the new data: it uses the readings of the new batch, never its labels. (3) The
  candidate lists below are closed. (4) Every trial is a row of `results/v2/trials.csv`. (5) If nothing improves, the report says so and no further
  candidate is tried.
* G4 (Drift-Dev protocol, batches 1-7 only). Dev-Train = batches 1-3 (months 1-13); Dev-Eval = batch 6 and batch 7 (months 17-21), each scored
  separately, then averaged. Everything is fitted on Dev-Train: the invalid-value cleaning rule, the scaler, the models, the fault statistics
  (sigma, p1, p99) and the detector (leave-one-batch-out over batches 1, 2, 3). Confirmation on the original split: Train 1-6, Validation 7 (as v1).
  Known weaknesses, logged now: Dev-Train has almost no toluene (74 rows in batch 1, 5 in batch 2, 0 in batch 3) while batches 6 and 7 have 467 and
  568, so Drift-Dev also measures a class-coverage gap, not drift alone; batch 7 was the v1 Validation batch.
* G5 (candidates, at most 6). SVM settings stay C=10, gamma=0.01; nothing is re-tuned. M1 and M2 are front-end transforms that map the readings of a
  batch back to raw units of the Train reference, so the frozen pipeline (StandardScaler -> SVM), the detector, A, B and the augmentation run on top of
  them unchanged.
  - M0: the v1 model (reference).
  - M1: per-batch robust normalisation. Each feature x of batch b -> (x - median_b) / s_b * s_ref + median_ref, s = IQR/1.349, (median_ref, s_ref) from
    the pooled cleaned Train rows. Training: every Train batch with its own statistics. Evaluation: the statistics of the new batch from its own readings
    (after fault injection when there is a fault), no labels. NaN are ignored in the statistics; where s_b = 0 (e.g. Stuck on every row) the feature is
    only shifted (s_b := s_ref).
  - M2: CORAL (Sun, Feng, Saenko, "Return of Frustratingly Easy Domain Adaptation", AAAI 2016; reference verified). In the Train-standardised space,
    Cs = cov(Train) + I, Ct = cov(new batch) + I, the new batch is mapped Z -> Z Ct^(-1/2) Cs^(1/2), then back to raw units. Stated deviation: the paper
    maps the SOURCE to the target and retrains the classifier; here the new batch is mapped to the Train statistics (the user's specification), so one
    classifier serves every batch. NaN (Dropout) are set to 0 (the Train mean) for the covariance and the mapping and put back afterwards.
  - M3: ensemble of one SVM per Train batch, weighted majority vote (Vergara et al., "Chemical gas sensor drift compensation using classifier
    ensembles", Sensors and Actuators B 2012, doi 10.1016/j.snb.2012.01.074; reference verified). Weight = Macro-F1 of the member on the most recent
    labelled Train batch (3 for Drift-Dev, 6 for the original split); for the member trained on that batch itself, 5-fold stratified cross-validated
    Macro-F1 inside the batch. Only this weighting is tried (not recency). Shared preprocessing (StandardScaler on the pooled Train rows).
  - M4: the two best of M1-M3 by the Drift-Dev mean (decided from M1-M3 only, before M4 runs), built only if both beat M0 on Drift-Dev; otherwise M4
    is not run. Fixed definitions: M1+M2 = M1, then CORAL fitted on the M1-normalised Train; M1+M3 = M1, then the batch ensemble on the normalised
    Train; M2+M3 = CORAL, then the batch ensemble.
  - M5: standard practice for the final model: after the choice, retrain on batches 1-7. Applied only in the final Test run.
* G6 (choice of the base model). Winner = highest clean SVM Macro-F1 on Drift-Dev (mean of batches 6 and 7) among the candidates that (a) stay at or
  above 0.859 - 0.01 = 0.849 on the original split (Validation 7) and (b) keep the detector usable: the v1 G2 statistic (median over the four fault
  types of the isolation AUROC, k=1, medium severity, 5 seeds, "median" detector fitted on the transformed Train rows) on Validation 7 >= 0.80.
  Tie = within 0.01 of the best eligible: then the simplest, in the order M0 < M1 < M2 < M3 < M4. A winner M0 means no candidate improved the base.
* G7 (fault layer on the v2 base, fixed now). Faults are injected on the raw readings, then the base transform (with the statistics of the faulted
  batch, as specified), then the detector and A/B. Consequence stated before any result: the v1 Bias fault shifts the WHOLE batch by a constant, so
  M1's per-batch median removes it exactly (M2 partly) and the detector cannot and need not see it. This is a property of the simulation (a fault
  present for a whole batch); Bias results of M1/M2 are reported as such and not presented as fault handling. Augmentation for M1/M2 is injected on
  the transformed Train rows (sigma, p1, p99 recomputed there). For M3: A = reconstruct, then the ensemble; B = an ensemble of reduced per-batch SVMs;
  augmentation = per-batch SVMs trained on augmented batch rows. After the choice, the fault layer (A, B, augmentation, Oracle) is run on the winner on
  Drift-Dev with a short scenario set (k=1 and k=2, medium severity, 5 seeds) to check that it still works.
* G8 (hybrid arbiter, three variants only, on top of the winning base model). n_flag = number of sensors flagged in the row (primary detector).
  Probabilities come from probability-enabled copies (Platt, SVC(probability=True), same data and settings) of the SVM, of the reduced B models and of
  the 5 SVM+Aug models (their mean = "Aug"); A's probability = that of the probability SVM on the reconstructed row.
  - H1: n_flag = 0 -> SVM; 1-2 -> A; >= 3 -> mean of the probabilities of B and Aug.
  - H2: n_flag = 0 -> SVM; 1 -> A; >= 2 -> mean of the probabilities of A, B and Aug.
  - H3: weighted mean of the probabilities of (SVM, A, Aug) with fixed, not learned, weights:
    n_flag 0: (0.8, 0.0, 0.2); 1: (0.2, 0.6, 0.2); 2: (0.1, 0.5, 0.4); >= 3: (0.0, 0.4, 0.6).
  Choice on Drift-Dev and on Validation 7, scenarios = clean + k=1 and k=2 at medium severity. Winner = highest mean Macro-F1 over all scenarios
  (clean included), averaged over the two protocols, provided that in every setting (clean, k=1, k=2; each protocol) it is not below the best single
  method (SVM, A, B, best of SVM+Aug/LGBM+Aug) by more than 0.01. If no variant satisfies this, no arbiter is adopted and the report says so.
  Known before running: on clean Validation rows the v1 detector flags 2.1 sensors per row on average (97% of the rows have a flag), so the n_flag = 0
  branch will be rare under drift; this is reported, not tuned.
* G9 (final run). Tag `frozen-v2` and `FREEZE_MANIFEST_v2.md`; final training on batches 1-7 (M5) with the winning method; the full v1 fault pipeline
  on Test once, same scenarios and seeds, memory guard (3 workers, 85%) and safe resume as before. In the same single run the winner trained on 1-6 is
  also evaluated, to separate the effect of the method from the effect of adding batch 7 to the training rows.
* G10 (report). `results/v2/V2_REPORT.md` + Arabic summary: the Drift-Dev table of every candidate; v1 vs v2 on Test (clean, A, B, augmentation, Oracle;
  pooled and per batch); arbiter vs every single method per fault type and k, with the clean case; worst case (lowest Macro-F1 over scenarios) per
  method; share of rows sent to each arbiter branch. Limitations: post-hoc and test-informed (G0); M1/M2 are transductive (they need a batch of
  unlabelled readings, so a single-sample edge deployment needs a buffer of recent readings); batch statistics depend on the gas mix of the batch.
* G11 (stop point). The work stops after the candidate table (G6) for the user's review, before the fault layer, the arbiter and the final run.

## H. Defect in `fast_svm_predict` for two-class models (found 2026-10-08 while writing the v2 tests; user decisions)
* H1 (defect). `src/fastsvm.py` reproduced libsvm's one-vs-one vote with sklearn's public `dual_coef_`/`intercept_`. For a TWO-class SVC sklearn
  stores these with the sign flipped relative to libsvm, so the function returned the opposite class for every row. With 3 or more classes it is
  exact (tested against `SVC.predict` since Part 2). Found by a v2 unit test of the batch ensemble (`tests/test_drift.py`) on two classes.
* H2 (effect on v1: none). `scripts/check_svm_classes.py` opened every saved model under `results/` (every *.joblib; SVC alone, inside a pipeline
  or in the list of C experts) and counted its classes: 5246 SVC models, ALL with 6 classes, none with fewer than 3, no unreadable file
  (`results/svm_class_inventory.txt`). This covers every model `fast_svm_predict` was applied to in v1: the base and the 5 augmented SVMs
  (`overnight/temporal/models`, `overnight/reference_iid/models`, `final_test/test/models`), every reduced B model (`.../reduced`, 1213 Validation,
  1126 reference, 1639 Test), and the 8 C experts (6 classes each; C uses `predict_proba`, not this function). Every v1 model is trained on rows
  that contain all 6 gases. v1 is NOT re-run.
* H3 (fix). The two-class case now uses the binary decision value (classes_[1] when f >= 0, the libsvm tie rule); a guard rejects a model with fewer
  than two classes. New test `tests/test_fastsvm.py::test_matches_sklearn_predict_for_few_classes` (2, 3 and 5 classes, two label sets) fails on
  the old code (both two-class cases) and passes on the new one; the full suite passes (106 tests). The user also asked for an assertion that rejects
  two-class models "until it is fixed": the fix and its test land in the same commit, so the rejection was not added (it would block the corrected
  path); only the < 2 classes guard is in place.
* H4 (v2 run stopped). The first `scripts/v2_dev.py` run (started on the uncommitted v2 code after commit 3e2365f) was stopped at the user's
  request after M0 (both protocols) and M1 (Drift-Dev); it had printed only run times, no score, and had written no file. It will be run again on the
  committed, corrected code.

## I. Implementation details of the fault-layer check and the arbiter (written before any arbiter number; fill gaps left by G7-G8)
* I1. Scenario set: the clean case + `build_scenarios(seeds 0-4, k1 and k2, medium)` = 1 + 480 scenarios per evaluation batch (Drift-Dev: batches 6
  and 7, each with its own batch transform; original split: batch 7). Faults are injected on the raw readings with the raw Train statistics, as in v1.
* I2. Single methods = the v1 definitions: SVM (no handling); A = A_det_twin (v1 headline, twin allowed as predictor); B = B_det (v1 cap of 4 acted
  sensors); augmentation = SVM+Aug and LGBM+Aug, each the mean Macro-F1 over the 5 augmentation seeds, "best aug" = the higher of the two per setting.
  Oracle A and B (true faulty sensors) are reported in the fault-layer check only; they are not arbiter components and not in the arbiter rule.
* I3. Probabilities: the SVM, the 5 SVM+Aug models and the reduced B models are trained once with probability=True (Platt, random_state 0); their
  labels for the single methods still come from the decision function (fast_svm_predict), exactly as v1. n_flag = all flagged sensors of the row
  (not capped); A and B act on the capped sets as in v1.
* I4. Rule of G8 read literally: "mean over all scenarios" = mean over the 481 per-scenario Macro-F1 values of a protocol (Drift-Dev: mean of the
  two batches), so the clean case weighs 1/481 there; the clean case is protected by the per-setting condition (clean, k1, k2, each protocol: not below
  the best single method by more than 0.01). The setting-balanced mean (clean, k1, k2 equally weighted) is shown for information only.
* I5. Worst case per method = lowest per-scenario Macro-F1 over the 481 scenarios (per evaluation batch). Branch shares = share of rows per branch
  of H1 and H2 and per n_flag level of H3, on the clean case, k1 and k2.
* I6 (operational incident, 2026-10-08). The arbiter run (`scripts/v2_arbiter.py` under `run_guarded.py`, started 21:55 at 54% memory load) was
  stopped by Claude Code's low-memory reaper while the session was idle (not by the 85% guard, not a programming error). State: the Drift-Dev fit was
  finished (`results/v2/arbiter/drift_dev/fitted.joblib`), the original-split fit (6 Platt SVMs) was in progress and wrote nothing; no scenario chunk
  existed; no python process survived (checked). No arbiter number was produced. Not restarted; waiting for the user.
* I7 (restart, user decision 2026-10-08 22:00). On the user's instruction, unneeded applications were closed (Chrome, chat apps, updaters; load 73% ->
  51%) and the run was restarted unchanged (same code, 3 workers, guard 85%) at 22:00:15; the cached Drift-Dev fit was reused, the original-split fit
  was redone ("original: fitted"), and reduced B models are being created from 22:01. Code review afterwards (not affecting the running process,
  which loaded the code before): chunk and fit files are now written through a temporary file and renamed (a kill mid-write can no longer leave a
  truncated file that a resume would reuse); the cache folder carries the base-model name (`base_model.txt`) and a mismatch stops the script; an M3 base
  is rejected explicitly (G7 needs its own A/B/augmentation, not implemented). None of this changes any computed value.
* I8 (sensitivity analysis requested by the user after the candidate table; does NOT change the G6 choice). Drift-Dev Macro-F1 of M0-M3 recomputed
  with and without the toluene rows of batches 6 and 7, because Dev-Train has almost no toluene (G4). "Without toluene" = the toluene rows are removed
  from the scored rows; a prediction of toluene on another gas still counts as an error; Macro-F1 over the 5 remaining gases. Same fitted models and
  code as the candidate table; the full-row numbers must reproduce `results/v2/candidates.csv` (checked). Script `scripts/v2_toluene_sensitivity.py`.

## J. Few-shot recalibration (POST-HOC, added by the user 2026-10-08 after the candidate table was seen; written before any arbiter number was seen)
* J0 (status). A new candidate added AFTER the unsupervised candidates failed to beat M0. It deliberately departs from G3(2) (it uses LABELS of the new
  batch) and from G3(3) (the list was closed); both by the user's decision. It is therefore a SEPARATE setting, reported as "with n labeled calibration
  samples per gas" next to the v1 results without calibration, never mixed with them or with the unsupervised v2 results, and labelled post-hoc. Adding
  a candidate after seeing the others fail is a forking path; the report says so.
* J1 (reference, verified). Lei Zhang and David Zhang, "Domain Adaptation Extreme Learning Machines for Drift Compensation in E-Nose Systems", IEEE
  Transactions on Instrumentation and Measurement 64(7):1790-1801, 2015 (arXiv 1505.06405): a few labeled target-domain samples for drift compensation.
  DAELM itself (an ELM with a separate target-domain penalty) is NOT implemented; we use the simplest form of its idea with the frozen SVM:
  "few-shot recalibration (DAELM-inspired)".
* J2 (motivation). Realistic IoT maintenance: a technician exposes the device to known gases and the readings are stored with their labels.
* J3 (design). Base = M0 (the G6 winner). For every evaluation batch separately: per gas, m = min(n, floor(count/2)) rows drawn at random
  (seed s in 0..4, generator keyed by the batch and n) from the CLEAN batch; a gas absent from the batch gives none. n in {5, 10} only. Adaptation =
  Train rows + calibration rows, unweighted (no separate target penalty, nothing tuned), and every Train-fitted object is refitted on them: StandardScaler,
  SVM, the 5 augmentation sets and models, the reduced B models, and the detector (the calibration rows form one extra group in its
  leave-one-batch-out). The fault definitions are unchanged (raw Train statistics of v1). Faults are applied to the FULL batch matrix exactly as in
  the uncalibrated runs (same faulted matrices); the calibration rows are then removed from scoring, for good. The uncalibrated M0 is scored on the SAME
  remaining rows of each seed, so every comparison is paired on identical rows.
* J4 (choice of n, clean only; stage 1). gain(n) = calibrated minus uncalibrated clean SVM Macro-F1 on the same rows, mean over the 5 seeds, computed for
  Drift-Dev (mean of batches 6 and 7) and for Validation 7, then averaged over these two. n* = 5 if gain(5) >= 0.9 * gain(10), else 10. If gain(10) <= 0,
  calibration does not help: reported, and no fault layer is run on it.
* J5 (stage 2). For n* only: the full fault layer (A, B, augmentation, Oracle) and the arbiters H1-H3 on the calibrated model, 5 seeds, the same 481
  scenarios (clean + k1/k2 medium), Drift-Dev batches 6 and 7 and Validation 7. The arbiter variant chosen by G8 on the uncalibrated model is carried
  over (no new choice); all three are shown. Results: mean +- std over the 5 calibration seeds.
* J6 (retention column, for every v2 fault table). retention = Macro-F1 with the fault / clean Macro-F1 of the SAME method, model, evaluation batch
  (and calibration seed), per scenario, then averaged like the Macro-F1. Computed from the per-scenario files; nothing is re-run for it. For v1 tables it
  is computed from the existing v1 per-scenario files when v1 is shown next to v2 (reporting only; Test is not read again).
* J7 (Test, only after the user's approval). One run: every Test batch (8, 9, 10) gets its own calibration rows (rule J3, n*, seeds 0-4), removed from
  scoring; pooled = the union of the remaining rows. Reported as its own setting next to v1.
