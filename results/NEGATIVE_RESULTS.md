# Negative and unconfirmed results

Every idea that failed its pre-registered criterion, or was not confirmed, is listed with the reason and the numbers.

**Common rules for every row**
- Macro-F1 throughout.
- **Dev** = Drift-Dev: train on batches 1–3, evaluate on batches 6 and 7 (mean).
- **Val 7** = train on batches 1–6, evaluate on batch 7.
- The rules are in `results/decisions_log.md`, sections G–L. All v2 work is POST-HOC.

## v1 (pre-registered)
| idea | result | source |
|---|---|---|
| **C: reliability-weighted replicate-pair experts** | Below the plain SVM. Validation clean: C_det 0.646 and C_equal 0.652, vs SVM 0.859. Test pooled clean: 0.405 and 0.410, vs 0.535. Reliability weighting adds nothing over equal weights. | `results/overnight/temporal/strategy_clean_eval.csv`, `results/final_test/TEST_REPORT.md` §2 |
| Gate G1 on Test batch 10 | 0 of 4 fault types lose ≥ 0.03 (k=1, medium), because the clean score is already low (0.489). G1 passes on the pooled Test only at the minimum (2 of 4). | `results/final_test/test/ft_verdicts.json` |

## v2: drift-robust base model, unsupervised (selection rule G6)
| candidate | Dev mean (Δ vs M0, 95% CI) | Val 7 (≥ 0.849 needed) | why it failed | source |
|---|---|---|---|---|
| M0 = v1 model (reference) | 0.618 | 0.859 | (winner by rule) | `results/v2/candidates.md` |
| M1: per-batch robust normalisation | 0.596 [−0.031, −0.014] | 0.652 | Below M0. Per-batch statistics depend on the gas mix of the batch. It also cancels a whole-batch Bias fault (detector AUROC for Bias = 0.50). | `results/v2/candidates.csv` |
| M2: CORAL (new batch mapped to the Train covariance) | 0.374 [−0.254, −0.233] | 0.506 | The implementation is correct: it matches an independent implementation to within 1e-14. The un-centred mapping doubles the batch-mean offset (5.2 → 10.5). The paper's direction is ≈ M0 on Dev (0.612, 0.623) and 0.759 on Val 7. | `results/v2/coral_check.md` |
| M3: per-batch SVM ensemble (Vergara et al.) | 0.593 [−0.031, −0.019] | 0.758 | Below M0. Members trained on small batches without toluene. | `results/v2/candidates.csv` |
| M4: best two of M1–M3 | not built | — | Rule G5: the two best (M1, M3) did not both beat M0. | `results/v2/choice.json` |
| M5: retrain on batches 1–7 | standard practice, not a candidate | — | Used as the Train set of the v2 final test. | `results/decisions_log.md` G5 |

Removing toluene from the Dev scores does not change the order: M0 0.776, M3 0.757, M1 0.735, M2 0.514. M0 recognises 0% of the toluene rows of batches 6 and 7, because Dev-Train holds only 79 toluene rows (`results/v2/toluene_sensitivity.md`).

## v2: hybrid arbiter H1–H3 on M0 (rule G8)
None is adopted. Each falls more than 0.01 below the best single method in at least one setting.

| variant | mean over all scenarios (two protocols) | worst gap to the best single method | source |
|---|---|---|---|
| H1 (0 flags → SVM, 1–2 → A, ≥3 → B + Aug) | 0.7236 | −0.020 | `results/v2/arbiter/choice.json` |
| H2 (0 → SVM, 1 → A, ≥2 → A + B + Aug) | 0.7239 | −0.030 | same |
| H3 (fixed weighted mean of SVM, A, Aug) | 0.7147 | −0.027 | same |
| A alone, for comparison | 0.7357 | — | same |

Reason: under drift almost every row carries an alarm (n_flag = 0 in only 3–13% of rows), so routing by alarm count cannot isolate faulty rows. On clean Val 7 every arbiter loses about 0.02 to the plain SVM.

## v2: improving the fault layer (rule L4: select on Dev, confirm on Val 7)
| variant | Dev: clean / mean under faults / worst | why it failed | source |
|---|---|---|---|
| V0 = v1 A (reference) | 0.646 / 0.6119 / 0.346 | — | `results/v2/improve_light/IMPROVE.md` |
| V1: twin-aware detection (max of v1 and leave-pair-out ratios) | 0.6395 / 0.6104 / 0.382 | Better isolation (k=2 Stuck AUROC 0.72 → 0.83, TPR 0.30 → 0.65), but more false alarms (Dev clean FAR 0.087 → 0.121), so no Macro-F1 gain | same |
| V2: 99th-percentile thresholds | 0.6457 / 0.6097 / 0.365 | Fewer false alarms (0.087 → 0.052) but lower TPR. No Macro-F1 gain. | same |
| V3: V1 with 99th-percentile thresholds | 0.6408 / 0.6091 / 0.364 | No gain | same |
| V5: guarded reconstruction (sensors with ratio > 0.5 excluded from the predictors) | 0.6247 / 0.6088 / 0.394 | Better worst case on Dev and Val 7 (0.494 → 0.556), and higher Val 7 mean under faults (0.8085 vs 0.8043). But Dev clean is −0.021, beyond the 0.005 margin, so it is ineligible. The most promising direction. | same |
| Routing A → B when n_flag ≥ 5 | Val 7 gain +0.0026 [0.0014, 0.0038] | Passed the Val 7 stage, but the Dev confirmation (it needs new reduced B models) was not run: **unconfirmed, not adopted, not in the v2 test** | `results/v2/light/lr_choice.json` |
| Routing A → augmented SVM (any threshold) | gain −0.019 to −0.081 on Val 7 | Worse than A | `results/v2/light/lr_variants.csv` |
| "A as partial drift correction" (descriptive) | clean A − SVM: Dev b7 +0.054, b6 +0.001 (n.s.), Val 7 −0.009 | Not consistent across batches. The b7 gain comes from S01 alone; reconstructing S02 alone costs −0.25 on Val 7. | `results/v2/light/la_clean.csv`, `la_attribution.csv` |

## Lessons
1. Under long-term drift, the unsupervised fixes tried here do not beat the plain model on held-out later batches.
2. **Better fault isolation (AUROC/TPR) does not turn into better classification** when it costs extra false alarms under drift.
3. The worst cases of A come from twin masking: a replicate pair biased together is not flagged, and healthy sensors are reconstructed from the biased pair. B is far more robust in its worst case.

## v4 (POST-HOC): carrying a calibration forward in time (decisions_log R; selection rule R3)
Development only (Drift-Dev Train 1-3; previous-period pairs 5 -> 6 and 6 -> 7; seeds 0-4; 481 scenarios). Score = A, Macro-F1 under faults
(k1/k2 equal), mean of targets 6 and 7. GO needed delta vs prev-analog >= 0.010 with clean SVM not below prev-analog by more than 0.005.
prev-analog = 0.7388 (kept rows) / 0.7363 (H2 rows); same-period = 0.9176; uncalibrated = 0.6297.

| configuration | delta vs prev (t6 / t7) | clean SVM vs prev | why it failed | source |
|---|---|---|---|---|
| W1: calibration memory (all past periods), unweighted | +0.0013 (0.000 / +0.003) | +0.003 | winner by the rule (tie with C1), far below +0.010 | `results/v4_recal/tournament.csv` |
| W5 / W20: memory with weight 5 / 20 | −0.0018 / −0.0036 | +0.004 / +0.001 | up-weighting barely moves the SVM (w=20 changes 5 of 2300 batch-6 labels; only 1 of 13 batch-5 support vectors is at the bound) | same |
| C1: remove the top drift direction | +0.0027 (+0.006 / −0.000) | +0.007 | best delta, still far below +0.010 | same |
| C2: remove the top 2 drift directions | −0.0018 (+0.052 / −0.055) | +0.001 | helps 5 -> 6, hurts 6 -> 7 by the same amount: unstable | same |
| S30: self-training, top 30% margins | −0.0143 | −0.007 | ineligible (clean −0.007) and worse | same |
| S60: self-training, top 60% margins | −0.0010 | +0.007 | no gain | same |

**Decision: NO-GO.** No Test run (`results/v4_recal/r3_decision.json`; the Test stage refused, `test_stage_refusal.log`). v3 (section Q)
stands as the previous-period result.

Lesson 4. Previous-period calibration gives a small gain that barely depends on how old it is (Test, Q9: A under faults +0.024 with 8 -> 9 or
9 -> 10 calibration, +0.021 with 13-14-month-old 8 -> 10 calibration). None of the seven ways of carrying it forward tested here (more memory,
weighting, drift-direction removal, self-training) adds 0.010 on development batches.
