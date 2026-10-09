"""Audit sanity checks on Drift-Dev and Validation only (batches 1-7; batches 8-10 are never loaded).

Usage: python results/audit/sanity_checks.py   -> results/audit/sanity_checks.json (printed)
1. Label shuffle: the v1 pipeline (StandardScaler -> SVM C=10, gamma=0.01) trained on randomly permuted Train labels (3 seeds).
   Expected: accuracy near the majority-class share of the evaluation batch, Macro-F1 far below the real model.
2. Batch identity: logistic regression predicting the batch id from the preprocessed Train features (5-fold CV) - diagnostic of drift.
"""
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.svm import SVC

sys.path.insert(0, ".")
from src.data import xy  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.models import scores  # noqa: E402
from src.preprocessing import fit_preprocessor  # noqa: E402
from src.splits import TEST_BATCHES, get_protocol_data, load_config  # noqa: E402

PROTOCOLS = {"drift_dev": "configs/v2_drift_dev.yaml", "temporal": "configs/preprocessing.yaml"}
SPEC = {"clip": "none", "slog": False, "scaler": "standard", "groups": [], "select": "none"}


def main():
    out = {}
    for name, cfg_path in PROTOCOLS.items():
        cfg = load_config(cfg_path)
        assert not set(cfg["split"]["train_batches"] + cfg["split"]["val_batches"]) & TEST_BATCHES
        proto = get_protocol_data(cfg)
        Xtr, ytr = xy(proto.train)
        btr = proto.train["batch"].to_numpy()
        pre = fit_preprocessor(SPEC, Xtr, ytr, btr)
        Ztr = fill_nan_zero(pre.transform(Xtr))
        res = {}
        for b in sorted(proto.eval["batch"].unique()):
            X, y = xy(proto.eval[proto.eval["batch"] == b])
            Z = fill_nan_zero(pre.transform(X))
            real = scores(y, SVC(kernel="rbf", C=10, gamma=0.01, random_state=0).fit(Ztr, ytr).predict(Z))
            shuf = []
            for s in range(3):
                yp = np.random.default_rng(s).permutation(ytr)
                shuf.append(scores(y, SVC(kernel="rbf", C=10, gamma=0.01, random_state=0).fit(Ztr, yp).predict(Z)))
            res[f"batch_{b}"] = {"real_macro_f1": real["macro_f1"], "real_accuracy": real["accuracy"],
                                 "shuffled_macro_f1": [r["macro_f1"] for r in shuf], "shuffled_accuracy": [r["accuracy"] for r in shuf],
                                 "majority_class_share": float(np.bincount(y).max() / len(y)), "n_classes": int(len(np.unique(y)))}
        cv = StratifiedKFold(5, shuffle=True, random_state=0)
        pred = cross_val_predict(LogisticRegression(max_iter=2000), Ztr, btr, cv=cv)
        res["batch_identity_cv_accuracy"] = float((pred == btr).mean())
        res["batch_identity_chance_majority"] = float(np.bincount(btr).max() / len(btr))
        out[name] = res
        print(name, json.dumps(res, indent=1), flush=True)
    Path("results/audit/sanity_checks.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
