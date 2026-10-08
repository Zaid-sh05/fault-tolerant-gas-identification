"""Gate P6: compare the results of the latest full run with the backup taken before it.

Usage: python scripts/verify_reproducibility.py
Compares every CSV/JSON that exists in both trees, numerically (rtol 1e-9), ignoring wall-clock columns.
Writes results/preprocessing/reproducibility.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

IGNORE_COLUMNS = {"seconds", "fit_s"}
NEW_ROOTS = ["preprocessing", "main", "main_cleaned", "main_cleaned_drop223"]
SKIP = {"reproducibility.json", "junit.xml"}


def compare_csv(a, b):
    x, y = pd.read_csv(a), pd.read_csv(b)
    cols = [c for c in x.columns if c not in IGNORE_COLUMNS]
    if list(x.columns) != list(y.columns) or len(x) != len(y):
        return "shape/columns differ"
    worst = 0.0
    for c in cols:
        if pd.api.types.is_numeric_dtype(x[c]) and not pd.api.types.is_bool_dtype(x[c]):
            d = np.nanmax(np.abs(x[c].to_numpy(float) - y[c].to_numpy(float))) if len(x) else 0.0
            tol = 1e-9 * max(1.0, float(np.nanmax(np.abs(x[c].to_numpy(float)))) if len(x) else 1.0)
            if d > tol:
                return f"column {c} differs by {d:.3g}"
            worst = max(worst, d)
        elif not x[c].astype(str).equals(y[c].astype(str)):
            return f"column {c} differs (text)"
    return None


def main():
    backup = Path(Path("results/_backup_latest.txt").read_text().strip())
    rows, differing = 0, []
    for root in NEW_ROOTS:
        for new in sorted(Path("results", root).rglob("*")):
            if new.suffix not in (".csv", ".json") or new.name in SKIP or "_done" in new.parts:
                continue
            old = backup / root / new.relative_to(Path("results", root))
            if not old.exists():
                differing.append({"file": str(new), "problem": "no counterpart in the backup (new file)"})
                continue
            rows += 1
            if new.suffix == ".csv":
                problem = compare_csv(old, new)
            else:
                problem = None if json.load(open(old)) == json.load(open(new)) else "json differs"
            if problem:
                differing.append({"file": str(new), "problem": problem})
    out = {"backup": str(backup), "files_compared": rows, "files_differing": len(differing), "differing": differing,
           "reproducible": len(differing) == 0}
    json.dump(out, open("results/preprocessing/reproducibility.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "differing"}, indent=1))
    for d in differing[:40]:
        print(" ", d)


if __name__ == "__main__":
    main()
