"""Part-1 decision rule (registered in results/decisions_log.md, B2) for the Phase 4 and Phase 5 candidates.

Usage: python scripts/pp45_decision_rule.py --config configs/preprocessing.yaml
A candidate is adopted only if (i) its SVM Macro-F1 beats the clean Baseline (StandardScaler, tuned SVM) by more than
0.005 AND (ii) the paired-bootstrap (1000) 95% interval of the difference excludes 0. Otherwise the Baseline is kept.
Everything is fitted on Train (batches 1-6); the choice is made on Validation (batch 7). LightGBM is shown for information.
Outputs: results/preprocessing/phase45/
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from src.data import xy
from src.evaluate import bootstrap_diff, fit_predict, load_decisions, load_split, log_trial, save_decisions
from src.models import scores
from src.splits import load_config


def main(cfg_path):
    cfg = load_config(cfg_path)
    out = Path("results/preprocessing/phase45")
    out.mkdir(parents=True, exist_ok=True)
    dec = load_decisions()
    nb = dec["new_baseline"]
    assert nb["trial_id"] == "standard", "the rule is written for the StandardScaler baseline"
    base_spec = nb["spec"]
    svm_p = {**cfg["models"]["svm"], **json.loads(nb["svm_tuned"]["params"])}
    lgbm_p = {**cfg["models"]["lgbm"], **json.loads(nb["lgbm_tuned"]["params"])}
    tr, va = load_split(cfg)
    yva = xy(va)[1]
    min_gain, b = cfg["decision_rule"]["min_gain"], {"n": 1000, "seed": 0, "ci": 0.95}

    cands = {"baseline": base_spec}
    for groups in cfg["phase4"]["candidates"]:
        cands["+".join(groups)] = {**base_spec, "groups": list(groups)}
    for c in cfg["phase5"]["candidates"]:
        if c["name"] != "none":
            cands[c["name"]] = {**base_spec, "select": {"drop_frac": c["drop_frac"],
                                                           "min_own": cfg["phase5"]["min_own_features_per_sensor"]}}
    preds, rows = {}, []
    for name, spec in cands.items():
        preds[name] = fit_predict(spec, tr, va, cfg, models=("svm", "lgbm"), svm_params=svm_p, lgbm_params=lgbm_p)
        m = {f"{k}_{s}": scores(yva, preds[name][k])[s] for k in ("svm", "lgbm") for s in ("macro_f1", "accuracy")}
        log_trial("part1_rule", f"R-{name}", spec, {**m, "n_features": -1}, note="tuned baseline settings")
        rows.append({"candidate": name, **m})
    table = pd.DataFrame(rows).set_index("candidate")

    verdicts = []
    for name in cands:
        if name == "baseline":
            continue
        mean, lo, hi, p_pos = bootstrap_diff(yva, preds[name]["svm"], preds["baseline"]["svm"], **b)
        gain = float(table.loc[name, "svm_macro_f1"] - table.loc["baseline", "svm_macro_f1"])
        verdicts.append({"candidate": name, "svm_macro_f1": table.loc[name, "svm_macro_f1"], "gain_vs_baseline": gain,
                         "ci_low": lo, "ci_high": hi, "gain_gt_0.005": gain > min_gain, "ci_excludes_0": lo > 0 or hi < 0,
                         "adopt": bool(gain > min_gain and lo > 0),
                         "lgbm_macro_f1": table.loc[name, "lgbm_macro_f1"],
                         "lgbm_gain_vs_baseline": table.loc[name, "lgbm_macro_f1"] - table.loc["baseline", "lgbm_macro_f1"]})
    v = pd.DataFrame(verdicts)
    table.round(4).to_csv(out / "candidates_tuned_val.csv")
    v.round(4).to_csv(out / "decision_rule.csv", index=False)
    pd.set_option("display.width", 220)
    print(table.round(4).to_string())
    print(v.round(4).to_string(index=False))

    adopted = v[v["adopt"]]
    final = cands[adopted.sort_values("gain_vs_baseline").iloc[-1]["candidate"]] if len(adopted) else base_spec
    dec["final_pipeline"] = {"spec": final, "svm_params": svm_p, "lgbm_params": lgbm_p,
                             "adopted_candidate": adopted["candidate"].tolist(),
                             "baseline_svm_macro_f1": float(table.loc["baseline", "svm_macro_f1"])}
    dec["history"].append({"phase": "part1_rule", "adopted": adopted["candidate"].tolist()})
    save_decisions(dec)
    json.dump(dec["final_pipeline"], open(out / "final_pipeline.json", "w"), indent=1)
    print("FINAL PIPELINE:", "baseline (no candidate adopted)" if not len(adopted) else adopted["candidate"].tolist())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
