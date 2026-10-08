"""Fast prediction for a fitted RBF SVC: kernel values by BLAS, then libsvm's one-vs-one voting.

SVC.predict evaluates the kernel one support vector at a time; for thousands of fault scenarios that dominates the run
time. This function returns the same labels (tests/test_fastsvm.py checks it against SVC.predict).
"""
import numpy as np
from sklearn.metrics.pairwise import rbf_kernel


def fast_svm_predict(model, X):
    assert model.kernel == "rbf"
    K = rbf_kernel(X, model.support_vectors_, gamma=model._gamma)
    n_class = len(model.classes_)
    assert n_class >= 2, "an SVC needs at least two classes"
    if n_class == 2:
        # sklearn stores the binary dual_coef_/intercept_ with the sign flipped relative to libsvm: classes_[1] when f >= 0
        f = K @ model.dual_coef_[0] + model.intercept_[0]
        return model.classes_[(f >= 0).astype(int)]
    starts = np.r_[0, np.cumsum(model.n_support_)]
    votes = np.zeros((len(X), n_class))
    p = 0
    for i in range(n_class):
        for j in range(i + 1, n_class):
            si, sj = slice(starts[i], starts[i + 1]), slice(starts[j], starts[j + 1])
            f = K[:, si] @ model.dual_coef_[j - 1, si] + K[:, sj] @ model.dual_coef_[i, sj] + model.intercept_[p]
            votes[f > 0, i] += 1
            votes[f <= 0, j] += 1
            p += 1
    return model.classes_[np.argmax(votes, axis=1)]
