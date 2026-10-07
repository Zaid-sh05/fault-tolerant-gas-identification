"""Synthetic raw data shaped like the real batch files, shared by several test modules."""
import numpy as np

from src.data import N_FEATURES, sensor_columns


def make_raw(n=400, seed=0, shift=0.0):
    """Positive |DR|-like and EMA-like columns with a gas-dependent pattern, in the real layout."""
    rng = np.random.default_rng(seed)
    y = rng.integers(1, 7, size=n)
    X = np.empty((n, N_FEATURES))
    for s in range(16):
        c = sensor_columns(s)
        amp = 1.0 + 0.3 * y[:, None] + 0.1 * rng.normal(size=(n, 1)) + shift
        X[:, c[0]] = 1e4 * amp[:, 0]                                  # DR
        X[:, c[1]] = 1.5 + amp[:, 0] + 0.05 * rng.normal(size=n)      # |DR|
        for i in range(2, 5):
            X[:, c[i]] = amp[:, 0] * (i + 1) + 0.1 * rng.normal(size=n)       # EMAi
        for i in range(5, 8):
            X[:, c[i]] = -amp[:, 0] * (i - 3) + 0.1 * rng.normal(size=n)      # EMAd
    return X, y, np.tile([1, 2, 3, 4, 5, 6], n // 6 + 1)[:n]


def write_batches(raw_dir, shifted=(), n_per_batch=60):
    """batch1..7 are valid files (those in `shifted` get a level shift); batch8..10 are unparseable,
    so any attempt to read them raises."""
    raw_dir.mkdir(exist_ok=True)
    for bid in range(1, 11):
        if bid >= 8:
            (raw_dir / f"batch{bid}.dat").write_text("CORRUPT - must not be read")
            continue
        X, y, _ = make_raw(n_per_batch, seed=bid, shift=1.0 if bid in shifted else 0.0)
        lines = [f"{y[i]} " + " ".join(f"{j + 1}:{X[i, j]:.6f}" for j in range(N_FEATURES)) for i in range(len(X))]
        (raw_dir / f"batch{bid}.dat").write_text("\n".join(lines) + "\n")
