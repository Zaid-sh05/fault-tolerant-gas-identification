"""One command that reproduces every preprocessing result (gate P6).

Usage: python scripts/run_preprocessing.py [--resume]
Each step writes a marker in results/preprocessing/_done/; --resume skips steps that already finished (checkpointing).
Before a fresh run the existing results are COPIED (never deleted) to results/_backup_<timestamp>/, so that
scripts/verify_reproducibility.py can compare the new numbers with the previous ones.
Batches 8-10 are never read by any step.
"""
import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

PY = sys.executable
CFG = "configs/preprocessing.yaml"
STEPS = [
    ("tests", [PY, "-m", "pytest", "-q", "-W", "ignore::sklearn.exceptions.ConvergenceWarning",
               "--junitxml=results/preprocessing/junit.xml"]),
    ("baselines_old", [PY, "scripts/02_baselines.py", "--config", "configs/main.yaml"]),
    ("baselines_cleaned", [PY, "scripts/02_baselines.py", "--config", "configs/main_cleaned.yaml"]),
    ("baselines_drop223", [PY, "scripts/02_baselines.py", "--config", "configs/main_cleaned_drop223.yaml"]),
    ("diag", [PY, "scripts/diag_baseline_shift.py"]),
    ("invalid_records", [PY, "scripts/pp0_invalid_records.py"]),
    ("pp1_temporal", [PY, "scripts/pp1_quality_imputation.py", "--config", CFG]),
    ("pp1_iid", [PY, "scripts/pp1_quality_imputation.py", "--config", "configs/reference_iid.yaml"]),
    ("pp1_temporal_drop223", [PY, "scripts/pp1_quality_imputation.py", "--config", "configs/sens_temporal_drop223.yaml"]),
    ("pp1_iid_keep223", [PY, "scripts/pp1_quality_imputation.py", "--config", "configs/sens_iid_keep223.yaml"]),
    ("pp1_compare", [PY, "scripts/pp1_compare_protocols.py"]),
    ("pp1_sensitivity", [PY, "scripts/pp1_sensitivity_223.py"]),
    ("pp1_pair_drift", [PY, "scripts/pp1_pair_drift.py", "--config", CFG]),
    ("pp2", [PY, "scripts/pp2_outliers.py", "--config", CFG]),
    ("pp3", [PY, "scripts/pp3_scaling.py", "--config", CFG]),
    ("pp3b", [PY, "scripts/pp3b_minmax_stress.py", "--config", CFG]),
    ("pp4", [PY, "scripts/pp4_features.py", "--config", CFG]),
    ("pp5", [PY, "scripts/pp5_drift.py", "--config", CFG]),
    ("pp45", [PY, "scripts/pp45_decision_rule.py", "--config", CFG]),
    ("pp6", [PY, "scripts/pp6_baselines_aug.py", "--config", CFG]),
    ("report", [PY, "scripts/pp_report.py", "--config", CFG]),
]
SNAPSHOT = ["results/preprocessing", "results/main", "results/main_cleaned", "results/main_cleaned_drop223"]


def main(resume):
    root = Path("results/preprocessing")
    done = root / "_done"
    if not resume:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        for d in SNAPSHOT:
            if Path(d).exists():
                shutil.copytree(d, f"results/_backup_{stamp}/{Path(d).name}")
        (Path("results") / "_backup_latest.txt").write_text(f"results/_backup_{stamp}\n")
        shutil.rmtree(done, ignore_errors=True)
        for stale in (root / "trials.csv", root / "decisions.json"):      # rebuilt by the steps (backup was taken above)
            stale.unlink(missing_ok=True)
    done.mkdir(parents=True, exist_ok=True)
    log = []
    for name, cmd in STEPS:
        marker = done / f"{name}.ok"
        if marker.exists():
            print(f"[skip] {name}")
            continue
        t0 = time.time()
        print(f"[run ] {name}", flush=True)
        res = subprocess.run(cmd)
        if res.returncode != 0 and name != "tests":
            raise SystemExit(f"step {name} failed with code {res.returncode}")
        marker.write_text(f"{time.time() - t0:.1f}s returncode={res.returncode}\n")
        log.append((name, round(time.time() - t0, 1)))
    print("steps run:", log)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true")
    main(ap.parse_args().resume)
