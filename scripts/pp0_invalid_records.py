"""Report which records the invalid-value rule (src/cleaning.py) captures. Deletes nothing.
(The actual dropping of Train records happens in src/splits.py when the config has a `cleaning` block.)

Usage: python scripts/pp0_invalid_records.py
For each protocol the rule is fitted on that protocol's Train rows only (median and MAD per feature),
then applied to its Train rows and to its evaluation rows. Batches 1-7 only.
Outputs: results/preprocessing/cleaning/invalid_records_<protocol>.csv, invalid_summary.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.cleaning import InvalidValueRule
from src.data import FEATURE_KINDS, FEATURES, GAS_NAMES, xy
from src.splits import get_protocol_data, load_config

CONFIGS = {"temporal": "configs/preprocessing.yaml", "reference_iid": "configs/reference_iid.yaml"}


def describe(rule, frame, role):
    X, _ = xy(frame)
    z = rule.robust_z(X)
    hit = rule.cells(X)
    rows = []
    for i in np.flatnonzero(hit.any(1)):
        cells = np.flatnonzero(hit[i])
        sensors = sorted({c // 8 + 1 for c in cells})
        worst = cells[np.argmax(z[i, cells])]
        rows.append({"role": role, "batch": int(frame["batch"].iloc[i]), "line": int(frame["line"].iloc[i]),
                     "gas": GAS_NAMES[int(frame["gas"].iloc[i])], "n_cells": len(cells),
                     "sensors": " ".join(f"S{s:02d}" for s in sensors),
                     "worst_feature": FEATURES[worst], "worst_value": float(X[i, worst]),
                     "worst_median": float(rule.median_[worst]), "max_robust_z": float(z[i, worst])})
    return rows


def main():
    out = Path("results/preprocessing/cleaning")
    out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name, path in CONFIGS.items():
        cfg = load_config(path)
        cfg.pop("cleaning", None)                      # report on the frames BEFORE any cleaning
        proto = get_protocol_data(cfg)
        rule = InvalidValueRule().fit(xy(proto.train)[0])
        rows = describe(rule, proto.train, "train") + describe(rule, proto.eval, "eval")
        table = pd.DataFrame(rows)
        table.to_csv(out / f"invalid_records_{name}.csv", index=False)
        summary[name] = {
            "threshold": rule.threshold, "features_not_scorable_mad0": int((~rule.scorable_).sum()),
            "records_checked": {"train": len(proto.train), "eval": len(proto.eval)},
            "flagged": {"train": int((table["role"] == "train").sum()) if len(table) else 0,
                        "eval": int((table["role"] == "eval").sum()) if len(table) else 0}}
        print(f"\n== {name}: rule fitted on {len(proto.train)} Train rows, threshold {rule.threshold:g} MADs ==")
        print(f"features with MAD = 0 (not scorable): {summary[name]['features_not_scorable_mad0']}")
        print("flagged:", summary[name]["flagged"])
        if len(table):
            print(table.round(1).to_string(index=False))
    json.dump(summary, open(out / "invalid_summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
