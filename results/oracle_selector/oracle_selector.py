"""POST-HOC, descriptive (decisions_log P): per-scenario oracle arbiter between A (A_det_twin) and B (B_det), from saved results only.

Usage (repository root): python results/oracle_selector/oracle_selector.py
No model is trained and nothing is run on Test. Test numbers are descriptive only and are not used to design any arbiter (P3).
Outputs in results/oracle_selector/: summary.csv, breakdown.csv, signals.csv, perrow.csv, test_v1_cells.csv.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.data import xy  # noqa: E402
from src.models import scores  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402

OUT = ROOT / "results/oracle_selector"
TIE = 0.005
V1_VAL = ROOT / "results/overnight/temporal"
V1_TEST = ROOT / "results/final_test/test"
RECAL = ROOT / "results/v2/recal/scenarios.csv"
V2_TEST = ROOT / "results/final_test_v2/test/scores.csv"


def load_sets():
    """{name: frame with A, B, flags, k, fault, level, sensors, batch}; one row = one scored scenario run (clean rows excluded)."""
    sets = {}
    for name, d in (("1_val7_v1", V1_VAL), ("3_test_v1_pooled", V1_TEST)):
        s = pd.read_csv(d / "strategy_scenarios.csv")
        sets[name] = pd.DataFrame({"A": s.A_det_twin_f1, "B": s.B_det_f1, "flags": s.mean_flagged_per_row, "k": s.kset,
                                   "fault": s.fault, "level": s.level.astype(str), "sensors": s.sensors.astype(str),
                                   "batch": "b7" if name.startswith("1") else "pooled_b8-10"})
    r = pd.read_csv(RECAL, dtype={"sensors": str})
    for model, tag in (("calibrated", "2_driftdev_calibrated"), ("uncalibrated", "2b_driftdev_uncalibrated")):
        s = r[(r.model == model) & (r.protocol == "drift_dev") & (r.setting != "clean")]
        sets[tag] = pd.DataFrame({"A": s.A, "B": s.B, "flags": s.mean_n_flag, "k": s.setting, "fault": s.fault, "level": "medium",
                                  "sensors": s.sensors, "batch": "b" + s.batch.astype(str)}).reset_index(drop=True)
    v = pd.read_csv(V2_TEST, dtype={"sensors": str})
    v = v[(v.model == "b") & v.subset.isin(["b8", "b9", "b10"]) & (v.setting != "clean") & v.method.isin(["A", "B"])]
    p = v.pivot_table(index=["subset", "cal_seed", "sid", "setting", "fault", "sensors", "level"], columns="method", values="f1").reset_index()
    sets["4_test_v2_b"] = pd.DataFrame({"A": p.A, "B": p.B, "flags": np.nan, "k": p.setting, "fault": p.fault,
                                        "level": p.level.astype(str), "sensors": p.sensors, "batch": p.subset})
    return sets


def outcome(d):
    return np.where(d.A - d.B >= TIE, "A>B", np.where(d.B - d.A >= TIE, "B>A", "tie"))


def summary(name, d):
    best = "A" if d.A.mean() >= d.B.mean() else "B"
    orc = np.maximum(d.A, d.B)
    o = pd.Series(outcome(d)).value_counts()
    return {"dataset": name, "n": len(d), "n_A>B": int(o.get("A>B", 0)), "n_B>A": int(o.get("B>A", 0)), "n_tie": int(o.get("tie", 0)),
            "mean_A": d.A.mean(), "mean_B": d.B.mean(), "mean_oracle": orc.mean(), "best_fixed": best,
            "gain_vs_best": orc.mean() - d[best].mean(), "worst_A": d.A.min(), "worst_B": d.B.min(), "worst_oracle": orc.min()}


def breakdown(name, d):
    """Gain over the dataset's better fixed method, split by each dimension; share = part of the total gain in that group."""
    best = "A" if d.A.mean() >= d.B.mean() else "B"
    d = d.assign(g=np.maximum(d.A, d.B) - d[best], s01s02=d.sensors.str.split("-").map(lambda s: bool({"1", "2"} & set(s))),
                 b_wins=outcome(d) == "B>A", a_wins=outcome(d) == "A>B")
    total = d.g.sum()
    rows = []
    for dim in ("fault", "level", "k", "sensors", "batch", "s01s02"):
        for val, x in d.groupby(dim):
            rows.append({"dataset": name, "dim": dim, "value": val, "n": len(x), "mean_A": x.A.mean(), "mean_B": x.B.mean(),
                         "mean_oracle": np.maximum(x.A, x.B).mean(), "mean_gain": x.g.mean(),
                         "share_of_total_gain": x.g.sum() / total if total > 0 else np.nan,
                         "frac_B>A": x.b_wins.mean(), "frac_A>B": x.a_wins.mean()})
    return rows


def signals(name, d):
    """Runtime-visible signal (mean flagged sensors per row) by outcome, overall and within each k; AUROC of B>A vs A>B (rank statistic)."""
    if d["flags"].isna().all():
        return [{"dataset": name, "k": "all", "note": "not available: no flag counts saved"}]
    d = d.assign(out=outcome(d))
    rows = []
    for k, x in [("all", d)] + list(d.groupby("k")):
        r = {"dataset": name, "k": k}
        for o in ("A>B", "B>A", "tie"):
            r[f"n_{o}"] = int((x.out == o).sum())
            r[f"flags_{o}"] = x["flags"][x.out == o].mean()
        ab = x[x.out != "tie"]
        r["auroc_flags_B>A_vs_A>B"] = roc_auc_score(ab.out == "B>A", ab["flags"]) if ab.out.nunique() == 2 else np.nan
        rows.append(r)
    return rows


def perrow_val7():
    """Validation 7 only: row correct if A or B is correct (extremely optimistic, not achievable). Labels of batch 7 via the loader."""
    y = xy(get_protocol_data(load_config(ROOT / "configs/preprocessing.yaml")).eval)[1]
    P = np.load(V1_VAL / "strategy_preds.npz")
    A, B = P["A_det_twin"], P["B_det"]
    s = pd.read_csv(V1_VAL / "strategy_scenarios.csv")
    fa = np.array([scores(y, a)["macro_f1"] for a in A])
    assert np.allclose(fa, s.A_det_twin_f1, atol=1e-9), "row order / labels do not reproduce the saved A scores"
    fb = np.array([scores(y, b)["macro_f1"] for b in B])
    assert np.allclose(fb, s.B_det_f1, atol=1e-9), "row order / labels do not reproduce the saved B scores"
    fo = np.array([scores(y, np.where(b == y, b, a))["macro_f1"] for a, b in zip(A, B)])
    return [{"dataset": "1_val7_v1", "n": len(fo), "mean_A": fa.mean(), "mean_B": fb.mean(), "mean_scenario_oracle": np.maximum(fa, fb).mean(),
             "mean_row_oracle_UNACHIEVABLE": fo.mean(), "worst_row_oracle": fo.min(), "rows_per_scenario": len(y)}]


def test_v1_cells():
    """v1 Test per batch: only cell means (kset x fault x level, mean over 5 fault seeds) are saved per batch."""
    c = pd.read_csv(V1_TEST / "ft_comparison.csv")
    rows = []
    for sub, x in c.groupby("subset"):
        best = "A_det_twin" if x.A_det_twin.mean() >= x.B_det.mean() else "B_det"
        o = np.maximum(x.A_det_twin, x.B_det)
        rows.append({"subset": sub, "n_cells": len(x), "mean_A": x.A_det_twin.mean(), "mean_B": x.B_det.mean(), "mean_cell_oracle": o.mean(),
                     "best_fixed": best, "gain_vs_best": o.mean() - x[best].mean(),
                     "cells_B>A": int((x.B_det - x.A_det_twin >= TIE).sum()), "cells_A>B": int((x.A_det_twin - x.B_det >= TIE).sum())})
    return rows


if __name__ == "__main__":
    sets = load_sets()
    pd.DataFrame([summary(n, d) for n, d in sets.items()]).round(4).to_csv(OUT / "summary.csv", index=False)
    pd.DataFrame([r for n, d in sets.items() for r in breakdown(n, d)]).round(4).to_csv(OUT / "breakdown.csv", index=False)
    pd.DataFrame([r for n, d in sets.items() for r in signals(n, d)]).round(4).to_csv(OUT / "signals.csv", index=False)
    pd.DataFrame(perrow_val7()).round(4).to_csv(OUT / "perrow.csv", index=False)
    pd.DataFrame(test_v1_cells()).round(4).to_csv(OUT / "test_v1_cells.csv", index=False)
    print(pd.read_csv(OUT / "summary.csv").to_string())
