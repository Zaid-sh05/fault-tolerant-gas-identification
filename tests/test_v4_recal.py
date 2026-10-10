"""Leakage, row-identity and reproduction tests of v4 (decisions_log Q9 and R). The fitted v2 models and the v3 predictions are read
(read-only) from the main checkout named in configs/v4_recal.yaml; without them the tests are skipped."""
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

sys.path.insert(0, "scripts")
_cfg = yaml.safe_load(open("configs/v4_recal.yaml"))
MAIN = Path(_cfg["main_checkout"])
pytestmark = pytest.mark.skipif(not (MAIN / _cfg["v2_models"] / "b9_s4" / "fitted.joblib").exists(), reason="main-checkout models absent")
SEEDS = (0, 1, 2, 3, 4)


@pytest.fixture(scope="module")
def v4():
    import v4_recal
    return v4_recal


# ---- Part 1 (Q9) ------------------------------------------------------------------------------------------
def test_arm_e_is_the_b8_model_and_contains_no_batch_10_row(v4):
    from v2_recal import calib_rows
    Xtr, ytr, _, ev = v4.test_data()
    rows10 = {r.tobytes() for r in ev[10][0]}
    for s in SEEDS:
        f = v4.load_v2("b8", s)
        assert not any(r.tobytes() in rows10 for r in f["Xtr"])
        cal = calib_rows(ev[8][1], 10, s, 8)
        assert np.array_equal(f["Xtr"], np.vstack([Xtr, ev[8][0][cal]])) and np.array_equal(f["ytr"], np.r_[ytr, ev[8][1][cal]])


def test_part1_arms_are_scored_on_the_v3_rows(v4):
    from ft_v2_recal import keep_mask
    ev = v4.test_data()[3]
    for t in (9, 10):
        for s in SEEDS:
            assert np.array_equal(v4.test_rows(t, s), np.flatnonzero(keep_mask(ev[t][1], s, t)))


def test_v4_prediction_reproduces_the_v3_labels_of_arm_c(v4):
    ev = v4.test_data()[3]
    sids = [0, 1, 300, 700, 1080]
    got = v4.predict(v4.as_model(v4.load_v2("b9", 0)), ev[10][0], v4.test_stats(), v4.test_scenarios(), sids)
    ref = v4.load_v3_preds("c", 10, 0)
    for m in ("svm", "A"):
        assert np.array_equal(got[m], ref[m][sids]), m


def test_stale_v3_chunks_are_rejected(v4, tmp_path):
    import pickle
    (tmp_path / "c_b10_s0").mkdir()
    for f in sorted((v4.V3_PREDS / "c_b10_s0").glob("chunk_*.pkl")):
        p = pickle.load(open(f, "rb"))
        if f.name == "chunk_000.pkl":
            p = {**p, "model": str(Path("results/final_test_v2/test/b10_s0"))}         # written by the same-period model
        pickle.dump(p, open(tmp_path / "c_b10_s0" / f.name, "wb"))
    assert v4.load_v3_preds("c", 10, 0)["A"].shape[0] == 1081
    with pytest.raises(AssertionError):
        v4.load_v3_preds("c", 10, 0, root=tmp_path)


# ---- Part 2 (R): candidates, written before the candidate code (R5 / §4 of the v4 request) ------------------------
CANDS = ("W1", "W5", "W20", "C1", "C2", "S30", "S60")


def _probe(m, X):
    """Fingerprint of a fitted model: its SVM labels on X, support vectors, dual coefficients and detector thresholds."""
    from src.evaluate import fill_nan_zero
    import v4_recal
    return (v4_recal.classify(m, X), m["svm"].support_.copy(), m["svm"].dual_coef_.copy(), m["det"].tau_.copy())


def _same(a, b):
    return all(np.array_equal(x, y) for x, y in zip(a, b))


def _with_target(v4, monkeypatch, t, fn):
    """Re-point dev_data at a copy whose batch t is changed by fn(X, y) -> (X, y)."""
    Xtr, ytr, btr, ev = v4.dev_data()
    ev2 = dict(ev)
    ev2[t] = fn(*ev[t])
    monkeypatch.setattr(v4, "dev_data", lambda: (Xtr, ytr, btr, ev2))


def test_1_no_label_of_the_evaluated_batch_enters_any_candidate_fit(v4, monkeypatch):
    """The kept rows (hence H1/H2) depend on batch-t labels only through the removal of the arm-(b) calibration rows (identical rows
    across arms, decisions_log R1); that selection is held fixed here, so the test isolates labels entering a fit."""
    t, s = 7, 0
    X7 = v4.dev_data()[3][t][0]
    ref = {k: _probe(v4.build("dev", k, t, s)[0], X7) for k in CANDS}
    rows, halves = v4.dev_rows(t, s), v4.halves("dev", t, s)
    monkeypatch.setattr(v4, "dev_rows", lambda tt, ss: rows)
    monkeypatch.setattr(v4, "halves", lambda d, tt, ss: halves)
    rng = np.random.default_rng(0)
    _with_target(v4, monkeypatch, t, lambda X, y: (X, rng.permutation(np.r_[y[1:], y[:1]]) % 6 + 1))   # every label of batch 7 scrambled
    for k in CANDS:
        assert _same(_probe(v4.build("dev", k, t, s)[0], X7), ref[k]), k


def test_2_halves_are_disjoint_and_no_H2_row_enters_the_self_training_fit(v4, monkeypatch):
    for t in (6, 7):
        for s in SEEDS:
            h1, h2 = v4.halves("dev", t, s)
            assert not set(h1) & set(h2) and np.array_equal(np.sort(np.r_[h1, h2]), v4.dev_rows(t, s))
    t, s = 7, 1
    h1, h2 = v4.halves("dev", t, s)
    X7 = v4.dev_data()[3][t][0]
    ref = {k: v4.build("dev", k, t, s) for k in ("S30", "S60")}
    for k, (m, info) in ref.items():
        assert set(info["pseudo_rows"]) <= set(h1) and len(info["pseudo_rows"]) > 0
    rng = np.random.default_rng(1)

    def poison(X, y):
        X = X.copy()
        X[h2] = rng.normal(size=X[h2].shape) * 1e3                                    # H2 rows replaced by noise
        return X, y
    _with_target(v4, monkeypatch, t, poison)
    for k, (m, _) in ref.items():
        assert _same(_probe(v4.build("dev", k, t, s)[0], X7[h1]), _probe(m, X7[h1])), k


def test_3_compared_arms_are_scored_on_identical_rows(v4):
    for t in (6, 7):
        for s in SEEDS:
            keep, (h1, h2) = v4.dev_rows(t, s), v4.halves("dev", t, s)
            for k in CANDS:
                want = h2 if k.startswith("S") else keep
                assert np.array_equal(v4.comparison_rows("dev", k, t, s), want), (k, t, s)


@pytest.mark.skipif(not (Path("results/v4_recal/dev_scores.csv").exists() and Path("results/v4_recal/preds/dev").exists()), reason="dev tournament not run yet, or its gitignored predictions are absent")
def test_3b_saved_dev_scores_rescore_on_the_comparison_rows(v4):
    import pandas as pd
    from src.models import scores
    df = pd.read_csv("results/v4_recal/dev_scores.csv").set_index(["rows", "key", "target", "cal_seed", "method", "sid"])["f1"]
    for k, t, s, sid in (("S30", 7, 2, 0), ("S60", 6, 4, 300), ("W20", 7, 0, 100), ("C2", 6, 1, 480)):
        rows, y = v4.comparison_rows("dev", k, t, s), v4.dev_data()[3][t][1]
        kind = "H2" if k.startswith("S") else "keep"
        for arm in (k, "prev"):                                       # the candidate and its reference, on the same rows
            labels = v4.load_dev_preds(arm, t, s)["A"][sid]
            assert abs(scores(y[rows], labels[rows])["macro_f1"] - df[(kind, arm, t, s, "A", sid)]) < 1e-12, (k, arm)


def test_4_dev_steps_never_read_batches_8_to_10(v4, monkeypatch):
    import src.data as D
    seen, orig = [], D.load_batch
    monkeypatch.setattr(D, "load_batch", lambda path, b: (seen.append(b), orig(path, b))[1])
    v4.dev_data.cache_clear()
    try:
        Xtr, ytr, btr, ev = v4.dev_data()
        for k in ("W5", "C1", "S30"):
            m, _ = v4.build("dev", k, 7, 0)
            v4.predict(m, ev[7][0][:50], v4.dev_stats(), v4.dev_scenarios(), [0, 1])
    finally:
        v4.dev_data.cache_clear()
    assert seen and set(seen) <= {1, 2, 3, 4, 5, 6, 7}, sorted(set(seen))


def test_4b_the_test_run_executes_once(v4, monkeypatch, tmp_path):
    (tmp_path / "test").mkdir()
    (tmp_path / "test" / "RUN_STARTED").write_text("earlier run")
    monkeypatch.setattr(v4, "OUT", tmp_path)
    with pytest.raises(SystemExit, match="refusing"):
        v4.stage_test(1)


def test_5_drift_directions_use_only_train_and_past_calibration_rows(v4, monkeypatch):
    t, s = 7, 0
    m, info = v4.build("dev", "C2", t, s)
    X, y, g, _ = v4.train_set("dev", v4.MEMORY[t], s)
    Z = v4.standardize(m["pre"], X)
    assert np.allclose(np.abs(info["V"]), np.abs(v4.drift_directions(Z, y, g >= v4.CAL_GROUP, 2)))
    assert set(np.unique(g[g >= v4.CAL_GROUP])) == {v4.CAL_GROUP + b for b in v4.MEMORY[t]} and t not in v4.MEMORY[t]
    rng = np.random.default_rng(2)
    _with_target(v4, monkeypatch, t, lambda X, y: (X + rng.normal(size=X.shape) * 1e3, y))     # batch 7 replaced by noise
    m2, info2 = v4.build("dev", "C2", t, s)
    assert np.array_equal(info2["V"], info["V"])


def test_memory_sets_never_contain_the_target_and_test_memory_has_no_target_row(v4):
    Xtr, _, _, ev = v4.test_data()
    for t in (6, 7, 9, 10):
        assert all(b < t for b in v4.MEMORY[t]) and t not in v4.MEMORY[t]
    X, y, g, _ = v4.train_set("test", v4.MEMORY[10], 0)
    rows10 = {r.tobytes() for r in ev[10][0]}
    assert not any(r.tobytes() in rows10 for r in X) and set(np.unique(g[g >= v4.CAL_GROUP])) == {v4.CAL_GROUP + 8, v4.CAL_GROUP + 9}
