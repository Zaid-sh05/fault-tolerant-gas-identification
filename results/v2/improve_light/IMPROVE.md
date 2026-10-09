# Night study, heavy part (POST-HOC, decisions_log L2-L4, L7)

| protocol   | method   |   clean |   mean_under_faults |   worst |
|:-----------|:---------|--------:|--------------------:|--------:|
| drift_dev  | V0       |  0.646  |              0.6119 |  0.3464 |
| drift_dev  | V1       |  0.6395 |              0.6104 |  0.382  |
| drift_dev  | V2       |  0.6457 |              0.6097 |  0.365  |
| drift_dev  | V3       |  0.6408 |              0.6091 |  0.3635 |
| drift_dev  | V5       |  0.6247 |              0.6088 |  0.3942 |
| drift_dev  | svm      |  0.6185 |              0.5626 |  0.3512 |
| original   | V0       |  0.8495 |              0.8043 |  0.4943 |
| original   | V1       |  0.8223 |              0.7968 |  0.5042 |
| original   | V2       |  0.852  |              0.7972 |  0.48   |
| original   | V3       |  0.8276 |              0.7925 |  0.4795 |
| original   | V5       |  0.8403 |              0.8085 |  0.5556 |
| original   | svm      |  0.859  |              0.7422 |  0.4655 |

Clean false alarms (share of sensor-rows) and rows with an alarm:

| protocol   |   V0_far_clean_or_fpr |   V1_far_clean_or_fpr |   V2_far_clean_or_fpr |   V3_far_clean_or_fpr |   V5_far_clean_or_fpr |   V0_rows_with_alarm |   V1_rows_with_alarm |   V2_rows_with_alarm |   V3_rows_with_alarm |   V5_rows_with_alarm |
|:-----------|----------------------:|----------------------:|----------------------:|----------------------:|----------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| drift_dev  |                0.0871 |                0.1211 |                0.0522 |                0.0689 |                0.0871 |               0.8727 |               0.9499 |               0.603  |               0.7441 |               0.8727 |
| original   |                0.1347 |                0.2214 |                0.0988 |                0.1539 |                0.1347 |               0.9709 |               0.987  |               0.8962 |               0.9159 |               0.9709 |

Detector (isolation AUROC, TPR):

| protocol   | setting   | fault   |   V0_auroc |   V0_tpr |   V1_auroc |   V1_tpr |   V2_auroc |   V2_tpr |   V3_auroc |   V3_tpr |
|:-----------|:----------|:--------|-----------:|---------:|-----------:|---------:|-----------:|---------:|-----------:|---------:|
| drift_dev  | k1        | bias    |      0.977 |    0.957 |      0.971 |    0.969 |      0.974 |    0.898 |      0.968 |    0.909 |
| drift_dev  | k1        | dropout |      1     |    1     |      1     |    1     |      1     |    1     |      1     |    1     |
| drift_dev  | k1        | random  |      0.974 |    0.976 |      0.971 |    0.98  |      0.972 |    0.924 |      0.969 |    0.934 |
| drift_dev  | k1        | stuck   |      0.911 |    0.801 |      0.899 |    0.82  |      0.909 |    0.708 |      0.898 |    0.727 |
| drift_dev  | k2        | bias    |      0.88  |    0.705 |      0.925 |    0.838 |      0.875 |    0.543 |      0.91  |    0.729 |
| drift_dev  | k2        | dropout |      1     |    1     |      1     |    1     |      1     |    1     |      1     |    1     |
| drift_dev  | k2        | random  |      0.955 |    0.871 |      0.953 |    0.937 |      0.951 |    0.744 |      0.949 |    0.834 |
| drift_dev  | k2        | stuck   |      0.72  |    0.297 |      0.834 |    0.652 |      0.722 |    0.161 |      0.825 |    0.49  |
| drift_dev  | k4        | bias    |      0.719 |    0.299 |      0.734 |    0.468 |      0.715 |    0.147 |      0.719 |    0.215 |
| drift_dev  | k4        | dropout |      1     |    1     |      1     |    1     |      1     |    1     |      1     |    1     |
| drift_dev  | k4        | random  |      0.933 |    0.736 |      0.925 |    0.796 |      0.926 |    0.546 |      0.917 |    0.608 |
| drift_dev  | k4        | stuck   |      0.566 |    0.131 |      0.621 |    0.256 |      0.565 |    0.081 |      0.611 |    0.143 |
| original   | k1        | bias    |      0.98  |    0.993 |      0.977 |    0.993 |      0.985 |    0.976 |      0.981 |    0.977 |
| original   | k1        | dropout |      1     |    1     |      1     |    1     |      1     |    1     |      1     |    1     |
| original   | k1        | random  |      0.974 |    0.998 |      0.975 |    0.999 |      0.981 |    0.983 |      0.98  |    0.986 |
| original   | k1        | stuck   |      0.937 |    0.949 |      0.93  |    0.958 |      0.945 |    0.904 |      0.936 |    0.919 |
| original   | k2        | bias    |      0.884 |    0.627 |      0.929 |    0.843 |      0.886 |    0.502 |      0.924 |    0.699 |
| original   | k2        | dropout |      1     |    1     |      1     |    1     |      1     |    1     |      1     |    1     |
| original   | k2        | random  |      0.968 |    0.959 |      0.962 |    0.98  |      0.974 |    0.883 |      0.964 |    0.925 |
| original   | k2        | stuck   |      0.755 |    0.493 |      0.853 |    0.815 |      0.759 |    0.34  |      0.852 |    0.684 |
| original   | k4        | bias    |      0.755 |    0.412 |      0.721 |    0.532 |      0.754 |    0.2   |      0.711 |    0.316 |
| original   | k4        | dropout |      1     |    1     |      1     |    1     |      1     |    1     |      1     |    1     |
| original   | k4        | random  |      0.956 |    0.862 |      0.946 |    0.895 |      0.955 |    0.687 |      0.941 |    0.743 |
| original   | k4        | stuck   |      0.625 |    0.25  |      0.701 |    0.471 |      0.629 |    0.182 |      0.699 |    0.341 |

```
{
 "rule": "decisions_log L4 (select on Drift-Dev, confirm on Validation 7)",
 "post_hoc": true,
 "selected": "V0",
 "success": false,
 "note": "no variant beat V0 on Drift-Dev (within the tie margin)",
 "lr_confirmation": {
  "note": "not part of the light run (needs new reduced B models, L8)"
 }
}
```