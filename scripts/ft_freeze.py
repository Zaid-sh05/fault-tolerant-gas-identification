"""Freeze everything the final test depends on: FREEZE_MANIFEST.md (repo root) and results/FREEZE_HASHES.json.

Usage: python scripts/ft_freeze.py                  # full freeze: needs a clean tracked tree, records HEAD
       python scripts/ft_freeze.py --artifacts-only  # only results/FREEZE_HASHES.json (used before the dry run)
The manifest lists the code commit, the sha256 of every config / source / script file, of the fitted objects (models,
detectors, reduced SVMs, all fitted on Train only) and the frozen choices read back from those files. The tag
`frozen-before-test` is placed on the commit that adds the manifest (it differs from the recorded code commit by the
manifest and hash files only).
"""
import argparse
import hashlib
import json
import platform
import subprocess
from datetime import date
from pathlib import Path

import joblib
import lightgbm
import numpy as np
import pandas as pd
import sklearn

from src.scenarios import LEVELS, MEDIUM, SENSOR_SETS, build_scenarios
from src.splits import load_config
from src.strategies import CAP
from src.study import AUG_SEEDS

TEMPORAL = Path("results/overnight/temporal")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def artifact_hashes():
    files = sorted(p for d in ("models", "detectors", "reduced") for p in (TEMPORAL / d).glob("*.joblib"))
    return {p.relative_to(TEMPORAL).as_posix(): sha(p) for p in files}


def table(rows, header):
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] +
                     ["| " + " | ".join(map(str, r)) + " |" for r in rows])


def main(artifacts_only):
    arts = artifact_hashes()
    json.dump({"artifacts": arts}, open("results/FREEZE_HASHES.json", "w"), indent=1)
    print(f"{len(arts)} fitted objects hashed")
    if artifacts_only:
        return
    assert not git("status", "--porcelain", "--untracked-files=no"), "tracked files have uncommitted changes"
    head = git("rev-parse", "HEAD")
    cfgs = sorted(Path("configs").glob("*.yaml"))
    code = sorted([*Path("src").glob("*.py"), *Path("scripts").glob("*.py"), Path("scripts/run_final_test.sh")])
    extra = [Path("requirements.txt"), Path("pyproject.toml"), Path("results/overnight/final_pipeline.json"),
             TEMPORAL / "g2_verdict.json", Path("results/decisions_log.md")]

    fin = json.load(open("results/overnight/final_pipeline.json"))
    g2 = json.load(open(TEMPORAL / "g2_verdict.json"))
    chosen = g2["chosen_normalisation"]
    det = joblib.load(TEMPORAL / "detectors" / f"{chosen}.joblib")
    pre = load_config("configs/preprocessing.yaml")
    scenarios = build_scenarios(AUG_SEEDS)
    scen_hash = hashlib.sha256(repr(scenarios).encode()).hexdigest()
    sensors = [f"S{s + 1:02d}" for s in range(16)]

    md = [f"# FREEZE MANIFEST - everything fixed before batches 8-10 are opened",
          f"Date: {date.today().isoformat()}   |   code commit: `{head}`   |   branch: `{git('branch', '--show-current')}`   "
          f"|   tag: `frozen-before-test` (on the commit that adds this file)",
          f"Environment: Python {platform.python_version()}, scikit-learn {sklearn.__version__}, lightgbm {lightgbm.__version__}, "
          f"numpy {np.__version__}, pandas {pd.__version__}; requirements.txt hash below.", "",
          "## 1. Rules of the single run",
          "- Batches 8-10 are opened once, by `bash scripts/run_final_test.sh configs/final_test.yaml` (marker file `RUN_STARTED` "
          "refuses a second start). Approval: the user, 2026-10-08.",
          "- Same code and configs, verbatim. No change after the run, whatever the outcome. A programming error stops the run and "
          "is reported; it is not fixed and re-run without telling the user.",
          "- Nothing is refitted: the models, detectors, thresholds and reduced SVMs below were fitted on Train (batches 1-6) at "
          "Validation time. Reduced SVMs for sensor sets that Validation never produced are trained on demand from the same Train "
          "rows with the frozen parameters.",
          "- Test results are reported per batch (8, 9, 10) and pooled, with the same tables as Validation.", "",
          "## 2. Frozen choices (read back from the files, not retyped)",
          f"- Pipeline spec: `{json.dumps(fin['spec'])}` (raw 128 features, StandardScaler fitted on Train, NaN -> 0 for the SVM).",
          f"- SVM: RBF, C={fin['svm_params']['C']}, gamma={fin['svm_params']['gamma']}, seed {pre['seed']}.  LightGBM: `{json.dumps(fin['lgbm_params'])}`.",
          f"- Cleaning: invalid-value rule |x - median| / MAD > {pre['cleaning']['invalid_value_rule']['threshold']} fitted on Train; flagged Train rows dropped; "
          "evaluation rows never dropped (flagged ones are counted).",
          f"- Fault augmentation: seeds {list(AUG_SEEDS)}, copies {pre['augmentation']['copies']}; 5 seeds per augmented baseline.",
          f"- Faults: Dropout, Bias, Stuck, Random on whole 8-feature blocks; levels {json.dumps(LEVELS)}; medium severity {json.dumps(MEDIUM)}; "
          f"Bias unit sigma_robust = IQR/1.349 of cleaned Train; shared affected rows; {len(AUG_SEEDS)} seeds.",
          f"- Sensor sets: k=1 all 16 sensors; k=2 replicate pairs; k=4 groups (HYPOTHESIS, not documented by the dataset): `{json.dumps(SENSOR_SETS['k4'])}` (0-based).",
          f"- Scenario list: {len(scenarios)} scenarios, sha256 of its repr `{scen_hash}`.",
          f"- Detector: Ridge in standardised signed-log space, normalisation **{chosen}** (Validation median isolation AUROC "
          f"{g2['median_auroc']:.4f}; the other normalisation scored {min(g2['candidates_median_auroc'].values()):.4f}); alarm threshold = "
          f"{det.pct:g}th percentile of the Train out-of-fold normalised score; leave-pair-out detector = sensitivity analysis only.",
          f"- Strategies: A reconstruct flagged blocks (Ridge from unflagged sensors) then the clean SVM; B SVM trained without the flagged sensors; "
          f"C eight replicate-pair experts, reliability weight 1/max(1, ratio)^2 (min over the expert's two sensors); at most {CAP} sensors "
          "acted upon per row; Oracle variants use the true faulty sensors (analysis bound only). Main result: A, with B and the Oracle as references; "
          "C is reported as a negative result and is not redesigned.",
          "- Gates (rules unchanged, `results/decisions_log.md` B4, B6-B8, B11): G1 >= 2 of 4 fault types lose >= 0.03 Macro-F1 at k=1, medium severity; "
          "G2 median isolation AUROC over the four fault types at k=1, medium >= 0.80; G3 at least one comparison of a real-detector strategy beats the best "
          "augmented baseline with a paired-bootstrap 95% interval excluding 0 (lenient; the full tables are shown). Intervals resample rows only, so they are optimistic.", "",
          "### Detector parameters (primary detector)",
          table([(s, f"{a:g}", f"{t:.4f}") for s, a, t in zip(sensors, det.alpha_, det.tau_)], ["sensor", "ridge alpha", "alarm threshold tau"]), "",
          "## 3. Files", f"Fitted objects: {len(arts)} files, hashes in `results/FREEZE_HASHES.json` (verified by `scripts/ft_prepare.py` before the run).", "",
          "### Configs", table([(p.as_posix(), sha(p)) for p in cfgs], ["file", "sha256"]), "",
          "### Other frozen inputs", table([(p.as_posix(), sha(p)) for p in extra], ["file", "sha256"]), "",
          "### Source and scripts", table([(p.as_posix(), sha(p)) for p in code], ["file", "sha256"]), ""]
    Path("FREEZE_MANIFEST.md").write_text("\n".join(md), encoding="utf-8")
    print(f"FREEZE_MANIFEST.md written for commit {head}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts-only", action="store_true")
    main(ap.parse_args().artifacts_only)
