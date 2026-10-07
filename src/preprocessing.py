"""Preprocessing pipeline: raw 128 features -> clip -> build features -> scale -> select -> NaN fill.

Design rules
  * Every transformer is fitted on Train rows only (the caller decides which rows it passes to fit).
  * Faults are injected on the RAW 128 features, then the pipeline runs, so every derived feature
    is computed from the (possibly faulty) raw values inside the pipeline.
  * Every output column can be traced to the sensor(s) it was computed from (`pipeline_provenance`),
    because faults are injected and reliability is scored per sensor.
  * NaN (Dropout fault) flows through: scalers ignore it, derived features stay NaN, and the optional
    last step fills NaN with 0 (the Train mean after standardisation) for models that need it (SVM).
"""
import warnings

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import f_classif, mutual_info_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler, RobustScaler, StandardScaler

from .data import FEATURE_KINDS, FEATURES, N_FEAT_PER_SENSOR, N_SENSORS
from .models import signed_log

KIND = {k: i for i, k in enumerate(FEATURE_KINDS)}
TRANSIENT = [k for k in FEATURE_KINDS if k.startswith("EMA")]
SCALERS = {"standard": StandardScaler, "robust": RobustScaler, "minmax": MinMaxScaler}


def sname(s):
    return f"S{s + 1:02d}"


def fill_nan_zero(X):
    """NaN -> 0. After standardisation 0 is the Train mean, i.e. 'no information' for the SVM."""
    return np.where(np.isnan(X), 0.0, X)


def raw_provenance():
    rows = [{"feature": f, "sources": (s,), "group": "raw", "formula": f"raw {k}"}
            for s in range(N_SENSORS) for k, f in zip(FEATURE_KINDS, FEATURES[s * 8:(s + 1) * 8])]
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# Clipper (Tukey inner fences fitted on Train)
# --------------------------------------------------------------------------------------
class IQRClipper(BaseEstimator, TransformerMixin):
    """Winsorise every feature to [Q1 - k*IQR, Q3 + k*IQR] computed on the fitted rows."""

    def __init__(self, k=1.5):
        self.k = k

    def fit(self, X, y=None):
        q1, q3 = np.nanpercentile(X, [25, 75], axis=0)
        iqr = q3 - q1
        flat = iqr == 0                                   # a constant-ish feature: do not clip
        self.lo_ = np.where(flat, -np.inf, q1 - self.k * iqr)
        self.hi_ = np.where(flat, np.inf, q3 + self.k * iqr)
        return self

    def transform(self, X):
        return np.clip(X, self.lo_, self.hi_)             # NaN stays NaN

    def outside(self, X):
        return (X < self.lo_) | (X > self.hi_)


# --------------------------------------------------------------------------------------
# Feature builder: optional signed-log of the raw block + engineered groups
# --------------------------------------------------------------------------------------
def _quiet(fn):
    def wrapped(*a, **k):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)       # all-NaN rows (Dropout of every sensor)
            return fn(*a, **k)
    return wrapped


@_quiet
def _pn_l2(B):
    """Array normalisation: each sensor's value divided by the L2 norm of the 16 values of the same kind."""
    cols = []
    for kind in ("DR", "absDR"):
        v = B[:, :, KIND[kind]]
        norm = np.sqrt(np.nansum(v ** 2, axis=1, keepdims=True))
        cols.append(np.divide(v, norm, out=np.zeros_like(v), where=norm > 0))
    return np.hstack(cols)


@_quiet
def _pn_logmed(B):
    """Concentration-robust pattern: signed-log of |DR| minus its median over the 16 sensors."""
    u = signed_log(B[:, :, KIND["absDR"]])
    return u - np.nanmedian(u, axis=1, keepdims=True)


@_quiet
def _trans_ratio(B):
    """Dynamics relative to amplitude: log1p|EMA| - log1p||DR||, per sensor, for the 6 EMA features."""
    amp = np.log1p(np.abs(B[:, :, KIND["absDR"]]))
    return np.hstack([np.log1p(np.abs(B[:, :, KIND[k]])) - amp for k in TRANSIENT])


GROUPS = {
    # name: (function, output column names, source sensors per column, formula)
    "pn_l2": (_pn_l2, [f"{sname(j)}_pnl2_{k}" for k in ("DR", "absDR") for j in range(16)],
              lambda c: tuple(range(16)), "x_j / sqrt(sum_k x_k^2) over the 16 sensors, kinds DR and |DR|"),
    "pn_logmed": (_pn_logmed, [f"{sname(j)}_pnlogmed_absDR" for j in range(16)],
                  lambda c: tuple(range(16)), "slog(|DR|_j) - median_k slog(|DR|_k)"),
    "trans_ratio": (_trans_ratio, [f"{sname(j)}_trratio_{k}" for k in TRANSIENT for j in range(16)],
                    lambda c: (c % 16,), "log1p|EMA_j| - log1p(||DR||_j)"),
}


class FeatureBuilder(BaseEstimator, TransformerMixin):
    """[raw 128 (optionally signed-log)] + engineered groups. Stateless; engineered groups are
    always computed from the raw (clipped) values, never from the signed-log block."""

    def __init__(self, slog_raw=False, groups=()):
        self.slog_raw = slog_raw
        self.groups = tuple(groups)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        B = X.reshape(len(X), N_SENSORS, N_FEAT_PER_SENSOR)
        parts = [signed_log(X) if self.slog_raw else X]
        parts += [GROUPS[g][0](B) for g in self.groups]
        return np.hstack(parts)

    def provenance(self):
        prov = raw_provenance()
        if self.slog_raw:
            prov["formula"] = "slog(" + prov["formula"] + ")"
        extra = []
        for g in self.groups:
            _, names, sources, formula = GROUPS[g]
            extra += [{"feature": n, "sources": sources(c), "group": g, "formula": formula}
                      for c, n in enumerate(names)]
        return pd.concat([prov, pd.DataFrame(extra)], ignore_index=True)


# --------------------------------------------------------------------------------------
# Selector: redundancy filter + score-based top fraction, never drops a sensor
# --------------------------------------------------------------------------------------
class ScoreSelector(BaseEstimator, TransformerMixin):
    """score = mean(rank(MI), rank(ANOVA-F)) * (1 - batch_eta2), all computed on Train.

    batch_eta2: share of the variance (after removing the gas effect) explained by the batch,
    i.e. how much the feature drifts inside Train. Lower is better.
    `owner[j]` is the single sensor feature j was computed from (-1 if it mixes sensors);
    every sensor keeps at least `min_own` of its own features.
    """

    def __init__(self, owner, corr_threshold=0.95, keep_frac=1.0, min_own=2, mi_neighbors=3, seed=0):
        self.owner = owner
        self.corr_threshold, self.keep_frac = corr_threshold, keep_frac
        self.min_own, self.mi_neighbors, self.seed = min_own, mi_neighbors, seed

    def fit(self, X, y, batches):
        owner = np.asarray(self.owner)
        self.mi_ = mutual_info_classif(X, y, n_neighbors=self.mi_neighbors, random_state=self.seed)
        self.f_ = np.nan_to_num(f_classif(X, y)[0])
        resid = X - pd.DataFrame(X).groupby(y).transform("mean").to_numpy()
        total = (resid ** 2).sum(0)
        bm = pd.DataFrame(resid).groupby(np.asarray(batches)).transform("mean").to_numpy()
        self.eta2_ = np.divide((bm ** 2).sum(0), total, out=np.zeros(X.shape[1]), where=total > 0)
        rank = lambda v: pd.Series(v).rank(pct=True).to_numpy()
        self.score_ = (rank(self.mi_) + rank(self.f_)) / 2 * (1 - self.eta2_)

        order = np.argsort(-self.score_)
        corr = np.abs(np.nan_to_num(np.corrcoef(X, rowvar=False)))
        kept = []
        for j in order:                                   # greedy: best score first, drop later near-duplicates
            if not kept or corr[j, kept].max() <= self.corr_threshold:
                kept.append(j)
        kept = self._restore_sensors(set(kept), order, owner)
        if self.keep_frac < 1.0:
            n_keep = int(np.ceil(self.keep_frac * len(kept)))
            top = [j for j in order if j in kept][:n_keep]
            kept = self._restore_sensors(set(top), order, owner)
        self.support_ = np.array(sorted(kept))
        return self

    def _restore_sensors(self, kept, order, owner):
        for s in range(N_SENSORS):
            own = [j for j in order if owner[j] == s]
            missing = self.min_own - sum(j in kept for j in own)
            kept |= set([j for j in own if j not in kept][:max(missing, 0)])
        return kept

    def transform(self, X):
        return X[:, self.support_]


# --------------------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------------------
def build_preprocessor(spec, fill_nan=False, iqr_k=1.5, seed=0):
    """spec: {clip: none|iqr, slog: bool, scaler: standard|robust|minmax, groups: [...],
              select: none | {corr_threshold, keep_frac, min_own, mi_neighbors}}"""
    builder = FeatureBuilder(spec["slog"], tuple(spec["groups"]))
    steps = [("clip", IQRClipper(iqr_k))] if spec["clip"] == "iqr" else []
    steps += [("build", builder), ("scale", SCALERS[spec["scaler"]]())]
    if spec["select"] != "none":
        owner = [s[0] if len(s) == 1 else -1 for s in builder.provenance()["sources"]]
        steps.append(("select", ScoreSelector(owner, seed=seed, **spec["select"])))
    if fill_nan:
        steps.append(("fill", FunctionTransformer(fill_nan_zero)))
    return Pipeline(steps)


def fit_preprocessor(spec, X, y, batches, fill_nan=False, **kw):
    pipe = build_preprocessor(spec, fill_nan, **kw)
    params = {"select__batches": np.asarray(batches)} if "select" in pipe.named_steps else {}
    return pipe.fit(X, y, **params)


def pipeline_provenance(pipe):
    """One row per output column: feature name, source sensors, group, formula."""
    prov = pipe.named_steps["build"].provenance()
    if "select" in pipe.named_steps:
        prov = prov.iloc[pipe.named_steps["select"].support_]
    prov = prov.reset_index(drop=True)
    prov["n_sources"] = prov["sources"].map(len)
    prov["sources"] = prov["sources"].map(lambda t: "|".join(sname(s) for s in t))
    return prov[["feature", "sources", "n_sources", "group", "formula"]]
