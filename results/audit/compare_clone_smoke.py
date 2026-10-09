"""Reproduction check: the Drift-Dev smoke run made in a CLEAN CLONE at tag frozen-before-test-v2 (batches 1-7 only copied in) must equal
the stage-2 results of this repository (configuration drift_dev_b6_n10_s0, seed 0), as scripts/ft_v2_checks.py smoke does in place.

Usage: python results/audit/compare_clone_smoke.py   (reads the clone path from results/audit/clone_dir.txt)
"""
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

REC = Path("results/v2/recal")
clone = Path(Path("results/audit/clone_dir.txt").read_text().strip()) / "repo"
mine = pd.read_csv(clone / "results/v2/ft_smoke/scores.csv")
mine = mine[(mine.subset == "b6") & (mine.cal_seed == 0)]
cal = [r for f in sorted((REC / "drift_dev_b6_n10_s0" / "chunks").glob("chunk_*.pkl")) for r in pickle.load(open(f, "rb"))]
unc = [r for f in sorted((REC / "uncal_drift_dev_b6_n10").glob("chunk_*.pkl")) for r in pickle.load(open(f, "rb")) if r["cal_seed"] == 0]
worst, n = 0.0, 0
for model, ref in (("b", cal), ("a", unc)):
    ref = pd.DataFrame(ref).sort_values("sid")
    for m in ("svm", "A", "B"):
        a = mine[(mine.model == model) & (mine.method == m)].sort_values("sid")["f1"].to_numpy()
        assert len(a) == len(ref), (model, m, len(a), len(ref))
        worst = max(worst, float(np.abs(a - ref[m].to_numpy()).max()))
        n += len(a)
print(f"clean clone at tag frozen-before-test-v2 vs stage 2: {n} scenario-method values, max |difference| = {worst:.2e} -> "
      f"{'IDENTICAL' if worst < 1e-9 else 'MISMATCH'}")
