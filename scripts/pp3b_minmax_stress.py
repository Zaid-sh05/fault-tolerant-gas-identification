"""Phase 3b: stress check of the Phase-3 winner (MinMax) before adopting it.

Usage: python scripts/pp3b_minmax_stress.py --config configs/preprocessing.yaml
Outputs: results/preprocessing/phase3/stress_*.csv, stress_check.json (and an updated decisions.json)

The adoption rule is registered in configs/preprocessing.yaml (phase3_stress) before this script is run:
adopt MinMax only if (A) the bootstrap interval of MinMax - Standard excludes 0 AND (B) MinMax with 1-99
percentile bounds still beats Standard by more than min_gain; otherwise StandardScaler.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.data import FEATURES, xy
from src.evaluate import bootstrap_diff, fit_predict, load_decisions, load_split, log_trial, save_decisions, tune
from src.models import scores
from src.splits import load_config


def feature_squeeze_table(Xtr, lo, hi):
    p_lo, p_hi = np.percentile(Xtr, [lo, hi], axis=0)
    rng = Xtr.max(0) - Xtr.min(0)
    return pd.DataFrame({"feature": FEATURES, "p_range": p_hi - p_lo, "minmax_range": rng,
                         "ratio": np.divide(p_hi - p_lo, rng, out=np.ones(len(rng)), where=rng > 0)})


def main(cfg_path):
    cfg = load_config(cfg_path)
    st = cfg["phase3_stress"]
    min_gain = cfg["decision_rule"]["min_gain"]
    out = Path("results/preprocessing/phase3")
    dec = load_decisions()
    base_spec = dec["incumbent_spec"]                                  # the Phase-3 winner (MinMax)
    tr, va = load_split(cfg)
    Xtr, _ = xy(tr)
    yva = xy(va)[1]

    # 1. how much does full MinMax squeeze each feature?
    sq = feature_squeeze_table(Xtr, *st["percentiles"])
    sq.round(5).to_csv(out / "stress_feature_ratio.csv", index=False)
    flagged = sq[sq["ratio"] < st["ratio_flag"]]
    print(f"features with (p{st['percentiles'][0]}-p{st['percentiles'][1]} range)/(min-max range) < {st['ratio_flag']}: "
          f"{len(flagged)} of 128")
    print(flagged.round(4).to_string(index=False))

    # 2. standard vs minmax vs minmax with percentile bounds
    specs = {"standard": {**base_spec, "scaler": "standard"}, "minmax": {**base_spec, "scaler": "minmax"},
             "minmax_p1_99": {**base_spec, "scaler": "minmax_p1_99"}}
    preds, rows = {}, []
    for name, spec in specs.items():
        preds[name] = fit_predict(spec, tr, va, cfg, models=("svm", "lgbm"))
        m = {f"{k}_{s}": scores(yva, preds[name][k])[s] for k in ("svm", "lgbm") for s in ("macro_f1", "accuracy")}
        rows.append({"scaler": name, **m})
        log_trial("phase3b", f"P3b-{name}", spec, {**m, "n_features": 128})
    table = pd.DataFrame(rows).set_index("scaler")
    table.round(4).to_csv(out / "stress_scalers_val.csv")
    print(table.round(4).to_string())

    # 3. paired bootstrap on the SVM
    b = st["bootstrap"]
    boot = []
    for a_, b_ in (("minmax", "standard"), ("minmax_p1_99", "standard"), ("minmax", "minmax_p1_99")):
        mean, lo, hi, p_pos = bootstrap_diff(yva, preds[a_]["svm"], preds[b_]["svm"], b["n"], b["seed"], b["ci"])
        boot.append({"difference": f"{a_} - {b_}", "mean": mean, "ci_low": lo, "ci_high": hi, "share_positive": p_pos})
    boot = pd.DataFrame(boot)
    boot.round(4).to_csv(out / "stress_bootstrap.csv", index=False)
    print(boot.round(4).to_string(index=False))

    # 4. pre-registered rule
    f1 = table["svm_macro_f1"]
    cond_a = bool(boot.loc[0, "ci_low"] > 0)
    cond_b = bool(f1["minmax_p1_99"] - f1["standard"] > min_gain)
    if cond_a and cond_b:
        adopted = "minmax_p1_99" if f1["minmax_p1_99"] - f1["minmax"] > min_gain else "minmax"
    else:
        adopted = "standard"
    verdict = {"features_squeezed_below_flag": flagged["feature"].tolist(), "condition_A_ci_excludes_zero": cond_a,
               "condition_B_percentile_minmax_gain_over_standard": float(f1["minmax_p1_99"] - f1["standard"]),
               "condition_B_met": cond_b, "adopted_scaler": adopted}
    json.dump(verdict, open(out / "stress_check.json", "w"), indent=1)
    print("VERDICT:", json.dumps(verdict, indent=1))

    # 5. the adopted scaler becomes the new baseline (tuned on the old grids, like the old baselines)
    spec = specs[adopted]
    grid = tune(spec, tr, va, cfg)
    grid.round(4).to_csv(out / "new_baseline_grid_val.csv", index=False)
    best = {m: grid[grid.model == m].sort_values("macro_f1", ascending=False).iloc[0] for m in ("svm", "lgbm")}
    dec["incumbent_spec"] = spec
    dec["new_baseline"] = {"spec": spec, "trial_id": adopted, "svm_fixed_params_macro_f1": float(f1[adopted]),
                           "svm_tuned": {"params": best["svm"]["params"], "macro_f1": float(best["svm"]["macro_f1"]),
                                         "accuracy": float(best["svm"]["accuracy"])},
                           "lgbm_tuned": {"params": best["lgbm"]["params"], "macro_f1": float(best["lgbm"]["macro_f1"]),
                                          "accuracy": float(best["lgbm"]["accuracy"])}}
    dec["history"].append({"phase": "phase3b_stress", "winner": adopted})
    json.dump(dec["new_baseline"], open(out / "new_baseline.json", "w"), indent=1)
    save_decisions(dec)
    print("NEW BASELINE:", json.dumps(dec["new_baseline"], indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
