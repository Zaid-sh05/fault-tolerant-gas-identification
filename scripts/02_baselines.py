"""Step 2: clean baselines, selected and evaluated on Validation only.

Usage: python scripts/02_baselines.py --config configs/main.yaml
Test batches are never loaded here.
"""
import argparse, sys, json, time
from pathlib import Path
import numpy as np, pandas as pd, yaml, joblib
from sklearn.metrics import f1_score, confusion_matrix

from src.data import xy, GAS_NAMES
from src.splits import get_protocol_data, load_config
from src.models import make_lgbm, make_svm, grid, scores
from src.faults import augment_with_faults


def main(cfg_path):
    cfg = load_config(cfg_path); seed = cfg["seeds"]["model"]
    out = Path("results") / Path(cfg_path).stem / "02_baselines"; (out / "models").mkdir(parents=True, exist_ok=True)
    proto = get_protocol_data(cfg)                    # Test files are never opened; cleaning rule applied to Train only
    tr, va = proto.train, proto.eval
    print(f"Train rows {len(tr)} (dropped by cleaning rule: {proto.dropped_train.values.tolist()}), "
          f"Validation rows {len(va)} (invalid but kept: {proto.flagged_eval.values.tolist()})")
    Xtr, ytr = xy(tr); Xva, yva = xy(va)
    std_train = np.nanstd(Xtr, axis=0)
    np.save(out / "std_train.npy", std_train)

    log, selected = [], {}
    for name, maker, g in [("lgbm", make_lgbm, cfg["models"]["lgbm_grid"]),
                           ("svm", make_svm, cfg["models"]["svm_grid"])]:
        best = None
        for params in grid(g):
            t = time.time(); m = maker(params, seed).fit(Xtr, ytr)
            sc = scores(yva, m.predict(Xva))
            log.append({"model": name, "params": json.dumps(params), **sc, "fit_s": round(time.time() - t, 1)})
            print(log[-1])
            if best is None or sc[cfg["models"]["selection_metric"]] > best[0]:
                best = (sc[cfg["models"]["selection_metric"]], params, m)
        selected[name] = best[1]
        joblib.dump(best[2], out / "models" / f"{name}.joblib")

    # Fault-augmented variants: same selected hyper-parameters, no re-tuning.
    rng = np.random.default_rng(seed)
    Xaug, yaug = augment_with_faults(Xtr, ytr, std_train, rng, cfg["fault_augmentation"]["copies"])
    for name, maker in [("lgbm", make_lgbm), ("svm", make_svm)]:
        m = maker(selected[name], seed).fit(Xaug, yaug)
        joblib.dump(m, out / "models" / f"{name}_aug.joblib")
        selected[f"{name}_aug"] = selected[name]

    pd.DataFrame(log).to_csv(out / "grid_val.csv", index=False)
    json.dump(selected, open(out / "selected_params.json", "w"), indent=1)

    rows, per_class = [], []
    labels = sorted(GAS_NAMES)
    for name in ["lgbm", "svm", "lgbm_aug", "svm_aug"]:
        m = joblib.load(out / "models" / f"{name}.joblib"); p = m.predict(Xva)
        rows.append({"model": name, **scores(yva, p)})
        f = f1_score(yva, p, labels=labels, average=None, zero_division=0)
        per_class.append({"model": name, **{GAS_NAMES[l]: v for l, v in zip(labels, f)}})
        pd.DataFrame(confusion_matrix(yva, p, labels=labels),
                     index=[GAS_NAMES[l] for l in labels],
                     columns=[GAS_NAMES[l] for l in labels]).to_csv(out / f"confusion_val_{name}.csv")
    res = pd.DataFrame(rows); pc = pd.DataFrame(per_class)
    res.to_csv(out / "clean_val.csv", index=False); pc.to_csv(out / "per_class_f1_val.csv", index=False)
    print(res.round(4).to_string(index=False)); print(pc.round(3).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", default="configs/main.yaml")
    main(ap.parse_args().config)
