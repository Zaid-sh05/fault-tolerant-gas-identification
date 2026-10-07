"""Loading and naming for the UCI Gas Sensor Array Drift Dataset (UCI #224).

File format of the downloaded batchN.dat files, one record per line:
  "<gas_class> 1:<f1> 2:<f2> ... 128:<f128>"
(an optional ";<concentration>" after the class is tolerated and ignored; the
files we downloaded do not contain it.)

Feature order (documented on UCI dataset 270): sensor-major blocks of 8:
  DR_j, |DR|_j, EMAi0.001_j, EMAi0.01_j, EMAi0.1_j, EMAd0.001_j, EMAd0.01_j, EMAd0.1_j, j = 1..16
The mapping sensor index -> sensor type (TGS2600/2602/2610/2620) is NOT given
in the dataset documentation.

Leakage rule: callers pass the batch ids they are allowed to see. Batches that
are not requested are never opened (tests/test_data.py proves it).
"""
from pathlib import Path

import numpy as np
import pandas as pd

N_SENSORS = 16
N_FEAT_PER_SENSOR = 8
N_FEATURES = N_SENSORS * N_FEAT_PER_SENSOR
FEATURE_KINDS = ["DR", "absDR", "EMAi0.001", "EMAi0.01", "EMAi0.1",
                 "EMAd0.001", "EMAd0.01", "EMAd0.1"]
GAS_NAMES = {1: "Ethanol", 2: "Ethylene", 3: "Ammonia",
             4: "Acetaldehyde", 5: "Acetone", 6: "Toluene"}
FEATURES = [f"S{s + 1:02d}_{k}" for s in range(N_SENSORS) for k in FEATURE_KINDS]


def sensor_columns(sensor_idx):
    """0-based sensor index -> 0-based column indices of its 8 features."""
    start = sensor_idx * N_FEAT_PER_SENSOR
    return list(range(start, start + N_FEAT_PER_SENSOR))


def _parse_line(line, where):
    """Parse one record; raise ValueError (with file:line) on anything unexpected."""
    head, *pairs = line.split()
    gas = int(head.split(";")[0])
    if gas not in GAS_NAMES:
        raise ValueError(f"{where}: unknown gas class {gas}")
    if len(pairs) != N_FEATURES:
        raise ValueError(f"{where}: expected {N_FEATURES} features, got {len(pairs)}")
    keys, _, vals = zip(*(p.partition(":") for p in pairs))
    if [int(k) for k in keys] != list(range(1, N_FEATURES + 1)):
        raise ValueError(f"{where}: feature indices are not 1..{N_FEATURES} in order")
    x = np.array(vals, dtype=float)
    if not np.isfinite(x).all():
        raise ValueError(f"{where}: non-finite feature value")
    return gas, x


def load_batch(path, batch_id):
    path = Path(path)
    parsed = [_parse_line(line, f"{path.name}:{i + 1}")
              for i, line in enumerate(path.read_text().splitlines()) if line.strip()]
    df = pd.DataFrame(np.vstack([x for _, x in parsed]), columns=FEATURES)
    df.insert(0, "gas", [g for g, _ in parsed])
    df.insert(1, "batch", batch_id)
    return df


def load_batches(raw_dir, batches):
    """Load ONLY the requested batches (ids 1..10), stacked in batch order."""
    return pd.concat([load_batch(Path(raw_dir) / f"batch{b}.dat", b) for b in sorted(batches)],
                     ignore_index=True)


def split_by_batches(df, batches):
    return df[df["batch"].isin(batches)].reset_index(drop=True)


def xy(df):
    return df[FEATURES].to_numpy(dtype=float), df["gas"].to_numpy(dtype=int)
