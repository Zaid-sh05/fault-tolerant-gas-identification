# Numbers used in the paper and where they come from

Every value is read from a result file by `scripts/ft_paper.py`; nothing is typed by hand. Intervals: paired bootstrap over evaluation rows only (1000 resamples), so they are optimistic: they ignore the variation of the fault draw, of the training set and of the batch. Gate G3 passes if a single comparison passes (lenient).

| number | value | source |
|---|---|---|
| Validation clean Macro-F1, SVM | 0.8590 | results\overnight\temporal/clean_eval.csv, rows ['svm'], column macro_f1 (mean over rows) |
| Test clean Macro-F1, SVM, pooled | 0.5354 | results\final_test\test/ft_clean_by_subset.csv, subset=pooled, methods ['svm'], column macro_f1 (mean) |
| Test clean Macro-F1, SVM, b8 | 0.7979 | results\final_test\test/ft_clean_by_subset.csv, subset=b8, methods ['svm'], column macro_f1 (mean) |
| Test clean Macro-F1, SVM, b9 | 0.6553 | results\final_test\test/ft_clean_by_subset.csv, subset=b9, methods ['svm'], column macro_f1 (mean) |
| Test clean Macro-F1, SVM, b10 | 0.4801 | results\final_test\test/ft_clean_by_subset.csv, subset=b10, methods ['svm'], column macro_f1 (mean) |
| Validation clean Macro-F1, SVM + fault augmentation | 0.7779 | results\overnight\temporal/clean_eval.csv, rows ['svm_aug0', 'svm_aug1', 'svm_aug2', 'svm_aug3', 'svm_aug4'], column macro_f1 (mean over rows) |
| Test clean Macro-F1, SVM + fault augmentation, pooled | 0.5307 | results\final_test\test/ft_clean_by_subset.csv, subset=pooled, methods ['svm_aug0', 'svm_aug1', 'svm_aug2', 'svm_aug3', 'svm_aug4'], column macro_f1 (mean) |
| Test clean Macro-F1, SVM + fault augmentation, b8 | 0.7563 | results\final_test\test/ft_clean_by_subset.csv, subset=b8, methods ['svm_aug0', 'svm_aug1', 'svm_aug2', 'svm_aug3', 'svm_aug4'], column macro_f1 (mean) |
| Test clean Macro-F1, SVM + fault augmentation, b9 | 0.7630 | results\final_test\test/ft_clean_by_subset.csv, subset=b9, methods ['svm_aug0', 'svm_aug1', 'svm_aug2', 'svm_aug3', 'svm_aug4'], column macro_f1 (mean) |
| Test clean Macro-F1, SVM + fault augmentation, b10 | 0.4711 | results\final_test\test/ft_clean_by_subset.csv, subset=b10, methods ['svm_aug0', 'svm_aug1', 'svm_aug2', 'svm_aug3', 'svm_aug4'], column macro_f1 (mean) |
| Validation clean Macro-F1, LightGBM | 0.6918 | results\overnight\temporal/clean_eval.csv, rows ['lgbm'], column macro_f1 (mean over rows) |
| Test clean Macro-F1, LightGBM, pooled | 0.5141 | results\final_test\test/ft_clean_by_subset.csv, subset=pooled, methods ['lgbm'], column macro_f1 (mean) |
| Test clean Macro-F1, LightGBM, b8 | 0.5867 | results\final_test\test/ft_clean_by_subset.csv, subset=b8, methods ['lgbm'], column macro_f1 (mean) |
| Test clean Macro-F1, LightGBM, b9 | 0.5576 | results\final_test\test/ft_clean_by_subset.csv, subset=b9, methods ['lgbm'], column macro_f1 (mean) |
| Test clean Macro-F1, LightGBM, b10 | 0.4889 | results\final_test\test/ft_clean_by_subset.csv, subset=b10, methods ['lgbm'], column macro_f1 (mean) |
| Validation clean Macro-F1, LightGBM + fault augmentation | 0.7006 | results\overnight\temporal/clean_eval.csv, rows ['lgbm_aug0', 'lgbm_aug1', 'lgbm_aug2', 'lgbm_aug3', 'lgbm_aug4'], column macro_f1 (mean over rows) |
| Test clean Macro-F1, LightGBM + fault augmentation, pooled | 0.4745 | results\final_test\test/ft_clean_by_subset.csv, subset=pooled, methods ['lgbm_aug0', 'lgbm_aug1', 'lgbm_aug2', 'lgbm_aug3', 'lgbm_aug4'], column macro_f1 (mean) |
| Test clean Macro-F1, LightGBM + fault augmentation, b8 | 0.6275 | results\final_test\test/ft_clean_by_subset.csv, subset=b8, methods ['lgbm_aug0', 'lgbm_aug1', 'lgbm_aug2', 'lgbm_aug3', 'lgbm_aug4'], column macro_f1 (mean) |
| Test clean Macro-F1, LightGBM + fault augmentation, b9 | 0.5599 | results\final_test\test/ft_clean_by_subset.csv, subset=b9, methods ['lgbm_aug0', 'lgbm_aug1', 'lgbm_aug2', 'lgbm_aug3', 'lgbm_aug4'], column macro_f1 (mean) |
| Test clean Macro-F1, LightGBM + fault augmentation, b10 | 0.4346 | results\final_test\test/ft_clean_by_subset.csv, subset=b10, methods ['lgbm_aug0', 'lgbm_aug1', 'lgbm_aug2', 'lgbm_aug3', 'lgbm_aug4'], column macro_f1 (mean) |
| Number of evaluation rows, pooled | 4364 | results\final_test\test/ft_clean_by_subset.csv, method=svm, column rows |
| Number of evaluation rows, b8 | 294 | results\final_test\test/ft_clean_by_subset.csv, method=svm, column rows |
| Number of evaluation rows, b9 | 470 | results\final_test\test/ft_clean_by_subset.csv, method=svm, column rows |
| Number of evaluation rows, b10 | 3600 | results\final_test\test/ft_clean_by_subset.csv, method=svm, column rows |
| A minus best augmented baseline, dropout, k=1, medium, Test pooled | 0.0263 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, dropout, k=1, medium, Test pooled | 0.0203 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, dropout, k=1, medium, Test pooled | 0.5073 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column svm |
| Macro-F1 A, dropout, k=1, medium, Test pooled | 0.5430 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column A_det_twin |
| Macro-F1 B, dropout, k=1, medium, Test pooled | 0.5369 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column B_det |
| Macro-F1 C, dropout, k=1, medium, Test pooled | 0.4057 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column C_det |
| Macro-F1 Oracle A, dropout, k=1, medium, Test pooled | 0.5340 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, dropout, k=1, medium, Test pooled | 0.5360 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, dropout, k=1, medium, Test pooled | 0.5167 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=dropout, level=0.5, column svm_aug |
| A minus best augmented baseline, dropout, k=2, medium, Test pooled | 0.0416 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, dropout, k=2, medium, Test pooled | 0.0354 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, dropout, k=2, medium, Test pooled | 0.4797 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column svm |
| Macro-F1 A, dropout, k=2, medium, Test pooled | 0.5413 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column A_det_twin |
| Macro-F1 B, dropout, k=2, medium, Test pooled | 0.5351 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column B_det |
| Macro-F1 C, dropout, k=2, medium, Test pooled | 0.4046 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column C_det |
| Macro-F1 Oracle A, dropout, k=2, medium, Test pooled | 0.5362 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, dropout, k=2, medium, Test pooled | 0.5340 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, dropout, k=2, medium, Test pooled | 0.4997 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=dropout, level=0.5, column svm_aug |
| A minus best augmented baseline, dropout, k=4, medium, Test pooled | 0.0734 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, dropout, k=4, medium, Test pooled | 0.0670 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, dropout, k=4, medium, Test pooled | 0.4426 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column svm |
| Macro-F1 A, dropout, k=4, medium, Test pooled | 0.5373 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column A_det_twin |
| Macro-F1 B, dropout, k=4, medium, Test pooled | 0.5309 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column B_det |
| Macro-F1 C, dropout, k=4, medium, Test pooled | 0.4058 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column C_det |
| Macro-F1 Oracle A, dropout, k=4, medium, Test pooled | 0.5331 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, dropout, k=4, medium, Test pooled | 0.5277 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, dropout, k=4, medium, Test pooled | 0.4639 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=dropout, level=0.5, column svm_aug |
| A minus best augmented baseline, bias, k=1, medium, Test pooled | 0.0127 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=bias, level=1.0, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, bias, k=1, medium, Test pooled | 0.0076 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=bias, level=1.0, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, bias, k=1, medium, Test pooled | 0.5161 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column svm |
| Macro-F1 A, bias, k=1, medium, Test pooled | 0.5362 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column A_det_twin |
| Macro-F1 B, bias, k=1, medium, Test pooled | 0.5311 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column B_det |
| Macro-F1 C, bias, k=1, medium, Test pooled | 0.4068 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column C_det |
| Macro-F1 Oracle A, bias, k=1, medium, Test pooled | 0.5321 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column A_orc_twin |
| Macro-F1 Oracle B, bias, k=1, medium, Test pooled | 0.5354 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column B_orc |
| Macro-F1 best augmented baseline, bias, k=1, medium, Test pooled | 0.5235 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=bias, level=1.0, column svm_aug |
| A minus best augmented baseline, bias, k=2, medium, Test pooled | -0.0053 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=bias, level=1.0, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, bias, k=2, medium, Test pooled | 0.0033 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=bias, level=1.0, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, bias, k=2, medium, Test pooled | 0.4644 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column svm |
| Macro-F1 A, bias, k=2, medium, Test pooled | 0.5050 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column A_det_twin |
| Macro-F1 B, bias, k=2, medium, Test pooled | 0.5137 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column B_det |
| Macro-F1 C, bias, k=2, medium, Test pooled | 0.4096 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column C_det |
| Macro-F1 Oracle A, bias, k=2, medium, Test pooled | 0.5362 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column A_orc_twin |
| Macro-F1 Oracle B, bias, k=2, medium, Test pooled | 0.5315 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column B_orc |
| Macro-F1 best augmented baseline, bias, k=2, medium, Test pooled | 0.5104 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=bias, level=1.0, column svm_aug |
| A minus best augmented baseline, bias, k=4, medium, Test pooled | -0.0696 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=bias, level=1.0, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, bias, k=4, medium, Test pooled | -0.0368 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=bias, level=1.0, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, bias, k=4, medium, Test pooled | 0.3930 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column svm |
| Macro-F1 A, bias, k=4, medium, Test pooled | 0.3958 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column A_det_twin |
| Macro-F1 B, bias, k=4, medium, Test pooled | 0.4285 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column B_det |
| Macro-F1 C, bias, k=4, medium, Test pooled | 0.3969 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column C_det |
| Macro-F1 Oracle A, bias, k=4, medium, Test pooled | 0.5284 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column A_orc_twin |
| Macro-F1 Oracle B, bias, k=4, medium, Test pooled | 0.5141 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column B_orc |
| Macro-F1 best augmented baseline, bias, k=4, medium, Test pooled | 0.4653 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=bias, level=1.0, column svm_aug |
| A minus best augmented baseline, stuck, k=1, medium, Test pooled | 0.0321 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, stuck, k=1, medium, Test pooled | 0.0287 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, stuck, k=1, medium, Test pooled | 0.5008 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column svm |
| Macro-F1 A, stuck, k=1, medium, Test pooled | 0.5422 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column A_det_twin |
| Macro-F1 B, stuck, k=1, medium, Test pooled | 0.5388 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column B_det |
| Macro-F1 C, stuck, k=1, medium, Test pooled | 0.4064 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column C_det |
| Macro-F1 Oracle A, stuck, k=1, medium, Test pooled | 0.5339 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, stuck, k=1, medium, Test pooled | 0.5354 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, stuck, k=1, medium, Test pooled | 0.5102 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=stuck, level=0.5, column svm_aug |
| A minus best augmented baseline, stuck, k=2, medium, Test pooled | 0.0164 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, stuck, k=2, medium, Test pooled | 0.0166 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, stuck, k=2, medium, Test pooled | 0.4868 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column svm |
| Macro-F1 A, stuck, k=2, medium, Test pooled | 0.5113 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column A_det_twin |
| Macro-F1 B, stuck, k=2, medium, Test pooled | 0.5115 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column B_det |
| Macro-F1 C, stuck, k=2, medium, Test pooled | 0.4031 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column C_det |
| Macro-F1 Oracle A, stuck, k=2, medium, Test pooled | 0.5365 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, stuck, k=2, medium, Test pooled | 0.5345 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, stuck, k=2, medium, Test pooled | 0.4949 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=stuck, level=0.5, column svm_aug |
| A minus best augmented baseline, stuck, k=4, medium, Test pooled | -0.0002 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, stuck, k=4, medium, Test pooled | -0.0025 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, stuck, k=4, medium, Test pooled | 0.4425 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column svm |
| Macro-F1 A, stuck, k=4, medium, Test pooled | 0.4534 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column A_det_twin |
| Macro-F1 B, stuck, k=4, medium, Test pooled | 0.4511 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column B_det |
| Macro-F1 C, stuck, k=4, medium, Test pooled | 0.3973 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column C_det |
| Macro-F1 Oracle A, stuck, k=4, medium, Test pooled | 0.5326 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, stuck, k=4, medium, Test pooled | 0.5263 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, stuck, k=4, medium, Test pooled | 0.4536 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=stuck, level=0.5, column svm_aug |
| A minus best augmented baseline, random, k=1, medium, Test pooled | 0.0532 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=random, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, random, k=1, medium, Test pooled | 0.0488 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k1, fault=random, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, random, k=1, medium, Test pooled | 0.4653 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column svm |
| Macro-F1 A, random, k=1, medium, Test pooled | 0.5426 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column A_det_twin |
| Macro-F1 B, random, k=1, medium, Test pooled | 0.5383 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column B_det |
| Macro-F1 C, random, k=1, medium, Test pooled | 0.4053 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column C_det |
| Macro-F1 Oracle A, random, k=1, medium, Test pooled | 0.5338 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, random, k=1, medium, Test pooled | 0.5355 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, random, k=1, medium, Test pooled | 0.4895 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k1, fault=random, level=0.5, column svm_aug |
| A minus best augmented baseline, random, k=2, medium, Test pooled | 0.0871 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=random, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, random, k=2, medium, Test pooled | 0.0826 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k2, fault=random, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, random, k=2, medium, Test pooled | 0.4183 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column svm |
| Macro-F1 A, random, k=2, medium, Test pooled | 0.5328 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column A_det_twin |
| Macro-F1 B, random, k=2, medium, Test pooled | 0.5284 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column B_det |
| Macro-F1 C, random, k=2, medium, Test pooled | 0.4056 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column C_det |
| Macro-F1 Oracle A, random, k=2, medium, Test pooled | 0.5364 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, random, k=2, medium, Test pooled | 0.5337 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, random, k=2, medium, Test pooled | 0.4458 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k2, fault=random, level=0.5, column svm_aug |
| A minus best augmented baseline, random, k=4, medium, Test pooled | 0.0710 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=random, level=0.5, method=A_det_twin, column diff (CI: ci_low, ci_high) |
| B minus best augmented baseline, random, k=4, medium, Test pooled | 0.0751 | results\final_test\test/ft_vs_best_aug.csv, subset=pooled, kset=k4, fault=random, level=0.5, method=B_det, column diff (CI: ci_low, ci_high) |
| Macro-F1 SVM, random, k=4, medium, Test pooled | 0.3808 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column svm |
| Macro-F1 A, random, k=4, medium, Test pooled | 0.4707 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column A_det_twin |
| Macro-F1 B, random, k=4, medium, Test pooled | 0.4748 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column B_det |
| Macro-F1 C, random, k=4, medium, Test pooled | 0.4030 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column C_det |
| Macro-F1 Oracle A, random, k=4, medium, Test pooled | 0.5324 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column A_orc_twin |
| Macro-F1 Oracle B, random, k=4, medium, Test pooled | 0.5275 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column B_orc |
| Macro-F1 best augmented baseline, random, k=4, medium, Test pooled | 0.3997 | results\final_test\test/ft_comparison.csv, subset=pooled, kset=k4, fault=random, level=0.5, column lgbm_aug |
| G3 comparisons passing, pooled | 61 of 108 | results\final_test\test/ft_verdicts.json, pooled, cells_passing / comparisons |
| G3 passing after Bonferroni, pooled | 58 | results\final_test\test/ft_verdicts.json, pooled, passing_after_bonferroni |
| G1 passes, pooled | True | results\final_test\test/ft_verdicts.json, pooled, G1.G1_passes |
| G1 drop of the best clean baseline, dropout, k=1, medium, pooled | 0.0281 | results\final_test\test/ft_verdicts.json, pooled, G1.k1_medium_mean_drop_by_fault.dropout |
| G1 drop of the best clean baseline, bias, k=1, medium, pooled | 0.0193 | results\final_test\test/ft_verdicts.json, pooled, G1.k1_medium_mean_drop_by_fault.bias |
| G1 drop of the best clean baseline, stuck, k=1, medium, pooled | 0.0346 | results\final_test\test/ft_verdicts.json, pooled, G1.k1_medium_mean_drop_by_fault.stuck |
| G1 drop of the best clean baseline, random, k=1, medium, pooled | 0.0701 | results\final_test\test/ft_verdicts.json, pooled, G1.k1_medium_mean_drop_by_fault.random |
| G3 comparisons passing, b8 | 52 of 108 | results\final_test\test/ft_verdicts.json, b8, cells_passing / comparisons |
| G3 passing after Bonferroni, b8 | 44 | results\final_test\test/ft_verdicts.json, b8, passing_after_bonferroni |
| G1 passes, b8 | True | results\final_test\test/ft_verdicts.json, b8, G1.G1_passes |
| G1 drop of the best clean baseline, dropout, k=1, medium, b8 | 0.0738 | results\final_test\test/ft_verdicts.json, b8, G1.k1_medium_mean_drop_by_fault.dropout |
| G1 drop of the best clean baseline, bias, k=1, medium, b8 | 0.0768 | results\final_test\test/ft_verdicts.json, b8, G1.k1_medium_mean_drop_by_fault.bias |
| G1 drop of the best clean baseline, stuck, k=1, medium, b8 | 0.0735 | results\final_test\test/ft_verdicts.json, b8, G1.k1_medium_mean_drop_by_fault.stuck |
| G1 drop of the best clean baseline, random, k=1, medium, b8 | 0.1701 | results\final_test\test/ft_verdicts.json, b8, G1.k1_medium_mean_drop_by_fault.random |
| G3 comparisons passing, b9 | 29 of 108 | results\final_test\test/ft_verdicts.json, b9, cells_passing / comparisons |
| G3 passing after Bonferroni, b9 | 22 | results\final_test\test/ft_verdicts.json, b9, passing_after_bonferroni |
| G1 passes, b9 | True | results\final_test\test/ft_verdicts.json, b9, G1.G1_passes |
| G1 drop of the best clean baseline, dropout, k=1, medium, b9 | 0.0351 | results\final_test\test/ft_verdicts.json, b9, G1.k1_medium_mean_drop_by_fault.dropout |
| G1 drop of the best clean baseline, bias, k=1, medium, b9 | 0.0355 | results\final_test\test/ft_verdicts.json, b9, G1.k1_medium_mean_drop_by_fault.bias |
| G1 drop of the best clean baseline, stuck, k=1, medium, b9 | 0.0409 | results\final_test\test/ft_verdicts.json, b9, G1.k1_medium_mean_drop_by_fault.stuck |
| G1 drop of the best clean baseline, random, k=1, medium, b9 | 0.0904 | results\final_test\test/ft_verdicts.json, b9, G1.k1_medium_mean_drop_by_fault.random |
| G3 comparisons passing, b10 | 70 of 108 | results\final_test\test/ft_verdicts.json, b10, cells_passing / comparisons |
| G3 passing after Bonferroni, b10 | 64 | results\final_test\test/ft_verdicts.json, b10, passing_after_bonferroni |
| G1 passes, b10 | False | results\final_test\test/ft_verdicts.json, b10, G1.G1_passes |
| G1 drop of the best clean baseline, dropout, k=1, medium, b10 | 0.0195 | results\final_test\test/ft_verdicts.json, b10, G1.k1_medium_mean_drop_by_fault.dropout |
| G1 drop of the best clean baseline, bias, k=1, medium, b10 | 0.0225 | results\final_test\test/ft_verdicts.json, b10, G1.k1_medium_mean_drop_by_fault.bias |
| G1 drop of the best clean baseline, stuck, k=1, medium, b10 | 0.0153 | results\final_test\test/ft_verdicts.json, b10, G1.k1_medium_mean_drop_by_fault.stuck |
| G1 drop of the best clean baseline, random, k=1, medium, b10 | 0.0231 | results\final_test\test/ft_verdicts.json, b10, G1.k1_medium_mean_drop_by_fault.random |
| Detector isolation AUROC, dropout, Validation | 1.0000 | results\overnight\temporal/g2_verdict.json, isolation_auroc_by_fault_k1_medium.dropout |
| Detector isolation AUROC, dropout, Test pooled | 1.0000 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.median.by_fault.dropout |
| Detector isolation AUROC, dropout, Test b8 | 1.0000 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.median.by_fault.dropout |
| Detector isolation AUROC, dropout, Test b9 | 1.0000 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.median.by_fault.dropout |
| Detector isolation AUROC, dropout, Test b10 | 1.0000 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.median.by_fault.dropout |
| Detector isolation AUROC, bias, Validation | 0.9797 | results\overnight\temporal/g2_verdict.json, isolation_auroc_by_fault_k1_medium.bias |
| Detector isolation AUROC, bias, Test pooled | 0.9779 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.median.by_fault.bias |
| Detector isolation AUROC, bias, Test b8 | 0.9730 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.median.by_fault.bias |
| Detector isolation AUROC, bias, Test b9 | 0.9907 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.median.by_fault.bias |
| Detector isolation AUROC, bias, Test b10 | 0.9771 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.median.by_fault.bias |
| Detector isolation AUROC, stuck, Validation | 0.9373 | results\overnight\temporal/g2_verdict.json, isolation_auroc_by_fault_k1_medium.stuck |
| Detector isolation AUROC, stuck, Test pooled | 0.9484 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.median.by_fault.stuck |
| Detector isolation AUROC, stuck, Test b8 | 0.9060 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.median.by_fault.stuck |
| Detector isolation AUROC, stuck, Test b9 | 0.9633 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.median.by_fault.stuck |
| Detector isolation AUROC, stuck, Test b10 | 0.9501 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.median.by_fault.stuck |
| Detector isolation AUROC, random, Validation | 0.9744 | results\overnight\temporal/g2_verdict.json, isolation_auroc_by_fault_k1_medium.random |
| Detector isolation AUROC, random, Test pooled | 0.9793 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.median.by_fault.random |
| Detector isolation AUROC, random, Test b8 | 0.9583 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.median.by_fault.random |
| Detector isolation AUROC, random, Test b9 | 0.9861 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.median.by_fault.random |
| Detector isolation AUROC, random, Test b10 | 0.9807 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.median.by_fault.random |
| G2 median isolation AUROC, Validation | 0.9770 | results\overnight\temporal/g2_verdict.json, median_auroc |
| G2 median isolation AUROC, Test pooled | 0.9786 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.median.median_auroc |
| G2 passes, Test pooled | True | results\final_test\test/ft_g2_by_subset.json, pooled, G2_passes |
| G2 median AUROC of the sensitivity detector sensor, Test pooled | 0.9548 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.sensor.median_auroc |
| G2 median AUROC of the sensitivity detector sensor_lpo, Test pooled | 0.9531 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.sensor_lpo.median_auroc |
| G2 median AUROC of the sensitivity detector median_lpo, Test pooled | 0.9662 | results\final_test\test/ft_g2_by_subset.json, pooled, detectors.median_lpo.median_auroc |
| G2 median isolation AUROC, Test b8 | 0.9657 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.median.median_auroc |
| G2 passes, Test b8 | True | results\final_test\test/ft_g2_by_subset.json, b8, G2_passes |
| G2 median AUROC of the sensitivity detector sensor, Test b8 | 0.9641 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.sensor.median_auroc |
| G2 median AUROC of the sensitivity detector sensor_lpo, Test b8 | 0.9681 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.sensor_lpo.median_auroc |
| G2 median AUROC of the sensitivity detector median_lpo, Test b8 | 0.9595 | results\final_test\test/ft_g2_by_subset.json, b8, detectors.median_lpo.median_auroc |
| G2 median isolation AUROC, Test b9 | 0.9884 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.median.median_auroc |
| G2 passes, Test b9 | True | results\final_test\test/ft_g2_by_subset.json, b9, G2_passes |
| G2 median AUROC of the sensitivity detector sensor, Test b9 | 0.9846 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.sensor.median_auroc |
| G2 median AUROC of the sensitivity detector sensor_lpo, Test b9 | 0.9892 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.sensor_lpo.median_auroc |
| G2 median AUROC of the sensitivity detector median_lpo, Test b9 | 0.9863 | results\final_test\test/ft_g2_by_subset.json, b9, detectors.median_lpo.median_auroc |
| G2 median isolation AUROC, Test b10 | 0.9789 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.median.median_auroc |
| G2 passes, Test b10 | True | results\final_test\test/ft_g2_by_subset.json, b10, G2_passes |
| G2 median AUROC of the sensitivity detector sensor, Test b10 | 0.9518 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.sensor.median_auroc |
| G2 median AUROC of the sensitivity detector sensor_lpo, Test b10 | 0.9478 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.sensor_lpo.median_auroc |
| G2 median AUROC of the sensitivity detector median_lpo, Test b10 | 0.9647 | results\final_test\test/ft_g2_by_subset.json, b10, detectors.median_lpo.median_auroc |
| False-alarm rate per sensor-row, all, all sensors, Validation | 0.1347 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=all, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, all sensors, Test pooled | 0.0783 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=all, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, all sensors, Test b8 | 0.1518 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=all, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, all sensors, Test b9 | 0.0670 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=all, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, all sensors, Test b10 | 0.0738 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=all, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, without S01,S02, Validation | 0.0322 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=all, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, without S01,S02, Test pooled | 0.0455 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=all, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, without S01,S02, Test b8 | 0.0318 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=all, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, without S01,S02, Test b9 | 0.0505 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=all, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, all, without S01,S02, Test b10 | 0.0460 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=all, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, all sensors, Validation | 0.1406 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Acetaldehyde, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, all sensors, Test pooled | 0.0891 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Acetaldehyde, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, all sensors, Test b8 | 0.1515 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Acetaldehyde, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, all sensors, Test b9 | 0.1233 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Acetaldehyde, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, all sensors, Test b10 | 0.0814 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Acetaldehyde, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, without S01,S02, Validation | 0.0358 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Acetaldehyde, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, without S01,S02, Test pooled | 0.0455 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Acetaldehyde, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, without S01,S02, Test b8 | 0.0303 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Acetaldehyde, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, without S01,S02, Test b9 | 0.0562 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Acetaldehyde, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetaldehyde, without S01,S02, Test b10 | 0.0450 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Acetaldehyde, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, all sensors, Validation | 0.1469 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Acetone, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, all sensors, Test pooled | 0.1132 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Acetone, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, all sensors, Test b8 | 0.1469 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Acetone, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, all sensors, Test b9 | 0.1026 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Acetone, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, all sensors, Test b10 | 0.1066 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Acetone, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, without S01,S02, Validation | 0.0406 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Acetone, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, without S01,S02, Test pooled | 0.0566 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Acetone, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, without S01,S02, Test b8 | 0.0255 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Acetone, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, without S01,S02, Test b9 | 0.0595 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Acetone, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Acetone, without S01,S02, Test b10 | 0.0636 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Acetone, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, all sensors, Validation | 0.1158 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Ammonia, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, all sensors, Test pooled | 0.0829 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Ammonia, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, all sensors, Test b8 | 0.1641 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Ammonia, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, all sensors, Test b9 | 0.0069 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Ammonia, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, all sensors, Test b10 | 0.0902 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Ammonia, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, without S01,S02, Validation | 0.0163 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Ammonia, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, without S01,S02, Test pooled | 0.0505 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Ammonia, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, without S01,S02, Test b8 | 0.0446 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Ammonia, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, without S01,S02, Test b9 | 0.0071 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Ammonia, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ammonia, without S01,S02, Test b10 | 0.0581 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Ammonia, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, all sensors, Validation | 0.1418 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Ethanol, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, all sensors, Test pooled | 0.0349 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Ethanol, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, all sensors, Test b8 | 0.1479 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Ethanol, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, all sensors, Test b9 | 0.0809 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Ethanol, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, all sensors, Test b10 | 0.0246 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Ethanol, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, without S01,S02, Validation | 0.0517 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Ethanol, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, without S01,S02, Test pooled | 0.0277 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Ethanol, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, without S01,S02, Test b8 | 0.0262 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Ethanol, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, without S01,S02, Test b9 | 0.0902 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Ethanol, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethanol, without S01,S02, Test b10 | 0.0214 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Ethanol, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, all sensors, Validation | 0.1175 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Ethylene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, all sensors, Test pooled | 0.0672 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Ethylene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, all sensors, Test b8 | 0.1333 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Ethylene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, all sensors, Test b9 | 0.0386 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Ethylene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, all sensors, Test b10 | 0.0666 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Ethylene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, without S01,S02, Validation | 0.0244 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Ethylene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, without S01,S02, Test pooled | 0.0287 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Ethylene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, without S01,S02, Test b8 | 0.0190 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Ethylene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, without S01,S02, Test b9 | 0.0429 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Ethylene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Ethylene, without S01,S02, Test b10 | 0.0279 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Ethylene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, all sensors, Validation | 0.1375 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Toluene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, all sensors, Test pooled | 0.0753 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Toluene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, all sensors, Test b8 | 0.2014 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Toluene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, all sensors, Test b9 | 0.0644 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Toluene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, all sensors, Test b10 | 0.0733 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Toluene, sensors=all sensors, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, without S01,S02, Validation | 0.0151 | results\overnight\temporal/far_by_gas.csv, detector=median, gas=Toluene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, without S01,S02, Test pooled | 0.0609 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=pooled, gas=Toluene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, without S01,S02, Test b8 | 0.0873 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b8, gas=Toluene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, without S01,S02, Test b9 | 0.0622 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b9, gas=Toluene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| False-alarm rate per sensor-row, Toluene, without S01,S02, Test b10 | 0.0599 | results\final_test\test/ft_far_by_gas.csv, detector=median, subset=b10, gas=Toluene, sensors=without S01,S02, column alarm_rate_per_sensor_row |
| Reliability rank 1 (least reliable first), Test pooled: sensor S01 alarm rate | 0.5023 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=pooled, rank=1, column alarm_rate |
| Reliability rank 2 (least reliable first), Test pooled: sensor S08 alarm rate | 0.2713 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=pooled, rank=2, column alarm_rate |
| Reliability rank 3 (least reliable first), Test pooled: sensor S07 alarm rate | 0.0357 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=pooled, rank=3, column alarm_rate |
| Reliability rank 1 (least reliable first), Test b8: sensor S01 alarm rate | 1.0000 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b8, rank=1, column alarm_rate |
| Reliability rank 2 (least reliable first), Test b8: sensor S02 alarm rate | 0.9830 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b8, rank=2, column alarm_rate |
| Reliability rank 3 (least reliable first), Test b8: sensor S12 alarm rate | 0.0782 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b8, rank=3, column alarm_rate |
| Reliability rank 1 (least reliable first), Test b9: sensor S08 alarm rate | 0.2872 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b9, rank=1, column alarm_rate |
| Reliability rank 2 (least reliable first), Test b9: sensor S16 alarm rate | 0.0787 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b9, rank=2, column alarm_rate |
| Reliability rank 3 (least reliable first), Test b9: sensor S01 alarm rate | 0.1255 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b9, rank=3, column alarm_rate |
| Reliability rank 1 (least reliable first), Test b10: sensor S01 alarm rate | 0.5108 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b10, rank=1, column alarm_rate |
| Reliability rank 2 (least reliable first), Test b10: sensor S08 alarm rate | 0.2886 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b10, rank=2, column alarm_rate |
| Reliability rank 3 (least reliable first), Test b10: sensor S07 alarm rate | 0.0339 | results\final_test\test/ft_reliability_ranking.csv, detector=median, subset=b10, rank=3, column alarm_rate |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/raw, twin available, reference protocol | 0.9427 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/raw, twin available, temporal protocol | 0.7729 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), knn/raw, twin available | 0.1698 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/raw, twin available, reference | 0.9785 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/raw, twin available, temporal | 0.9149 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), knn/raw, twin available | 0.0636 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/raw, twin missing, reference protocol | 0.9409 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/raw, twin missing, temporal protocol | 0.7613 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), knn/raw, twin missing | 0.1796 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/raw, twin missing, reference | 0.9727 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/raw, twin missing, temporal | 0.9089 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), knn/raw, twin missing | 0.0638 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/slog, twin available, reference protocol | 0.9375 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/slog, twin available, temporal protocol | 0.7518 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), knn/slog, twin available | 0.1858 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/slog, twin available, reference | 0.9733 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/slog, twin available, temporal | 0.9054 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), knn/slog, twin available | 0.0679 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/slog, twin missing, reference protocol | 0.9354 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), knn/slog, twin missing, temporal protocol | 0.7364 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), knn/slog, twin missing | 0.1990 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/slog, twin missing, reference | 0.9696 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, knn/slog, twin missing, temporal | 0.8932 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), knn/slog, twin missing | 0.0764 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/raw, twin available, reference protocol | 0.9228 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/raw, twin available, temporal protocol | 0.8881 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), ridge/raw, twin available | 0.0347 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/raw, twin available, reference | 0.9800 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/raw, twin available, temporal | 0.9639 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), ridge/raw, twin available | 0.0161 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/raw, twin missing, reference protocol | 0.8565 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/raw, twin missing, temporal protocol | 0.7859 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), ridge/raw, twin missing | 0.0706 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/raw, twin missing, reference | 0.9517 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/raw, twin missing, temporal | 0.9007 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), ridge/raw, twin missing | 0.0511 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/slog, twin available, reference protocol | 0.9437 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/slog, twin available, temporal protocol | 0.9093 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), ridge/slog, twin available | 0.0344 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/slog, twin available, reference | 0.9844 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/slog, twin available, temporal | 0.9812 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), ridge/slog, twin available | 0.0033 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/slog, twin missing, reference protocol | 0.9003 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Reconstruction skill (1 - MAE/MAE_median, median over sensors), ridge/slog, twin missing, temporal protocol | 0.8381 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost of reconstruction (skill_reference - skill_temporal; positive = the method loses its advantage over median imputation under drift), ridge/slog, twin missing | 0.0623 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/slog, twin missing, reference | 0.9696 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Median R2 over sensors, ridge/slog, twin missing, temporal | 0.9560 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Drift cost in R2 (R2_reference - R2_temporal), ridge/slog, twin missing | 0.0136 | results/preprocessing/phase1/{temporal,reference_iid}/reconstruction_per_sensor.csv, scripts/ft_paper.py skill_table() |
| Detector alarm rate of S01 on clean rows, batch 1 | 0.0112 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=1, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 2 | 0.0829 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=2, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 3 | 0.0025 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=3, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 4 | 0.0000 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=4, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 5 | 0.0000 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=5, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 6 | 0.0804 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=6, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 8 | 1.0000 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=8, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 9 | 0.1255 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=9, column alarm_rate |
| Detector alarm rate of S01 on clean rows, batch 10 | 0.5108 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S01, batch=10, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 1 | 0.0000 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=1, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 2 | 0.0161 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=2, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 3 | 0.1274 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=3, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 4 | 0.0745 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=4, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 5 | 0.0000 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=5, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 6 | 0.0274 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=6, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 8 | 0.9830 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=8, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 9 | 0.2404 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=9, column alarm_rate |
| Detector alarm rate of S02 on clean rows, batch 10 | 0.0258 | results\final_test\test/sensor_alarm_rate_by_batch.csv, sensor=S02, batch=10, column alarm_rate |
| S01-S02 Spearman correlation, batch 1 | 0.9905 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=1, column spearman |
| S01-S02 median offset, batch 1 | 0.0889 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=1, column median_offset |
| S01-S02 Spearman correlation, batch 2 | 0.9880 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=2, column spearman |
| S01-S02 median offset, batch 2 | 0.1096 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=2, column median_offset |
| S01-S02 Spearman correlation, batch 3 | 0.9926 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=3, column spearman |
| S01-S02 median offset, batch 3 | 0.0711 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=3, column median_offset |
| S01-S02 Spearman correlation, batch 4 | 0.9934 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=4, column spearman |
| S01-S02 median offset, batch 4 | -0.0006 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=4, column median_offset |
| S01-S02 Spearman correlation, batch 5 | 0.9786 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=5, column spearman |
| S01-S02 median offset, batch 5 | 0.1067 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=5, column median_offset |
| S01-S02 Spearman correlation, batch 6 | 0.9516 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=6, column spearman |
| S01-S02 median offset, batch 6 | 0.0417 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=6, column median_offset |
| S01-S02 Spearman correlation, batch 8 | 0.4046 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=8, column spearman |
| S01-S02 median offset, batch 8 | -0.5909 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=8, column median_offset |
| S01-S02 Spearman correlation, batch 9 | 0.8591 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=9, column spearman |
| S01-S02 median offset, batch 9 | -0.1708 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=9, column median_offset |
| S01-S02 Spearman correlation, batch 10 | 0.9370 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=10, column spearman |
| S01-S02 median offset, batch 10 | -0.0701 | results\final_test\test/pair_consistency_by_batch_all.csv, pair=S01-S02, batch=10, column median_offset |
| Bundle size of pipeline A (KB) | 797.7910 | results\edge_cost\edge_cost.json, bundle_kb |
| Latency median, fault_free (ms) | 5.7043 | results\edge_cost\edge_cost.json, fault_free.median_ms |
| Latency p95, fault_free (ms) | 10.0487 | results\edge_cost\edge_cost.json, fault_free.p95_ms |
| Latency median, bias_one_sensor (ms) | 6.1055 | results\edge_cost\edge_cost.json, bias_one_sensor.median_ms |
| Latency p95, bias_one_sensor (ms) | 10.3575 | results\edge_cost\edge_cost.json, bias_one_sensor.p95_ms |
| Latency median, bias_one_sensor_cold_weights (ms) | 7.9862 | results\edge_cost\edge_cost.json, bias_one_sensor_cold_weights.median_ms |
| Latency p95, bias_one_sensor_cold_weights (ms) | 14.5539 | results\edge_cost\edge_cost.json, bias_one_sensor_cold_weights.p95_ms |
| Peak memory (MB) | 146.7734 | results\edge_cost\edge_cost.json, memory_peak_mb |


## v2 post-hoc

SEPARATE SETTING: 'with 10 labeled calibration samples per gas' (few-shot recalibration). POST-HOC and test-informed design (decisions_log G0, J0, N0); single Test run at tag `frozen-before-test-v2`. Train = batches 1-7, so (a) is NOT the v1 model; do not compare these numbers with the v1 numbers above. Calibration rows are interleaved in time with the scored rows (optimistic, N9).

| quantity | value | source |
|---|---|---|
| v2 clean Macro-F1 SVM, b10, (a) no calibration | 0.6743 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, b10, (b) 10 per gas (mean of 5 seeds) | 0.8183 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, b8, (a) no calibration | 0.8994 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, b8, (b) 10 per gas (mean of 5 seeds) | 0.9391 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, b9, (a) no calibration | 0.736 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, b9, (b) 10 per gas (mean of 5 seeds) | 0.9806 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, pooled, (a) no calibration | 0.7056 | results/final_test_v2/test/clean.csv |
| v2 clean Macro-F1 SVM, pooled, (b) 10 per gas (mean of 5 seeds) | 0.8418 | results/final_test_v2/test/clean.csv |
| v2 clean (b)-(a) SVM, b10, diff [95% CI] | 0.1440 [0.1384, 0.1495] | results/final_test_v2/test/clean_ci.csv |
| v2 clean (b)-(a) SVM, b8, diff [95% CI] | 0.0397 [0.0264, 0.0597] | results/final_test_v2/test/clean_ci.csv |
| v2 clean (b)-(a) SVM, b9, diff [95% CI] | 0.2446 [0.2372, 0.2531] | results/final_test_v2/test/clean_ci.csv |
| v2 clean (b)-(a) SVM, pooled, diff [95% CI] | 0.1362 [0.1315, 0.1413] | results/final_test_v2/test/clean_ci.csv |
| v2 pooled A, model (a): mean under faults / worst / retained | 0.6549 / 0.1146 / 0.9630 | results/final_test_v2/test/faults.csv |
| v2 pooled B, model (a): mean under faults / worst / retained | 0.6608 / 0.2626 / 0.9565 | results/final_test_v2/test/faults.csv |
| v2 pooled svm, model (a): mean under faults / worst / retained | 0.5441 / 0.1370 / 0.7899 | results/final_test_v2/test/faults.csv |
| v2 pooled A, model (b): mean under faults / worst / retained | 0.7912 / 0.1370 / 0.9686 | results/final_test_v2/test/faults.csv |
| v2 pooled B, model (b): mean under faults / worst / retained | 0.8094 / 0.3360 / 0.9734 | results/final_test_v2/test/faults.csv |
| v2 pooled svm, model (b): mean under faults / worst / retained | 0.6637 / 0.1691 / 0.8079 | results/final_test_v2/test/faults.csv |
| v2 pooled (b)-(a) svm under faults [95% CI] | 0.1196 [0.1185, 0.1207] | results/final_test_v2/test/faults_ci.csv |
| v2 pooled (b)-(a) A under faults [95% CI] | 0.1363 [0.1351, 0.1376] | results/final_test_v2/test/faults_ci.csv |
| v2 pooled (b)-(a) B under faults [95% CI] | 0.1486 [0.1477, 0.1495] | results/final_test_v2/test/faults_ci.csv |
| v2 pooled A-SVM under faults, model (a) [95% CI] | 0.1108 [0.1072, 0.1147] | results/final_test_v2/test/faults_ci.csv |
| v2 pooled A-SVM under faults, model (b) [95% CI] | 0.1275 [0.1231, 0.1318] | results/final_test_v2/test/faults_ci.csv |
| v2 verdict N8 (success) | True | results/final_test_v2/test/verdict.json |
