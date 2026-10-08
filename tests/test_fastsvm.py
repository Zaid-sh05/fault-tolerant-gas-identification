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
