**Table 1. Clean (fault-free) Macro-F1 of the reference models.** Augmented models: mean ± std over 5 augmentation seeds. Models are trained on batches 1-6 only.

| model                         | Validation (batch 7)   | Test pooled   | Test b8       | Test b9       | Test b10      |
|:------------------------------|:-----------------------|:--------------|:--------------|:--------------|:--------------|
| SVM                           | 0.859                  | 0.535         | 0.798         | 0.655         | 0.480         |
| SVM + fault augmentation      | 0.778 ± 0.020          | 0.531 ± 0.020 | 0.756 ± 0.050 | 0.763 ± 0.079 | 0.471 ± 0.015 |
| LightGBM                      | 0.692                  | 0.514         | 0.587         | 0.558         | 0.489         |
| LightGBM + fault augmentation | 0.701 ± 0.007          | 0.474 ± 0.008 | 0.628 ± 0.045 | 0.560 ± 0.028 | 0.435 ± 0.013 |

Evaluation rows: pooled = 4364, b8 = 294, b9 = 470, b10 = 3600
