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
