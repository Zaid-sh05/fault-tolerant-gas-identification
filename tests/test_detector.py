"""ReliabilityDetector on synthetic low-rank sensor data with replicate pairs."""
import numpy as np
import pytest
from sklearn.metrics import roc_auc_score

from src.data import sensor_columns
from src.detector import ReliabilityDetector


def make_data(n, seed):
    rng = np.random.default_rng(seed)
    loadings = np.random.default_rng(7)
    latent = rng.normal(size=(n, 3))
    X = np.empty((n, 128))
    for pair in range(8):
        base = latent @ loadings.normal(size=(3, 8))
        for s in (2 * pair, 2 * pair + 1):
            X[:, sensor_columns(s)] = base + 0.15 * rng.normal(size=(n, 8))
    return np.sign(X) * np.expm1(np.abs(X))                     # so that the signed-log space is the Gaussian one


X_TR, X_EV = make_data(1200, 0), make_data(600, 1)
BATCHES = np.tile([1, 2, 3, 4, 5, 6], 200)


@pytest.fixture(scope="module", params=["sensor", "median"])
def det(request):
    return ReliabilityDetector(request.param).fit(X_TR, BATCHES)


def test_alarm_rate_on_clean_rows_is_near_the_calibrated_five_percent(det):
    rate = det.flags(X_EV).mean()
    assert 0.02 < rate < 0.10


def test_a_bias_fault_is_detected_and_isolated(det):
    Xf = X_EV.copy()
    Xf[:, sensor_columns(5)] += 3.0
    ratio = det.ratio(Xf)
    faulty, healthy = ratio[:, 5], np.delete(ratio, 5, axis=1).ravel()
    y = np.r_[np.ones(len(faulty)), np.zeros(len(healthy))]
    assert roc_auc_score(y, np.r_[faulty, healthy]) > 0.95
    assert det.flags(Xf)[:, 5].mean() > 0.9


def test_a_missing_block_is_flagged_by_definition_and_does_not_break_other_sensors(det):
    Xf = X_EV.copy()
    Xf[:50, sensor_columns(2)] = np.nan
    flags, ratio = det.flags(Xf), det.ratio(Xf)
    assert flags[:50, 2].all() and np.isinf(ratio[:50, 2]).all()
    assert np.isfinite(np.delete(ratio, 2, axis=1)).all()


def test_fit_is_deterministic_and_uses_only_the_given_rows():
    a = ReliabilityDetector("sensor").fit(X_TR, BATCHES)
    b = ReliabilityDetector("sensor").fit(X_TR, BATCHES)
    assert np.array_equal(a.tau_, b.tau_) and np.array_equal(a.alpha_, b.alpha_)


def test_leave_pair_out_removes_the_twin_from_the_predictors():
    full = ReliabilityDetector("sensor").fit(X_TR, BATCHES)
    lpo = ReliabilityDetector("sensor", lpo=True).fit(X_TR, BATCHES)
    assert len(full.W_[0][0]) == 120 and len(lpo.W_[0][0]) == 112
    assert not set(sensor_columns(1)) & set(lpo.W_[0][0])


def test_block_prediction_excludes_unavailable_sensors():
    det = ReliabilityDetector("sensor").fit(X_TR, BATCHES)
    P, _ = det._weights(4, (6, 7))
    assert not set(sensor_columns(6)) & set(P) and not set(sensor_columns(4)) & set(P)
    Z = np.nan_to_num(det.to_z(X_EV))
    pred = det.block_prediction(Z, 4, (6, 7))
    assert pred.shape == (len(X_EV), 8)
