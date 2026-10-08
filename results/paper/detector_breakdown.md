# Detector breakdown, v1 final test (batches 8-10), primary detector `median`

Read from existing result files only (`results/final_test/test/`); no experiment was run and the Test data were not read again. Threshold = the frozen alarm threshold (95th percentile of the Train out-of-fold scores). 'غير محسوب' = not present in the result files, deliberately not derived.

Definitions: AUROC = isolation AUROC (faulty blocks vs healthy blocks of the same rows), mean over the scenarios of the cell; TPR = share of faulty blocks flagged; FPR(healthy, same rows) = share of healthy blocks flagged in the faulted rows; FAR(clean) = share of sensor-rows flagged on the clean (no injected fault) Test rows.

## 1. AUROC and TPR at the frozen threshold, per fault type x severity x k (Test pooled)

| k   | fault   |   severity |   scenarios |   AUROC |    TPR |   FPR (healthy, same rows) |
|:----|:--------|-----------:|------------:|--------:|-------:|---------------------------:|
| k1  | bias    |        0.5 |          80 |  0.9507 | 0.8854 |                     0.1118 |
| k1  | bias    |        1   |          80 |  0.9779 | 0.9641 |                     0.1373 |
| k1  | bias    |        3   |          80 |  0.9926 | 0.9996 |                     0.1553 |
| k1  | dropout |        0.5 |          80 |  1      | 1      |                     0.1237 |
| k1  | dropout |        1   |          80 |  1      | 1      |                     0.1236 |
| k1  | random  |        0.5 |          80 |  0.9793 | 0.9894 |                     0.139  |
| k1  | random  |        1   |          80 |  0.9793 | 0.9894 |                     0.1391 |
| k1  | stuck   |        0.5 |          80 |  0.9484 | 0.9104 |                     0.1285 |
| k1  | stuck   |        1   |          80 |  0.9492 | 0.9127 |                     0.127  |
| k2  | bias    |        0.5 |          40 |  0.8371 | 0.5137 |                     0.0794 |
| k2  | bias    |        1   |          40 |  0.8776 | 0.6278 |                     0.0826 |
| k2  | bias    |        3   |          40 |  0.9228 | 0.7578 |                     0.111  |
| k2  | dropout |        0.5 |          40 |  1      | 1      |                     0.0676 |
| k2  | dropout |        1   |          40 |  1      | 1      |                     0.0675 |
| k2  | random  |        0.5 |          40 |  0.9723 | 0.9277 |                     0.0913 |
| k2  | random  |        1   |          40 |  0.9726 | 0.9293 |                     0.0907 |
| k2  | stuck   |        0.5 |          40 |  0.7701 | 0.451  |                     0.0846 |
| k2  | stuck   |        1   |          40 |  0.7877 | 0.4552 |                     0.0845 |
| k4  | bias    |        0.5 |          20 |  0.7351 | 0.2717 |                     0.0699 |
| k4  | bias    |        1   |          20 |  0.7582 | 0.3899 |                     0.123  |
| k4  | bias    |        3   |          20 |  0.8021 | 0.4168 |                     0.1087 |
| k4  | dropout |        0.5 |          20 |  1      | 1      |                     0.032  |
| k4  | dropout |        1   |          20 |  1      | 1      |                     0.032  |
| k4  | random  |        0.5 |          20 |  0.9558 | 0.8256 |                     0.0543 |
| k4  | random  |        1   |          20 |  0.956  | 0.8261 |                     0.0541 |
| k4  | stuck   |        0.5 |          20 |  0.6737 | 0.2042 |                     0.0627 |
| k4  | stuck   |        1   |          20 |  0.6174 | 0.1825 |                     0.0712 |

## 2. AUROC and FAR per Test batch

An AUROC pooled over all scenarios of a batch is not in the files; the per-cell values of every batch are in `ft_detector_summary.csv` (and the per-batch k=1 medium values below).

| subset   | AUROC over all scenarios   |   G2 statistic (median over fault types, k=1 medium) |   AUROC k=1 medium dropout |   AUROC k=1 medium bias |   AUROC k=1 medium stuck |   AUROC k=1 medium random |   FAR clean, all sensors |   FAR clean, without S01,S02 |   clean rows with any alarm |
|:---------|:---------------------------|-----------------------------------------------------:|---------------------------:|------------------------:|-------------------------:|--------------------------:|-------------------------:|-----------------------------:|----------------------------:|
| b8       | غير محسوب                  |                                               0.9657 |                          1 |                  0.973  |                   0.906  |                    0.9583 |                   0.1518 |                       0.0318 |                      1      |
| b9       | غير محسوب                  |                                               0.9884 |                          1 |                  0.9907 |                   0.9633 |                    0.9861 |                   0.067  |                       0.0505 |                      0.6064 |
| b10      | غير محسوب                  |                                               0.9789 |                          1 |                  0.9771 |                   0.9501 |                    0.9807 |                   0.0738 |                       0.046  |                      0.7386 |
| pooled   | غير محسوب                  |                                               0.9786 |                          1 |                  0.9779 |                   0.9484 |                    0.9793 |                   0.0783 |                       0.0455 |                      0.742  |

## 3. FAR per sensor on the clean Test rows (alarm rate of the sensor at the frozen threshold)

| sensor   |   pooled |     b8 |     b9 |    b10 |
|:---------|---------:|-------:|-------:|-------:|
| S01      |   0.5023 | 1      | 0.1255 | 0.5108 |
| S02      |   0.1134 | 0.983  | 0.2404 | 0.0258 |
| S03      |   0.0096 | 0.119  | 0.0064 | 0.0011 |
| S04      |   0.0268 | 0.0442 | 0.0319 | 0.0247 |
| S05      |   0.0181 | 0      | 0.0723 | 0.0125 |
| S06      |   0.0323 | 0.0034 | 0.0277 | 0.0353 |
| S07      |   0.0357 | 0.0204 | 0.0596 | 0.0339 |
| S08      |   0.2713 | 0.034  | 0.2872 | 0.2886 |
| S09      |   0.063  | 0.1361 | 0.083  | 0.0544 |
| S10      |   0.0112 | 0      | 0.0021 | 0.0133 |
| S11      |   0.0082 | 0      | 0      | 0.01   |
| S12      |   0.0648 | 0.0782 | 0.0255 | 0.0689 |
| S13      |   0.0124 | 0      | 0.0021 | 0.0147 |
| S14      |   0.0337 | 0      | 0.0043 | 0.0403 |
| S15      |   0.0179 | 0.0068 | 0.0255 | 0.0178 |
| S16      |   0.0319 | 0.0034 | 0.0787 | 0.0281 |

Expected without drift: about 0.05 per sensor (the threshold is the 95th percentile of the Train out-of-fold scores).
