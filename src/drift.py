"""v2 drift-robust base models (POST-HOC, registered in results/decisions_log.md section G5).

Front-end transforms map the readings of ONE batch back to raw units of the Train reference, so everything downstream
(StandardScaler -> SVM, detector, A, B, augmentation) is unchanged:
  Identity         M0 (and M3, which has no transform)
  BatchRobustNorm  M1: per batch (x - median_b) / s_b * s_ref + median_ref, s = IQR / 1.349
  Coral            M2: CORAL (Sun, Feng, Saenko, AAAI 2016), the new batch mapped to the Train covariance
  Chain            M4 combinations of two transforms
`train_transform(X, batches)` maps the Train rows (M1: every Train batch with its own statistics); `transform(X)` maps one
new batch with statistics computed from its own readings (no labels). BatchEnsemble is M3 (Vergara et al. 2012).
"""
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.svm import SVC

from .evaluate import fill_nan_zero
from .fastsvm import fast_svm_predict
from .models import scores


def robust_stats(X):
    med = np.nanmedian(X, axis=0)
    q1, q3 = np.nanpercentile(X, [25, 75], axis=0)
    return med, (q3 - q1) / 1.349


class Identity:
    def fit(self, X, batches):
        return self

    def train_transform(self, X, batches):
        return X

    def transform(self, X):
        return X


class BatchRobustNorm:
    def fit(self, X, batches):
        self.med_, self.s_ = robust_stats(X)
        return self

    def _map(self, X):
        med, s = robust_stats(X)
        s = np.where(s > 0, s, self.s_)                         # constant feature in this batch (e.g. Stuck): shift only
        return (X - med) / s * self.s_ + self.med_

    def train_transform(self, X, batches):
        out = np.empty_like(X)
        for b in np.unique(batches):
            m = batches == b
            out[m] = self._map(X[m])
        return out

    def transform(self, X):
        return self._map(X)


def _sym_power(C, p):
    w, V = np.linalg.eigh(C)
    return (V * np.maximum(w, 1e-12) ** p) @ V.T


class Coral:
    """Z -> Z Ct^(-1/2) Cs^(1/2) in the Train-standardised space (covariances + I), then back to raw units.
    Deviation from the paper (logged): the target is mapped to the source, so the classifier is not retrained."""

    def fit(self, X, batches):
        self.mu_, self.sd_ = X.mean(0), X.std(0)
        self.sd_[self.sd_ == 0] = 1.0
        Z = (X - self.mu_) / self.sd_
        self.cs_half_ = _sym_power(np.cov(Z, rowvar=False) + np.eye(X.shape[1]), 0.5)
        return self

    def train_transform(self, X, batches):
        return X

    def transform(self, X):
        Z = (X - self.mu_) / self.sd_
        missing = np.isnan(Z)
        Z0 = np.where(missing, 0.0, Z)
        ct = np.cov(Z0, rowvar=False) + np.eye(X.shape[1])
        Zc = Z0 @ _sym_power(ct, -0.5) @ self.cs_half_
        Zc[missing] = np.nan                                    # a missing block stays missing
        return Zc * self.sd_ + self.mu_


class Chain:
    """first, then second (second fitted on the first's Train output)."""

    def __init__(self, first, second):
        self.first, self.second = first, second

    def fit(self, X, batches):
        self.first.fit(X, batches)
        self.second.fit(self.first.train_transform(X, batches), batches)
        return self

    def train_transform(self, X, batches):
        return self.second.train_transform(self.first.train_transform(X, batches), batches)

    def transform(self, X):
        return self.second.transform(self.first.transform(X))


class BatchEnsemble:
    """One SVM per Train batch, weighted majority vote. Weight = Macro-F1 on the most recent Train batch; the member of that
    batch gets its 5-fold stratified cross-validated Macro-F1 instead."""

    def __init__(self, svm_params, seed=0):
        self.svm_params, self.seed = svm_params, seed

    def fit(self, Z, y, batches):
        Z = fill_nan_zero(Z)
        self.batches_ = np.unique(batches)
        latest = self.batches_.max()
        ml = batches == latest
        self.members_, self.weights_ = [], []
        for b in self.batches_:
            m = batches == b
            svm = SVC(kernel="rbf", random_state=self.seed, **self.svm_params).fit(Z[m], y[m])
            if b == latest:
                cv = StratifiedKFold(5, shuffle=True, random_state=self.seed)
                pred = cross_val_predict(SVC(kernel="rbf", random_state=self.seed, **self.svm_params), Z[ml], y[ml], cv=cv)
            else:
                pred = fast_svm_predict(svm, Z[ml])
            self.members_.append(svm)
            self.weights_.append(scores(y[ml], pred)["macro_f1"])
        self.classes_ = np.unique(y)
        return self

    def predict(self, Z):
        Z = fill_nan_zero(Z)
        votes = np.zeros((len(Z), len(self.classes_)))
        for svm, w in zip(self.members_, self.weights_):
            votes[np.arange(len(Z)), np.searchsorted(self.classes_, fast_svm_predict(svm, Z))] += w
        return self.classes_[np.argmax(votes, axis=1)]
