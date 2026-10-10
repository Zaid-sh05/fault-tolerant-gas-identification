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
