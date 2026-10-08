"""Fault scenarios: only the target blocks change, shared rows, bias unit, determinism, saved hashes."""
import numpy as np
import pytest

from src.data import sensor_columns
from src.scenarios import (LEVELS, MEDIUM, SENSOR_SETS, FaultStats, Scenario, apply_scenario, build_scenarios,
                           matrix_hash, scenario_table)
from synth import make_raw

X_TRAIN = make_raw(600, seed=0)[0]
X_EVAL = make_raw(300, seed=1)[0]
STATS = FaultStats.fit(X_TRAIN)


def sc(fault, level, sensors=(3,), kset="k1", seed=0):
    return Scenario(0, kset, tuple(sensors), fault, level, seed)


def untouched(Xf, sensors):
    other = [c for c in range(128) if c not in sum((sensor_columns(s) for s in sensors), [])]
    return np.array_equal(Xf[:, other], X_EVAL[:, other])


@pytest.mark.parametrize("fault,level", [("dropout", 0.5), ("bias", 1.0), ("stuck", 0.5), ("random", 0.5)])
def test_only_the_target_block_changes_and_the_input_is_not_modified(fault, level):
    before = X_EVAL.copy()
    Xf, truth = apply_scenario(X_EVAL, sc(fault, level, (2, 3), "k2"), STATS)
    assert np.array_equal(X_EVAL, before) and untouched(Xf, (2, 3))
    assert truth.shape == (300, 16) and set(np.flatnonzero(truth.any(0))) == {2, 3}


def test_dropout_rows_are_shared_by_all_sensors_of_the_set():
    Xf, truth = apply_scenario(X_EVAL, sc("dropout", 0.5, (0, 1, 8, 9), "k4"), STATS)
    nan_rows = [np.isnan(Xf[:, sensor_columns(s)]).all(1) for s in (0, 1, 8, 9)]
    assert all(np.array_equal(nan_rows[0], r) for r in nan_rows) and 0.4 < nan_rows[0].mean() < 0.6
    assert np.array_equal(truth[:, 0], nan_rows[0])
    assert not np.isnan(Xf[~nan_rows[0]]).any()


def test_level_one_affects_every_row():
    for fault in ("dropout", "stuck", "random"):
        _, truth = apply_scenario(X_EVAL, sc(fault, 1.0), STATS)
        assert truth[:, 3].all()


def test_bias_shifts_by_delta_times_robust_sigma_with_one_shared_sign():
    Xf, truth = apply_scenario(X_EVAL, sc("bias", 3.0, (4, 5), "k2"), STATS)
    c4, c5 = sensor_columns(4), sensor_columns(5)
    shift4 = (Xf[:, c4] - X_EVAL[:, c4]) / STATS.sigma[c4]
    shift5 = (Xf[:, c5] - X_EVAL[:, c5]) / STATS.sigma[c5]
    assert np.allclose(np.abs(shift4), 3.0) and np.allclose(shift4, shift5)       # same sign for the whole set
    assert truth[:, [4, 5]].all()


def test_stuck_rows_equal_one_reading_of_the_evaluation_set():
    Xf, truth = apply_scenario(X_EVAL, sc("stuck", 1.0, (6,)), STATS)
    c = sensor_columns(6)
    assert (Xf[:, c] == Xf[0, c]).all()
    assert any(np.array_equal(Xf[0, c], X_EVAL[i, c]) for i in range(len(X_EVAL)))


def test_random_values_lie_between_the_train_percentiles():
    Xf, truth = apply_scenario(X_EVAL, sc("random", 1.0, (7,)), STATS)
    c = sensor_columns(7)
    assert (Xf[:, c] >= STATS.p1[c]).all() and (Xf[:, c] <= STATS.p99[c]).all()
    assert not np.allclose(Xf[:, c], X_EVAL[:, c])


def test_scenarios_are_deterministic_and_seeds_differ():
    a, b = sc("random", 0.5, seed=1), sc("random", 0.5, seed=2)
    assert matrix_hash(apply_scenario(X_EVAL, a, STATS)[0]) == matrix_hash(apply_scenario(X_EVAL, a, STATS)[0])
    assert matrix_hash(apply_scenario(X_EVAL, a, STATS)[0]) != matrix_hash(apply_scenario(X_EVAL, b, STATS)[0])


def test_scenario_list_sizes_and_sets():
    full = build_scenarios(seeds=range(5))
    settings = sum(len(v) for v in LEVELS.values())                                   # 9 fault settings
    assert len(full) == (16 + 8 + 4) * settings * 5
    assert len({s.sid for s in full}) == len(full)
    reduced = build_scenarios(seeds=range(5), ksets=("k1", "k2"), reduced=True)
    assert len(reduced) == (16 + 8) * 4 * 5 and {s.level for s in reduced if s.fault == "bias"} == {MEDIUM["bias"]}
    assert SENSOR_SETS["k2"][0] == (0, 1) and SENSOR_SETS["k4"][0] == (0, 1, 8, 9)


def test_table_hashes_match_a_fresh_application():
    scenarios = build_scenarios(seeds=[0], ksets=("k2",), reduced=True)[:6]
    table, masks = scenario_table(scenarios, X_EVAL, STATS)
    for s, h in zip(scenarios, table["hash"]):
        assert matrix_hash(apply_scenario(X_EVAL, s, STATS)[0]) == h
    assert len(masks) == 6
