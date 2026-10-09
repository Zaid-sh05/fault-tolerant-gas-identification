# Previous-period recalibration: implementation plan

**Goal:** test decisions_log Q (arm (c) = model calibrated on batch t-1, applied unchanged to batch t) against arms (a) and (b) on identical rows.
**Architecture:** one new script `scripts/v3_prevbatch.py` that imports the frozen v2 code (`ft_v2_recal`, `v2_recal`, `paper_corrections`) and only reads the
fitted v2 models; per-(arm, t, s) prediction chunks are written atomically to `results/v3_prevbatch/`, then scored and tabulated.
**Tech:** Python 3.11, numpy, pandas, scikit-learn 1.8, joblib; Windows, 1 BLAS thread per worker, 3 workers.
**Spec:** `results/decisions_log.md` section Q (commit fe127f5, written before any result).

## Global constraints (from the request)
- New files only: `scripts/v3_prevbatch.py`, `configs/v3_prevbatch.yaml`, `tests/test_v3_prevbatch.py`, `results/v3_prevbatch/**`,
  `results/paper/PAPER_NUMBERS_v3.md`. No edit to frozen code, configs, or `results/{final_test,final_test_v2,overnight,v2}/`.
- Branch `exp/prev-batch-recal`, local commits, no push, tags untouched. OMP/OPENBLAS/MKL = 1.
- Floor (constraint-driven-development, non-interactive): no skipped tests, no suppressed checks, no stubs; the full pytest suite passes.
  A root `CONSTRAINTS.md` is NOT created (outside the allowed files); the floor is applied and recorded here.

## Readiness audit (evidence)
| point | evidence | status |
|---|---|---|
| a. calib_rows covers all gases in b8, b9 | `scripts/v2_recal.py:36-40` (per gas min(n, count//2)); run 2026-10-10: b8 counts {1:30, 2:30, 3:40, 4:33, 5:143, 6:18} -> 10,10,10,10,10,9 (59 rows) for every seed; b9 {61,55,100,75,78,101} -> 10 each (60 rows); b10 600 each -> 10 each | confirmed |
| b. scenarios, faults, seeds | `scripts/ft_v2_recal.py:70-72` (`[None] + build_scenarios(AUG_SEEDS, ("k1","k2"))` = 1081), `:106` (`apply_scenario(X, sc, raw_stats)` on the full batch), `:159` (`raw_stats = FaultStats.fit(Xtr)`, Train 1-7), `configs/final_test_v2.yaml` seeds [0..4] | confirmed |
| c. fitted models present | `results/final_test_v2/test/{uncalibrated, b8_s0..4, b9_s0..4, b10_s0..4}/fitted.joblib` + `reduced/` (1012-1726 cached B models each); keys pre, svm, det (ReliabilityDetector, median), Xtr, ytr, params; Xtr rows: uncal 9543, b8_s0 9602 (= 9543 + 59), b9_s0 9603 (= 9543 + 60). Built by `ft_v2_recal.py:168-174` (Train + `X[calib_rows]`, group CAL_GROUP + b) | confirmed |
| d. scored rows | `scripts/ft_v2_recal.py:75-78` `keep_mask(y, seed, batch)`; used for scoring at `:200-206` | confirmed |

Decisions: section letter Q (P taken); in-place branch instead of a worktree (the 13 GB of ignored v2 models live only in this checkout and are
read by relative path); reduced B models missing from a v2 cache are fitted by the frozen routine into `results/v3_prevbatch/models/`.

## Tasks
- [x] T0 audit, branch, baseline `pytest` (112 passed)
- [x] T1 pre-registration Q committed alone (fe127f5)
- [ ] T2 config + script skeleton (data, arm -> model dir, scored rows) + tests 1-3 written first and failing, then passing
- [ ] T3 smoke (b9, seed 0, 12 scenarios, arms a/b vs v2 chunks)
- [ ] T4 reproduction gate: arms a, b on b9, b10, all scenarios, labels == v2 chunks, F1 == scores.csv (<= 1e-9)
- [ ] T5 arm c run (RUN_STARTED / RUN_FINISHED, log)
- [ ] T6 scoring + TABLES.md + CSVs (Q3, Q4)
- [ ] T7 independent audit subagent + code review
- [ ] T8 PAPER_NUMBERS_v3.md, PREV_BATCH_REPORT.md, full pytest, final commit

## Risks
| risk | mitigation |
|---|---|
| arm c needs reduced B models not in the b{t-1} cache | frozen fit routine, cached in results/v3_prevbatch/models; counted and reported |
| Windows file races between workers | SafeKit pattern + atomic writes |
| memory (b10 = 3600 rows x 1081 scenarios) | chunks of 40 scenarios, 3 workers, int8 labels |
