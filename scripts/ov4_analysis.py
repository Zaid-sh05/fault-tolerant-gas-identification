"""Overnight Part 4 analysis: strategies against the best augmented baseline, paired bootstrap, gate G3.

Usage: python scripts/ov4_analysis.py --config configs/preprocessing.yaml --name temporal
Outputs: results/overnight/<name>/{strategy_comparison.csv, strategy_vs_best_aug.csv, g3_verdict.json}

Paired bootstrap over the evaluation rows (1000 resamples, the same resample for every method and scenario): the
Macro-F1 of every (scenario, method) is recomputed on each resample from weighted confusion matrices; the Macro-F1 of a
setting (fault type x severity x k) is the mean over its scenarios (sensor sets x fault seeds), the augmented baselines
are first averaged over their 5 augmentation seeds. The interval therefore reflects row sampling only.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from scipy.stats import norm  # noqa: E402

from src.study import AUG_SEEDS, Study  # noqa: E402

B = 1000
STRATEGIES = ["A_det_twin", "A_det_notwin", "B_det", "C_det"]               # count for G3
EXTRA = ["A_orc_twin", "A_orc_notwin", "B_orc", "C_equal"]                   # analysis only
BASELINES = ["svm", "svm_aug", "lgbm_aug", "lgbm"]


def boot_f1(y, preds, W):
    """Bootstrapped Macro-F1: preds (S, n) ints -> (S, B). Present classes of the resample only (as `scores`)."""
    out = np.empty((len(preds), W.shape[0]))
    for s, p in enumerate(preds):
        M = np.zeros((len(y), 36), dtype=np.float32)
        M[np.arange(len(y)), (y - 1) * 6 + (p.astype(int) - 1)] = 1.0
        C = (W @ M).reshape(-1, 6, 6)                                       # (B, true, predicted)
        tp = np.einsum("bcc->bc", C)
        true_n, pred_n = C.sum(2), C.sum(1)
        denom = true_n + pred_n
        f1 = np.divide(2 * tp, denom, out=np.zeros_like(tp), where=denom > 0)
        present = true_n > 0
        out[s] = (f1 * present).sum(1) / present.sum(1)
    return out


def chunk_job(y, preds, W):
    return boot_f1(y, preds, W)


def main(cfg_path, name):
    study = Study(cfg_path, name)
    y = study.yev.astype(int)
    strat_rows = pd.read_csv(study.dir / "strategy_scenarios.csv")             # may be a subset of the scenarios
    sids = strat_rows["sid"].to_numpy()
    scen = pd.read_csv(study.dir / "scenarios.csv").set_index("sid").loc[sids].reset_index()
    base_all = np.load(study.dir / "baseline_preds.npz")
    base = {m: base_all[m][sids] for m in base_all.files}
    strat = np.load(study.dir / "strategy_preds.npz")
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(y), (B, len(y)))
    W = np.stack([np.bincount(i, minlength=len(y)) for i in idx]).astype(np.float32)

    methods = {m: strat[m] for m in STRATEGIES + EXTRA}
    methods.update({m: base[m] for m in ("svm", "lgbm")})
    for kind in ("svm", "lgbm"):
        for s in AUG_SEEDS:
            methods[f"{kind}_aug{s}"] = base[f"{kind}_aug{s}"]
    names = list(methods)
    S = len(scen)
    step = 60
    jobs = [(m, a, min(a + step, S)) for m in names for a in range(0, S, step)]
    res = Parallel(n_jobs=6, verbose=2)(delayed(chunk_job)(y, methods[m][a:b], W) for m, a, b in jobs)
    boot = {m: np.concatenate([r for (mm, _, _), r in zip(jobs, res) if mm == m]) for m in names}          # (S, B)
    for kind in ("svm", "lgbm"):                                            # average of the 5 augmentation seeds
        boot[f"{kind}_aug"] = np.mean([boot[f"{kind}_aug{s}"] for s in AUG_SEEDS], axis=0)

    # point estimates per scenario (exact, no resampling)
    sc_rows = strat_rows.merge(pd.read_csv(study.dir / "baseline_scenarios.csv"), on="sid", suffixes=("", "_b"))
    for kind in ("svm", "lgbm"):
        sc_rows[f"{kind}_aug_f1"] = sc_rows[[f"{kind}_aug{s}_f1" for s in AUG_SEEDS]].mean(axis=1)
    cells = scen.groupby(["kset", "fault", "level"]).indices
    table, vs = [], []
    for (kset, fault, level), ix in cells.items():
        row = {"kset": kset, "fault": fault, "level": level, "n_scenarios": len(ix)}
        sub = sc_rows.iloc[ix]
        for m in STRATEGIES + EXTRA + ["svm", "svm_aug", "lgbm_aug", "lgbm"]:
            col = f"{m}_f1"
            per_seed = sub.groupby("seed")[col].mean()
            row[f"{m}"], row[f"{m}_std_over_seeds"] = float(sub[col].mean()), float(per_seed.std())
        best = "svm_aug" if row["svm_aug"] >= row["lgbm_aug"] else "lgbm_aug"
        row["best_aug_baseline"] = best
        table.append(row)
        base_b = boot[best][ix].mean(0)
        for m in STRATEGIES + EXTRA:
            d = boot[m][ix].mean(0) - base_b
            lo, hi = np.percentile(d, [2.5, 97.5])
            vs.append({"kset": kset, "fault": fault, "level": level, "method": m, "counts_for_G3": m in STRATEGIES,
                       "best_aug_baseline": best, "method_f1": row[m], "best_aug_f1": row[best], "diff": row[m] - row[best],
                       "ci_low": float(lo), "ci_high": float(hi), "boot_mean_diff": float(d.mean()),
                       "z": float(d.mean() / d.std()) if d.std() > 0 else np.nan, "beats_and_ci_excludes_0": bool(lo > 0)})
    pd.DataFrame(table).round(4).to_csv(study.dir / "strategy_comparison.csv", index=False)
    v = pd.DataFrame(vs)
    v.round(4).to_csv(study.dir / "strategy_vs_best_aug.csv", index=False)

    g3 = v[v.counts_for_G3]
    passing = g3[g3.beats_and_ci_excludes_0]
    m_total = len(g3)
    bonf_z = norm.ppf(1 - 0.05 / (2 * m_total))
    verdict = {"scenarios_analysed": int(S), "scenarios_total_in_set": int(len(pd.read_csv(study.dir / "scenarios.csv"))),
               "G3_passes": len(passing) > 0, "comparisons": m_total, "cells_passing": int(len(passing)),
               "passing": passing[["kset", "fault", "level", "method", "diff", "ci_low", "ci_high"]].round(4).to_dict("records"),
               "bonferroni_supplement": {"z_threshold": float(bonf_z),
                                         "passing_after_bonferroni": int((g3[g3.beats_and_ci_excludes_0]["z"] > bonf_z).sum()),
                                         "note": "normal approximation of the bootstrap distribution; does not change the gate"},
               "rule": "results/decisions_log.md B11; real detector only, oracle excluded"}
    json.dump(verdict, open(study.dir / "g3_verdict.json", "w"), indent=1)
    pd.set_option("display.width", 220)
    print(json.dumps({k: v_ for k, v_ in verdict.items() if k != "passing"}, indent=1))
    print(passing.round(4).head(30).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    ap.add_argument("--name", default="temporal")
    a = ap.parse_args()
    main(a.config, a.name)
