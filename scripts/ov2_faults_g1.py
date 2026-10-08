"""Overnight Part 2: faults on whole sensor blocks, baselines under faults, gate G1.

Usage: python scripts/ov2_faults_g1.py --config configs/preprocessing.yaml --name temporal
       python scripts/ov2_faults_g1.py --config configs/reference_iid.yaml --name reference_iid --reduced
Outputs: results/overnight/<name>/{scenarios.csv, truth_masks.npz, baseline_scenarios.csv, baseline_preds.npz,
                                    g1_summary.csv, g1_verdict.json}
Scenarios are generated once (src/scenarios.py), their hashes are saved, and every method receives the same faulted
matrix. Chunks are checkpointed: re-running skips finished chunks.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):     # one BLAS thread per worker: no oversubscription
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

from src.models import scores  # noqa: E402
from src.scenarios import MEDIUM, apply_scenario, build_scenarios, scenario_table  # noqa: E402
from src.study import AUG_SEEDS, Study  # noqa: E402

CHUNK = 30


def run_chunk(cfg_path, name, reduced, index, sids):
    study = Study(cfg_path, name)
    path = study.dir / "g1_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    scenarios = build_scenarios(AUG_SEEDS, ("k1", "k2") if reduced else ("k1", "k2", "k4"), reduced)
    models = study.models()
    rows, preds = [], {n: [] for n in models}
    for sid in sids:
        sc = scenarios[sid]
        Xf, _ = apply_scenario(study.Xev, sc, study.stats)
        p = study.predict(models, study.pre.transform(Xf))
        row = {"sid": sid}
        for n, y_hat in p.items():
            s = scores(study.yev, y_hat)
            row[f"{n}_f1"], row[f"{n}_acc"] = s["macro_f1"], s["accuracy"]
            preds[n].append(y_hat.astype(np.int8))
        rows.append(row)
    path.parent.mkdir(exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"rows": rows, "preds": {n: np.stack(v) for n, v in preds.items()}}, f)
    return str(path)


def main(cfg_path, name, reduced, jobs=6):
    study = Study(cfg_path, name)
    seeds = AUG_SEEDS
    ksets = ("k1", "k2") if reduced else ("k1", "k2", "k4")
    scenarios = build_scenarios(seeds, ksets, reduced)
    if not (study.dir / "scenarios.csv").exists():
        table, masks = scenario_table(scenarios, study.Xev, study.stats)
        table.to_csv(study.dir / "scenarios.csv", index=False)
        np.savez_compressed(study.dir / "truth_masks.npz", masks=masks, n_rows=len(study.Xev))
    print(f"{name}: {len(scenarios)} scenarios, train {len(study.Xtr)}, eval {len(study.Xev)}", flush=True)
    models = study.models()                                           # trains and caches missing models
    clean = {n: scores(study.yev, p) for n, p in study.predict(models, study.pre.transform(study.Xev)).items()}
    pd.DataFrame(clean).T.round(4).to_csv(study.dir / "clean_eval.csv")
    print("clean:", {n: round(v["macro_f1"], 4) for n, v in clean.items() if "aug" not in n}, flush=True)

    sids = list(range(len(scenarios)))
    chunks = [sids[i:i + CHUNK] for i in range(0, len(sids), CHUNK)]
    Parallel(n_jobs=jobs, verbose=5)(delayed(run_chunk)(cfg_path, name, reduced, i, c) for i, c in enumerate(chunks))

    rows, preds = [], {}
    for i in range(len(chunks)):
        with open(study.dir / "g1_chunks" / f"chunk_{i:03d}.pkl", "rb") as f:
            d = pickle.load(f)
        rows += d["rows"]
        for n, v in d["preds"].items():
            preds.setdefault(n, []).append(v)
    res = pd.DataFrame(rows).merge(pd.read_csv(study.dir / "scenarios.csv"), on="sid")
    res.to_csv(study.dir / "baseline_scenarios.csv", index=False)
    np.savez_compressed(study.dir / "baseline_preds.npz", **{n: np.concatenate(v) for n, v in preds.items()})

    # ---- G1 ---------------------------------------------------------------------------
    best_clean = max(("svm", "lgbm"), key=lambda n: clean[n]["macro_f1"])
    res["drop"] = clean[best_clean]["macro_f1"] - res[f"{best_clean}_f1"]
    for kind in ("svm", "lgbm"):
        res[f"{kind}_aug_f1"] = res[[f"{kind}_aug{s}_f1" for s in AUG_SEEDS]].mean(axis=1)
    res["svm_drop"] = clean["svm"]["macro_f1"] - res["svm_f1"]
    res["svm_aug_drop"] = clean["svm"]["macro_f1"] - res["svm_aug_f1"]
    g = (res.groupby(["kset", "fault", "level"])
         .agg(n=("sid", "size"), best_clean_drop=("drop", "mean"), svm_drop=("svm_drop", "mean"),
              svm_f1=("svm_f1", "mean"), lgbm_f1=("lgbm_f1", "mean"), svm_aug_f1=("svm_aug_f1", "mean"),
              lgbm_aug_f1=("lgbm_aug_f1", "mean")).reset_index())
    # std over the augmentation seeds (mean over scenarios first)
    for kind in ("svm", "lgbm"):
        per_seed = pd.concat([res.groupby(["kset", "fault", "level"])[f"{kind}_aug{s}_f1"].mean() for s in AUG_SEEDS], axis=1)
        g[f"{kind}_aug_f1_std_over_aug_seeds"] = per_seed.std(axis=1).to_numpy()
    g.round(4).to_csv(study.dir / "g1_summary.csv", index=False)

    k1 = g[g.kset == "k1"]
    per_type = {f: float(k1[(k1.fault == f) & (k1.level == MEDIUM[f])]["best_clean_drop"].iloc[0]) for f in MEDIUM}
    counted = [f for f, d in per_type.items() if d >= 0.03]
    verdict = {"best_clean_baseline": best_clean, "clean_macro_f1": clean[best_clean]["macro_f1"],
               "k1_medium_mean_drop_by_fault": per_type, "types_with_drop_ge_0.03": counted,
               "G1_passes": len(counted) >= 2, "rule": "registered in results/decisions_log.md B4"}
    json.dump(verdict, open(study.dir / "g1_verdict.json", "w"), indent=1)
    pd.set_option("display.width", 220)
    print(g[g.kset == "k1"].round(4).to_string(index=False))
    print(json.dumps(verdict, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    ap.add_argument("--name", default="temporal")
    ap.add_argument("--reduced", action="store_true")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    main(a.config, a.name, a.reduced, a.jobs)
