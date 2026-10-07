"""Preprocessing pipeline tests: fences, features, provenance (P4), no leakage (P2), baseline equivalence."""
import numpy as np
import pytest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.data import N_FEATURES, sensor_columns
from src.evaluate import fit_on_batches
from src.preprocessing import IQRClipper, fit_preprocessor, pipeline_provenance
from synth import make_raw, write_batches

BASELINE = {"clip": "none", "slog": False, "scaler": "standard", "groups": [], "select": "none"}
FULL = {"clip": "iqr", "slog": True, "scaler": "robust",
        "groups": ["pn_l2", "pn_logmed", "trans_ratio"],
        "select": {"corr_threshold": 0.95, "keep_frac": 0.75, "min_own": 2, "mi_neighbors": 3}}


def test_baseline_spec_equals_the_old_svm_pipeline():
    X, y, b = make_raw()
    Xv, *_ = make_raw(100, 1)
    Xv[:5, sensor_columns(2)] = np.nan                                # Dropout fault
    new = fit_preprocessor(BASELINE, X, y, b, fill_nan=True)
    old = make_pipeline(StandardScaler(), SimpleImputer(strategy="constant", fill_value=0.0)).fit(X)
    assert np.array_equal(new.transform(Xv), old.transform(Xv))


def test_iqr_clipper_uses_fitted_fences_only():
    X, *_ = make_raw()
    clip = IQRClipper(1.5).fit(X)
    probe = X[:3].copy()
    probe[0, 0] = 1e12
    probe[1, 1] = np.nan
    out = clip.transform(probe)
    assert out[0, 0] == clip.hi_[0] and np.isnan(out[1, 1])
    assert np.array_equal(out[2], probe[2]) or (out[2] <= clip.hi_).all()


@pytest.mark.parametrize("sensor", [0, 5, 15])
@pytest.mark.parametrize("fault", ["dropout", "bias"])
def test_fault_changes_only_features_traced_to_that_sensor(sensor, fault):
    """P4: a fault in one sensor may change an output column only if that sensor is among its sources."""
    X, y, b = make_raw()
    pipe = fit_preprocessor(FULL, X, y, b, fill_nan=False)
    prov = pipeline_provenance(pipe)
    Xf = X.copy()
    cols = sensor_columns(sensor)
    Xf[:, cols] = np.nan if fault == "dropout" else Xf[:, cols] + 3 * X.std(0)[cols]
    changed = ~np.isclose(pipe.transform(X), pipe.transform(Xf), equal_nan=True).all(axis=0)
    tag = f"S{sensor + 1:02d}"
    traced = prov["sources"].map(lambda s: tag in s.split("|")).to_numpy()
    assert changed.any() and not (changed & ~traced).any()


def test_provenance_covers_every_output_column_and_every_sensor():
    X, y, b = make_raw()
    pipe = fit_preprocessor(FULL, X, y, b)
    prov = pipeline_provenance(pipe)
    assert len(prov) == pipe.transform(X).shape[1]
    assert (prov["n_sources"] >= 1).all()
    own = prov[prov["n_sources"] == 1]["sources"].value_counts()
    assert all(own.get(f"S{s + 1:02d}", 0) >= 2 for s in range(16))      # no sensor was dropped


def test_selector_removes_near_duplicates():
    X, y, b = make_raw()
    pipe = fit_preprocessor({**BASELINE, "select": {"corr_threshold": 0.95, "keep_frac": 1.0,
                                                    "min_own": 2, "mi_neighbors": 3}}, X, y, b)
    assert pipe.transform(X).shape[1] < N_FEATURES


@pytest.mark.parametrize("spec", [BASELINE, FULL], ids=["baseline", "full"])
def test_pipeline_parameters_depend_on_train_batches_only(tmp_path, spec):
    """P2: changing batch 7 cannot change the fitted pipeline; changing a Train batch must."""
    probe, *_ = make_raw(50, seed=99)
    a, b, c = tmp_path / "a", tmp_path / "b", tmp_path / "c"
    write_batches(a)
    write_batches(b, shifted=(7,))
    write_batches(c, shifted=(6,))
    train = [1, 2, 3, 4, 5, 6]
    out_a = fit_on_batches(a, spec, train).transform(probe)
    out_b = fit_on_batches(b, spec, train).transform(probe)
    out_c = fit_on_batches(c, spec, train).transform(probe)
    assert np.array_equal(out_a, out_b)
    assert out_a.shape != out_c.shape or not np.allclose(out_a, out_c)   # selection may change the width
    # Test files are unparseable here, so any read of batches 8-10 would have raised.
