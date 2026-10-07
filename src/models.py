"""Baseline models. All preprocessing is fitted on Train only inside the pipeline."""
import itertools
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from sklearn.metrics import f1_score, accuracy_score
from lightgbm import LGBMClassifier


def signed_log(X):
    return np.sign(X) * np.log1p(np.abs(X))


def make_lgbm(params, seed):
    # LightGBM handles NaN (dropout) natively.
    return LGBMClassifier(random_state=seed, deterministic=True, n_jobs=4, verbose=-1, **params)


def make_svm(params, seed):
    p = dict(params); transform = p.pop("transform", "none")
    steps = [FunctionTransformer(signed_log)] if transform == "slog" else []
    # NaN -> 0 after standardisation = Train mean (documented imputation choice).
    steps += [StandardScaler(), SimpleImputer(strategy="constant", fill_value=0.0),
              SVC(kernel="rbf", random_state=seed, **p)]
    return make_pipeline(*steps)


def grid(d):
    keys = list(d)
    for vals in itertools.product(*(d[k] for k in keys)):
        yield dict(zip(keys, vals))


def scores(y_true, y_pred):
    labels = np.unique(y_true)  # Macro-F1 over classes present in the evaluated set
    return {"macro_f1": f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0),
            "accuracy": accuracy_score(y_true, y_pred)}
