# Dev tournament (decisions_log R1-R3; Drift-Dev targets 6 and 7, seeds 0-4, A under faults, k1/k2 equal)

| config   | rows   |   dev_score_A_faults |   prev_same_rows |   delta_vs_prev |   delta_t6 |   delta_t7 |   clean_svm |   clean_svm_minus_prev | candidate   |
|:---------|:-------|---------------------:|-----------------:|----------------:|-----------:|-----------:|------------:|-----------------------:|:------------|
| uncal    | keep   |               0.6297 |           0.7388 |         -0.1091 |    -0.02   |    -0.1982 |      0.6166 |                -0.1279 | False       |
| same     | keep   |               0.9176 |           0.7388 |          0.1788 |     0.2896 |     0.068  |      0.939  |                 0.1945 | False       |
| prev     | keep   |               0.7388 |           0.7388 |          0      |     0      |     0      |      0.7445 |                 0      | False       |
| prev     | H2     |               0.7363 |           0.7363 |          0      |     0      |     0      |      0.7413 |                 0      | False       |
| W1       | keep   |               0.7401 |           0.7388 |          0.0013 |     0      |     0.0027 |      0.7478 |                 0.0033 | True        |
| W5       | keep   |               0.737  |           0.7388 |         -0.0018 |     0      |    -0.0036 |      0.7487 |                 0.0042 | True        |
| W20      | keep   |               0.7351 |           0.7388 |         -0.0036 |     0      |    -0.0073 |      0.7453 |                 0.0008 | True        |
| C1       | keep   |               0.7415 |           0.7388 |          0.0027 |     0.0059 |    -0.0004 |      0.7511 |                 0.0066 | True        |
| C2       | keep   |               0.737  |           0.7388 |         -0.0018 |     0.0516 |    -0.0552 |      0.7452 |                 0.0007 | True        |
| S30      | H2     |               0.722  |           0.7363 |         -0.0143 |    -0.011  |    -0.0175 |      0.7343 |                -0.007  | True        |
| S60      | H2     |               0.7352 |           0.7363 |         -0.001  |    -0.0063 |     0.0042 |      0.7478 |                 0.0065 | True        |

```
{
 "rule": "decisions_log R3",
 "eligible": [
  "W1",
  "W5",
  "W20",
  "C1",
  "C2",
  "S60"
 ],
 "winner": "W1",
 "go": false,
 "winner_delta_vs_prev": 0.0013270167424072055,
 "winner_clean_svm_minus_prev": 0.0032782604798876624,
 "thresholds": {
  "go_delta": 0.01,
  "clean_tol": 0.005,
  "tie": 0.002
 },
 "check_W1_equals_prev_on_target_6": true,
 "tournament_seconds": 3465
}
```
