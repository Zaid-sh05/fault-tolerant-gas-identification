"""PARTIAL summary of recalibration stage 2 while it is still running (reads finished chunk files only; computes nothing new).

Usage: python scripts/v2_recal_partial.py   ->  results/v2/recal/PARTIAL.md (printed)
Only calibrated configurations with all their chunks are used. The exact paired reference (uncalibrated M0 on the same rows) is written by
stage 2 last; until then the reference shown is the arbiter run (uncalibrated M0 on ALL rows of the batch), marked APPROXIMATE.
"""
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, "scripts")
import v2_arbiter as arb  # noqa: E402

REC = Path("results/v2/recal")
METHODS = ["svm", "A", "B", "svm_aug", "H1", "H2", "H3", "A_oracle", "B_oracle"]


def main():
    n_chunks = len(range(0, len(arb.scenario_list()), arb.CHUNK))
    rows, done = [], []
    for d in sorted(REC.glob("*_n*_s*")):
        files = sorted((d / "chunks").glob("chunk_*.pkl"))
        if len(files) == n_chunks:
            done.append(d.name)
            rows += [r for f in files for r in pickle.load(open(f, "rb"))]
    total = len(list(REC.glob("*_n*_s*")))
    md = [f"# Recalibration stage 2: PARTIAL ({len(done)} of {total} calibrated configurations complete)", ""]
    if not rows:
        md.append("No configuration is complete yet.")
    else:
        df = pd.DataFrame(rows)
        df["k"] = df["setting"]
        cal = (df.groupby(["protocol", "batch", "cal_seed", "k"])[METHODS].mean().reset_index()
               .groupby(["protocol", "batch", "k"])[METHODS].agg(["mean", "std"]))
        ref = pd.read_csv(arb.OUT / "scenarios.csv")
        ref = ref[ref.set_index(["protocol", "batch"]).index.isin(df.set_index(["protocol", "batch"]).index.unique())]
        approx = ref.groupby(["protocol", "batch", "setting"])[METHODS].mean()
        fmt = pd.DataFrame({m: cal[(m, "mean")].map("{:.3f}".format) + " ± " + cal[(m, "std")].map("{:.3f}".format) for m in METHODS})
        seeds = df.groupby(["protocol", "batch"])["cal_seed"].nunique()
        md += ["Calibrated (n = 10 per gas), mean ± std over the finished calibration seeds:", "", fmt.to_markdown(), "",
               "Seeds finished per batch: " + ", ".join(f"{p} b{b}: {v}" for (p, b), v in seeds.items()), "",
               "APPROXIMATE uncalibrated reference (arbiter run, all rows of the batch, not paired):", "", approx.round(3).to_markdown(), "",
               "Finished configurations: " + ", ".join(done)]
    (REC / "PARTIAL.md").write_text(chr(10).join(md), encoding="utf-8")
    print(chr(10).join(md))


if __name__ == "__main__":
    main()
