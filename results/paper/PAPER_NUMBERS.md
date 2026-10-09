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

SEPARATE SETTING: 'with 10 labeled calibration samples per gas' (few-shot recalibration). POST-HOC and test-informed design (decisions_log G0, J0, N0); single Test run at tag `frozen-before-test-v2`. Train = batches 1-7, so (a) is NOT the v1 model; do not compare these numbers with the v1 numbers above. Calibration rows are interleaved in time with the scored rows (optimistic, N9). Generated by scripts/v2_paper.py.

| number | value | source |
|---|---|---|
| v2 clean Macro-F1 A, b10, (a) no calibration | 0.6565 | results/final_test_v2/test/clean.csv, subset=b10, method=A, column a |
| v2 clean Macro-F1 A, b10, (b) 10 per gas, mean of 5 seeds | 0.8014 | results/final_test_v2/test/clean.csv, subset=b10, method=A, column b |
| v2 clean Macro-F1 B, b10, (a) no calibration | 0.6657 | results/final_test_v2/test/clean.csv, subset=b10, method=B, column a |
| v2 clean Macro-F1 B, b10, (b) 10 per gas, mean of 5 seeds | 0.8143 | results/final_test_v2/test/clean.csv, subset=b10, method=B, column b |
| v2 clean Macro-F1 SVM, b10, (a) no calibration | 0.6743 | results/final_test_v2/test/clean.csv, subset=b10, method=svm, column a |
| v2 clean Macro-F1 SVM, b10, (b) 10 per gas, mean of 5 seeds | 0.8183 | results/final_test_v2/test/clean.csv, subset=b10, method=svm, column b |
| v2 clean Macro-F1 A, b8, (a) no calibration | 0.8491 | results/final_test_v2/test/clean.csv, subset=b8, method=A, column a |
| v2 clean Macro-F1 A, b8, (b) 10 per gas, mean of 5 seeds | 0.8628 | results/final_test_v2/test/clean.csv, subset=b8, method=A, column b |
| v2 clean Macro-F1 B, b8, (a) no calibration | 0.9183 | results/final_test_v2/test/clean.csv, subset=b8, method=B, column a |
| v2 clean Macro-F1 B, b8, (b) 10 per gas, mean of 5 seeds | 0.9587 | results/final_test_v2/test/clean.csv, subset=b8, method=B, column b |
| v2 clean Macro-F1 SVM, b8, (a) no calibration | 0.8994 | results/final_test_v2/test/clean.csv, subset=b8, method=svm, column a |
| v2 clean Macro-F1 SVM, b8, (b) 10 per gas, mean of 5 seeds | 0.9391 | results/final_test_v2/test/clean.csv, subset=b8, method=svm, column b |
| v2 clean Macro-F1 A, b9, (a) no calibration | 0.7544 | results/final_test_v2/test/clean.csv, subset=b9, method=A, column a |
| v2 clean Macro-F1 A, b9, (b) 10 per gas, mean of 5 seeds | 0.9965 | results/final_test_v2/test/clean.csv, subset=b9, method=A, column b |
| v2 clean Macro-F1 B, b9, (a) no calibration | 0.7548 | results/final_test_v2/test/clean.csv, subset=b9, method=B, column a |
| v2 clean Macro-F1 B, b9, (b) 10 per gas, mean of 5 seeds | 0.9970 | results/final_test_v2/test/clean.csv, subset=b9, method=B, column b |
| v2 clean Macro-F1 SVM, b9, (a) no calibration | 0.7360 | results/final_test_v2/test/clean.csv, subset=b9, method=svm, column a |
| v2 clean Macro-F1 SVM, b9, (b) 10 per gas, mean of 5 seeds | 0.9806 | results/final_test_v2/test/clean.csv, subset=b9, method=svm, column b |
| v2 clean Macro-F1 A, pooled, (a) no calibration | 0.6922 | results/final_test_v2/test/clean.csv, subset=pooled, method=A, column a |
| v2 clean Macro-F1 A, pooled, (b) 10 per gas, mean of 5 seeds | 0.8281 | results/final_test_v2/test/clean.csv, subset=pooled, method=A, column b |
| v2 clean Macro-F1 B, pooled, (a) no calibration | 0.7005 | results/final_test_v2/test/clean.csv, subset=pooled, method=B, column a |
| v2 clean Macro-F1 B, pooled, (b) 10 per gas, mean of 5 seeds | 0.8402 | results/final_test_v2/test/clean.csv, subset=pooled, method=B, column b |
| v2 clean Macro-F1 SVM, pooled, (a) no calibration | 0.7056 | results/final_test_v2/test/clean.csv, subset=pooled, method=svm, column a |
| v2 clean Macro-F1 SVM, pooled, (b) 10 per gas, mean of 5 seeds | 0.8418 | results/final_test_v2/test/clean.csv, subset=pooled, method=svm, column b |
| v2 clean gain (b)-(a) SVM, b10, diff | 0.1440 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=svm, column diff |
| v2 clean gain (b)-(a) SVM, b10, ci_low [superseded: v2 corrected CIs] | 0.1384 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=svm, column ci_low |
| v2 clean gain (b)-(a) SVM, b10, ci_high [superseded: v2 corrected CIs] | 0.1495 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=svm, column ci_high |
| v2 clean gain (b)-(a) A, b10, diff | 0.1449 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=A, column diff |
| v2 clean gain (b)-(a) A, b10, ci_low [superseded: v2 corrected CIs] | 0.1391 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=A, column ci_low |
| v2 clean gain (b)-(a) A, b10, ci_high [superseded: v2 corrected CIs] | 0.1509 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=A, column ci_high |
| v2 clean gain (b)-(a) B, b10, diff | 0.1486 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=B, column diff |
| v2 clean gain (b)-(a) B, b10, ci_low [superseded: v2 corrected CIs] | 0.1431 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=B, column ci_low |
| v2 clean gain (b)-(a) B, b10, ci_high [superseded: v2 corrected CIs] | 0.1544 | results/final_test_v2/test/clean_ci.csv, subset=b10, method=B, column ci_high |
| v2 clean gain (b)-(a) SVM, b8, diff | 0.0397 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=svm, column diff |
| v2 clean gain (b)-(a) SVM, b8, ci_low [superseded: v2 corrected CIs] | 0.0264 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=svm, column ci_low |
| v2 clean gain (b)-(a) SVM, b8, ci_high [superseded: v2 corrected CIs] | 0.0597 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=svm, column ci_high |
| v2 clean gain (b)-(a) A, b8, diff | 0.0137 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=A, column diff |
| v2 clean gain (b)-(a) A, b8, ci_low [superseded: v2 corrected CIs] | -0.0131 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=A, column ci_low |
| v2 clean gain (b)-(a) A, b8, ci_high [superseded: v2 corrected CIs] | 0.0417 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=A, column ci_high |
| v2 clean gain (b)-(a) B, b8, diff | 0.0403 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=B, column diff |
| v2 clean gain (b)-(a) B, b8, ci_low [superseded: v2 corrected CIs] | 0.0239 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=B, column ci_low |
| v2 clean gain (b)-(a) B, b8, ci_high [superseded: v2 corrected CIs] | 0.0654 | results/final_test_v2/test/clean_ci.csv, subset=b8, method=B, column ci_high |
| v2 clean gain (b)-(a) SVM, b9, diff | 0.2446 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=svm, column diff |
| v2 clean gain (b)-(a) SVM, b9, ci_low [superseded: v2 corrected CIs] | 0.2372 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=svm, column ci_low |
| v2 clean gain (b)-(a) SVM, b9, ci_high [superseded: v2 corrected CIs] | 0.2531 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=svm, column ci_high |
| v2 clean gain (b)-(a) A, b9, diff | 0.2421 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=A, column diff |
| v2 clean gain (b)-(a) A, b9, ci_low [superseded: v2 corrected CIs] | 0.2354 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=A, column ci_low |
| v2 clean gain (b)-(a) A, b9, ci_high [superseded: v2 corrected CIs] | 0.2499 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=A, column ci_high |
| v2 clean gain (b)-(a) B, b9, diff | 0.2421 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=B, column diff |
| v2 clean gain (b)-(a) B, b9, ci_low [superseded: v2 corrected CIs] | 0.2357 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=B, column ci_low |
| v2 clean gain (b)-(a) B, b9, ci_high [superseded: v2 corrected CIs] | 0.2496 | results/final_test_v2/test/clean_ci.csv, subset=b9, method=B, column ci_high |
| v2 clean gain (b)-(a) SVM, pooled, diff | 0.1362 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=svm, column diff |
| v2 clean gain (b)-(a) SVM, pooled, ci_low [superseded: v2 corrected CIs] | 0.1315 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=svm, column ci_low |
| v2 clean gain (b)-(a) SVM, pooled, ci_high [superseded: v2 corrected CIs] | 0.1413 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=svm, column ci_high |
| v2 clean gain (b)-(a) A, pooled, diff | 0.1359 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=A, column diff |
| v2 clean gain (b)-(a) A, pooled, ci_low [superseded: v2 corrected CIs] | 0.1310 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=A, column ci_low |
| v2 clean gain (b)-(a) A, pooled, ci_high [superseded: v2 corrected CIs] | 0.1411 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=A, column ci_high |
| v2 clean gain (b)-(a) B, pooled, diff | 0.1397 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=B, column diff |
| v2 clean gain (b)-(a) B, pooled, ci_low [superseded: v2 corrected CIs] | 0.1348 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=B, column ci_low |
| v2 clean gain (b)-(a) B, pooled, ci_high [superseded: v2 corrected CIs] | 0.1450 | results/final_test_v2/test/clean_ci.csv, subset=pooled, method=B, column ci_high |
| v2 mean_under_faults A, model (a), b10 | 0.6211 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=A, column mean_under_faults |
| v2 k1 A, model (a), b10 | 0.6564 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=A, column k1 |
| v2 k2 A, model (a), b10 | 0.5859 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=A, column k2 |
| v2 worst A, model (a), b10 | 0.0596 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=A, column worst |
| v2 retained A, model (a), b10 | 0.9640 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=A, column retained |
| v2 mean_under_faults B, model (a), b10 | 0.6287 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=B, column mean_under_faults |
| v2 k1 B, model (a), b10 | 0.6573 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=B, column k1 |
| v2 k2 B, model (a), b10 | 0.6002 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=B, column k2 |
| v2 worst B, model (a), b10 | 0.1458 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=B, column worst |
| v2 retained B, model (a), b10 | 0.9587 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=B, column retained |
| v2 mean_under_faults SVM, model (a), b10 | 0.5121 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=svm, column mean_under_faults |
| v2 k1 SVM, model (a), b10 | 0.5508 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=svm, column k1 |
| v2 k2 SVM, model (a), b10 | 0.4734 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=svm, column k2 |
| v2 worst SVM, model (a), b10 | 0.0297 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=svm, column worst |
| v2 retained SVM, model (a), b10 | 0.7786 | results/final_test_v2/test/faults.csv, subset=b10, model=a, method=svm, column retained |
| v2 mean_under_faults A, model (b), b10 | 0.7653 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=A, column mean_under_faults |
| v2 k1 A, model (b), b10 | 0.7970 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=A, column k1 |
| v2 k2 A, model (b), b10 | 0.7336 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=A, column k2 |
| v2 worst A, model (b), b10 | 0.0721 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=A, column worst |
| v2 retained A, model (b), b10 | 0.9682 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=A, column retained |
| v2 mean_under_faults B, model (b), b10 | 0.7843 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=B, column mean_under_faults |
| v2 k1 B, model (b), b10 | 0.8099 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=B, column k1 |
| v2 k2 B, model (b), b10 | 0.7587 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=B, column k2 |
| v2 worst B, model (b), b10 | 0.1743 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=B, column worst |
| v2 retained B, model (b), b10 | 0.9737 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=B, column retained |
| v2 mean_under_faults SVM, model (b), b10 | 0.6415 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=svm, column mean_under_faults |
| v2 k1 SVM, model (b), b10 | 0.6891 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=svm, column k1 |
| v2 k2 SVM, model (b), b10 | 0.5938 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=svm, column k2 |
| v2 worst SVM, model (b), b10 | 0.0440 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=svm, column worst |
| v2 retained SVM, model (b), b10 | 0.8034 | results/final_test_v2/test/faults.csv, subset=b10, model=b, method=svm, column retained |
| v2 mean_under_faults A, model (a), b8 | 0.8409 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=A, column mean_under_faults |
| v2 k1 A, model (a), b8 | 0.8860 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=A, column k1 |
| v2 k2 A, model (a), b8 | 0.7959 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=A, column k2 |
| v2 worst A, model (a), b8 | 0.0297 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=A, column worst |
| v2 retained A, model (a), b8 | 1.0090 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=A, column retained |
| v2 mean_under_faults B, model (a), b8 | 0.8733 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=B, column mean_under_faults |
| v2 k1 B, model (a), b8 | 0.9122 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=B, column k1 |
| v2 k2 B, model (a), b8 | 0.8344 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=B, column k2 |
| v2 worst B, model (a), b8 | 0.3135 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=B, column worst |
| v2 retained B, model (a), b8 | 0.9651 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=B, column retained |
| v2 mean_under_faults SVM, model (a), b8 | 0.6941 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=svm, column mean_under_faults |
| v2 k1 SVM, model (a), b8 | 0.7481 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=svm, column k1 |
| v2 k2 SVM, model (a), b8 | 0.6401 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=svm, column k2 |
| v2 worst SVM, model (a), b8 | 0.0985 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=svm, column worst |
| v2 retained SVM, model (a), b8 | 0.7919 | results/final_test_v2/test/faults.csv, subset=b8, model=a, method=svm, column retained |
| v2 mean_under_faults A, model (b), b8 | 0.8764 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=A, column mean_under_faults |
| v2 k1 A, model (b), b8 | 0.9181 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=A, column k1 |
| v2 k2 A, model (b), b8 | 0.8347 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=A, column k2 |
| v2 worst A, model (b), b8 | 0.0297 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=A, column worst |
| v2 retained A, model (b), b8 | 1.0321 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=A, column retained |
| v2 mean_under_faults B, model (b), b8 | 0.9192 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=B, column mean_under_faults |
| v2 k1 B, model (b), b8 | 0.9503 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=B, column k1 |
| v2 k2 B, model (b), b8 | 0.8880 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=B, column k2 |
| v2 worst B, model (b), b8 | 0.3807 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=B, column worst |
| v2 retained B, model (b), b8 | 0.9696 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=B, column retained |
| v2 mean_under_faults SVM, model (b), b8 | 0.7423 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=svm, column mean_under_faults |
| v2 k1 SVM, model (b), b8 | 0.7974 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=svm, column k1 |
| v2 k2 SVM, model (b), b8 | 0.6873 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=svm, column k2 |
| v2 worst SVM, model (b), b8 | 0.0953 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=svm, column worst |
| v2 retained SVM, model (b), b8 | 0.8101 | results/final_test_v2/test/faults.csv, subset=b8, model=b, method=svm, column retained |
| v2 mean_under_faults A, model (a), b9 | 0.7059 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=A, column mean_under_faults |
| v2 k1 A, model (a), b9 | 0.7377 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=A, column k1 |
| v2 k2 A, model (a), b9 | 0.6741 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=A, column k2 |
| v2 worst A, model (a), b9 | 0.0372 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=A, column worst |
| v2 retained A, model (a), b9 | 0.9498 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=A, column retained |
| v2 mean_under_faults B, model (a), b9 | 0.7041 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=B, column mean_under_faults |
| v2 k1 B, model (a), b9 | 0.7239 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=B, column k1 |
| v2 k2 B, model (a), b9 | 0.6842 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=B, column k2 |
| v2 worst B, model (a), b9 | 0.3430 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=B, column worst |
| v2 retained B, model (a), b9 | 0.9416 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=B, column retained |
| v2 mean_under_faults SVM, model (a), b9 | 0.6095 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=svm, column mean_under_faults |
| v2 k1 SVM, model (a), b9 | 0.6490 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=svm, column k1 |
| v2 k2 SVM, model (a), b9 | 0.5701 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=svm, column k2 |
| v2 worst SVM, model (a), b9 | 0.1168 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=svm, column worst |
| v2 retained SVM, model (a), b9 | 0.8461 | results/final_test_v2/test/faults.csv, subset=b9, model=a, method=svm, column retained |
| v2 mean_under_faults A, model (b), b9 | 0.9404 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=A, column mean_under_faults |
| v2 k1 A, model (b), b9 | 0.9852 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=A, column k1 |
| v2 k2 A, model (b), b9 | 0.8957 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=A, column k2 |
| v2 worst A, model (b), b9 | 0.0564 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=A, column worst |
| v2 retained A, model (b), b9 | 0.9588 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=A, column retained |
| v2 mean_under_faults B, model (b), b9 | 0.9547 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=B, column mean_under_faults |
| v2 k1 B, model (b), b9 | 0.9859 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=B, column k1 |
| v2 k2 B, model (b), b9 | 0.9234 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=B, column k2 |
| v2 worst B, model (b), b9 | 0.2466 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=B, column worst |
| v2 retained B, model (b), b9 | 0.9680 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=B, column retained |
| v2 mean_under_faults SVM, model (b), b9 | 0.7714 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=svm, column mean_under_faults |
| v2 k1 SVM, model (b), b9 | 0.8359 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=svm, column k1 |
| v2 k2 SVM, model (b), b9 | 0.7069 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=svm, column k2 |
| v2 worst SVM, model (b), b9 | 0.0622 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=svm, column worst |
| v2 retained SVM, model (b), b9 | 0.8086 | results/final_test_v2/test/faults.csv, subset=b9, model=b, method=svm, column retained |
| v2 mean_under_faults A, model (a), pooled | 0.6549 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=A, column mean_under_faults |
| v2 k1 A, model (a), pooled | 0.6901 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=A, column k1 |
| v2 k2 A, model (a), pooled | 0.6197 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=A, column k2 |
| v2 worst A, model (a), pooled | 0.1146 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=A, column worst |
| v2 retained A, model (a), pooled | 0.9630 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=A, column retained |
| v2 mean_under_faults B, model (a), pooled | 0.6608 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=B, column mean_under_faults |
| v2 k1 B, model (a), pooled | 0.6886 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=B, column k1 |
| v2 k2 B, model (a), pooled | 0.6331 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=B, column k2 |
| v2 worst B, model (a), pooled | 0.2626 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=B, column worst |
| v2 retained B, model (a), pooled | 0.9565 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=B, column retained |
| v2 mean_under_faults SVM, model (a), pooled | 0.5441 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=svm, column mean_under_faults |
| v2 k1 SVM, model (a), pooled | 0.5838 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=svm, column k1 |
| v2 k2 SVM, model (a), pooled | 0.5044 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=svm, column k2 |
| v2 worst SVM, model (a), pooled | 0.1370 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=svm, column worst |
| v2 retained SVM, model (a), pooled | 0.7899 | results/final_test_v2/test/faults.csv, subset=pooled, model=a, method=svm, column retained |
| v2 mean_under_faults A, model (b), pooled | 0.7912 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=A, column mean_under_faults |
| v2 k1 A, model (b), pooled | 0.8237 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=A, column k1 |
| v2 k2 A, model (b), pooled | 0.7587 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=A, column k2 |
| v2 worst A, model (b), pooled | 0.1370 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=A, column worst |
| v2 retained A, model (b), pooled | 0.9686 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=A, column retained |
| v2 mean_under_faults B, model (b), pooled | 0.8094 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=B, column mean_under_faults |
| v2 k1 B, model (b), pooled | 0.8348 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=B, column k1 |
| v2 k2 B, model (b), pooled | 0.7840 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=B, column k2 |
| v2 worst B, model (b), pooled | 0.3360 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=B, column worst |
| v2 retained B, model (b), pooled | 0.9734 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=B, column retained |
| v2 mean_under_faults SVM, model (b), pooled | 0.6637 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=svm, column mean_under_faults |
| v2 k1 SVM, model (b), pooled | 0.7125 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=svm, column k1 |
| v2 k2 SVM, model (b), pooled | 0.6150 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=svm, column k2 |
| v2 worst SVM, model (b), pooled | 0.1691 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=svm, column worst |
| v2 retained SVM, model (b), pooled | 0.8079 | results/final_test_v2/test/faults.csv, subset=pooled, model=b, method=svm, column retained |
| v2 (b)-(a) svm under faults, b10, diff | 0.1294 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) svm under faults, column diff |
| v2 (b)-(a) svm under faults, b10, ci_low [superseded: v2 corrected CIs] | 0.1283 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) svm under faults, column ci_low |
| v2 (b)-(a) svm under faults, b10, ci_high [superseded: v2 corrected CIs] | 0.1304 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) svm under faults, column ci_high |
| v2 (b)-(a) A under faults, b10, diff | 0.1441 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) A under faults, column diff |
| v2 (b)-(a) A under faults, b10, ci_low [superseded: v2 corrected CIs] | 0.1428 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) A under faults, column ci_low |
| v2 (b)-(a) A under faults, b10, ci_high [superseded: v2 corrected CIs] | 0.1455 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) A under faults, column ci_high |
| v2 (b)-(a) B under faults, b10, diff | 0.1555 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) B under faults, column diff |
| v2 (b)-(a) B under faults, b10, ci_low [superseded: v2 corrected CIs] | 0.1545 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) B under faults, column ci_low |
| v2 (b)-(a) B under faults, b10, ci_high [superseded: v2 corrected CIs] | 0.1566 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=(b)-(a) B under faults, column ci_high |
| v2 A-SVM under faults, model (a), b10, diff | 0.1090 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=A-SVM under faults, model (a), column diff |
| v2 A-SVM under faults, model (a), b10, ci_low [superseded: v2 corrected CIs] | 0.1056 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=A-SVM under faults, model (a), column ci_low |
| v2 A-SVM under faults, model (a), b10, ci_high [superseded: v2 corrected CIs] | 0.1127 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=A-SVM under faults, model (a), column ci_high |
| v2 A-SVM under faults, model (b), b10, diff | 0.1238 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=A-SVM under faults, model (b), column diff |
| v2 A-SVM under faults, model (b), b10, ci_low [superseded: v2 corrected CIs] | 0.1200 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=A-SVM under faults, model (b), column ci_low |
| v2 A-SVM under faults, model (b), b10, ci_high [superseded: v2 corrected CIs] | 0.1281 | results/final_test_v2/test/faults_ci.csv, subset=b10, comparison=A-SVM under faults, model (b), column ci_high |
| v2 (b)-(a) svm under faults, b8, diff | 0.0482 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) svm under faults, column diff |
| v2 (b)-(a) svm under faults, b8, ci_low [superseded: v2 corrected CIs] | 0.0464 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) svm under faults, column ci_low |
| v2 (b)-(a) svm under faults, b8, ci_high [superseded: v2 corrected CIs] | 0.0499 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) svm under faults, column ci_high |
| v2 (b)-(a) A under faults, b8, diff | 0.0354 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) A under faults, column diff |
| v2 (b)-(a) A under faults, b8, ci_low [superseded: v2 corrected CIs] | 0.0342 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) A under faults, column ci_low |
| v2 (b)-(a) A under faults, b8, ci_high [superseded: v2 corrected CIs] | 0.0367 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) A under faults, column ci_high |
| v2 (b)-(a) B under faults, b8, diff | 0.0459 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) B under faults, column diff |
| v2 (b)-(a) B under faults, b8, ci_low [superseded: v2 corrected CIs] | 0.0449 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) B under faults, column ci_low |
| v2 (b)-(a) B under faults, b8, ci_high [superseded: v2 corrected CIs] | 0.0471 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=(b)-(a) B under faults, column ci_high |
| v2 A-SVM under faults, model (a), b8, diff | 0.1468 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=A-SVM under faults, model (a), column diff |
| v2 A-SVM under faults, model (a), b8, ci_low [superseded: v2 corrected CIs] | 0.1412 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=A-SVM under faults, model (a), column ci_low |
| v2 A-SVM under faults, model (a), b8, ci_high [superseded: v2 corrected CIs] | 0.1529 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=A-SVM under faults, model (a), column ci_high |
| v2 A-SVM under faults, model (b), b8, diff | 0.1340 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=A-SVM under faults, model (b), column diff |
| v2 A-SVM under faults, model (b), b8, ci_low [superseded: v2 corrected CIs] | 0.1282 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=A-SVM under faults, model (b), column ci_low |
| v2 A-SVM under faults, model (b), b8, ci_high [superseded: v2 corrected CIs] | 0.1402 | results/final_test_v2/test/faults_ci.csv, subset=b8, comparison=A-SVM under faults, model (b), column ci_high |
| v2 (b)-(a) svm under faults, b9, diff | 0.1618 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) svm under faults, column diff |
| v2 (b)-(a) svm under faults, b9, ci_low [superseded: v2 corrected CIs] | 0.1585 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) svm under faults, column ci_low |
| v2 (b)-(a) svm under faults, b9, ci_high [superseded: v2 corrected CIs] | 0.1652 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) svm under faults, column ci_high |
| v2 (b)-(a) A under faults, b9, diff | 0.2345 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) A under faults, column diff |
| v2 (b)-(a) A under faults, b9, ci_low [superseded: v2 corrected CIs] | 0.2323 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) A under faults, column ci_low |
| v2 (b)-(a) A under faults, b9, ci_high [superseded: v2 corrected CIs] | 0.2368 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) A under faults, column ci_high |
| v2 (b)-(a) B under faults, b9, diff | 0.2506 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) B under faults, column diff |
| v2 (b)-(a) B under faults, b9, ci_low [superseded: v2 corrected CIs] | 0.2485 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) B under faults, column ci_low |
| v2 (b)-(a) B under faults, b9, ci_high [superseded: v2 corrected CIs] | 0.2527 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=(b)-(a) B under faults, column ci_high |
| v2 A-SVM under faults, model (a), b9, diff | 0.0964 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=A-SVM under faults, model (a), column diff |
| v2 A-SVM under faults, model (a), b9, ci_low [superseded: v2 corrected CIs] | 0.0926 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=A-SVM under faults, model (a), column ci_low |
| v2 A-SVM under faults, model (a), b9, ci_high [superseded: v2 corrected CIs] | 0.1005 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=A-SVM under faults, model (a), column ci_high |
| v2 A-SVM under faults, model (b), b9, diff | 0.1691 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=A-SVM under faults, model (b), column diff |
| v2 A-SVM under faults, model (b), b9, ci_low [superseded: v2 corrected CIs] | 0.1635 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=A-SVM under faults, model (b), column ci_low |
| v2 A-SVM under faults, model (b), b9, ci_high [superseded: v2 corrected CIs] | 0.1752 | results/final_test_v2/test/faults_ci.csv, subset=b9, comparison=A-SVM under faults, model (b), column ci_high |
| v2 (b)-(a) svm under faults, pooled, diff | 0.1196 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) svm under faults, column diff |
| v2 (b)-(a) svm under faults, pooled, ci_low [superseded: v2 corrected CIs] | 0.1185 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) svm under faults, column ci_low |
| v2 (b)-(a) svm under faults, pooled, ci_high [superseded: v2 corrected CIs] | 0.1207 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) svm under faults, column ci_high |
| v2 (b)-(a) A under faults, pooled, diff | 0.1363 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) A under faults, column diff |
| v2 (b)-(a) A under faults, pooled, ci_low [superseded: v2 corrected CIs] | 0.1351 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) A under faults, column ci_low |
| v2 (b)-(a) A under faults, pooled, ci_high [superseded: v2 corrected CIs] | 0.1376 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) A under faults, column ci_high |
| v2 (b)-(a) B under faults, pooled, diff | 0.1486 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) B under faults, column diff |
| v2 (b)-(a) B under faults, pooled, ci_low [superseded: v2 corrected CIs] | 0.1477 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) B under faults, column ci_low |
| v2 (b)-(a) B under faults, pooled, ci_high [superseded: v2 corrected CIs] | 0.1495 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=(b)-(a) B under faults, column ci_high |
| v2 A-SVM under faults, model (a), pooled, diff | 0.1108 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=A-SVM under faults, model (a), column diff |
| v2 A-SVM under faults, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.1072 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=A-SVM under faults, model (a), column ci_low |
| v2 A-SVM under faults, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.1147 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=A-SVM under faults, model (a), column ci_high |
| v2 A-SVM under faults, model (b), pooled, diff | 0.1275 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=A-SVM under faults, model (b), column diff |
| v2 A-SVM under faults, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.1231 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=A-SVM under faults, model (b), column ci_low |
| v2 A-SVM under faults, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.1318 | results/final_test_v2/test/faults_ci.csv, subset=pooled, comparison=A-SVM under faults, model (b), column ci_high |
| v2 level clean A, model (a), pooled, value | 0.6922 | results/paper/v2_figure_data.csv, model=a, method=A, kind=clean, column value |
| v2 level clean A, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.6916 | results/paper/v2_figure_data.csv, model=a, method=A, kind=clean, column ci_low |
| v2 level clean A, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.6928 | results/paper/v2_figure_data.csv, model=a, method=A, kind=clean, column ci_high |
| v2 level faults A, model (a), pooled, value | 0.6549 | results/paper/v2_figure_data.csv, model=a, method=A, kind=faults, column value |
| v2 level faults A, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.6521 | results/paper/v2_figure_data.csv, model=a, method=A, kind=faults, column ci_low |
| v2 level faults A, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.6576 | results/paper/v2_figure_data.csv, model=a, method=A, kind=faults, column ci_high |
| v2 level clean B, model (a), pooled, value | 0.7005 | results/paper/v2_figure_data.csv, model=a, method=B, kind=clean, column value |
| v2 level clean B, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.7000 | results/paper/v2_figure_data.csv, model=a, method=B, kind=clean, column ci_low |
| v2 level clean B, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.7011 | results/paper/v2_figure_data.csv, model=a, method=B, kind=clean, column ci_high |
| v2 level faults B, model (a), pooled, value | 0.6608 | results/paper/v2_figure_data.csv, model=a, method=B, kind=faults, column value |
| v2 level faults B, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.6588 | results/paper/v2_figure_data.csv, model=a, method=B, kind=faults, column ci_low |
| v2 level faults B, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.6629 | results/paper/v2_figure_data.csv, model=a, method=B, kind=faults, column ci_high |
| v2 level clean SVM, model (a), pooled, value | 0.7056 | results/paper/v2_figure_data.csv, model=a, method=svm, kind=clean, column value |
| v2 level clean SVM, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.7046 | results/paper/v2_figure_data.csv, model=a, method=svm, kind=clean, column ci_low |
| v2 level clean SVM, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.7066 | results/paper/v2_figure_data.csv, model=a, method=svm, kind=clean, column ci_high |
| v2 level faults SVM, model (a), pooled, value | 0.5441 | results/paper/v2_figure_data.csv, model=a, method=svm, kind=faults, column value |
| v2 level faults SVM, model (a), pooled, ci_low [superseded: v2 corrected CIs] | 0.5409 | results/paper/v2_figure_data.csv, model=a, method=svm, kind=faults, column ci_low |
| v2 level faults SVM, model (a), pooled, ci_high [superseded: v2 corrected CIs] | 0.5476 | results/paper/v2_figure_data.csv, model=a, method=svm, kind=faults, column ci_high |
| v2 level clean A, model (b), pooled, value | 0.8281 | results/paper/v2_figure_data.csv, model=b, method=A, kind=clean, column value |
| v2 level clean A, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.8122 | results/paper/v2_figure_data.csv, model=b, method=A, kind=clean, column ci_low |
| v2 level clean A, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.8440 | results/paper/v2_figure_data.csv, model=b, method=A, kind=clean, column ci_high |
| v2 level faults A, model (b), pooled, value | 0.7912 | results/paper/v2_figure_data.csv, model=b, method=A, kind=faults, column value |
| v2 level faults A, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.7884 | results/paper/v2_figure_data.csv, model=b, method=A, kind=faults, column ci_low |
| v2 level faults A, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.7938 | results/paper/v2_figure_data.csv, model=b, method=A, kind=faults, column ci_high |
| v2 level clean B, model (b), pooled, value | 0.8402 | results/paper/v2_figure_data.csv, model=b, method=B, kind=clean, column value |
| v2 level clean B, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.8222 | results/paper/v2_figure_data.csv, model=b, method=B, kind=clean, column ci_low |
| v2 level clean B, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.8583 | results/paper/v2_figure_data.csv, model=b, method=B, kind=clean, column ci_high |
| v2 level faults B, model (b), pooled, value | 0.8094 | results/paper/v2_figure_data.csv, model=b, method=B, kind=faults, column value |
| v2 level faults B, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.8072 | results/paper/v2_figure_data.csv, model=b, method=B, kind=faults, column ci_low |
| v2 level faults B, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.8114 | results/paper/v2_figure_data.csv, model=b, method=B, kind=faults, column ci_high |
| v2 level clean SVM, model (b), pooled, value | 0.8418 | results/paper/v2_figure_data.csv, model=b, method=svm, kind=clean, column value |
| v2 level clean SVM, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.8215 | results/paper/v2_figure_data.csv, model=b, method=svm, kind=clean, column ci_low |
| v2 level clean SVM, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.8620 | results/paper/v2_figure_data.csv, model=b, method=svm, kind=clean, column ci_high |
| v2 level faults SVM, model (b), pooled, value | 0.6637 | results/paper/v2_figure_data.csv, model=b, method=svm, kind=faults, column value |
| v2 level faults SVM, model (b), pooled, ci_low [superseded: v2 corrected CIs] | 0.6598 | results/paper/v2_figure_data.csv, model=b, method=svm, kind=faults, column ci_low |
| v2 level faults SVM, model (b), pooled, ci_high [superseded: v2 corrected CIs] | 0.6676 | results/paper/v2_figure_data.csv, model=b, method=svm, kind=faults, column ci_high |
| v2 verdict N8 success | True | results/final_test_v2/test/verdict.json, success |
| v2 edge size (KB), svm_calibrated | 511.4727 | results/edge_cost/edge_cost_v2.json, size_kb.svm_calibrated |
| v2 edge size (KB), preprocessing | 3.5791 | results/edge_cost/edge_cost_v2.json, size_kb.preprocessing |
| v2 edge size (KB), detector_for_A | 266.8877 | results/edge_cost/edge_cost_v2.json, size_kb.detector_for_A |
| v2 edge size (KB), B_136_reduced_models | 61972.9023 | results/edge_cost/edge_cost_v2.json, size_kb.B_136_reduced_models |
| v2 edge size (KB), A_bundle_svm_pre_detector | 781.9395 | results/edge_cost/edge_cost_v2.json, size_kb.A_bundle_svm_pre_detector |
| v2 edge size (KB), B_bundle_pre_detector_136_models | 62243.3691 | results/edge_cost/edge_cost_v2.json, size_kb.B_bundle_pre_detector_136_models |
| v2 edge latency median_ms, svm_only_fault_free | 5.4085 | results/edge_cost/edge_cost_v2.json, svm_only_fault_free.median_ms |
| v2 edge latency p95_ms, svm_only_fault_free | 11.6326 | results/edge_cost/edge_cost_v2.json, svm_only_fault_free.p95_ms |
| v2 edge latency median_ms, A_fault_free | 9.3431 | results/edge_cost/edge_cost_v2.json, A_fault_free.median_ms |
| v2 edge latency p95_ms, A_fault_free | 20.5187 | results/edge_cost/edge_cost_v2.json, A_fault_free.p95_ms |
| v2 edge latency median_ms, A_bias_one_sensor | 7.7726 | results/edge_cost/edge_cost_v2.json, A_bias_one_sensor.median_ms |
| v2 edge latency p95_ms, A_bias_one_sensor | 18.4471 | results/edge_cost/edge_cost_v2.json, A_bias_one_sensor.p95_ms |
| v2 edge latency median_ms, B_fault_free | 7.4476 | results/edge_cost/edge_cost_v2.json, B_fault_free.median_ms |
| v2 edge latency p95_ms, B_fault_free | 17.0380 | results/edge_cost/edge_cost_v2.json, B_fault_free.p95_ms |
| v2 edge latency median_ms, B_bias_one_sensor | 7.2465 | results/edge_cost/edge_cost_v2.json, B_bias_one_sensor.median_ms |
| v2 edge latency p95_ms, B_bias_one_sensor | 18.4304 | results/edge_cost/edge_cost_v2.json, B_bias_one_sensor.p95_ms |
| v2 edge calibration_svm_s | 1.4251 | results/edge_cost/edge_cost_v2.json, calibration_svm_s |
| v2 edge calibration_detector_s | 2.3879 | results/edge_cost/edge_cost_v2.json, calibration_detector_s |
| v2 edge calibration_B_136_models_s | 149.1085 | results/edge_cost/edge_cost_v2.json, calibration_B_136_models_s |
| v2 edge calibration_total_s | 152.9215 | results/edge_cost/edge_cost_v2.json, calibration_total_s |
| v2 edge train_data_kb_float64 | 5991 | results/edge_cost/edge_cost_v2.json, train_data_kb_float64 |
| v2 edge memory_peak_mb | 227.8906 | results/edge_cost/edge_cost_v2.json, memory_peak_mb |
| v2 edge calibration_rows | 60 | results/edge_cost/edge_cost_v2.json, calibration_rows |
| v2 edge train_rows_for_calibration | 5991 | results/edge_cost/edge_cost_v2.json, train_rows_for_calibration |


## v2 corrected CIs

Post-audit correction (decisions_log O). Replaces the v2 intervals marked '[superseded: v2 corrected CIs]' above (kept, not deleted). Under faults: shared-index scenario bootstrap over the 5 calibration seeds; clean: 95% t-interval over the 5 seeds (calibration-draw variance only; row sampling would need the Test labels, not read again). Point estimates are unchanged.

| number | value | source |
|---|---|---|
| v2c (b)-(a) A clean, b10, value | 0.1449 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) A clean, column value |
| v2c (b)-(a) A clean, b10, ci_low | 0.1260 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) A clean, column ci_low |
| v2c (b)-(a) A clean, b10, ci_high | 0.1637 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) A clean, column ci_high |
| v2c A model (b) clean, b10, value | 0.8014 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=A model (b) clean, column value |
| v2c A model (b) clean, b10, ci_low | 0.7824 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=A model (b) clean, column ci_low |
| v2c A model (b) clean, b10, ci_high | 0.8204 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=A model (b) clean, column ci_high |
| v2c A model (a) clean, b10, value | 0.6565 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=A model (a) clean, column value |
| v2c (b)-(a) B clean, b10, value | 0.1486 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) B clean, column value |
| v2c (b)-(a) B clean, b10, ci_low | 0.1274 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) B clean, column ci_low |
| v2c (b)-(a) B clean, b10, ci_high | 0.1697 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) B clean, column ci_high |
| v2c B model (b) clean, b10, value | 0.8143 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=B model (b) clean, column value |
| v2c B model (b) clean, b10, ci_low | 0.7927 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=B model (b) clean, column ci_low |
| v2c B model (b) clean, b10, ci_high | 0.8359 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=B model (b) clean, column ci_high |
| v2c B model (a) clean, b10, value | 0.6657 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=B model (a) clean, column value |
| v2c (b)-(a) svm clean, b10, value | 0.1440 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) svm clean, column value |
| v2c (b)-(a) svm clean, b10, ci_low | 0.1205 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) svm clean, column ci_low |
| v2c (b)-(a) svm clean, b10, ci_high | 0.1675 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b10, comparison=(b)-(a) svm clean, column ci_high |
| v2c svm model (b) clean, b10, value | 0.8183 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=svm model (b) clean, column value |
| v2c svm model (b) clean, b10, ci_low | 0.7945 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=svm model (b) clean, column ci_low |
| v2c svm model (b) clean, b10, ci_high | 0.8421 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=svm model (b) clean, column ci_high |
| v2c svm model (a) clean, b10, value | 0.6743 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b10, comparison=svm model (a) clean, column value |
| v2c (b)-(a) A clean, b8, value | 0.0137 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) A clean, column value |
| v2c (b)-(a) A clean, b8, ci_low | -0.0267 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) A clean, column ci_low |
| v2c (b)-(a) A clean, b8, ci_high | 0.0541 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) A clean, column ci_high |
| v2c A model (b) clean, b8, value | 0.8628 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=A model (b) clean, column value |
| v2c A model (b) clean, b8, ci_low | 0.8365 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=A model (b) clean, column ci_low |
| v2c A model (b) clean, b8, ci_high | 0.8891 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=A model (b) clean, column ci_high |
| v2c A model (a) clean, b8, value | 0.8491 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=A model (a) clean, column value |
| v2c (b)-(a) B clean, b8, value | 0.0403 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) B clean, column value |
| v2c (b)-(a) B clean, b8, ci_low | 0.0334 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) B clean, column ci_low |
| v2c (b)-(a) B clean, b8, ci_high | 0.0472 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) B clean, column ci_high |
| v2c B model (b) clean, b8, value | 0.9587 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=B model (b) clean, column value |
| v2c B model (b) clean, b8, ci_low | 0.9493 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=B model (b) clean, column ci_low |
| v2c B model (b) clean, b8, ci_high | 0.9680 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=B model (b) clean, column ci_high |
| v2c B model (a) clean, b8, value | 0.9183 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=B model (a) clean, column value |
| v2c (b)-(a) svm clean, b8, value | 0.0397 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) svm clean, column value |
| v2c (b)-(a) svm clean, b8, ci_low | 0.0190 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) svm clean, column ci_low |
| v2c (b)-(a) svm clean, b8, ci_high | 0.0604 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b8, comparison=(b)-(a) svm clean, column ci_high |
| v2c svm model (b) clean, b8, value | 0.9391 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=svm model (b) clean, column value |
| v2c svm model (b) clean, b8, ci_low | 0.9064 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=svm model (b) clean, column ci_low |
| v2c svm model (b) clean, b8, ci_high | 0.9717 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=svm model (b) clean, column ci_high |
| v2c svm model (a) clean, b8, value | 0.8994 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b8, comparison=svm model (a) clean, column value |
| v2c (b)-(a) A clean, b9, value | 0.2421 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) A clean, column value |
| v2c (b)-(a) A clean, b9, ci_low | 0.2399 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) A clean, column ci_low |
| v2c (b)-(a) A clean, b9, ci_high | 0.2443 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) A clean, column ci_high |
| v2c A model (b) clean, b9, value | 0.9965 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=A model (b) clean, column value |
| v2c A model (b) clean, b9, ci_low | 0.9929 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=A model (b) clean, column ci_low |
| v2c A model (b) clean, b9, ci_high | 1.0000 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=A model (b) clean, column ci_high |
| v2c A model (a) clean, b9, value | 0.7544 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=A model (a) clean, column value |
| v2c (b)-(a) B clean, b9, value | 0.2421 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) B clean, column value |
| v2c (b)-(a) B clean, b9, ci_low | 0.2408 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) B clean, column ci_low |
| v2c (b)-(a) B clean, b9, ci_high | 0.2435 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) B clean, column ci_high |
| v2c B model (b) clean, b9, value | 0.9970 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=B model (b) clean, column value |
| v2c B model (b) clean, b9, ci_low | 0.9943 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=B model (b) clean, column ci_low |
| v2c B model (b) clean, b9, ci_high | 0.9996 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=B model (b) clean, column ci_high |
| v2c B model (a) clean, b9, value | 0.7548 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=B model (a) clean, column value |
| v2c (b)-(a) svm clean, b9, value | 0.2446 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) svm clean, column value |
| v2c (b)-(a) svm clean, b9, ci_low | 0.2398 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) svm clean, column ci_low |
| v2c (b)-(a) svm clean, b9, ci_high | 0.2495 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=b9, comparison=(b)-(a) svm clean, column ci_high |
| v2c svm model (b) clean, b9, value | 0.9806 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=svm model (b) clean, column value |
| v2c svm model (b) clean, b9, ci_low | 0.9758 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=svm model (b) clean, column ci_low |
| v2c svm model (b) clean, b9, ci_high | 0.9854 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=svm model (b) clean, column ci_high |
| v2c svm model (a) clean, b9, value | 0.7360 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=b9, comparison=svm model (a) clean, column value |
| v2c (b)-(a) A clean, pooled, value | 0.1359 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) A clean, column value |
| v2c (b)-(a) A clean, pooled, ci_low | 0.1204 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) A clean, column ci_low |
| v2c (b)-(a) A clean, pooled, ci_high | 0.1513 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) A clean, column ci_high |
| v2c A model (b) clean, pooled, value | 0.8281 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=A model (b) clean, column value |
| v2c A model (b) clean, pooled, ci_low | 0.8122 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=A model (b) clean, column ci_low |
| v2c A model (b) clean, pooled, ci_high | 0.8440 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=A model (b) clean, column ci_high |
| v2c A model (a) clean, pooled, value | 0.6922 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=A model (a) clean, column value |
| v2c (b)-(a) B clean, pooled, value | 0.1397 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) B clean, column value |
| v2c (b)-(a) B clean, pooled, ci_low | 0.1219 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) B clean, column ci_low |
| v2c (b)-(a) B clean, pooled, ci_high | 0.1575 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) B clean, column ci_high |
| v2c B model (b) clean, pooled, value | 0.8402 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=B model (b) clean, column value |
| v2c B model (b) clean, pooled, ci_low | 0.8222 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=B model (b) clean, column ci_low |
| v2c B model (b) clean, pooled, ci_high | 0.8583 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=B model (b) clean, column ci_high |
| v2c B model (a) clean, pooled, value | 0.7005 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=B model (a) clean, column value |
| v2c (b)-(a) svm clean, pooled, value | 0.1362 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) svm clean, column value |
| v2c (b)-(a) svm clean, pooled, ci_low | 0.1166 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) svm clean, column ci_low |
| v2c (b)-(a) svm clean, pooled, ci_high | 0.1557 | results/paper/v2_corrected_ci.csv, kind=clean_gain, subset=pooled, comparison=(b)-(a) svm clean, column ci_high |
| v2c svm model (b) clean, pooled, value | 0.8418 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=svm model (b) clean, column value |
| v2c svm model (b) clean, pooled, ci_low | 0.8215 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=svm model (b) clean, column ci_low |
| v2c svm model (b) clean, pooled, ci_high | 0.8620 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=svm model (b) clean, column ci_high |
| v2c svm model (a) clean, pooled, value | 0.7056 | results/paper/v2_corrected_ci.csv, kind=clean_level, subset=pooled, comparison=svm model (a) clean, column value |
| v2c (b)-(a) svm under faults, b10, value | 0.1294 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) svm under faults, column value |
| v2c (b)-(a) svm under faults, b10, ci_low | 0.1272 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) svm under faults, column ci_low |
| v2c (b)-(a) svm under faults, b10, ci_high | 0.1315 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) svm under faults, column ci_high |
| v2c svm model (a) under faults, b10, value | 0.5121 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=svm model (a) under faults, column value |
| v2c svm model (a) under faults, b10, ci_low | 0.5037 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=svm model (a) under faults, column ci_low |
| v2c svm model (a) under faults, b10, ci_high | 0.5205 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=svm model (a) under faults, column ci_high |
| v2c svm model (b) under faults, b10, value | 0.6415 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=svm model (b) under faults, column value |
| v2c svm model (b) under faults, b10, ci_low | 0.6329 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=svm model (b) under faults, column ci_low |
| v2c svm model (b) under faults, b10, ci_high | 0.6501 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=svm model (b) under faults, column ci_high |
| v2c (b)-(a) A under faults, b10, value | 0.1441 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) A under faults, column value |
| v2c (b)-(a) A under faults, b10, ci_low | 0.1413 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) A under faults, column ci_low |
| v2c (b)-(a) A under faults, b10, ci_high | 0.1469 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) A under faults, column ci_high |
| v2c A model (a) under faults, b10, value | 0.6211 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=A model (a) under faults, column value |
| v2c A model (a) under faults, b10, ci_low | 0.6148 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=A model (a) under faults, column ci_low |
| v2c A model (a) under faults, b10, ci_high | 0.6270 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=A model (a) under faults, column ci_high |
| v2c A model (b) under faults, b10, value | 0.7653 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=A model (b) under faults, column value |
| v2c A model (b) under faults, b10, ci_low | 0.7587 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=A model (b) under faults, column ci_low |
| v2c A model (b) under faults, b10, ci_high | 0.7714 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=A model (b) under faults, column ci_high |
| v2c (b)-(a) B under faults, b10, value | 0.1555 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) B under faults, column value |
| v2c (b)-(a) B under faults, b10, ci_low | 0.1532 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) B under faults, column ci_low |
| v2c (b)-(a) B under faults, b10, ci_high | 0.1575 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=(b)-(a) B under faults, column ci_high |
| v2c B model (a) under faults, b10, value | 0.6287 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=B model (a) under faults, column value |
| v2c B model (a) under faults, b10, ci_low | 0.6239 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=B model (a) under faults, column ci_low |
| v2c B model (a) under faults, b10, ci_high | 0.6332 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=B model (a) under faults, column ci_high |
| v2c B model (b) under faults, b10, value | 0.7843 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=B model (b) under faults, column value |
| v2c B model (b) under faults, b10, ci_low | 0.7792 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=B model (b) under faults, column ci_low |
| v2c B model (b) under faults, b10, ci_high | 0.7887 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b10, comparison=B model (b) under faults, column ci_high |
| v2c A-SVM under faults, model (a), b10, value | 0.1090 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=A-SVM under faults, model (a), column value |
| v2c A-SVM under faults, model (a), b10, ci_low | 0.1008 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=A-SVM under faults, model (a), column ci_low |
| v2c A-SVM under faults, model (a), b10, ci_high | 0.1178 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=A-SVM under faults, model (a), column ci_high |
| v2c A-SVM under faults, model (b), b10, value | 0.1238 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=A-SVM under faults, model (b), column value |
| v2c A-SVM under faults, model (b), b10, ci_low | 0.1147 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=A-SVM under faults, model (b), column ci_low |
| v2c A-SVM under faults, model (b), b10, ci_high | 0.1344 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b10, comparison=A-SVM under faults, model (b), column ci_high |
| v2c (b)-(a) svm under faults, b8, value | 0.0482 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) svm under faults, column value |
| v2c (b)-(a) svm under faults, b8, ci_low | 0.0446 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) svm under faults, column ci_low |
| v2c (b)-(a) svm under faults, b8, ci_high | 0.0518 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) svm under faults, column ci_high |
| v2c svm model (a) under faults, b8, value | 0.6941 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=svm model (a) under faults, column value |
| v2c svm model (a) under faults, b8, ci_low | 0.6816 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=svm model (a) under faults, column ci_low |
| v2c svm model (a) under faults, b8, ci_high | 0.7068 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=svm model (a) under faults, column ci_high |
| v2c svm model (b) under faults, b8, value | 0.7423 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=svm model (b) under faults, column value |
| v2c svm model (b) under faults, b8, ci_low | 0.7288 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=svm model (b) under faults, column ci_low |
| v2c svm model (b) under faults, b8, ci_high | 0.7554 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=svm model (b) under faults, column ci_high |
| v2c (b)-(a) A under faults, b8, value | 0.0354 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) A under faults, column value |
| v2c (b)-(a) A under faults, b8, ci_low | 0.0331 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) A under faults, column ci_low |
| v2c (b)-(a) A under faults, b8, ci_high | 0.0378 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) A under faults, column ci_high |
| v2c A model (a) under faults, b8, value | 0.8409 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=A model (a) under faults, column value |
| v2c A model (a) under faults, b8, ci_low | 0.8317 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=A model (a) under faults, column ci_low |
| v2c A model (a) under faults, b8, ci_high | 0.8499 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=A model (a) under faults, column ci_high |
| v2c A model (b) under faults, b8, value | 0.8764 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=A model (b) under faults, column value |
| v2c A model (b) under faults, b8, ci_low | 0.8668 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=A model (b) under faults, column ci_low |
| v2c A model (b) under faults, b8, ci_high | 0.8850 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=A model (b) under faults, column ci_high |
| v2c (b)-(a) B under faults, b8, value | 0.0459 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) B under faults, column value |
| v2c (b)-(a) B under faults, b8, ci_low | 0.0438 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) B under faults, column ci_low |
| v2c (b)-(a) B under faults, b8, ci_high | 0.0482 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=(b)-(a) B under faults, column ci_high |
| v2c B model (a) under faults, b8, value | 0.8733 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=B model (a) under faults, column value |
| v2c B model (a) under faults, b8, ci_low | 0.8663 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=B model (a) under faults, column ci_low |
| v2c B model (a) under faults, b8, ci_high | 0.8796 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=B model (a) under faults, column ci_high |
| v2c B model (b) under faults, b8, value | 0.9192 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=B model (b) under faults, column value |
| v2c B model (b) under faults, b8, ci_low | 0.9124 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=B model (b) under faults, column ci_low |
| v2c B model (b) under faults, b8, ci_high | 0.9251 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b8, comparison=B model (b) under faults, column ci_high |
| v2c A-SVM under faults, model (a), b8, value | 0.1468 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=A-SVM under faults, model (a), column value |
| v2c A-SVM under faults, model (a), b8, ci_low | 0.1344 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=A-SVM under faults, model (a), column ci_low |
| v2c A-SVM under faults, model (a), b8, ci_high | 0.1600 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=A-SVM under faults, model (a), column ci_high |
| v2c A-SVM under faults, model (b), b8, value | 0.1340 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=A-SVM under faults, model (b), column value |
| v2c A-SVM under faults, model (b), b8, ci_low | 0.1203 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=A-SVM under faults, model (b), column ci_low |
| v2c A-SVM under faults, model (b), b8, ci_high | 0.1476 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b8, comparison=A-SVM under faults, model (b), column ci_high |
| v2c (b)-(a) svm under faults, b9, value | 0.1618 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) svm under faults, column value |
| v2c (b)-(a) svm under faults, b9, ci_low | 0.1532 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) svm under faults, column ci_low |
| v2c (b)-(a) svm under faults, b9, ci_high | 0.1704 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) svm under faults, column ci_high |
| v2c svm model (a) under faults, b9, value | 0.6095 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=svm model (a) under faults, column value |
| v2c svm model (a) under faults, b9, ci_low | 0.5993 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=svm model (a) under faults, column ci_low |
| v2c svm model (a) under faults, b9, ci_high | 0.6193 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=svm model (a) under faults, column ci_high |
| v2c svm model (b) under faults, b9, value | 0.7714 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=svm model (b) under faults, column value |
| v2c svm model (b) under faults, b9, ci_low | 0.7581 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=svm model (b) under faults, column ci_low |
| v2c svm model (b) under faults, b9, ci_high | 0.7848 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=svm model (b) under faults, column ci_high |
| v2c (b)-(a) A under faults, b9, value | 0.2345 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) A under faults, column value |
| v2c (b)-(a) A under faults, b9, ci_low | 0.2295 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) A under faults, column ci_low |
| v2c (b)-(a) A under faults, b9, ci_high | 0.2389 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) A under faults, column ci_high |
| v2c A model (a) under faults, b9, value | 0.7059 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=A model (a) under faults, column value |
| v2c A model (a) under faults, b9, ci_low | 0.6993 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=A model (a) under faults, column ci_low |
| v2c A model (a) under faults, b9, ci_high | 0.7123 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=A model (a) under faults, column ci_high |
| v2c A model (b) under faults, b9, value | 0.9404 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=A model (b) under faults, column value |
| v2c A model (b) under faults, b9, ci_low | 0.9310 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=A model (b) under faults, column ci_low |
| v2c A model (b) under faults, b9, ci_high | 0.9493 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=A model (b) under faults, column ci_high |
| v2c (b)-(a) B under faults, b9, value | 0.2506 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) B under faults, column value |
| v2c (b)-(a) B under faults, b9, ci_low | 0.2460 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) B under faults, column ci_low |
| v2c (b)-(a) B under faults, b9, ci_high | 0.2550 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=(b)-(a) B under faults, column ci_high |
| v2c B model (a) under faults, b9, value | 0.7041 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=B model (a) under faults, column value |
| v2c B model (a) under faults, b9, ci_low | 0.6992 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=B model (a) under faults, column ci_low |
| v2c B model (a) under faults, b9, ci_high | 0.7089 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=B model (a) under faults, column ci_high |
| v2c B model (b) under faults, b9, value | 0.9547 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=B model (b) under faults, column value |
| v2c B model (b) under faults, b9, ci_low | 0.9474 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=B model (b) under faults, column ci_low |
| v2c B model (b) under faults, b9, ci_high | 0.9609 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=b9, comparison=B model (b) under faults, column ci_high |
| v2c A-SVM under faults, model (a), b9, value | 0.0964 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=A-SVM under faults, model (a), column value |
| v2c A-SVM under faults, model (a), b9, ci_low | 0.0876 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=A-SVM under faults, model (a), column ci_low |
| v2c A-SVM under faults, model (a), b9, ci_high | 0.1055 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=A-SVM under faults, model (a), column ci_high |
| v2c A-SVM under faults, model (b), b9, value | 0.1691 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=A-SVM under faults, model (b), column value |
| v2c A-SVM under faults, model (b), b9, ci_low | 0.1548 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=A-SVM under faults, model (b), column ci_low |
| v2c A-SVM under faults, model (b), b9, ci_high | 0.1834 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=b9, comparison=A-SVM under faults, model (b), column ci_high |
| v2c (b)-(a) svm under faults, pooled, value | 0.1196 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) svm under faults, column value |
| v2c (b)-(a) svm under faults, pooled, ci_low | 0.1173 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) svm under faults, column ci_low |
| v2c (b)-(a) svm under faults, pooled, ci_high | 0.1220 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) svm under faults, column ci_high |
| v2c svm model (a) under faults, pooled, value | 0.5441 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=svm model (a) under faults, column value |
| v2c svm model (a) under faults, pooled, ci_low | 0.5359 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=svm model (a) under faults, column ci_low |
| v2c svm model (a) under faults, pooled, ci_high | 0.5523 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=svm model (a) under faults, column ci_high |
| v2c svm model (b) under faults, pooled, value | 0.6637 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=svm model (b) under faults, column value |
| v2c svm model (b) under faults, pooled, ci_low | 0.6551 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=svm model (b) under faults, column ci_low |
| v2c svm model (b) under faults, pooled, ci_high | 0.6727 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=svm model (b) under faults, column ci_high |
| v2c (b)-(a) A under faults, pooled, value | 0.1363 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) A under faults, column value |
| v2c (b)-(a) A under faults, pooled, ci_low | 0.1339 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) A under faults, column ci_low |
| v2c (b)-(a) A under faults, pooled, ci_high | 0.1386 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) A under faults, column ci_high |
| v2c A model (a) under faults, pooled, value | 0.6549 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=A model (a) under faults, column value |
| v2c A model (a) under faults, pooled, ci_low | 0.6485 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=A model (a) under faults, column ci_low |
| v2c A model (a) under faults, pooled, ci_high | 0.6608 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=A model (a) under faults, column ci_high |
| v2c A model (b) under faults, pooled, value | 0.7912 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=A model (b) under faults, column value |
| v2c A model (b) under faults, pooled, ci_low | 0.7848 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=A model (b) under faults, column ci_low |
| v2c A model (b) under faults, pooled, ci_high | 0.7975 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=A model (b) under faults, column ci_high |
| v2c (b)-(a) B under faults, pooled, value | 0.1486 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) B under faults, column value |
| v2c (b)-(a) B under faults, pooled, ci_low | 0.1466 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) B under faults, column ci_low |
| v2c (b)-(a) B under faults, pooled, ci_high | 0.1503 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=(b)-(a) B under faults, column ci_high |
| v2c B model (a) under faults, pooled, value | 0.6608 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=B model (a) under faults, column value |
| v2c B model (a) under faults, pooled, ci_low | 0.6563 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=B model (a) under faults, column ci_low |
| v2c B model (a) under faults, pooled, ci_high | 0.6651 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=B model (a) under faults, column ci_high |
| v2c B model (b) under faults, pooled, value | 0.8094 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=B model (b) under faults, column value |
| v2c B model (b) under faults, pooled, ci_low | 0.8046 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=B model (b) under faults, column ci_low |
| v2c B model (b) under faults, pooled, ci_high | 0.8137 | results/paper/v2_corrected_ci.csv, kind=faults_level, subset=pooled, comparison=B model (b) under faults, column ci_high |
| v2c A-SVM under faults, model (a), pooled, value | 0.1108 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=A-SVM under faults, model (a), column value |
| v2c A-SVM under faults, model (a), pooled, ci_low | 0.1024 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=A-SVM under faults, model (a), column ci_low |
| v2c A-SVM under faults, model (a), pooled, ci_high | 0.1195 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=A-SVM under faults, model (a), column ci_high |
| v2c A-SVM under faults, model (b), pooled, value | 0.1275 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=A-SVM under faults, model (b), column value |
| v2c A-SVM under faults, model (b), pooled, ci_low | 0.1181 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=A-SVM under faults, model (b), column ci_low |
| v2c A-SVM under faults, model (b), pooled, ci_high | 0.1381 | results/paper/v2_corrected_ci.csv, kind=faults_diff, subset=pooled, comparison=A-SVM under faults, model (b), column ci_high |


## Detector AUROC without Dropout

Mean isolation AUROC over the fault types (each type first averaged over its severities), primary 'median' detector. Dropout scores 1.0 by construction (a missing block is +inf), so it is shown with and without it (decisions_log O). v2 has no pooled detector value (each Test batch has its own model).

| number | value | source |
|---|---|---|
| AUROC v1 Validation k1, with Dropout | 0.9712 | results/paper/auroc_no_dropout.csv, version=v1, subset=Validation, model=-, k=k1, column with_dropout |
| AUROC v1 Validation k1, without Dropout | 0.9616 | results/paper/auroc_no_dropout.csv, version=v1, subset=Validation, model=-, k=k1, column without_dropout |
| AUROC v1 Validation k2, with Dropout | 0.9016 | results/paper/auroc_no_dropout.csv, version=v1, subset=Validation, model=-, k=k2, column with_dropout |
| AUROC v1 Validation k2, without Dropout | 0.8689 | results/paper/auroc_no_dropout.csv, version=v1, subset=Validation, model=-, k=k2, column without_dropout |
| AUROC v1 b10 k1, with Dropout | 0.9760 | results/paper/auroc_no_dropout.csv, version=v1, subset=b10, model=-, k=k1, column with_dropout |
| AUROC v1 b10 k1, without Dropout | 0.9680 | results/paper/auroc_no_dropout.csv, version=v1, subset=b10, model=-, k=k1, column without_dropout |
| AUROC v1 b10 k2, with Dropout | 0.9061 | results/paper/auroc_no_dropout.csv, version=v1, subset=b10, model=-, k=k2, column with_dropout |
| AUROC v1 b10 k2, without Dropout | 0.8748 | results/paper/auroc_no_dropout.csv, version=v1, subset=b10, model=-, k=k2, column without_dropout |
| AUROC v1 b8 k1, with Dropout | 0.9579 | results/paper/auroc_no_dropout.csv, version=v1, subset=b8, model=-, k=k1, column with_dropout |
| AUROC v1 b8 k1, without Dropout | 0.9438 | results/paper/auroc_no_dropout.csv, version=v1, subset=b8, model=-, k=k1, column without_dropout |
| AUROC v1 b8 k2, with Dropout | 0.8945 | results/paper/auroc_no_dropout.csv, version=v1, subset=b8, model=-, k=k2, column with_dropout |
| AUROC v1 b8 k2, without Dropout | 0.8594 | results/paper/auroc_no_dropout.csv, version=v1, subset=b8, model=-, k=k2, column without_dropout |
| AUROC v1 b9 k1, with Dropout | 0.9851 | results/paper/auroc_no_dropout.csv, version=v1, subset=b9, model=-, k=k1, column with_dropout |
| AUROC v1 b9 k1, without Dropout | 0.9801 | results/paper/auroc_no_dropout.csv, version=v1, subset=b9, model=-, k=k1, column without_dropout |
| AUROC v1 b9 k2, with Dropout | 0.9292 | results/paper/auroc_no_dropout.csv, version=v1, subset=b9, model=-, k=k2, column with_dropout |
| AUROC v1 b9 k2, without Dropout | 0.9056 | results/paper/auroc_no_dropout.csv, version=v1, subset=b9, model=-, k=k2, column without_dropout |
| AUROC v1 pooled k1, with Dropout | 0.9755 | results/paper/auroc_no_dropout.csv, version=v1, subset=pooled, model=-, k=k1, column with_dropout |
| AUROC v1 pooled k1, without Dropout | 0.9673 | results/paper/auroc_no_dropout.csv, version=v1, subset=pooled, model=-, k=k1, column without_dropout |
| AUROC v1 pooled k2, with Dropout | 0.9076 | results/paper/auroc_no_dropout.csv, version=v1, subset=pooled, model=-, k=k2, column with_dropout |
| AUROC v1 pooled k2, without Dropout | 0.8768 | results/paper/auroc_no_dropout.csv, version=v1, subset=pooled, model=-, k=k2, column without_dropout |
| AUROC v2 b10 model (a) k1, with Dropout | 0.9557 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=a, k=k1, column with_dropout |
| AUROC v2 b10 model (a) k1, without Dropout | 0.9410 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=a, k=k1, column without_dropout |
| AUROC v2 b10 model (a) k2, with Dropout | 0.8814 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=a, k=k2, column with_dropout |
| AUROC v2 b10 model (a) k2, without Dropout | 0.8418 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=a, k=k2, column without_dropout |
| AUROC v2 b10 model (b) k1, with Dropout | 0.9636 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=b, k=k1, column with_dropout |
| AUROC v2 b10 model (b) k1, without Dropout | 0.9515 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=b, k=k1, column without_dropout |
| AUROC v2 b10 model (b) k2, with Dropout | 0.9008 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=b, k=k2, column with_dropout |
| AUROC v2 b10 model (b) k2, without Dropout | 0.8678 | results/paper/auroc_no_dropout.csv, version=v2, subset=b10, model=b, k=k2, column without_dropout |
| AUROC v2 b8 model (a) k1, with Dropout | 0.9681 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=a, k=k1, column with_dropout |
| AUROC v2 b8 model (a) k1, without Dropout | 0.9575 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=a, k=k1, column without_dropout |
| AUROC v2 b8 model (a) k2, with Dropout | 0.8979 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=a, k=k2, column with_dropout |
| AUROC v2 b8 model (a) k2, without Dropout | 0.8638 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=a, k=k2, column without_dropout |
| AUROC v2 b8 model (b) k1, with Dropout | 0.9700 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=b, k=k1, column with_dropout |
| AUROC v2 b8 model (b) k1, without Dropout | 0.9599 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=b, k=k1, column without_dropout |
| AUROC v2 b8 model (b) k2, with Dropout | 0.9043 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=b, k=k2, column with_dropout |
| AUROC v2 b8 model (b) k2, without Dropout | 0.8725 | results/paper/auroc_no_dropout.csv, version=v2, subset=b8, model=b, k=k2, column without_dropout |
| AUROC v2 b9 model (a) k1, with Dropout | 0.9641 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=a, k=k1, column with_dropout |
| AUROC v2 b9 model (a) k1, without Dropout | 0.9521 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=a, k=k1, column without_dropout |
| AUROC v2 b9 model (a) k2, with Dropout | 0.8969 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=a, k=k2, column with_dropout |
| AUROC v2 b9 model (a) k2, without Dropout | 0.8625 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=a, k=k2, column without_dropout |
| AUROC v2 b9 model (b) k1, with Dropout | 0.9663 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=b, k=k1, column with_dropout |
| AUROC v2 b9 model (b) k1, without Dropout | 0.9551 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=b, k=k1, column without_dropout |
| AUROC v2 b9 model (b) k2, with Dropout | 0.9060 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=b, k=k2, column with_dropout |
| AUROC v2 b9 model (b) k2, without Dropout | 0.8746 | results/paper/auroc_no_dropout.csv, version=v2, subset=b9, model=b, k=k2, column without_dropout |


## Sanity checks and per-sensor false alarms

Read from existing files only (no new run, no Test re-read). Batch identity: logistic regression, 5-fold stratified CV, predicting the batch id from the preprocessed Train features (results/audit/sanity_checks.py); chance = share of the largest batch. Per-sensor false-alarm rate: share of the clean Test rows in which the sensor is flagged by the frozen v1 'median' detector (design rate on OOF Train: 5%). See results/paper/METHODS_FACTS.md.

| number | value | source |
|---|---|---|
| Batch-identity CV accuracy, Train 1-6 | 0.9823 | results/audit/sanity_checks.json, temporal.batch_identity_cv_accuracy |
| Batch-identity chance level (largest batch share), Train 1-6 | 0.3878 | results/audit/sanity_checks.json, temporal.batch_identity_chance_majority |
| Batch-identity CV accuracy, Drift-Dev Train 1-3 | 0.9862 | results/audit/sanity_checks.json, drift_dev.batch_identity_cv_accuracy |
| Batch-identity chance level (largest batch share), Drift-Dev Train 1-3 | 0.4847 | results/audit/sanity_checks.json, drift_dev.batch_identity_chance_majority |
| Clean false-alarm rate S01, Test pooled | 0.5023 | results/final_test/test/ft_reliability_ranking.csv, subset=pooled, detector=median, sensor=S01, column alarm_rate |
| Clean false-alarm rate S02, Test pooled | 0.1134 | results/final_test/test/ft_reliability_ranking.csv, subset=pooled, detector=median, sensor=S02, column alarm_rate |
| Clean false-alarm rate S08, Test pooled | 0.2713 | results/final_test/test/ft_reliability_ranking.csv, subset=pooled, detector=median, sensor=S08, column alarm_rate |
| Clean false-alarm rate S01, Test b8 | 1.0000 | results/final_test/test/ft_reliability_ranking.csv, subset=b8, detector=median, sensor=S01, column alarm_rate |
| Clean false-alarm rate S02, Test b8 | 0.9830 | results/final_test/test/ft_reliability_ranking.csv, subset=b8, detector=median, sensor=S02, column alarm_rate |
| Clean false-alarm rate S08, Test b8 | 0.0340 | results/final_test/test/ft_reliability_ranking.csv, subset=b8, detector=median, sensor=S08, column alarm_rate |
| Clean false-alarm rate S01, Test b9 | 0.1255 | results/final_test/test/ft_reliability_ranking.csv, subset=b9, detector=median, sensor=S01, column alarm_rate |
| Clean false-alarm rate S02, Test b9 | 0.2404 | results/final_test/test/ft_reliability_ranking.csv, subset=b9, detector=median, sensor=S02, column alarm_rate |
| Clean false-alarm rate S08, Test b9 | 0.2872 | results/final_test/test/ft_reliability_ranking.csv, subset=b9, detector=median, sensor=S08, column alarm_rate |
| Clean false-alarm rate S01, Test b10 | 0.5108 | results/final_test/test/ft_reliability_ranking.csv, subset=b10, detector=median, sensor=S01, column alarm_rate |
| Clean false-alarm rate S02, Test b10 | 0.0258 | results/final_test/test/ft_reliability_ranking.csv, subset=b10, detector=median, sensor=S02, column alarm_rate |
| Clean false-alarm rate S08, Test b10 | 0.2886 | results/final_test/test/ft_reliability_ranking.csv, subset=b10, detector=median, sensor=S08, column alarm_rate |
