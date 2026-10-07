# Data cleaning rule

## Two kinds of extreme values
| kind | what it is | decision |
|---|---|---|
| statistical outliers (Tukey IQR fences) | real drift and strong responses; 83 of the 128 features show a batch-drift pattern and the outliers occur in bursts (dispersion index 19.7 in Train) | **kept** (Phase 2: winsorising lowers SVM Macro-F1 by 0.021, dropping the 587 rows with >10% outlying features gains only 0.004 < 0.005) |
| physically invalid values | corrupt records, e.g. `|DR|` = 31,165 where the median is about 2.6 | **removed from Train only**, by the rule below |

## Rule (fixed, `src/cleaning.py`)
* For every feature, median and MAD (median absolute deviation, unscaled) are computed on the **Train rows of the protocol only**.
* A cell is invalid if `|x - median| / MAD > 1000`; a record is invalid if any of its 128 cells is.
* Features with MAD = 0 cannot be scored (none occur).
* Train: flagged records are dropped before anything is fitted (scalers, imputers, selectors, models, fault scales).
* Evaluation rows (Validation, reference hold-out, later Test): **never dropped**, only counted, because a corrupt record in operation is a real fault the system must survive. They stay in classification scoring. They are left out of the reconstruction errors only, since their "true" value is itself corrupt.
* The threshold was fixed before looking at its effect and was not tuned.

## Records captured (batches 1-7)
| protocol | rule fitted on | flagged in Train (dropped) | flagged in evaluation (kept) |
|---|---|---|---|
| temporal | batches 1-6 (5,933 rows) | batch 2 line 222 (Ethanol), batch 2 line 380 (Ethylene) | none |
| reference_iid | 80% hold-out Train (7,636 rows) | batch 2 line 223 (Ethanol), batch 2 line 380 (Ethylene) | batch 2 line 222 (Ethanol) |

| record | invalid cells (beyond 1000 MAD) | values |
|---|---|---|
| batch 2, line 222, Ethanol | S06, S07, S08 `|DR|` (3 cells) | S06 31,165; S07 8,229; S08 16,242 (typical median 2.6-4) |
| batch 2, line 380, Ethylene | S04 `EMAi0.1` (1 cell) | 12,006 (median 12.2) |
| batch 2, line 223, Ethanol (borderline) | S05 `EMAd0.1` (1 cell, only in the reference protocol, 1,085 MAD; below the threshold in the temporal protocol) | -880 (median -4.2) |

Observation, without claiming a cause: in the first record the `|DR|` of S05 (344) to S08 are abnormal together in a single record, although only S06-S08 exceed the rule; in the second, S03 `EMAi0.1` (3,231) is also elevated next to S04. So anomalous events that touch several sensors at once exist in the real data. Their origin is not established here.

## Effect on the Train statistics and on the old baseline
Standard deviation of the Train features before / after dropping the two records: `S06 |DR|` x316, `S08 |DR|` x48, `S07 |DR|` x25, `S05 |DR|` x3.7, `S04 EMAi0.1` x3.0, `S01 |DR|` x2.3, `S05 EMAi0.1` x1.6 (all other features unchanged).
StandardScaler therefore compressed these features by accident. A 2x2 design (C=10, gamma=scale) isolates the cause: SVM fitted on the cleaned rows but scaled with the old statistics gives 0.8764; scaled with the cleaned statistics 0.8563. The two records as training samples are irrelevant (-0.002); the whole change comes from the scaler statistics. The previously reported SVM Macro-F1 of **0.878 was inflated by 0.022** by two corrupt Train records that, through the inflated standard deviation, down-weighted drift-sensitive features by chance. Per-gas SVM F1 change: Acetaldehyde -0.048, Toluene -0.038, Acetone -0.025, Ethanol -0.010, Ethylene -0.008, Ammonia +0.015.
Files: `results/main_cleaned/diagnosis/`, `results/preprocessing/cleaning/`.
