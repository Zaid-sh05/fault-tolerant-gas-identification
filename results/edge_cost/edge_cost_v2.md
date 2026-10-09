# Edge cost of v2 (few-shot recalibration)

| part | size (KB) |
|---|---|
| svm_calibrated | 511 |
| preprocessing | 4 |
| detector_for_A | 267 |
| B_136_reduced_models | 61973 |
| A_bundle_svm_pre_detector | 782 |
| B_bundle_pre_detector_136_models | 62243 |
| Train rows needed on the device (or server) for the calibration refit, float64 | 5991 |

| single-sample case | median (ms) | p95 (ms) |
|---|---|---|
| svm_only_fault_free | 5.409 | 11.633 |
| A_fault_free | 9.343 | 20.519 |
| A_bias_one_sensor | 7.773 | 18.447 |
| B_fault_free | 7.448 | 17.038 |
| B_bias_one_sensor | 7.246 | 18.430 |

| calibration step (one core) | seconds |
|---|---|
| preprocessing + SVM refit | 1.43 |
| detector refit | 2.39 |
| 136 reduced B models | 149.11 |
| total | 152.92 |

Calibration rows: 60; refit on 5991 rows. Memory: 138 MB after imports, 228 MB peak.

v2 deployment simulated on Validation batch 7 (calibration seed 0, 10 rows per gas); one core, one BLAS thread, laptop CPU; pickled float64 sizes. B covers every k=1 and k=2 exclusion set (136 models); its latency uses the two highest-ratio flagged sensors.