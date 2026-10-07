"""Loader tests on tiny synthetic files; no real data needed."""
import numpy as np
import pytest

from src.data import N_FEATURES, load_batch, load_batches


def _line(gas, x, head_suffix=""):
    return f"{gas}{head_suffix} " + " ".join(f"{i + 1}:{v:.6f}" for i, v in enumerate(x))


def _write(path, n=3, seed=0):
    x = np.random.default_rng(seed).normal(size=(n, N_FEATURES))
    path.write_text("\n".join(_line(1 + i % 6, x[i]) for i in range(n)) + "\n")
    return x


def test_roundtrip_values_and_labels(tmp_path):
    x = _write(tmp_path / "batch1.dat", n=4)
    df = load_batch(tmp_path / "batch1.dat", 1)
    assert df.shape == (4, 3 + N_FEATURES)
    assert df["gas"].tolist() == [1, 2, 3, 4]
    assert np.allclose(df.iloc[:, 3:].to_numpy(), x, atol=1e-6)


def test_optional_concentration_is_ignored(tmp_path):
    x = np.zeros(N_FEATURES)
    (tmp_path / "batch1.dat").write_text(_line(2, x, ";10.000000") + "\n")
    assert load_batch(tmp_path / "batch1.dat", 1)["gas"].tolist() == [2]


@pytest.mark.parametrize("bad", [
    "9 " + " ".join(f"{i + 1}:0" for i in range(N_FEATURES)),        # unknown gas class
    "1 " + " ".join(f"{i + 1}:0" for i in range(N_FEATURES - 1)),    # missing feature
    "1 " + " ".join(f"{i + 2}:0" for i in range(N_FEATURES)),        # wrong feature indices
    "1 " + " ".join(f"{i + 1}:nan" for i in range(N_FEATURES)),      # non-finite value
])
def test_malformed_record_is_rejected(tmp_path, bad):
    (tmp_path / "batch1.dat").write_text(bad + "\n")
    with pytest.raises(ValueError):
        load_batch(tmp_path / "batch1.dat", 1)


def test_unrequested_batches_are_never_opened(tmp_path):
    """Leakage guard: Test files are unparseable garbage, so any read would raise."""
    for b in range(1, 8):
        _write(tmp_path / f"batch{b}.dat", n=2, seed=b)
    for b in (8, 9, 10):
        (tmp_path / f"batch{b}.dat").write_text("CORRUPT - must not be read")
    df = load_batches(tmp_path, [1, 2, 3, 4, 5, 6, 7])
    assert sorted(df["batch"].unique()) == [1, 2, 3, 4, 5, 6, 7]
    with pytest.raises(ValueError):
        load_batches(tmp_path, [7, 8])
