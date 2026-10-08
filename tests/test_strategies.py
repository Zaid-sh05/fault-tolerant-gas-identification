"""Strategies A/B/C on synthetic data."""
import numpy as np
import pytest
from sklearn.svm import SVC

from src.data import sensor_columns
from src.detector import ReliabilityDetector
from src.evaluate import fill_nan_zero
from src.fastsvm import fast_svm_predict
from src.preprocessing import fit_preprocessor
from src.strategies import CAP, StrategyKit, acted_sets, group_by_set
from synth import make_raw

SPEC = {"clip": "none", "slog": False, "scaler": "standard", "groups": [], "select": "none"}
X_TR, Y_TR, B_TR = make_raw(480, seed=0)
X_EV, Y_EV, _ = make_raw(120, seed=1)


@pytest.fixture(scope="module")
def kit(tmp_path_factory):
    pre = fit_preprocessor(SPEC, X_TR, Y_TR, B_TR)
    svm = SVC(kernel="rbf", C=10, gamma=0.01).fit(fill_nan_zero(pre.transform(X_TR)), Y_TR)
    det = ReliabilityDetector("sensor").fit(X_TR, B_TR % 6)
    return StrategyKit(pre, svm, X_TR, Y_TR, det, {"C": 10, "gamma": 0.01}, str(tmp_path_factory.mktemp("cache")))


def test_acted_sets_keep_the_highest_ratio_when_more_than_the_cap_are_flagged():
    ratio = np.array([[5.0, 4.0, 3.0, 2.0, 1.5, 9.0] + [0.1] * 10])
    flags = ratio > 1
    assert acted_sets(ratio, flags)[0] == (0, 1, 2, 5) and len(acted_sets(ratio, flags)[0]) == CAP
    assert acted_sets(np.array([[0.5] * 16]), np.array([[False] * 16]))[0] == ()


def test_reconstruction_changes_only_the_flagged_blocks(kit):
    Xf = X_EV.copy()
    Xf[:, sensor_columns(3)] += 50
    groups = {(3,): np.arange(60), (): np.arange(60, 120)}
    Xr = kit.reconstruct(Xf, groups, exclude_twin=False)
    other = [c for c in range(128) if c not in sensor_columns(3)]
    assert np.array_equal(Xr[:, other], Xf[:, other])
    assert np.isfinite(Xr[:60][:, sensor_columns(3)]).all()
    assert np.array_equal(Xr[60:][:, sensor_columns(3)], Xf[60:][:, sensor_columns(3)])
    assert not np.allclose(Xr[:60][:, sensor_columns(3)], Xf[:60][:, sensor_columns(3)])


def test_reconstruction_repairs_a_dropout_so_that_the_clean_svm_can_predict(kit):
    Xf = X_EV.copy()
    Xf[:, sensor_columns(5)] = np.nan
    sets = [(5,)] * len(Xf)
    y = kit.predict_A(Xf, sets, exclude_twin=True)
    assert len(y) == len(Xf) and set(y) <= set(range(1, 7))


def test_without_flags_A_and_B_equal_the_clean_svm(kit):
    clean = fast_svm_predict(kit.svm, fill_nan_zero(kit.pre.transform(X_EV)))
    sets = [()] * len(X_EV)
    assert np.array_equal(kit.predict_A(X_EV, sets, False), clean)
    assert np.array_equal(kit.predict_B(X_EV, sets), clean)


def test_B_trains_one_model_per_excluded_set_without_those_columns(kit):
    sets = [(2,)] * 60 + [(2, 7)] * 60
    y = kit.predict_B(X_EV, sets)
    assert len(y) == 120
    assert kit.reduced_model((2,)).n_features_in_ == 120 and kit.reduced_model((2, 7)).n_features_in_ == 112
    assert kit.reduced_model((2,)) is kit.reduced_model((2,))                      # cached
    assert not set(sensor_columns(2)) & set(kit.keep_columns((2, 7)))


def test_C_expert_weights_follow_reliability(kit):
    ratio = np.full((4, 16), 0.5)
    ratio[0, 0] = np.inf                       # sensor 0 missing -> expert 0 weight 0
    ratio[1, 3] = 4.0                          # sensor 3 moderately unreliable -> expert 1 weight 1/16
    w = StrategyKit.expert_weights(ratio)
    assert w[0, 0] == 0 and np.allclose(w[0, 1:], 1) and np.isclose(w[1, 1], 1 / 16) and np.allclose(w[2:], 1)


def test_C_combination_ignores_an_expert_with_zero_weight(kit):
    proba = kit.expert_proba(X_EV)
    assert proba.shape == (120, 8, 6)
    ratio = np.full((120, 16), 0.5)
    equal, weighted = kit.combine(proba, None), kit.combine(proba, ratio)
    assert np.array_equal(equal, weighted)                                          # nothing flagged: same as equal weights
    ratio[:, :2] = np.inf                                                           # kill expert 0
    manual = kit.experts()[0][1].classes_[np.argmax(proba[:, 1:, :].sum(1), axis=1)]
    assert np.array_equal(kit.combine(proba, ratio), manual)
