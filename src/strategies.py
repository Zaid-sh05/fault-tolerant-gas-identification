"""Inference-time strategies for faulty sensors (overnight Part 4). Registered in results/decisions_log.md (B10).

A  reconstruction : the 8 features of every flagged sensor (per row) are replaced by a Ridge prediction in signed-log
                    space made from the sensors that are NOT flagged in that row (and, optionally, not the twin);
                    then the clean SVM.
B  exclusion      : an SVM trained without the flagged sensors (one model per excluded set, cached on disk).
C  experts        : 8 replicate-pair experts (SVM with probabilities, 16 features each), combined with weights that
                    follow the reliability of their sensors, or with equal weights.
At most CAP sensors are acted upon in a row (the CAP with the highest alarm ratio) so that the number of distinct
excluded sets stays bounded; this applies to A and B alike.
"""
import os
from collections import defaultdict

import joblib
import numpy as np
from sklearn.svm import SVC

from .data import sensor_columns
from .evaluate import fill_nan_zero
from .fastsvm import fast_svm_predict
from .imputation import twin_of

CAP = 4
PAIRS = [(2 * p, 2 * p + 1) for p in range(8)]


def acted_sets(ratio, flags, cap=CAP):
    """Per row, the tuple of flagged sensors to act on: all of them, or the `cap` with the highest ratio."""
    sets = []
    for r, f in zip(ratio, flags):
        idx = np.flatnonzero(f)
        if len(idx) > cap:
            idx = idx[np.argsort(-r[idx])[:cap]]
        sets.append(tuple(sorted(int(i) for i in idx)))
    return sets


def group_by_set(sets):
    groups = defaultdict(list)
    for i, s in enumerate(sets):
        groups[s].append(i)
    return {s: np.array(rows) for s, rows in groups.items()}


class StrategyKit:
    def __init__(self, pre, svm, Xtr, ytr, detector, svm_params, cache_dir, seed=0):
        self.pre, self.svm, self.det, self.seed = pre, svm, detector, seed
        self.svm_params, self.cache_dir = svm_params, cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.ytr = ytr
        self.Ztr = fill_nan_zero(pre.transform(Xtr))
        self._reduced, self._experts = {}, None

    # ---- A ---------------------------------------------------------------------------------------
    def reconstruct(self, Xf, groups, exclude_twin):
        Zf = np.nan_to_num(self.det.to_z(Xf))
        Xr = Xf.copy()
        for pattern, rows in groups.items():
            for s in pattern:
                unavailable = set(pattern) | ({twin_of(s)} if exclude_twin else set())
                z = self.det.block_prediction(Zf[rows], s, tuple(sorted(unavailable - {s})))
                Xr[np.ix_(rows, sensor_columns(s))] = self.det.from_z_block(z, sensor_columns(s))
        return Xr

    def predict_A(self, Xf, sets, exclude_twin):
        Xr = self.reconstruct(Xf, group_by_set(sets), exclude_twin)
        return fast_svm_predict(self.svm, fill_nan_zero(self.pre.transform(Xr)))

    # ---- B ---------------------------------------------------------------------------------------
    def reduced_model(self, pattern):
        if pattern not in self._reduced:
            path = os.path.join(self.cache_dir, "B_" + ("none" if not pattern else "_".join(map(str, pattern))) + ".joblib")
            if os.path.exists(path):
                try:
                    self._reduced[pattern] = joblib.load(path)
                except Exception:
                    os.remove(path)
            if pattern not in self._reduced:
                keep = self.keep_columns(pattern)
                model = SVC(kernel="rbf", random_state=self.seed, **self.svm_params).fit(self.Ztr[:, keep], self.ytr)
                tmp = f"{path}.{os.getpid()}.tmp"
                joblib.dump(model, tmp)
                os.replace(tmp, path)                                          # atomic: workers may race
                self._reduced[pattern] = model
        return self._reduced[pattern]

    @staticmethod
    def keep_columns(pattern):
        hidden = {c for s in pattern for c in sensor_columns(s)}
        return np.array([c for c in range(128) if c not in hidden])

    def predict_B(self, Xf, sets):
        Z = fill_nan_zero(self.pre.transform(Xf))
        y = np.empty(len(Xf), dtype=int)
        for pattern, rows in group_by_set(sets).items():
            y[rows] = fast_svm_predict(self.reduced_model(pattern), Z[rows][:, self.keep_columns(pattern)])
        return y

    # ---- C ---------------------------------------------------------------------------------------
    def experts(self):
        if self._experts is None:
            path = os.path.join(self.cache_dir, "C_experts.joblib")
            if os.path.exists(path):
                self._experts = joblib.load(path)
            else:
                self._experts = []
                for pair in PAIRS:
                    cols = np.array(sum((sensor_columns(s) for s in pair), []))
                    clf = SVC(kernel="rbf", C=self.svm_params["C"], gamma="scale", probability=True,
                              random_state=self.seed).fit(self.Ztr[:, cols], self.ytr)
                    self._experts.append((cols, clf))
                tmp = f"{path}.{os.getpid()}.tmp"
                joblib.dump(self._experts, tmp)
                os.replace(tmp, path)
        return self._experts

    @staticmethod
    def expert_weights(ratio):
        """Per row and expert: min over its two sensors of 1 / max(1, ratio)^2 (ratio = score / alarm threshold)."""
        with np.errstate(divide="ignore", over="ignore"):
            w_sensor = 1.0 / np.maximum(1.0, ratio) ** 2
        w_sensor[np.isinf(ratio)] = 0.0
        return np.stack([np.minimum(w_sensor[:, a], w_sensor[:, b]) for a, b in PAIRS], axis=1)

    def expert_proba(self, Xf):
        """(n, 8, 6) class probabilities of the 8 pair experts; computed once per scenario."""
        Z = fill_nan_zero(self.pre.transform(Xf))
        return np.stack([clf.predict_proba(Z[:, cols]) for cols, clf in self.experts()], axis=1)

    def combine(self, proba, ratio=None):
        """ratio=None: equal weights; otherwise reliability weights."""
        w = np.ones(proba.shape[:2]) if ratio is None else self.expert_weights(ratio)
        w[w.sum(1) == 0] = 1.0                                                                       # nothing reliable: equal
        return self.experts()[0][1].classes_[np.argmax((proba * w[:, :, None]).sum(1), axis=1)]
