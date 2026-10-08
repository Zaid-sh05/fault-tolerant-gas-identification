"""fast_svm_predict must return exactly the labels of SVC.predict."""
import numpy as np
import pytest
from sklearn.svm import SVC

from src.fastsvm import fast_svm_predict


@pytest.mark.parametrize("gamma", ["scale", 0.01, 0.5])
def test_matches_sklearn_predict_on_six_classes(gamma):
    rng = np.random.default_rng(0)
    centers = rng.normal(size=(6, 20)) * 2.0
    y = rng.integers(1, 7, size=900)
    X = centers[y - 1] + rng.normal(size=(900, 20))
    model = SVC(kernel="rbf", C=10, gamma=gamma).fit(X[:600], y[:600])
    Xt = X[600:] + rng.normal(size=(300, 20)) * 0.5
    assert np.array_equal(fast_svm_predict(model, Xt), model.predict(Xt))
    assert np.array_equal(fast_svm_predict(model, X[:100]), model.predict(X[:100]))


@pytest.mark.parametrize("n_class", [2, 3, 5])
@pytest.mark.parametrize("labels_offset", [0, 4])
def test_matches_sklearn_predict_for_few_classes(n_class, labels_offset):
    """Two classes was wrong before (sklearn flips the binary sign); unordered labels check the classes_ mapping."""
    rng = np.random.default_rng(n_class)
    centers = rng.normal(size=(n_class, 5)) * 1.5
    k = rng.integers(0, n_class, size=600)
    X = centers[k] + rng.normal(size=(600, 5))
    y = np.array([7, 3, 9, 1, 5])[k] + labels_offset
    model = SVC(kernel="rbf", C=10, gamma=0.3).fit(X[:400], y[:400])
    assert np.array_equal(fast_svm_predict(model, X[400:]), model.predict(X[400:]))
    assert np.array_equal(fast_svm_predict(model, X[:400]), model.predict(X[:400]))
