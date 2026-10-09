# Fault-tolerant gas identification under long-term sensor drift (ICSIC 2026 companion repository)

A metal-oxide (MOX) gas-sensor array is used to identify six gases over three years of real drift. We ask: **at inference time, when some sensors
become unreliable, what is the least harmful way to keep classifying?**

- **A — reconstruct** the faulty sensor block from the other sensors (Ridge), then use the normal classifier.
- **B — exclude** it, using a classifier trained without that sensor.
- **C — hybrid**, combining pair-of-sensor experts weighted by reliability.

The faulty sensors are found by an unsupervised reliability detector that never sees which sensor was corrupted.
The pre-registered study (v1) is complete. A post-hoc extension (v2) is reported separately and labelled as such everywhere.

## Data

UCI Machine Learning Repository, **Gas Sensor Array Drift Dataset** (dataset 224; Vergara et al., 2012).
- 13,910 samples in 10 batches (36 months).
- 16 sensors × 8 features = 128 features.
- 6 gases: ethanol, ethylene, ammonia, acetaldehyde, acetone, toluene.

1. Download `batch1.dat` … `batch10.dat` from https://archive.ics.uci.edu/dataset/224/gas+sensor+array+drift+dataset into `data/raw/`.
2. Check the files against `data/raw/SHA256SUMS.txt`, which lists the name, size and SHA-256 of each file. Use for example `sha256sum batch1.dat` (Linux/macOS) or `certutil -hashfile batch1.dat SHA256` (Windows).

Faults are **simulated** on whole 8-feature sensor blocks: dropout, bias, stuck and random, with 1, 2 or 4 faulty sensors (k=1, 2, 4). They are not recorded real faults.

## Protocols

| protocol | train | evaluate | role |
|---|---|---|---|
| **temporal** (main) | batches 1–6 | batch 7 (Validation) | every choice of v1 (`configs/preprocessing.yaml`) |
| **reference IID** | random 80% of batches 1–7 | stratified 20% hold-out | no-drift reference (`configs/reference_iid.yaml`) |
| **Drift-Dev** (v2) | batches 1–3 | batches 6 and 7, scored separately | v2 development under a large time gap (`configs/v2_drift_dev.yaml`) |
| **final test v1** | batches 1–6 | batches 8, 9, 10 (once) | `configs/final_test.yaml`, tag `frozen-before-test` |
| **final test v2** | batches 1–7 (+10 labeled rows per gas of the test batch) | batches 8, 9, 10 (once) | `configs/final_test_v2.yaml`, tag `frozen-before-test-v2` |

**Batches 8–10 are opened only by the two final-test configs.** These configs need `approved_by_user: true`, and the code checks this before reading any file.
Every decision, including the post-hoc ones and the incidents, is in [`results/decisions_log.md`](results/decisions_log.md). Each entry is written before the result it governs.

## Setup

Python 3.11 (tested on Windows 11):

```
python -m venv .venv
.venv\Scripts\activate          (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
pip install -e .
pytest                           (106 tests)
```

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
| 7. v2 edge cost and paper material | `python scripts/ft_edge_cost_v2.py`, `python scripts/v2_paper.py` | `results/edge_cost/edge_cost_v2.md`, `results/paper/` |
| 8. consistency of every paper number | `python scripts/check_paper_numbers.py` | prints any number that does not match its source |

Seeds are fixed everywhere, and SVM/LightGBM run deterministically with one BLAS thread. Re-running a final test is not part of the scientific protocol: each was run once. Their code and inputs are hashed in `FREEZE_MANIFEST.md` and `FREEZE_MANIFEST_v2.md`. The hashes refer to the tagged commits; later cosmetic edits, such as the README or path cleanup, do not change those commits.

## Main results (details in `results/paper/PAPER_NUMBERS.md`, every number with its source file)

- **v1 (pre-registered):**
  - Clean Macro-F1 falls from 0.859 on Validation to 0.535 on the Test batches. This is long-term drift, not faults.
  - Under simulated faults, A and B beat SVM in most cells, and also beat fault-augmented training. The exceptions are several faulty Bias/Stuck sensors at once.
  - Strategy C (reliability-weighted pair experts) is a negative result.
- **v2 (post-hoc, separate setting "with 10 labeled calibration samples per gas"):**
  - Recalibration raises the clean Test Macro-F1 by +0.136 (95% CI [0.132, 0.141]).
  - A and B keep about 97% of their clean score under faults; SVM keeps 81%.
  - Caveats: the calibration rows are interleaved in time with the scored rows, so the gain is optimistic, and the design is test-informed.
- Failed and unconfirmed ideas are summarised in [`results/NEGATIVE_RESULTS.md`](results/NEGATIVE_RESULTS.md).

## Repository layout

```
configs/            YAML configs of every protocol (base: preprocessing.yaml)
data/raw/           the 10 batch files of UCI #224 (not in git) + SHA256SUMS.txt
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
  edge_cost/        size, latency and memory of the pipelines
  paper/            figures, tables (latex/), PAPER_NUMBERS.md
  NEGATIVE_RESULTS.md
FREEZE_MANIFEST.md, FREEZE_MANIFEST_v2.md   hashes of the code and inputs of the two final tests
```

Bulky intermediate files are ignored by git: chunk files, fitted models, and reduced SVMs. The scripts regenerate them.
