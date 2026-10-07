"""Preprocessing phase 3: scaler x signed-log, on the incumbent pipeline (cleaned data).

Usage: python scripts/pp3_scaling.py --config configs/preprocessing.yaml
Needs results/preprocessing/decisions.json from phase 2. Outputs: results/preprocessing/phase3/

Six combinations (StandardScaler/RobustScaler/MinMaxScaler, with and without sign(x)*log(1+|x|)) with the
fixed model settings. The winner (pre-registered rule) becomes the NEW BASELINE: its SVM and LightGBM are then
tuned on the old grids, and that SVM Macro-F1 is the reference of gate P3.
LightGBM is shown for completeness: trees only use the order of values, so scaling should not matter.
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from src.evaluate import choose, evaluate_spec, load_decisions, load_split, log_trial, save_decisions, tune
from src.splits import load_config


def main(cfg_path):
    cfg = load_config(cfg_path)
    p3 = cfg["phase3"]
    out = Path("results/preprocessing/phase3")
    out.mkdir(parents=True, exist_ok=True)
    dec = load_decisions()
    incumbent_spec = dec["incumbent_spec"]
    tr, va = load_split(cfg)

    results, specs = {}, {}
    for scaler in p3["scalers"]:
        for slog in p3["slog"]:
            name = f"{scaler}{'+slog' if slog else ''}"
            specs[name] = {**incumbent_spec, "scaler": scaler, "slog": slog}
            results[name] = evaluate_spec(specs[name], tr, va, cfg)
            log_trial("phase3", f"P3-{name}", specs[name], results[name])
            print(f"{name:16s} SVM {results[name]['svm_macro_f1']:.4f}  LGBM {results[name]['lgbm_macro_f1']:.4f}")
    table = pd.DataFrame(results).T
    table.round(4).to_csv(out / "scaling_options_val.csv")

    inc_name = f"{incumbent_spec['scaler']}{'+slog' if incumbent_spec['slog'] else ''}"
    inc = {"trial_id": inc_name, "spec": specs[inc_name], **results[inc_name]}
    cands = [{"trial_id": n, "spec": specs[n], **r} for n, r in results.items()]
    winner, flag = choose(inc, cands, cfg["decision_rule"])
    print("phase 3 winner:", winner["trial_id"], "| LightGBM drop flag:", flag)

    grid = tune(winner["spec"], tr, va, cfg)
    grid.round(4).to_csv(out / "new_baseline_grid_val.csv", index=False)
    best = {m: grid[grid.model == m].sort_values("macro_f1", ascending=False).iloc[0] for m in ("svm", "lgbm")}
    new_baseline = {"spec": winner["spec"], "trial_id": winner["trial_id"],
                    "svm_fixed_params_macro_f1": winner["svm_macro_f1"],
                    "svm_tuned": {"params": best["svm"]["params"], "macro_f1": float(best["svm"]["macro_f1"]),
                                  "accuracy": float(best["svm"]["accuracy"])},
                    "lgbm_tuned": {"params": best["lgbm"]["params"], "macro_f1": float(best["lgbm"]["macro_f1"]),
                                   "accuracy": float(best["lgbm"]["accuracy"])}}
    json.dump(new_baseline, open(out / "new_baseline.json", "w"), indent=1)
    print("NEW BASELINE:", json.dumps(new_baseline, indent=1))

    dec["incumbent_spec"] = winner["spec"]
    dec["new_baseline"] = new_baseline
    dec["history"].append({"phase": "phase3", "winner": winner["trial_id"], "lgbm_flag": bool(flag)})
    save_decisions(dec)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
