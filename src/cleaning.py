"""Data cleaning rule for physically invalid (corrupt) records.

Two different things must not be confused:
  * statistical outliers (IQR fences): real drift and strong responses. KEPT, by decision.
  * invalid values: records whose value is so far from the Train median that it cannot be a sensor
    response (e.g. |DR| of 31,165 where the median is ~4). These are corrupt records.

Rule (fixed, computed on Train only, deliberately far beyond any drift):
    a cell is invalid  if  |x - median_f| / MAD_f > threshold      (default threshold = 1000)
    a record is invalid if any of its 128 cells is invalid.
median_f and MAD_f (median absolute deviation, unscaled) are fitted on the Train rows of the protocol.
Features with MAD == 0 cannot be scored and are never flagged.

Use: the flagged Train records are dropped before anything is fitted. Evaluation rows (Validation,
reference folds, Test) are never dropped, only counted, because a corrupt record in operation is a
real fault the system has to survive.
"""
import numpy as np

DEFAULT_THRESHOLD = 1000.0


class InvalidValueRule:
    def __init__(self, threshold=DEFAULT_THRESHOLD):
        self.threshold = threshold

    def fit(self, X):
        self.median_ = np.median(X, axis=0)
        self.mad_ = np.median(np.abs(X - self.median_), axis=0)
        self.scorable_ = self.mad_ > 0
        return self

    def robust_z(self, X):
        """|x - median| / MAD per cell; 0 for features that cannot be scored."""
        z = np.zeros(X.shape)
        np.divide(np.abs(X - self.median_), self.mad_, out=z, where=self.scorable_)
        return z

    def cells(self, X):
        return self.robust_z(X) > self.threshold

    def records(self, X):
        return self.cells(X).any(axis=1)
