# Part 1 (decisions_log Q9; secondary, defined after the Q results, not pre-registered)

From the saved v3 predictions and one extra arm (e) = v2 model b8_s{s} applied unchanged to batch 10. Under faults = k1/k2 equal weight, mean over 5 calibration seeds; 95% v2 shared-index scenario bootstrap (faults), 95% t over seeds (clean).

## part1_levels

| subset   | arm                              | method   |   value |   ci_low |   ci_high |
|:---------|:---------------------------------|:---------|--------:|---------:|----------:|
| b9       | (a) uncalibrated                 | svm      |  0.6095 |   0.5993 |    0.6193 |
| b9       | (a) uncalibrated                 | A        |  0.7059 |   0.6993 |    0.7123 |
| b9       | (a) uncalibrated                 | B        |  0.7041 |   0.6992 |    0.7089 |
| b9       | (b) same-period                  | svm      |  0.7714 |   0.7581 |    0.7848 |
| b9       | (b) same-period                  | A        |  0.9404 |   0.931  |    0.9493 |
| b9       | (b) same-period                  | B        |  0.9547 |   0.9474 |    0.9609 |
| b9       | (c) previous-period              | svm      |  0.6341 |   0.6241 |    0.6436 |
| b9       | (c) previous-period              | A        |  0.7297 |   0.7226 |    0.7362 |
| b9       | (c) previous-period              | B        |  0.7371 |   0.7323 |    0.7417 |
| b10      | (a) uncalibrated                 | svm      |  0.5121 |   0.5037 |    0.5205 |
| b10      | (a) uncalibrated                 | A        |  0.6211 |   0.6148 |    0.627  |
| b10      | (a) uncalibrated                 | B        |  0.6287 |   0.6239 |    0.6332 |
| b10      | (b) same-period                  | svm      |  0.6415 |   0.6329 |    0.6501 |
| b10      | (b) same-period                  | A        |  0.7653 |   0.7587 |    0.7714 |
| b10      | (b) same-period                  | B        |  0.7843 |   0.7792 |    0.7887 |
| b10      | (c) previous-period              | svm      |  0.5359 |   0.5271 |    0.5446 |
| b10      | (c) previous-period              | A        |  0.6455 |   0.6394 |    0.6511 |
| b10      | (c) previous-period              | B        |  0.6567 |   0.6516 |    0.661  |
| pooled   | (a) uncalibrated                 | svm      |  0.5293 |   0.5213 |    0.5372 |
| pooled   | (a) uncalibrated                 | A        |  0.6364 |   0.6302 |    0.6421 |
| pooled   | (a) uncalibrated                 | B        |  0.6423 |   0.6378 |    0.6466 |
| pooled   | (b) same-period                  | svm      |  0.6577 |   0.6492 |    0.6665 |
| pooled   | (b) same-period                  | A        |  0.7836 |   0.7772 |    0.7899 |
| pooled   | (b) same-period                  | B        |  0.802  |   0.7971 |    0.8063 |
| pooled   | (c) previous-period              | svm      |  0.5539 |   0.5455 |    0.5622 |
| pooled   | (c) previous-period              | A        |  0.6612 |   0.655  |    0.6667 |
| pooled   | (c) previous-period              | B        |  0.6716 |   0.6668 |    0.6758 |
| b10      | (e) two periods back (b8 on b10) | svm      |  0.5292 |   0.5208 |    0.5377 |
| b10      | (e) two periods back (b8 on b10) | A        |  0.6416 |   0.6352 |    0.6478 |

## part1_full_pipeline

| subset   | comparison                                  |   value |   ci_low |   ci_high |
|:---------|:--------------------------------------------|--------:|---------:|----------:|
| b9       | A in arm (c) - SVM in arm (a), under faults |  0.1201 |   0.1103 |    0.1299 |
| b9       | B in arm (c) - SVM in arm (a), under faults |  0.1276 |   0.1194 |    0.1365 |
| b10      | A in arm (c) - SVM in arm (a), under faults |  0.1334 |   0.1247 |    0.1422 |
| b10      | B in arm (c) - SVM in arm (a), under faults |  0.1446 |   0.1367 |    0.153  |
| pooled   | A in arm (c) - SVM in arm (a), under faults |  0.1319 |   0.1236 |    0.1406 |
| pooled   | B in arm (c) - SVM in arm (a), under faults |  0.1422 |   0.1348 |    0.1502 |

## part1_retention

| subset   | arm                              | method   |   retention_j6 |   worst |
|:---------|:---------------------------------|:---------|---------------:|--------:|
| b9       | (a) uncalibrated                 | svm      |         0.8282 |  0.1168 |
| b9       | (a) uncalibrated                 | A        |         0.9358 |  0.0372 |
| b9       | (a) uncalibrated                 | B        |         0.9328 |  0.343  |
| b9       | (b) same-period                  | svm      |         0.7866 |  0.0622 |
| b9       | (b) same-period                  | A        |         0.9438 |  0.0564 |
| b9       | (b) same-period                  | B        |         0.9576 |  0.2466 |
| b9       | (c) previous-period              | svm      |         0.8526 |  0.1304 |
| b9       | (c) previous-period              | A        |         0.9613 |  0.0476 |
| b9       | (c) previous-period              | B        |         0.9693 |  0.3293 |
| b10      | (a) uncalibrated                 | svm      |         0.7595 |  0.0297 |
| b10      | (a) uncalibrated                 | A        |         0.9461 |  0.0596 |
| b10      | (a) uncalibrated                 | B        |         0.9445 |  0.1458 |
| b10      | (b) same-period                  | svm      |         0.784  |  0.044  |
| b10      | (b) same-period                  | A        |         0.955  |  0.0721 |
| b10      | (b) same-period                  | B        |         0.9632 |  0.1743 |
| b10      | (c) previous-period              | svm      |         0.774  |  0.0289 |
| b10      | (c) previous-period              | A        |         0.9575 |  0.0678 |
| b10      | (c) previous-period              | B        |         0.9601 |  0.1483 |
| pooled   | (a) uncalibrated                 | svm      |         0.7712 |  0.1268 |
| pooled   | (a) uncalibrated                 | A        |         0.9463 |  0.1178 |
| pooled   | (a) uncalibrated                 | B        |         0.9436 |  0.2322 |
| pooled   | (b) same-period                  | svm      |         0.7885 |  0.1607 |
| pooled   | (b) same-period                  | A        |         0.9548 |  0.1373 |
| pooled   | (b) same-period                  | B        |         0.9634 |  0.3027 |
| pooled   | (c) previous-period              | svm      |         0.7867 |  0.1263 |
| pooled   | (c) previous-period              | A        |         0.9586 |  0.1021 |
| pooled   | (c) previous-period              | B        |         0.9616 |  0.2364 |
| b10      | (e) two periods back (b8 on b10) | svm      |         0.7639 |  0.0434 |
| b10      | (e) two periods back (b8 on b10) | A        |         0.953  |  0.1015 |

## part1_shelf_life

| calibration                   | age                      | target   |   A_faults_gain_vs_a |   A_ci_low |   A_ci_high |   share_of_same_period_gain |   clean_svm_gain_vs_a |   clean_ci_low |   clean_ci_high |
|:------------------------------|:-------------------------|:---------|---------------------:|-----------:|------------:|----------------------------:|----------------------:|---------------:|----------------:|
| same period (b)               | 0 (rows interleaved, N9) | b9       |               0.2345 |     0.2295 |      0.2389 |                      1      |                0.2446 |         0.2398 |          0.2495 |
| same period (b)               | 0 (rows interleaved, N9) | b10      |               0.1441 |     0.1413 |      0.1469 |                      1      |                0.144  |         0.1205 |          0.1675 |
| 8 -> 9 (c)                    | 1-8 months               | b9       |               0.0238 |     0.0211 |      0.0265 |                      0.1013 |                0.0078 |         0.0021 |          0.0134 |
| 9 -> 10 (c)                   | 6-12 months              | b10      |               0.0244 |     0.0231 |      0.0256 |                      0.169  |                0.0181 |         0.011  |          0.0251 |
| 8 -> 10 (e)                   | 13-14 months             | b10      |               0.0205 |     0.0196 |      0.0213 |                      0.1421 |                0.0184 |         0.0141 |          0.0227 |
| 8 -> 10 (e) minus 9 -> 10 (c) | 13-14 vs 6-12 months     | b10      |              -0.0039 |    -0.0051 |     -0.0027 |                    nan      |              nan      |       nan      |        nan      |
