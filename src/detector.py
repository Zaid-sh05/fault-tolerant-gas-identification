"""Reliability detector: per sensor, a Ridge model predicts the 8 features of its block from the other sensors.

Registered in results/decisions_log.md (section B5):
  * space: signed-log of the raw features, standardised with Train mean/std; ridge without intercept on that space
  * predictors: ALL other 15 sensors (leave-pair-out variant: also without the twin), NaN predictors are filled with 0
  * score of a sensor in a row: mean over its 8 features of |prediction - value|; a block containing NaN scores +inf
  * alpha per sensor: leave-one-batch-out on Train batches (via Gram matrices, no extra data passes)
  * out-of-fold (OOF) scores: leave-one-batch-out inside the Train batches
  * normalisation (a) "sensor": score / median of the sensor's own OOF scores
                    (b) "median": score / median of the 16 scores of the same row
  * alarm threshold per sensor: `pct`-th percentile (default 95) of its OOF normalised scores
Everything is fitted on Train rows only.
"""
import numpy as np

from .data import N_SENSORS, sensor_columns
from .imputation import twin_of
from .models import signed_log

ALPHAS = (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)


class ReliabilityDetector:
    def __init__(self, normalization="sensor", lpo=False, pct=95.0, alphas=ALPHAS):
        assert normalization in ("sensor", "median")
        self.normalization, self.lpo, self.pct, self.alphas = normalization, lpo, pct, tuple(alphas)
        self._w_cache = {}

    # ---- space ----------------------------------------------------------------------------
    def to_z(self, X):
        return (signed_log(X) - self.mu_) / self.sd_

    def _predictors(self, sensor, extra_excluded=()):
        hidden = set(sensor_columns(sensor))
        if self.lpo:
            hidden |= set(sensor_columns(twin_of(sensor)))
        for e in extra_excluded:
            hidden |= set(sensor_columns(e))
        return np.array([c for c in range(128) if c not in hidden])

    # ---- fit --------------------------------------------------------------------------------
    def fit(self, X_train, batches):
        L = signed_log(X_train)
        self.mu_, self.sd_ = L.mean(0), L.std(0)
        Z = (L - self.mu_) / self.sd_
        batches = np.asarray(batches)
        self.batch_ids_ = np.unique(batches)
        self.G_ = Z.T @ Z
        self.Gb_ = {b: Z[batches == b].T @ Z[batches == b] for b in self.batch_ids_}
        self.nb_ = {b: int((batches == b).sum()) for b in self.batch_ids_}
        self.alpha_, E_oof = np.zeros(N_SENSORS), np.zeros((len(Z), N_SENSORS))
        for s in range(N_SENSORS):
            P, T = self._predictors(s), np.array(sensor_columns(s))
            # alpha: mean held-out MSE over the leave-one-batch-out folds, from Gram matrices
            best = (np.inf, None)
            for a in self.alphas:
                mse = []
                for b in self.batch_ids_:
                    Gtr = self.G_ - self.Gb_[b]
                    W = np.linalg.solve(Gtr[np.ix_(P, P)] + a * np.eye(len(P)), Gtr[np.ix_(P, T)])
                    Gb = self.Gb_[b]
                    sse = np.trace(Gb[np.ix_(T, T)]) - 2 * np.sum(W * Gb[np.ix_(P, T)]) + np.sum(W * (Gb[np.ix_(P, P)] @ W))
                    mse.append(sse / (self.nb_[b] * len(T)))
                if np.mean(mse) < best[0]:
                    best = (np.mean(mse), a)
            self.alpha_[s] = best[1]
            for b in self.batch_ids_:                                      # OOF residual scores
                m = batches == b
                Gtr = self.G_ - self.Gb_[b]
                W = np.linalg.solve(Gtr[np.ix_(P, P)] + best[1] * np.eye(len(P)), Gtr[np.ix_(P, T)])
                E_oof[m, s] = np.abs(Z[m][:, P] @ W - Z[m][:, T]).mean(1)
        self.E_oof_ = E_oof
        self.scale_ = np.median(E_oof, axis=0)
        N_oof = self._normalise(E_oof)
        self.tau_ = np.percentile(N_oof, self.pct, axis=0)
        self.W_ = {s: self._weights(s, ()) for s in range(N_SENSORS)}
        return self

    def _weights(self, sensor, extra_excluded):
        key = (sensor, tuple(sorted(extra_excluded)))
        if key not in self._w_cache:
            P, T = self._predictors(sensor, extra_excluded), np.array(sensor_columns(sensor))
            self._w_cache[key] = (P, np.linalg.solve(self.G_[np.ix_(P, P)] + self.alpha_[sensor] * np.eye(len(P)),
                                                     self.G_[np.ix_(P, T)]))
        return self._w_cache[key]

    # ---- scoring ------------------------------------------------------------------------------
    def raw_scores(self, X):
        """(n, 16) mean absolute residual per sensor block; +inf where the block contains NaN."""
        Z = self.to_z(X)
        Zf = np.nan_to_num(Z, nan=0.0)
        E = np.empty((len(X), N_SENSORS))
        for s in range(N_SENSORS):
            P, W = self.W_[s]
            T = np.array(sensor_columns(s))
            E[:, s] = np.abs(Zf[:, P] @ W - Z[:, T]).mean(1)
            E[np.isnan(Z[:, T]).any(1), s] = np.inf
        return E

    def _normalise(self, E):
        if self.normalization == "sensor":
            return E / self.scale_
        with np.errstate(invalid="ignore", divide="ignore"):
            return E / np.median(E, axis=1, keepdims=True)

    def normalised(self, X):
        E = self.raw_scores(X)
        N = self._normalise(E)
        N[np.isinf(E)] = np.inf                                           # missing block: flagged by definition
        N[np.isnan(N)] = np.inf
        return N

    def ratio(self, X):
        """normalised score / threshold: > 1 means alarm."""
        return self.normalised(X) / self.tau_

    def flags(self, X):
        return self.ratio(X) > 1.0

    # ---- reconstruction support (strategy A) ----------------------------------------------------------
    def block_prediction(self, Z_rows, sensor, unavailable):
        """Prediction (in z space) of `sensor`'s block from the sensors that are not in `unavailable` (and not the
        sensor itself); the twin is also excluded when lpo=True. Z_rows has NaN already replaced by 0."""
        P, W = self._weights(sensor, tuple(u for u in unavailable if u != sensor))
        return Z_rows[:, P] @ W

    def from_z_block(self, Z, cols):
        """Back to the raw feature scale for the columns `cols` (inverse of the signed-log + standardisation)."""
        y = Z * self.sd_[cols] + self.mu_[cols]
        return np.sign(y) * np.expm1(np.abs(y))
