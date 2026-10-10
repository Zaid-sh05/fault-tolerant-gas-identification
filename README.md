# Detect, Compensate, Recalibrate for Robust IoT Gas Identification under Sensor Faults and Drift

Companion code for the paper submitted to **ICSIC 2026 (submitted)**.

**Authors:** Maria Nedal Natheir Shishani, Zaid Mohammad Ahmad Alshobaki and Hossam Sayel Oqlah Almahasneh (Amman Arab University).

A metal-oxide (MOX) gas-sensor array identifies six gases over three years of real drift. The question: **at inference time, when some
sensors become unreliable, what is the least harmful way to keep classifying?**

## Overview

- **Detect.** One shared, unsupervised, ridge-based reliability detector. For each sensor, a Ridge model predicts the sensor's 8-feature block
  from the other sensors, and a large residual flags the sensor. It never sees which sensor was corrupted.
- **Compensate (A) vs exclude (B).** A reconstructs each flagged block with the same Ridge models and keeps the normal classifier.
  B drops the flagged sensors and switches to an SVM trained without them.
- **Stage 1: frozen chronological test (pre-registered, v1).** Every choice was made on batches 1–7. Batches 8–10 were evaluated
  once, at the tag `frozen-before-test`.
- **Stage 2: few-shot recalibration (exploratory, post hoc, v2).** 10 labeled calibration samples per gas from each evaluated batch,
  evaluated once at the tag `frozen-before-test-v2`.

A third strategy, reliability-weighted pair-of-sensor experts (C), is a negative result; see
[`results/NEGATIVE_RESULTS.md`](results/NEGATIVE_RESULTS.md).

## Data

UCI Machine Learning Repository, **Gas Sensor Array Drift Dataset** (dataset 224; Vergara et al., 2012).
- 13,910 samples in 10 batches (36 months).
- 16 sensors × 8 features = 128 features.
- 6 gases: ethanol, ethylene, ammonia, acetaldehyde, acetone, toluene.

The 10 batch files are included in `data/raw/` (redistributed under the dataset's CC BY 4.0 license; source:
https://archive.ics.uci.edu/dataset/224/gas+sensor+array+drift+dataset). Their names, sizes and SHA-256 are in `data/raw/SHA256SUMS.txt`.
- Check the included copy: `python scripts/download_data.py --verify-only`
- Fresh independent copy from UCI (downloads, extracts, checks): `python scripts/download_data.py`

Faults are **simulated** on whole 8-feature sensor blocks: dropout, bias, stuck and random, with 1, 2 or 4 faulty sensors (k=1, 2, 4).
They are not recorded real faults.

## Main results

Test batches 8–10, pooled; Macro-F1 unless stated otherwise. Every number below is listed with its source file in the PAPER_NUMBERS file named.

- **Drift alone:** the clean SVM's Macro-F1 falls from 0.859 on Validation (batch 7) to 0.535 on the Test batches
  ([`PAPER_NUMBERS.md`](results/paper/PAPER_NUMBERS.md)).
- **Detection:** detector AUROC 0.967 (k=1, without dropout) ([`PAPER_NUMBERS.md`](results/paper/PAPER_NUMBERS.md), "AUROC v1 pooled k1,
  without Dropout").
- **Compensation:** with one faulty sensor at medium severity, A scores 0.536–0.543 across the four fault types, against a fault-free
  0.535 ([`PAPER_NUMBERS.md`](results/paper/PAPER_NUMBERS.md), "Macro-F1 A, ..., k=1, medium, Test pooled" and "Test clean Macro-F1, SVM,
  pooled").
- **Stage 2, under faults:** Macro-F1 rises from 0.544 (SVM without calibration) to 0.791 (A) and 0.809 (B).
  - A and B keep a ratio of 0.97 of their clean score; this is the mean of per-scenario ratios, against 0.81 for SVM.
  - Recalibration raises the clean SVM by +0.136 (95% t-interval over the 5 calibration seeds [0.117, 0.156]).
  - Source: [`PAPER_NUMBERS.md`](results/paper/PAPER_NUMBERS.md), the "v2 mean_under_faults", "v2 retained" and "v2c" rows.
- **Model size:** 782 KB for A vs 62,243 KB for B ([`PAPER_NUMBERS.md`](results/paper/PAPER_NUMBERS.md), "v2 edge size (KB)").

**Caveat:** Stage 2 is post hoc, and its design is test-informed. The calibration rows are interleaved in time with the scored rows, so its
gains are optimistic.

## Additional analyses (exploratory, post hoc)

These analyses came after the paper's two stages. Each was designed in [`results/decisions_log.md`](results/decisions_log.md) before its
result was computed.

- **Previous-period recalibration (v3, decisions_log Q).** The model is calibrated on samples of the previous batch only (8→9, 9→10).
  - A under faults improves by +0.0248 [0.0235, 0.0260] over the uncalibrated model.
  - Within that setting, A − SVM is +0.1074.
  - Source: [`PAPER_NUMBERS_v3.md`](results/paper/PAPER_NUMBERS_v3.md). Report:
    [`results/v3_prevbatch/PREV_BATCH_REPORT.md`](results/v3_prevbatch/PREV_BATCH_REPORT.md).
- **Carrying calibration forward (v4, decisions_log R).** Seven ways to strengthen previous-period recalibration were compared on
  development batches only.
  - None met the pre-registered threshold. The decision was NO-GO, so there was no Test run.
  - Report: [`results/v4_recal/V4_REPORT.md`](results/v4_recal/V4_REPORT.md).
- **Oracle selector between A and B (decisions_log P).** A per-scenario oracle choosing the better of A and B gains at most 0.01 on
  development data over the better fixed strategy.
  - Source: [`PAPER_NUMBERS_extra.md`](results/paper/PAPER_NUMBERS_extra.md). Analysis:
    [`results/oracle_selector/`](results/oracle_selector/).

## Protocols

| protocol | train | evaluate | role |
|---|---|---|---|
| **temporal** (main) | batches 1–6 | batch 7 (Validation) | every choice of v1 (`configs/preprocessing.yaml`) |
| **reference IID** | random 80% of batches 1–7 | stratified 20% hold-out | no-drift reference (`configs/reference_iid.yaml`) |
| **Drift-Dev** (v2) | batches 1–3 | batches 6 and 7, scored separately | v2 development under a large time gap (`configs/v2_drift_dev.yaml`) |
| **final test v1** (Stage 1) | batches 1–6 | batches 8, 9, 10 (once) | `configs/final_test.yaml`, tag `frozen-before-test` |
| **final test v2** (Stage 2) | batches 1–7 (+10 labeled rows per gas of the test batch) | batches 8, 9, 10 (once) | `configs/final_test_v2.yaml`, tag `frozen-before-test-v2` |
| **previous period** (v3) | batches 1–7 (+10 labeled rows per gas of the previous batch) | batches 9 and 10 | `configs/v3_prevbatch.yaml`; reuses the v2 models (decisions_log Q) |
| **calibration forward** (v4) | Drift-Dev, batches 1–3 (+ calibration rows of earlier batches: 5→6, 6→7) | batches 6 and 7; no Test run (NO-GO) | `configs/v4_recal.yaml`; Part 1 applied the saved v2 models to the Test batches, descriptively (decisions_log Q9, R) |

**Batches 8–10 are read only by configs with `approved_by_user: true`:** the two final tests and the post-hoc v3 and v4 configs
(decisions_log Q0, Q9). The code checks this flag before reading any file.
Every decision, including the post-hoc ones and the incidents, is in [`results/decisions_log.md`](results/decisions_log.md). Each entry is written before the result it governs.

## Setup

Python 3.11 (tested on Windows 11):

```
python -m venv .venv
.venv\Scripts\activate          (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
pip install -e .
pytest
```

`pytest` on a clean clone: 112 passed, 18 skipped. The v3 and v4 tests skip without the local, gitignored models and predictions.
With all of them present, the 130 tests pass. A clone on a machine that holds the models at `main_checkout` (`configs/v4_recal.yaml`)
gives 123 passed, 7 skipped.

All scripts are run from the repository root. Long runs use `scripts/run_guarded.py`, which stops the whole process tree if the memory
load reaches 85%. Their intermediate results are checkpointed in chunks, so a run can resume.

## Reproduction, step by step

| step | command | output |
|---|---|---|
| 1. audit and preprocessing study (gates P1–P6) | `python scripts/run_preprocessing.py` | `results/preprocessing/` |
| 2. v1 study on Validation: faults and gate G1, detector and G2, strategies and G3, clean reference | `python scripts/ov2_faults_g1.py --config configs/preprocessing.yaml --name temporal`<br>`python scripts/ov3_detector.py --config configs/preprocessing.yaml --name temporal`<br>`python scripts/ov4_strategies.py --config configs/preprocessing.yaml --name temporal`<br>`python scripts/ov4_analysis.py --config configs/preprocessing.yaml --name temporal`<br>`python scripts/ov4_clean_reference.py --config configs/preprocessing.yaml --name temporal`<br>(the same with `--config configs/reference_iid.yaml --name reference_iid --reduced` for the reference) | `results/overnight/` |
| 3. v1 final test (once, at tag `frozen-before-test`) | `git checkout frozen-before-test` then `bash scripts/run_final_test.sh configs/final_test.yaml` | `results/final_test/` |
| 4. v1 reports, edge cost, paper material | `python scripts/ft_report.py`, `python scripts/ft_edge_cost.py`, `python scripts/ft_paper.py`, `python scripts/detector_breakdown.py` | `results/final_test/TEST_REPORT.md`, `results/edge_cost/`, `results/paper/` |
| 5. v2 development (post-hoc, batches 1–7 only) | `python scripts/v2_dev.py`, `python scripts/v2_toluene_sensitivity.py`, `python scripts/v2_coral_check.py`, `python scripts/v2_arbiter.py`, `python scripts/v2_recal.py --stage clean`, `python scripts/v2_recal.py --stage faults`, `python scripts/v2_light.py`, `python scripts/v2_improve.py --light` | `results/v2/` |
| 6. v2 final test (once, at tag `frozen-before-test-v2`) | `python scripts/ft_v2_checks.py smoke` (needs `python scripts/ft_v2_recal.py --config configs/v2_drift_dev.yaml --smoke` first), `python scripts/ft_v2_checks.py estimate`, then at the tag `python scripts/ft_v2_recal.py --config configs/final_test_v2.yaml` and `python scripts/ft_v2_tables.py` | `results/final_test_v2/` |
| 7. v2 edge cost and paper material (post-audit, decisions_log O) | `python scripts/ft_edge_cost_v2.py`, `python scripts/paper_corrections.py ci`, `python scripts/paper_corrections.py auroc`, `python scripts/paper_material.py` (do not re-run the superseded `scripts/v2_paper.py`, see `results/paper/SUPERSEDED.md`) | `results/edge_cost/edge_cost_v2.md`, `results/paper/` |
| 8. consistency of every paper number | `python scripts/check_paper_numbers.py` | prints any number that does not match its source |
| 9. v3 previous-period recalibration (needs the v2 models of step 6) | `python scripts/v3_prevbatch.py` with the stages `smoke`, `gate`, `run`, `score`, `tables`, `paper` | `results/v3_prevbatch/` |
| 10. v4 calibration forward (set `main_checkout` in `configs/v4_recal.yaml` to the clone holding the v2 models and v3 predictions) | `python scripts/v4_recal.py` with the stages `part1`, `devgate`, `tournament`, `paper` (`test` runs only after a committed GO decision) | `results/v4_recal/` |
| 11. oracle selector (descriptive, from saved results) | `python results/oracle_selector/oracle_selector.py` | `results/oracle_selector/` |

Seeds are fixed everywhere, and SVM/LightGBM run deterministically with one BLAS thread. Re-running a final test is not part of the scientific protocol: each was run once. Their code and inputs are hashed in `FREEZE_MANIFEST.md` and `FREEZE_MANIFEST_v2.md`. The hashes refer to the tagged commits; later cosmetic edits, such as the README or path cleanup, do not change those commits.

## Repository layout

```
configs/            YAML configs of every protocol (base: preprocessing.yaml)
data/raw/           the 10 batch files of UCI #224 (CC BY 4.0) + SHA256SUMS.txt
src/                data loading, splits, cleaning, preprocessing, faults/scenarios, detector, strategies, drift (v2), fast SVM
scripts/            one script per study step (see the table above); run_guarded.py / tree_guard.py = memory guard
tests/              unit tests (pytest)
results/
  decisions_log.md  every decision, PRE / POST-HOC, incidents
  preprocessing/    preprocessing study (P1-P6)
  overnight/        v1 study on Validation (temporal, reference_iid)
  final_test/       v1 final test (TEST_REPORT.md)
  v2/               v2 development (candidates, arbiter, recalibration, night study)
  final_test_v2/    v2 final test (TEST_V2_REPORT.md)
  v3_prevbatch/     v3 previous-period recalibration (PREV_BATCH_REPORT.md)
  v4_recal/         v4 calibration forward: shelf life, dev tournament, NO-GO (V4_REPORT.md)
  oracle_selector/  oracle selector between A and B (descriptive)
  audit/            independent audits, sanity checks, commit hash map
  edge_cost/        size, latency and memory of the pipelines
  paper/            figures, tables (latex/), PAPER_NUMBERS*.md
  NEGATIVE_RESULTS.md
FREEZE_MANIFEST.md, FREEZE_MANIFEST_v2.md   hashes of the code and inputs of the two final tests
CITATION.cff        citation metadata
```

Bulky intermediate files are ignored by git: chunk files, fitted models, and reduced SVMs (about 23 GB). The scripts regenerate them.

## How to cite

Please cite the paper and, if you use the code, this repository (GitHub's "Cite this repository" button reads `CITATION.cff`).

> M. N. N. Shishani, Z. M. A. Alshobaki and H. S. O. Almahasneh, "Detect, Compensate, Recalibrate for Robust IoT Gas Identification under
> Sensor Faults and Drift," ICSIC 2026 (submitted).

> M. N. N. Shishani, Z. M. A. Alshobaki and H. S. O. Almahasneh, *fault-tolerant-gas-identification* (companion code), 2026.
> https://github.com/Zaid-sh05/fault-tolerant-gas-identification

## License

Code and results: MIT (see `LICENSE`), © 2026 Zaid M. Alshobaki. Data: UCI Gas Sensor Array Drift Dataset, CC BY 4.0
(A. Vergara, S. Vembu, T. Ayhan, M. Ryan, M. Homer, R. Huerta, "Chemical gas sensor drift compensation using classifier ensembles",
Sensors and Actuators B: Chemical 166-167 (2012) 320-329, doi:10.1016/j.snb.2012.01.074).
