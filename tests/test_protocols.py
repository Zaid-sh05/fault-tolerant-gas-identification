"""Evaluation protocols: reference_iid must never read batches 8-10 and must split cleanly."""
import numpy as np
import pytest

from src.data import FEATURES
from src.splits import get_protocol_data, load_config
from synth import write_batches

IID = {"data": {"raw_dir": None},
       "split": {"type": "iid", "batches": [1, 2, 3, 4, 5, 6, 7], "holdout": 0.2, "inner_folds": 5, "seed": 0}}
TEMPORAL = {"data": {"raw_dir": None},
            "split": {"train_batches": [1, 2, 3, 4, 5, 6], "val_batches": [7],
                      "inner_folds": [[1], [2], [3], [4, 5], [6]]}}


@pytest.fixture()
def raw(tmp_path):
    write_batches(tmp_path, n_per_batch=120)           # batches 8-10 are unparseable garbage
    return tmp_path


def cfg_for(base, raw_dir, **split_override):
    cfg = {**base, "data": {"raw_dir": str(raw_dir)}}
    cfg["split"] = {**base["split"], **split_override}
    return cfg


def test_iid_never_reads_test_batches(raw):
    p = get_protocol_data(cfg_for(IID, raw))               # would raise on the corrupt files if it read them
    assert set(p.train["batch"]) | set(p.eval["batch"]) <= {1, 2, 3, 4, 5, 6, 7}


def test_iid_refuses_a_config_that_asks_for_test_batches(raw):
    with pytest.raises(AssertionError):
        get_protocol_data(cfg_for(IID, raw, batches=[1, 2, 3, 4, 5, 6, 7, 8]))


def test_temporal_never_reads_test_batches(raw):
    p = get_protocol_data(cfg_for(TEMPORAL, raw))
    assert set(p.train["batch"]) == {1, 2, 3, 4, 5, 6} and set(p.eval["batch"]) == {7}


def test_iid_split_is_disjoint_stratified_and_deterministic(raw):
    cfg = cfg_for(IID, raw)
    p, q = get_protocol_data(cfg), get_protocol_data(cfg)
    key = lambda df: set(map(tuple, df[FEATURES[:3]].round(6).to_numpy()))
    assert not key(p.train) & key(p.eval)
    assert len(p.train) + len(p.eval) == 7 * 120
    assert abs(len(p.eval) / (7 * 120) - 0.2) < 0.01
    overall = np.bincount(np.r_[p.train["gas"], p.eval["gas"]], minlength=7)[1:] / (7 * 120)
    held = np.bincount(p.eval["gas"], minlength=7)[1:] / len(p.eval)
    assert np.abs(overall - held).max() < 0.03              # stratified by gas
    assert p.train.equals(q.train) and p.eval.equals(q.eval)


def test_iid_inner_folds_partition_the_train_part(raw):
    p = get_protocol_data(cfg_for(IID, raw))
    assert sorted(set(p.groups)) == [1, 2, 3, 4, 5] and len(p.groups) == len(p.train)
    sizes = np.bincount(p.groups)[1:]
    assert sizes.max() - sizes.min() <= 2


def test_config_files_parse_and_iid_config_excludes_test_batches():
    cfg = load_config("configs/reference_iid.yaml")
    assert cfg["split"]["type"] == "iid" and not set(cfg["split"]["batches"]) & {8, 9, 10}
    assert "phase1" in cfg                                  # inherited from the base file


FINAL = {"data": {"raw_dir": None},
         "split": {"type": "final_test", "train_batches": [1, 2, 3, 4, 5, 6], "test_batches": [8, 9, 10],
                   "inner_folds": [[1], [2], [3], [4, 5], [6]]}}


def test_final_test_refuses_batches_8_10_without_approval_before_reading(tmp_path):
    cfg = {**FINAL, "data": {"raw_dir": str(tmp_path / "does_not_exist")}}       # a read would raise FileNotFoundError
    with pytest.raises(AssertionError, match="approved_by_user"):
        get_protocol_data(cfg)


def test_final_test_dry_run_uses_train_and_a_validation_subsample(raw):
    p = get_protocol_data(cfg_for(FINAL, raw, test_batches=[7], subsample=50))
    assert set(p.train["batch"]) == {1, 2, 3, 4, 5, 6} and set(p.eval["batch"]) == {7} and len(p.eval) == 50


def test_final_test_configs_parse():
    real, dry = load_config("configs/final_test.yaml"), load_config("configs/final_test_dryrun.yaml")
    assert real["split"]["test_batches"] == [8, 9, 10] and real["split"]["approved_by_user"] is True
    assert dry["split"]["test_batches"] == [7] and not set(dry["split"]["test_batches"]) & {8, 9, 10}
