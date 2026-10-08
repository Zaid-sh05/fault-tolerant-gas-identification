# FREEZE MANIFEST - everything fixed before batches 8-10 are opened
Date: 2026-10-08   |   code commit: `4e414a9239bbee38be50be441ab6f289813ca6a4`   |   branch: `main`   |   tag: `frozen-before-test` (on the commit that adds this file)
Environment: Python 3.11.9, scikit-learn 1.8.0, lightgbm 4.7.0, numpy 2.4.6, pandas 3.0.6; requirements.txt hash below.

## 1. Rules of the single run
- Batches 8-10 are opened once, by `bash scripts/run_final_test.sh configs/final_test.yaml` (marker file `RUN_STARTED` refuses a second start). Approval: the user, 2026-10-08.
- Same code and configs, verbatim. No change after the run, whatever the outcome. A programming error stops the run and is reported; it is not fixed and re-run without telling the user.
- Nothing is refitted: the models, detectors, thresholds and reduced SVMs below were fitted on Train (batches 1-6) at Validation time. Reduced SVMs for sensor sets that Validation never produced are trained on demand from the same Train rows with the frozen parameters.
- Test results are reported per batch (8, 9, 10) and pooled, with the same tables as Validation.

## 2. Frozen choices (read back from the files, not retyped)
- Pipeline spec: `{"clip": "none", "slog": false, "scaler": "standard", "groups": [], "select": "none"}` (raw 128 features, StandardScaler fitted on Train, NaN -> 0 for the SVM).
- SVM: RBF, C=10, gamma=0.01, seed 0.  LightGBM: `{"num_leaves": 31, "n_estimators": 400, "learning_rate": 0.05, "class_weight": null}`.
- Cleaning: invalid-value rule |x - median| / MAD > 1000 fitted on Train; flagged Train rows dropped; evaluation rows never dropped (flagged ones are counted).
- Fault augmentation: seeds [0, 1, 2, 3, 4], copies 1; 5 seeds per augmented baseline.
- Faults: Dropout, Bias, Stuck, Random on whole 8-feature blocks; levels {"dropout": [0.5, 1.0], "bias": [0.5, 1.0, 3.0], "stuck": [0.5, 1.0], "random": [0.5, 1.0]}; medium severity {"dropout": 0.5, "bias": 1.0, "stuck": 0.5, "random": 0.5}; Bias unit sigma_robust = IQR/1.349 of cleaned Train; shared affected rows; 5 seeds.
- Sensor sets: k=1 all 16 sensors; k=2 replicate pairs; k=4 groups (HYPOTHESIS, not documented by the dataset): `[[0, 1, 8, 9], [2, 3, 10, 11], [4, 5, 12, 13], [6, 7, 14, 15]]` (0-based).
- Scenario list: 1260 scenarios, sha256 of its repr `e5bab97b3a4d76cb534520777717f4291460afc43ffccbe09c60e35fe19387ab`.
- Detector: Ridge in standardised signed-log space, normalisation **median** (Validation median isolation AUROC 0.9770; the other normalisation scored 0.9570); alarm threshold = 95th percentile of the Train out-of-fold normalised score; leave-pair-out detector = sensitivity analysis only.
- Strategies: A reconstruct flagged blocks (Ridge from unflagged sensors) then the clean SVM; B SVM trained without the flagged sensors; C eight replicate-pair experts, reliability weight 1/max(1, ratio)^2 (min over the expert's two sensors); at most 4 sensors acted upon per row; Oracle variants use the true faulty sensors (analysis bound only). Main result: A, with B and the Oracle as references; C is reported as a negative result and is not redesigned.
- Gates (rules unchanged, `results/decisions_log.md` B4, B6-B8, B11): G1 >= 2 of 4 fault types lose >= 0.03 Macro-F1 at k=1, medium severity; G2 median isolation AUROC over the four fault types at k=1, medium >= 0.80; G3 at least one comparison of a real-detector strategy beats the best augmented baseline with a paired-bootstrap 95% interval excluding 0 (lenient; the full tables are shown). Intervals resample rows only, so they are optimistic.

### Detector parameters (primary detector)
| sensor | ridge alpha | alarm threshold tau |
|---|---|---|
| S01 | 100 | 2.1438 |
| S02 | 100 | 3.2858 |
| S03 | 100 | 2.0416 |
| S04 | 100 | 2.0253 |
| S05 | 100 | 4.9494 |
| S06 | 10 | 3.3288 |
| S07 | 10 | 1.0540 |
| S08 | 10 | 1.0683 |
| S09 | 10 | 1.8036 |
| S10 | 10 | 2.6421 |
| S11 | 10 | 2.2423 |
| S12 | 10 | 1.9964 |
| S13 | 10 | 2.4329 |
| S14 | 10 | 2.5003 |
| S15 | 1 | 1.0489 |
| S16 | 1 | 0.9901 |

## 3. Files
Fitted objects: 1222 files, hashes in `results/FREEZE_HASHES.json` (verified by `scripts/ft_prepare.py` before the run).

### Configs
| file | sha256 |
|---|---|
| configs/final_test.yaml | 7a1aa8845b9a88918cb8f7486e2d4bbe891021a0cc3823c4376c77d875bcebdc |
| configs/final_test_dryrun.yaml | b7d48062014eb3ddca3267592a03cd034a54d1149f55584aaade7c9af16a16f0 |
| configs/main.yaml | 9314953510193fe8e46892b1817bd768544d49676a13b05da4b480ec24906efd |
| configs/main_cleaned.yaml | fe394e263294683197cd1e799de31cc9d2c1b651c5eb6d8c32f67ece44c7cdce |
| configs/main_cleaned_drop223.yaml | 84b0778d56c2753588fb14f5b82e9aefa56737e107febdda6a59abf74fa14e00 |
| configs/preprocessing.yaml | cdef8f01862c048b404de502caf3592fc4124b7ce2947f5ce163d4094fbb375a |
| configs/reference_iid.yaml | 51ab293a8531edada3dc33c05278a9f2ba75d280ff3cbc512769155b541da7d3 |
| configs/sens_iid_keep223.yaml | 6bc254e8460c3dcc382ed7eed94d29bfefeb9065c65d6e60139ba9524d9b1890 |
| configs/sens_temporal_drop223.yaml | 28578deb87c2f3962c6b6e42be56a0d5310829056dd9816b950a757d1cb16966 |

### Other frozen inputs
| file | sha256 |
|---|---|
| requirements.txt | 2fe4b91fb4fab74501026652f749716e0ea4f25596ebe401b39da1e77727e0d7 |
| pyproject.toml | 358a695b2d0d01ded0f87bd15041a2ddf432c20b8d09b07c5d662cdea87452c9 |
| results/overnight/final_pipeline.json | efce735a48a95dea0113f3946ac58e6d795f91b7d0ca5b10d1bfc2043aedef6a |
| results/overnight/temporal/g2_verdict.json | 8bbce1b64040fa60d01e4b7db96ec5809b54433b84a65b0e3b305cddb4561f33 |
| results/decisions_log.md | 7a26d6d31df7743ff3924b2be66dc6da5493c275dac565300d4171951a62bbc6 |

### Source and scripts
| file | sha256 |
|---|---|
| scripts/01_audit.py | 8613ab6b143bea9f6f1c3255a386e3efb9761335a582d03122463e0234eb32bd |
| scripts/02_baselines.py | 1c70c7134845cc567ce87cf0b9b03e384be3793f9c0d30b4eac43e97b5b0ec32 |
| scripts/diag_baseline_shift.py | e2df79a71fac65e151f97244b9b1fe68aa8cc0fd79406cafbf422786c79aabec |
| scripts/ft_analysis.py | 9d6fa61e4a0753a07e67299383aefc5d42cea1f4eed89c146c0d6b4ecbf9a653 |
| scripts/ft_detector.py | 5a35a2fee3e3b394ad7234566f7427eabc75fbc49e0858a4800102eb73e455e2 |
| scripts/ft_freeze.py | 624976e24dd062ec9d690c0cbba20a2cbe0a70eac937dd6181ab002730eec79e |
| scripts/ft_prepare.py | 32a2c4a61feaa151d25c9e63c2fc0f22e7aff029cecf3b042e9de515f9790489 |
| scripts/ft_s01s02.py | b97bcf349716709155c9f1d2d0f333f564776a135594d23ba34edbb6613a3ad4 |
| scripts/ov2_faults_g1.py | 375bf5c1fcad06000253acd8b62e7c21974c8b86918d05f3131e91f30e4c937e |
| scripts/ov3_detector.py | 530bddbb74dd6a05920cac03e2b1ff168b56fc359fd3196a41d5330f775efad0 |
| scripts/ov4_analysis.py | 5f7c46393ef8b5d3ec4d9b592f872c1b0ec216db5d57e8f99e893c1f40c96094 |
| scripts/ov4_clean_reference.py | 115a393c406d36f1dff2cb551059ab1b5e5a42106b41259c82a34aa68199bfeb |
| scripts/ov4_strategies.py | 947cc32500f320c4720fe07d5498a470d95b3ddddecd94bd691a77c68d7ca97d |
| scripts/ov_morning_report.py | ab893af67b0e72ee8ddf6038506466dd463f7eb8a52759872c6516aedd346165 |
| scripts/pp0_invalid_records.py | e8118befdab4802feb8d8eb9c13ee20fbfa34308bc0ef6e23ec1d70c08f437fc |
| scripts/pp1_compare_protocols.py | 9944825d067d7eda5dabc7fb392195823f6add7cf234023d400798c4adb6d972 |
| scripts/pp1_pair_drift.py | 7d1d8da11f611467f983497e098f988ce1e97f8ad052c66c6ddabc231e18c708 |
| scripts/pp1_quality_imputation.py | 1bbcbb4649dcd029a7538ca01f734773d5020ddd7ef7776b3606fe9e3d15e97d |
| scripts/pp1_sensitivity_223.py | 424b2d92da1fbbb12ad3bb39dfbf93aa54927808a040fbdbef8267dd9cca0e19 |
| scripts/pp2_outliers.py | 075e06593d48e46603f4864cb11e27da2c9984acc70a2b9aa227626fa3a1ad0c |
| scripts/pp3_scaling.py | d99865de5f3231ef369e3e7aca1a9d98d1c9cbf9b1fbf913d0c218a7457bb6ee |
| scripts/pp3b_minmax_stress.py | ca41edcd4456e042e95827feca45809220e1295b730410424918a0163c3064b3 |
| scripts/pp45_decision_rule.py | 8d9562d4f73b6b2da2f8ad04c7122b74fd545d3e731bb341ab24b1d1091ca11c |
| scripts/pp4_features.py | e23c8069d39a4f98528f828203631c3daf0422b6f81ec94afc39bd1ba45f6fed |
| scripts/pp5_drift.py | 98a593629533b3a17654d42cf41660e0b0a9100a3a743356c58b44cb62017ad2 |
| scripts/pp6_baselines_aug.py | ca5b4abd3e7c0e67616c8faf98da11a4fbd04c9cc66bce01941d6a7e4391ce17 |
| scripts/pp_report.py | fed67ceafdf2b585571c043bb9d6b529d5d67ca2d93eb6a9f87352e96daaaf70 |
| scripts/run_final_test.sh | c3bd7c694f07a6cce0c07ea45994480902340db6fd5f75407bebe702a74b462f |
| scripts/run_preprocessing.py | 35e4d267ee8ea25b4a81f60e7d906a8575c6a80855e985358e2bbd1a498effa1 |
| scripts/verify_reproducibility.py | 26ade5990d4534a6ce267b0463ddf8c608d612f614da13cde898ed6b47701afb |
| src/__init__.py | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| src/cleaning.py | c6e57d1f60791bbd34e91e580b1dddb9c813179b07825cb0f1fdb86168c7e154 |
| src/data.py | 3175cf75027e5ce614b13359fe03f20c8ff24af3c389b44210424d1bc6073718 |
| src/detector.py | fb01c82b06dcd0a6583d857549caf6d16f1f94ccee7ea8aa436aaaa4632f9faa |
| src/evaluate.py | 53c64797afdc8e5c40257727de74532d2f67663eebf7b0c731b3c6f85d779bf4 |
| src/fastsvm.py | e1cc5d59f7de6abace188718f4d04691636681ce8a52aca9e7e575833cfe9e7b |
| src/faults.py | a6c4b4c36e2d056c075a457bebfc017769c2be2f3e11bcd7fb69b4f8018afee3 |
| src/imputation.py | 3446c4f9a9ec0d3b43ee5653c292455f58c24673016f0249d2a7e2fe53692a76 |
| src/models.py | 2dd8bbec59536701f31cb8fb09e109391c5a0896d629bbdd9ebaf98515ccff19 |
| src/preprocessing.py | 5bdb85589f4f4cccdc792eb65b6baad0dd3abaa44161bac31a85b906660d3cfa |
| src/scenarios.py | 3b617a7ca11d14f590faa4708cebc5d36d112da0e91697b840d8f5403dc3c9fc |
| src/splits.py | 3966914fb940f474a526f6257da539ed3c67f12408aebb699154aeff5188f0b4 |
| src/strategies.py | 24a156ecfc69b568596f4e684b1559be580d7231e62f0c8097c8527042037a36 |
| src/study.py | b3bbee2a2d502ea08423f7f30a119feee253f28f9d3b66c4755675f3530bf21d |

## 4. Post-freeze operational amendment (2026-10-08, after the run was interrupted by memory exhaustion)
The tag `frozen-before-test` is unchanged. The ONLY differences from the tag in anything the run executes are the number of worker processes and operational wrappers; no computation, parameter, chunking or file format changed. Details:
- `scripts/run_final_test.sh`: reads `JOBS` (default 6, as before) and passes `--jobs "$JOBS"` to the steps that run workers.
- `scripts/ov4_analysis.py`: gets a `--jobs` option (default 6) instead of the constant 6 in `Parallel(...)`.
- New files, no effect on results: `scripts/run_guarded.py` (kills the run's process tree if the machine memory load reaches 85%, moves truncated chunk files aside, exits with code 3) and `scripts/ft_ops.py` (chunk verification; determinism check of one finished chunk).
- Analysis, paper and report scripts added after the tag (`ft_paper.py`, `ft_report.py`, `ft_edge_cost.py`) only read result files.
- Verified: `git diff frozen-before-test` over `src/`, `configs/` and all other run scripts is empty.

Current sha256 of the two modified files and the two new ones (the tables above keep the frozen hashes):

| file | sha256 |
|---|---|
| scripts/ov4_analysis.py | 9bd7d09527ab1a7cea92cd1da14c402817b46c6b86b2c5775b29cbfd5d5323a2 |
| scripts/run_final_test.sh | d4c6233ca9d1033a1ffd17f22f6684ec5cf16addaca732d2cacefc44c58c52cb |
| scripts/run_guarded.py | a5c39754ca6527ced2339e20ff83b544fc20e2a2976b63b23cf8621ead15160b |
| scripts/ft_ops.py | 743226e7f202db93e6b6549e8455e1ff9f5acd10e79f7fbb1365fd62d805ea49 |

`scripts/ft_ops.py` hash above is the version with the added `recheck` command (structure check and recomputation of a finished chunk in a separate folder); it does not write into the run folder.
