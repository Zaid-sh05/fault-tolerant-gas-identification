# FREEZE MANIFEST v2 (single Test run of the few-shot recalibration; POST-HOC design)

Code commit at freeze: `55a1cebbbcbf69e7a92a0b971172525ed60b1194` (tag `frozen-before-test-v2` is placed on the commit that adds this file).
Design and rules: `results/decisions_log.md` section N (N0-N12). Nothing below may change after the tag; a bug found after the run is
fixed, logged, the run repeated and both results shown (N10).

## Frozen choices
- base model M0 recipe of stage 2 (StandardScaler -> SVM C=10, gamma=0.01; median detector, 95th percentile; A twin allowed; B cap 4)
- Train = batches 1-7 (invalid-value rule fitted on 1-7); evaluation batches 8, 9, 10, each with its own calibration rows
- n = 10 calibration rows per gas (min(10, count // 2)), calibration seeds 0-4, rows removed from scoring; (a) vs (b) on the same rows
- scenarios: clean + k1, k2, every v1 fault type and severity, fault seeds 0-4 (1081 per batch); methods SVM, A, B; no routing, no arbiter
- success (N8): (b) > (a) clean (pooled, interval above 0) and calibrated A >= SVM under faults (pooled)
- pre-run checks (N12): smoke identical to stage 2 (1.1e-16); estimate 1.9 h

## SHA-256 of code and configuration

| file | sha256 |
|---|---|
| `configs/final_test_v2.yaml` | `65fcb5a0ed68f40b1f440d7d75931e8c03236f749102572355d3b4336697fdf0` |
| `configs/preprocessing.yaml` | `cdef8f01862c048b404de502caf3592fc4124b7ce2947f5ce163d4094fbb375a` |
| `results/overnight/final_pipeline.json` | `efce735a48a95dea0113f3946ac58e6d795f91b7d0ca5b10d1bfc2043aedef6a` |
| `scripts/ft_v2_recal.py` | `86359a69639b5b1d1a80d9ddc68acde55948847ad803e110a4d5597c7753d4bb` |
| `scripts/ft_v2_tables.py` | `148212ac420ae5b2559344b937a954af08c7e1f9cba604b2906ba330ca15db9f` |
| `scripts/ft_v2_checks.py` | `c2aaad01ceab09a2d5618f777627eb977249ed7cabd594be3f05f7968b20ac07` |
| `scripts/v2_recal.py` | `8937ed15e22c08054bb8535dddca50160d1763f4e4411398f25d7457e5888381` |
| `scripts/v2_arbiter.py` | `27322505131218482be093b09b58f403e69ca25948e7cfcd4641726495141c2e` |
| `scripts/v2_dev.py` | `4236b31cfa2beebcd067a4ac09a42afc56b170e410724b2c3d287576c6219554` |
| `scripts/ov3_detector.py` | `530bddbb74dd6a05920cac03e2b1ff168b56fc359fd3196a41d5330f775efad0` |
| `scripts/run_guarded.py` | `0aad7de63df15f288c4f11523f197192a4f0be63e755c7e1139e08e9dd0bca5f` |
| `scripts/tree_guard.py` | `8f664444527137fcf3747883c872ad33a198c44192d3ee05aff50269f02e3f72` |
| `scripts/ft_ops.py` | `743226e7f202db93e6b6549e8455e1ff9f5acd10e79f7fbb1365fd62d805ea49` |
| `src/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `src/cleaning.py` | `c6e57d1f60791bbd34e91e580b1dddb9c813179b07825cb0f1fdb86168c7e154` |
| `src/data.py` | `3175cf75027e5ce614b13359fe03f20c8ff24af3c389b44210424d1bc6073718` |
| `src/detector.py` | `fb01c82b06dcd0a6583d857549caf6d16f1f94ccee7ea8aa436aaaa4632f9faa` |
| `src/drift.py` | `74f8747d1713534b634a7dab77d05a9bc3f6ea01d2683f8129382a6928c33f39` |
| `src/evaluate.py` | `53c64797afdc8e5c40257727de74532d2f67663eebf7b0c731b3c6f85d779bf4` |
| `src/fastsvm.py` | `28817ebf2e16f57fc53ffb72f6b4c475782c565d4ec8e395b66253f14cb017d4` |
| `src/faults.py` | `a6c4b4c36e2d056c075a457bebfc017769c2be2f3e11bcd7fb69b4f8018afee3` |
| `src/imputation.py` | `3446c4f9a9ec0d3b43ee5653c292455f58c24673016f0249d2a7e2fe53692a76` |
| `src/models.py` | `2dd8bbec59536701f31cb8fb09e109391c5a0896d629bbdd9ebaf98515ccff19` |
| `src/preprocessing.py` | `5bdb85589f4f4cccdc792eb65b6baad0dd3abaa44161bac31a85b906660d3cfa` |
| `src/scenarios.py` | `3b617a7ca11d14f590faa4708cebc5d36d112da0e91697b840d8f5403dc3c9fc` |
| `src/splits.py` | `3966914fb940f474a526f6257da539ed3c67f12408aebb699154aeff5188f0b4` |
| `src/strategies.py` | `24a156ecfc69b568596f4e684b1559be580d7231e62f0c8097c8527042037a36` |
| `src/study.py` | `b3bbee2a2d502ea08423f7f30a119feee253f28f9d3b66c4755675f3530bf21d` |

## Run command

```
python scripts/run_guarded.py --limit 85 --log results/final_test_v2/run.log -- <venv python> -u scripts/ft_v2_recal.py --config configs/final_test_v2.yaml --jobs 3
python scripts/ft_v2_tables.py --dir results/final_test_v2/test
```
