"""Shared setup of the overnight study: one protocol, its fitted preprocessing and its reference models.

Everything is fitted on the Train rows of the protocol (cleaned by the invalid-value rule). Evaluation rows are only
used to compute predictions. Batches 8-10 are read only by the final_test protocol (src/splits.py), once, with approval.
"""
import json
from pathlib import Path

import joblib
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.svm import SVC

from .data import xy
from .evaluate import fill_nan_zero
from .fastsvm import fast_svm_predict
from .faults import augment_with_faults
from .preprocessing import fit_preprocessor
from .scenarios import FaultStats
from .splits import get_protocol_data, load_config

OVERNIGHT = Path("results/overnight")
AUG_SEEDS = (0, 1, 2, 3, 4)


class Study:
    def __init__(self, cfg_path, name):
        self.cfg, self.name = load_config(cfg_path), name
        fin = json.load(open(OVERNIGHT / "final_pipeline.json"))
        self.spec = fin["spec"]
        self.svm_params = {**self.cfg["models"]["svm"], **fin["svm_params"]}
        self.lgbm_params = fin["lgbm_params"]
        self.seed = self.cfg["seed"]
        self.proto = get_protocol_data(self.cfg)
        self.Xtr, self.ytr = xy(self.proto.train)
        self.Xev, self.yev = xy(self.proto.eval)
        self.pre = fit_preprocessor(self.spec, self.Xtr, self.ytr, self.proto.groups, fill_nan=False)
        self.stats = FaultStats.fit(self.Xtr)
        self.dir = Path(self.cfg.get("output_root", OVERNIGHT)) / name
        self.dir.mkdir(parents=True, exist_ok=True)

    # ---- models -------------------------------------------------------------------------
    def new_svm(self, probability=False):
        return SVC(kernel="rbf", random_state=self.seed, probability=probability, **self.svm_params)

    def new_lgbm(self, n_jobs=4):
        return LGBMClassifier(random_state=self.seed, deterministic=True, n_jobs=n_jobs, verbose=-1, **self.lgbm_params)

    def fit_model(self, kind, X, y):
        Z = self.pre.transform(X)
        return self.new_svm().fit(fill_nan_zero(Z), y) if kind == "svm" else self.new_lgbm().fit(Z, y)

    def models(self):
        """svm, lgbm and 5 fault-augmented versions of each (cached on disk)."""
        mdir = self.dir / "models"
        mdir.mkdir(exist_ok=True)
        sigma = self.stats.sigma
        out = {}
        for kind in ("svm", "lgbm"):
            for tag, seed in [(kind, None)] + [(f"{kind}_aug{s}", s) for s in AUG_SEEDS]:
                path = mdir / f"{tag}.joblib"
                if not path.exists():
                    X, y = self.Xtr, self.ytr
                    if seed is not None:
                        X, y = augment_with_faults(X, y, sigma, np.random.default_rng(seed), self.cfg["augmentation"]["copies"])
                    joblib.dump(self.fit_model(kind, X, y), path)
                out[tag] = joblib.load(path)
        for m in out.values():
            if isinstance(m, LGBMClassifier):
                m.set_params(n_jobs=1)
        return out

    def predict(self, models, Z, names=None):
        """Predictions of the named models on preprocessed features Z (NaN allowed)."""
        return {n: (fast_svm_predict(m, fill_nan_zero(Z)) if n.startswith("svm") else m.predict(Z))
                for n, m in models.items() if names is None or n in names}
