"""New baselines on the final pipeline: SVM, LightGBM, and their fault-augmented versions with 5 seeds.

Usage: python scripts/pp6_baselines_aug.py --config configs/preprocessing.yaml
Needs decisions.json. Outputs: results/preprocessing/final/aug_baselines*.csv

* Preprocessing is fitted on the clean Train rows only. Fault augmentation (one corrupted copy of every Train row,
  one random sensor with a random fault: Dropout, Bias 0.5-3 sigma, Stuck) is applied to the RAW rows and the
  classifier is trained on the transformed clean + corrupted rows.
* Bias unit sigma_robust = IQR / 1.349 (configs/preprocessing.yaml, faults.bias_scale), not the plain std.
* Model settings: the tuned values of the new baseline (results/preprocessing/phase3/new_baseline.json).
* Augmentation seeds 0-4; reported as mean +- std.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.data import xy
from src.evaluate import fill_nan_zero, load_decisions, load_split, make_classifier
from src.faults import augment_with_faults, robust_sigma
from src.models import scores
from src.preprocessing import fit_preprocessor
from src.splits import load_config


def main(cfg_path):
    cfg = load_config(cfg_path)
    assert cfg["faults"]["bias_scale"] == "robust_iqr"
    out = Path("results/preprocessing/final")
    out.mkdir(parents=True, exist_ok=True)
    dec = load_decisions()
    spec, nb = dec["incumbent_spec"], dec["new_baseline"]
    params = {"svm": {**cfg["models"]["svm"], **json.loads(nb["svm_tuned"]["params"])},
              "lgbm": {**cfg["models"]["lgbm"], **json.loads(nb["lgbm_tuned"]["params"])}}
    tr, va = load_split(cfg)
    Xtr, ytr = xy(tr)
    Xva, yva = xy(va)
    sigma = robust_sigma(Xtr)
    pre = fit_preprocessor(spec, Xtr, ytr, tr["batch"].to_numpy(), fill_nan=False, iqr_k=cfg["phase2"]["iqr_k"])
    Zva = pre.transform(Xva)

    def fit_score(name, X_fit, y_fit):
        Zf = pre.transform(X_fit)
        a, b = (fill_nan_zero(Zf), fill_nan_zero(Zva)) if name == "svm" else (Zf, Zva)
        clf = make_classifier(name, cfg["models"], cfg["seed"],
                              svm_params=params["svm"] if name == "svm" else None,
                              lgbm_params=params["lgbm"] if name == "lgbm" else None).fit(a, y_fit)
        return scores(yva, clf.predict(b))

    rows = []
    for name in ("svm", "lgbm"):
        s = fit_score(name, Xtr, ytr)
        rows.append({"model": name, "aug_seed": "", **s})
        for seed in cfg["augmentation"]["seeds"]:
            rng = np.random.default_rng(seed)
            Xa, ya = augment_with_faults(Xtr, ytr, sigma, rng, cfg["augmentation"]["copies"])
            s = fit_score(name, Xa, ya)
            rows.append({"model": f"{name}_aug", "aug_seed": seed, **s})
            print(f"{name}_aug seed {seed}: Macro-F1 {s['macro_f1']:.4f}  Accuracy {s['accuracy']:.4f}")
    per_seed = pd.DataFrame(rows)
    per_seed.round(4).to_csv(out / "aug_baselines_per_seed.csv", index=False)
    summary = (per_seed.groupby("model").agg(n=("macro_f1", "size"), macro_f1_mean=("macro_f1", "mean"),
                                             macro_f1_std=("macro_f1", "std"), accuracy_mean=("accuracy", "mean"),
                                             accuracy_std=("accuracy", "std")).fillna(0.0).reset_index())
    order = {"svm": 0, "lgbm": 1, "svm_aug": 2, "lgbm_aug": 3}
    summary = summary.sort_values("model", key=lambda s: s.map(order))
    summary.round(4).to_csv(out / "aug_baselines_summary.csv", index=False)
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
