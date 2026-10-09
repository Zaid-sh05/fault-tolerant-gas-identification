# Commit hash map (history rewrite, 2026-10-09)

On 2026-10-09 the commit messages were rewritten to drop the AI co-author trailer lines (user decision). Only the messages changed: every
commit keeps its tree (file contents), author, author date and commit date, so all file hashes in FREEZE_MANIFEST.md and
FREEZE_MANIFEST_v2.md still hold. Only the commit hashes changed. Files written before the rewrite (FREEZE_MANIFEST*.md, results/audit/AUDIT_REPORT.md,
results/decisions_log.md, results/MORNING_REPORT_v1_overnight.md) cite the OLD hashes; use this table to translate them.

Tags: `frozen-before-test` 07e9eac -> e3fac02, `frozen-before-test-v2` d8fd992 -> ac6b9a9 (same trees as before).

| old | new | subject |
|---|---|---|
| cc48b1c | f21ac4b | Add project scaffold: pinned Python 3.11 env and smoke test |
| f1e507a | 200f515 | Reproduce clean baselines on real data with a leak-proof loader |
| 817ab0d | feecb80 | Add data audit restricted to Train/Val batches |
| 6ec57e9 | 1e57d45 | Preprocessing phase 1: integrity re-check and sensor-block reconstruction |
| 8a8288a | 3727676 | Add evaluation protocols, cleaning rule and preprocessing pipeline code |
| d7a91c9 | 1cefdd8 | Results: cleaned baselines, reconstruction in both protocols, phases 2-3 |
| 805c0ef | b9e775f | Pre-register robust fault scale, MinMax stress check and shortened phases 4-5 |
| 327634a | e37dc43 | Register interpretations and decision rules for the overnight run |
| a4b7cd1 | 64b82cd | Part 1: stress check, phases 4-5, decision rule, new baselines, runner and report |
| 3877498 | 4a62bc9 | Parts 2-3: fault scenarios, G1 and reliability detector with G2 |
| 40c4320 | eea1168 | Part 4 (temporal protocol): strategies A/B/C, bootstrap comparison and G3 |
| a243d97 | 947930c | Reference protocol (no drift, reduced scenarios): G1, G2, strategies and G3 |
| d784515 | ab6debe | Overnight run: reproduction check (P6), reports and decisions log |
| 4e414a9 | a106348 | Final-test code path, per-batch analysis scripts, dry run on Validation, decisions D1-D8 |
| 07e9eac | e3fac02 | Freeze manifest before the final test |
| a8732b5 | f0b45da | Reporting scripts (paper material, test report, edge cost); Figure 1 on a scale-free skill score (post-hoc E2) |
| 92c39d9 | a059f29 | Operational only: --jobs option, memory guard launcher and chunk checks for resuming the final test (no change to computations) |
| 3cebb50 | 76fd561 | Integrity check of the inherited chunks (recheck command, decisions F3); operational only |
| 79ab460 | 395661c | Fix the memory reading in the edge-cost measurement |
| d931b20 | 38d1a8c | Add final-test results, edge cost and paper materials |
| 3e2365f | 7558d7e | Register v2 (post-hoc): Drift-Dev protocol, candidates M0-M5, arbiter H1-H3, selection rules |
| 3b00aa9 | 3cf9364 | Fix fast_svm_predict for two-class models; prove v1 was unaffected |
| 72d6c07 | dbfe913 | Add v2 candidates M0-M4 and the Drift-Dev evaluation (post-hoc, decisions_log G4-G6) |
| 33664a0 | 42e8d51 | v2 candidate table (M0 wins: no candidate improved the base) and the arbiter script |
| 07288ba | 3f162aa | Make arbiter checkpoints atomic and tie the cache to the base model |
| 33b202e | ba175e6 | Add Drift-Dev toluene sensitivity of the v2 candidates (post-hoc, decisions_log I8) |
| 0c071aa | f0602d9 | Register few-shot recalibration (post-hoc, decisions_log J0-J7) before coding it |
| 689d2a8 | e54d9b1 | Add few-shot recalibration (decisions_log J) and the retention column |
| eb5bfaa | 24cabca | Register the overnight order and the CORAL diagnostic (decisions_log K1-K2) |
| 4aab5f6 | ab2603f | CORAL check result and the overnight chain |
| e0d5ca6 | fa031e1 | v2 arbiter results (no variant passes G8) and recalibration stage 1 (n* = 10) |
| 8374d22 | 0b6db46 | Add the v1 Test detector breakdown (read from existing result files only) |
| 8643dfc | c4946ca | Register the night improvement study (post-hoc, decisions_log L0-L6) before any result |
| b15e810 | b7d5ef5 | Amend the night study: light experiments on saved v1 outputs first (decisions_log L7) |
| b8353a5 | 5e67c6e | Add the light night study (LD, LR, LA; decisions_log L7) |
| 60cbadc | 819cf9b | Light night study results (LR passes the Validation stage with a small gain; LD; LA) and the heavy script |
| 51d1075 | acbb6fb | Run the A variants as a light job (decisions_log L8); light mode in v2_improve.py |
| 314eb4b | c2cde42 | Add the routing-only confirmation mode (LR on Drift-Dev, heavy, after stage 2) |
| 7774b92 | 41b5d39 | A variants V0-V5 on Drift-Dev and Validation 7: none beats V0 (decisions_log L4, L8) |
| 27ea311 | f017ae5 | Add a partial stage-2 summary (finished configurations only, approximate reference marked) |
| 4629916 | 676bd93 | Fix the memory guard: kill the whole process tree pid by pid and verify (decisions_log M1) |
| 649a77e | f87b089 | Keep the v1 overnight morning report under a new name (the new morning report takes its path) |
| 6ac8ecf | 5a80d50 | Morning report (v2 night: arbiter, recalibration partial, night study, incidents) |
| a9c7083 | 3f66cef | Morning report: add the arbiter table |
| 99874e3 | 2708475 | Morning report: stage 2 snapshot at 08:57 |
| 37a62a8 | 39f1f23 | Register the single Test v2 run of the recalibration (PRE-TEST v2, post-hoc design; decisions_log N0-N10) |
| aa3c9a8 | 5f9aefa | Test v2 recalibration run: script, tables, pre-run checks and config (not run yet) |
| 3d8cda4 | ecb2e48 | Recalibration stage 2 complete; morning report updated; ignore bulky v2 intermediates |
| 3d77f2e | eed4a5f | Guard: write the STOPPED_MEMORY marker next to the run log (it went into results/final_test) |
| 3e61fcc | 6f5a80a | Guard: write STOPPED_MEMORY next to the run log (the previous commit only moved the old marker) |
| 7561079 | 634c8b5 | Test v2 script: survive the concurrent replace of a reduced model on Windows (decisions_log N11) |
| 55a1ceb | 20e2156 | Pre-run checks passed: smoke identical to stage 2, estimate 1.9 h, seeds stay 0-4 (decisions_log N12) |
| d8fd992 | ac6b9a9 | Freeze manifest v2: hashes of code and config for the single Test v2 run |
| 947f506 | 8e51136 | Test v2 (single run, few-shot recalibration): results, report and PAPER_NUMBERS v2 section |
| 557fe0c | 75f0bcd | Edge cost of v2: calibrated SVM, A, B (136 models for k=1/k=2 coverage) and the calibration step |
| b41297f | 6b65ccc | Paper material v2: 2x2 recalibration figure, per-batch gain figure, LaTeX tables for v1 and v2 |
| e96eef9 | 1aaec3e | Repository cleanup for publication: README, NEGATIVE_RESULTS, relative paths, track SHA256SUMS |
| f0e2bb2 | d46551c | Add the PAPER_NUMBERS consistency check (676 rows and 249 table numbers, no mismatch) |
| 2669e5d | 7e94514 | Independent audit: no leakage found; v2 confidence intervals too narrow (report only, nothing fixed) |
| fed8c02 | 25abc07 | check_paper_numbers: compare every table cell with its own named number (TDD) |
| c781b05 | c93f8a1 | Corrected v2 intervals: shared-index scenario bootstrap (faults) and seed t-interval (clean) |
| bc47562 | 08d9c4f | Detector AUROC with and without Dropout (v1 Validation/Test, v2 per batch and model; k=1, k=2) |
| 6813b22 | e1fa68c | Paper material with the corrected v2 intervals, cell maps for every table, IEEE column figures |
| 14c194c | a44836b | Log the post-audit correction (decisions_log O1-O3) and the final consistency check (0 problems) |
| c56158e | 830faeb | Add METHODS_FACTS.md and the sanity-check / per-sensor FAR numbers |
| 0ab0402 | 3d6c370 | Prepare the public release: MIT license, raw data, download script |
| 54fd077 | 61e5502 | Add the post-hoc oracle-selector bound between A and B (decisions_log P) |
