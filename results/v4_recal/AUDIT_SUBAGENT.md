# Independent audit of v4 (decisions_log Q9 and R), branch exp/prev-recal-v4

Auditor: independent subagent, 2026-10-10. Scope: commit order and isolation, tests, independent recomputation of the R3 tournament and
one Part 1 (Q9) number, code review. Helper scripts (auditor's own code) and their outputs are in the session scratchpad
(`audit_v4/mtimes.py`, `audit_r3.py`, `audit_refit.py`, `audit_part1.py`, `audit_compare.py`, `*.out`). Nothing was committed, and nothing
in the main checkout was written.

**Exposure before step 3 (disclosure).** I saw two things before my own numbers existed. (1) The subject of commit 8a397a1 ("R3 decision:
NO-GO (winner W1, delta +0.0013 < 0.010); no Test run"), which the required `git log` prints. (2) Fragments of R7, lines 586 and 589 of
decisions_log.md ("R7 (outcome ...)", "Doubt check of the 0.0000 deltas of W5/W20 on target 6: the weights reach the SVM ..."), from a grep
for section headers. I did not open any embargoed file (tournament.csv, TOURNAMENT.md, r3_decision.json, tournament.log, dev_scores.csv,
part1_shelf_life.csv, PART1.md, PAPER_NUMBERS_v4.md, R7, the v4 section of NEGATIVE_RESULTS.md) before step 3. All my numbers come from
code applied to the prediction files, so this exposure could not change them.

## 1. Timeline and isolation

| time (+0300) | event | evidence |
|---|---|---|
| 03:13:18 | slice 1: config, Part 1 code, tests | commit 78ed276 |
| 03:13:52-03:26:32 | arm (e) prediction chunks (140) | mtimes, preds/part1 |
| 03:27:11 | PART1.md written | mtime |
| 03:27:36 | Part 1 commit: Q9 text + Part 1 results | dc0b85f (decisions_log.md, part1_*, PART1.md, .gitignore) |
| 03:27:44 | **R pre-registration** | 283f498: touches **only** results/decisions_log.md (68 lines added, 0 removed) |
| 03:30:41 | slice 2: candidate code, tests, mutation_checks.md | f204166 |
| 03:31:04 | smoke check (same-period b6 s0, 5 scenarios) | smoke.log |
| 03:32:47 | **first dev prediction file** (uncal_b6_s0.pkl) | mtime; 92 dev pkl files in total, the last at 04:34:29 |
| 03:40:20 | devgate.json (19,240 rows, max diff 5.0e-6, passed) | mtime |
| 03:40:40 | dev gate commit | 6eb03a6 |
| 03:40:44 | DEV_STARTED; prev and candidate files 03:42:10-04:34:29 | mtimes |
| 04:38:28 | r3_decision.json, tournament.log | mtimes |
| 04:39:41 | **R3 decision commit** (NO-GO) | 8a397a1 |
| 04:39:50-53 | Test stage run, refused: "R3 decision is NO-GO: no Test run" | test_stage_refusal.log (dir entry 04:39:50, content 04:39:53) |
| 04:40:20, 04:42:28 | R7 + NEGATIVE_RESULTS; PAPER_NUMBERS_v4 (+ an additive `paper` stage) | c4d543d, 67a7c6d |

- **1a. Holds.** The R commit touches only decisions_log.md and comes before every R number: the first dev pkl is 5 min later, then
  devgate.json and DEV_STARTED. R0-R6 were never edited afterwards (later commits only add lines).
- **1b. Holds.** Q9 (dc0b85f) and R (283f498) are separate commits. Q9 was committed together with its results, which matches its own
  label "not pre-registered".
- **1c. Holds.** The decision commit (04:39:41) comes before the only Test-stage invocation (04:39:50), and that invocation refused. There is
  no `results/v4_recal/test/` and no `preds/test/`. Directory mtimes back this up: `results/v4_recal` last changed at 04:39:50 (creation of
  the refusal log) and `results/v4_recal/preds` at 03:32:47 (creation of `preds/dev`). So no test folder was created and then deleted. The
  guard in `stage_test` raises before it creates `test/`. Its git check is real: on this machine both `git ls-files --error-unmatch` and
  `git status --porcelain` match Windows backslash paths. `scripts/v4_recal.py` is identical between f204166 and 8a397a1, so the tournament
  ran on committed code. The only later code change (67a7c6d) adds `paper_numbers` and leaves the tournament logic untouched.
- **1d. Holds.** No file or directory under C:\Users\Admin\icsic2026-gasdrift (including .venv; .git excluded) has an mtime or creation
  time after 2026-10-10 03:08:12. `git -C <main> status --short` shows only `?? results/audit/clone_dir.txt`. main = 67346ca,
  exp/prev-batch-recal = 6a7239e, frozen-before-test = e3fac02, frozen-before-test-v2 = ac6b9a9.
- R6 time box: tournament ended 04:38, 1 h 11 min after the R commit (box: 6 h).

## 2. Tests

`python -m pytest tests/test_v4_recal.py -v -p no:cacheprovider`: **12 passed in 21 s** (test_3b included, since dev_scores.csv exists).

What each test actually guards. I read mutation_checks.md but did not re-run the mutations.

| claim | test | verdict |
|---|---|---|
| no batch-t label in any fit | test_1: scrambles every batch-7 label (kept rows / halves held fixed, as R1 allows), refits all 7 candidates, compares SVM labels, support vectors, dual coefficients and detector thresholds | **Guards it**, for t=7, s=0. It would catch S using true H1 labels and W/C memory containing t (M1, M1b). |
| H1/H2 disjoint, no H2 row in a fit | test_2: disjointness and H1 ∪ H2 = kept for all (t, s); H2 replaced by noise leaves S30/S60 unchanged | **Guards it**. |
| identical scored rows across compared arms | test_3 restates the definition of `comparison_rows` (close to a tautology); test_3b rescores saved labels of the candidate and prev on the comparison rows for 4 cells and matches dev_scores.csv | **Partly**. test_3b is the real check. It does not cover the pairing inside `stage_tournament` (`kbal(df, kind, "prev")`). My full recomputation covers that (section 3). |
| dev never reads batches 8-10 | test_4: records `src.data.load_batch` calls while rebuilding dev data and W5/C1/S30 | **Mostly**. Gap (Minor): `test_data()`/`test_stats()` are lru-cached and already warmed by the Part 1 tests, so a dev path reading Test data through the cache would not be recorded. In practice such a path would crash on the batch keys (5/6/7 vs 8/9/10). |
| Test runs once | test_4b: RUN_STARTED present means refusal | **Guards that single claim**. It does not test the "decision committed" and "NO-GO" refusals. The NO-GO path was exercised for real (refusal log). |
| drift directions from Train + past calibration only | test_5: V recomputed; memory groups exclude t; batch 7 replaced by noise leaves V unchanged | **Guards it**. |
| Part 1: arm (e) = b8 | test_arm_e checks the *content* of `load_v2("b8")`, not that `job_e` calls it with "b8" | **Gap (Minor)**: `job_e` hard-codes the model and writes its own provenance label. My re-prediction closes the gap for the saved files (saved arm (e) labels = b8_s0 re-predicted, 0 mismatches; vs b9_s0, 1,284 / 1,352 mismatches). |

## 3. Independent recomputation

### 3a. R3 tournament (auditor's code: own Macro-F1, own kept rows / H2, own rule written from the text of R3)

Inputs: the 92 saved dev pickles (provenance fields and shapes checked: 481 scenarios × all rows of batch t), labels from
`v2_dev.load("configs/v2_drift_dev.yaml")`, k1/k2 from `v2_arbiter.scenario_info` (320 k1, 160 k2, sid 0 clean).

| config | rows | dev score (A, faults) | prev, same rows | **delta** | delta t6 | delta t7 | clean SVM | **clean - prev** |
|---|---|---|---|---|---|---|---|---|
| W1 | keep | 0.74009 | 0.73876 | **+0.00133** | +0.00000 | +0.00265 | 0.74778 | +0.00328 |
| W5 | keep | 0.73698 | 0.73876 | -0.00178 | +0.00003 | -0.00358 | 0.74867 | +0.00417 |
| W20 | keep | 0.73514 | 0.73876 | -0.00363 | +0.00003 | -0.00728 | 0.74527 | +0.00077 |
| C1 | keep | 0.74148 | 0.73876 | +0.00271 | +0.00586 | -0.00043 | 0.75105 | +0.00655 |
| C2 | keep | 0.73698 | 0.73876 | -0.00178 | +0.05163 | -0.05519 | 0.74521 | +0.00071 |
| S30 | H2 | 0.72201 | 0.73628 | -0.01427 | -0.01102 | -0.01751 | 0.73432 | **-0.00701** (ineligible) |
| S60 | H2 | 0.73523 | 0.73628 | -0.00105 | -0.00632 | +0.00423 | 0.74781 | +0.00648 |

References: uncal 0.62968 (keep), same 0.91756 (keep), prev 0.73876 (keep) / 0.73628 (H2).
Rule: eligible = {W1, W5, W20, C1, C2, S60}. Best eligible delta = C1 +0.00271. W1 (+0.00133) is within 0.002 of it and comes first in the
order, so **winner = W1, delta = +0.00133 < 0.010, NO-GO**. The verdict does not depend on eligibility or the tie rule: no configuration
reaches 0.010 (the maximum over all seven is +0.0027).

Refit check (the saved labels really come from the R2 recipes). With my own assembly (src primitives only, no v4 functions) I refitted
prev, W1, W5, C1 and S60 for (t=7, s=0) and (t=6, s=3) and predicted clean + 9 fault scenarios: **0 label mismatches** for SVM and A in
all 10 model/target combinations.

### 3b. Part 1 (Q9) arm (e), batch 10, kept rows keep_mask(y_10, s, 10) (3,540 rows), shared-index bootstrap

| quantity | auditor | author (part1_shelf_life.csv) |
|---|---|---|
| A under faults, (e) - (a) | +0.020487 [0.019579, 0.021312] | +0.020487 [0.019579, 0.021312] |
| clean SVM, (e) - (a), t over seeds | +0.018398 [0.014093, 0.022702] | +0.018398 [0.014093, 0.022702] |
| A under faults, level (e) / (a) | 0.6416 / 0.6211 | (consistent: share 0.1421 = 0.020487 / 0.144149) |

All 140 arm (e) chunks and 28 arm (a) chunks passed the provenance checks (arm, target, seed, model, sids 0..1080).

### 3c. Comparison with the author's files (opened after 3a/3b)

- tournament.csv vs auditor, every column of the 7 candidates: **max |diff| 5.0e-7** (the CSV is rounded to 6 dp).
- r3_decision.json: same eligible set, winner W1, go = false; winner delta identical (diff 0.0); check_W1_equals_prev_on_target_6 = true,
  which I confirmed independently (identical labels, all 5 seeds).
- dev_scores.csv: **all 125,060 per-scenario Macro-F1 values recomputed, max |diff| 1.1e-16.**
- part1_shelf_life.csv (8 -> 10 row): identical to 6 dp. PAPER_NUMBERS_v4.md quotes the same values (W1 0.0013; arm (e) 0.0205
  [0.0196, 0.0213]).
- R7 and the NEGATIVE_RESULTS v4 table agree with my numbers. The one wording issue is listed under Doubts.

## 4. Code review (scripts/v4_recal.py, tests/test_v4_recal.py)

**Critical: none found.**

Correctness, checked against the text:
- R3 (`stage_tournament`, `kbal`, `clean_svm`): exact. Per (t, s) the k1 and k2 means are averaged, then the mean over seeds and targets;
  delta and clean are computed on the candidate's own rows kind; eligibility >= -0.005; tie within 0.002 resolved in CANDS order (the YAML
  insertion order W1, W5, W20, C1, C2, S30, S60); GO iff >= 0.010. Unrounded values are used for the decision.
- CAND-W: Train + calib rows of M(t), sample_weight w on calibration rows only (w = 1 without weights), unweighted scaler, detector refitted
  with one group per calibration batch. Matches R2.
- CAND-C: scaler on Train + M(t) rows, per-gas d_g over gases present in both, uncentered SVD, projection applied to Train/cal/evaluation
  rows and after reconstruction for A, prev's detector. Matches R2. At t=7 the calibration rows of batches 5 and 6 are pooled per gas,
  which follows R2's wording ("the calibration rows").
- CAND-S: H1/H2 from `default_rng([s, t])`, clean H1 labelled by prev, margin = top-1 minus top-2 of the (default 'ovr') decision_function,
  ceil(q n_c) per predicted class, scaler + SVM refitted on prev rows + kept H1, prev's detector, scored on H2. Matches R2.
- Rows: kept = batch t minus `calib_rows(y_t, 10, s, t)`. Batch 5 is loaded raw, and I checked that the dev eval batches 6/7 from
  proto.eval are byte-identical to a raw load, so the treatment is consistent. Reconstruction uses `exclude_twin=False` (twin allowed, R1).
- Test-stage guards: RUN_STARTED, then "decision tracked and unmodified", then GO; the marker is written only after all three pass. R4 rows
  for the reference arms reuse `comparison_rows(winner)`. Fine (not exercised: NO-GO).

Important:
- *Prediction reuse without content provenance* (`job_dev`, `job_test`, `job_e`: `if not path.exists()`). The provenance checks cover
  domain/key/target/seed/sids only, and the pickles are git-ignored. A file left over from an earlier code version would be reused
  silently, and git alone cannot tie the saved labels to the committed code. **No impact found**: my refits of 5 configurations reproduce
  the saved labels exactly. Suggest storing a hash of the fit rows and weights (or the commit) in each pickle and checking it on load.

Minor:
- `w1_check` (R2's "built-in check") is recorded in r3_decision.json but does not stop the run if false. It was true.
- DEV_STARTED is written but never checked, so a re-run of the tournament is not refused (R6 is enforced by process, not code).
- R3 says r3_decision.json "is committed alone". Commit 8a397a1 also contains TOURNAMENT.md, tournament.csv/log, dev_scores.csv and
  DEV_STARTED (no Test output, so the intent holds).
- Test gaps listed in section 2 (warm `test_data` cache in test_4; `job_e` model choice untested; test_4b covers only the marker).
- Robustness: small JSON/marker files are written non-atomically, and `pickle.load(open(...))`/`json.load(open(...))` leave handles to the
  GC. `atomic()` works in CPython only because the temporary file object is collected before `os.replace`; `with open(...)` would be
  safer on Windows. All paths are relative, so the script must be run from the worktree root.
- Windows/loky: the `worker(name)` indirection (pickling by reference to the imported module) is sound and evidently worked (3 workers).
- Readability: dense comprehension one-liners (`build` for S, `stage_part1` tables, `test_tables`); unused import in `_probe`
  (`fill_nan_zero`).

## 5. Doubts investigated

- **delta_t6 = 0.0000 for W1:** expected by construction (M(6) = {5} = prev's calibration set, w = 1 without weights). Labels identical to
  prev for all 5 seeds.
- **delta_t6 = +0.00003 for W5/W20 (near zero):** explained by SVM optimality. Raising the box bound of rows that are not at the bound
  leaves the optimum unchanged. Per seed (W1 fit, batch-5 calibration rows): s0 has 13 calibration support vectors, 1 at the bound, and the
  W5 SVM differs (13,600 labels over 481 scenarios × 2 methods; 5 clean-SVM labels). s1, s3 and s4 have 0 at the bound and the **W5 SVM is
  identical** to W1. s2 has 0 at the bound by `isclose` and differs in 8 labels (solver tolerance). R7 and NEGATIVE_RESULTS ("the weights
  reach the SVM ... change 5 of 2,300 labels ... 1 of 13 support vectors at the bound") describe **seed 0 only**. For 3 of 5 seeds the
  weights do not reach the SVM at all. This is a wording fix, not a numbers fix.
- **C2 +0.052 on t6, -0.055 on t7:** reproduced by refit for C1; C2 runs the same code with r = 2. The R2 rule allows this behaviour
  (t=6: 5 gases from batch 5 only; t=7: batches 5 and 6 pooled per gas). It is a real instability, not a bug, and is correctly flagged as
  unstable in NEGATIVE_RESULTS.
- **W5 and C2 have the same delta to 5 dp (-0.00178; 0.736984 vs 0.736985):** a coincidence. The per-target deltas and labels differ
  completely.
- **Why self-training fails (post-decision diagnostic, dev labels used only here):** the high-margin pseudo-labels are no more accurate
  than all H1 labels (t7 s0: 0.818 vs 0.812; t6 s3: 0.726 vs 0.729). sklearn's 'ovr' decision_function for SVC is a vote count plus a
  small confidence term, so its top-1 minus top-2 margin is a coarse filter.
- **Ordering of Part 1 and R:** the R text was committed 33 s after the Part 1 results were written (Test-batch results). R says it was
  drafted before any Q9 number was read; git cannot prove that. R0 already labels R as test-informed, and the R decision uses dev data
  only, so the impact is low.
- **NEGATIVE_RESULTS "Lesson 4" wording** ("barely depends on how old it is"): the direct same-target comparison (e) - (c) on b10 is
  -0.0039 [-0.0051, -0.0027]. The interval excludes 0: the 13-14-month calibration keeps about 84% of the 9 -> 10 gain. "Barely" is a
  judgment call, and the 8 -> 9 figure is on a different target batch.
- **Registered caveat, not a defect:** the kept rows (hence H1) depend on batch-t labels through the stratified removal of 60 calibration
  rows (R1 states this). test_1 holds that selection fixed by design.

## 6. Verdict

- **The R3 decision stands.** My code reproduces every tournament number (max diff 5e-7 against the rounded CSV, 1e-16 per scenario),
  the eligible set, the winner (W1 by the tie rule over C1) and **NO-GO**. The verdict is robust: no configuration comes within 0.007 of
  the 0.010 threshold. Five candidate fits rebuilt from R2's text reproduce the saved labels exactly.
- **The "no Test run" claim is true.** There is no `test/` or `preds/test/` folder, the directory mtimes show none was created and
  removed, the only Test-stage invocation refused on NO-GO after the decision commit, and the main checkout is untouched (status, branch
  tips and tags as expected; no file newer than 03:08:12 outside .git).
- Part 1 arm (e) spot check reproduces exactly (+0.0205 [0.0196, 0.0213]); the arm (e) labels come from b8_s0, not b9_s0.
- Open items: the Important robustness issue (content provenance of reused predictions; no impact found), the R7/NEGATIVE_RESULTS wording
  on W5/W20 (seed 0 only), and the Minor test gaps.
