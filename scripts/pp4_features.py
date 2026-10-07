"""Preprocessing phase 4 (short): sensor-local engineered features.

Usage: python scripts/pp4_features.py --config configs/preprocessing.yaml
Needs decisions.json (phase 3b). Outputs: results/preprocessing/phase4/

Gate P4 (structural): a group is rejected if any of its columns depends on more than one sensor, because a fault in
one sensor would then change the features of every sensor and the per-sensor reliability score could not tell
which sensor is at fault. pn_l2 and pn_logmed are evaluated for information only and are never eligible.
"""
import argparse
from pathlib import Path

import pandas as pd

from src.evaluate import choose, evaluate_spec, load_decisions, load_split, log_trial, save_decisions
from src.preprocessing import FeatureBuilder
from src.splits import load_config

# Rationale and references. Only sources that were checked are cited; the exact ratios are our construction.
CATALOGUE = {
    "trans_ratio": {
        "formula": "log1p|EMA_k| - log1p(||DR||), k in {EMAi, EMAd} x alpha {0.001, 0.01, 0.1}  (6 per sensor)",
        "rationale": "Transient (EMA) amplitude relative to the steady-state amplitude of the same sensor: a "
                     "response-shape descriptor that cancels the common concentration scale to first order. "
                     "Built from one sensor only.",
        "references": "EMA feature definition: Fonollosa, Rodriguez-Lujan, Huerta, Data in Brief 2015 (PMC4510048). "
                      "Transient features carry gas identity: Muezzinoglu et al., Sens. Actuators B 137(2):507-512, 2009 "
                      "(title and venue verified, text not read). Normalisation by a reference response: Yan et al., "
                      "Sensors 15(11):27804, 2015 (doi 10.3390/s151127804). The exact ratio is our construction."},
    "ema_shape": {
        "formula": "log1p|EMA(0.1)| - log1p|EMA(0.001)| for the rising and the decaying part  (2 per sensor)",
        "rationale": "alpha sets the time scale of the EMA: 0.1 follows the fast part of the response, 0.001 the slow part. "
                     "Their ratio describes the response kinetics (adsorption/desorption speed) independently of "
                     "amplitude. Built from one sensor only.",
        "references": "EMA definition: Fonollosa et al. 2015 (Data in Brief). Use of transient features: Muezzinoglu "
                      "et al. 2009 (as above). The exact ratio is our construction; no reference proposes it."},
}


def main(cfg_path):
    cfg = load_config(cfg_path)
    p4 = cfg["phase4"]
    out = Path("results/preprocessing/phase4")
    out.mkdir(parents=True, exist_ok=True)
    dec = load_decisions()
    base = dec["incumbent_spec"]
    tr, va = load_split(cfg)

    pd.DataFrame([{"group": g, **c} for g, c in CATALOGUE.items()]).to_csv(out / "feature_catalogue.csv", index=False)

    inc_metrics = evaluate_spec(base, tr, va, cfg)
    log_trial("phase4", "P4-incumbent", base, inc_metrics)
    inc = {"trial_id": "incumbent", "spec": base, **inc_metrics}
    print(f"incumbent  SVM {inc_metrics['svm_macro_f1']:.4f}  LGBM {inc_metrics['lgbm_macro_f1']:.4f}")

    rows, eligible = [], []
    for groups, is_eligible in [(g, True) for g in p4["candidates"]] + [(g, False) for g in p4["rejected_by_p4_logged_only"]]:
        prov = FeatureBuilder(False, tuple(groups)).provenance()
        new = prov[prov["group"].isin(groups)]
        max_sources = int(new["sources"].map(len).max())
        passes_p4 = max_sources == 1
        assert passes_p4 == is_eligible, (groups, max_sources)
        spec = {**base, "groups": list(groups)}
        m = evaluate_spec(spec, tr, va, cfg)
        name = "+".join(groups)
        log_trial("phase4", f"P4-{name}", spec, m, note="eligible" if passes_p4 else "rejected_by_P4_info_only")
        rows.append({"groups": name, "new_columns": len(new), "max_source_sensors": max_sources,
                     "passes_P4": passes_p4, **m})
        print(f"{name:26s} cols +{len(new):3d} sources<= {max_sources:2d} P4 {'ok' if passes_p4 else 'REJECTED'}  "
              f"SVM {m['svm_macro_f1']:.4f}  LGBM {m['lgbm_macro_f1']:.4f}")
        if passes_p4:
            eligible.append({"trial_id": name, "spec": spec, **m})
    table = pd.DataFrame(rows)
    table.round(4).to_csv(out / "candidates_val.csv", index=False)

    winner, flag = choose(inc, eligible, cfg["decision_rule"])
    print("phase 4 winner:", winner["trial_id"], "| LightGBM drop flag:", flag)
    dec["incumbent_spec"] = winner["spec"]
    dec["history"].append({"phase": "phase4", "winner": winner["trial_id"], "lgbm_flag": bool(flag)})
    save_decisions(dec)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
