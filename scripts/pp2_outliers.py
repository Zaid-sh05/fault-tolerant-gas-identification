"""Preprocessing phase 2: IQR outliers.

Usage: python scripts/pp2_outliers.py --config configs/preprocessing.yaml
Outputs: results/preprocessing/phase2/

1. Tukey fences [Q1 - k*IQR, Q3 + k*IQR] per feature, fitted on Train (batches 1-6).
2. Where do the outliers live? rate per feature x batch / gas, Cramer's V of the outlier flag against
   batch and against gas (also conditioned on the other factor, because gas mix and batch are
   confounded in this dataset), and a row-level dispersion index (do outliers come in bursts?).
3. Three options on Validation: keep_all, winsorize (clip to Train fences), drop_train_rows
   (never touches Validation).
4. Mandatory check: does clipping hide a Bias fault? Quick single-sensor Bias scenarios, scored with
   a Ridge-residual detector with and without clipping.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import chi2_contingency
from sklearn.metrics import roc_auc_score

from src.data import FEATURES, FEATURE_KINDS, N_SENSORS, sensor_columns, xy
from src.evaluate import choose, evaluate_spec, load_split, log_trial, save_decisions
from src.faults import Scenario, apply_fault
from src.imputation import BlockImputer
from src.preprocessing import IQRClipper

BASELINE = {"clip": "none", "slog": False, "scaler": "standard", "groups": [], "select": "none"}


def cramers_v(flag, factor):
    """Cramer's V between a boolean flag and a categorical factor (0 if the table is degenerate)."""
    table = pd.crosstab(factor, flag)
    if table.shape[0] < 2 or table.shape[1] < 2:
        return 0.0
    chi2 = chi2_contingency(table, correction=False)[0]
    return float(np.sqrt(chi2 / (table.values.sum() * (min(table.shape) - 1))))


def conditional_v(flag, factor, stratum, min_n=30):
    """Weighted mean of V(flag, factor) inside each stratum (e.g. batch effect within each gas)."""
    vs, ws = [], []
    for s in np.unique(stratum):
        m = stratum == s
        if m.sum() >= min_n and len(np.unique(factor[m])) > 1:
            vs.append(cramers_v(flag[m], factor[m]))
            ws.append(m.sum())
    return float(np.average(vs, weights=ws)) if vs else 0.0


def analyse_outliers(clip, tr, va, out):
    df = pd.concat([tr, va], ignore_index=True)
    flags = clip.outside(df[FEATURES].to_numpy())
    batch, gas = df["batch"].to_numpy(), df["gas"].to_numpy()
    fl = pd.DataFrame(flags, columns=FEATURES)

    fl.groupby(batch).mean().T.round(4).to_csv(out / "outlier_rate_feature_by_batch.csv")
    fl.groupby(gas).mean().T.round(4).to_csv(out / "outlier_rate_feature_by_gas.csv")
    sensor_rate = pd.DataFrame({f"S{s + 1:02d}": fl.iloc[:, sensor_columns(s)].mean(axis=1).groupby(batch).mean()
                                for s in range(N_SENSORS)}).T
    sensor_rate.round(4).to_csv(out / "outlier_rate_sensor_by_batch.csv")

    rows = []
    for j, f in enumerate(FEATURES):
        fj = flags[:, j]
        rows.append({"feature": f, "kind": FEATURE_KINDS[j % 8], "rate_train": fj[batch <= 6].mean(),
                     "rate_val": fj[batch == 7].mean(),
                     "v_batch": cramers_v(fj, batch), "v_gas": cramers_v(fj, gas),
                     "v_batch_given_gas": conditional_v(fj, batch, gas),
                     "v_gas_given_batch": conditional_v(fj, gas, batch)})
    feat = pd.DataFrame(rows)

    def label(r):                                    # Cohen (1988): V >= 0.1 is at least a small effect
        if r.rate_train + r.rate_val == 0:
            return "no_outliers"
        b, g = r.v_batch_given_gas, r.v_gas_given_batch
        if max(b, g) < 0.1:
            return "diffuse"
        return "batch_drift" if b >= g else "gas_related"

    feat["pattern"] = feat.apply(label, axis=1)
    feat.round(4).to_csv(out / "outlier_features.csv", index=False)

    count = flags.sum(1)                              # row level
    p = flags.mean(0)
    expected_var = float((p * (1 - p)).sum())
    row_stats = {
        "mean_share_train": float(flags[batch <= 6].mean()), "mean_share_val": float(flags[batch == 7].mean()),
        "share_gt_10pct_train": float((flags[batch <= 6].mean(1) > 0.10).mean()),
        "share_gt_10pct_val": float((flags[batch == 7].mean(1) > 0.10).mean()),
        "dispersion_index_train": float(count[batch <= 6].var() / expected_var),
        "dispersion_index_val": float(count[batch == 7].var() / expected_var),
        "pattern_counts": feat["pattern"].value_counts().to_dict(),
        "pattern_by_kind": feat.groupby("kind")["pattern"].agg(lambda s: s.value_counts().to_dict()).to_dict(),
    }
    json.dump(row_stats, open(out / "outlier_summary.json", "w"), indent=1)
    return feat, row_stats


def bias_hiding_check(clip, Xtr, train_batches, Xva, cfg, out):
    """AUROC of a Ridge-residual score separating a Bias-faulted sensor block from the clean block,
    with and without clipping. Also reports how much of the injected shift survives the clip."""
    p1, p2 = cfg["phase1"], cfg["phase2"]
    std_train = np.nanstd(Xtr, axis=0)
    folds = [tuple(f) for f in cfg["split"]["inner_folds"]]
    ctx = {}
    for cond in ("raw", "clipped"):
        f = (lambda X: clip.transform(X)) if cond == "clipped" else (lambda X: X)
        Xt = f(Xtr)
        imp = BlockImputer("ridge", "slog", ridge_alphas=p1["ridge_alphas"], seed=cfg["seed"]).fit(
            Xt, train_batches)
        ctx[cond] = (f, imp, Xt.mean(0), Xt.std(0))
    rows = []
    for delta in p2["bias_deltas"]:
        for seed in p2["bias_seeds"]:
            for s in range(N_SENSORS):
                Xf = apply_fault(Xva, Scenario("k1", (s,), "bias", delta, seed), std_train)
                cols = sensor_columns(s)
                for twin in (False, True):
                    rec = {"delta": delta, "seed": seed, "sensor": f"S{s + 1:02d}", "exclude_twin": twin}
                    for cond, (f, imp, mu, sd) in ctx.items():
                        scores = []
                        for X in (Xva, Xf):
                            Xc = f(X)
                            resid = np.abs(imp.reconstruct(Xc, s, twin, folds)[:, cols] - Xc[:, cols]) / sd[cols]
                            scores.append(resid.mean(1))
                        y = np.r_[np.zeros(len(Xva)), np.ones(len(Xva))]
                        rec[f"auroc_{cond}"] = roc_auc_score(y, np.r_[scores[0], scores[1]])
                    shift_raw = np.abs(Xf[:, cols] - Xva[:, cols]).mean()
                    shift_clip = np.abs(clip.transform(Xf)[:, cols] - clip.transform(Xva)[:, cols]).mean()
                    rec["shift_retained"] = shift_clip / shift_raw
                    rows.append(rec)
    res = pd.DataFrame(rows)
    res.to_csv(out / "bias_hiding_check.csv", index=False)
    summ = (res.groupby(["delta", "exclude_twin"])[["auroc_raw", "auroc_clipped", "shift_retained"]]
            .mean().round(4).reset_index())
    summ["auroc_drop"] = (summ["auroc_raw"] - summ["auroc_clipped"]).round(4)
    summ.to_csv(out / "bias_hiding_summary.csv", index=False)
    return summ


def main(cfg_path):
    cfg = yaml.safe_load(open(cfg_path))
    p2 = cfg["phase2"]
    out = Path("results/preprocessing/phase2")
    out.mkdir(parents=True, exist_ok=True)
    tr, va = load_split(cfg)
    Xtr, _ = xy(tr)
    Xva, _ = xy(va)
    clip = IQRClipper(p2["iqr_k"]).fit(Xtr)

    feat, row_stats = analyse_outliers(clip, tr, va, out)
    print("outlier rates: train %.3f  val %.3f | rows with >10%% outlying features: train %.3f val %.3f"
          % (row_stats["mean_share_train"], row_stats["mean_share_val"],
             row_stats["share_gt_10pct_train"], row_stats["share_gt_10pct_val"]))
    print("dispersion index (1 = independent):", round(row_stats["dispersion_index_train"], 1),
          round(row_stats["dispersion_index_val"], 1))
    print("feature patterns:", row_stats["pattern_counts"])

    # ---- options on Validation -------------------------------------------------------
    results = {}
    results["keep_all"] = evaluate_spec(BASELINE, tr, va, cfg)
    results["winsorize"] = evaluate_spec({**BASELINE, "clip": "iqr"}, tr, va, cfg)
    drop = clip.outside(Xtr).mean(1) > p2["drop_row_share"]
    removed = tr.loc[drop].groupby(["batch", "gas"]).size().rename("removed").reset_index()
    removed.to_csv(out / "dropped_train_rows.csv", index=False)
    results["drop_train_rows"] = evaluate_spec(BASELINE, tr[~drop].reset_index(drop=True), va, cfg)
    results["drop_train_rows"]["rows_removed"] = int(drop.sum())
    print(f"drop_train_rows removes {int(drop.sum())} of {len(tr)} Train rows")

    specs = {"keep_all": BASELINE, "winsorize": {**BASELINE, "clip": "iqr"}, "drop_train_rows": BASELINE}
    for name, m in results.items():
        log_trial("phase2", f"P2-{name}", specs[name], {k: v for k, v in m.items() if k != "rows_removed"},
                  note=f"rows_removed={m.get('rows_removed', 0)}")
    table = pd.DataFrame(results).T
    table.round(4).to_csv(out / "outlier_options_val.csv")
    print(table.round(4).to_string())

    inc = {"trial_id": "keep_all", "spec": BASELINE, **results["keep_all"]}
    cands = [{"trial_id": n, "spec": specs[n], **results[n]} for n in ("keep_all", "winsorize", "drop_train_rows")]
    winner, flag = choose(inc, cands, cfg["decision_rule"])
    print("phase 2 winner:", winner["trial_id"], "| LightGBM drop flag:", flag)

    # ---- does clipping hide a Bias fault? ------------------------------------------------
    summ = bias_hiding_check(clip, Xtr, tr["batch"].to_numpy(), Xva, cfg, out)
    print(summ.to_string(index=False))

    save_decisions({"incumbent_spec": winner["spec"], "drop_train_rows": winner["trial_id"] == "drop_train_rows",
                    "history": [{"phase": "phase2", "winner": winner["trial_id"], "lgbm_flag": bool(flag)}]})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
