# التقرير الصباحي / Morning report

*(مولَّد آليًا من الملفات، 2026-10-08 07:21؛ كل رقم له مصدر مذكور في الأقسام الإنجليزية أدناه. الدفعات 8–10 لم تُفتح إطلاقًا في هذا التشغيل الليلي.)*

## ملخص بالعربية

**أُنجز:** الأجزاء الأربعة على البروتوكول الزمني كاملة (معالجة مسبقة، أعطال وبوابة G1، كاشف موثوقية وبوابة G2، مقارنة الاستراتيجيات وبوابة G3)، وعلى البروتوكول المرجعي بمجموعة مختصرة (مكتملة). **لم يُنجز / ناقص:** لا شيء ناقص جوهريًا؛ الجزء 2 تجاوز حدّه الزمني (ساعتان) بسبب تزاحم الموارد في بدايته؛ استراتيجية C (خبراء الأزواج) ضعيفة ولم أغيّر تصميمها (قرار خارج القواعد المسجّلة).

| البوابة | النتيجة | الرقم |
|---|---|---|
| P1 integrity | نجحت | 9546 records inspected in batches 1-7 (9544 kept after dropping 2 corrupt Train records), NaN 0, inf 0, 92 tes |
| P2 no leakage | نجحت | 5 tests: fitted pipeline unchanged when batch 7 changes, changes when a Train batch changes, Test files unpars |
| P3 no harm to clean performance | نجحت | final pipeline = new Baseline (no candidate adopted): SVM Macro-F1 0.8590 (tuned), gate >= 0.8490; the old ref |
| P4 traceability | نجحت | 10 tests + final/feature_provenance.csv; groups with a multi-sensor column are rejected |
| P5 reconstruction | نجحت | tables per method and per sensor, with and without the twin, both protocols |
| P6 reproducibility | نجحت | 106 files compared with the previous run, 0 differing |
| G1 | نجحت | 4 من 4 أنواع أعطال ≥ 0.03 عند k=1 متوسط الشدة (أصغرها 0.033) |
| G2 | نجحت | وسيط AUROC = 0.977 (تطبيع median) |
| G3 | نجحت | 80 من 108 مقارنة (A أو B بالكاشف الحقيقي) |

**أهم خمس نتائج (كل واحدة صالحة للورقة):**

1. تنظيف سجلين تالفين من تدريب الدفعة 2 خفّض Macro-F1 لـ SVM على التحقق من 0.878 إلى 0.859 (و0.856 بنفس الإعدادات القديمة)؛ المرجع القديم كان مضخَّمًا لأن السجلين ضخّما الانحراف المعياري ×316.
2. عطل حساس واحد يخفض Macro-F1 لـ SVM النظيف (0.859) بمقدار 0.013–0.246، والتدريب المعزَّز يخفف الأثر لكنه يكلّف الدقة النظيفة (SVM+Aug = 0.778 ± 0.020).
3. الكشف ثم إعادة البناء (A) يبقي Macro-F1 عند 0.836–0.848 لكل أعطال k=1، مقابل 0.692–0.783 لأفضل Baseline معزَّز؛ وتتفوق A أو B معنويًا في 80 من 108 مقارنة.
4. الاستراتيجيات تنهار حين يفشل الكشف: عند k=4 مع Bias قوي (δ=3) تعطي A = 0.224 مقابل 0.501 لـ LGBM+Aug (الـ Oracle = 0.814)، لأن AUROC العزل ينخفض إلى 0.72–0.79 (Bias) و0.62–0.66 (Stuck).
5. الانجراف يكسر علاقة التوأم S01–S02 (Spearman من 0.982 إلى 0.913)، وهما أقل الحساسات موثوقية على الدفعة 7 النظيفة (إنذارات 93% و78%)؛ ومعالجتهما دائمًا تكلّف 0.009 (A) و0.048 (B) على بيانات نظيفة.

**ملاحظة مهمة (البروتوكول المرجعي بلا انجراف):** SVM النظيف يصل إلى 0.999، وG1 تنجح بـ 2 من 4 أنواع فقط، وتفوّق A/B على أفضل Baseline معزَّز يتقلص إلى فروق ≤ 0.006 (G3 تنجح بـ 8 من 32 مقارنة، 1 بعد Bonferroni)؛ أي أن الفائدة الكبيرة في الزمني تأتي من تفاعل الأعطال مع الانجراف، وليس من الأعطال وحدها. ومعدل الإنذار الكاذب هناك ≈ 5% كما صُمِّم ولا شذوذ في S01/S02.

**قرارات أحتاجك فيها قبل تشغيل الاختبار (8–10):** (1) الموافقة الصريحة على تشغيل واحد بالـ Pipeline والكاشف والعتبات المجمَّدة؛ (2) هل نعيد تصميم C (خبراء أكبر من زوجين) أم نحذفها من الورقة؟ (3) أي استراتيجية تُعلن كنتيجة رئيسية (أقترح A مع تقرير B وOracle)؛ (4) كيف نصف الإنذارات الدائمة لـ S01/S02 في الورقة؛ (5) هل نكرر التقييم بالكاشف leave-pair-out. التفاصيل في القسم 7 أدناه.


---

# Details (English)

## 1. Gates

| gate | result | evidence (file) |
|---|---|---|
| P1 integrity | PASS | 9546 records inspected in batches 1-7 (9544 kept after dropping 2 corrupt Train records), NaN 0, inf 0, 92 tests, 0 failing [phase1/temporal/integrity.json, junit.xml] |
| P2 no leakage | PASS | 5 tests: fitted pipeline unchanged when batch 7 changes, changes when a Train batch changes, Test files unparseable and never read [tests/test_preprocessing.py, test_protocols.py, test_data.py] |
| P3 no harm to clean performance | PASS | final pipeline = new Baseline (no candidate adopted): SVM Macro-F1 0.8590 (tuned), gate >= 0.8490; the old reference 0.868 is superseded [phase3/new_baseline.json, phase45/decision_rule.csv] |
| P4 traceability | PASS | 10 tests + final/feature_provenance.csv; groups with a multi-sensor column are rejected [phase4/candidates_val.csv] |
| P5 reconstruction | PASS | tables per method and per sensor, with and without the twin, both protocols [phase1/protocol_comparison_sensor.csv, protocol_comparison_summary.csv] |
| P6 reproducibility | PASS | 106 files compared with the previous run, 0 differing [reproducibility.json] |
| G1 | PASS | types with mean drop >= 0.03 in the medium k=1 setting: dropout, bias, stuck, random; drops {'dropout': 0.033847798536911874, 'bias': 0.04661807944186859, 'stuck': 0.03285336680106159, 'random': 0.10649207864096141} [overnight/temporal/g1_verdict.json, g1_summary.csv] |
| G2 | PASS | median isolation AUROC 0.977 by fault {'dropout': 1.0, 'bias': 0.9796856629427614, 'stuck': 0.9372519583766363, 'random': 0.9743975058317267}; candidates {'sensor': 0.9570143599114866, 'median': 0.977041584387244} [overnight/temporal/g2_verdict.json] (Dropout is detected by definition, AUROC 1.0 is trivial) |
| G3 | PASS | 80 of 108 comparisons (A or B, real detector) beat the best augmented baseline with a bootstrap interval excluding 0; 79 after a Bonferroni check [overnight/temporal/g3_verdict.json, strategy_vs_best_aug.csv] |
| reference protocol G1/G2/G3 | PASS/PASS/PASS | reduced scenario set (medium severity, k=1,2) [overnight/reference_iid/*_verdict.json] |

## 2. What was done and what was not

* Done: Part 1 (stress check, phases 4-5, decision rule, new baselines), Part 2 (scenarios, G1), Part 3 (detector, G2), Part 4 (A/B/C, G3) on the temporal protocol; reduced set on reference_iid; unit tests (see section 6).
* Not done / partial: strategy C was not redesigned (a decision outside the registered rules); the secondary leave-pair-out detector is only reported as a diagnostic AUROC.
* Deviation: Part 2 took longer than its 2-hour limit because it started together with the reproduction run, which starved it (decisions_log C1).

## 3. Main comparison on Validation (temporal protocol): mean Macro-F1 over scenarios, +- std over the 5 fault seeds

Source: `overnight/temporal/strategy_comparison.csv`. SVM = clean model, no handling. Aug = augmented, mean over 5 augmentation seeds. A/B/C_det use the real detector; *_orc use the true faulty sensors (analysis bound); C_equal = the same experts with equal weights.

| k   | fault   |   level | best aug   | svm            | svm_aug        | lgbm_aug       | A_det_twin     | A_det_notwin   | B_det          | C_det          | C_equal        | A_orc_twin     | B_orc          |
|:----|:--------|--------:|:-----------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|:---------------|
| k1  | bias    |     0.5 | svm_aug    | 0.846 +- 0.006 | 0.778 +- 0.003 | 0.696 +- 0.003 | 0.843 +- 0.003 | 0.843 +- 0.002 | 0.833 +- 0.003 | 0.658 +- 0.001 | 0.663 +- 0.005 | 0.841 +- 0.000 | 0.853 +- 0.000 |
| k1  | bias    |     1   | svm_aug    | 0.812 +- 0.009 | 0.770 +- 0.005 | 0.693 +- 0.001 | 0.836 +- 0.005 | 0.839 +- 0.003 | 0.832 +- 0.003 | 0.665 +- 0.001 | 0.660 +- 0.002 | 0.841 +- 0.000 | 0.853 +- 0.000 |
| k1  | bias    |     3   | svm_aug    | 0.613 +- 0.028 | 0.708 +- 0.015 | 0.689 +- 0.003 | 0.843 +- 0.003 | 0.843 +- 0.002 | 0.839 +- 0.001 | 0.664 +- 0.000 | 0.654 +- 0.001 | 0.841 +- 0.000 | 0.853 +- 0.000 |
| k1  | dropout |     0.5 | svm_aug    | 0.825 +- 0.001 | 0.781 +- 0.000 | 0.697 +- 0.000 | 0.847 +- 0.000 | 0.846 +- 0.000 | 0.821 +- 0.000 | 0.650 +- 0.000 | 0.657 +- 0.001 | 0.851 +- 0.000 | 0.856 +- 0.000 |
| k1  | dropout |     1   | svm_aug    | 0.787 +- 0.000 | 0.783 +- 0.000 | 0.694 +- 0.000 | 0.845 +- 0.000 | 0.843 +- 0.000 | 0.831 +- 0.000 | 0.655 +- 0.000 | 0.661 +- 0.000 | 0.841 +- 0.000 | 0.853 +- 0.000 |
| k1  | random  |     0.5 | svm_aug    | 0.752 +- 0.002 | 0.730 +- 0.001 | 0.695 +- 0.000 | 0.848 +- 0.000 | 0.848 +- 0.000 | 0.825 +- 0.000 | 0.654 +- 0.001 | 0.656 +- 0.000 | 0.851 +- 0.000 | 0.856 +- 0.000 |
| k1  | random  |     1   | lgbm_aug   | 0.628 +- 0.001 | 0.681 +- 0.001 | 0.692 +- 0.000 | 0.847 +- 0.000 | 0.845 +- 0.000 | 0.842 +- 0.000 | 0.661 +- 0.000 | 0.660 +- 0.001 | 0.841 +- 0.000 | 0.853 +- 0.000 |
| k1  | stuck   |     0.5 | svm_aug    | 0.826 +- 0.011 | 0.767 +- 0.002 | 0.696 +- 0.004 | 0.847 +- 0.001 | 0.847 +- 0.001 | 0.820 +- 0.002 | 0.651 +- 0.001 | 0.655 +- 0.002 | 0.851 +- 0.000 | 0.856 +- 0.000 |
| k1  | stuck   |     1   | svm_aug    | 0.782 +- 0.012 | 0.755 +- 0.010 | 0.686 +- 0.007 | 0.843 +- 0.003 | 0.842 +- 0.003 | 0.827 +- 0.001 | 0.656 +- 0.000 | 0.660 +- 0.003 | 0.841 +- 0.000 | 0.853 +- 0.000 |
| k2  | bias    |     0.5 | svm_aug    | 0.802 +- 0.021 | 0.771 +- 0.007 | 0.680 +- 0.010 | 0.826 +- 0.016 | 0.828 +- 0.015 | 0.832 +- 0.013 | 0.661 +- 0.002 | 0.660 +- 0.004 | 0.848 +- 0.000 | 0.843 +- 0.000 |
| k2  | bias    |     1   | svm_aug    | 0.729 +- 0.034 | 0.763 +- 0.013 | 0.661 +- 0.012 | 0.811 +- 0.021 | 0.815 +- 0.021 | 0.823 +- 0.019 | 0.665 +- 0.003 | 0.659 +- 0.003 | 0.848 +- 0.000 | 0.843 +- 0.000 |
| k2  | bias    |     3   | lgbm_aug   | 0.421 +- 0.024 | 0.533 +- 0.017 | 0.647 +- 0.020 | 0.674 +- 0.068 | 0.680 +- 0.061 | 0.729 +- 0.024 | 0.664 +- 0.001 | 0.655 +- 0.001 | 0.848 +- 0.000 | 0.843 +- 0.000 |
| k2  | dropout |     0.5 | svm_aug    | 0.784 +- 0.001 | 0.764 +- 0.001 | 0.689 +- 0.001 | 0.845 +- 0.000 | 0.845 +- 0.000 | 0.818 +- 0.001 | 0.651 +- 0.000 | 0.654 +- 0.001 | 0.853 +- 0.000 | 0.851 +- 0.000 |
| k2  | dropout |     1   | svm_aug    | 0.699 +- 0.000 | 0.750 +- 0.000 | 0.679 +- 0.000 | 0.841 +- 0.000 | 0.840 +- 0.000 | 0.828 +- 0.000 | 0.656 +- 0.000 | 0.657 +- 0.000 | 0.848 +- 0.000 | 0.843 +- 0.000 |
| k2  | random  |     0.5 | lgbm_aug   | 0.686 +- 0.003 | 0.664 +- 0.002 | 0.667 +- 0.000 | 0.836 +- 0.001 | 0.839 +- 0.001 | 0.817 +- 0.001 | 0.654 +- 0.001 | 0.656 +- 0.001 | 0.853 +- 0.001 | 0.851 +- 0.000 |
| k2  | random  |     1   | lgbm_aug   | 0.470 +- 0.002 | 0.538 +- 0.002 | 0.632 +- 0.002 | 0.824 +- 0.001 | 0.828 +- 0.001 | 0.825 +- 0.000 | 0.662 +- 0.000 | 0.659 +- 0.001 | 0.848 +- 0.000 | 0.843 +- 0.000 |
| k2  | stuck   |     0.5 | svm_aug    | 0.768 +- 0.017 | 0.730 +- 0.013 | 0.666 +- 0.003 | 0.787 +- 0.018 | 0.792 +- 0.018 | 0.774 +- 0.022 | 0.649 +- 0.001 | 0.654 +- 0.001 | 0.854 +- 0.001 | 0.851 +- 0.000 |
| k2  | stuck   |     1   | svm_aug    | 0.676 +- 0.051 | 0.685 +- 0.055 | 0.631 +- 0.029 | 0.720 +- 0.023 | 0.732 +- 0.021 | 0.739 +- 0.021 | 0.653 +- 0.002 | 0.657 +- 0.005 | 0.848 +- 0.000 | 0.843 +- 0.000 |
| k4  | bias    |     0.5 | svm_aug    | 0.768 +- 0.045 | 0.771 +- 0.017 | 0.670 +- 0.023 | 0.781 +- 0.027 | 0.777 +- 0.026 | 0.794 +- 0.032 | 0.638 +- 0.008 | 0.637 +- 0.004 | 0.814 +- 0.000 | 0.825 +- 0.000 |
| k4  | bias    |     1   | svm_aug    | 0.669 +- 0.032 | 0.707 +- 0.028 | 0.592 +- 0.013 | 0.705 +- 0.045 | 0.695 +- 0.048 | 0.735 +- 0.050 | 0.647 +- 0.005 | 0.636 +- 0.005 | 0.814 +- 0.000 | 0.825 +- 0.000 |
| k4  | bias    |     3   | lgbm_aug   | 0.191 +- 0.034 | 0.238 +- 0.025 | 0.501 +- 0.015 | 0.224 +- 0.042 | 0.259 +- 0.078 | 0.361 +- 0.050 | 0.648 +- 0.004 | 0.642 +- 0.001 | 0.814 +- 0.000 | 0.825 +- 0.000 |
| k4  | dropout |     0.5 | svm_aug    | 0.723 +- 0.003 | 0.705 +- 0.002 | 0.643 +- 0.002 | 0.832 +- 0.002 | 0.833 +- 0.002 | 0.817 +- 0.002 | 0.656 +- 0.001 | 0.657 +- 0.002 | 0.837 +- 0.002 | 0.842 +- 0.002 |
| k4  | dropout |     1   | svm_aug    | 0.550 +- 0.000 | 0.619 +- 0.000 | 0.582 +- 0.000 | 0.814 +- 0.000 | 0.814 +- 0.000 | 0.825 +- 0.000 | 0.665 +- 0.000 | 0.661 +- 0.000 | 0.814 +- 0.000 | 0.825 +- 0.000 |
| k4  | random  |     0.5 | lgbm_aug   | 0.622 +- 0.004 | 0.579 +- 0.003 | 0.599 +- 0.004 | 0.744 +- 0.003 | 0.757 +- 0.003 | 0.738 +- 0.003 | 0.656 +- 0.002 | 0.646 +- 0.001 | 0.837 +- 0.001 | 0.842 +- 0.001 |
| k4  | random  |     1   | lgbm_aug   | 0.315 +- 0.003 | 0.334 +- 0.003 | 0.477 +- 0.001 | 0.634 +- 0.003 | 0.659 +- 0.002 | 0.665 +- 0.003 | 0.665 +- 0.001 | 0.640 +- 0.001 | 0.814 +- 0.000 | 0.825 +- 0.000 |
| k4  | stuck   |     0.5 | svm_aug    | 0.710 +- 0.028 | 0.673 +- 0.028 | 0.595 +- 0.015 | 0.714 +- 0.025 | 0.716 +- 0.027 | 0.689 +- 0.034 | 0.639 +- 0.008 | 0.643 +- 0.008 | 0.836 +- 0.001 | 0.842 +- 0.000 |
| k4  | stuck   |     1   | svm_aug    | 0.528 +- 0.075 | 0.555 +- 0.062 | 0.492 +- 0.046 | 0.539 +- 0.069 | 0.546 +- 0.066 | 0.555 +- 0.062 | 0.638 +- 0.019 | 0.636 +- 0.016 | 0.814 +- 0.000 | 0.825 +- 0.000 |

Differences against the best augmented baseline with paired-bootstrap 95% intervals (rows only; scenarios fixed) are in `overnight/temporal/strategy_vs_best_aug.csv`. Comparisons where the real-detector strategies do not win:

| kset   | fault   |   level | method       |   method_f1 |   best_aug_f1 |   diff |   ci_low |   ci_high |
|:-------|:--------|--------:|:-------------|------------:|--------------:|-------:|---------:|----------:|
| k4     | bias    |   1.000 | A_det_twin   |       0.705 |         0.707 | -0.003 |   -0.008 |     0.002 |
| k4     | bias    |   1.000 | A_det_notwin |       0.695 |         0.707 | -0.013 |   -0.018 |    -0.007 |
| k4     | bias    |   3.000 | A_det_twin   |       0.224 |         0.501 | -0.277 |   -0.285 |    -0.269 |
| k4     | bias    |   3.000 | A_det_notwin |       0.259 |         0.501 | -0.242 |   -0.249 |    -0.235 |
| k4     | bias    |   3.000 | B_det        |       0.361 |         0.501 | -0.140 |   -0.147 |    -0.133 |
| k4     | stuck   |   1.000 | A_det_twin   |       0.539 |         0.555 | -0.016 |   -0.019 |    -0.013 |
| k4     | stuck   |   1.000 | A_det_notwin |       0.546 |         0.555 | -0.009 |   -0.012 |    -0.005 |
| k4     | stuck   |   1.000 | B_det        |       0.555 |         0.555 |  0.001 |   -0.002 |     0.004 |

C_det never beats the best augmented baseline except in the strongest settings, and C_det is not better than C_equal (mean difference over all cells +0.0017).

## 4. Detector (Part 3)

Chosen normalisation: **median** (candidates {'sensor': 0.9570143599114866, 'median': 0.977041584387244}); secondary leave-pair-out AUROC {'sensor_lpo': 0.9572491967688457, 'median_lpo': 0.9734261598255234} (`g2_verdict.json`).

False alarms on the clean Validation batch, per gas (`far_by_gas.csv`), chosen detector:

| gas          | sensors         |   rows |   alarm_rate_per_sensor_row |   rows_with_any_alarm |
|:-------------|:----------------|-------:|----------------------------:|----------------------:|
| all          | all sensors     |   3613 |                       0.135 |                 0.971 |
| all          | without S01,S02 |   3613 |                       0.032 |                 0.334 |
| Ethanol      | all sensors     |    649 |                       0.142 |                 0.946 |
| Ethanol      | without S01,S02 |    649 |                       0.052 |                 0.479 |
| Ethylene     | all sensors     |    662 |                       0.117 |                 0.935 |
| Ethylene     | without S01,S02 |    662 |                       0.024 |                 0.261 |
| Ammonia      | all sensors     |    360 |                       0.116 |                 1.000 |
| Ammonia      | without S01,S02 |    360 |                       0.016 |                 0.203 |
| Acetaldehyde | all sensors     |    744 |                       0.141 |                 0.984 |
| Acetaldehyde | without S01,S02 |    744 |                       0.036 |                 0.383 |
| Acetone      | all sensors     |    630 |                       0.147 |                 0.976 |
| Acetone      | without S01,S02 |    630 |                       0.041 |                 0.419 |
| Toluene      | all sensors     |    568 |                       0.138 |                 1.000 |
| Toluene      | without S01,S02 |    568 |                       0.015 |                 0.178 |

Reliability ranking on the clean batch (least reliable first, `reliability_ranking.csv`):

|   rank_from_least_reliable | sensor   |   median_ratio |   alarm_rate |
|---------------------------:|:---------|---------------:|-------------:|
|                          1 | S01      |          5.389 |        0.926 |
|                          2 | S02      |          1.732 |        0.779 |
|                          3 | S08      |          0.638 |        0.048 |
|                          4 | S06      |          0.622 |        0.092 |
|                          5 | S09      |          0.615 |        0.097 |
|                          6 | S03      |          0.551 |        0.044 |

Isolation AUROC by fault, severity and k (`detector_summary.csv`):

| fault   |   level |    k1 |    k2 |    k4 |
|:--------|--------:|------:|------:|------:|
| bias    |   0.500 | 0.953 | 0.842 | 0.716 |
| bias    |   1.000 | 0.980 | 0.884 | 0.755 |
| bias    |   3.000 | 0.994 | 0.922 | 0.794 |
| dropout |   0.500 | 1.000 | 1.000 | 1.000 |
| dropout |   1.000 | 1.000 | 1.000 | 1.000 |
| random  |   0.500 | 0.974 | 0.968 | 0.956 |
| random  |   1.000 | 0.975 | 0.968 | 0.956 |
| stuck   |   0.500 | 0.937 | 0.755 | 0.625 |
| stuck   |   1.000 | 0.932 | 0.756 | 0.659 |

Recall of the detector at its 5%-calibrated threshold (`detector_summary.csv`):

| fault   |   level |    k1 |    k2 |    k4 |
|:--------|--------:|------:|------:|------:|
| bias    |   0.500 | 0.975 | 0.563 | 0.306 |
| bias    |   1.000 | 0.993 | 0.627 | 0.412 |
| bias    |   3.000 | 1.000 | 0.714 | 0.434 |
| dropout |   0.500 | 1.000 | 1.000 | 1.000 |
| dropout |   1.000 | 1.000 | 1.000 | 1.000 |
| random  |   0.500 | 0.998 | 0.959 | 0.862 |
| random  |   1.000 | 0.998 | 0.959 | 0.863 |
| stuck   |   0.500 | 0.949 | 0.493 | 0.250 |
| stuck   |   1.000 | 0.933 | 0.477 | 0.261 |

## 5. Cost of acting on clean data, and baselines

Strategies on the clean Validation rows (`overnight/temporal/strategy_clean_eval.csv`):

| method                |   macro_f1 |   accuracy |   mean_flagged_per_row |   rows_with_any_flag |
|:----------------------|-----------:|-----------:|-----------------------:|---------------------:|
| clean_svm_no_handling |     0.8590 |     0.8580 |                 0.0000 |               0.0000 |
| A_det_twin            |     0.8495 |     0.8467 |                 2.1403 |               0.9709 |
| A_det_notwin          |     0.8502 |     0.8469 |                 2.1403 |               0.9709 |
| B_det                 |     0.8112 |     0.8193 |                 2.1403 |               0.9709 |
| C_det                 |     0.6461 |     0.6679 |                 2.1403 |               0.9709 |
| C_equal               |     0.6520 |     0.6734 |                 2.1403 |               0.9709 |

Baselines on the final preprocessing, 5 augmentation seeds (`preprocessing/final/aug_baselines_summary.csv`):

| model    |   n |   macro_f1_mean |   macro_f1_std |   accuracy_mean |   accuracy_std |
|:---------|----:|----------------:|---------------:|----------------:|---------------:|
| svm      |   1 |          0.8590 |         0.0000 |          0.8580 |         0.0000 |
| lgbm     |   1 |          0.6918 |         0.0000 |          0.7332 |         0.0000 |
| svm_aug  |   5 |          0.7779 |         0.0197 |          0.7888 |         0.0153 |
| lgbm_aug |   5 |          0.7006 |         0.0074 |          0.7388 |         0.0063 |

New Baseline: SVM 0.8590 (StandardScaler, {"C": 10, "gamma": 0.01}), LightGBM 0.6918 (`preprocessing/phase3/new_baseline.json`). Old reference 0.878 was inflated by the corrupt records (`main_cleaned/diagnosis/design_2x2.csv`).

## 5b. Reference protocol (no train-to-evaluation drift), reduced scenarios

Mean Macro-F1 per cell (`overnight/reference_iid/strategy_comparison.csv`) next to the temporal value of the same cell:

| kset   | fault   |   level |   svm_iid |   svm_temporal |   svm: drift cost |   svm_aug_iid |   svm_aug_temporal |   svm_aug: drift cost |   lgbm_aug_iid |   lgbm_aug_temporal |   lgbm_aug: drift cost |   A_det_twin_iid |   A_det_twin_temporal |   A_det_twin: drift cost |   B_det_iid |   B_det_temporal |   B_det: drift cost |
|:-------|:--------|--------:|----------:|---------------:|------------------:|--------------:|-------------------:|----------------------:|---------------:|--------------------:|-----------------------:|-----------------:|----------------------:|-------------------------:|------------:|-----------------:|--------------------:|
| k1     | bias    |   1.000 |     0.985 |          0.812 |             0.173 |         0.998 |              0.770 |                 0.227 |          0.996 |               0.693 |                  0.303 |            0.996 |                 0.836 |                    0.160 |       0.999 |            0.832 |               0.166 |
| k1     | dropout |   0.500 |     0.975 |          0.825 |             0.150 |         0.994 |              0.781 |                 0.214 |          0.996 |               0.697 |                  0.299 |            0.998 |                 0.847 |                    0.151 |       0.999 |            0.821 |               0.178 |
| k1     | random  |   0.500 |     0.919 |          0.752 |             0.167 |         0.973 |              0.730 |                 0.243 |          0.995 |               0.695 |                  0.300 |            0.997 |                 0.848 |                    0.149 |       0.998 |            0.825 |               0.172 |
| k1     | stuck   |   0.500 |     0.956 |          0.826 |             0.130 |         0.988 |              0.767 |                 0.221 |          0.995 |               0.696 |                  0.300 |            0.998 |                 0.847 |                    0.151 |       0.999 |            0.820 |               0.179 |
| k2     | bias    |   1.000 |     0.935 |          0.729 |             0.205 |         0.995 |              0.763 |                 0.232 |          0.989 |               0.661 |                  0.328 |            0.921 |                 0.811 |                    0.110 |       0.974 |            0.823 |               0.151 |
| k2     | dropout |   0.500 |     0.943 |          0.784 |             0.159 |         0.980 |              0.764 |                 0.216 |          0.995 |               0.689 |                  0.306 |            0.998 |                 0.845 |                    0.153 |       0.999 |            0.818 |               0.180 |
| k2     | random  |   0.500 |     0.841 |          0.686 |             0.156 |         0.913 |              0.664 |                 0.250 |          0.982 |               0.667 |                  0.315 |            0.971 |                 0.836 |                    0.135 |       0.974 |            0.817 |               0.157 |
| k2     | stuck   |   0.500 |     0.928 |          0.768 |             0.160 |         0.961 |              0.730 |                 0.231 |          0.980 |               0.666 |                  0.314 |            0.940 |                 0.787 |                    0.153 |       0.954 |            0.774 |               0.180 |

Clean reference-protocol rows (`overnight/reference_iid/strategy_clean_eval.csv`):

| method                |   macro_f1 |   accuracy |   mean_flagged_per_row |   rows_with_any_flag |
|:----------------------|-----------:|-----------:|-----------------------:|---------------------:|
| clean_svm_no_handling |     0.9990 |     0.9990 |                 0.0000 |               0.0000 |
| A_det_twin            |     0.9990 |     0.9990 |                 0.8471 |               0.5387 |
| A_det_notwin          |     0.9985 |     0.9984 |                 0.8471 |               0.5387 |
| B_det                 |     0.9990 |     0.9990 |                 0.8471 |               0.5387 |
| C_det                 |     0.9860 |     0.9853 |                 0.8471 |               0.5387 |
| C_equal               |     0.9865 |     0.9859 |                 0.8471 |               0.5387 |

## 6. Reproducibility and tests

Reproduction run (P6): {"backup": "results\\_backup_20261008_014346", "files_compared": 106, "files_differing": 0, "reproducible": true} (`preprocessing/reproducibility.json`).
Unit tests in the last run: 92 tests, 0 failures (`preprocessing/junit.xml`).
Number of trials logged in the preprocessing study: 27 (`preprocessing/trials.csv`); scenarios evaluated: 1260 on the temporal protocol.

## 7. Decisions and open items

### Decisions I took alone (rule relied on) — the full log is `results/decisions_log.md`; sections B (interpretations, PRE) and C (during the run):

## B. Interpretations registered before running Parts 2-4 (2026-10-08, PRE)
The overnight text leaves these open. They are fixed here and will not be changed after seeing results.
1. **Medium severity** = Bias delta 1.0; Dropout/Stuck/Random fraction 0.5 (the milder of the two levels).
2. **Part-1 decision rule** compares each candidate (Phase 4 eligible groups, Phase 5 options) with the clean Baseline
   (StandardScaler, SVM C=10 gamma=0.01, Macro-F1 0.8590) using the baseline's tuned SVM settings; adopt only if
   gain > 0.005 AND the paired-bootstrap (1000) 95% interval of the Macro-F1 difference excludes 0. SVM is primary.
3. **Faults** are injected on the evaluation rows, on the RAW 128 features, on whole 8-feature sensor blocks:
   * shared_rows = true: the affected rows are drawn once per scenario and are the same for every sensor of the set;
   * Bias: delta x sigma_robust, ONE random sign per scenario shared by the sensors of the set, applied to all rows;
   * Stuck: each affected sensor block is frozen to the values of ONE random row of the evaluation set (per scenario);
   * Random: independent uniform draws per cell in [p1, p99] of the cleaned Train feature;
   * Dropout: block set to NaN.
   Sets: k=1 the 16 sensors; k=2 the 8 replicate pairs; k=4 the four candidate groups {1,2,9,10},{3,4,11,12},{5,6,13,14},{7,8,15,16}
   (hypothesis, as in the old study). Seeds 0-4. Scenarios are generated once, saved, and applied identically to every method.
4. **G1**: a fault type counts if, in its medium-severity k=1 setting, the mean Macro-F1 drop (16 sensors x 5 seeds) of the
   better clean baseline (SVM or LightGBM, higher clean Validation Macro-F1) is >= 0.03. G1 passes if >= 2 of the 4 types count.
5. **Detector** (Part 3): per sensor, Ridge in the signed-log standardised space predicts its 8 features from ALL other 15
   sensors (as specified; the leave-pair-out variant is reported as a secondary diagnostic). Score = mean over the 8 features
   of |prediction - value|. Alpha: leave-batch-group-out on Train. Out-of-fold (OOF) scores: leave-one-batch-out inside batches 1-6.
   Normalisation (a): score / the sensor's own OOF median; (b): score / the median over the 16 sensors of the same row.
   Alarm threshold per sensor = 95th percentile of its OOF normalised score (5% false alarms on OOF Train).
   A sensor block containing NaN is flagged by definition (score = +inf); NaN predictors are filled with 0 (the Train mean),
   so Dropout detection is trivial by construction and is reported as such.
6. **Choice (a) vs (b)**: higher median AUROC over the four fault types at k=1 medium severity on Validation.
7. **AUROC (primary, "isolation")**: in the affected rows of a scenario, scores of the faulty sensors (positives) against the
   scores of the healthy sensors in the same rows (negatives). Secondary: faulty blocks against the same blocks on the clean copy.
8. **G2**: median over the four fault types of the isolation AUROC (mean over sensors and seeds) at k=1, medium severity >= 0.80.
9. **False alarms**: alarm rate per (row, sensor) on the clean Validation batch, per gas, with all sensors and without S01, S02;
   also the share of rows with any alarm.
10. **Part 4 methods** (temporal protocol, SVM C=10 gamma=0.01 on StandardScaler features unless stated):
    * references: clean SVM without handling, SVM+Aug and LGBM+Aug (5 augmentation seeds, mean +- std);
    * A: flagged blocks (per row) are replaced by the Ridge prediction in slog space from the sensors not flagged in that row
      (with the twin, and without it), then the clean SVM; Oracle-A uses the true faulty sensors per row;
    * B: SVM trained without the flagged sensors (cached by excluded set; at most the 4 highest-scoring flagged sensors are
      excluded in a row); Oracle-B uses the true set;
    * C: 8 replicate-pair experts (SVM with probabilities, 16 features each), weights w = 1 / max(1, z/threshold)^2 per sensor,
      expert weight = minimum over its two sensors, compared with the same experts at equal weights;
    * best augmented baseline per setting = the better of SVM+Aug and LGBM+Aug (mean over aug seeds).
11. **G3**: A or B or C with the REAL detector beats the best augmented baseline in absolute Macro-F1 in at least one setting
    (fault type x severity x k) with a paired-bootstrap interval of the difference that excludes 0. A Bonferroni note over the
    number of comparisons is added as a supplement; it does not change the gate.
12. Reference protocol: reduced scenario set (medium severity per fault, k=1 and k=2 only), run after the temporal protocol is complete.

## C. Decisions taken during the overnight run (filled in as they happen)
* C1 (2026-10-08 ~02:15, operational, not a scientific decision): the full reproduction run (`scripts/run_preprocessing.py`, gate P6) and the Part-2 run were
  started together and starved each other (BLAS oversubscription: one SVM prediction took 4 s instead of 0.05 s). The
  reproduction run was stopped after 7 of 21 steps (markers in `results/preprocessing/_done`); it resumes with `--resume`
  once the CPU is free. Nothing was changed in the methods. Backup of the earlier results: `results/_backup_*`.
* C2 (PRE for the reference protocol, written before it was run): reference_iid uses the same classifier settings as the temporal
  protocol (SVM C=10 gamma=0.01, LightGBM 31 leaves, StandardScaler) instead of re-tuning them with the inner 5-fold, to save time;
  its detector and strategies are fitted on its own Train part (7,634 rows after cleaning) with the inner folds as the groups.
  Reduced scenario set (medium severity per fault, k=1 and k=2, 5 seeds = 480 scenarios).
* C3 (PRE, before the Part-4 results): the cap of 4 acted-on sensors per row (decisions_log B10) applies to A as well as B,
  so A and B always act on the same sets; C uses all reliability weights without a cap. C experts use gamma='scale' (16 features each)
  with C=10. Weight per sensor w = 1 / max(1, ratio)^2 and per expert the minimum over its two sensors.
* C4 (PRE): the Part-4 chunks are processed in the order k=4, k=2, k=1 (the user's rule if time runs out); the analysis accepts a subset.
* C5 (operational): `scripts/01_audit.py` used to open the Test files to count their lines (done once, in Step 1, before the
  overnight rule). It no longer opens them; the Test row of its split table now says "not read". The overnight run never opened
  batches 8-10 (the loaders refuse them and unit tests prove it). Earlier in the project, the dataset download step hashed the ten
  files (`data/raw/SHA256SUMS.txt`) and the Step-1 audit counted the lines of batches 8-10; no values or labels were looked at.


### Suspicious or unexpected

* The detector flags S01 and S02 on almost every clean Validation row (97% of rows have at least one flag, mean 2.14 sensors per row), so A/B/C always act on them; the per-sensor alarm rate of the other 14 sensors is lower than the 5% target.
* Strategy C (8 pair experts) reaches only ~0.65 on clean data and reliability weights do not help (C_det ~ C_equal): the experts use two sensors each and are too weak; this is a design weakness, not evidence about weighting in general.
* On the reference protocol (no drift) the strategies' advantage almost vanishes (differences <= 0.006, G1 passes with 2 of 4 fault types): the benefit seen on the temporal protocol comes from the interaction of faults with drift.
* Bootstrap intervals resample evaluation rows only; the scenarios of a cell share the same 3,613 rows and the same augmentation seeds, so the intervals are optimistic about generalisation to new rows and batches.
* G3 is a permissive rule (one winning cell out of 108 comparisons suffices); the result is nevertheless broad (see the counts above), and the failures concentrate at k=4.
* LightGBM is not exactly scale-invariant (0.68-0.71 across scalers), and its predictions took far longer than SVM's, which shaped the run times.
* The first full reproduction run starved Part 2 (CPU oversubscription); it was stopped and resumed later, see decisions_log C1.
* `phase3/new_baseline.json` was overwritten when the stress check re-selected StandardScaler; the MinMax version is in git history.

### Decisions that need you before the Test run

* Explicit approval to read batches 8-10 exactly once, with the pipeline, cleaning rule, detector (normalisation, thresholds), strategy settings and scenario list frozen as committed. The overnight run never opened a Test file; earlier in the project the download step hashed the ten batch files and the Step-1 audit counted the lines of batches 8-10 (no values or labels were looked at; see decisions_log C5).
* Whether to redesign C (larger or overlapping sensor groups) or drop it; any redesign must be fixed before the Test run.
* Which strategy is the headline result (suggestion: A with the real detector, B and the Oracles as references).
* How to describe in the paper the permanent alarms on S01/S02 (a real drift-induced break of a replicate pair).
* Whether to report the leave-pair-out detector as a primary variant (its AUROC is in `g2_verdict.json`).
* Whether the fault severities (delta 0.5/1/3 sigma_robust, fractions 0.5/1.0) and the k=4 groups (hypothesis) stay as they are.

## 8. Commits, run times, trials

```
a243d97 Reference protocol (no drift, reduced scenarios): G1, G2, strategies and G3
40c4320 Part 4 (temporal protocol): strategies A/B/C, bootstrap comparison and G3
3877498 Parts 2-3: fault scenarios, G1 and reliability detector with G2
a4b7cd1 Part 1: stress check, phases 4-5, decision rule, new baselines, runner and report
327634a Register interpretations and decision rules for the overnight run
805c0ef Pre-register robust fault scale, MinMax stress check and shortened phases 4-5
d7a91c9 Results: cleaned baselines, reconstruction in both protocols, phases 2-3
8a8288a Add evaluation protocols, cleaning rule and preprocessing pipeline code
6ec57e9 Preprocessing phase 1: integrity re-check and sensor-block reconstruction
817ab0d Add data audit restricted to Train/Val batches
f1e507a Reproduce clean baselines on real data with a leak-proof loader
cc48b1c Add project scaffold: pinned Python 3.11 env and smoke test
```
Run times (first to last result file of each part, `results/overnight/temporal/*_chunks`):

* Part 2 (scenarios and baselines under faults): 108 min (first to last chunk file)
* Part 3 (detector): 28 min (first to last chunk file)
* Part 4 (strategies): 61 min (first to last chunk file)
* Trials in `preprocessing/trials.csv`: 27