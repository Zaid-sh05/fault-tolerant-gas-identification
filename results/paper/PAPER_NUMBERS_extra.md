# Extra numbers: oracle selector between A and B (POST-HOC, DESCRIPTIVE; decisions_log P)

Source: `results/oracle_selector/summary.csv`, written by `results/oracle_selector/oracle_selector.py` from saved results (no model trained,
nothing re-run). Gain = mean Macro-F1 of a per-scenario oracle that picks the better of A (`A_det_twin`) and B (`B_det`), minus the mean of
the better fixed strategy on the same scenarios (column `best_fixed`). Development data only (Validation 7 and Drift-Dev, batches 1-7).
The paper's "at most 0.01 on development data" is the largest of these gains at two decimals (0.0101 rounds to 0.01).

| number | value | source |
|---|---|---|
| Oracle selector gain over the better fixed strategy, Validation 7 (v1) | 0.0101 | results/oracle_selector/summary.csv, dataset=1_val7_v1, column gain_vs_best |
| Oracle selector gain over the better fixed strategy, Drift-Dev calibrated | 0.0030 | results/oracle_selector/summary.csv, dataset=2_driftdev_calibrated, column gain_vs_best |
| Oracle selector gain over the better fixed strategy, Drift-Dev uncalibrated | 0.0046 | results/oracle_selector/summary.csv, dataset=2b_driftdev_uncalibrated, column gain_vs_best |
