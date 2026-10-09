"""Leakage and row-identity tests of the previous-period recalibration (decisions_log Q5(1)). They read batches 8-10 through
configs/v3_prevbatch.yaml and the fitted v2 models (git-ignored); without those models they are skipped."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, "scripts")
V2 = Path("results/final_test_v2/test")
pytestmark = pytest.mark.skipif(not (V2 / "b9_s4" / "fitted.joblib").exists(), reason="fitted v2 models not present")

TARGETS, SEEDS = (9, 10), (0, 1, 2, 3, 4)


@pytest.fixture(scope="module")
def v3():
    import v3_prevbatch
    return v3_prevbatch


@pytest.fixture(scope="module")
def data(v3):
    return v3.load_data()


def test_arm_models_are_the_v2_models(v3):
    for t in TARGETS:
        for s in SEEDS:
            assert v3.model_dir("a", t, s) == V2 / "uncalibrated"
            assert v3.model_dir("b", t, s) == V2 / f"b{t}_s{s}"
            assert v3.model_dir("c", t, s) == V2 / f"b{t - 1}_s{s}"


def test_arm_c_training_rows_contain_no_row_of_the_target_batch(v3, data):
    from v2_recal import calib_rows
    Xtr, ytr, _, evals = data
    for t in TARGETS:
        Xt = evals[t][0]
        target_rows = {r.tobytes() for r in Xt}
        Xp, yp = evals[t - 1]
        for s in SEEDS:
            f = v3.load_fitted("c", t, s)
            assert not any(r.tobytes() in target_rows for r in f["Xtr"]), f"batch {t} row in the arm (c) training data, seed {s}"
            cal = calib_rows(yp, 10, s, t - 1)
            assert np.array_equal(f["Xtr"], np.vstack([Xtr, Xp[cal]])) and np.array_equal(f["ytr"], np.r_[ytr, yp[cal]])


def test_scored_rows_are_identical_across_arms(v3, data):
    from ft_v2_recal import keep_mask
    evals = data[3]
    for t in TARGETS:
        y = evals[t][1]
        for s in SEEDS:
            ref = np.flatnonzero(keep_mask(y, s, t))
            for arm in ("a", "b", "c"):
                assert np.array_equal(v3.scored_rows(arm, t, s, y), ref), (arm, t, s)
            assert len(ref) == len(y) - 60


@pytest.mark.skipif(not Path("results/v3_prevbatch/scores.csv").exists(), reason="scores.csv not computed yet")
def test_saved_scores_of_every_arm_use_the_shared_scored_rows(v3, data):
    """Rescore saved labels on keep_mask rows; an arm scored on other rows would not reproduce its scores.csv value."""
    import pandas as pd
    from ft_v2_recal import keep_mask
    from src.models import scores
    evals = data[3]
    df = pd.read_csv("results/v3_prevbatch/scores.csv").set_index(["subset", "cal_seed", "arm", "method", "sid"])["f1"]
    for t, s, sid in ((9, 3, 0), (9, 1, 700), (10, 4, 0), (10, 2, 1000)):
        y = evals[t][1]
        keep = keep_mask(y, s, t)
        for arm in ("a", "b", "c"):
            labels = v3.load_preds(arm, t, s)["A"][sid]
            assert abs(scores(y[keep], labels[keep])["macro_f1"] - df[(f"b{t}", s, arm, "A", sid)]) < 1e-12, (arm, t, s, sid)


def test_chunks_from_another_model_are_rejected(v3, tmp_path, monkeypatch):
    import pickle
    good = pickle.load(open(v3.pred_dir("c", 9, 0) / "chunk_000.pkl", "rb"))
    d = tmp_path / "c_b9_s0"
    d.mkdir()
    for i, _ in v3.chunks():
        src = pickle.load(open(v3.pred_dir("c", 9, 0) / f"chunk_{i:03d}.pkl", "rb"))
        if i == 0:
            src = {**good, "model": str(v3.model_dir("b", 9, 0))}                     # a stale chunk written by the same-period model
        pickle.dump(src, open(d / f"chunk_{i:03d}.pkl", "wb"))
    monkeypatch.setattr(v3, "pred_dir", lambda arm, t, s: d)
    with pytest.raises(AssertionError):
        v3.load_preds("c", 9, 0)


def test_arm_c_detector_is_the_stored_t_minus_1_detector_and_never_refit(v3, data, monkeypatch, tmp_path):
    from src.detector import ReliabilityDetector
    from v2_recal import CAL_GROUP, calib_rows
    evals = data[3]
    for t in TARGETS:
        for s in SEEDS:
            det = v3.load_fitted("c", t, s)["det"]
            assert CAL_GROUP + t - 1 in det.batch_ids_ and CAL_GROUP + t not in det.batch_ids_
            assert det.nb_[CAL_GROUP + t - 1] == len(calib_rows(evals[t - 1][1], 10, s, t - 1))

    def no_fit(*_a, **_k):
        raise AssertionError("detector refitted")
    monkeypatch.setattr(ReliabilityDetector, "fit", no_fit)
    f = v3.load_fitted("c", 9, 0)
    tau = f["det"].tau_.copy()
    preds = v3.predict_scenarios(f, tmp_path / "b8_s0" / "reduced", evals[9][0], data[0], [0, 1])   # temporary cache, not the run's
    assert np.array_equal(f["det"].tau_, tau)
    assert set(preds) == {"svm", "A", "B"} and preds["A"].shape == (2, len(evals[9][1]))
