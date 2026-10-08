"""Fault scenarios on whole sensor blocks (8 features) of the evaluation rows.

Registered in results/decisions_log.md (section B3). Faults are injected on the RAW 128 features of a clean copy of the
evaluation rows, AFTER the split, and every method receives exactly the same faulted matrix (the hash of each faulted
matrix is stored in the scenario table so that identical application can be verified).

  dropout : block -> NaN on the affected rows
  bias    : block + sign * delta * sigma_robust on ALL rows; one random sign per scenario, shared by the sensors of the set
  stuck   : block frozen to the values of ONE random evaluation row (per scenario) on the affected rows
  random  : block replaced by independent uniform draws in [p1, p99] of the cleaned Train feature on the affected rows
shared_rows = true: the affected rows are drawn once per scenario and are the same for every sensor of the set.

`truth` (n_rows x 16, bool) says which sensor is really faulty in which row; only the Oracle strategies and the detector
metrics may look at it.
"""
import hashlib
import zlib
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import sensor_columns

SENSOR_SETS = {
    "k1": [(s,) for s in range(16)],
    "k2": [(2 * p, 2 * p + 1) for p in range(8)],                                    # replicate pairs
    "k4": [(0, 1, 8, 9), (2, 3, 10, 11), (4, 5, 12, 13), (6, 7, 14, 15)],            # candidate groups (hypothesis)
}
LEVELS = {"dropout": [0.5, 1.0], "bias": [0.5, 1.0, 3.0], "stuck": [0.5, 1.0], "random": [0.5, 1.0]}
MEDIUM = {"dropout": 0.5, "bias": 1.0, "stuck": 0.5, "random": 0.5}
FAULTS = tuple(LEVELS)


@dataclass(frozen=True)
class Scenario:
    sid: int
    kset: str
    sensors: tuple
    fault: str
    level: float
    seed: int


@dataclass
class FaultStats:
    """Fitted on the cleaned Train rows."""
    sigma: np.ndarray        # robust scale IQR / 1.349 of every feature (Bias unit)
    p1: np.ndarray
    p99: np.ndarray

    @classmethod
    def fit(cls, X_train):
        q1, q3 = np.nanpercentile(X_train, [25, 75], axis=0)
        iqr = q3 - q1
        sigma = np.where(iqr > 0, iqr / 1.349, np.nanstd(X_train, axis=0))
        p1, p99 = np.nanpercentile(X_train, [1, 99], axis=0)
        return cls(sigma, p1, p99)


def build_scenarios(seeds, ksets=("k1", "k2", "k4"), reduced=False):
    """Deterministic scenario list. reduced=True: medium severity only (used for the reference protocol)."""
    out = []
    for kset in ksets:
        for sensors in SENSOR_SETS[kset]:
            for fault in FAULTS:
                for level in ([MEDIUM[fault]] if reduced else LEVELS[fault]):
                    for seed in seeds:
                        out.append(Scenario(len(out), kset, tuple(sensors), fault, float(level), int(seed)))
    return out


def _rng(sc):
    key = zlib.crc32(repr((sc.kset, sc.sensors, sc.fault, sc.level)).encode())      # process independent
    return np.random.default_rng([sc.seed, key])


def apply_scenario(X, sc, stats):
    """Return (X_faulted, truth) for a clean evaluation matrix X (not modified)."""
    rng, n = _rng(sc), len(X)
    Xf = X.copy()
    cols = [sensor_columns(s) for s in sc.sensors]
    if sc.fault == "bias":
        rows = np.ones(n, dtype=bool)
        sign = rng.choice([-1.0, 1.0])
        for c in cols:
            Xf[:, c] = X[:, c] + sign * sc.level * stats.sigma[c]
    else:
        rows = rng.random(n) < sc.level                                  # level 1.0 -> every row
        if sc.fault == "stuck":
            ref = rng.integers(n)
        for c in cols:
            if sc.fault == "dropout":
                Xf[np.ix_(rows, c)] = np.nan
            elif sc.fault == "stuck":
                Xf[np.ix_(rows, c)] = X[ref, c]
            elif sc.fault == "random":
                Xf[np.ix_(rows, c)] = stats.p1[c] + rng.random((int(rows.sum()), len(c))) * (stats.p99[c] - stats.p1[c])
            else:
                raise ValueError(sc.fault)
    truth = np.zeros((n, 16), dtype=bool)
    truth[np.ix_(rows, list(sc.sensors))] = True
    return Xf, truth


def matrix_hash(Xf):
    return hashlib.blake2b(np.ascontiguousarray(np.nan_to_num(Xf, nan=-1.2345e30)).tobytes(), digest_size=8).hexdigest()


def scenario_table(scenarios, X, stats):
    """One row per scenario with the hash of its faulted matrix, and the packed truth masks."""
    rows, masks = [], []
    for sc in scenarios:
        Xf, truth = apply_scenario(X, sc, stats)
        rows.append({"sid": sc.sid, "kset": sc.kset, "sensors": "-".join(f"{s + 1}" for s in sc.sensors), "fault": sc.fault,
                     "level": sc.level, "seed": sc.seed, "rows_affected": int(truth.any(1).sum()), "hash": matrix_hash(Xf)})
        masks.append(np.packbits(truth, axis=None))
    return pd.DataFrame(rows), np.stack(masks)
