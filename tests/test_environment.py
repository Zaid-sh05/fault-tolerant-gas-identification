"""Step 0 smoke test: the pinned versions that produced the reference numbers are installed."""
import sys

import lightgbm
import sklearn


def test_python_311():
    assert sys.version_info[:2] == (3, 11)


def test_pinned_ml_versions():
    assert sklearn.__version__ == "1.8.0"
    assert lightgbm.__version__ == "4.7.0"
