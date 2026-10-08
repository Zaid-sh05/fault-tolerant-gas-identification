"""Final test: tables per evaluation batch and pooled (baselines, strategies, gates G1 and G3), from saved predictions.

Usage: python scripts/ft_analysis.py --config configs/final_test.yaml --name test
Needs ov2_faults_g1.py and ov4_strategies.py to have finished (baseline_preds.npz, strategy_preds.npz).
Outputs in <output_root>/<name>/: ft_clean_by_subset.csv, ft_comparison.csv, ft_vs_best_aug.csv, ft_g1_summary.csv,
ft_verdicts.json. Subsets: "pooled" and one per evaluation batch ("b8", "b9", "b10"); each uses only its own rows, for the
point estimates and for the paired bootstrap (1000 resamples, seed 0, same design as ov4_analysis.py: the interval reflects
row sampling only). The pooled subset is cross-checked against ov4_analysis.py's files and the script stops on a mismatch.
Rules are those of results/decisions_log.md (B4 for G1, B11 for G3); nothing is re-tuned on the test rows.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from scipy.stats import norm  # noqa: E402

sys.path.insert(0, "scripts")
from ov4_analysis import B, BASELINES, EXTRA, STRATEGIES, boot_f1  # noqa: E402,F401
from ov4_strategies import make_kit  # noqa: E402
from src.models import scores  # noqa: E402
from src.scenarios import MEDIUM  # noqa: E402
from src.strategies import acted_sets  # noqa: E402
from src.study import AUG_SEEDS, Study  # noqa: E402

CELL = ["kset", "fault", "level"]
STEP = 60


def point_f1(y, preds):
    """Exact Macro-F1 (present classes) of every row of preds (S, n)."""
    return boot_f1(y, preds, np.ones((1, len(y)), dtype=np.float32))[:, 0]


def bootstrap(y, methods, W, jobs=6):
    S = len(next(iter(methods.values())))
    tasks = [(m, a, min(a + STEP, S)) for m in methods for a in range(0, S, STEP)]
    res = Parallel(n_jobs=jobs)(delayed(boot_f1)(y, methods[m][a:b], W) for m, a, b in tasks)
    return {m: np.concatenate([r for (mm, _, _), r in zip(tasks, res) if mm == m]) for m in methods}     # (S, B)


def clean_table(study, kit, det, subsets):
    """Clean (no fault) scores of every baseline and strategy, per subset."""
    X, y = study.Xev, study.yev
    preds = study.predict(study.models(), study.pre.transform(X))
    R = det.ratio(X)
    sets = acted_sets(R, R > 1.0)
    proba = kit.expert_proba(X)
    preds.update({"A_det_twin": kit.predict_A(X, sets, False), "A_det_notwin": kit.predict_A(X, sets, True),
                  "B_det": kit.predict_B(X, sets), "C_det": kit.combine(proba, R), "C_equal": kit.combine(proba, None)})
    n_flag = np.array([len(s) for s in sets])
    rows = []
    for name, sel in subsets.items():
        for m, p in preds.items():
            s = scores(y[sel], p[sel])
            acts = m.startswith(("A_", "B_", "C_"))
            rows.append({"subset": name, "method": m, "rows": int(sel.sum()), **s,
                         "mean_flagged_per_row": float(n_flag[sel].mean()) if acts else 0.0,
                         "rows_with_any_flag": float((n_flag[sel] > 0).mean()) if acts else 0.0})
    return pd.DataFrame(rows)


def analyse(name, sel, study, scen, base, strat, clean, jobs):
    y = study.yev.astype(int)[sel]
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(y), (B, len(y)))
    W = np.stack([np.bincount(i, minlength=len(y)) for i in idx]).astype(np.float32)
    methods = {m: strat[m][:, sel] for m in STRATEGIES + EXTRA}
    methods.update({m: base[m][:, sel] for m in ("svm", "lgbm")})
    for kind in ("svm", "lgbm"):
        methods.update({f"{kind}_aug{s}": base[f"{kind}_aug{s}"][:, sel] for s in AUG_SEEDS})
    boot = bootstrap(y, methods, W, jobs)
    for kind in ("svm", "lgbm"):
        boot[f"{kind}_aug"] = np.mean([boot[f"{kind}_aug{s}"] for s in AUG_SEEDS], axis=0)
    f1 = pd.DataFrame({m: point_f1(y, p) for m, p in methods.items()})                       # per scenario, exact
    for kind in ("svm", "lgbm"):
        f1[f"{kind}_aug"] = f1[[f"{kind}_aug{s}" for s in AUG_SEEDS]].mean(axis=1)
    f1 = pd.concat([scen[["sid", "seed"] + CELL], f1], axis=1)

    cells = f1.groupby(CELL).indices
    table, vs = [], []
    for (kset, fault, level), ix in cells.items():
        sub = f1.iloc[ix]
        row = {"subset": name, "kset": kset, "fault": fault, "level": level, "n_scenarios": len(ix)}
        for m in STRATEGIES + EXTRA + ["svm", "svm_aug", "lgbm_aug", "lgbm"]:
            row[m], row[f"{m}_std_over_seeds"] = float(sub[m].mean()), float(sub.groupby("seed")[m].mean().std())
        best = "svm_aug" if row["svm_aug"] >= row["lgbm_aug"] else "lgbm_aug"
        row["best_aug_baseline"] = best
        table.append(row)
        base_b = boot[best][ix].mean(0)
        for m in STRATEGIES + EXTRA:
            d = boot[m][ix].mean(0) - base_b
            lo, hi = np.percentile(d, [2.5, 97.5])
            vs.append({"subset": name, "kset": kset, "fault": fault, "level": level, "method": m,
                       "counts_for_G3": m in STRATEGIES, "best_aug_baseline": best, "method_f1": row[m],
                       "best_aug_f1": row[best], "diff": row[m] - row[best], "ci_low": float(lo), "ci_high": float(hi),
                       "z": float(d.mean() / d.std()) if d.std() > 0 else np.nan, "beats_and_ci_excludes_0": bool(lo > 0)})
    comp, vs = pd.DataFrame(table), pd.DataFrame(vs)

    # ---- G3 (real detector only) --------------------------------------------------------------
    g3 = vs[vs.counts_for_G3]
    passing = g3[g3.beats_and_ci_excludes_0]
    bonf_z = norm.ppf(1 - 0.05 / (2 * len(g3)))
    verdict = {"G3_passes": bool(len(passing) > 0), "comparisons": int(len(g3)), "cells_passing": int(len(passing)),
               "passing_after_bonferroni": int((passing["z"] > bonf_z).sum()),
               "note": "intervals resample rows only (optimistic); G3 needs a single passing comparison (lenient)"}

    # ---- G1 (decisions_log B4): best clean baseline of this subset, k=1, medium severity ----------------
    cl = clean[(clean.subset == name) & clean.method.isin(["svm", "lgbm"])].set_index("method")["macro_f1"]
    best_clean = cl.idxmax()
    f1["drop"] = cl[best_clean] - f1[best_clean]
    f1["svm_drop"] = cl["svm"] - f1["svm"]
    g = (f1.groupby(CELL).agg(n=("sid", "size"), best_clean_drop=("drop", "mean"), svm_drop=("svm_drop", "mean"),
                              svm_f1=("svm", "mean"), lgbm_f1=("lgbm", "mean"), svm_aug_f1=("svm_aug", "mean"),
                              lgbm_aug_f1=("lgbm_aug", "mean")).reset_index())
    g.insert(0, "subset", name)
    k1 = g[g.kset == "k1"]
    per_type = {f: float(k1[(k1.fault == f) & (k1.level == MEDIUM[f])]["best_clean_drop"].iloc[0]) for f in MEDIUM}
    counted = [f for f, d in per_type.items() if d >= 0.03]
    verdict["G1"] = {"best_clean_baseline": best_clean, "clean_macro_f1": float(cl[best_clean]),
                     "k1_medium_mean_drop_by_fault": per_type, "types_with_drop_ge_0.03": counted,
                     "G1_passes": len(counted) >= 2}
    return comp, vs, g, verdict


def cross_check(study, comp, vs, verdict):
    """The pooled subset must reproduce ov4_analysis.py (same rows, same resamples)."""
    ref = pd.read_csv(study.dir / "strategy_comparison.csv")
    mine = comp[comp.subset == "pooled"].merge(ref, on=CELL, suffixes=("", "_ref"))
    cols = [c for c in STRATEGIES + EXTRA + ["svm", "svm_aug", "lgbm_aug", "lgbm"]]
    err = max(float(np.abs(mine[c] - mine[f"{c}_ref"]).max()) for c in cols)
    ref_vs = pd.read_csv(study.dir / "strategy_vs_best_aug.csv")
    m2 = vs[vs.subset == "pooled"].merge(ref_vs, on=CELL + ["method"], suffixes=("", "_ref"))
    err_ci = float(max(np.abs(m2.ci_low - m2.ci_low_ref).max(), np.abs(m2.ci_high - m2.ci_high_ref).max()))
    g3_ref = json.load(open(study.dir / "g3_verdict.json"))
    assert err < 1e-4 and err_ci < 1e-4, f"pooled tables differ from ov4_analysis.py: f1 {err}, ci {err_ci}"
    assert g3_ref["cells_passing"] == verdict["pooled"]["cells_passing"], "G3 count differs from ov4_analysis.py"
    print(f"cross-check with ov4_analysis.py: max |f1 diff| {err:.2e}, max |ci diff| {err_ci:.2e}, same G3 count", flush=True)


def main(cfg_path, name, jobs=6):
    study = Study(cfg_path, name)
    scen = pd.read_csv(study.dir / "scenarios.csv")
    base, strat = np.load(study.dir / "baseline_preds.npz"), np.load(study.dir / "strategy_preds.npz")
    base, strat = {m: base[m] for m in base.files}, {m: strat[m] for m in strat.files}
    assert all(len(v) == len(scen) for v in list(base.values()) + list(strat.values())), "predictions miss scenarios"
    batch = study.proto.eval["batch"].to_numpy()
    subsets = {"pooled": np.ones(len(batch), dtype=bool), **{f"b{b}": batch == b for b in sorted(set(batch))}}
    kit, det = make_kit(study)
    clean = clean_table(study, kit, det, subsets)
    clean.round(4).to_csv(study.dir / "ft_clean_by_subset.csv", index=False)
    pd.set_option("display.width", 220)
    print(clean[clean.method.isin(["svm", "lgbm", "A_det_twin", "B_det"])].round(4).to_string(index=False), flush=True)

    comps, vss, gs, verdicts = [], [], [], {}
    for sname, sel in subsets.items():
        print(f"analysing {sname} ({int(sel.sum())} rows)", flush=True)
        comp, vs, g, v = analyse(sname, sel, study, scen, base, strat, clean, jobs)
        comps.append(comp), vss.append(vs), gs.append(g)
        verdicts[sname] = {"rows": int(sel.sum()), **v}
    comp, vs, g = pd.concat(comps), pd.concat(vss), pd.concat(gs)
    cross_check(study, comp, vs, verdicts)
    comp.round(4).to_csv(study.dir / "ft_comparison.csv", index=False)
    vs.round(4).to_csv(study.dir / "ft_vs_best_aug.csv", index=False)
    g.round(4).to_csv(study.dir / "ft_g1_summary.csv", index=False)
    json.dump(verdicts, open(study.dir / "ft_verdicts.json", "w"), indent=1)
    print(json.dumps({k: {"G1": v["G1"]["G1_passes"], "G3": v["G3_passes"], "G3_cells": f'{v["cells_passing"]}/{v["comparisons"]}'}
                      for k, v in verdicts.items()}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/final_test.yaml")
    ap.add_argument("--name", default="test")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    main(a.config, a.name, a.jobs)
