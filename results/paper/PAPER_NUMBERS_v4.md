# Numbers of v4: carrying a calibration forward (POST-HOC, EXPLORATORY; decisions_log Q9 and R)

Every value is read from a result file by `python scripts/v4_recal.py paper`; nothing is typed by hand. Under faults = k1/k2 weighted equally, mean over 5 calibration seeds. Test intervals: 95% shared-index scenario bootstrap (faults; scenarios only, O2), 95% t over seeds (clean). Dev tournament: Drift-Dev, targets 6 and 7, point values (selection rule R3).

R3 decision (results/v4_recal/r3_decision.json): winner = W1, delta = 0.0013, GO = False. Dev gate (devgate.json): 19240 rows, max |diff| 5.0e-06, passed = True. No Test run for R (NO-GO), so there is no R5 number.

| number | value | source |
|---|---|---|
| v4 shelf life, same period (b), b9, A_faults_gain_vs_a | 0.2345 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column A_faults_gain_vs_a |
| v4 shelf life, same period (b), b9, A_ci_low | 0.2295 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column A_ci_low |
| v4 shelf life, same period (b), b9, A_ci_high | 0.2389 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column A_ci_high |
| v4 shelf life, same period (b), b9, share_of_same_period_gain | 1.0000 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column share_of_same_period_gain |
| v4 shelf life, same period (b), b9, clean_svm_gain_vs_a | 0.2446 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column clean_svm_gain_vs_a |
| v4 shelf life, same period (b), b9, clean_ci_low | 0.2398 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column clean_ci_low |
| v4 shelf life, same period (b), b9, clean_ci_high | 0.2495 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b9, column clean_ci_high |
| v4 shelf life, same period (b), b10, A_faults_gain_vs_a | 0.1441 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column A_faults_gain_vs_a |
| v4 shelf life, same period (b), b10, A_ci_low | 0.1413 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column A_ci_low |
| v4 shelf life, same period (b), b10, A_ci_high | 0.1469 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column A_ci_high |
| v4 shelf life, same period (b), b10, share_of_same_period_gain | 1.0000 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column share_of_same_period_gain |
| v4 shelf life, same period (b), b10, clean_svm_gain_vs_a | 0.1440 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column clean_svm_gain_vs_a |
| v4 shelf life, same period (b), b10, clean_ci_low | 0.1205 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column clean_ci_low |
| v4 shelf life, same period (b), b10, clean_ci_high | 0.1675 | results/v4_recal/part1_shelf_life.csv, calibration=same period (b), target=b10, column clean_ci_high |
| v4 shelf life, 8 -> 9 (c), b9, A_faults_gain_vs_a | 0.0238 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column A_faults_gain_vs_a |
| v4 shelf life, 8 -> 9 (c), b9, A_ci_low | 0.0211 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column A_ci_low |
| v4 shelf life, 8 -> 9 (c), b9, A_ci_high | 0.0265 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column A_ci_high |
| v4 shelf life, 8 -> 9 (c), b9, share_of_same_period_gain | 0.1013 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column share_of_same_period_gain |
| v4 shelf life, 8 -> 9 (c), b9, clean_svm_gain_vs_a | 0.0078 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column clean_svm_gain_vs_a |
| v4 shelf life, 8 -> 9 (c), b9, clean_ci_low | 0.0021 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column clean_ci_low |
| v4 shelf life, 8 -> 9 (c), b9, clean_ci_high | 0.0134 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 9 (c), target=b9, column clean_ci_high |
| v4 shelf life, 9 -> 10 (c), b10, A_faults_gain_vs_a | 0.0244 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column A_faults_gain_vs_a |
| v4 shelf life, 9 -> 10 (c), b10, A_ci_low | 0.0231 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column A_ci_low |
| v4 shelf life, 9 -> 10 (c), b10, A_ci_high | 0.0256 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column A_ci_high |
| v4 shelf life, 9 -> 10 (c), b10, share_of_same_period_gain | 0.1690 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column share_of_same_period_gain |
| v4 shelf life, 9 -> 10 (c), b10, clean_svm_gain_vs_a | 0.0181 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column clean_svm_gain_vs_a |
| v4 shelf life, 9 -> 10 (c), b10, clean_ci_low | 0.0110 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column clean_ci_low |
| v4 shelf life, 9 -> 10 (c), b10, clean_ci_high | 0.0251 | results/v4_recal/part1_shelf_life.csv, calibration=9 -> 10 (c), target=b10, column clean_ci_high |
| v4 shelf life, 8 -> 10 (e), b10, A_faults_gain_vs_a | 0.0205 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column A_faults_gain_vs_a |
| v4 shelf life, 8 -> 10 (e), b10, A_ci_low | 0.0196 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column A_ci_low |
| v4 shelf life, 8 -> 10 (e), b10, A_ci_high | 0.0213 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column A_ci_high |
| v4 shelf life, 8 -> 10 (e), b10, share_of_same_period_gain | 0.1421 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column share_of_same_period_gain |
| v4 shelf life, 8 -> 10 (e), b10, clean_svm_gain_vs_a | 0.0184 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column clean_svm_gain_vs_a |
| v4 shelf life, 8 -> 10 (e), b10, clean_ci_low | 0.0141 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column clean_ci_low |
| v4 shelf life, 8 -> 10 (e), b10, clean_ci_high | 0.0227 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e), target=b10, column clean_ci_high |
| v4 shelf life, 8 -> 10 (e) minus 9 -> 10 (c), b10, A_faults_gain_vs_a | -0.0039 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e) minus 9 -> 10 (c), target=b10, column A_faults_gain_vs_a |
| v4 shelf life, 8 -> 10 (e) minus 9 -> 10 (c), b10, A_ci_low | -0.0051 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e) minus 9 -> 10 (c), target=b10, column A_ci_low |
| v4 shelf life, 8 -> 10 (e) minus 9 -> 10 (c), b10, A_ci_high | -0.0027 | results/v4_recal/part1_shelf_life.csv, calibration=8 -> 10 (e) minus 9 -> 10 (c), target=b10, column A_ci_high |
| v4 A in arm (c) - SVM in arm (a), under faults, b9, value | 0.1201 | results/v4_recal/part1_full_pipeline.csv, subset=b9, comparison=A in arm (c) - SVM in arm (a), under faults, column value |
| v4 A in arm (c) - SVM in arm (a), under faults, b9, ci_low | 0.1103 | results/v4_recal/part1_full_pipeline.csv, subset=b9, comparison=A in arm (c) - SVM in arm (a), under faults, column ci_low |
| v4 A in arm (c) - SVM in arm (a), under faults, b9, ci_high | 0.1299 | results/v4_recal/part1_full_pipeline.csv, subset=b9, comparison=A in arm (c) - SVM in arm (a), under faults, column ci_high |
| v4 B in arm (c) - SVM in arm (a), under faults, b9, value | 0.1276 | results/v4_recal/part1_full_pipeline.csv, subset=b9, comparison=B in arm (c) - SVM in arm (a), under faults, column value |
| v4 B in arm (c) - SVM in arm (a), under faults, b9, ci_low | 0.1194 | results/v4_recal/part1_full_pipeline.csv, subset=b9, comparison=B in arm (c) - SVM in arm (a), under faults, column ci_low |
| v4 B in arm (c) - SVM in arm (a), under faults, b9, ci_high | 0.1365 | results/v4_recal/part1_full_pipeline.csv, subset=b9, comparison=B in arm (c) - SVM in arm (a), under faults, column ci_high |
| v4 A in arm (c) - SVM in arm (a), under faults, b10, value | 0.1334 | results/v4_recal/part1_full_pipeline.csv, subset=b10, comparison=A in arm (c) - SVM in arm (a), under faults, column value |
| v4 A in arm (c) - SVM in arm (a), under faults, b10, ci_low | 0.1247 | results/v4_recal/part1_full_pipeline.csv, subset=b10, comparison=A in arm (c) - SVM in arm (a), under faults, column ci_low |
| v4 A in arm (c) - SVM in arm (a), under faults, b10, ci_high | 0.1422 | results/v4_recal/part1_full_pipeline.csv, subset=b10, comparison=A in arm (c) - SVM in arm (a), under faults, column ci_high |
| v4 B in arm (c) - SVM in arm (a), under faults, b10, value | 0.1446 | results/v4_recal/part1_full_pipeline.csv, subset=b10, comparison=B in arm (c) - SVM in arm (a), under faults, column value |
| v4 B in arm (c) - SVM in arm (a), under faults, b10, ci_low | 0.1367 | results/v4_recal/part1_full_pipeline.csv, subset=b10, comparison=B in arm (c) - SVM in arm (a), under faults, column ci_low |
| v4 B in arm (c) - SVM in arm (a), under faults, b10, ci_high | 0.1530 | results/v4_recal/part1_full_pipeline.csv, subset=b10, comparison=B in arm (c) - SVM in arm (a), under faults, column ci_high |
| v4 A in arm (c) - SVM in arm (a), under faults, pooled, value | 0.1319 | results/v4_recal/part1_full_pipeline.csv, subset=pooled, comparison=A in arm (c) - SVM in arm (a), under faults, column value |
| v4 A in arm (c) - SVM in arm (a), under faults, pooled, ci_low | 0.1236 | results/v4_recal/part1_full_pipeline.csv, subset=pooled, comparison=A in arm (c) - SVM in arm (a), under faults, column ci_low |
| v4 A in arm (c) - SVM in arm (a), under faults, pooled, ci_high | 0.1406 | results/v4_recal/part1_full_pipeline.csv, subset=pooled, comparison=A in arm (c) - SVM in arm (a), under faults, column ci_high |
| v4 B in arm (c) - SVM in arm (a), under faults, pooled, value | 0.1422 | results/v4_recal/part1_full_pipeline.csv, subset=pooled, comparison=B in arm (c) - SVM in arm (a), under faults, column value |
| v4 B in arm (c) - SVM in arm (a), under faults, pooled, ci_low | 0.1348 | results/v4_recal/part1_full_pipeline.csv, subset=pooled, comparison=B in arm (c) - SVM in arm (a), under faults, column ci_low |
| v4 B in arm (c) - SVM in arm (a), under faults, pooled, ci_high | 0.1502 | results/v4_recal/part1_full_pipeline.csv, subset=pooled, comparison=B in arm (c) - SVM in arm (a), under faults, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, b9, value | 0.6095 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=svm, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, b9, ci_low | 0.5993 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=svm, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, b9, ci_high | 0.6193 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=svm, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, A, b9, value | 0.7059 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=A, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, A, b9, ci_low | 0.6993 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=A, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, A, b9, ci_high | 0.7123 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=A, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, B, b9, value | 0.7041 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=B, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, B, b9, ci_low | 0.6992 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=B, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, B, b9, ci_high | 0.7089 | results/v4_recal/part1_levels.csv, subset=b9, arm=(a) uncalibrated, method=B, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, svm, b9, value | 0.7714 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=svm, column value |
| v4 Macro-F1 under faults, (b) same-period, svm, b9, ci_low | 0.7581 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=svm, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, svm, b9, ci_high | 0.7848 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=svm, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, A, b9, value | 0.9404 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=A, column value |
| v4 Macro-F1 under faults, (b) same-period, A, b9, ci_low | 0.9310 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=A, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, A, b9, ci_high | 0.9493 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=A, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, B, b9, value | 0.9547 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=B, column value |
| v4 Macro-F1 under faults, (b) same-period, B, b9, ci_low | 0.9474 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=B, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, B, b9, ci_high | 0.9609 | results/v4_recal/part1_levels.csv, subset=b9, arm=(b) same-period, method=B, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, svm, b9, value | 0.6341 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=svm, column value |
| v4 Macro-F1 under faults, (c) previous-period, svm, b9, ci_low | 0.6241 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=svm, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, svm, b9, ci_high | 0.6436 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=svm, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, A, b9, value | 0.7297 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=A, column value |
| v4 Macro-F1 under faults, (c) previous-period, A, b9, ci_low | 0.7226 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=A, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, A, b9, ci_high | 0.7362 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=A, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, B, b9, value | 0.7371 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=B, column value |
| v4 Macro-F1 under faults, (c) previous-period, B, b9, ci_low | 0.7323 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=B, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, B, b9, ci_high | 0.7417 | results/v4_recal/part1_levels.csv, subset=b9, arm=(c) previous-period, method=B, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, b10, value | 0.5121 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=svm, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, b10, ci_low | 0.5037 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=svm, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, b10, ci_high | 0.5205 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=svm, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, A, b10, value | 0.6211 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=A, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, A, b10, ci_low | 0.6148 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=A, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, A, b10, ci_high | 0.6270 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=A, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, B, b10, value | 0.6287 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=B, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, B, b10, ci_low | 0.6239 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=B, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, B, b10, ci_high | 0.6332 | results/v4_recal/part1_levels.csv, subset=b10, arm=(a) uncalibrated, method=B, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, svm, b10, value | 0.6415 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=svm, column value |
| v4 Macro-F1 under faults, (b) same-period, svm, b10, ci_low | 0.6329 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=svm, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, svm, b10, ci_high | 0.6501 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=svm, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, A, b10, value | 0.7653 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=A, column value |
| v4 Macro-F1 under faults, (b) same-period, A, b10, ci_low | 0.7587 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=A, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, A, b10, ci_high | 0.7714 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=A, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, B, b10, value | 0.7843 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=B, column value |
| v4 Macro-F1 under faults, (b) same-period, B, b10, ci_low | 0.7792 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=B, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, B, b10, ci_high | 0.7887 | results/v4_recal/part1_levels.csv, subset=b10, arm=(b) same-period, method=B, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, svm, b10, value | 0.5359 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=svm, column value |
| v4 Macro-F1 under faults, (c) previous-period, svm, b10, ci_low | 0.5271 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=svm, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, svm, b10, ci_high | 0.5446 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=svm, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, A, b10, value | 0.6455 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=A, column value |
| v4 Macro-F1 under faults, (c) previous-period, A, b10, ci_low | 0.6394 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=A, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, A, b10, ci_high | 0.6511 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=A, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, B, b10, value | 0.6567 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=B, column value |
| v4 Macro-F1 under faults, (c) previous-period, B, b10, ci_low | 0.6516 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=B, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, B, b10, ci_high | 0.6610 | results/v4_recal/part1_levels.csv, subset=b10, arm=(c) previous-period, method=B, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, pooled, value | 0.5293 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=svm, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, pooled, ci_low | 0.5213 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=svm, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, svm, pooled, ci_high | 0.5372 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=svm, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, A, pooled, value | 0.6364 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=A, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, A, pooled, ci_low | 0.6302 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=A, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, A, pooled, ci_high | 0.6421 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=A, column ci_high |
| v4 Macro-F1 under faults, (a) uncalibrated, B, pooled, value | 0.6423 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=B, column value |
| v4 Macro-F1 under faults, (a) uncalibrated, B, pooled, ci_low | 0.6378 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=B, column ci_low |
| v4 Macro-F1 under faults, (a) uncalibrated, B, pooled, ci_high | 0.6466 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(a) uncalibrated, method=B, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, svm, pooled, value | 0.6577 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=svm, column value |
| v4 Macro-F1 under faults, (b) same-period, svm, pooled, ci_low | 0.6492 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=svm, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, svm, pooled, ci_high | 0.6665 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=svm, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, A, pooled, value | 0.7836 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=A, column value |
| v4 Macro-F1 under faults, (b) same-period, A, pooled, ci_low | 0.7772 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=A, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, A, pooled, ci_high | 0.7899 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=A, column ci_high |
| v4 Macro-F1 under faults, (b) same-period, B, pooled, value | 0.8020 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=B, column value |
| v4 Macro-F1 under faults, (b) same-period, B, pooled, ci_low | 0.7971 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=B, column ci_low |
| v4 Macro-F1 under faults, (b) same-period, B, pooled, ci_high | 0.8063 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(b) same-period, method=B, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, svm, pooled, value | 0.5539 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=svm, column value |
| v4 Macro-F1 under faults, (c) previous-period, svm, pooled, ci_low | 0.5455 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=svm, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, svm, pooled, ci_high | 0.5622 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=svm, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, A, pooled, value | 0.6612 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=A, column value |
| v4 Macro-F1 under faults, (c) previous-period, A, pooled, ci_low | 0.6550 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=A, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, A, pooled, ci_high | 0.6667 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=A, column ci_high |
| v4 Macro-F1 under faults, (c) previous-period, B, pooled, value | 0.6716 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=B, column value |
| v4 Macro-F1 under faults, (c) previous-period, B, pooled, ci_low | 0.6668 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=B, column ci_low |
| v4 Macro-F1 under faults, (c) previous-period, B, pooled, ci_high | 0.6758 | results/v4_recal/part1_levels.csv, subset=pooled, arm=(c) previous-period, method=B, column ci_high |
| v4 Macro-F1 under faults, (e) two periods back (b8 on b10), svm, b10, value | 0.5292 | results/v4_recal/part1_levels.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=svm, column value |
| v4 Macro-F1 under faults, (e) two periods back (b8 on b10), svm, b10, ci_low | 0.5208 | results/v4_recal/part1_levels.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=svm, column ci_low |
| v4 Macro-F1 under faults, (e) two periods back (b8 on b10), svm, b10, ci_high | 0.5377 | results/v4_recal/part1_levels.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=svm, column ci_high |
| v4 Macro-F1 under faults, (e) two periods back (b8 on b10), A, b10, value | 0.6416 | results/v4_recal/part1_levels.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=A, column value |
| v4 Macro-F1 under faults, (e) two periods back (b8 on b10), A, b10, ci_low | 0.6352 | results/v4_recal/part1_levels.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=A, column ci_low |
| v4 Macro-F1 under faults, (e) two periods back (b8 on b10), A, b10, ci_high | 0.6478 | results/v4_recal/part1_levels.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=A, column ci_high |
| v4 retention_j6, (a) uncalibrated, svm, b9 | 0.8282 | results/v4_recal/part1_retention.csv, subset=b9, arm=(a) uncalibrated, method=svm, column retention_j6 |
| v4 worst, (a) uncalibrated, svm, b9 | 0.1168 | results/v4_recal/part1_retention.csv, subset=b9, arm=(a) uncalibrated, method=svm, column worst |
| v4 retention_j6, (a) uncalibrated, A, b9 | 0.9358 | results/v4_recal/part1_retention.csv, subset=b9, arm=(a) uncalibrated, method=A, column retention_j6 |
| v4 worst, (a) uncalibrated, A, b9 | 0.0372 | results/v4_recal/part1_retention.csv, subset=b9, arm=(a) uncalibrated, method=A, column worst |
| v4 retention_j6, (a) uncalibrated, B, b9 | 0.9328 | results/v4_recal/part1_retention.csv, subset=b9, arm=(a) uncalibrated, method=B, column retention_j6 |
| v4 worst, (a) uncalibrated, B, b9 | 0.3430 | results/v4_recal/part1_retention.csv, subset=b9, arm=(a) uncalibrated, method=B, column worst |
| v4 retention_j6, (b) same-period, svm, b9 | 0.7866 | results/v4_recal/part1_retention.csv, subset=b9, arm=(b) same-period, method=svm, column retention_j6 |
| v4 worst, (b) same-period, svm, b9 | 0.0622 | results/v4_recal/part1_retention.csv, subset=b9, arm=(b) same-period, method=svm, column worst |
| v4 retention_j6, (b) same-period, A, b9 | 0.9438 | results/v4_recal/part1_retention.csv, subset=b9, arm=(b) same-period, method=A, column retention_j6 |
| v4 worst, (b) same-period, A, b9 | 0.0564 | results/v4_recal/part1_retention.csv, subset=b9, arm=(b) same-period, method=A, column worst |
| v4 retention_j6, (b) same-period, B, b9 | 0.9576 | results/v4_recal/part1_retention.csv, subset=b9, arm=(b) same-period, method=B, column retention_j6 |
| v4 worst, (b) same-period, B, b9 | 0.2466 | results/v4_recal/part1_retention.csv, subset=b9, arm=(b) same-period, method=B, column worst |
| v4 retention_j6, (c) previous-period, svm, b9 | 0.8526 | results/v4_recal/part1_retention.csv, subset=b9, arm=(c) previous-period, method=svm, column retention_j6 |
| v4 worst, (c) previous-period, svm, b9 | 0.1304 | results/v4_recal/part1_retention.csv, subset=b9, arm=(c) previous-period, method=svm, column worst |
| v4 retention_j6, (c) previous-period, A, b9 | 0.9613 | results/v4_recal/part1_retention.csv, subset=b9, arm=(c) previous-period, method=A, column retention_j6 |
| v4 worst, (c) previous-period, A, b9 | 0.0476 | results/v4_recal/part1_retention.csv, subset=b9, arm=(c) previous-period, method=A, column worst |
| v4 retention_j6, (c) previous-period, B, b9 | 0.9693 | results/v4_recal/part1_retention.csv, subset=b9, arm=(c) previous-period, method=B, column retention_j6 |
| v4 worst, (c) previous-period, B, b9 | 0.3293 | results/v4_recal/part1_retention.csv, subset=b9, arm=(c) previous-period, method=B, column worst |
| v4 retention_j6, (a) uncalibrated, svm, b10 | 0.7595 | results/v4_recal/part1_retention.csv, subset=b10, arm=(a) uncalibrated, method=svm, column retention_j6 |
| v4 worst, (a) uncalibrated, svm, b10 | 0.0297 | results/v4_recal/part1_retention.csv, subset=b10, arm=(a) uncalibrated, method=svm, column worst |
| v4 retention_j6, (a) uncalibrated, A, b10 | 0.9461 | results/v4_recal/part1_retention.csv, subset=b10, arm=(a) uncalibrated, method=A, column retention_j6 |
| v4 worst, (a) uncalibrated, A, b10 | 0.0596 | results/v4_recal/part1_retention.csv, subset=b10, arm=(a) uncalibrated, method=A, column worst |
| v4 retention_j6, (a) uncalibrated, B, b10 | 0.9445 | results/v4_recal/part1_retention.csv, subset=b10, arm=(a) uncalibrated, method=B, column retention_j6 |
| v4 worst, (a) uncalibrated, B, b10 | 0.1458 | results/v4_recal/part1_retention.csv, subset=b10, arm=(a) uncalibrated, method=B, column worst |
| v4 retention_j6, (b) same-period, svm, b10 | 0.7840 | results/v4_recal/part1_retention.csv, subset=b10, arm=(b) same-period, method=svm, column retention_j6 |
| v4 worst, (b) same-period, svm, b10 | 0.0440 | results/v4_recal/part1_retention.csv, subset=b10, arm=(b) same-period, method=svm, column worst |
| v4 retention_j6, (b) same-period, A, b10 | 0.9550 | results/v4_recal/part1_retention.csv, subset=b10, arm=(b) same-period, method=A, column retention_j6 |
| v4 worst, (b) same-period, A, b10 | 0.0721 | results/v4_recal/part1_retention.csv, subset=b10, arm=(b) same-period, method=A, column worst |
| v4 retention_j6, (b) same-period, B, b10 | 0.9632 | results/v4_recal/part1_retention.csv, subset=b10, arm=(b) same-period, method=B, column retention_j6 |
| v4 worst, (b) same-period, B, b10 | 0.1743 | results/v4_recal/part1_retention.csv, subset=b10, arm=(b) same-period, method=B, column worst |
| v4 retention_j6, (c) previous-period, svm, b10 | 0.7740 | results/v4_recal/part1_retention.csv, subset=b10, arm=(c) previous-period, method=svm, column retention_j6 |
| v4 worst, (c) previous-period, svm, b10 | 0.0289 | results/v4_recal/part1_retention.csv, subset=b10, arm=(c) previous-period, method=svm, column worst |
| v4 retention_j6, (c) previous-period, A, b10 | 0.9575 | results/v4_recal/part1_retention.csv, subset=b10, arm=(c) previous-period, method=A, column retention_j6 |
| v4 worst, (c) previous-period, A, b10 | 0.0678 | results/v4_recal/part1_retention.csv, subset=b10, arm=(c) previous-period, method=A, column worst |
| v4 retention_j6, (c) previous-period, B, b10 | 0.9601 | results/v4_recal/part1_retention.csv, subset=b10, arm=(c) previous-period, method=B, column retention_j6 |
| v4 worst, (c) previous-period, B, b10 | 0.1483 | results/v4_recal/part1_retention.csv, subset=b10, arm=(c) previous-period, method=B, column worst |
| v4 retention_j6, (a) uncalibrated, svm, pooled | 0.7712 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(a) uncalibrated, method=svm, column retention_j6 |
| v4 worst, (a) uncalibrated, svm, pooled | 0.1268 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(a) uncalibrated, method=svm, column worst |
| v4 retention_j6, (a) uncalibrated, A, pooled | 0.9463 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(a) uncalibrated, method=A, column retention_j6 |
| v4 worst, (a) uncalibrated, A, pooled | 0.1178 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(a) uncalibrated, method=A, column worst |
| v4 retention_j6, (a) uncalibrated, B, pooled | 0.9436 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(a) uncalibrated, method=B, column retention_j6 |
| v4 worst, (a) uncalibrated, B, pooled | 0.2322 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(a) uncalibrated, method=B, column worst |
| v4 retention_j6, (b) same-period, svm, pooled | 0.7885 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(b) same-period, method=svm, column retention_j6 |
| v4 worst, (b) same-period, svm, pooled | 0.1607 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(b) same-period, method=svm, column worst |
| v4 retention_j6, (b) same-period, A, pooled | 0.9548 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(b) same-period, method=A, column retention_j6 |
| v4 worst, (b) same-period, A, pooled | 0.1373 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(b) same-period, method=A, column worst |
| v4 retention_j6, (b) same-period, B, pooled | 0.9634 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(b) same-period, method=B, column retention_j6 |
| v4 worst, (b) same-period, B, pooled | 0.3027 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(b) same-period, method=B, column worst |
| v4 retention_j6, (c) previous-period, svm, pooled | 0.7867 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(c) previous-period, method=svm, column retention_j6 |
| v4 worst, (c) previous-period, svm, pooled | 0.1263 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(c) previous-period, method=svm, column worst |
| v4 retention_j6, (c) previous-period, A, pooled | 0.9586 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(c) previous-period, method=A, column retention_j6 |
| v4 worst, (c) previous-period, A, pooled | 0.1021 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(c) previous-period, method=A, column worst |
| v4 retention_j6, (c) previous-period, B, pooled | 0.9616 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(c) previous-period, method=B, column retention_j6 |
| v4 worst, (c) previous-period, B, pooled | 0.2364 | results/v4_recal/part1_retention.csv, subset=pooled, arm=(c) previous-period, method=B, column worst |
| v4 retention_j6, (e) two periods back (b8 on b10), svm, b10 | 0.7639 | results/v4_recal/part1_retention.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=svm, column retention_j6 |
| v4 worst, (e) two periods back (b8 on b10), svm, b10 | 0.0434 | results/v4_recal/part1_retention.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=svm, column worst |
| v4 retention_j6, (e) two periods back (b8 on b10), A, b10 | 0.9530 | results/v4_recal/part1_retention.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=A, column retention_j6 |
| v4 worst, (e) two periods back (b8 on b10), A, b10 | 0.1015 | results/v4_recal/part1_retention.csv, subset=b10, arm=(e) two periods back (b8 on b10), method=A, column worst |
| v4 dev tournament, uncal (keep rows), dev_score_A_faults | 0.6297 | results/v4_recal/tournament.csv, config=uncal, rows=keep, column dev_score_A_faults |
| v4 dev tournament, uncal (keep rows), delta_vs_prev | -0.1091 | results/v4_recal/tournament.csv, config=uncal, rows=keep, column delta_vs_prev |
| v4 dev tournament, uncal (keep rows), delta_t6 | -0.0200 | results/v4_recal/tournament.csv, config=uncal, rows=keep, column delta_t6 |
| v4 dev tournament, uncal (keep rows), delta_t7 | -0.1982 | results/v4_recal/tournament.csv, config=uncal, rows=keep, column delta_t7 |
| v4 dev tournament, uncal (keep rows), clean_svm | 0.6166 | results/v4_recal/tournament.csv, config=uncal, rows=keep, column clean_svm |
| v4 dev tournament, uncal (keep rows), clean_svm_minus_prev | -0.1279 | results/v4_recal/tournament.csv, config=uncal, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, same (keep rows), dev_score_A_faults | 0.9176 | results/v4_recal/tournament.csv, config=same, rows=keep, column dev_score_A_faults |
| v4 dev tournament, same (keep rows), delta_vs_prev | 0.1788 | results/v4_recal/tournament.csv, config=same, rows=keep, column delta_vs_prev |
| v4 dev tournament, same (keep rows), delta_t6 | 0.2896 | results/v4_recal/tournament.csv, config=same, rows=keep, column delta_t6 |
| v4 dev tournament, same (keep rows), delta_t7 | 0.0680 | results/v4_recal/tournament.csv, config=same, rows=keep, column delta_t7 |
| v4 dev tournament, same (keep rows), clean_svm | 0.9390 | results/v4_recal/tournament.csv, config=same, rows=keep, column clean_svm |
| v4 dev tournament, same (keep rows), clean_svm_minus_prev | 0.1945 | results/v4_recal/tournament.csv, config=same, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, prev (keep rows), dev_score_A_faults | 0.7388 | results/v4_recal/tournament.csv, config=prev, rows=keep, column dev_score_A_faults |
| v4 dev tournament, prev (keep rows), delta_vs_prev | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=keep, column delta_vs_prev |
| v4 dev tournament, prev (keep rows), delta_t6 | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=keep, column delta_t6 |
| v4 dev tournament, prev (keep rows), delta_t7 | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=keep, column delta_t7 |
| v4 dev tournament, prev (keep rows), clean_svm | 0.7445 | results/v4_recal/tournament.csv, config=prev, rows=keep, column clean_svm |
| v4 dev tournament, prev (keep rows), clean_svm_minus_prev | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, prev (H2 rows), dev_score_A_faults | 0.7363 | results/v4_recal/tournament.csv, config=prev, rows=H2, column dev_score_A_faults |
| v4 dev tournament, prev (H2 rows), delta_vs_prev | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=H2, column delta_vs_prev |
| v4 dev tournament, prev (H2 rows), delta_t6 | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=H2, column delta_t6 |
| v4 dev tournament, prev (H2 rows), delta_t7 | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=H2, column delta_t7 |
| v4 dev tournament, prev (H2 rows), clean_svm | 0.7413 | results/v4_recal/tournament.csv, config=prev, rows=H2, column clean_svm |
| v4 dev tournament, prev (H2 rows), clean_svm_minus_prev | 0.0000 | results/v4_recal/tournament.csv, config=prev, rows=H2, column clean_svm_minus_prev |
| v4 dev tournament, W1 (keep rows), dev_score_A_faults | 0.7401 | results/v4_recal/tournament.csv, config=W1, rows=keep, column dev_score_A_faults |
| v4 dev tournament, W1 (keep rows), delta_vs_prev | 0.0013 | results/v4_recal/tournament.csv, config=W1, rows=keep, column delta_vs_prev |
| v4 dev tournament, W1 (keep rows), delta_t6 | 0.0000 | results/v4_recal/tournament.csv, config=W1, rows=keep, column delta_t6 |
| v4 dev tournament, W1 (keep rows), delta_t7 | 0.0027 | results/v4_recal/tournament.csv, config=W1, rows=keep, column delta_t7 |
| v4 dev tournament, W1 (keep rows), clean_svm | 0.7478 | results/v4_recal/tournament.csv, config=W1, rows=keep, column clean_svm |
| v4 dev tournament, W1 (keep rows), clean_svm_minus_prev | 0.0033 | results/v4_recal/tournament.csv, config=W1, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, W5 (keep rows), dev_score_A_faults | 0.7370 | results/v4_recal/tournament.csv, config=W5, rows=keep, column dev_score_A_faults |
| v4 dev tournament, W5 (keep rows), delta_vs_prev | -0.0018 | results/v4_recal/tournament.csv, config=W5, rows=keep, column delta_vs_prev |
| v4 dev tournament, W5 (keep rows), delta_t6 | 0.0000 | results/v4_recal/tournament.csv, config=W5, rows=keep, column delta_t6 |
| v4 dev tournament, W5 (keep rows), delta_t7 | -0.0036 | results/v4_recal/tournament.csv, config=W5, rows=keep, column delta_t7 |
| v4 dev tournament, W5 (keep rows), clean_svm | 0.7487 | results/v4_recal/tournament.csv, config=W5, rows=keep, column clean_svm |
| v4 dev tournament, W5 (keep rows), clean_svm_minus_prev | 0.0042 | results/v4_recal/tournament.csv, config=W5, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, W20 (keep rows), dev_score_A_faults | 0.7351 | results/v4_recal/tournament.csv, config=W20, rows=keep, column dev_score_A_faults |
| v4 dev tournament, W20 (keep rows), delta_vs_prev | -0.0036 | results/v4_recal/tournament.csv, config=W20, rows=keep, column delta_vs_prev |
| v4 dev tournament, W20 (keep rows), delta_t6 | 0.0000 | results/v4_recal/tournament.csv, config=W20, rows=keep, column delta_t6 |
| v4 dev tournament, W20 (keep rows), delta_t7 | -0.0073 | results/v4_recal/tournament.csv, config=W20, rows=keep, column delta_t7 |
| v4 dev tournament, W20 (keep rows), clean_svm | 0.7453 | results/v4_recal/tournament.csv, config=W20, rows=keep, column clean_svm |
| v4 dev tournament, W20 (keep rows), clean_svm_minus_prev | 0.0008 | results/v4_recal/tournament.csv, config=W20, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, C1 (keep rows), dev_score_A_faults | 0.7415 | results/v4_recal/tournament.csv, config=C1, rows=keep, column dev_score_A_faults |
| v4 dev tournament, C1 (keep rows), delta_vs_prev | 0.0027 | results/v4_recal/tournament.csv, config=C1, rows=keep, column delta_vs_prev |
| v4 dev tournament, C1 (keep rows), delta_t6 | 0.0059 | results/v4_recal/tournament.csv, config=C1, rows=keep, column delta_t6 |
| v4 dev tournament, C1 (keep rows), delta_t7 | -0.0004 | results/v4_recal/tournament.csv, config=C1, rows=keep, column delta_t7 |
| v4 dev tournament, C1 (keep rows), clean_svm | 0.7511 | results/v4_recal/tournament.csv, config=C1, rows=keep, column clean_svm |
| v4 dev tournament, C1 (keep rows), clean_svm_minus_prev | 0.0066 | results/v4_recal/tournament.csv, config=C1, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, C2 (keep rows), dev_score_A_faults | 0.7370 | results/v4_recal/tournament.csv, config=C2, rows=keep, column dev_score_A_faults |
| v4 dev tournament, C2 (keep rows), delta_vs_prev | -0.0018 | results/v4_recal/tournament.csv, config=C2, rows=keep, column delta_vs_prev |
| v4 dev tournament, C2 (keep rows), delta_t6 | 0.0516 | results/v4_recal/tournament.csv, config=C2, rows=keep, column delta_t6 |
| v4 dev tournament, C2 (keep rows), delta_t7 | -0.0552 | results/v4_recal/tournament.csv, config=C2, rows=keep, column delta_t7 |
| v4 dev tournament, C2 (keep rows), clean_svm | 0.7452 | results/v4_recal/tournament.csv, config=C2, rows=keep, column clean_svm |
| v4 dev tournament, C2 (keep rows), clean_svm_minus_prev | 0.0007 | results/v4_recal/tournament.csv, config=C2, rows=keep, column clean_svm_minus_prev |
| v4 dev tournament, S30 (H2 rows), dev_score_A_faults | 0.7220 | results/v4_recal/tournament.csv, config=S30, rows=H2, column dev_score_A_faults |
| v4 dev tournament, S30 (H2 rows), delta_vs_prev | -0.0143 | results/v4_recal/tournament.csv, config=S30, rows=H2, column delta_vs_prev |
| v4 dev tournament, S30 (H2 rows), delta_t6 | -0.0110 | results/v4_recal/tournament.csv, config=S30, rows=H2, column delta_t6 |
| v4 dev tournament, S30 (H2 rows), delta_t7 | -0.0175 | results/v4_recal/tournament.csv, config=S30, rows=H2, column delta_t7 |
| v4 dev tournament, S30 (H2 rows), clean_svm | 0.7343 | results/v4_recal/tournament.csv, config=S30, rows=H2, column clean_svm |
| v4 dev tournament, S30 (H2 rows), clean_svm_minus_prev | -0.0070 | results/v4_recal/tournament.csv, config=S30, rows=H2, column clean_svm_minus_prev |
| v4 dev tournament, S60 (H2 rows), dev_score_A_faults | 0.7352 | results/v4_recal/tournament.csv, config=S60, rows=H2, column dev_score_A_faults |
| v4 dev tournament, S60 (H2 rows), delta_vs_prev | -0.0010 | results/v4_recal/tournament.csv, config=S60, rows=H2, column delta_vs_prev |
| v4 dev tournament, S60 (H2 rows), delta_t6 | -0.0063 | results/v4_recal/tournament.csv, config=S60, rows=H2, column delta_t6 |
| v4 dev tournament, S60 (H2 rows), delta_t7 | 0.0042 | results/v4_recal/tournament.csv, config=S60, rows=H2, column delta_t7 |
| v4 dev tournament, S60 (H2 rows), clean_svm | 0.7478 | results/v4_recal/tournament.csv, config=S60, rows=H2, column clean_svm |
| v4 dev tournament, S60 (H2 rows), clean_svm_minus_prev | 0.0065 | results/v4_recal/tournament.csv, config=S60, rows=H2, column clean_svm_minus_prev |
