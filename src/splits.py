"""Evaluation protocols.

temporal       (main)      Train batches 1-6, Validation batch 7. Real drift between Train and Validation.
reference_iid  (reference) Batches 1-7 only, stratified (by gas) random 80/20 hold-out with a fixed seed,
                           plus a stratified K-fold inside the 80% for choosing settings. No drift between
                           Train and evaluation rows. The batch id is kept for analysis only.

Both protocols: every fitted object (imputers, scalers, selectors, models, fault-augmented training)
may use the training rows only. Faults are injected AFTER the split, on a clean copy of the evaluation rows.
Batches 8-10 are never opened by either protocol.

final_test     (once)      Train batches 1-6 (same cleaning, same fitted objects) and the evaluation batches named in
                           `test_batches`. Opening batches 8-10 needs `approved_by_user: true` in the config; the check
                           happens before any file is read. Used by configs/final_test.yaml only; the dry run
                           (configs/final_test_dryrun.yaml) evaluates on a random subsample of Validation instead.

Data cleaning (config key `cleaning`): the invalid-value rule of src/cleaning.py is fitted on the Train
rows and the records it flags are dropped from Train only. Evaluation rows are never dropped; the flagged
ones are listed in `Protocol.flagged_eval` so they can be reported.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import StratifiedKFold, train_test_split

from .cleaning import InvalidValueRule
from .data import load_batches, split_by_batches, xy

TEST_BATCHES = {8, 9, 10}


@dataclass
class Protocol:
    name: str
    train: pd.DataFrame
    eval: pd.DataFrame
    groups: np.ndarray        # group label of every Train row (batch id, or inner-fold id)
    inner_folds: list         # leave-group-out folds for hyper-parameters fitted on Train: [(label, ...), ...]
    dropped_train: pd.DataFrame = None   # Train records removed by the cleaning rule (batch, line, gas)
    flagged_eval: pd.DataFrame = None    # evaluation records the rule flags; KEPT, only reported


def load_config(path):
    """YAML with an optional `base:` file; top-level keys of the child replace the base's."""
    cfg = yaml.safe_load(open(path))
    base = cfg.pop("base", None)
    return {**load_config(base), **cfg} if base else cfg


ID_COLUMNS = ["batch", "line", "gas"]


def _clean_train(cfg, train, evaluation):
    """Apply the invalid-value rule: drop flagged Train rows, only report flagged evaluation rows."""
    clean_cfg = cfg.get("cleaning", {})
    rule_cfg = clean_cfg.get("invalid_value_rule")
    if not rule_cfg:
        empty = train.iloc[:0][ID_COLUMNS]
        return train, empty, empty
    rule = InvalidValueRule(rule_cfg["threshold"]).fit(xy(train)[0])
    bad_train, bad_eval = rule.records(xy(train)[0]), rule.records(xy(evaluation)[0])
    # Sensitivity analysis only: force a record in (extra_drop) or out (never_drop) of the Train drop list.
    keys = pd.Series(list(zip(train["batch"], train["line"])), index=train.index)
    bad_train = (bad_train | keys.isin({tuple(k) for k in clean_cfg.get("extra_drop", [])}).to_numpy())         & ~keys.isin({tuple(k) for k in clean_cfg.get("never_drop", [])}).to_numpy()
    return (train[~bad_train].reset_index(drop=True), train[bad_train][ID_COLUMNS].reset_index(drop=True),
            evaluation[bad_eval][ID_COLUMNS].reset_index(drop=True))


def get_protocol_data(cfg):
    sp = cfg["split"]
    kind = sp.get("type", "temporal")
    raw_dir = cfg["data"]["raw_dir"]
    if kind == "temporal":
        wanted = sp["train_batches"] + sp["val_batches"]
        assert not set(wanted) & TEST_BATCHES, "Test batches must never be loaded"
        df = load_batches(raw_dir, wanted)
        tr, va = split_by_batches(df, sp["train_batches"]), split_by_batches(df, sp["val_batches"])
        tr, dropped, flagged = _clean_train(cfg, tr, va)
        return Protocol("temporal", tr, va, tr["batch"].to_numpy(), [tuple(f) for f in sp["inner_folds"]],
                        dropped, flagged)
    if kind == "iid":
        assert not set(sp["batches"]) & TEST_BATCHES, "reference_iid must not read batches 8-10"
        df = load_batches(raw_dir, sp["batches"])
        tr_idx, ev_idx = train_test_split(np.arange(len(df)), test_size=sp["holdout"],
                                          stratify=df["gas"], random_state=sp["seed"])
        tr = df.iloc[np.sort(tr_idx)].reset_index(drop=True)
        ev = df.iloc[np.sort(ev_idx)].reset_index(drop=True)
        tr, dropped, flagged = _clean_train(cfg, tr, ev)
        groups = np.zeros(len(tr), dtype=int)
        folds = StratifiedKFold(sp["inner_folds"], shuffle=True, random_state=sp["seed"])
        for k, (_, held_out) in enumerate(folds.split(tr, tr["gas"]), start=1):
            groups[held_out] = k
        return Protocol("reference_iid", tr, ev, groups, [(k,) for k in range(1, sp["inner_folds"] + 1)],
                        dropped, flagged)
    if kind == "final_test":
        ev_b = sp["test_batches"]
        if set(ev_b) & TEST_BATCHES:
            assert sp.get("approved_by_user") is True, "opening batches 8-10 needs approved_by_user: true"
        assert not set(ev_b) & set(sp["train_batches"]), "evaluation batches overlap Train"
        df = load_batches(raw_dir, sp["train_batches"] + ev_b)
        tr, ev = split_by_batches(df, sp["train_batches"]), split_by_batches(df, ev_b)
        if sp.get("subsample"):                                         # dry run only: fewer rows, same code path
            ev = ev.sample(n=sp["subsample"], random_state=0).sort_index().reset_index(drop=True)
        tr, dropped, flagged = _clean_train(cfg, tr, ev)
        return Protocol("final_test", tr, ev, tr["batch"].to_numpy(), [tuple(f) for f in sp["inner_folds"]],
                        dropped, flagged)
    raise ValueError(kind)
