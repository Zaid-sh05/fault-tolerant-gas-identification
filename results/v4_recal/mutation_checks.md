# Mutation checks of tests/test_v4_recal.py (2026-10-10, before any dev run)

Each leak was injected on purpose (Part 1: monkeypatching; Part 2: a mutated copy of scripts/v4_recal.py loaded as the module) and the
matching test was run against it. Every one failed, so each test can detect the leak it guards against.

| mutation | test | result |
|---|---|---|
| arm (e) uses the b9 model instead of b8 | test_arm_e_is_the_b8_model_and_contains_no_batch_10_row | FAILED as expected |
| Part 1 arms scored on all rows | test_part1_arms_are_scored_on_the_v3_rows | FAILED as expected |
| A reconstruction without the twin | test_v4_prediction_reproduces_the_v3_labels_of_arm_c | FAILED as expected |
| stale v3 chunk (same-period model) | test_stale_v3_chunks_are_rejected (built-in negative case) | raises as expected |
| M1 CAND-S uses the true labels of H1 | test_1 (no batch-t label in any fit) | FAILED as expected |
| M1b CAND-W memory includes the target batch | test_1 | FAILED as expected |
| M2 CAND-S pseudo-labels H1 and H2 | test_2 (halves; no H2 row in any fit) | FAILED as expected |
| M3 CAND-S scored on all kept rows | test_3 (identical rows across compared arms) | FAILED as expected |
| M4 a dev step reads batch 8 | test_4 (dev never reads 8-10) | FAILED as expected |
| M4b the Test stage ignores RUN_STARTED | test_4b (one Test run) | FAILED as expected |
| M5 CAND-C directions use target-batch rows | test_5 (directions from Train + past calibration only) | FAILED as expected |
