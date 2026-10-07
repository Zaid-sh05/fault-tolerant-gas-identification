"""BlockImputer on synthetic low-rank data with replicate pairs (no real data needed)."""
import numpy as np
import pytest

from src.data import sensor_columns
from src.imputation import METHODS, BlockImputer, block_errors, twin_of


def make_data(n=500, seed=0):
    """3 shared latent factors drive every sensor; each replicate pair (2p, 2p+1) also shares a
    pair-specific factor that no other sensor sees, so the twin carries unique information."""
    rng = np.random.default_rng(seed)
    loadings = np.random.default_rng(123)          # same sensor physics for Train and Val
    latent = rng.normal(size=(n, 3))
    X = np.empty((n, 128))
    for pair in range(8):
        base = latent @ loadings.normal(size=(3, 8)) + rng.normal(size=(n, 2)) @ loadings.normal(size=(2, 8))
        for s in (2 * pair, 2 * pair + 1):
            X[:, sensor_columns(s)] = base + 0.05 * rng.normal(size=(n, 8))
    return X


X_TRAIN, X_VAL = make_data(600, 0), make_data(300, 1)
BATCHES = np.tile([1, 2, 3, 4, 5, 6], 100)
FOLDS = [(1,), (2,), (3,), (4, 5), (6,)]


def fitted(method, **kw):
    return BlockImputer(method, iterative={"max_iter": 3, "mask_fraction": 0.5}, **kw).fit(X_TRAIN, BATCHES)


def r2(imp, sensor, exclude_twin):
    Xh = imp.reconstruct(X_VAL, sensor, exclude_twin, FOLDS)
    return block_errors(X_VAL, Xh, X_TRAIN.mean(0), X_TRAIN.std(0), sensor)["r2"].mean()


@pytest.mark.parametrize("method", METHODS)
def test_only_target_block_changes(method):
    Xh = fitted(method).reconstruct(X_VAL, 3, False, FOLDS)
    other = [c for c in range(128) if c not in sensor_columns(3)]
    assert np.array_equal(Xh[:, other], X_VAL[:, other])
    assert not np.allclose(Xh[:, sensor_columns(3)], X_VAL[:, sensor_columns(3)])


@pytest.mark.parametrize("method", METHODS)
def test_output_does_not_depend_on_the_block_being_rebuilt(method):
    imp = fitted(method)
    corrupted = X_VAL.copy()
    corrupted[:, sensor_columns(5)] = 1e6
    a = imp.reconstruct(X_VAL, 5, False, FOLDS)[:, sensor_columns(5)]
    b = imp.reconstruct(corrupted, 5, False, FOLDS)[:, sensor_columns(5)]
    assert np.allclose(a, b)


def test_mean_and_median_use_train_statistics():
    cols = sensor_columns(0)
    assert np.allclose(fitted("mean").reconstruct(X_VAL, 0)[:, cols], X_TRAIN[:, cols].mean(0))
    assert np.allclose(fitted("median").reconstruct(X_VAL, 0)[:, cols], np.median(X_TRAIN[:, cols], axis=0))


@pytest.mark.parametrize("method", ["ridge", "knn", "iterative"])
def test_models_beat_the_mean_when_structure_exists(method):
    # kNN is a weak regressor on continuous low-rank data, hence the modest absolute bar
    assert r2(fitted(method), 4, False) > 0.5 > r2(fitted("mean"), 4, False)


@pytest.mark.parametrize("method", ["ridge", "knn", "iterative"])
def test_leave_pair_out_is_harder_when_the_twin_is_informative(method):
    imp = fitted(method)
    assert twin_of(4) == 5
    assert r2(imp, 4, True) < r2(imp, 4, False) - 0.05


@pytest.mark.parametrize("exclude_twin", [False, True])
def test_fast_knn_equals_sklearn_knnimputer(exclude_twin):
    imp = fitted("knn")
    cols = sensor_columns(6)
    fast = imp.reconstruct(X_VAL, 6, exclude_twin)[:, cols]
    Z = imp._to_z(X_VAL)
    Z[:, cols] = imp._knn_general(Z, 6, exclude_twin)        # sklearn KNNImputer path
    assert np.allclose(fast, imp._from_z(Z)[:, cols])


def test_iterative_stays_inside_the_train_range():
    imp = fitted("iterative")
    Xh = imp.reconstruct(X_VAL, 2, True, FOLDS)[:, sensor_columns(2)]
    cols = sensor_columns(2)
    assert (Xh >= X_TRAIN[:, cols].min(0) - 1e-9).all() and (Xh <= X_TRAIN[:, cols].max(0) + 1e-9).all()


def test_slog_space_round_trips():
    imp = BlockImputer("median", space="slog").fit(np.abs(X_TRAIN) + 1, BATCHES)
    Z = imp._to_z(np.abs(X_VAL) + 1)
    assert np.allclose(imp._from_z(Z), np.abs(X_VAL) + 1)
