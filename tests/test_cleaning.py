"""The invalid-value rule: |x - median| / MAD > 1000, fitted on Train, far beyond any drift."""
import numpy as np

from src.cleaning import InvalidValueRule
from src.splits import get_protocol_data
from synth import make_raw, write_batches


def train_matrix():
    return make_raw(500, seed=0)[0]


def test_flags_only_the_corrupt_record():
    X = train_matrix()
    probe = make_raw(50, seed=1)[0]
    probe[7, 5] = 1e9                                        # impossible value in one cell
    rule = InvalidValueRule().fit(X)
    assert rule.records(probe).tolist() == [i == 7 for i in range(50)]
    assert rule.cells(probe).sum() == 1


def test_does_not_flag_strong_drift_or_a_large_response():
    X = train_matrix()
    rule = InvalidValueRule().fit(X)
    mad = rule.mad_
    drifted = X[:20] + 50 * mad                              # a 50-MAD shift of every feature
    assert not rule.records(drifted).any()
    assert not rule.records(X).any()                         # nothing in the fitted data itself


def test_threshold_is_1000_mads():
    X = train_matrix()
    rule = InvalidValueRule().fit(X)
    probe = X[:2].copy()
    probe[0, 3] = rule.median_[3] + 999 * rule.mad_[3]
    probe[1, 3] = rule.median_[3] + 1001 * rule.mad_[3]
    assert rule.records(probe).tolist() == [False, True]


def test_fit_uses_only_the_rows_it_is_given():
    X = train_matrix()
    a = InvalidValueRule().fit(X)
    b = InvalidValueRule().fit(np.vstack([X, np.full((5, 128), 1e9)]))   # contaminated "evaluation" rows
    assert not np.array_equal(a.mad_, b.mad_)                # the statistics do follow the rows given to fit
    c = InvalidValueRule().fit(X)
    assert np.array_equal(a.median_, c.median_) and np.array_equal(a.mad_, c.mad_)   # deterministic


def test_features_with_zero_mad_are_never_flagged():
    X = train_matrix()
    X[:, 4] = 3.0                                            # constant feature: MAD = 0
    rule = InvalidValueRule().fit(X)
    probe = X[:3].copy()
    probe[0, 4] = 1e9
    assert not rule.scorable_[4] and not rule.cells(probe)[:, 4].any()


def _protocol_cfg(raw_dir):
    return {"data": {"raw_dir": str(raw_dir)},
            "split": {"train_batches": [1, 2, 3, 4, 5, 6], "val_batches": [7],
                      "inner_folds": [[1], [2], [3], [4, 5], [6]]},
            "cleaning": {"invalid_value_rule": {"threshold": 1000}}}


def _corrupt_one_record(raw_dir, batch):
    path = raw_dir / f"batch{batch}.dat"
    lines = path.read_text().splitlines()
    head, *pairs = lines[3].split()
    pairs[10] = "11:999999999.0"
    lines[3] = " ".join([head] + pairs)
    path.write_text("\n".join(lines) + "\n")


def test_protocol_drops_corrupt_train_rows_but_keeps_corrupt_evaluation_rows(tmp_path):
    write_batches(tmp_path, n_per_batch=100)
    _corrupt_one_record(tmp_path, 3)                         # a Train batch
    _corrupt_one_record(tmp_path, 7)                         # the Validation batch
    p = get_protocol_data(_protocol_cfg(tmp_path))
    assert len(p.train) == 6 * 100 - 1 and len(p.eval) == 100            # Train loses one, evaluation keeps all
    assert p.dropped_train[["batch", "line"]].values.tolist() == [[3, 4]]
    assert p.flagged_eval[["batch", "line"]].values.tolist() == [[7, 4]]
    assert (p.eval[["batch", "line"]].values == [7, 4]).all(1).any()      # the corrupt row is still there


def test_without_a_cleaning_block_nothing_is_dropped(tmp_path):
    write_batches(tmp_path, n_per_batch=100)
    _corrupt_one_record(tmp_path, 3)
    cfg = _protocol_cfg(tmp_path)
    del cfg["cleaning"]
    p = get_protocol_data(cfg)
    assert len(p.train) == 600 and len(p.dropped_train) == 0
