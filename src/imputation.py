"""Reconstruction of a whole sensor block (8 features) from the other sensors.

Building block for Strategy A ("repair the faulty sensor"). Everything is fitted on
Train rows only; `reconstruct` never looks at the columns it is asked to rebuild.

Methods
  mean / median : per-feature Train statistic (the Mode is not applicable: all 128
                  features are continuous, so no value repeats often enough to be a mode)
  knn           : sklearn KNNImputer on the standardised features (Troyanskaya et al. 2001)
  ridge         : multi-output Ridge from the other sensors; alpha chosen on Train with
                  leave-batch-group-out folds, because drift makes random folds optimistic
  iterative     : sklearn IterativeImputer with BayesianRidge (van Buuren & Groothuis-Oudshoorn 2011)

`exclude_twin=True` hides the near-identical replicate sensor (pairs (1,2),(3,4),...)
from the predictors (leave-pair-out), which is the realistic setting.
"""
import numpy as np
from sklearn.experimental import enable_iterative_imputer  # noqa: F401  (activates IterativeImputer)
from sklearn.impute import IterativeImputer, KNNImputer
from sklearn.linear_model import BayesianRidge, Ridge
from sklearn.neighbors import NearestNeighbors

from .data import N_FEATURES, N_FEAT_PER_SENSOR, sensor_columns
from .models import signed_log

METHODS = ("mean", "median", "knn", "ridge", "iterative")


def twin_of(sensor):
    """0-based index of the replicate partner: (0,1), (2,3), ..., (14,15)."""
    return sensor ^ 1


def inverse_signed_log(y):
    return np.sign(y) * np.expm1(np.abs(y))


class BlockImputer:
    def __init__(self, method, space="raw", knn_neighbors=5,
                 ridge_alphas=(0.001, 0.01, 0.1, 1, 10, 100, 1000),
                 iterative=None, seed=0):
        if method not in METHODS or space not in ("raw", "slog"):
            raise ValueError((method, space))
        self.method, self.space, self.knn_neighbors = method, space, knn_neighbors
        self.ridge_alphas = tuple(ridge_alphas)
        self.iterative = iterative or {"max_iter": 5, "mask_fraction": 0.5}
        self.seed = seed
        self._cache = {}

    # ---- space handling -------------------------------------------------
    def _to_z(self, X):
        Z = signed_log(X) if self.space == "slog" else X
        return (Z - self.mu_) / self.sd_

    def _from_z(self, Z):
        Z = Z * self.sd_ + self.mu_
        return inverse_signed_log(Z) if self.space == "slog" else Z

    # ---- fitting --------------------------------------------------------
    def fit(self, X, batches):
        """X: Train matrix (n, 128) without NaN; batches: batch id per row (for ridge alpha)."""
        Z = signed_log(X) if self.space == "slog" else X
        self.mu_, self.sd_ = Z.mean(0), Z.std(0)
        self.Z_ = (Z - self.mu_) / self.sd_
        self.batches_ = np.asarray(batches)
        self._cache = {}
        if self.method == "median":
            self.center_ = np.median(self.Z_, axis=0)
        elif self.method == "knn":
            self.knn_ = KNNImputer(n_neighbors=self.knn_neighbors).fit(self.Z_)
        return self

    # ---- column bookkeeping ----------------------------------------------
    @staticmethod
    def _columns(sensor, exclude_twin):
        target = sensor_columns(sensor)
        hidden = set(target) | (set(sensor_columns(twin_of(sensor))) if exclude_twin else set())
        return target, [c for c in range(N_FEATURES) if c not in hidden]

    def _ridge_model(self, sensor, exclude_twin, inner_folds):
        key = ("ridge", sensor, exclude_twin)
        if key not in self._cache:
            target, pred = self._columns(sensor, exclude_twin)
            P, T = self.Z_[:, pred], self.Z_[:, target]
            best_alpha, best_err = None, np.inf
            for alpha in self.ridge_alphas:
                errs = []
                for fold in inner_folds:
                    test = np.isin(self.batches_, fold)
                    m = Ridge(alpha=alpha).fit(P[~test], T[~test])
                    errs.append(np.mean((m.predict(P[test]) - T[test]) ** 2))
                if np.mean(errs) < best_err:
                    best_alpha, best_err = alpha, float(np.mean(errs))
            self._cache[key] = (Ridge(alpha=best_alpha).fit(P, T), best_alpha)
        return self._cache[key]

    def _knn_general(self, Z, sensor, exclude_twin):
        """KNNImputer (Troyanskaya et al. 2001) with the target block (and twin) hidden."""
        Zq = Z.copy()
        Zq[:, sensor_columns(sensor)] = np.nan
        if exclude_twin:
            Zq[:, sensor_columns(twin_of(sensor))] = np.nan
        return self.knn_.transform(Zq)[:, sensor_columns(sensor)]

    def _knn_index(self, sensor, exclude_twin):
        key = ("knn", sensor, exclude_twin)
        if key not in self._cache:
            _, pred = self._columns(sensor, exclude_twin)
            self._cache[key] = NearestNeighbors(n_neighbors=self.knn_neighbors).fit(self.Z_[:, pred])
        return self._cache[key]

    def _iterative_model(self, sensor, exclude_twin):
        key = ("iter", sensor, exclude_twin)
        if key not in self._cache:
            target, pred = self._columns(sensor, exclude_twin)
            M = self.Z_[:, target + pred].copy()
            lo, hi = M.min(0), M.max(0)
            # IterativeImputer only learns columns that are missing at fit time, so hide the
            # target block in a random share of the Train rows.
            rng = np.random.default_rng([self.seed, sensor, int(exclude_twin)])
            M[rng.random(len(M)) < self.iterative["mask_fraction"], :N_FEAT_PER_SENSOR] = np.nan
            # Imputed values are bounded to the Train range: the unbounded chain diverged on a few
            # heavy-tailed blocks in the first run (see results/preprocessing/phase1/first_run).
            imp = IterativeImputer(estimator=BayesianRidge(), max_iter=self.iterative["max_iter"],
                                   initial_strategy="mean", skip_complete=True,
                                   min_value=lo, max_value=hi,
                                   random_state=self.seed)
            self._cache[key] = imp.fit(M)
        return self._cache[key]

    # ---- reconstruction -------------------------------------------------
    def reconstruct(self, X, sensor, exclude_twin=False, inner_folds=((1,),)):
        """Copy of X where the 8 features of `sensor` are predicted from the other sensors."""
        target, pred = self._columns(sensor, exclude_twin)
        Z = self._to_z(X)
        if self.method == "mean":
            T = np.zeros((len(X), len(target)))          # mean of the standardised Train column
        elif self.method == "median":
            T = np.tile(self.center_[target], (len(X), 1))
        elif self.method == "knn":
            if np.isnan(Z[:, pred]).any():               # other sensors also faulty: use sklearn's NaN-aware path
                T = self._knn_general(Z, sensor, exclude_twin)
            else:                                        # same result as KNNImputer, ~100x faster
                idx = self._knn_index(sensor, exclude_twin).kneighbors(Z[:, pred], return_distance=False)
                T = self.Z_[:, target][idx].mean(axis=1)
        elif self.method == "ridge":
            model, _ = self._ridge_model(sensor, exclude_twin, inner_folds)
            T = model.predict(np.nan_to_num(Z[:, pred]))
        else:
            imp = self._iterative_model(sensor, exclude_twin)
            Mq = np.column_stack([np.full((len(X), len(target)), np.nan), Z[:, pred]])
            T = imp.transform(Mq)[:, :len(target)]
        Zr = Z.copy()
        Zr[:, target] = T
        out = X.copy()
        out[:, target] = self._from_z(Zr)[:, target]
        return out

    def ridge_alpha(self, sensor, exclude_twin):
        return self._cache[("ridge", sensor, exclude_twin)][1]


def block_errors(X_true, X_hat, mu_raw, sd_raw, sensor):
    """Per-feature errors of one rebuilt block on the raw standardised scale ((x - Train mean) / Train std):
    rmse, mae, medae (median absolute error) and r2. RMSE is very sensitive to a single extreme record,
    MAE less so and the median absolute error hardly at all. R^2 uses the mean of the evaluated set."""
    cols = sensor_columns(sensor)
    t = (X_true[:, cols] - mu_raw[cols]) / sd_raw[cols]
    h = (X_hat[:, cols] - mu_raw[cols]) / sd_raw[cols]
    err = np.abs(h - t)
    sse = (err ** 2).sum(0)
    sst = ((t - t.mean(0)) ** 2).sum(0)
    return {"rmse": np.sqrt(sse / len(t)), "mae": err.mean(0), "medae": np.median(err, axis=0),
            "r2": 1.0 - sse / sst}
