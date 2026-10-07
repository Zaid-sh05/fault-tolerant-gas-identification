"""Fit/score helpers shared by the preprocessing experiments, plus trial logging and the decision rule."""
import itertools
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.svm import SVC

from .data import load_batches, xy
from .models import scores
from .preprocessing import fill_nan_zero, fit_preprocessor
from .splits import get_protocol_data

RESULTS = Path("results/preprocessing")


def load_split(cfg):
    """Train and evaluation frames of the configured protocol (cleaning rule applied to Train only).
    Test batches are never opened."""
    p = get_protocol_data(cfg)
    return p.train, p.eval


def fit_on_batches(raw_dir, spec, batches, fill_nan=False):
    """Load ONLY `batches`, fit the preprocessor on them. Used by the leakage tests."""
    df = load_batches(raw_dir, batches)
    X, y = xy(df)
    return fit_preprocessor(spec, X, y, df["batch"].to_numpy(), fill_nan)


def make_classifier(name, models_cfg, seed, svm_params=None, lgbm_params=None):
    if name == "svm":
        return SVC(kernel="rbf", random_state=seed, **(svm_params or models_cfg["svm"]))
    return LGBMClassifier(random_state=seed, deterministic=True, n_jobs=4, verbose=-1,
                          **(lgbm_params or models_cfg["lgbm"]))


def evaluate_spec(spec, tr, va, cfg, svm_params=None, lgbm_params=None, fitted=None):
    """Fit preprocessing on Train, fit SVM and LightGBM on the result, score on Validation.
    Returns a flat dict of metrics. `fitted` lets a caller reuse an already fitted preprocessor."""
    seed = cfg["seed"]
    Xtr, ytr = xy(tr)
    Xva, yva = xy(va)
    t0 = time.time()
    pre = fitted or fit_preprocessor(spec, Xtr, ytr, tr["batch"].to_numpy(), fill_nan=False,
                                     iqr_k=cfg["phase2"]["iqr_k"], seed=seed)
    Ztr, Zva = pre.transform(Xtr), pre.transform(Xva)
    out = {"n_features": Ztr.shape[1]}
    for name in ("svm", "lgbm"):
        a, b = (fill_nan_zero(Ztr), fill_nan_zero(Zva)) if name == "svm" else (Ztr, Zva)
        clf = make_classifier(name, cfg["models"], seed, svm_params, lgbm_params).fit(a, ytr)
        s = scores(yva, clf.predict(b))
        out[f"{name}_macro_f1"], out[f"{name}_accuracy"] = s["macro_f1"], s["accuracy"]
    out["seconds"] = round(time.time() - t0, 1)
    return out


def fit_predict(spec, tr, va, cfg, models=("svm",), svm_params=None, lgbm_params=None):
    """Fit preprocessing on Train, the requested models on the result, return their Validation predictions."""
    seed = cfg["seed"]
    Xtr, ytr = xy(tr)
    Xva, _ = xy(va)
    pre = fit_preprocessor(spec, Xtr, ytr, tr["batch"].to_numpy(), fill_nan=False,
                           iqr_k=cfg["phase2"]["iqr_k"], seed=seed)
    Ztr, Zva = pre.transform(Xtr), pre.transform(Xva)
    preds = {}
    for name in models:
        a, b = (fill_nan_zero(Ztr), fill_nan_zero(Zva)) if name == "svm" else (Ztr, Zva)
        preds[name] = make_classifier(name, cfg["models"], seed, svm_params, lgbm_params).fit(a, ytr).predict(b)
    return preds


def bootstrap_diff(y, pred_a, pred_b, n=1000, seed=0, ci=0.95):
    """Paired bootstrap over evaluation rows of Macro-F1(a) - Macro-F1(b): (mean, ci_low, ci_high, share > 0)."""
    rng = np.random.default_rng(seed)
    diffs = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, len(y), len(y))
        diffs[i] = scores(y[idx], pred_a[idx])["macro_f1"] - scores(y[idx], pred_b[idx])["macro_f1"]
    lo, hi = np.percentile(diffs, [(1 - ci) / 2 * 100, (1 + ci) / 2 * 100])
    return float(diffs.mean()), float(lo), float(hi), float((diffs > 0).mean())


def grid_points(grid):
    keys = list(grid)
    return [dict(zip(keys, vals)) for vals in itertools.product(*(grid[k] for k in keys))]


def tune(spec, tr, va, cfg):
    """Pick the best SVM and LightGBM settings of the pre-registered grids on Validation (same protocol as
    the old baselines). One preprocessor fit is shared by all grid points. Every point is returned."""
    seed = cfg["seed"]
    Xtr, ytr = xy(tr)
    pre = fit_preprocessor(spec, Xtr, ytr, tr["batch"].to_numpy(), fill_nan=False,
                           iqr_k=cfg["phase2"]["iqr_k"], seed=seed)
    rows = []
    for name, grid, base in (("svm", cfg["models"]["final_svm_grid"], cfg["models"]["svm"]),
                             ("lgbm", cfg["models"]["final_lgbm_grid"], cfg["models"]["lgbm"])):
        for point in grid_points(grid):
            params = {**base, **point}
            m = evaluate_spec(spec, tr, va, cfg, svm_params=params if name == "svm" else None,
                              lgbm_params=params if name == "lgbm" else None, fitted=pre)
            rows.append({"model": name, "params": json.dumps(point), "macro_f1": m[f"{name}_macro_f1"],
                         "accuracy": m[f"{name}_accuracy"]})
    return pd.DataFrame(rows)


def log_trial(phase, trial_id, spec, metrics, note=""):
    """Append one row to results/preprocessing/trials.csv (every combination tried is kept)."""
    RESULTS.mkdir(parents=True, exist_ok=True)
    row = pd.DataFrame([{"phase": phase, "trial_id": trial_id, "spec": json.dumps(spec, sort_keys=True),
                         **metrics, "note": note}])
    path = RESULTS / "trials.csv"
    row.to_csv(path, mode="a", header=not path.exists(), index=False)


def choose(incumbent, candidates, rule):
    """Pre-registered rule: best candidate on the primary metric wins only if it beats the incumbent
    by more than min_gain; otherwise the incumbent (the simpler pipeline) stays.
    incumbent/candidates: dicts with 'trial_id', 'spec' and the metrics."""
    key = rule["primary"]
    best = max(candidates, key=lambda c: c[key])
    winner = best if best[key] - incumbent[key] > rule["min_gain"] else incumbent
    flag = incumbent["lgbm_macro_f1"] - winner["lgbm_macro_f1"] > rule["lgbm_flag_drop"]
    return winner, flag


def load_decisions():
    path = RESULTS / "decisions.json"
    return json.load(open(path)) if path.exists() else None


def save_decisions(d):
    RESULTS.mkdir(parents=True, exist_ok=True)
    json.dump(d, open(RESULTS / "decisions.json", "w"), indent=1)
