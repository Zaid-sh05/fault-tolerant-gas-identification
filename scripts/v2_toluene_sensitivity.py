"""Sensitivity of the Drift-Dev candidate scores to toluene (POST-HOC, decisions_log I8; does not change the G6 choice). Batches 1-7 only.

Usage: python scripts/v2_toluene_sensitivity.py
Output: results/v2/toluene_sensitivity.csv and .md. Same build code as scripts/v2_dev.py; the all-rows column must reproduce candidates.csv.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys  # noqa: E402

import pandas as pd  # noqa: E402

sys.path.insert(0, "scripts")
from v2_dev import OUT, PROTOCOLS, SIMPLICITY, build, load  # noqa: E402
from src.models import scores  # noqa: E402

TOLUENE = 6


def main():
    Xtr, ytr, btr, evals = load(PROTOCOLS["drift_dev"])
    ref = pd.read_csv(OUT / "candidates.csv").set_index("candidate")
    rows = []
    for name in SIMPLICITY:
        _, _, predict = build(name, Xtr, ytr, btr)
        row = {"candidate": name}
        for b, (X, y) in evals.items():
            p = predict(X)
            keep = y != TOLUENE
            row[f"b{b}_all"] = scores(y, p)["macro_f1"]
            row[f"b{b}_no_toluene"] = scores(y[keep], p[keep])["macro_f1"]
            row[f"b{b}_toluene_rows"] = int((~keep).sum())
            row[f"b{b}_toluene_recall"] = float((p[~keep] == TOLUENE).mean())
            assert abs(row[f"b{b}_all"] - ref.loc[name, f"drift_dev_b{b}"]) < 5e-4, f"{name} b{b} does not reproduce candidates.csv"
        row["mean_all"] = (row["b6_all"] + row["b7_all"]) / 2
        row["mean_no_toluene"] = (row["b6_no_toluene"] + row["b7_no_toluene"]) / 2
        rows.append(row)
        print(name, "done", flush=True)
    tab = pd.DataFrame(rows)
    tab.round(4).to_csv(OUT / "toluene_sensitivity.csv", index=False)
    (OUT / "toluene_sensitivity.md").write_text(
        "# Drift-Dev with and without toluene (POST-HOC sensitivity, decisions_log I8)\n\n" + tab.round(3).to_markdown(index=False) + "\n",
        encoding="utf-8")
    print(tab.round(3).to_markdown(index=False))


if __name__ == "__main__":
    main()
