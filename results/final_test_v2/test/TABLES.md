# Test v2 tables (POST-HOC; decisions_log N)

## Clean Macro-F1, (a) without and (b) with calibration, same rows

| subset   | method   |      a |   a_std |      b |   b_std |   b_minus_a |
|:---------|:---------|-------:|--------:|-------:|--------:|------------:|
| b10      | A        | 0.6565 |  0.0009 | 0.8014 |  0.0153 |      0.1449 |
| b10      | B        | 0.6657 |  0.0007 | 0.8143 |  0.0174 |      0.1486 |
| b10      | svm      | 0.6743 |  0.0008 | 0.8183 |  0.0192 |      0.144  |
| b8       | A        | 0.8491 |  0.0391 | 0.8628 |  0.0212 |      0.0137 |
| b8       | B        | 0.9183 |  0.0115 | 0.9587 |  0.0075 |      0.0403 |
| b8       | svm      | 0.8994 |  0.0257 | 0.9391 |  0.0263 |      0.0397 |
| b9       | A        | 0.7544 |  0.002  | 0.9965 |  0.0029 |      0.2421 |
| b9       | B        | 0.7548 |  0.002  | 0.997  |  0.0021 |      0.2421 |
| b9       | svm      | 0.736  |  0.0018 | 0.9806 |  0.0039 |      0.2446 |
| pooled   | A        | 0.6922 |  0.0005 | 0.8281 |  0.0128 |      0.1359 |
| pooled   | B        | 0.7005 |  0.0004 | 0.8402 |  0.0146 |      0.1397 |
| pooled   | svm      | 0.7056 |  0.0008 | 0.8418 |  0.0163 |      0.1362 |

Row-bootstrap intervals of (b)-(a) on clean rows:

| subset   | method   |   diff |   ci_low |   ci_high |
|:---------|:---------|-------:|---------:|----------:|
| b10      | svm      | 0.144  |   0.1384 |    0.1495 |
| b10      | A        | 0.1449 |   0.1391 |    0.1509 |
| b10      | B        | 0.1486 |   0.1431 |    0.1544 |
| b8       | svm      | 0.0397 |   0.0264 |    0.0597 |
| b8       | A        | 0.0137 |  -0.0131 |    0.0417 |
| b8       | B        | 0.0403 |   0.0239 |    0.0654 |
| b9       | svm      | 0.2446 |   0.2372 |    0.2531 |
| b9       | A        | 0.2421 |   0.2354 |    0.2499 |
| b9       | B        | 0.2421 |   0.2357 |    0.2496 |
| pooled   | svm      | 0.1362 |   0.1315 |    0.1413 |
| pooled   | A        | 0.1359 |   0.131  |    0.1411 |
| pooled   | B        | 0.1397 |   0.1348 |    0.145  |

## Under faults (k1, k2; every type and severity; k weighted equally)

| subset   | model   | method   |   mean_under_faults |     k1 |     k2 |   worst |   retained |   mean_under_faults_std |
|:---------|:--------|:---------|--------------------:|-------:|-------:|--------:|-----------:|------------------------:|
| b10      | a       | A        |              0.6211 | 0.6564 | 0.5859 |  0.0596 |     0.964  |                  0.0007 |
| b10      | a       | B        |              0.6287 | 0.6573 | 0.6002 |  0.1458 |     0.9587 |                  0.0004 |
| b10      | a       | svm      |              0.5121 | 0.5508 | 0.4734 |  0.0297 |     0.7786 |                  0.0004 |
| b10      | b       | A        |              0.7653 | 0.797  | 0.7336 |  0.0721 |     0.9682 |                  0.0139 |
| b10      | b       | B        |              0.7843 | 0.8099 | 0.7587 |  0.1743 |     0.9737 |                  0.0128 |
| b10      | b       | svm      |              0.6415 | 0.6891 | 0.5938 |  0.044  |     0.8034 |                  0.013  |
| b8       | a       | A        |              0.8409 | 0.886  | 0.7959 |  0.0297 |     1.009  |                  0.0195 |
| b8       | a       | B        |              0.8733 | 0.9122 | 0.8344 |  0.3135 |     0.9651 |                  0.0133 |
| b8       | a       | svm      |              0.6941 | 0.7481 | 0.6401 |  0.0985 |     0.7919 |                  0.0169 |
| b8       | b       | A        |              0.8764 | 0.9181 | 0.8347 |  0.0297 |     1.0321 |                  0.0166 |
| b8       | b       | B        |              0.9192 | 0.9503 | 0.888  |  0.3807 |     0.9696 |                  0.0135 |
| b8       | b       | svm      |              0.7423 | 0.7974 | 0.6873 |  0.0953 |     0.8101 |                  0.0195 |
| b9       | a       | A        |              0.7059 | 0.7377 | 0.6741 |  0.0372 |     0.9498 |                  0.0015 |
| b9       | a       | B        |              0.7041 | 0.7239 | 0.6842 |  0.343  |     0.9416 |                  0.0022 |
| b9       | a       | svm      |              0.6095 | 0.649  | 0.5701 |  0.1168 |     0.8461 |                  0.0018 |
| b9       | b       | A        |              0.9404 | 0.9852 | 0.8957 |  0.0564 |     0.9588 |                  0.0041 |
| b9       | b       | B        |              0.9547 | 0.9859 | 0.9234 |  0.2466 |     0.968  |                  0.0019 |
| b9       | b       | svm      |              0.7714 | 0.8359 | 0.7069 |  0.0622 |     0.8086 |                  0.0041 |
| pooled   | a       | A        |              0.6549 | 0.6901 | 0.6197 |  0.1146 |     0.963  |                  0.0005 |
| pooled   | a       | B        |              0.6608 | 0.6886 | 0.6331 |  0.2626 |     0.9565 |                  0.0004 |
| pooled   | a       | svm      |              0.5441 | 0.5838 | 0.5044 |  0.137  |     0.7899 |                  0.0007 |
| pooled   | b       | A        |              0.7912 | 0.8237 | 0.7587 |  0.137  |     0.9686 |                  0.0114 |
| pooled   | b       | B        |              0.8094 | 0.8348 | 0.784  |  0.336  |     0.9734 |                  0.0106 |
| pooled   | b       | svm      |              0.6637 | 0.7125 | 0.615  |  0.1691 |     0.8079 |                  0.0106 |

Scenario-bootstrap intervals:

| subset   | comparison                    |   diff |   ci_low |   ci_high |
|:---------|:------------------------------|-------:|---------:|----------:|
| b10      | (b)-(a) svm under faults      | 0.1294 |   0.1283 |    0.1304 |
| b10      | (b)-(a) A under faults        | 0.1441 |   0.1428 |    0.1455 |
| b10      | (b)-(a) B under faults        | 0.1555 |   0.1545 |    0.1566 |
| b10      | A-SVM under faults, model (a) | 0.109  |   0.1056 |    0.1127 |
| b10      | A-SVM under faults, model (b) | 0.1238 |   0.12   |    0.1281 |
| b8       | (b)-(a) svm under faults      | 0.0482 |   0.0464 |    0.0499 |
| b8       | (b)-(a) A under faults        | 0.0354 |   0.0342 |    0.0367 |
| b8       | (b)-(a) B under faults        | 0.0459 |   0.0449 |    0.0471 |
| b8       | A-SVM under faults, model (a) | 0.1468 |   0.1412 |    0.1529 |
| b8       | A-SVM under faults, model (b) | 0.134  |   0.1282 |    0.1402 |
| b9       | (b)-(a) svm under faults      | 0.1618 |   0.1585 |    0.1652 |
| b9       | (b)-(a) A under faults        | 0.2345 |   0.2323 |    0.2368 |
| b9       | (b)-(a) B under faults        | 0.2506 |   0.2485 |    0.2527 |
| b9       | A-SVM under faults, model (a) | 0.0964 |   0.0926 |    0.1005 |
| b9       | A-SVM under faults, model (b) | 0.1691 |   0.1635 |    0.1752 |
| pooled   | (b)-(a) svm under faults      | 0.1196 |   0.1185 |    0.1207 |
| pooled   | (b)-(a) A under faults        | 0.1363 |   0.1351 |    0.1376 |
| pooled   | (b)-(a) B under faults        | 0.1486 |   0.1477 |    0.1495 |
| pooled   | A-SVM under faults, model (a) | 0.1108 |   0.1072 |    0.1147 |
| pooled   | A-SVM under faults, model (b) | 0.1275 |   0.1231 |    0.1318 |

## Detector

| subset   | model   | setting   | fault   |    auroc |      tpr |   far_clean |   rows_with_alarm_clean |
|:---------|:--------|:----------|:--------|---------:|---------:|------------:|------------------------:|
| b10      | a       | clean     | none    | nan      | nan      |      0.0606 |                  0.6214 |
| b10      | a       | k1        | bias    |   0.9482 |   0.8825 |    nan      |                nan      |
| b10      | a       | k1        | dropout |   1      |   1      |    nan      |                nan      |
| b10      | a       | k1        | random  |   0.9603 |   0.9308 |    nan      |                nan      |
| b10      | a       | k1        | stuck   |   0.9145 |   0.867  |    nan      |                nan      |
| b10      | a       | k2        | bias    |   0.8338 |   0.5853 |    nan      |                nan      |
| b10      | a       | k2        | dropout |   1      |   1      |    nan      |                nan      |
| b10      | a       | k2        | random  |   0.9365 |   0.8652 |    nan      |                nan      |
| b10      | a       | k2        | stuck   |   0.7551 |   0.4305 |    nan      |                nan      |
| b10      | b       | clean     | none    | nan      | nan      |      0.054  |                  0.5487 |
| b10      | b       | k1        | bias    |   0.9571 |   0.9065 |    nan      |                nan      |
| b10      | b       | k1        | dropout |   1      |   1      |    nan      |                nan      |
| b10      | b       | k1        | random  |   0.9698 |   0.9526 |    nan      |                nan      |
| b10      | b       | k1        | stuck   |   0.9275 |   0.8894 |    nan      |                nan      |
| b10      | b       | k2        | bias    |   0.8699 |   0.6844 |    nan      |                nan      |
| b10      | b       | k2        | dropout |   1      |   1      |    nan      |                nan      |
| b10      | b       | k2        | random  |   0.9501 |   0.8924 |    nan      |                nan      |
| b10      | b       | k2        | stuck   |   0.7833 |   0.4927 |    nan      |                nan      |
| b8       | a       | clean     | none    | nan      | nan      |      0.0934 |                  0.8553 |
| b8       | a       | k1        | bias    |   0.9833 |   0.9708 |    nan      |                nan      |
| b8       | a       | k1        | dropout |   1      |   1      |    nan      |                nan      |
| b8       | a       | k1        | random  |   0.9819 |   0.9735 |    nan      |                nan      |
| b8       | a       | k1        | stuck   |   0.9073 |   0.8243 |    nan      |                nan      |
| b8       | a       | k2        | bias    |   0.8725 |   0.6374 |    nan      |                nan      |
| b8       | a       | k2        | dropout |   1      |   1      |    nan      |                nan      |
| b8       | a       | k2        | random  |   0.964  |   0.8977 |    nan      |                nan      |
| b8       | a       | k2        | stuck   |   0.755  |   0.4109 |    nan      |                nan      |
| b8       | b       | clean     | none    | nan      | nan      |      0.0897 |                  0.8417 |
| b8       | b       | k1        | bias    |   0.9849 |   0.9809 |    nan      |                nan      |
| b8       | b       | k1        | dropout |   1      |   1      |    nan      |                nan      |
| b8       | b       | k1        | random  |   0.983  |   0.9792 |    nan      |                nan      |
| b8       | b       | k1        | stuck   |   0.9119 |   0.8344 |    nan      |                nan      |
| b8       | b       | k2        | bias    |   0.8837 |   0.6511 |    nan      |                nan      |
| b8       | b       | k2        | dropout |   1      |   1      |    nan      |                nan      |
| b8       | b       | k2        | random  |   0.9696 |   0.9084 |    nan      |                nan      |
| b8       | b       | k2        | stuck   |   0.7641 |   0.4286 |    nan      |                nan      |
| b9       | a       | clean     | none    | nan      | nan      |      0.0777 |                  0.761  |
| b9       | a       | k1        | bias    |   0.9803 |   0.9571 |    nan      |                nan      |
| b9       | a       | k1        | dropout |   1      |   1      |    nan      |                nan      |
| b9       | a       | k1        | random  |   0.9828 |   0.9799 |    nan      |                nan      |
| b9       | a       | k1        | stuck   |   0.8932 |   0.7817 |    nan      |                nan      |
| b9       | a       | k2        | bias    |   0.8711 |   0.6388 |    nan      |                nan      |
| b9       | a       | k2        | dropout |   1      |   1      |    nan      |                nan      |
| b9       | a       | k2        | random  |   0.9634 |   0.8942 |    nan      |                nan      |
| b9       | a       | k2        | stuck   |   0.753  |   0.3655 |    nan      |                nan      |
| b9       | b       | clean     | none    | nan      | nan      |      0.0775 |                  0.74   |
| b9       | b       | k1        | bias    |   0.9826 |   0.966  |    nan      |                nan      |
| b9       | b       | k1        | dropout |   1      |   1      |    nan      |                nan      |
| b9       | b       | k1        | random  |   0.9841 |   0.9852 |    nan      |                nan      |
| b9       | b       | k1        | stuck   |   0.8985 |   0.7966 |    nan      |                nan      |
| b9       | b       | k2        | bias    |   0.8823 |   0.67   |    nan      |                nan      |
| b9       | b       | k2        | dropout |   1      |   1      |    nan      |                nan      |
| b9       | b       | k2        | random  |   0.9678 |   0.9084 |    nan      |                nan      |
| b9       | b       | k2        | stuck   |   0.7738 |   0.4104 |    nan      |                nan      |

```
{
 "rule": "decisions_log N8",
 "post_hoc": true,
 "subset": "pooled",
 "clean_b_minus_a_svm": [
  0.1361554495626392,
  0.1315113872479087,
  0.1413067931980161
 ],
 "calibrated_A_minus_SVM_under_faults": 0.12749683730636174,
 "success": true
}
```