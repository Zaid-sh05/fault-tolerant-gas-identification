# CORAL check (DIAGNOSTIC ONLY, decisions_log K1)

| protocol   |   batch |   max_abs_diff_vs_independent |   cov_gap_before |   cov_gap_after |   mean_norm_train |   mean_norm_batch_before |   mean_norm_batch_after |   f1_M0 |   f1_M2_ours | M2_reproduces_candidates   |   f1_coral_paper_direction |
|:-----------|--------:|------------------------------:|-----------------:|----------------:|------------------:|-------------------------:|------------------------:|--------:|-------------:|:---------------------------|---------------------------:|
| drift_dev  |       6 |                             0 |           0.5665 |          0.1747 |                 0 |                   5.1758 |                 10.4505 |  0.6182 |       0.3548 | True                       |                     0.6116 |
| drift_dev  |       7 |                             0 |           0.4833 |          0.2043 |                 0 |                   5.0701 |                 10.9157 |  0.6187 |       0.3941 | True                       |                     0.6231 |
| original   |       7 |                             0 |           0.445  |          0.189  |                 0 |                   3.5312 |                  7.3108 |  0.859  |       0.5057 | True                       |                     0.7588 |
