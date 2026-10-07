"""Feature-level fault simulation.

Faults act on the 8 extracted features of selected sensors. They are NOT
simulations of the raw resistance signal and NOT recorded real faults.
  dropout: selected samples -> NaN (reading missing)
  bias:    all samples -> x + sign * delta * std_train (per feature)
  stuck:   selected samples -> features of one reference reading from the same stream
"""
from dataclasses import dataclass, asdict
import zlib
import numpy as np
from .data import sensor_columns


@dataclass(frozen=True)
class Scenario:
    group: str            # e.g. "k1", "k2", "k4"
    sensors: tuple        # 0-based sensor indices
    fault: str            # dropout | bias | stuck
    severity: float       # fraction (dropout/stuck) or delta (bias)
    seed: int

    def to_dict(self):
        d = asdict(self); d["sensors"] = "-".join(str(s + 1) for s in self.sensors); return d


def robust_sigma(X):
    """Outlier-resistant scale of every feature: IQR / 1.349 (equals the std for normal data).
    Used as the Bias unit instead of the plain std, which a few corrupt records can inflate by orders of magnitude."""
    q1, q3 = np.nanpercentile(X, [25, 75], axis=0)
    iqr = q3 - q1
    return np.where(iqr > 0, iqr / 1.349, np.nanstd(X, axis=0))


def apply_fault(X, sc: Scenario, std_train):
    """Return a corrupted copy of raw-feature matrix X. std_train: per-feature std (Train only)."""
    key = zlib.crc32(repr((sc.group, sc.sensors, sc.fault, sc.severity)).encode())  # process-independent
    rng = np.random.default_rng([sc.seed, key])
    Xf = X.copy(); n = len(X)
    for s in sc.sensors:
        cols = sensor_columns(s)
        if sc.fault == "dropout":
            rows = rng.random(n) < sc.severity
            Xf[np.ix_(rows, cols)] = np.nan
        elif sc.fault == "bias":
            sign = rng.choice([-1.0, 1.0])
            Xf[:, cols] = Xf[:, cols] + sign * sc.severity * std_train[cols]
        elif sc.fault == "stuck":
            rows = rng.random(n) < sc.severity
            ref = rng.integers(n)
            Xf[np.ix_(rows, cols)] = X[ref, cols]
        else:
            raise ValueError(sc.fault)
    return Xf


def build_scenarios(cfg, groups):
    """groups: dict name -> list of sensor tuples. Same scenario list is used for every method."""
    out = []
    ft = cfg["faults"]["types"]
    sev = {"dropout": ft["dropout"]["fraction"], "bias": ft["bias"]["delta"],
           "stuck": ft["stuck"]["fraction"]}
    for gname, sets in groups.items():
        for sensors in sets:
            for fault, levels in sev.items():
                for lv in levels:
                    for seed in cfg["seeds"]["faults"]:
                        out.append(Scenario(gname, tuple(sensors), fault, float(lv), int(seed)))
    return out


def augment_with_faults(X, y, std_train, rng, copies=1):
    """Training-time augmentation: each copy gets one random sensor with a random fault."""
    Xs, ys = [X], [y]
    n = len(X)
    for _ in range(copies):
        Xa = X.copy()
        sensors = rng.integers(16, size=n)
        kinds = rng.integers(3, size=n)
        for i in range(n):
            cols = sensor_columns(sensors[i])
            if kinds[i] == 0:
                Xa[i, cols] = np.nan
            elif kinds[i] == 1:
                Xa[i, cols] += rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 3.0) * std_train[cols]
            else:
                Xa[i, cols] = X[rng.integers(n), cols]
        Xs.append(Xa); ys.append(y)
    return np.vstack(Xs), np.concatenate(ys)
