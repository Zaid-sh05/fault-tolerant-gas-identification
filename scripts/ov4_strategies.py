"""Overnight Part 4: inference-time strategies on the faulted evaluation rows (Validation only).

Usage: python scripts/ov4_strategies.py --config configs/preprocessing.yaml --name temporal
       python scripts/ov4_strategies.py --config configs/reference_iid.yaml --name reference_iid --reduced
Needs Part 2 (scenarios, baseline predictions) and Part 3 (detectors, g2_verdict.json).
Outputs: results/overnight/<name>/{strategy_scenarios.csv, strategy_preds.npz}
Methods per scenario (decisions_log B10): A_det_twin, A_det_notwin, A_orc_twin, A_orc_notwin, B_det, B_orc, C_det, C_equal.
The Oracle variants use the true faulty sensors per row and are an analysis bound only. Chunks are checkpointed.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

from src.models import scores  # noqa: E402
from src.scenarios import apply_scenario, build_scenarios  # noqa: E402
from src.strategies import StrategyKit, acted_sets  # noqa: E402
from src.study import AUG_SEEDS, Study  # noqa: E402

CHUNK = 30
METHODS = ["A_det_twin", "A_det_notwin", "A_orc_twin", "A_orc_notwin", "B_det", "B_orc", "C_det", "C_equal"]


def make_kit(study):
    chosen = json.load(open(study.dir / "g2_verdict.json"))["chosen_normalisation"]
    det = joblib.load(study.dir / "detectors" / f"{chosen}.joblib")
    svm = joblib.load(study.dir / "models" / "svm.joblib")
    return StrategyKit(study.pre, svm, study.Xtr, study.ytr, det, study.svm_params, str(study.dir / "reduced"), study.seed), det


def run_chunk(cfg_path, name, reduced, index, sids):
    study = Study(cfg_path, name)
    path = study.dir / "ov4_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    kit, det = make_kit(study)
    scenarios = build_scenarios(AUG_SEEDS, ("k1", "k2") if reduced else ("k1", "k2", "k4"), reduced)
    rows, preds = [], {m: [] for m in METHODS}
    for sid in sids:
        sc = scenarios[sid]
        Xf, truth = apply_scenario(study.Xev, sc, study.stats)
        R = det.ratio(Xf)
        det_sets = acted_sets(R, R > 1.0)
        orc_sets = acted_sets(truth.astype(float), truth)
        proba = kit.expert_proba(Xf)
        out = {"A_det_twin": kit.predict_A(Xf, det_sets, False), "A_det_notwin": kit.predict_A(Xf, det_sets, True),
               "A_orc_twin": kit.predict_A(Xf, orc_sets, False), "A_orc_notwin": kit.predict_A(Xf, orc_sets, True),
               "B_det": kit.predict_B(Xf, det_sets), "B_orc": kit.predict_B(Xf, orc_sets),
               "C_det": kit.combine(proba, R), "C_equal": kit.combine(proba, None)}
        row = {"sid": sid, "mean_flagged_per_row": float(np.mean([len(s) for s in det_sets]))}
        for m, y_hat in out.items():
            s = scores(study.yev, y_hat)
            row[f"{m}_f1"], row[f"{m}_acc"] = s["macro_f1"], s["accuracy"]
            preds[m].append(y_hat.astype(np.int8))
        rows.append(row)
    path.parent.mkdir(exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"rows": rows, "preds": {m: np.stack(v) for m, v in preds.items()}}, f)
    return str(path)


def main(cfg_path, name, reduced):
    study = Study(cfg_path, name)
    scenarios = build_scenarios(AUG_SEEDS, ("k1", "k2") if reduced else ("k1", "k2", "k4"), reduced)
    priority = {"k4": 0, "k2": 1, "k1": 2}                    # the user's order if time runs out: k=4 and k=2 first
    sids = sorted(range(len(scenarios)), key=lambda i: (priority[scenarios[i].kset], i))
    chunks = [sids[i:i + CHUNK] for i in range(0, len(sids), CHUNK)]
    print(f"{name}: {len(scenarios)} scenarios in {len(chunks)} chunks (k4, k2, then k1)", flush=True)
    Parallel(n_jobs=6, verbose=5)(delayed(run_chunk)(cfg_path, name, reduced, i, c) for i, c in enumerate(chunks))
    merge(study, len(chunks))


def merge(study, n_chunks):
    """Merge the finished chunks (a partial set is allowed; the analysis works on the scenarios that exist)."""
    rows, preds = [], {}
    for i in range(n_chunks):
        path = study.dir / "ov4_chunks" / f"chunk_{i:03d}.pkl"
        if not path.exists():
            continue
        with open(path, "rb") as f:
            d = pickle.load(f)
        rows += d["rows"]
        for m, v in d["preds"].items():
            preds.setdefault(m, []).append(v)
    df = pd.DataFrame(rows).merge(pd.read_csv(study.dir / "scenarios.csv"), on="sid")
    order = np.argsort(df["sid"].to_numpy())
    df.iloc[order].reset_index(drop=True).to_csv(study.dir / "strategy_scenarios.csv", index=False)
    np.savez_compressed(study.dir / "strategy_preds.npz", **{m: np.concatenate(v)[order] for m, v in preds.items()})
    print(f"merged {len(df)} scenarios from {n_chunks} chunk files", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    ap.add_argument("--name", default="temporal")
    ap.add_argument("--reduced", action="store_true")
    a = ap.parse_args()
    main(a.config, a.name, a.reduced)
