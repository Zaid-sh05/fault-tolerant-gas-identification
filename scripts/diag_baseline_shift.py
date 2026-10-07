"""Why did the SVM baseline move after the two corrupt Train records were dropped?

Usage: python scripts/diag_baseline_shift.py
Writes results/main_cleaned/diagnosis/*.csv

1. selected hyper-parameters and the Validation score of every SVM grid point, before/after
2. Train std of every feature of S05-S08, before/after the two records are dropped
3. per-gas F1, before/after
4. a 2x2 design that separates the two possible mechanisms for the SVM (fixed C=10 and gamma as given):
     rows fitted on   : uncleaned Train  |  cleaned Train
     scaler fitted on : uncleaned Train  |  cleaned Train
   "scaler statistics" (mean/std inflated by the corrupt cells) vs "the two records as training samples".
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.data import FEATURES, FEATURE_KINDS, xy
from src.models import scores
from src.splits import get_protocol_data, load_config

OLD, NEW = "results/main/02_baselines", "results/main_cleaned/02_baselines"
out = Path("results/main_cleaned/diagnosis")
out.mkdir(parents=True, exist_ok=True)
pd.set_option("display.width", 220)


def main():
    # 1. parameters and grid ------------------------------------------------------------
    sel = {k: json.load(open(f"{d}/selected_params.json"))["svm"] for k, d in (("before", OLD), ("after", NEW))}
    print("selected SVM params  before:", sel["before"], "| after:", sel["after"])
    grid = {k: pd.read_csv(f"{d}/grid_val.csv") for k, d in (("before", OLD), ("after", NEW))}
    g = grid["before"].query("model == 'svm'").merge(grid["after"].query("model == 'svm'"), on="params",
                                                     suffixes=("_before", "_after"))
    g = g[["params", "macro_f1_before", "macro_f1_after"]]
    g["change"] = g["macro_f1_after"] - g["macro_f1_before"]
    g.round(4).to_csv(out / "svm_grid_before_after.csv", index=False)
    print("\nSVM grid, Validation Macro-F1 for every parameter set:")
    print(g.round(4).to_string(index=False))

    # 2. std of S05-S08 ------------------------------------------------------------------
    p_old = get_protocol_data(load_config("configs/main.yaml"))              # no cleaning block
    p_new = get_protocol_data(load_config("configs/main_cleaned.yaml"))
    Xo, yo = xy(p_old.train)
    Xn, yn = xy(p_new.train)
    Xva, yva = xy(p_new.eval)
    rows = [{"feature": f, "std_before": Xo[:, j].std(), "std_after": Xn[:, j].std()}
            for j, f in enumerate(FEATURES) if int(f[1:3]) in (5, 6, 7, 8)]
    sd = pd.DataFrame(rows)
    sd["inflation"] = sd["std_before"] / sd["std_after"]
    sd.round(3).to_csv(out / "std_s05_s08_before_after.csv", index=False)
    print("\nTrain std of S05-S08 features (all inflated by more than 1.5x):")
    print(sd[sd.inflation > 1.5].round(2).to_string(index=False))
    allsd = pd.DataFrame({"feature": FEATURES, "inflation": Xo.std(0) / Xn.std(0)})
    print("features over all 16 sensors with inflation > 1.5x:", allsd[allsd.inflation > 1.5].round(1).values.tolist())

    # 3. per-gas F1 -----------------------------------------------------------------------
    pc = {k: pd.read_csv(f"{d}/per_class_f1_val.csv").set_index("model") for k, d in (("before", OLD), ("after", NEW))}
    diff = (pc["after"] - pc["before"]).round(3)
    diff.to_csv(out / "per_gas_f1_change.csv")
    print("\nper-gas F1 change (after - before), Validation:")
    print(diff.loc[["svm", "lgbm"]].to_string())

    # 4. 2x2 design -----------------------------------------------------------------------
    res = []
    for gamma in ("scale", 0.01):
        for fit_rows, (Xf, yf) in (("uncleaned", (Xo, yo)), ("cleaned", (Xn, yn))):
            for scaler_on, Xs in (("uncleaned", Xo), ("cleaned", Xn)):
                sc = StandardScaler().fit(Xs)
                clf = SVC(kernel="rbf", C=10, gamma=gamma, random_state=0).fit(sc.transform(Xf), yf)
                res.append({"gamma": gamma, "svm_fitted_on": fit_rows, "scaler_fitted_on": scaler_on,
                            "macro_f1": scores(yva, clf.predict(sc.transform(Xva)))["macro_f1"]})
    d2 = pd.DataFrame(res)
    d2.round(4).to_csv(out / "design_2x2.csv", index=False)
    print("\n2x2 design (C=10):")
    print(d2.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
