# Edge cost of pipeline A (detector + reconstruction + SVM)

Bundle size: **798 KB** (svm 527 KB, pre 4 KB, det 267 KB, det_full_with_training_arrays 1777 KB)

| case | median (ms) | p95 (ms) | mean flagged sensors |
|---|---|---|---|
| fault_free | 5.704 | 10.049 | 2.19 |
| bias_one_sensor | 6.106 | 10.358 | 3.52 |
| bias_one_sensor_cold_weights | 7.986 | 14.554 | 3.52 |

Memory: 138 MB after imports, 147 MB peak (working set of the measuring process, 1000 runs per case).

Validation rows, one core, one BLAS thread, laptop CPU; sizes are pickles (float64). The bundle holds the SVM, the preprocessing and the detector without its training-only arrays.