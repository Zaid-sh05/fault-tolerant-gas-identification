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
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler, RobustScaler, StandardScaler

from .data import FEATURE_KINDS, FEATURES, N_FEAT_PER_SENSOR, N_SENSORS
from .models import signed_log

KIND = {k: i for i, k in enumerate(FEATURE_KINDS)}
TRANSIENT = [k for k in FEATURE_KINDS if k.startswith("EMA")]


class PercentileMinMax(BaseEstimator, TransformerMixin):
    """MinMax with the `lo`/`hi` percentiles of the fitted rows as bounds; values outside are clipped to
    [0, 1] at transform time only (the fit never sees the clipped values)."""

    def __init__(self, lo=1, hi=99):
        self.lo, self.hi = lo, hi

    def fit(self, X, y=None):
        self.low_, self.high_ = np.nanpercentile(X, [self.lo, self.hi], axis=0)
        self.span_ = np.where(self.high_ > self.low_, self.high_ - self.low_, 1.0)
        return self

    def transform(self, X):
        return np.clip((X - self.low_) / self.span_, 0.0, 1.0)


SCALERS = {"standard": StandardScaler, "robust": RobustScaler, "minmax": MinMaxScaler,
           "minmax_p1_99": PercentileMinMax}


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


@_quiet
def _ema_shape(B):
    """Kinetics: fast EMA (alpha 0.1) relative to slow EMA (alpha 0.001) of the same sensor, rising and decaying."""
    cols = []
    for fast, slow in (("EMAi0.1", "EMAi0.001"), ("EMAd0.1", "EMAd0.001")):
        cols.append(np.log1p(np.abs(B[:, :, KIND[fast]])) - np.log1p(np.abs(B[:, :, KIND[slow]])))
    return np.hstack(cols)


GROUPS = {
    # name: (function, output column names, source sensors per column, formula)
    "pn_l2": (_pn_l2, [f"{sname(j)}_pnl2_{k}" for k in ("DR", "absDR") for j in range(16)],
              lambda c: tuple(range(16)), "x_j / sqrt(sum_k x_k^2) over the 16 sensors, kinds DR and |DR|"),
    "pn_logmed": (_pn_logmed, [f"{sname(j)}_pnlogmed_absDR" for j in range(16)],
                  lambda c: tuple(range(16)), "slog(|DR|_j) - median_k slog(|DR|_k)"),
    "ema_shape": (_ema_shape, [f"{sname(j)}_emashape_{d}" for d in ("rise", "decay") for j in range(16)],
                  lambda c: (c % 16,), "log1p|EMA(alpha=0.1)| - log1p|EMA(alpha=0.001)|, rising and decaying"),
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
# Drift-sensitivity filter (Phase 5)
# --------------------------------------------------------------------------------------
def batch_eta2(X, y, batches):
    """Per feature: share of the variance, after removing the gas effect, that the batch explains.
    High = the feature drifts between batches. Scale-invariant, so it does not depend on the scaler."""
    resid = X - pd.DataFrame(X).groupby(y).transform("mean").to_numpy()
    total = (resid ** 2).sum(0)
    by_batch = pd.DataFrame(resid).groupby(np.asarray(batches)).transform("mean").to_numpy()
    return np.divide((by_batch ** 2).sum(0), total, out=np.zeros(X.shape[1]), where=total > 0)


class DriftFilter(BaseEstimator, TransformerMixin):
    """Drop the `drop_frac` most drift-sensitive columns (eta2 on the fitted rows, i.e. Train batches only).
    `owner[j]` is the single sensor column j was computed from (-1 if it mixes sensors); every sensor keeps at
    least `min_own` of its own columns, so no sensor disappears from the fault study."""

    def __init__(self, owner, drop_frac=0.1, min_own=2):
        self.owner, self.drop_frac, self.min_own = owner, drop_frac, min_own

    def fit(self, X, y, batches):
        owner = np.asarray(self.owner)
        self.eta2_ = batch_eta2(X, y, batches)
        order = np.argsort(-self.eta2_)                               # most drifting first
        dropped = set(order[:int(round(self.drop_frac * X.shape[1]))])
        for sensor in range(N_SENSORS):                               # give back the least drifting if too few remain
            own = [j for j in order[::-1] if owner[j] == sensor]
            missing = self.min_own - sum(j not in dropped for j in own)
            dropped -= set([j for j in own if j in dropped][:max(missing, 0)])
        self.support_ = np.array(sorted(set(range(X.shape[1])) - dropped))
        return self

    def transform(self, X):
        return X[:, self.support_]


# --------------------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------------------
def build_preprocessor(spec, fill_nan=False, iqr_k=1.5, seed=0):
    """spec: {clip: none|iqr, slog: bool, scaler: standard|robust|minmax|minmax_p1_99, groups: [...],
              select: none | {drop_frac, min_own}}"""
    builder = FeatureBuilder(spec["slog"], tuple(spec["groups"]))
    steps = [("clip", IQRClipper(iqr_k))] if spec["clip"] == "iqr" else []
    steps += [("build", builder), ("scale", SCALERS[spec["scaler"]]())]
    if spec["select"] != "none":
        owner = [s[0] if len(s) == 1 else -1 for s in builder.provenance()["sources"]]
        steps.append(("select", DriftFilter(owner, **spec["select"])))
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
