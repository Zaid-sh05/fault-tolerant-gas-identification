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

## K. Overnight plan and CORAL check (user 2026-10-08 ~23:15; written before the arbiter numbers were seen)
* K1 (CORAL correctness check, DIAGNOSTIC ONLY: does not change the G6 choice and adds no candidate). Requested because M2 fell far below M0.
  On Drift-Dev (batches 6, 7) and Validation 7: (a) our mapping equals an independent implementation (scipy.linalg.sqrtm / inv) of
  Z Ct^(-1/2) Cs^(1/2); (b) the covariance of the mapped batch is closer to the Train covariance than before (relative Frobenius gap);
  (c) the norm of the batch mean in the Train-standardised space before and after the mapping (CORAL as specified does not centre); (d) M2's
  scores reproduce `candidates.csv`; (e) the paper's own direction (Train mapped to the new batch, SVM retrained on the mapped Train rows in the
  standardised space, same C and gamma) as a diagnostic of whether the reversed direction explains the drop. Script `scripts/v2_coral_check.py`.
* K2 (order of the night, no further user input): when the arbiter run ends with exit code 0: (1) rebuild its tables with the retention column
  (`v2_arbiter.py --report-only`); (2) check that the refactored scenario code reproduces one saved arbiter chunk exactly; (3) recalibration stage 1,
  then stage 2 if J4 allows, each under the memory guard (85%, 3 workers); (4) one morning report. A failing step stops the chain and is reported; if
  the system stops a run for memory, it is reported, not restarted. Test is not touched.

## L. Night improvement study (POST-HOC; user 2026-10-09 ~01:00, "improve freely within the integrity rules"; written BEFORE any result of it)
* L0 (rules). Test (8-10) is never read. Selection on Drift-Dev (train 1-3, eval 6 and 7; mean of the two), confirmation on Validation 7
  (train 1-6), fixed in this direction. Stage 2 of the recalibration is not touched. Resources: the user answered "no problem" when the worker
  cap was raised; this is read as permission for ONE extra single-thread analysis process next to stage 2 (12 logical cores, CPU about 50%,
  memory 65%), under the 85% memory guard; checkpointed atomic chunks. No new experiment starts after 09:00.
* L1 (answers from files, no new run). Worst A scenario (Drift-Dev b7, F1 0.315): k=2, Bias, medium severity (1.0 sigma), sensors S05-S06 (a
  replicate pair), fault seed 4; SVM 0.613, B 0.609, Oracle A 0.603. Detection was not stored in the result files; a one-scenario light
  diagnostic (Dev only) shows masking: the faulty pair was flagged in 2% (S05) and 25% (S06) of the rows, while healthy S03, S08, S13, S14
  were flagged in 27-51% and reconstructed FROM the biased pair. v1 frozen Test output: A_det_twin on clean pooled Test rows = 0.5436 vs SVM
  0.5354 (`results/final_test/test/ft_clean_by_subset.csv`; per batch b8 0.758 vs 0.798, b9 0.637 vs 0.655, b10 0.493 vs 0.480).
* L2 (closed list of variants, base model M0, decision labels only; nothing else is tried):
  - V0: A as in v1 (median detector, 95th-percentile thresholds). Reference.
  - V1: twin-aware detection against masking: a sensor is flagged if EITHER the v1 detector OR its leave-pair-out version (predicts the sensor
    without its twin; the existing "median_lpo" variant, fitted on the same Train rows) exceeds its own 95th-percentile threshold;
    ratio = max of the two ratios.
  - V2: fewer false alarms: v1 detector with 99th-percentile thresholds (of the same Train out-of-fold scores).
  - V3: V1 with 99th-percentile thresholds.
  - V5: guarded reconstruction against error propagation: as V0, but when a flagged block is reconstructed, every sensor whose ratio exceeds 0.5
    (half the alarm threshold) is also excluded from the predictors.
  - V4: routing for the worst case: on top of the best of V0-V3/V5, rows with n_flag >= t go to SVM+Aug (the 5 v1-style augmented SVMs,
    mean Macro-F1 over seeds as in v1) instead of A; t in {2, 3, 4, 5} chosen on Drift-Dev. (SVM+Aug, not B, because B needs one model per
    excluded set: about a thousand extra SVM fits per protocol, impossible tonight next to stage 2.)
* L3 (scenarios and metrics). Clean + k=1, k=2, k=4 at medium severity, 5 fault seeds (1 + 320 + 160 + 80 = 561 per batch), faults on raw
  readings with raw Train statistics as v1. Per variant: clean Macro-F1, mean Macro-F1 under faults (k1, k2, k4 weighted equally), worst case
  (lowest per-scenario Macro-F1), detector isolation AUROC and TPR (per fault x k), clean FAR (per sensor-row) and share of clean rows with an alarm.
* L4 (selection and success, fixed now). Primary = mean Macro-F1 under faults on Drift-Dev. Eligible only if (a) clean Macro-F1 on Drift-Dev not
  below V0 by more than 0.005 and (b) worst case on Drift-Dev not below V0. Best eligible, ties (< 0.005) to the simplest in the order
  V0 < V2 < V1 < V3 < V5, then V4's t the same way (V4 adopted only if it passes the same eligibility against its base). SUCCESS only if, against
  V0, the gain in the primary metric has a 95% paired bootstrap interval above 0 on Drift-Dev (bootstrap over SCENARIOS, 1000 resamples, seed 0:
  this resamples the fault draws, not only rows) AND is confirmed on Validation 7 (gain > 0 with the same kind of interval above 0, clean drop
  <= 0.005). Otherwise the variant is reported as failed.
* L5 (descriptive, no selection). "A as partial drift correction": clean A - SVM per Dev batch (6, 7) and Validation 7 with a row bootstrap;
  attribution: A restricted to one sensor's flags at a time (16 runs per batch, clean rows), gain per sensor.
* L6. Few-shot recalibration (J) is not part of L; its stage 2 is summarised separately when it ends.
* L7 (amendment, user 2026-10-09 ~01:20, written before any L result). Tonight, while stage 2 runs: only LIGHT experiments that use saved
  outputs (v1 per-row predictions of Validation 7 in `results/overnight/temporal/{strategy_preds,baseline_preds,truth_masks}.npz`, the saved
  v1 detectors) and detector inference without any fitting. Experiments that need fitting or new SVM predictions over the scenario set are
  coded, tested on a small sample, and run only after stage 2 ends, until 14:00 at the latest, with these criteria (all registered before 09:00).
  Direction per experiment, fixed now:
  - LR (light, routing): selection on Validation 7 from the saved v1 outputs, confirmation on Drift-Dev in the heavy run. Rows with n_flag >= t
    (v1 median detector, all flagged sensors) go to target T instead of A_det_twin; T in {B_det, SVM+Aug (mean Macro-F1 over the 5 seeds)},
    t in {2, 3, 4, 5}. Scenarios: the v1 medium-severity cells k1, k2, k4 (5 seeds each) and the clean rows (A, B labels on clean rows
    recomputed by inference with the saved v1 models). Metric, eligibility, tie rule and success test as L4 with the roles of the two protocols
    swapped (eligibility and the scenario bootstrap on Validation 7; confirmation on Drift-Dev: gain > 0 with its interval above 0, clean drop <= 0.005).
    Ties to the larger t (closer to plain A), then B before SVM+Aug.
  - LD (light, detector, descriptive only on Validation 7): D0 (v1), D1 (max of median and median_lpo ratios), D2 (99th-percentile thresholds),
    D3 (D1 at 99th); isolation AUROC and TPR per fault x k (medium), clean FAR, share of clean rows with an alarm, and for k=2 pair faults the TPR
    of the faulty pair and the alarm rate of the healthy sensors in the faulted rows (masking). No choice is made from LD.
  - LA (light, descriptive): clean A - SVM per batch (Dev 6, 7 from the arbiter files; Validation 7 from the v1 files) and per-sensor attribution
    by inference with saved models on clean rows only.
  - V0-V5 of L2 (heavy: new A predictions over the scenarios on Drift-Dev and Validation 7): unchanged, L4 (select on Drift-Dev, confirm on
    Validation 7). V4 of L2 is replaced by LR.
* L8 (operational decision 01:30, before any V result). Stage 2 runs far slower than estimated (9 of 234 chunks in 40 min: every calibrated
  configuration fits its own Platt-scaled reduced models), so it will likely end around noon and the heavy window (until 14:00) would be too short.
  The A variants V0-V3, V5 need no model fitting: inference with saved models, plus one leave-pair-out detector on the Drift-Dev Train rows
  (a closed-form ridge fit of about a minute; Validation 7 reuses the saved v1 one). They are therefore run NOW as a light single-thread job
  (`v2_improve.py --light`: no B, no augmentation, no routing; output `results/v2/improve_light/`), with the unchanged L4 rule (select on
  Drift-Dev, confirm on Validation 7). The Drift-Dev confirmation of LR needs new reduced B models (fitting) and stays a heavy job for after stage 2,
  until 14:00, same criteria (L7).

## M. Night incidents (2026-10-09)
* M1 (07:22, memory). The memory load reached 87%: the largest consumer was the "ollama app" (3.9 GB, a background LLM server, not part of
  this project), plus Chrome. `run_guarded.py` logged that it stopped stage 2, but its `taskkill /T` did NOT end the tree (the venv launcher
  -> python -> loky workers survived), so stage 2 kept running unguarded; the Claude Code memory reaper also ended the overnight chain shell
  (`v2_overnight.sh`; it had nothing left to start). Actions: Ollama was closed (the user had earlier asked to close unneeded applications to
  free memory; load 88% -> 64%); stage 2 was left running (rule: it is not stopped or modified); a new tree guard (`scripts/tree_guard.py`,
  85%) watches its process tree from 07:30; `run_guarded.py` now kills the whole tree pid by pid and verifies (self-test: parent + child
  killed, none left). No result file was lost: chunks are written atomically (103 of 234 finished at 07:22).

## N. PRE-TEST v2: single final Test run of the few-shot recalibration (POST-HOC design; user decision 2026-10-09 ~11:20)
Written before the run and before batches 8-10 are opened for v2. Batches 8-10 are read only in step 5, once.
* N0 (status). The design is POST-HOC and test-informed (G0, J0): the v1 Test results were seen before recalibration was proposed. The result is a
  separate setting, "with n labeled calibration samples per gas", shown next to v1 and never mixed with it. Every outcome is reported as it is.
* N1 (configuration). n* = 10 per gas (J4; chosen in stage 1 on Drift-Dev and Validation 7; not changed). Stage 2 has no further selection rule
  (no arbiter was adopted, G8), so no other setting is chosen from it.
* N2 (base model and recipe). The stage-2 recipe unchanged (J3): M0 = StandardScaler on the raw 128 features -> SVM (C=10, gamma=0.01), the "median"
  reliability detector (95th-percentile thresholds of the leave-one-group-out scores; the calibration rows form one extra group), A = Ridge
  reconstruction of the flagged blocks (twin allowed), B = reduced SVM without the flagged sensors (cap 4). Train = batches 1-7, cleaned by the
  invalid-value rule fitted on batches 1-7 (as every protocol). The SVMs are fitted without Platt probabilities because neither the arbiter nor the
  augmentation is part of this run; the smoke test (N6) checks that the labels equal the stage-2 labels (Platt-enabled models) exactly.
* N3 (calibration). For each Test batch (8, 9, 10) separately and each seed: per gas min(10, count // 2) rows drawn at random by the stage-2 function
  (`calib_rows`, generator keyed by seed, n and batch) from the clean batch, added to Train for that batch's calibrated model and REMOVED from scoring.
  Seeds 0-4 (or 0-2, see N7).
* N4 (paired comparison). On exactly the same remaining rows of each seed: (a) M0 trained on batches 1-7 without calibration, (b) M0 with the
  calibration rows of that batch. The v1 Test numbers are not used for this comparison (other rows, other Train).
* N5 (fault layer and metrics). Faults on the full raw batch matrix with the raw Train statistics (1-7), exactly as stage 2; then scoring on the
  remaining rows. Scenarios: clean + k=1 and k=2, every fault type and every severity of v1 (dropout 0.5/1, bias 0.5/1/3, stuck 0.5/1, random 0.5/1),
  fault seeds 0-4: 1 + 720 + 360 = 1081 per batch. Methods: SVM (no handling), A, B, for both (a) and (b). Routing A->B is NOT included (not confirmed).
  Metrics per batch and pooled (pooled = the union of the remaining rows of the three batches, each batch with its own model): clean Macro-F1, mean
  Macro-F1 under faults (k1 and k2 weighted equally), worst case (lowest per-scenario Macro-F1), retained ratio (fault / clean, same method, model,
  batch, seed), detector isolation AUROC and TPR, clean FAR and share of clean rows with an alarm. Intervals: clean (b)-(a) by a paired row bootstrap
  (1000, per seed, averaged over seeds); under faults by a scenario bootstrap stratified by k (1000). Mean +- std over calibration seeds.
* N6 (checks before the run). (1) Smoke test of the same script on Drift-Dev (train 1-3, batch 6, seed 0, medium scenarios): labels-based Macro-F1
  of SVM, A and B, calibrated and uncalibrated, must equal the stage-2 values of configuration drift_dev_b6_n10_s0 (difference < 1e-9), otherwise stop
  and log. (2) Ollama closed; the fixed guard (`run_guarded.py`, tree kill), 3 workers, resumable atomic chunks.
* N7 (time). The run time is estimated from timings on batches 1-7 Train rows only (no Test data). If the estimate for 5 seeds exceeds 10 hours,
  seeds are reduced to 0-2 BEFORE the freeze, and the decision is logged here.
* N8 (expectations, registered now). Success = (b) above (a) on clean Macro-F1 (pooled, interval above 0) AND, for the calibrated model, A >= SVM in
  the mean Macro-F1 under faults (pooled). Whatever the outcome, it is reported as it is.
* N9 (caveat, must appear in the report). The calibration rows are drawn from the whole batch, not from its beginning, because the time order inside a
  batch file is unknown; the gain is therefore optimistic (calibration rows are interleaved in time with the scored rows).
* N10 (freeze). `configs/final_test_v2.yaml`, tag `frozen-before-test-v2`, `FREEZE_MANIFEST_v2.md` with the hashes of code and config. No change
  after the freeze; a bug found after the run is fixed, logged, the run repeated, and both results shown.
* N11 (pre-freeze fix found by the smoke test, 13:25). Two workers that needed the same reduced B model at the same moment collided on Windows:
  `os.replace` onto a file another process had open raised PermissionError and the smoke run stopped (no number produced). Fix in the v2
  script only (`SafeKit` in `ft_v2_recal.py`; the frozen v1 `src/strategies.py` is not touched): on that error the other worker's file (the
  same fit: same rows, same seed) is loaded. The smoke folder was deleted and the smoke test re-run from scratch.
* N12 (checks passed, before the freeze, 13:30). Smoke test (Drift-Dev b6, seed 0, 481 medium scenarios, calibrated and uncalibrated, SVM/A/B):
  IDENTICAL to stage 2 (max difference 1.1e-16), which also confirms that the SVMs fitted without Platt probabilities give the same labels.
  Time estimate from fits on the Train rows of batches 1-7 only (no Test data): 1.9 h for 5 seeds (one reduced SVM 0.6 s without Platt), far
  below 10 h, so seeds stay 0-4 (N7). Ollama closed; memory load 53%; the fixed tree-killing guard is used.

## O. POST-AUDIT correction (user decision 2026-10-09, option 2: no new reading of the Test data or labels)
* O1 (problem). The independent audit (`results/audit/AUDIT_REPORT.md`, finding A1) showed that the v2 intervals averaged INDEPENDENT
  bootstrap replicates of the 5 calibration seeds (`scripts/ft_v2_recal.py:229-238` clean rows; `scripts/ft_v2_tables.py:16-24` and
  `scripts/v2_paper.py` scenarios). The seeds score almost the same rows and scenarios, so the row/scenario variance shrank by about 5x and
  the variance of the calibration draw was left out: e.g. 4 of the 5 per-seed pooled clean gains fell outside the reported interval.
  The point estimates were computed correctly. The v1 intervals share one weight matrix across methods and are not affected.
* O2 (correction; frozen code, configs and v1/v2 result files are untouched; new files and sections only).
  - Under faults: scenario bootstrap (k-stratified, 1000, seed 0) with ONE resample index per replicate shared by all seeds, from the
    existing `results/final_test_v2/test/scores.csv`.
  - Clean: 95% t-interval over the 5 per-seed values. LIMITATION, stated in the paper: it captures the calibration-draw variance only; the
    row-sampling part would need the Test labels, which are not read again (user decision). Where the seeds agree closely (batch 9) this
    interval is NARROWER than the old row bootstrap (SVM gain b9: old [0.237, 0.253], corrected [0.240, 0.249]); the paper should therefore
    describe the clean intervals as "variation over calibration draws", not as full confidence intervals.
  - `scripts/paper_corrections.py` writes `results/paper/v2_corrected_ci.csv` (reproduces all 32 intervals of `results/audit/ci_impact.md`)
    and the PAPER_NUMBERS sections "v2 corrected CIs" and "Detector AUROC without Dropout" (audit finding B1: Dropout scores 1.0 by
    construction). The 88 old interval rows are kept and marked "[superseded: v2 corrected CIs]"; no line was deleted; the v1 part of
    PAPER_NUMBERS is byte-identical.
  - `scripts/paper_material.py` writes new figures and tables with the corrected intervals and a cell map per table; the old v2 figures and
    tables are kept and listed in `results/paper/SUPERSEDED.md` and `latex/SUPERSEDED.txt`; `scripts/v2_paper.py` must not be re-run.
  - `scripts/check_paper_numbers.py` now compares every table cell with its own named number (audit finding B6); test-first:
    `tests/test_check_paper_numbers.py` failed on the old code (swapped cells passed) and passes now. Final run: 936 rows and 287 table
    numbers, 0 problems.
* O3 (why no conclusion changes). Every point estimate is unchanged. Every interval that excluded 0 still excludes 0, and the only interval
  that contains 0 is the same as before (gain of A on batch 8: old [-0.013, 0.042], corrected [-0.027, 0.054]). Key widths: pooled clean SVM
  gain +0.136, [0.132, 0.141] -> [0.117, 0.156]; calibrated A - SVM under faults +0.127, [0.123, 0.132] -> [0.118, 0.138]. The N8 verdict
  (clean gain > 0 with its interval above 0, and calibrated A >= SVM under faults) still holds. Without Dropout the mean detector AUROC is
  lower by about 0.01 (k=1) and 0.03 (k=2), and G2 still passes (the remaining fault types are all >= 0.90 per Test batch at k=1, medium).

## P. POST-HOC ANALYSIS: oracle selector bound (user request 2026-10-09; written before any number of it was computed)

* P1. Descriptive analysis only, from saved results: no model is trained, nothing is re-run on Test, no existing file is changed (this
  entry is appended). New files only in `results/oracle_selector/` (`scripts/` untouched).
* P2. Question: how much would a per-scenario "perfect arbiter" that picks A (`A_det_twin`) or B (`B_det`) gain over the better fixed
  method, where are the gains, and do runtime-visible signals (mean number of flagged sensors per row) separate the scenarios where B wins?
  Tie: |A - B| < 0.005 Macro-F1. Max score/threshold ratio is not saved in any result file and is reported as not available.
* P3. Order: Validation 7 (v1) and Drift-Dev stage 2 (v2 recal, batches 6 and 7) first; they are the only reference for any future arbiter
  design. v1 Test and v2 Test (calibrated model b) are DESCRIPTIVE ONLY: their numbers will NOT be used to design, tune or select any
  arbiter.
* P4. Per-row bound ("a row is correct if A or B is correct"): only where per-row predictions AND labels are available without reading
  Test labels (Validation 7: saved predictions + batch-7 labels from the loader). Extremely optimistic and not achievable; marked as such.

## Q. Previous-period recalibration (POST-HOC, EXPLORATORY; written before any of its results were computed)
User request 2026-10-10. Requested as section "P"; P is already the oracle-selector entry, so this is Q (same content).
* Q0 (status and data access). Exploratory and test-informed: batches 8-10 and the v2 Test results were seen before this design. It re-opens
  batches 8-10 (data AND labels) for a new evaluation; this departs from O ("no new reading of the Test data or labels") for this experiment
  only, by the user's decision of 2026-10-10 (new config `configs/v3_prevbatch.yaml`, `approved_by_user: true`). No frozen file, config, tag
  or earlier result is changed; new code in `scripts/v3_prevbatch.py`, tests in `tests/test_v3_prevbatch.py`, outputs in
  `results/v3_prevbatch/`. Branch `exp/prev-batch-recal`, local only.
* Q1 (question). Does few-shot recalibration with labelled rows from the PREVIOUS period still improve gas identification under faults,
  with zero labels from the evaluated period?
* Q2 (three arms, identical rows). For target t in {9, 10} and calibration seed s in {0..4}, the scored rows are
  `keep_mask(y_t, s, t)` (`scripts/ft_v2_recal.py:75-78`) in every arm, i.e. batch t minus the rows the v2 run used to calibrate batch t
  with seed s (arm c also leaves them out although it never used them, so the rows are identical):
  (a) uncal = the v2 model `results/final_test_v2/test/uncalibrated` (Train 1-7);
  (b) same  = the v2 model `b{t}_s{s}` (Train 1-7 + calibration rows of batch t);
  (c) prev  = the v2 model `b{t-1}_s{s}` (Train 1-7 + calibration rows of batch t-1, i.e. b8 rows for t=9 and b9 rows for t=10), applied
      unchanged to batch t: same scaler, SVM and median detector as fitted by v2 (no refit on batch t, thresholds unchanged), cap 4,
      C=10, gamma=0.01.
  The fitted v2 files are only read. Reduced B models are taken from that model's v2 cache (read-only); a reduced model missing there (a new
  acted set) is fitted by the frozen `StrategyKit.reduced_model` routine on the same model's Train+calibration rows (same seed, C, gamma)
  and cached under `results/v3_prevbatch/models/` only. Faults: the same 1081 scenarios (`ft_v2_recal.scenario_list()`, clean + k1/k2,
  every type and severity, fault seeds 0-4) applied to the FULL raw batch t with the raw Train 1-7 statistics, as v2, so the faulted
  matrices are identical across arms. Methods: SVM (no handling), A, B.
* Q3 (primary endpoint). A, mean Macro-F1 under faults (k1 and k2 weighted equally, N5), arm (c) minus arm (a), POOLED = per seed and
  scenario the Macro-F1 on the union of the kept rows of batches 9 and 10 (each batch predicted by its own arm model). Paired by scenario.
  95% interval: the v2 shared-index scenario bootstrap (`scripts/paper_corrections.py: shared_boot`; k-stratified, 1000 replicates,
  generator seed 0, one resample index per replicate shared by the 5 seeds). Verdict SUPPORTED if the whole interval is above 0;
  otherwise NOT SUPPORTED.
* Q4 (secondary, all reported, per batch 9, batch 10 and pooled side by side; batch 9 has 410 scored rows, batch 10 3540).
  - clean SVM gain (c)-(a): 95% t-interval over the 5 seeds (`paper_corrections.seed_t`); also for A and B;
  - within arm (c), A-SVM and B-SVM under faults (shared-index bootstrap);
  - gap to same-period calibration (c)-(b), clean (t over seeds) and under faults (bootstrap), SVM/A/B; share of the same-period gain kept
    = ((c)-(a)) / ((b)-(a)) under faults for A and B (point value, descriptive);
  - retention (J6): per scenario Macro-F1 under the fault / clean Macro-F1 of the same method, arm, subset and seed, averaged; worst case as
    `ft_v2_tables` (per seed the lowest per-scenario Macro-F1 including clean, mean over seeds) plus the identity of the worst scenarios.
* Q5 (gates, in this order; any failure = stop and report, no partial claim).
  (1) Tests first (`tests/test_v3_prevbatch.py`), must pass before the full run: no row of batch t is in the training or calibration data of
      the arm (c) model for t (and its Train rows equal Train 1-7 + the t-1 calibration rows exactly); scored indices identical across arms
      for every (t, s); the arm (c) detector is the stored v2 detector of `b{t-1}_s{s}` (its groups contain CAL_GROUP+(t-1), not
      CAL_GROUP+t) and is never refitted.
  (2) Smoke test (seed 0, a few scenarios), then the reproduction gate: arms (a) and (b) recomputed for batches 9 and 10, all 1081 scenarios,
      SVM/A/B: per-row labels identical to the saved v2 chunks, and Macro-F1 equal to `results/final_test_v2/test/scores.csv` (max |diff|
      <= 1e-9), clean values consistent with `clean.csv`.
  (3) Only then arm (c).
* Q6 (caveats registered now). The N9 interleaving caveat applies to (b) only; (c) has a real time gap (calibration from the previous batch).
  Batch 10 dominates the pooled rows. One calibration draw per seed; intervals resample scenarios only (O2 limitation).
* Q7 (no changes after results). No new n, seeds, models, scenarios, batches, arms or endpoint after any result is seen.
* Q8 (after the results and the independent audit, 2026-10-10 02:45; no analysis choice changed). The audit (`results/v3_prevbatch/AUDIT_SUBAGENT.md`)
  reproduced Q3 (+0.0248 [0.0235, 0.0260]) and every Q4 table, and found no Critical issue. Its Important findings were fixed without touching
  any prediction: (1) retention now follows J6's text (k1 and k2 weighted equally), and the unweighted value used by `ft_v2_tables` is
  kept next to it, labelled; (2) the row-identity test was tautological, so a test now rescores saved labels on the shared rows and must
  equal scores.csv for every arm (checked: arm (c) scored on other rows differs by ~1e-3); (3) prediction chunks are checked for arm,
  target, model and sids before use. Also, a re-run refuses an existing RUN_STARTED marker, sids are checked before pairing, and tests use
  a temporary model cache. After the fixes, scores.csv and q3_primary.csv were recomputed byte-identical.
* Q9 (secondary, defined after the Q results, not pre-registered; user request 2026-10-10, v4 Part 1; branch exp/prev-recal-v4, worktree
  ../fti-v4). From the saved v3 predictions and scores, plus ONE extra arm that needs no refit: (e) = the v2 model `b8_s{s}` applied unchanged
  to batch 10 (calibration 13-14 months old), the v3 kept rows `keep_mask(y_10, s, 10)`, all 1081 scenarios, SVM and A.
  (a) Macro-F1 under faults (k1/k2 equal) for SVM, A, B in arms (a), (b), (c), per batch and pooled; (b) full-pipeline effect A(c) - SVM(a)
  and B(c) - SVM(a) with the v2 shared-index scenario bootstrap; (c) J6 retention (k1/k2 equal) per arm; (d) shelf life: A-under-faults gain
  over (a) against calibration age (same period, 8->9, 9->10, 8->10), with the share of the same-period gain on the same target batch.
  Batch months (UCI documentation): 8 = 22-23, 9 = 24 and 30, 10 = 36. Outputs `results/v4_recal/part1_*.csv`, `PART1.md`. Descriptive only.

## R. Carrying calibration forward (POST-HOC, EXPLORATORY; designed after the Q results; written before any R result was computed)
User request 2026-10-10 (v4). Branch `exp/prev-recal-v4` in the worktree `../fti-v4` (from `exp/prev-batch-recal` 6a7239e); the main checkout is
read-only (v2 models, v3 predictions through the absolute path in `configs/v4_recal.yaml`). Drafted while Q9 was running, before any Q9 number
was read. Code: `scripts/v4_recal.py`; tests: `tests/test_v4_recal.py`; outputs: `results/v4_recal/`.
* R0 (status). Post-hoc and test-informed (the v3 Test results motivated it). Every choice below is made on development batches (1-7);
  Test (8-10) is opened once, and only if R3 says GO.
* R1 (development protocol, no Test data in any decision).
  - Base Train = the Drift-Dev Train of v2 (`configs/v2_drift_dev.yaml`: batches 1-3, cleaned by the invalid-value rule fitted on 1-3;
    verified: 3272 rows, batches {1, 2, 3}). Dev targets t in {6, 7}; previous-period pairs 5 -> 6 and 6 -> 7. Batch 5 is read only for its
    calibration rows (raw rows, like every evaluation batch). No development step reads batches 8-10 (test 4).
  - Calibration rows of batch b, seed s: `calib_rows(y_b, 10, s, b)`. Verified: batch 5 has NO gas 6 (toluene), so 5 -> 6 carries no toluene
    calibration (cf. batch 8: 18 toluene rows, 9 used); batches 6 and 7 give 10 rows for each of the six gases.
  - Scored rows: `keep_mask(y_t, s, t)` (the target's own seed-s calibration rows removed, so the same-period arm is scored on the same rows);
    for CAND-S the half H2 of those rows. The kept rows depend on batch-t labels only through this removal (identical rows across arms);
    no label of batch t enters any fit (test 1).
  - Scenarios: the v2 Drift-Dev set (`v2_arbiter.scenario_list()`: clean + k1/k2 at medium severity, fault seeds 0-4; 481), applied to the full
    raw batch t with the raw Train 1-3 statistics, as stage 2. Methods: SVM (no handling) and A (median detector, flag = ratio > 1, cap 4,
    twin allowed).
  - Model recipe unless a candidate says otherwise = `ft_v2_recal.fit_model` (N2): StandardScaler, SVC (C=10, gamma=0.01, random_state 0),
    median detector with each calibration batch as one extra group (CAL_GROUP + batch).
  - Reference arms on the same rows: uncal (Train 1-3), same (Train + cal(t)), prev (Train + cal(t-1)) = the v3 analog.
  - Dev gate (before any candidate number is used): uncal and same must reproduce v2 stage 2 (`results/v2/recal/scenarios.csv`, protocol
    drift_dev, models uncalibrated / calibrated) for SVM and A in every (t, s, scenario), max |diff| <= 5.1e-6 (the CSV has 5 decimals).
    Failure = stop and debug, no tournament.
  - Dev score of a configuration = A, Macro-F1 under faults: per (t, s) the k1 and k2 means averaged equally, then the mean over the 5 seeds
    and the 2 targets.
* R2 (candidates: seven configurations, fixed now; also in `configs/v4_recal.yaml`). Memory M(t) = the calibration periods before t that are
  not in Train, mirroring the Test chain: M(6) = {5}, M(7) = {5, 6}; on Test M(9) = {8}, M(10) = {8, 9}. Batch 4 is not used (the request
  fixes M(7) = {5, 6}). Calibration rows of every memory batch use the same seed s.
  - CAND-W, w in {1, 5, 20} (W1, W5, W20): Train + the calibration rows of every b in M(t); SVM sample_weight 1 for Train rows and w for
    calibration rows (w = 1 is fitted without weights); scaler unweighted; detector refitted on the same rows as in v2, unweighted, each
    calibration batch its own group. W1 at t = 6 equals prev exactly (a built-in check).
  - CAND-S, q in {0.3, 0.6} (S30, S60): H1/H2 = fixed disjoint halves of the kept rows of batch t
    (`perm = default_rng([s, t]).permutation(kept)`; H1 = the first floor(n/2), H2 = the rest). Start from prev. Predict the CLEAN, UNLABELED
    rows of H1 with prev's SVM (label = fast_svm_predict; margin = top-1 minus top-2 of the one-vs-rest `decision_function`); per predicted
    class c with n_c rows keep the ceil(q * n_c) largest margins. Refit the scaler and the SVM once on prev's rows (Train + cal(t-1)) plus
    the kept H1 rows with their pseudo-labels (unweighted); the detector is prev's, unchanged. Scored ONLY on H2; no H2 row, clean or faulted,
    enters any fit (test 2).
  - CAND-C, r in {1, 2} (C1, C2): rows = Train + the calibration rows of M(t), unweighted. The scaler is refitted on these rows; Z = their
    standardized values (NaN -> 0). For every gas g present in the calibration rows (and in Train): d_g = mean Z(calibration, g) - mean
    Z(Train, g). V = the top-r right singular vectors of the stacked d_g (uncentered SVD). Every classifier input is projected
    Z -> Z - Z V V^T (Train, calibration and evaluation rows; for A after reconstruction), and the SVM is refitted on the projected rows.
    The detector is prev's, unchanged. V uses only Train and past-period calibration rows (test 5).
  - prev on dev = the recipe on Train 1-3 + cal(t-1); on Test = the v2 model b{t-1}_s{s} (same recipe, checked to have Train 1-7 + cal(t-1)
    rows), which CAND-S and CAND-C start from.
* R3 (selection rule, dev only).
  - For configuration k: rows_k = H2 for CAND-S, the kept rows otherwise. delta_k = dev score(k) - dev score(prev), both on rows_k (paired
    by scenario); clean_k = clean SVM Macro-F1(k) - clean SVM Macro-F1(prev) on rows_k, mean over targets and seeds.
  - Eligible = clean_k >= -0.005. Winner = the largest delta among the eligible; every eligible configuration within 0.002 of that delta is
    tied, and the tie goes to the first in the order W1, W5, W20, C1, C2, S30, S60 (simpler first).
  - GO iff a winner exists and delta_winner >= 0.010. Otherwise NO-GO: no Test run, an entry in `results/NEGATIVE_RESULTS.md`, and v4 ends
    with Q9.
  - The script writes `results/v4_recal/r3_decision.json`; it is committed alone before the Test run, and the Test stage refuses to start
    unless that file is committed (tracked, no local change) and says GO.
* R4 (Test, one run, only on GO). Arm (d) = the winner fitted on Train 1-7 (+ the M(t) calibration rows, seeds 0-4) for targets 9 and 10, all
  1081 v2 scenarios, SVM and A. B is NOT added (decided now: it needs thousands of new reduced SVMs per model, outside the time box).
  Scored rows: H2 if the winner is a CAND-S configuration, otherwise the kept rows; arms (a), (b), (c) are re-scored on exactly those rows
  from the saved v3 predictions (provenance-checked). A RUN_STARTED marker refuses a second Test run (test 4b).
  - Reproduction gate before any Test number is used: (1) the saved v3 labels of arms (a), (b), (c), re-scored on the kept rows, equal
    `results/v3_prevbatch/scores.csv` (SVM, A, B; every (t, s, scenario); max |diff| <= 1e-9); (2) the v4 prediction code applied to the v2
    model of arm (c) (seed 0, 12 scenarios per target) gives labels identical to v3. Failure = hard stop.
* R5 (primary endpoint). A under faults (k1/k2 equal), (d) - (c), POOLED 9+10 (per seed and scenario, Macro-F1 on the union of the scored
  rows), paired by scenario; 95% interval = the v2 shared-index scenario bootstrap (`paper_corrections.shared_boot`: k-stratified, 1000,
  seed 0). SUPPORTED iff the lower bound > 0. Secondary: (d) - (a), (d) - (b), A - SVM within (d), per batch, J6 retention, worst scenarios,
  clean SVM (t over seeds).
* R6 (no changes after results). Nothing in R1-R5 changes once any R number is seen. Time box: the dev tournament must finish within 6 hours
  of this commit; otherwise stop, and v3 stands.
