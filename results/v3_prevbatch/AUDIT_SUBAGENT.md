# Independent audit: previous-period recalibration (decisions_log Q)

Auditor: independent subagent, 2026-10-10, branch `exp/prev-batch-recal` at `7a81a90`. I had read-only access except for this file.
My helper scripts are outside the repository, in the session scratchpad `audit/` folder: `audit_endpoint.py`, `audit_leak.py`,
`audit_repredict.py`, `audit_compare.py`, `audit_doubts.py` and `audit_testfits.py`.
I computed my numbers (step 3a/3b) before I opened `q3_primary.csv`, `q4_*.csv`, `TABLES.md` or `scores.csv`.
One exception: `run.log` was on the list of timeline files to check, and its last line prints the P3 value. I read it during the
timeline check, before my own computation. My own computation imports only `load_data` (labels) and `scenario_list` (scenario
definitions). The calibration rows, Macro-F1, k-balanced mean, bootstrap and t-interval are my own code. I checked my Macro-F1
against sklearn `f1_score` on 20 random cells (|diff| < 1e-12).

## Timeline

| event | time (+0300, 2026-10-10) | evidence |
|---|---|---|
| Pre-registration `fe127f5` "Q: pre-register previous-period recalibration" | 00:56:59 | `git show --stat`: 1 file, `results/decisions_log.md`, +47 lines. The whole hunk is the new section Q, appended after P. |
| PLAN.md / configs/v3_prevbatch.yaml written | 00:57:21 / 00:58:50 | file mtimes |
| Unit tests predict 2 arm-(c) scenarios (c, t=9, s=0, sids 0, 1), in memory only | 01:00:22 | 20 files in `models/b8_s0/reduced` were created before `1c3066d` |
| Script + tests committed `1c3066d` | 01:01:29 | |
| Smoke run | 01:02:02 | smoke.log; 0 label mismatches |
| Gate run starts | 01:03:02 | gate.log; first a_b9 chunk 01:03:21 |
| Loky / clean.csv fix committed `3641533` | 01:05:49 | |
| gate.json written (passed) | 01:31:34 | mtime; `"passed": true`, labels identical, max dF1 1.1e-16, clean diff 0 at 4 decimals |
| Gate commit `d5df331` (adds gate.json) | 01:32:02 | |
| RUN_STARTED / run.log "run: arm c" | 01:32:11 | file content and log |
| First arm-(c) prediction chunk (`c_b9_s0/chunk_000.pkl`) | 01:32:22 | getmtime/getctime of all 280 c chunks: min 01:32:22, max 02:18:12 |
| RUN_FINISHED; results commit `7a81a90` | 02:18:12; 02:24:51 | |

The pre-registration came first. It was committed alone, touching only `decisions_log.md`, about 35 minutes before the first arm-(c)
output. It came about 3.5 minutes before the unit tests' in-memory arm-(c) predictions, which printed no metric. The gate commit and
`passed: true` came 9 s before RUN_STARTED.

Remarks, all non-blocking:
- The gate that produced gate.json **started at 01:03:02 on working-tree code that was committed only at 01:05:49** (`3641533`).
  gate.json uses the key names introduced by that commit (`clean_csv_rows_compared`, `clean_max_abs_diff_at_4_decimals`), so the gate
  ran the post-fix code. I cannot prove byte-for-byte that the committed file equals what ran. The commit message says the first
  attempt crashed before any comparison, so the loosened clean.csv check (1e-9 changed to "equal at 4 decimals") was not driven by
  results. The old check could never have passed against a 4-decimal CSV.
- Unit-test fits in `models/b8_s0/reduced` (20 files, 01:00:22) predate the script commit. I re-fitted 3 of them fresh with the frozen
  recipe: support vectors and dual coefficients are identical. **This does not matter**: they are deterministic fits from the same
  data, and they postdate the pre-registration.
- `results/audit/clone_dir.txt` is untracked. It was already present when I started, and I did not create it.

## Tests and leakage

`.venv\Scripts\python -m pytest tests/test_v3_prevbatch.py -v`: **4 passed** in 5.3 s, with no skips.

How well the tests cover each requirement:
1. **No batch-t row in the arm-(c) training/calibration data.** This is really tested.
   `test_arm_c_training_rows_contain_no_row_of_the_target_batch` checks byte equality of every Xtr row against batch t, for all
   10 (t, s). It also checks exactly that `Xtr == vstack(Train, X_{t-1}[calib_rows])` and `ytr` likewise. Two things are not tested:
   the reduced B models (from the v2 cache of b{t-1}_s{s}, or fitted new) and the preprocessor. Both are derived from that same
   `Xtr` by construction.
2. **Identical scored rows across arms.** This test is weak, close to tautological. `scored_rows(arm, t, s, y)` ignores `arm`, so the
   test only checks that `keep_mask` is deterministic. The real guarantee is structural: `score_rows` calls `scored_rows("a", ...)`
   once per seed and uses those rows for every arm. I confirmed it numerically (see below).
3. **Detector = stored t-1 detector, never refit.** This is reasonably tested. Group ids contain 1000+(t-1) and not 1000+t, and
   `nb_` equals the number of calibration rows, for all (t, s). `ReliabilityDetector.fit` is monkeypatched to raise, and `tau_` is
   unchanged, but only over 2 scenarios of (c, 9, 0).

My own checks (`audit_leak.py`, `audit_repredict.py`, `audit_testfits.py`):
- For all 10 arm-(c) models, Xtr is 9543 Train rows plus 59 calibration rows (b8) or 60 (b9). The match is exact with my own
  re-implementation of `calib_rows`. **0 batch-t rows** are in Xtr. Detector calibration groups are `[1008]`, nb=59 (t=9) and
  `[1009]`, nb=60 (t=10). There are no exact duplicate rows between batches 8/9/10, or between Train and batches 9/10. The
  preprocessor is a plain standard scaler (no transductive step).
- The keep masks from my own `calib_rows` equal `keep_mask` for every (t, s), with len = n - 60.
- Saved predictions: all 22 keys have 28 chunks. The sids are exactly 0..1080. Shapes are (1081, n_rows of batch t) with n = 470 or
  3600, so every row of the full batch is predicted. Labels are within the gas set. The `model` field of every chunk names the right
  model: a = uncalibrated, b = b{t}_s{s}, c = b{t-1}_s{s}. 0 chunks are wrong.
- I re-predicted 5 arm-(c) scenarios with the stored t-1 model, using my own scratch cache, so every reduced B model was a fresh fit:
  c_b9_s3 sids 0, 681 (k1), 946 (k2), and c_b10_s1 sids 0, 493 (k1). SVM came from sklearn `svm.predict`. **0 mismatches** for SVM, A
  and B on all rows. The detector `tau_` was unchanged after prediction. So the saved arm-(c) labels come from the stored t-1 detector
  and model, and the cached reduced models equal fresh frozen fits.
- No file under results/final_test, final_test_v2 (including the git-ignored `reduced/` caches), overnight, v2 or configs was created
  or modified after 2026-10-09 23:17, except the new `configs/v3_prevbatch.yaml`. I scanned 46,880 files. `git diff main...HEAD --stat`
  touches only `configs/v3_prevbatch.yaml`, `results/decisions_log.md` (+47, section Q), `results/v3_prevbatch/*`,
  `scripts/v3_prevbatch.py` and `tests/test_v3_prevbatch.py`.

## Independent recomputation

### My numbers (computed before opening the author's tables)

**Primary endpoint (Q3), A under faults, (c) - (a), pooled b9+b10: +0.024814, 95% CI [+0.023543, +0.026007]. The lower bound is above 0, so SUPPORTED.**

| A under faults, (c)-(a) | value | 95% CI |
|---|---|---|
| b9 | +0.023751 | [+0.021071, +0.026467] |
| b10 | +0.024356 | [+0.023060, +0.025620] |
| pooled | +0.024814 | [+0.023543, +0.026007] |

| pooled, mean over 5 seeds | arm a | arm b | arm c |
|---|---|---|---|
| clean (sid 0) SVM Macro-F1 | 0.686364 | 0.834286 | 0.704072 |
| A under faults (k-balanced) | 0.636399 | 0.783648 | 0.661213 |
| B under faults | 0.642346 | 0.802007 | 0.671567 |
| SVM under faults | 0.529319 | 0.657727 | 0.553858 |

### Comparison with the author's tables

| file | rows (author / mine / matched) | max abs difference |
|---|---|---|
| q3_primary.csv (value, ci_low, ci_high; verdict SUPPORTED) | 1/1/1 | 1.5e-07 |
| q4_levels_faults.csv | 27/27/27 | 5.0e-07 |
| q4_diffs_faults.csv | 45/45/45 | 5.0e-07 |
| q4_clean.csv (t over seeds) | 54/54/54 | 5.0e-07 |
| q4_retention_worst.csv | 27/27/27 | 4.8e-07 |
| scores.csv, all rows against my own F1 | 145,935 | 1.1e-16 |

The differences are only the author's rounding to 6 decimals. The bootstrap intervals match exactly. I drew the indices with
`rng.integers` and the author with `rng.choice`, which consume the same stream.

Spot check against scores.csv (3 random cells, own F1 against author f1):

| arm, subset, seed, method, sid | mine | author |
|---|---|---|
| c, b9, 0, A, 395 | 0.7547613138954147 | identical |
| b, b9, 1, A, 383 | 0.9768706129813028 | identical |
| c, pooled, 3, B, 779 | 0.7071999637872559 | identical |

**I found no disagreement in any recomputed number.**

## Code review (scripts/v3_prevbatch.py, tests/test_v3_prevbatch.py)

### Critical
None found. There is no leakage, no wrong model per arm and no row misalignment. The pooled set is built correctly (union of each
batch's kept rows, each batch predicted by its own arm model, labels concatenated in the same order). The bootstrap is the
registered `shared_boot`, and the verdict rule is `ci_low > 0`. I verified each of these independently above.

### Important
- **Retention is not "averaged like the Macro-F1" (J6).** J6 (decisions_log l.287) says retention is "averaged like the Macro-F1",
  meaning k1 and k2 weighted equally (N5). `tables()` computes `(gs.f1 / c).mean()` over all 1080 fault scenarios, so k1 gets 2/3 of
  the weight. This copies the frozen `ft_v2_tables.py:44`, so it is consistent with the v2 tables but not with J6's text. The effect
  is up to 0.022 (pooled A: 0.9634/0.9678/0.9743 unweighted against 0.9463/0.9548/0.9586 k-balanced for a/b/c). It affects only
  secondary, descriptive numbers, not Q3.
- **The row-identity test is tautological.** `scored_rows` ignores its `arm` argument, so `test_scored_rows_are_identical_across_arms`
  cannot fail for an arm-specific bug. Neither the test nor the gate checks the identity of rows in the saved scoring. It holds by
  construction and by my recomputation.
- **Chunks are reused without a provenance check.** `run_chunk` skips any existing chunk without checking its content. `load_preds`
  never checks the stored `model`, `arm` or `target` fields. A stale chunk from an earlier mapping or code version would be reused
  silently. For this run, I checked all 616 chunks and every one is correct.

### Minor
- `RUN_STARTED` is overwritten on a re-run without refusal. The v2 script refused, unless resume was logged. `stage_run` checks only
  `gate["passed"]`, not that the gate ran on the current code. The gate itself ran on uncommitted code for 3 minutes (see Timeline).
- Some writes are not atomic and leave file handles to the garbage collector: gate.json, smoke.json, run_info.json and the
  RUN_STARTED/RUN_FINISHED markers. `pickle.dump(out, open(p, "wb"))` inside `atomic()` relies on CPython refcounting to close the
  file before `os.replace`, which Windows requires. The same pattern is in the frozen v2 code.
- `tables()` pairs arms by position after `sort_values(... "sid")`. A missing sid in one arm would misalign silently rather than
  raise. `np.stack` only catches different lengths across seeds.
- The tests write fitted reduced models into the experiment cache `results/v3_prevbatch/models/b8_s0`, a side effect that the run
  reused. They are identical fits, but tests should use a temporary cache. The module-level `skipif` would turn a missing-models
  machine into a silent pass (here, 4 passed and 0 skipped).
- The test for requirement 3 covers 2 scenarios of one (t, s). It monkeypatches only `ReliabilityDetector.fit`.
- Readability: the log line says "P3" for section Q3. The `arm` parameter of `scored_rows` is unused and misleading. `tables()` is one
  70-line function. Many `# noqa: E402` lines.
- Robustness that is fine as written: PrevKit only reads the v2 cache (`joblib.load`, no write path). New fits go through
  `StrategyKit.reduced_model` into `results/v3_prevbatch/models` with the same seed, C and gamma, with an atomic tmp+replace and the
  SafeKit PermissionError fallback. Arm b (t=9) and arm c (t=10) share the `b9_s*` cache dir but ran at different times. The fits are
  deterministic, which I verified by re-fitting.

## Doubts

- **Arm c never beats arm b in a way that matters.** On clean data, c < b for every seed and subset. Under faults, c >= b in 0.4% of
  pooled A scenarios (b9: 1.7%), and c < a in 3.5% (b9: 5.4%). Every per-seed k-balanced (c)-(a) value is positive, in every subset and
  method. For pooled A by seed: 0.0278, 0.0174, 0.0280, 0.0260, 0.0249. Nothing is suspiciously good or bad.
- **The gain is small.** The share of the same-period gain kept is about 17% pooled for A (0.0248 of 0.147).
  - b9: the b8-calibrated model gets F1 = 0 for gas 6 on batch 9 in both arm a and arm c. b8 has only 18 gas-6 rows, so 9 are used
    for calibration. Arm b reaches 0.995.
  - b10: arm c mainly improves gas 1 (clean SVM F1 0.524 to 0.600) and gas 2. It confuses gas 4 with gas 6 more (176 to 263 rows).
- **The pooled value (+0.0248) is larger than both per-batch values (+0.0238, +0.0244).** This is possible because Macro-F1 on the
  union is not an average of the per-batch Macro-F1s (per-class F1 is recomputed on pooled counts, and b10 dominates with 3540 of 3950
  rows). I verified it with per-class F1 tables. It is not a bug.
- **The interval is narrow because it resamples scenarios only** (the O2 limitation, registered in Q6). It conditions on the 5
  calibration draws and on the fixed scored rows. A seed t-interval on the per-seed pooled A differences gives about [+0.019, +0.030],
  still above 0. I did not run a row-level bootstrap.
- **Context:** Q0 registers the design as post-hoc and test-informed. The pre-registration protects the analysis choices, not the
  novelty of the hypothesis.

## Verdict

**The primary-endpoint verdict stands.** My own recomputation gives (c)-(a) A under faults, pooled = **+0.0248, 95% CI [+0.0235,
+0.0260]**. The interval excludes 0, so the verdict is SUPPORTED, and it matches the author to rounding (max |diff| 1.5e-7). Every Q4
table I recomputed matches to below 5e-7, and scores.csv matches to 1e-16.

The timeline is clean: the pre-registration was committed alone, before any arm-(c) output, and the gate passed before RUN_STARTED.
I found no leakage, the arm-(c) model is the stored b{t-1}_s{s} with its own detector, and the scored rows are identical across arms.
I found no Critical issues. The Important issues are:
- the retention weighting departs from J6's text (secondary metric only);
- the row-identity unit test is tautological;
- chunks are reused without a provenance check.

None of them changes Q3. The effect is real but modest, about 17% of the same-period gain.
