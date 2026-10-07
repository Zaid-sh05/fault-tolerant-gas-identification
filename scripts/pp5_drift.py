"""Preprocessing phase 5 (short): exclude the most drift-sensitive features.

Usage: python scripts/pp5_drift.py --config configs/preprocessing.yaml
Needs decisions.json (phase 4). Outputs: results/preprocessing/phase5/

Drift sensitivity of a feature = eta2: the share of its variance (after removing the gas effect) explained by the
batch, computed on Train batches 1-6 only. Options (pre-registered): exclude none, the top 10%, the top 20%.
No sensor is removed completely (at least min_own_features_per_sensor of its own columns stay).
"""
import argparse
from pathlib import Path

import pandas as pd

from src.data import xy
from src.evaluate import choose, evaluate_spec, load_decisions, load_split, log_trial, save_decisions
from src.preprocessing import fit_preprocessor, pipeline_provenance
from src.splits import load_config


def main(cfg_path):
    cfg = load_config(cfg_path)
    p5 = cfg["phase5"]
    out = Path("results/preprocessing/phase5")
    out.mkdir(parents=True, exist_ok=True)
    dec = load_decisions()
    base = dec["incumbent_spec"]
    tr, va = load_split(cfg)
    Xtr, ytr = xy(tr)

    results, specs = {}, {}
    for cand in p5["candidates"]:
        spec = base if cand["name"] == "none" else {**base, "select": {"drop_frac": cand["drop_frac"],
                                                                          "min_own": p5["min_own_features_per_sensor"]}}
        specs[cand["name"]] = spec
        results[cand["name"]] = evaluate_spec(spec, tr, va, cfg)
        log_trial("phase5", f"P5-{cand['name']}", spec, results[cand["name"]])
        r = results[cand["name"]]
        print(f"{cand['name']:12s} columns {int(r['n_features']):3d}  SVM {r['svm_macro_f1']:.4f}  LGBM {r['lgbm_macro_f1']:.4f}")
    table = pd.DataFrame(results).T
    table.round(4).to_csv(out / "drift_options_val.csv")

    # which features are the most drift-sensitive, and which sensors they belong to
    full = {**base, "select": {"drop_frac": 0.0, "min_own": 0}}
    pipe = fit_preprocessor(full, Xtr, ytr, tr["batch"].to_numpy())
    prov = pipeline_provenance(pipe)
    prov["eta2"] = pipe.named_steps["select"].eta2_
    prov = prov.sort_values("eta2", ascending=False)
    prov["rank"] = range(1, len(prov) + 1)
    prov.round(4).to_csv(out / "drift_sensitivity_train_1_6.csv", index=False)
    print("most drift-sensitive features (eta2 on batches 1-6):")
    print(prov.head(13)[["feature", "eta2"]].round(3).to_string(index=False))

    inc = {"trial_id": "none", "spec": specs["none"], **results["none"]}
    cands = [{"trial_id": n, "spec": specs[n], **results[n]} for n in results]
    winner, flag = choose(inc, cands, cfg["decision_rule"])
    print("phase 5 winner:", winner["trial_id"], "| LightGBM drop flag:", flag)
    dec["incumbent_spec"] = winner["spec"]
    dec["history"].append({"phase": "phase5", "winner": winner["trial_id"], "lgbm_flag": bool(flag)})
    save_decisions(dec)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
