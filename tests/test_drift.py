import numpy as np

from src.drift import BatchEnsemble, BatchRobustNorm, Coral


def test_batch_norm_removes_a_whole_batch_shift_and_keeps_nan():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(300, 4))
    norm = BatchRobustNorm().fit(X, np.zeros(300))
    Xs = X + np.array([5.0, 0, 0, -2.0])
    Xs[0, 1] = np.nan
    out = norm.transform(Xs)
    assert np.isnan(out[0, 1])
    np.testing.assert_allclose(out[:, [0, 3]], norm.transform(X)[:, [0, 3]])


def test_batch_norm_constant_feature_is_only_shifted():
    X = np.random.default_rng(1).normal(size=(100, 2))
    norm = BatchRobustNorm().fit(X, np.zeros(100))
    Xc = X.copy()
    Xc[:, 0] = 7.0
    assert np.isfinite(norm.transform(Xc)).all()


def test_coral_is_identity_when_the_covariances_match():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(5000, 3)) @ np.array([[1, 0.5, 0], [0, 1, 0.3], [0, 0, 2.0]])
    coral = Coral().fit(X, np.zeros(len(X)))
    np.testing.assert_allclose(coral.transform(X), X, atol=1e-8)


def test_coral_moves_the_target_covariance_towards_train():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(4000, 3))
    T = rng.normal(size=(4000, 3)) * np.array([3.0, 0.2, 1.0])
    coral = Coral().fit(X, np.zeros(len(X)))
    std = lambda A: (A - coral.mu_) / coral.sd_
    cs = np.cov(std(X), rowvar=False)
    gap = lambda A: np.linalg.norm(np.cov(std(A), rowvar=False) - cs)
    assert gap(coral.transform(T)) < 0.5 * gap(T)


def test_ensemble_weights_and_votes():
    rng = np.random.default_rng(4)
    y = np.tile([1, 2, 3], 40)
    Z = rng.normal(size=(120, 2)) + y[:, None] * 2.0
    batches = np.repeat([1, 2], 60)
    ens = BatchEnsemble({"C": 10, "gamma": 0.5}).fit(Z, y, batches)
    assert len(ens.weights_) == 2 and all(0 <= w <= 1 for w in ens.weights_)
    assert (ens.predict(Z) == y).mean() > 0.9
