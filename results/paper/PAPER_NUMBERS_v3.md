# Numbers of the previous-period recalibration (v3; POST-HOC, EXPLORATORY; decisions_log Q)

Every value is read from a result file by `python scripts/v3_prevbatch.py paper`; nothing is typed by hand. Arms on identical rows: (a) uncalibrated, (b) calibrated on batch t, (c) calibrated on batch t-1, scored on batch t in {9, 10}. Under faults = k1/k2 weighted equally, mean over 5 calibration seeds. Intervals: 95% shared-index scenario bootstrap (faults; resamples scenarios only, O2) and 95% t over the 5 seeds (clean).

| number | value | source |
|---|---|---|
| v3 primary (Q3): A under faults (c)-(a), pooled b9+b10, value | 0.0248 | results/v3_prevbatch/q3_primary.csv, single row, column value |
| v3 primary (Q3): A under faults (c)-(a), pooled b9+b10, ci_low | 0.0235 | results/v3_prevbatch/q3_primary.csv, single row, column ci_low |
| v3 primary (Q3): A under faults (c)-(a), pooled b9+b10, ci_high | 0.0260 | results/v3_prevbatch/q3_primary.csv, single row, column ci_high |
| v3 Macro-F1 under faults, b9, svm, a, value | 0.6095 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=a, column value |
| v3 Macro-F1 under faults, b9, svm, a, ci_low | 0.5993 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=a, column ci_low |
| v3 Macro-F1 under faults, b9, svm, a, ci_high | 0.6193 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=a, column ci_high |
| v3 Macro-F1 under faults, b9, svm, b, value | 0.7714 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=b, column value |
| v3 Macro-F1 under faults, b9, svm, b, ci_low | 0.7581 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=b, column ci_low |
| v3 Macro-F1 under faults, b9, svm, b, ci_high | 0.7848 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=b, column ci_high |
| v3 Macro-F1 under faults, b9, svm, c, value | 0.6341 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=c, column value |
| v3 Macro-F1 under faults, b9, svm, c, ci_low | 0.6241 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=c, column ci_low |
| v3 Macro-F1 under faults, b9, svm, c, ci_high | 0.6436 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=svm, arm=c, column ci_high |
| v3 Macro-F1 under faults, b9, A, a, value | 0.7059 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=a, column value |
| v3 Macro-F1 under faults, b9, A, a, ci_low | 0.6993 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=a, column ci_low |
| v3 Macro-F1 under faults, b9, A, a, ci_high | 0.7123 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=a, column ci_high |
| v3 Macro-F1 under faults, b9, A, b, value | 0.9404 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=b, column value |
| v3 Macro-F1 under faults, b9, A, b, ci_low | 0.9310 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=b, column ci_low |
| v3 Macro-F1 under faults, b9, A, b, ci_high | 0.9493 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=b, column ci_high |
| v3 Macro-F1 under faults, b9, A, c, value | 0.7297 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=c, column value |
| v3 Macro-F1 under faults, b9, A, c, ci_low | 0.7226 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=c, column ci_low |
| v3 Macro-F1 under faults, b9, A, c, ci_high | 0.7362 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=A, arm=c, column ci_high |
| v3 Macro-F1 under faults, b9, B, a, value | 0.7041 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=a, column value |
| v3 Macro-F1 under faults, b9, B, a, ci_low | 0.6992 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=a, column ci_low |
| v3 Macro-F1 under faults, b9, B, a, ci_high | 0.7089 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=a, column ci_high |
| v3 Macro-F1 under faults, b9, B, b, value | 0.9547 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=b, column value |
| v3 Macro-F1 under faults, b9, B, b, ci_low | 0.9474 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=b, column ci_low |
| v3 Macro-F1 under faults, b9, B, b, ci_high | 0.9609 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=b, column ci_high |
| v3 Macro-F1 under faults, b9, B, c, value | 0.7371 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=c, column value |
| v3 Macro-F1 under faults, b9, B, c, ci_low | 0.7323 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=c, column ci_low |
| v3 Macro-F1 under faults, b9, B, c, ci_high | 0.7417 | results/v3_prevbatch/q4_levels_faults.csv, subset=b9, method=B, arm=c, column ci_high |
| v3 Macro-F1 under faults, b10, svm, a, value | 0.5121 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=a, column value |
| v3 Macro-F1 under faults, b10, svm, a, ci_low | 0.5037 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=a, column ci_low |
| v3 Macro-F1 under faults, b10, svm, a, ci_high | 0.5205 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=a, column ci_high |
| v3 Macro-F1 under faults, b10, svm, b, value | 0.6415 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=b, column value |
| v3 Macro-F1 under faults, b10, svm, b, ci_low | 0.6329 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=b, column ci_low |
| v3 Macro-F1 under faults, b10, svm, b, ci_high | 0.6501 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=b, column ci_high |
| v3 Macro-F1 under faults, b10, svm, c, value | 0.5359 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=c, column value |
| v3 Macro-F1 under faults, b10, svm, c, ci_low | 0.5271 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=c, column ci_low |
| v3 Macro-F1 under faults, b10, svm, c, ci_high | 0.5446 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=svm, arm=c, column ci_high |
| v3 Macro-F1 under faults, b10, A, a, value | 0.6211 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=a, column value |
| v3 Macro-F1 under faults, b10, A, a, ci_low | 0.6148 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=a, column ci_low |
| v3 Macro-F1 under faults, b10, A, a, ci_high | 0.6270 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=a, column ci_high |
| v3 Macro-F1 under faults, b10, A, b, value | 0.7653 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=b, column value |
| v3 Macro-F1 under faults, b10, A, b, ci_low | 0.7587 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=b, column ci_low |
| v3 Macro-F1 under faults, b10, A, b, ci_high | 0.7714 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=b, column ci_high |
| v3 Macro-F1 under faults, b10, A, c, value | 0.6455 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=c, column value |
| v3 Macro-F1 under faults, b10, A, c, ci_low | 0.6394 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=c, column ci_low |
| v3 Macro-F1 under faults, b10, A, c, ci_high | 0.6511 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=A, arm=c, column ci_high |
| v3 Macro-F1 under faults, b10, B, a, value | 0.6287 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=a, column value |
| v3 Macro-F1 under faults, b10, B, a, ci_low | 0.6239 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=a, column ci_low |
| v3 Macro-F1 under faults, b10, B, a, ci_high | 0.6332 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=a, column ci_high |
| v3 Macro-F1 under faults, b10, B, b, value | 0.7843 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=b, column value |
| v3 Macro-F1 under faults, b10, B, b, ci_low | 0.7792 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=b, column ci_low |
| v3 Macro-F1 under faults, b10, B, b, ci_high | 0.7887 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=b, column ci_high |
| v3 Macro-F1 under faults, b10, B, c, value | 0.6567 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=c, column value |
| v3 Macro-F1 under faults, b10, B, c, ci_low | 0.6516 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=c, column ci_low |
| v3 Macro-F1 under faults, b10, B, c, ci_high | 0.6610 | results/v3_prevbatch/q4_levels_faults.csv, subset=b10, method=B, arm=c, column ci_high |
| v3 Macro-F1 under faults, pooled, svm, a, value | 0.5293 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=a, column value |
| v3 Macro-F1 under faults, pooled, svm, a, ci_low | 0.5213 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=a, column ci_low |
| v3 Macro-F1 under faults, pooled, svm, a, ci_high | 0.5372 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=a, column ci_high |
| v3 Macro-F1 under faults, pooled, svm, b, value | 0.6577 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=b, column value |
| v3 Macro-F1 under faults, pooled, svm, b, ci_low | 0.6492 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=b, column ci_low |
| v3 Macro-F1 under faults, pooled, svm, b, ci_high | 0.6665 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=b, column ci_high |
| v3 Macro-F1 under faults, pooled, svm, c, value | 0.5539 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=c, column value |
| v3 Macro-F1 under faults, pooled, svm, c, ci_low | 0.5455 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=c, column ci_low |
| v3 Macro-F1 under faults, pooled, svm, c, ci_high | 0.5622 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=svm, arm=c, column ci_high |
| v3 Macro-F1 under faults, pooled, A, a, value | 0.6364 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=a, column value |
| v3 Macro-F1 under faults, pooled, A, a, ci_low | 0.6302 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=a, column ci_low |
| v3 Macro-F1 under faults, pooled, A, a, ci_high | 0.6421 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=a, column ci_high |
| v3 Macro-F1 under faults, pooled, A, b, value | 0.7836 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=b, column value |
| v3 Macro-F1 under faults, pooled, A, b, ci_low | 0.7772 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=b, column ci_low |
| v3 Macro-F1 under faults, pooled, A, b, ci_high | 0.7899 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=b, column ci_high |
| v3 Macro-F1 under faults, pooled, A, c, value | 0.6612 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=c, column value |
| v3 Macro-F1 under faults, pooled, A, c, ci_low | 0.6550 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=c, column ci_low |
| v3 Macro-F1 under faults, pooled, A, c, ci_high | 0.6667 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=A, arm=c, column ci_high |
| v3 Macro-F1 under faults, pooled, B, a, value | 0.6423 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=a, column value |
| v3 Macro-F1 under faults, pooled, B, a, ci_low | 0.6378 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=a, column ci_low |
| v3 Macro-F1 under faults, pooled, B, a, ci_high | 0.6466 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=a, column ci_high |
| v3 Macro-F1 under faults, pooled, B, b, value | 0.8020 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=b, column value |
| v3 Macro-F1 under faults, pooled, B, b, ci_low | 0.7971 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=b, column ci_low |
| v3 Macro-F1 under faults, pooled, B, b, ci_high | 0.8063 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=b, column ci_high |
| v3 Macro-F1 under faults, pooled, B, c, value | 0.6716 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=c, column value |
| v3 Macro-F1 under faults, pooled, B, c, ci_low | 0.6668 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=c, column ci_low |
| v3 Macro-F1 under faults, pooled, B, c, ci_high | 0.6758 | results/v3_prevbatch/q4_levels_faults.csv, subset=pooled, method=B, arm=c, column ci_high |
| v3 b9, (c)-(a) svm under faults, value | 0.0246 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) svm under faults, column value |
| v3 b9, (c)-(a) svm under faults, ci_low | 0.0207 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) svm under faults, column ci_low |
| v3 b9, (c)-(a) svm under faults, ci_high | 0.0284 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) svm under faults, column ci_high |
| v3 b9, (b)-(a) svm under faults, value | 0.1618 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) svm under faults, column value |
| v3 b9, (b)-(a) svm under faults, ci_low | 0.1532 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) svm under faults, column ci_low |
| v3 b9, (b)-(a) svm under faults, ci_high | 0.1704 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) svm under faults, column ci_high |
| v3 b9, (c)-(b) svm under faults, value | -0.1373 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) svm under faults, column value |
| v3 b9, (c)-(b) svm under faults, ci_low | -0.1449 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) svm under faults, column ci_low |
| v3 b9, (c)-(b) svm under faults, ci_high | -0.1303 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) svm under faults, column ci_high |
| v3 b9, (c)-(a) A under faults, value | 0.0238 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) A under faults, column value |
| v3 b9, (c)-(a) A under faults, ci_low | 0.0211 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) A under faults, column ci_low |
| v3 b9, (c)-(a) A under faults, ci_high | 0.0265 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) A under faults, column ci_high |
| v3 b9, (b)-(a) A under faults, value | 0.2345 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) A under faults, column value |
| v3 b9, (b)-(a) A under faults, ci_low | 0.2295 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) A under faults, column ci_low |
| v3 b9, (b)-(a) A under faults, ci_high | 0.2389 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) A under faults, column ci_high |
| v3 b9, (c)-(b) A under faults, value | -0.2108 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) A under faults, column value |
| v3 b9, (c)-(b) A under faults, ci_low | -0.2156 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) A under faults, column ci_low |
| v3 b9, (c)-(b) A under faults, ci_high | -0.2061 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) A under faults, column ci_high |
| v3 b9, (c)-(a) B under faults, value | 0.0330 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) B under faults, column value |
| v3 b9, (c)-(a) B under faults, ci_low | 0.0304 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) B under faults, column ci_low |
| v3 b9, (c)-(a) B under faults, ci_high | 0.0359 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(a) B under faults, column ci_high |
| v3 b9, (b)-(a) B under faults, value | 0.2506 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) B under faults, column value |
| v3 b9, (b)-(a) B under faults, ci_low | 0.2460 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) B under faults, column ci_low |
| v3 b9, (b)-(a) B under faults, ci_high | 0.2550 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(b)-(a) B under faults, column ci_high |
| v3 b9, (c)-(b) B under faults, value | -0.2175 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) B under faults, column value |
| v3 b9, (c)-(b) B under faults, ci_low | -0.2215 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) B under faults, column ci_low |
| v3 b9, (c)-(b) B under faults, ci_high | -0.2136 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=(c)-(b) B under faults, column ci_high |
| v3 b9, A-SVM under faults, arm (a), value | 0.0964 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (a), column value |
| v3 b9, A-SVM under faults, arm (a), ci_low | 0.0876 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (a), column ci_low |
| v3 b9, A-SVM under faults, arm (a), ci_high | 0.1055 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (a), column ci_high |
| v3 b9, B-SVM under faults, arm (a), value | 0.0945 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (a), column value |
| v3 b9, B-SVM under faults, arm (a), ci_low | 0.0863 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (a), column ci_low |
| v3 b9, B-SVM under faults, arm (a), ci_high | 0.1032 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (a), column ci_high |
| v3 b9, A-SVM under faults, arm (b), value | 0.1691 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (b), column value |
| v3 b9, A-SVM under faults, arm (b), ci_low | 0.1548 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (b), column ci_low |
| v3 b9, A-SVM under faults, arm (b), ci_high | 0.1834 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (b), column ci_high |
| v3 b9, B-SVM under faults, arm (b), value | 0.1833 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (b), column value |
| v3 b9, B-SVM under faults, arm (b), ci_low | 0.1710 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (b), column ci_low |
| v3 b9, B-SVM under faults, arm (b), ci_high | 0.1964 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (b), column ci_high |
| v3 b9, A-SVM under faults, arm (c), value | 0.0956 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (c), column value |
| v3 b9, A-SVM under faults, arm (c), ci_low | 0.0859 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (c), column ci_low |
| v3 b9, A-SVM under faults, arm (c), ci_high | 0.1059 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=A-SVM under faults, arm (c), column ci_high |
| v3 b9, B-SVM under faults, arm (c), value | 0.1030 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (c), column value |
| v3 b9, B-SVM under faults, arm (c), ci_low | 0.0945 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (c), column ci_low |
| v3 b9, B-SVM under faults, arm (c), ci_high | 0.1121 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b9, comparison=B-SVM under faults, arm (c), column ci_high |
| v3 b10, (c)-(a) svm under faults, value | 0.0238 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) svm under faults, column value |
| v3 b10, (c)-(a) svm under faults, ci_low | 0.0221 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) svm under faults, column ci_low |
| v3 b10, (c)-(a) svm under faults, ci_high | 0.0254 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) svm under faults, column ci_high |
| v3 b10, (b)-(a) svm under faults, value | 0.1294 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) svm under faults, column value |
| v3 b10, (b)-(a) svm under faults, ci_low | 0.1272 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) svm under faults, column ci_low |
| v3 b10, (b)-(a) svm under faults, ci_high | 0.1315 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) svm under faults, column ci_high |
| v3 b10, (c)-(b) svm under faults, value | -0.1056 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) svm under faults, column value |
| v3 b10, (c)-(b) svm under faults, ci_low | -0.1075 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) svm under faults, column ci_low |
| v3 b10, (c)-(b) svm under faults, ci_high | -0.1039 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) svm under faults, column ci_high |
| v3 b10, (c)-(a) A under faults, value | 0.0244 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) A under faults, column value |
| v3 b10, (c)-(a) A under faults, ci_low | 0.0231 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) A under faults, column ci_low |
| v3 b10, (c)-(a) A under faults, ci_high | 0.0256 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) A under faults, column ci_high |
| v3 b10, (b)-(a) A under faults, value | 0.1441 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) A under faults, column value |
| v3 b10, (b)-(a) A under faults, ci_low | 0.1413 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) A under faults, column ci_low |
| v3 b10, (b)-(a) A under faults, ci_high | 0.1469 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) A under faults, column ci_high |
| v3 b10, (c)-(b) A under faults, value | -0.1198 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) A under faults, column value |
| v3 b10, (c)-(b) A under faults, ci_low | -0.1220 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) A under faults, column ci_low |
| v3 b10, (c)-(b) A under faults, ci_high | -0.1175 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) A under faults, column ci_high |
| v3 b10, (c)-(a) B under faults, value | 0.0279 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) B under faults, column value |
| v3 b10, (c)-(a) B under faults, ci_low | 0.0266 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) B under faults, column ci_low |
| v3 b10, (c)-(a) B under faults, ci_high | 0.0292 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(a) B under faults, column ci_high |
| v3 b10, (b)-(a) B under faults, value | 0.1555 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) B under faults, column value |
| v3 b10, (b)-(a) B under faults, ci_low | 0.1532 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) B under faults, column ci_low |
| v3 b10, (b)-(a) B under faults, ci_high | 0.1575 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(b)-(a) B under faults, column ci_high |
| v3 b10, (c)-(b) B under faults, value | -0.1276 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) B under faults, column value |
| v3 b10, (c)-(b) B under faults, ci_low | -0.1292 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) B under faults, column ci_low |
| v3 b10, (c)-(b) B under faults, ci_high | -0.1260 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=(c)-(b) B under faults, column ci_high |
| v3 b10, A-SVM under faults, arm (a), value | 0.1090 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (a), column value |
| v3 b10, A-SVM under faults, arm (a), ci_low | 0.1008 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (a), column ci_low |
| v3 b10, A-SVM under faults, arm (a), ci_high | 0.1178 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (a), column ci_high |
| v3 b10, B-SVM under faults, arm (a), value | 0.1166 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (a), column value |
| v3 b10, B-SVM under faults, arm (a), ci_low | 0.1092 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (a), column ci_low |
| v3 b10, B-SVM under faults, arm (a), ci_high | 0.1247 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (a), column ci_high |
| v3 b10, A-SVM under faults, arm (b), value | 0.1238 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (b), column value |
| v3 b10, A-SVM under faults, arm (b), ci_low | 0.1147 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (b), column ci_low |
| v3 b10, A-SVM under faults, arm (b), ci_high | 0.1344 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (b), column ci_high |
| v3 b10, B-SVM under faults, arm (b), value | 0.1428 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (b), column value |
| v3 b10, B-SVM under faults, arm (b), ci_low | 0.1343 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (b), column ci_low |
| v3 b10, B-SVM under faults, arm (b), ci_high | 0.1520 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (b), column ci_high |
| v3 b10, A-SVM under faults, arm (c), value | 0.1096 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (c), column value |
| v3 b10, A-SVM under faults, arm (c), ci_low | 0.1008 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (c), column ci_low |
| v3 b10, A-SVM under faults, arm (c), ci_high | 0.1189 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=A-SVM under faults, arm (c), column ci_high |
| v3 b10, B-SVM under faults, arm (c), value | 0.1208 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (c), column value |
| v3 b10, B-SVM under faults, arm (c), ci_low | 0.1130 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (c), column ci_low |
| v3 b10, B-SVM under faults, arm (c), ci_high | 0.1296 | results/v3_prevbatch/q4_diffs_faults.csv, subset=b10, comparison=B-SVM under faults, arm (c), column ci_high |
| v3 pooled, (c)-(a) svm under faults, value | 0.0245 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) svm under faults, column value |
| v3 pooled, (c)-(a) svm under faults, ci_low | 0.0229 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) svm under faults, column ci_low |
| v3 pooled, (c)-(a) svm under faults, ci_high | 0.0262 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) svm under faults, column ci_high |
| v3 pooled, (b)-(a) svm under faults, value | 0.1284 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) svm under faults, column value |
| v3 pooled, (b)-(a) svm under faults, ci_low | 0.1261 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) svm under faults, column ci_low |
| v3 pooled, (b)-(a) svm under faults, ci_high | 0.1308 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) svm under faults, column ci_high |
| v3 pooled, (c)-(b) svm under faults, value | -0.1039 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) svm under faults, column value |
| v3 pooled, (c)-(b) svm under faults, ci_low | -0.1058 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) svm under faults, column ci_low |
| v3 pooled, (c)-(b) svm under faults, ci_high | -0.1021 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) svm under faults, column ci_high |
| v3 pooled, (c)-(a) A under faults, value | 0.0248 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) A under faults, column value |
| v3 pooled, (c)-(a) A under faults, ci_low | 0.0235 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) A under faults, column ci_low |
| v3 pooled, (c)-(a) A under faults, ci_high | 0.0260 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) A under faults, column ci_high |
| v3 pooled, (b)-(a) A under faults, value | 0.1472 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) A under faults, column value |
| v3 pooled, (b)-(a) A under faults, ci_low | 0.1447 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) A under faults, column ci_low |
| v3 pooled, (b)-(a) A under faults, ci_high | 0.1497 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) A under faults, column ci_high |
| v3 pooled, (c)-(b) A under faults, value | -0.1224 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) A under faults, column value |
| v3 pooled, (c)-(b) A under faults, ci_low | -0.1245 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) A under faults, column ci_low |
| v3 pooled, (c)-(b) A under faults, ci_high | -0.1204 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) A under faults, column ci_high |
| v3 pooled, (c)-(a) B under faults, value | 0.0292 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) B under faults, column value |
| v3 pooled, (c)-(a) B under faults, ci_low | 0.0280 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) B under faults, column ci_low |
| v3 pooled, (c)-(a) B under faults, ci_high | 0.0304 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(a) B under faults, column ci_high |
| v3 pooled, (b)-(a) B under faults, value | 0.1597 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) B under faults, column value |
| v3 pooled, (b)-(a) B under faults, ci_low | 0.1576 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) B under faults, column ci_low |
| v3 pooled, (b)-(a) B under faults, ci_high | 0.1615 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(b)-(a) B under faults, column ci_high |
| v3 pooled, (c)-(b) B under faults, value | -0.1304 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) B under faults, column value |
| v3 pooled, (c)-(b) B under faults, ci_low | -0.1318 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) B under faults, column ci_low |
| v3 pooled, (c)-(b) B under faults, ci_high | -0.1290 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=(c)-(b) B under faults, column ci_high |
| v3 pooled, A-SVM under faults, arm (a), value | 0.1071 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (a), column value |
| v3 pooled, A-SVM under faults, arm (a), ci_low | 0.0989 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (a), column ci_low |
| v3 pooled, A-SVM under faults, arm (a), ci_high | 0.1158 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (a), column ci_high |
| v3 pooled, B-SVM under faults, arm (a), value | 0.1130 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (a), column value |
| v3 pooled, B-SVM under faults, arm (a), ci_low | 0.1058 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (a), column ci_low |
| v3 pooled, B-SVM under faults, arm (a), ci_high | 0.1207 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (a), column ci_high |
| v3 pooled, A-SVM under faults, arm (b), value | 0.1259 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (b), column value |
| v3 pooled, A-SVM under faults, arm (b), ci_low | 0.1166 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (b), column ci_low |
| v3 pooled, A-SVM under faults, arm (b), ci_high | 0.1365 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (b), column ci_high |
| v3 pooled, B-SVM under faults, arm (b), value | 0.1443 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (b), column value |
| v3 pooled, B-SVM under faults, arm (b), ci_low | 0.1354 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (b), column ci_low |
| v3 pooled, B-SVM under faults, arm (b), ci_high | 0.1536 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (b), column ci_high |
| v3 pooled, A-SVM under faults, arm (c), value | 0.1074 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (c), column value |
| v3 pooled, A-SVM under faults, arm (c), ci_low | 0.0988 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (c), column ci_low |
| v3 pooled, A-SVM under faults, arm (c), ci_high | 0.1164 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=A-SVM under faults, arm (c), column ci_high |
| v3 pooled, B-SVM under faults, arm (c), value | 0.1177 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (c), column value |
| v3 pooled, B-SVM under faults, arm (c), ci_low | 0.1103 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (c), column ci_low |
| v3 pooled, B-SVM under faults, arm (c), ci_high | 0.1262 | results/v3_prevbatch/q4_diffs_faults.csv, subset=pooled, comparison=B-SVM under faults, arm (c), column ci_high |
| v3 b9, (c)-(a) svm clean, value | 0.0078 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) svm clean, column value |
| v3 b9, (c)-(a) svm clean, ci_low | 0.0021 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) svm clean, column ci_low |
| v3 b9, (c)-(a) svm clean, ci_high | 0.0134 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) svm clean, column ci_high |
| v3 b9, (b)-(a) svm clean, value | 0.2446 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) svm clean, column value |
| v3 b9, (b)-(a) svm clean, ci_low | 0.2398 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) svm clean, column ci_low |
| v3 b9, (b)-(a) svm clean, ci_high | 0.2495 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) svm clean, column ci_high |
| v3 b9, (c)-(b) svm clean, value | -0.2369 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) svm clean, column value |
| v3 b9, (c)-(b) svm clean, ci_low | -0.2402 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) svm clean, column ci_low |
| v3 b9, (c)-(b) svm clean, ci_high | -0.2335 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) svm clean, column ci_high |
| v3 b9, (a) svm clean, value | 0.7360 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) svm clean, column value |
| v3 b9, (a) svm clean, ci_low | 0.7338 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) svm clean, column ci_low |
| v3 b9, (a) svm clean, ci_high | 0.7382 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) svm clean, column ci_high |
| v3 b9, (b) svm clean, value | 0.9806 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) svm clean, column value |
| v3 b9, (b) svm clean, ci_low | 0.9758 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) svm clean, column ci_low |
| v3 b9, (b) svm clean, ci_high | 0.9854 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) svm clean, column ci_high |
| v3 b9, (c) svm clean, value | 0.7438 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) svm clean, column value |
| v3 b9, (c) svm clean, ci_low | 0.7379 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) svm clean, column ci_low |
| v3 b9, (c) svm clean, ci_high | 0.7497 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) svm clean, column ci_high |
| v3 b9, (c)-(a) A clean, value | 0.0046 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) A clean, column value |
| v3 b9, (c)-(a) A clean, ci_low | 0.0034 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) A clean, column ci_low |
| v3 b9, (c)-(a) A clean, ci_high | 0.0059 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) A clean, column ci_high |
| v3 b9, (b)-(a) A clean, value | 0.2421 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) A clean, column value |
| v3 b9, (b)-(a) A clean, ci_low | 0.2399 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) A clean, column ci_low |
| v3 b9, (b)-(a) A clean, ci_high | 0.2443 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) A clean, column ci_high |
| v3 b9, (c)-(b) A clean, value | -0.2374 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) A clean, column value |
| v3 b9, (c)-(b) A clean, ci_low | -0.2397 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) A clean, column ci_low |
| v3 b9, (c)-(b) A clean, ci_high | -0.2352 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) A clean, column ci_high |
| v3 b9, (a) A clean, value | 0.7544 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) A clean, column value |
| v3 b9, (a) A clean, ci_low | 0.7519 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) A clean, column ci_low |
| v3 b9, (a) A clean, ci_high | 0.7568 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) A clean, column ci_high |
| v3 b9, (b) A clean, value | 0.9965 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) A clean, column value |
| v3 b9, (b) A clean, ci_low | 0.9929 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) A clean, column ci_low |
| v3 b9, (b) A clean, ci_high | 1.0000 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) A clean, column ci_high |
| v3 b9, (c) A clean, value | 0.7590 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) A clean, column value |
| v3 b9, (c) A clean, ci_low | 0.7571 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) A clean, column ci_low |
| v3 b9, (c) A clean, ci_high | 0.7609 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) A clean, column ci_high |
| v3 b9, (c)-(a) B clean, value | 0.0057 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) B clean, column value |
| v3 b9, (c)-(a) B clean, ci_low | 0.0037 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) B clean, column ci_low |
| v3 b9, (c)-(a) B clean, ci_high | 0.0076 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(a) B clean, column ci_high |
| v3 b9, (b)-(a) B clean, value | 0.2421 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) B clean, column value |
| v3 b9, (b)-(a) B clean, ci_low | 0.2408 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) B clean, column ci_low |
| v3 b9, (b)-(a) B clean, ci_high | 0.2435 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b)-(a) B clean, column ci_high |
| v3 b9, (c)-(b) B clean, value | -0.2365 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) B clean, column value |
| v3 b9, (c)-(b) B clean, ci_low | -0.2372 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) B clean, column ci_low |
| v3 b9, (c)-(b) B clean, ci_high | -0.2358 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c)-(b) B clean, column ci_high |
| v3 b9, (a) B clean, value | 0.7548 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) B clean, column value |
| v3 b9, (a) B clean, ci_low | 0.7524 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) B clean, column ci_low |
| v3 b9, (a) B clean, ci_high | 0.7573 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(a) B clean, column ci_high |
| v3 b9, (b) B clean, value | 0.9970 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) B clean, column value |
| v3 b9, (b) B clean, ci_low | 0.9943 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) B clean, column ci_low |
| v3 b9, (b) B clean, ci_high | 0.9996 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(b) B clean, column ci_high |
| v3 b9, (c) B clean, value | 0.7605 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) B clean, column value |
| v3 b9, (c) B clean, ci_low | 0.7579 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) B clean, column ci_low |
| v3 b9, (c) B clean, ci_high | 0.7630 | results/v3_prevbatch/q4_clean.csv, subset=b9, comparison=(c) B clean, column ci_high |
| v3 b10, (c)-(a) svm clean, value | 0.0181 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) svm clean, column value |
| v3 b10, (c)-(a) svm clean, ci_low | 0.0110 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) svm clean, column ci_low |
| v3 b10, (c)-(a) svm clean, ci_high | 0.0251 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) svm clean, column ci_high |
| v3 b10, (b)-(a) svm clean, value | 0.1440 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) svm clean, column value |
| v3 b10, (b)-(a) svm clean, ci_low | 0.1205 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) svm clean, column ci_low |
| v3 b10, (b)-(a) svm clean, ci_high | 0.1675 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) svm clean, column ci_high |
| v3 b10, (c)-(b) svm clean, value | -0.1259 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) svm clean, column value |
| v3 b10, (c)-(b) svm clean, ci_low | -0.1528 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) svm clean, column ci_low |
| v3 b10, (c)-(b) svm clean, ci_high | -0.0990 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) svm clean, column ci_high |
| v3 b10, (a) svm clean, value | 0.6743 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) svm clean, column value |
| v3 b10, (a) svm clean, ci_low | 0.6732 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) svm clean, column ci_low |
| v3 b10, (a) svm clean, ci_high | 0.6753 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) svm clean, column ci_high |
| v3 b10, (b) svm clean, value | 0.8183 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) svm clean, column value |
| v3 b10, (b) svm clean, ci_low | 0.7945 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) svm clean, column ci_low |
| v3 b10, (b) svm clean, ci_high | 0.8421 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) svm clean, column ci_high |
| v3 b10, (c) svm clean, value | 0.6924 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) svm clean, column value |
| v3 b10, (c) svm clean, ci_low | 0.6860 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) svm clean, column ci_low |
| v3 b10, (c) svm clean, ci_high | 0.6987 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) svm clean, column ci_high |
| v3 b10, (c)-(a) A clean, value | 0.0176 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) A clean, column value |
| v3 b10, (c)-(a) A clean, ci_low | 0.0097 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) A clean, column ci_low |
| v3 b10, (c)-(a) A clean, ci_high | 0.0256 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) A clean, column ci_high |
| v3 b10, (b)-(a) A clean, value | 0.1449 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) A clean, column value |
| v3 b10, (b)-(a) A clean, ci_low | 0.1260 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) A clean, column ci_low |
| v3 b10, (b)-(a) A clean, ci_high | 0.1637 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) A clean, column ci_high |
| v3 b10, (c)-(b) A clean, value | -0.1272 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) A clean, column value |
| v3 b10, (c)-(b) A clean, ci_low | -0.1508 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) A clean, column ci_low |
| v3 b10, (c)-(b) A clean, ci_high | -0.1037 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) A clean, column ci_high |
| v3 b10, (a) A clean, value | 0.6565 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) A clean, column value |
| v3 b10, (a) A clean, ci_low | 0.6553 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) A clean, column ci_low |
| v3 b10, (a) A clean, ci_high | 0.6577 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) A clean, column ci_high |
| v3 b10, (b) A clean, value | 0.8014 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) A clean, column value |
| v3 b10, (b) A clean, ci_low | 0.7824 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) A clean, column ci_low |
| v3 b10, (b) A clean, ci_high | 0.8204 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) A clean, column ci_high |
| v3 b10, (c) A clean, value | 0.6742 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) A clean, column value |
| v3 b10, (c) A clean, ci_low | 0.6672 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) A clean, column ci_low |
| v3 b10, (c) A clean, ci_high | 0.6811 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) A clean, column ci_high |
| v3 b10, (c)-(a) B clean, value | 0.0183 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) B clean, column value |
| v3 b10, (c)-(a) B clean, ci_low | 0.0129 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) B clean, column ci_low |
| v3 b10, (c)-(a) B clean, ci_high | 0.0236 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(a) B clean, column ci_high |
| v3 b10, (b)-(a) B clean, value | 0.1486 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) B clean, column value |
| v3 b10, (b)-(a) B clean, ci_low | 0.1274 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) B clean, column ci_low |
| v3 b10, (b)-(a) B clean, ci_high | 0.1697 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b)-(a) B clean, column ci_high |
| v3 b10, (c)-(b) B clean, value | -0.1303 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) B clean, column value |
| v3 b10, (c)-(b) B clean, ci_low | -0.1542 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) B clean, column ci_low |
| v3 b10, (c)-(b) B clean, ci_high | -0.1064 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c)-(b) B clean, column ci_high |
| v3 b10, (a) B clean, value | 0.6657 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) B clean, column value |
| v3 b10, (a) B clean, ci_low | 0.6648 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) B clean, column ci_low |
| v3 b10, (a) B clean, ci_high | 0.6666 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(a) B clean, column ci_high |
| v3 b10, (b) B clean, value | 0.8143 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) B clean, column value |
| v3 b10, (b) B clean, ci_low | 0.7927 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) B clean, column ci_low |
| v3 b10, (b) B clean, ci_high | 0.8359 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(b) B clean, column ci_high |
| v3 b10, (c) B clean, value | 0.6840 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) B clean, column value |
| v3 b10, (c) B clean, ci_low | 0.6794 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) B clean, column ci_low |
| v3 b10, (c) B clean, ci_high | 0.6886 | results/v3_prevbatch/q4_clean.csv, subset=b10, comparison=(c) B clean, column ci_high |
| v3 pooled, (c)-(a) svm clean, value | 0.0177 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) svm clean, column value |
| v3 pooled, (c)-(a) svm clean, ci_low | 0.0109 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) svm clean, column ci_low |
| v3 pooled, (c)-(a) svm clean, ci_high | 0.0245 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) svm clean, column ci_high |
| v3 pooled, (b)-(a) svm clean, value | 0.1479 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) svm clean, column value |
| v3 pooled, (b)-(a) svm clean, ci_low | 0.1271 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) svm clean, column ci_low |
| v3 pooled, (b)-(a) svm clean, ci_high | 0.1688 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) svm clean, column ci_high |
| v3 pooled, (c)-(b) svm clean, value | -0.1302 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) svm clean, column value |
| v3 pooled, (c)-(b) svm clean, ci_low | -0.1542 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) svm clean, column ci_low |
| v3 pooled, (c)-(b) svm clean, ci_high | -0.1062 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) svm clean, column ci_high |
| v3 pooled, (a) svm clean, value | 0.6864 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) svm clean, column value |
| v3 pooled, (a) svm clean, ci_low | 0.6853 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) svm clean, column ci_low |
| v3 pooled, (a) svm clean, ci_high | 0.6874 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) svm clean, column ci_high |
| v3 pooled, (b) svm clean, value | 0.8343 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) svm clean, column value |
| v3 pooled, (b) svm clean, ci_low | 0.8133 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) svm clean, column ci_low |
| v3 pooled, (b) svm clean, ci_high | 0.8553 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) svm clean, column ci_high |
| v3 pooled, (c) svm clean, value | 0.7041 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) svm clean, column value |
| v3 pooled, (c) svm clean, ci_low | 0.6978 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) svm clean, column ci_low |
| v3 pooled, (c) svm clean, ci_high | 0.7103 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) svm clean, column ci_high |
| v3 pooled, (c)-(a) A clean, value | 0.0173 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) A clean, column value |
| v3 pooled, (c)-(a) A clean, ci_low | 0.0103 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) A clean, column ci_low |
| v3 pooled, (c)-(a) A clean, ci_high | 0.0242 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) A clean, column ci_high |
| v3 pooled, (b)-(a) A clean, value | 0.1483 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) A clean, column value |
| v3 pooled, (b)-(a) A clean, ci_low | 0.1313 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) A clean, column ci_low |
| v3 pooled, (b)-(a) A clean, ci_high | 0.1653 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) A clean, column ci_high |
| v3 pooled, (c)-(b) A clean, value | -0.1310 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) A clean, column value |
| v3 pooled, (c)-(b) A clean, ci_low | -0.1520 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) A clean, column ci_low |
| v3 pooled, (c)-(b) A clean, ci_high | -0.1100 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) A clean, column ci_high |
| v3 pooled, (a) A clean, value | 0.6725 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) A clean, column value |
| v3 pooled, (a) A clean, ci_low | 0.6715 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) A clean, column ci_low |
| v3 pooled, (a) A clean, ci_high | 0.6735 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) A clean, column ci_high |
| v3 pooled, (b) A clean, value | 0.8208 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) A clean, column value |
| v3 pooled, (b) A clean, ci_low | 0.8037 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) A clean, column ci_low |
| v3 pooled, (b) A clean, ci_high | 0.8379 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) A clean, column ci_high |
| v3 pooled, (c) A clean, value | 0.6898 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) A clean, column value |
| v3 pooled, (c) A clean, ci_low | 0.6836 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) A clean, column ci_low |
| v3 pooled, (c) A clean, ci_high | 0.6959 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) A clean, column ci_high |
| v3 pooled, (c)-(a) B clean, value | 0.0177 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) B clean, column value |
| v3 pooled, (c)-(a) B clean, ci_low | 0.0131 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) B clean, column ci_low |
| v3 pooled, (c)-(a) B clean, ci_high | 0.0223 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(a) B clean, column ci_high |
| v3 pooled, (b)-(a) B clean, value | 0.1518 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) B clean, column value |
| v3 pooled, (b)-(a) B clean, ci_low | 0.1329 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) B clean, column ci_low |
| v3 pooled, (b)-(a) B clean, ci_high | 0.1707 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b)-(a) B clean, column ci_high |
| v3 pooled, (c)-(b) B clean, value | -0.1341 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) B clean, column value |
| v3 pooled, (c)-(b) B clean, ci_low | -0.1554 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) B clean, column ci_low |
| v3 pooled, (c)-(b) B clean, ci_high | -0.1129 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c)-(b) B clean, column ci_high |
| v3 pooled, (a) B clean, value | 0.6807 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) B clean, column value |
| v3 pooled, (a) B clean, ci_low | 0.6800 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) B clean, column ci_low |
| v3 pooled, (a) B clean, ci_high | 0.6815 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(a) B clean, column ci_high |
| v3 pooled, (b) B clean, value | 0.8325 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) B clean, column value |
| v3 pooled, (b) B clean, ci_low | 0.8133 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) B clean, column ci_low |
| v3 pooled, (b) B clean, ci_high | 0.8518 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(b) B clean, column ci_high |
| v3 pooled, (c) B clean, value | 0.6984 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) B clean, column value |
| v3 pooled, (c) B clean, ci_low | 0.6945 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) B clean, column ci_low |
| v3 pooled, (c) B clean, ci_high | 0.7023 | results/v3_prevbatch/q4_clean.csv, subset=pooled, comparison=(c) B clean, column ci_high |
| v3 under faults svm, b9, c_minus_a | 0.0246 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=svm, column c_minus_a |
| v3 under faults svm, b9, b_minus_a | 0.1618 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=svm, column b_minus_a |
| v3 under faults svm, b9, share_of_same_period_gain_kept | 0.1518 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=svm, column share_of_same_period_gain_kept |
| v3 under faults A, b9, c_minus_a | 0.0238 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=A, column c_minus_a |
| v3 under faults A, b9, b_minus_a | 0.2345 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=A, column b_minus_a |
| v3 under faults A, b9, share_of_same_period_gain_kept | 0.1013 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=A, column share_of_same_period_gain_kept |
| v3 under faults B, b9, c_minus_a | 0.0330 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=B, column c_minus_a |
| v3 under faults B, b9, b_minus_a | 0.2506 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=B, column b_minus_a |
| v3 under faults B, b9, share_of_same_period_gain_kept | 0.1319 | results/v3_prevbatch/q4_share_kept.csv, subset=b9, method=B, column share_of_same_period_gain_kept |
| v3 under faults svm, b10, c_minus_a | 0.0238 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=svm, column c_minus_a |
| v3 under faults svm, b10, b_minus_a | 0.1294 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=svm, column b_minus_a |
| v3 under faults svm, b10, share_of_same_period_gain_kept | 0.1837 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=svm, column share_of_same_period_gain_kept |
| v3 under faults A, b10, c_minus_a | 0.0244 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=A, column c_minus_a |
| v3 under faults A, b10, b_minus_a | 0.1441 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=A, column b_minus_a |
| v3 under faults A, b10, share_of_same_period_gain_kept | 0.1690 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=A, column share_of_same_period_gain_kept |
| v3 under faults B, b10, c_minus_a | 0.0279 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=B, column c_minus_a |
| v3 under faults B, b10, b_minus_a | 0.1555 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=B, column b_minus_a |
| v3 under faults B, b10, share_of_same_period_gain_kept | 0.1795 | results/v3_prevbatch/q4_share_kept.csv, subset=b10, method=B, column share_of_same_period_gain_kept |
| v3 under faults svm, pooled, c_minus_a | 0.0245 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=svm, column c_minus_a |
| v3 under faults svm, pooled, b_minus_a | 0.1284 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=svm, column b_minus_a |
| v3 under faults svm, pooled, share_of_same_period_gain_kept | 0.1911 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=svm, column share_of_same_period_gain_kept |
| v3 under faults A, pooled, c_minus_a | 0.0248 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=A, column c_minus_a |
| v3 under faults A, pooled, b_minus_a | 0.1472 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=A, column b_minus_a |
| v3 under faults A, pooled, share_of_same_period_gain_kept | 0.1685 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=A, column share_of_same_period_gain_kept |
| v3 under faults B, pooled, c_minus_a | 0.0292 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=B, column c_minus_a |
| v3 under faults B, pooled, b_minus_a | 0.1597 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=B, column b_minus_a |
| v3 under faults B, pooled, share_of_same_period_gain_kept | 0.1830 | results/v3_prevbatch/q4_share_kept.csv, subset=pooled, method=B, column share_of_same_period_gain_kept |
| v3 retention, svm, arm (a), b9 | 0.8282 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=a, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (a), b9 | 0.8461 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=a, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (a), b9 | 0.1168 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=a, column worst |
| v3 retention, svm, arm (b), b9 | 0.7866 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=b, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (b), b9 | 0.8086 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=b, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (b), b9 | 0.0622 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=b, column worst |
| v3 retention, svm, arm (c), b9 | 0.8526 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=c, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (c), b9 | 0.8709 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=c, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (c), b9 | 0.1304 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=svm, arm=c, column worst |
| v3 retention, A, arm (a), b9 | 0.9358 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=a, column retention |
| v3 retention_unweighted_v2_tables, A, arm (a), b9 | 0.9498 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=a, column retention_unweighted_v2_tables |
| v3 worst, A, arm (a), b9 | 0.0372 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=a, column worst |
| v3 retention, A, arm (b), b9 | 0.9438 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=b, column retention |
| v3 retention_unweighted_v2_tables, A, arm (b), b9 | 0.9588 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=b, column retention_unweighted_v2_tables |
| v3 worst, A, arm (b), b9 | 0.0564 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=b, column worst |
| v3 retention, A, arm (c), b9 | 0.9613 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=c, column retention |
| v3 retention_unweighted_v2_tables, A, arm (c), b9 | 0.9749 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=c, column retention_unweighted_v2_tables |
| v3 worst, A, arm (c), b9 | 0.0476 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=A, arm=c, column worst |
| v3 retention, B, arm (a), b9 | 0.9328 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=a, column retention |
| v3 retention_unweighted_v2_tables, B, arm (a), b9 | 0.9416 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=a, column retention_unweighted_v2_tables |
| v3 worst, B, arm (a), b9 | 0.3430 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=a, column worst |
| v3 retention, B, arm (b), b9 | 0.9576 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=b, column retention |
| v3 retention_unweighted_v2_tables, B, arm (b), b9 | 0.9680 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=b, column retention_unweighted_v2_tables |
| v3 worst, B, arm (b), b9 | 0.2466 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=b, column worst |
| v3 retention, B, arm (c), b9 | 0.9693 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=c, column retention |
| v3 retention_unweighted_v2_tables, B, arm (c), b9 | 0.9778 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=c, column retention_unweighted_v2_tables |
| v3 worst, B, arm (c), b9 | 0.3293 | results/v3_prevbatch/q4_retention_worst.csv, subset=b9, method=B, arm=c, column worst |
| v3 retention, svm, arm (a), b10 | 0.7595 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=a, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (a), b10 | 0.7786 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=a, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (a), b10 | 0.0297 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=a, column worst |
| v3 retention, svm, arm (b), b10 | 0.7840 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=b, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (b), b10 | 0.8034 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=b, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (b), b10 | 0.0440 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=b, column worst |
| v3 retention, svm, arm (c), b10 | 0.7740 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=c, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (c), b10 | 0.7927 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=c, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (c), b10 | 0.0289 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=svm, arm=c, column worst |
| v3 retention, A, arm (a), b10 | 0.9461 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=a, column retention |
| v3 retention_unweighted_v2_tables, A, arm (a), b10 | 0.9640 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=a, column retention_unweighted_v2_tables |
| v3 worst, A, arm (a), b10 | 0.0596 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=a, column worst |
| v3 retention, A, arm (b), b10 | 0.9550 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=b, column retention |
| v3 retention_unweighted_v2_tables, A, arm (b), b10 | 0.9682 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=b, column retention_unweighted_v2_tables |
| v3 worst, A, arm (b), b10 | 0.0721 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=b, column worst |
| v3 retention, A, arm (c), b10 | 0.9575 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=c, column retention |
| v3 retention_unweighted_v2_tables, A, arm (c), b10 | 0.9739 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=c, column retention_unweighted_v2_tables |
| v3 worst, A, arm (c), b10 | 0.0678 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=A, arm=c, column worst |
| v3 retention, B, arm (a), b10 | 0.9445 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=a, column retention |
| v3 retention_unweighted_v2_tables, B, arm (a), b10 | 0.9587 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=a, column retention_unweighted_v2_tables |
| v3 worst, B, arm (a), b10 | 0.1458 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=a, column worst |
| v3 retention, B, arm (b), b10 | 0.9632 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=b, column retention |
| v3 retention_unweighted_v2_tables, B, arm (b), b10 | 0.9737 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=b, column retention_unweighted_v2_tables |
| v3 worst, B, arm (b), b10 | 0.1743 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=b, column worst |
| v3 retention, B, arm (c), b10 | 0.9601 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=c, column retention |
| v3 retention_unweighted_v2_tables, B, arm (c), b10 | 0.9719 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=c, column retention_unweighted_v2_tables |
| v3 worst, B, arm (c), b10 | 0.1483 | results/v3_prevbatch/q4_retention_worst.csv, subset=b10, method=B, arm=c, column worst |
| v3 retention, svm, arm (a), pooled | 0.7712 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=a, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (a), pooled | 0.7898 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=a, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (a), pooled | 0.1268 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=a, column worst |
| v3 retention, svm, arm (b), pooled | 0.7885 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=b, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (b), pooled | 0.8078 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=b, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (b), pooled | 0.1607 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=b, column worst |
| v3 retention, svm, arm (c), pooled | 0.7867 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=c, column retention |
| v3 retention_unweighted_v2_tables, svm, arm (c), pooled | 0.8050 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=c, column retention_unweighted_v2_tables |
| v3 worst, svm, arm (c), pooled | 0.1263 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=svm, arm=c, column worst |
| v3 retention, A, arm (a), pooled | 0.9463 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=a, column retention |
| v3 retention_unweighted_v2_tables, A, arm (a), pooled | 0.9634 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=a, column retention_unweighted_v2_tables |
| v3 worst, A, arm (a), pooled | 0.1178 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=a, column worst |
| v3 retention, A, arm (b), pooled | 0.9548 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=b, column retention |
| v3 retention_unweighted_v2_tables, A, arm (b), pooled | 0.9678 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=b, column retention_unweighted_v2_tables |
| v3 worst, A, arm (b), pooled | 0.1373 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=b, column worst |
| v3 retention, A, arm (c), pooled | 0.9586 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=c, column retention |
| v3 retention_unweighted_v2_tables, A, arm (c), pooled | 0.9743 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=c, column retention_unweighted_v2_tables |
| v3 worst, A, arm (c), pooled | 0.1021 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=A, arm=c, column worst |
| v3 retention, B, arm (a), pooled | 0.9436 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=a, column retention |
| v3 retention_unweighted_v2_tables, B, arm (a), pooled | 0.9570 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=a, column retention_unweighted_v2_tables |
| v3 worst, B, arm (a), pooled | 0.2322 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=a, column worst |
| v3 retention, B, arm (b), pooled | 0.9634 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=b, column retention |
| v3 retention_unweighted_v2_tables, B, arm (b), pooled | 0.9736 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=b, column retention_unweighted_v2_tables |
| v3 worst, B, arm (b), pooled | 0.3027 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=b, column worst |
| v3 retention, B, arm (c), pooled | 0.9616 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=c, column retention |
| v3 retention_unweighted_v2_tables, B, arm (c), pooled | 0.9728 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=c, column retention_unweighted_v2_tables |
| v3 worst, B, arm (c), pooled | 0.2364 | results/v3_prevbatch/q4_retention_worst.csv, subset=pooled, method=B, arm=c, column worst |
