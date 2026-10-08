# Final test report (batches 8-10), facts only
Frozen commit/manifest: `FREEZE_MANIFEST.md`, tag `frozen-before-test`. Every number below is read from files in `results\final_test\test` (Test) or `results\overnight\temporal` (Validation). Interpretation is not part of this file.

## 1. Gates
| subset          | clean best baseline   |   clean Macro-F1 | G1 types >= 0.03   | G1    |   G2 median AUROC | G2   | G3 cells   | G3   |
|:----------------|:----------------------|-----------------:|:-------------------|:------|------------------:|:-----|:-----------|:-----|
| Validation (b7) | svm                   |            0.859 | 4 of 4             | True  |             0.977 | True | 80 of 108  | True |
| Test pooled     | svm                   |            0.535 | 2 of 4             | True  |             0.979 | True | 61 of 108  | True |
| Test b8         | svm                   |            0.798 | 4 of 4             | True  |             0.966 | True | 52 of 108  | True |
| Test b9         | svm                   |            0.655 | 4 of 4             | True  |             0.988 | True | 29 of 108  | True |
| Test b10        | lgbm                  |            0.489 | 0 of 4             | False |             0.979 | True | 70 of 108  | True |

G1 drop of the best clean baseline per fault type (k=1, medium severity):
| subset      |   dropout |   bias |   stuck |   random |
|:------------|----------:|-------:|--------:|---------:|
| Validation  |     0.034 |  0.047 |   0.033 |    0.106 |
| Test pooled |     0.028 |  0.019 |   0.035 |    0.070 |
| Test b8     |     0.074 |  0.077 |   0.073 |    0.170 |
| Test b9     |     0.035 |  0.036 |   0.041 |    0.090 |
| Test b10    |     0.019 |  0.022 |   0.015 |    0.023 |

G3 passes if a single comparison passes (lenient); intervals resample rows only (optimistic).

## 2. Clean (no injected fault) Macro-F1: do false alarms hurt?
| method       |   Validation |   Test pooled |   Test b8 |   Test b9 |   Test b10 |
|:-------------|-------------:|--------------:|----------:|----------:|-----------:|
| svm          |        0.859 |         0.535 |     0.798 |     0.655 |      0.480 |
| lgbm         |        0.692 |         0.514 |     0.587 |     0.558 |      0.489 |
| A_det_twin   |        0.850 |         0.544 |     0.758 |     0.637 |      0.493 |
| A_det_notwin |        0.850 |         0.540 |     0.764 |     0.637 |      0.489 |
| B_det        |        0.811 |         0.540 |     0.761 |     0.637 |      0.496 |
| C_det        |        0.646 |         0.405 |     0.478 |     0.320 |      0.407 |
| C_equal      |        0.652 |         0.410 |     0.451 |     0.321 |      0.412 |

Difference to the plain SVM on clean rows (negative = acting on false alarms costs accuracy):
| difference        |   Validation |   Test pooled |   Test b8 |   Test b9 |   Test b10 |
|:------------------|-------------:|--------------:|----------:|----------:|-----------:|
| A (twin) - SVM    |       -0.009 |         0.008 |    -0.040 |    -0.018 |      0.013 |
| A (no twin) - SVM |       -0.009 |         0.005 |    -0.034 |    -0.018 |      0.009 |
| B - SVM           |       -0.048 |         0.004 |    -0.037 |    -0.018 |      0.016 |

Share of clean rows on which at least one sensor is flagged, and mean flagged sensors per row (detector acting on clean data):
| subset     |     rows |   mean_flagged_per_row |   rows_with_any_flag |
|:-----------|---------:|-----------------------:|---------------------:|
| Validation |  nan     |                  2.140 |                0.971 |
| pooled     | 4364.000 |                  1.248 |                0.742 |
| b8         |  294.000 |                  2.418 |                1.000 |
| b9         |  470.000 |                  1.068 |                0.606 |
| b10        | 3600.000 |                  1.176 |                0.739 |

Clean accuracy (Test):
| method     |   b10 |    b8 |    b9 |   pooled |
|:-----------|------:|------:|------:|---------:|
| A_det_twin | 0.521 | 0.864 | 0.681 |    0.561 |
| B_det      | 0.521 | 0.837 | 0.681 |    0.559 |
| svm        | 0.506 | 0.850 | 0.689 |    0.549 |

## 3. Detector on clean data
Primary detector: `median` (alarm threshold = Train out-of-fold 95th percentile, so about 5% is expected without drift).
False-alarm rate per sensor-row, per batch:
| sensors         |   Validation |   Test pooled |   Test b8 |   Test b9 |   Test b10 |
|:----------------|-------------:|--------------:|----------:|----------:|-----------:|
| all sensors     |        0.135 |         0.078 |     0.152 |     0.067 |      0.074 |
| without S01,S02 |        0.032 |         0.045 |     0.032 |     0.051 |      0.046 |

Per gas, all sensors:
| gas          |   pooled |    b8 |    b9 |   b10 |
|:-------------|---------:|------:|------:|------:|
| Acetaldehyde |    0.089 | 0.151 | 0.123 | 0.081 |
| Acetone      |    0.113 | 0.147 | 0.103 | 0.107 |
| Ammonia      |    0.083 | 0.164 | 0.007 | 0.090 |
| Ethanol      |    0.035 | 0.148 | 0.081 | 0.025 |
| Ethylene     |    0.067 | 0.133 | 0.039 | 0.067 |
| Toluene      |    0.075 | 0.201 | 0.064 | 0.073 |
| all          |    0.078 | 0.152 | 0.067 | 0.074 |

Per gas, without S01 and S02:
| gas          |   pooled |    b8 |    b9 |   b10 |
|:-------------|---------:|------:|------:|------:|
| Acetaldehyde |    0.045 | 0.030 | 0.056 | 0.045 |
| Acetone      |    0.057 | 0.025 | 0.059 | 0.064 |
| Ammonia      |    0.051 | 0.045 | 0.007 | 0.058 |
| Ethanol      |    0.028 | 0.026 | 0.090 | 0.021 |
| Ethylene     |    0.029 | 0.019 | 0.043 | 0.028 |
| Toluene      |    0.061 | 0.087 | 0.062 | 0.060 |
| all          |    0.045 | 0.032 | 0.051 | 0.046 |

Sensors from least to most reliable on clean rows:
|   rank_from_least_reliable | pooled   | b8   | b9   | b10   |
|---------------------------:|:---------|:-----|:-----|:------|
|                          1 | S01      | S01  | S08  | S01   |
|                          2 | S08      | S02  | S16  | S08   |
|                          3 | S07      | S12  | S01  | S07   |
|                          4 | S09      | S09  | S05  | S14   |
|                          5 | S14      | S03  | S02  | S09   |
|                          6 | S16      | S04  | S15  | S12   |
|                          7 | S12      | S08  | S07  | S16   |
|                          8 | S04      | S07  | S03  | S04   |
|                          9 | S15      | S06  | S04  | S15   |
|                         10 | S06      | S16  | S06  | S06   |
|                         11 | S05      | S15  | S12  | S13   |
|                         12 | S03      | S13  | S09  | S05   |
|                         13 | S13      | S05  | S13  | S03   |
|                         14 | S02      | S10  | S14  | S02   |
|                         15 | S11      | S14  | S11  | S11   |
|                         16 | S10      | S11  | S10  | S10   |

Detector alarm rate of S01 and S02 per batch (batches 1-6 out-of-fold, 7-10 evaluation):
|   batch |   S01 |   S02 |
|--------:|------:|------:|
|   1.000 | 0.011 | 0.000 |
|   2.000 | 0.083 | 0.016 |
|   3.000 | 0.003 | 0.127 |
|   4.000 | 0.000 | 0.074 |
|   5.000 | 0.000 | 0.000 |
|   6.000 | 0.080 | 0.027 |
|   8.000 | 1.000 | 0.983 |
|   9.000 | 0.126 | 0.240 |
|  10.000 | 0.511 | 0.026 |

Isolation AUROC per fault type (k=1, medium severity), per batch:
| fault   |   pooled |    b8 |    b9 |   b10 |
|:--------|---------:|------:|------:|------:|
| bias    |    0.978 | 0.973 | 0.991 | 0.977 |
| dropout |    1.000 | 1.000 | 1.000 | 1.000 |
| random  |    0.979 | 0.958 | 0.986 | 0.981 |
| stuck   |    0.948 | 0.906 | 0.963 | 0.950 |

Hit rate (share of faulty blocks flagged) and false-alarm rate on the healthy blocks of the same rows (k=1, medium):
| fault   |   pooled |    b8 |    b9 |   b10 |
|:--------|---------:|------:|------:|------:|
| bias    |    0.964 | 0.985 | 0.994 | 0.959 |
| dropout |    1.000 | 1.000 | 1.000 | 1.000 |
| random  |    0.989 | 0.997 | 0.998 | 0.988 |
| stuck   |    0.910 | 0.922 | 0.945 | 0.905 |

| fault   |   pooled |    b8 |    b9 |   b10 |
|:--------|---------:|------:|------:|------:|
| bias    |    0.137 | 0.183 | 0.151 | 0.132 |
| dropout |    0.124 | 0.212 | 0.136 | 0.115 |
| random  |    0.139 | 0.211 | 0.152 | 0.132 |
| stuck   |    0.129 | 0.203 | 0.126 | 0.123 |

## 4. Did A and B stay above the best augmented baseline?
Per fault type and k, over every severity (levels) and the sensor sets: number of cells with a positive difference to the best augmented baseline and, in brackets, with an interval that excludes 0. Methods use the real detector.

A_det_twin:
| fault   |   k | Validation   | pooled   | b8      | b9      | b10     |
|:--------|----:|:-------------|:---------|:--------|:--------|:--------|
| bias    |   1 | 3/3 (3)      | 3/3 (3)  | 3/3 (2) | 1/3 (1) | 3/3 (3) |
| bias    |   2 | 3/3 (3)      | 1/3 (0)  | 1/3 (1) | 1/3 (0) | 1/3 (1) |
| bias    |   4 | 1/3 (1)      | 0/3 (0)  | 0/3 (0) | 0/3 (0) | 0/3 (0) |
| dropout |   1 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 1/2 (1) | 2/2 (2) |
| dropout |   2 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 1/2 (1) | 2/2 (2) |
| dropout |   4 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 2/2 (2) | 2/2 (2) |
| random  |   1 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 1/2 (1) | 2/2 (2) |
| random  |   2 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 2/2 (2) | 2/2 (2) |
| random  |   4 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 2/2 (2) | 2/2 (2) |
| stuck   |   1 | 2/2 (2)      | 2/2 (2)  | 2/2 (1) | 0/2 (0) | 2/2 (2) |
| stuck   |   2 | 2/2 (2)      | 2/2 (2)  | 1/2 (0) | 0/2 (0) | 2/2 (2) |
| stuck   |   4 | 1/2 (1)      | 0/2 (0)  | 0/2 (0) | 0/2 (0) | 1/2 (1) |

B_det:
| fault   |   k | Validation   | pooled   | b8      | b9      | b10     |
|:--------|----:|:-------------|:---------|:--------|:--------|:--------|
| bias    |   1 | 3/3 (3)      | 3/3 (2)  | 3/3 (2) | 1/3 (1) | 3/3 (3) |
| bias    |   2 | 3/3 (3)      | 3/3 (1)  | 2/3 (1) | 0/3 (0) | 3/3 (3) |
| bias    |   4 | 2/3 (2)      | 0/3 (0)  | 0/3 (0) | 0/3 (0) | 1/3 (0) |
| dropout |   1 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 0/2 (0) | 2/2 (2) |
| dropout |   2 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 1/2 (1) | 2/2 (2) |
| dropout |   4 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 1/2 (1) | 2/2 (2) |
| random  |   1 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 1/2 (1) | 2/2 (2) |
| random  |   2 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 2/2 (2) | 2/2 (2) |
| random  |   4 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 2/2 (2) | 2/2 (2) |
| stuck   |   1 | 2/2 (2)      | 2/2 (2)  | 2/2 (2) | 0/2 (0) | 2/2 (2) |
| stuck   |   2 | 2/2 (2)      | 2/2 (2)  | 2/2 (0) | 0/2 (0) | 2/2 (2) |
| stuck   |   4 | 2/2 (1)      | 0/2 (0)  | 0/2 (0) | 0/2 (0) | 1/2 (1) |

Totals:
| method     | subset     |   cells |   diff > 0 |   CI excludes 0 |   mean diff |   min diff |   max diff |
|:-----------|:-----------|--------:|-----------:|----------------:|------------:|-----------:|-----------:|
| A_det_twin | Validation |      27 |         24 |              24 |       0.073 |     -0.277 |      0.195 |
| A_det_twin | pooled     |      27 |         20 |              19 |       0.031 |     -0.170 |      0.151 |
| A_det_twin | b8         |      27 |         19 |              16 |       0.073 |     -0.124 |      0.296 |
| A_det_twin | b9         |      27 |         11 |              10 |      -0.021 |     -0.234 |      0.173 |
| A_det_twin | b10        |      27 |         21 |              21 |       0.029 |     -0.167 |      0.125 |
| B_det      | Validation |      27 |         26 |              25 |       0.076 |     -0.140 |      0.207 |
| B_det      | pooled     |      27 |         22 |              19 |       0.031 |     -0.142 |      0.137 |
| B_det      | b8         |      27 |         21 |              17 |       0.091 |     -0.100 |      0.328 |
| B_det      | b9         |      27 |          8 |               8 |      -0.036 |     -0.189 |      0.110 |
| B_det      | b10        |      27 |         24 |              23 |       0.033 |     -0.142 |      0.113 |

Cells where the sign of the difference to the best augmented baseline differs between Validation and Test (pooled):
| method     | kset   | fault   |   level |   Validation diff |   Test pooled diff |
|:-----------|:-------|:--------|--------:|------------------:|-------------------:|
| A_det_twin | k2     | bias    |   1.000 |             0.048 |             -0.005 |
| A_det_twin | k2     | bias    |   3.000 |             0.028 |             -0.002 |
| A_det_twin | k4     | bias    |   0.500 |             0.009 |             -0.015 |
| A_det_twin | k4     | stuck   |   0.500 |             0.041 |             -0.000 |
| B_det      | k4     | bias    |   0.500 |             0.023 |             -0.015 |
| B_det      | k4     | bias    |   1.000 |             0.028 |             -0.037 |
| B_det      | k4     | stuck   |   0.500 |             0.016 |             -0.003 |
| B_det      | k4     | stuck   |   1.000 |             0.001 |             -0.018 |

## 5. Main comparison per batch (medium severity, Macro-F1)
| subset   | fault   |   k |   SVM |   best aug |     A |     B |     C |   Oracle A |   Oracle B |
|:---------|:--------|----:|------:|-----------:|------:|------:|------:|-----------:|-----------:|
| pooled   | dropout |   1 | 0.507 |      0.517 | 0.543 | 0.537 | 0.406 |      0.534 |      0.536 |
| pooled   | dropout |   2 | 0.480 |      0.500 | 0.541 | 0.535 | 0.405 |      0.536 |      0.534 |
| pooled   | dropout |   4 | 0.443 |      0.464 | 0.537 | 0.531 | 0.406 |      0.533 |      0.528 |
| pooled   | bias    |   1 | 0.516 |      0.523 | 0.536 | 0.531 | 0.407 |      0.532 |      0.535 |
| pooled   | bias    |   2 | 0.464 |      0.510 | 0.505 | 0.514 | 0.410 |      0.536 |      0.531 |
| pooled   | bias    |   4 | 0.393 |      0.465 | 0.396 | 0.428 | 0.397 |      0.528 |      0.514 |
| pooled   | stuck   |   1 | 0.501 |      0.510 | 0.542 | 0.539 | 0.406 |      0.534 |      0.535 |
| pooled   | stuck   |   2 | 0.487 |      0.495 | 0.511 | 0.511 | 0.403 |      0.536 |      0.534 |
| pooled   | stuck   |   4 | 0.443 |      0.454 | 0.453 | 0.451 | 0.397 |      0.533 |      0.526 |
| pooled   | random  |   1 | 0.465 |      0.489 | 0.543 | 0.538 | 0.405 |      0.534 |      0.535 |
| pooled   | random  |   2 | 0.418 |      0.446 | 0.533 | 0.528 | 0.406 |      0.536 |      0.534 |
| pooled   | random  |   4 | 0.381 |      0.400 | 0.471 | 0.475 | 0.403 |      0.532 |      0.527 |
| b8       | dropout |   1 | 0.724 |      0.732 | 0.778 | 0.777 | 0.467 |      0.784 |      0.783 |
| b8       | dropout |   2 | 0.649 |      0.678 | 0.778 | 0.779 | 0.467 |      0.785 |      0.773 |
| b8       | dropout |   4 | 0.545 |      0.583 | 0.734 | 0.755 | 0.474 |      0.760 |      0.765 |
| b8       | bias    |   1 | 0.721 |      0.750 | 0.782 | 0.802 | 0.486 |      0.768 |      0.766 |
| b8       | bias    |   2 | 0.592 |      0.730 | 0.709 | 0.734 | 0.486 |      0.776 |      0.745 |
| b8       | bias    |   4 | 0.470 |      0.628 | 0.504 | 0.528 | 0.449 |      0.712 |      0.733 |
| b8       | stuck   |   1 | 0.724 |      0.721 | 0.760 | 0.783 | 0.468 |      0.784 |      0.781 |
| b8       | stuck   |   2 | 0.706 |      0.698 | 0.712 | 0.715 | 0.471 |      0.790 |      0.774 |
| b8       | stuck   |   4 | 0.633 |      0.633 | 0.620 | 0.629 | 0.472 |      0.759 |      0.764 |
| b8       | random  |   1 | 0.628 |      0.645 | 0.777 | 0.802 | 0.472 |      0.785 |      0.784 |
| b8       | random  |   2 | 0.535 |      0.555 | 0.753 | 0.785 | 0.482 |      0.789 |      0.772 |
| b8       | random  |   4 | 0.502 |      0.489 | 0.602 | 0.624 | 0.497 |      0.758 |      0.765 |
| b9       | dropout |   1 | 0.620 |      0.706 | 0.644 | 0.635 | 0.324 |      0.652 |      0.655 |
| b9       | dropout |   2 | 0.583 |      0.668 | 0.640 | 0.621 | 0.325 |      0.648 |      0.639 |
| b9       | dropout |   4 | 0.531 |      0.617 | 0.631 | 0.599 | 0.328 |      0.638 |      0.608 |
| b9       | bias    |   1 | 0.620 |      0.730 | 0.641 | 0.614 | 0.316 |      0.647 |      0.651 |
| b9       | bias    |   2 | 0.559 |      0.685 | 0.622 | 0.612 | 0.334 |      0.639 |      0.621 |
| b9       | bias    |   4 | 0.433 |      0.640 | 0.487 | 0.533 | 0.363 |      0.629 |      0.553 |
| b9       | stuck   |   1 | 0.614 |      0.729 | 0.640 | 0.633 | 0.324 |      0.651 |      0.654 |
| b9       | stuck   |   2 | 0.591 |      0.703 | 0.604 | 0.600 | 0.322 |      0.648 |      0.640 |
| b9       | stuck   |   4 | 0.554 |      0.657 | 0.556 | 0.560 | 0.339 |      0.638 |      0.607 |
| b9       | random  |   1 | 0.565 |      0.659 | 0.642 | 0.628 | 0.320 |      0.651 |      0.652 |
| b9       | random  |   2 | 0.491 |      0.582 | 0.630 | 0.613 | 0.317 |      0.648 |      0.640 |
| b9       | random  |   4 | 0.447 |      0.508 | 0.557 | 0.548 | 0.318 |      0.638 |      0.608 |
| b10      | dropout |   1 | 0.459 |      0.461 | 0.492 | 0.492 | 0.407 |      0.480 |      0.482 |
| b10      | dropout |   2 | 0.440 |      0.450 | 0.490 | 0.491 | 0.406 |      0.484 |      0.484 |
| b10      | dropout |   4 | 0.412 |      0.424 | 0.491 | 0.490 | 0.407 |      0.484 |      0.481 |
| b10      | bias    |   1 | 0.469 |      0.466 | 0.487 | 0.485 | 0.407 |      0.480 |      0.483 |
| b10      | bias    |   2 | 0.426 |      0.457 | 0.457 | 0.466 | 0.409 |      0.486 |      0.487 |
| b10      | bias    |   4 | 0.369 |      0.419 | 0.366 | 0.398 | 0.392 |      0.483 |      0.470 |
| b10      | stuck   |   1 | 0.451 |      0.452 | 0.492 | 0.494 | 0.408 |      0.480 |      0.482 |
| b10      | stuck   |   2 | 0.439 |      0.438 | 0.464 | 0.470 | 0.404 |      0.484 |      0.485 |
| b10      | stuck   |   4 | 0.398 |      0.402 | 0.411 | 0.411 | 0.396 |      0.484 |      0.480 |
| b10      | random  |   1 | 0.427 |      0.443 | 0.492 | 0.493 | 0.407 |      0.480 |      0.482 |
| b10      | random  |   2 | 0.389 |      0.410 | 0.484 | 0.484 | 0.407 |      0.484 |      0.484 |
| b10      | random  |   4 | 0.354 |      0.375 | 0.435 | 0.443 | 0.404 |      0.483 |      0.480 |

All severities and sets: `ft_comparison.csv`, `ft_vs_best_aug.csv` (columns subset, kset, fault, level).

## 6. Caveats
- Intervals: paired bootstrap over evaluation rows only, so optimistic (fault draw, training set and batch are not resampled).
- G3 passes on a single comparison (lenient); the tables above are the evidence, not the gate.
- The number of Test records flagged by the invalid-value rule was not recorded (decision E1); Test files were read once.
- k=4 sensor groups are a hypothesis. Per-batch rows use the faulted matrices drawn on the pooled Test rows (Stuck reference rows and Dropout/Random row choices are shared across batches).
- Batch 8 has few rows; per-batch Macro-F1 over the classes present in that batch only.
