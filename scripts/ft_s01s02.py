"""Final test: the S01-S02 replicate relation across all evaluated batches (Train 1-6 plus the evaluation batches).

Usage: python scripts/ft_s01s02.py --config configs/final_test.yaml --name test
Outputs in <output_root>/<name>/: pair_consistency_by_batch_all.csv, sensor_alarm_rate_by_batch.csv,
figures/s01_s02_across_batches_1_10.png
On u = log1p(|DR|) per batch: Spearman correlation and median offset of every replicate pair (S01-S02 highlighted), and the
alarm rate of the frozen detector per sensor and batch (Train batches: out-of-fold scores, evaluation batches: real
scoring), so that the plot shows whether the S01/S02 alarms seen at Validation persist, grow or vanish. Train rows are the
cleaned ones (invalid-value rule).
"""
import argparse
import json

import joblib
import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.data import FEATURE_KINDS  # noqa: E402
from src.study import Study  # noqa: E402

ABS_DR = FEATURE_KINDS.index("absDR")


def main(cfg_path, name):
    study = Study(cfg_path, name)
    batch = np.r_[study.proto.train["batch"].to_numpy(), study.proto.eval["batch"].to_numpy()]
    X = np.vstack([study.Xtr, study.Xev])
    batches = sorted(set(batch))
    train_batches = set(study.proto.train["batch"])
    u = lambda s: np.log1p(X[:, s * 8 + ABS_DR])
    rows = []
    for pair in range(8):
        a, b = 2 * pair, 2 * pair + 1
        d = u(a) - u(b)
        for bid in batches:
            m = batch == bid
            rows.append({"pair": f"S{a + 1:02d}-S{b + 1:02d}", "batch": bid, "n": int(m.sum()),
                         "spearman": spearmanr(u(a)[m], u(b)[m])[0], "median_offset": float(np.median(d[m])),
                         "iqr_offset": float(np.subtract(*np.percentile(d[m], [75, 25])))})
    tab = pd.DataFrame(rows)
    tab.round(4).to_csv(study.dir / "pair_consistency_by_batch_all.csv", index=False)

    chosen = json.load(open(study.dir / "g2_verdict.json"))["chosen_normalisation"]
    det = joblib.load(study.dir / "detectors" / f"{chosen}.joblib")
    A_tr = det._normalise(det.E_oof_) / det.tau_ > 1.0
    A_ev = det.ratio(study.Xev) > 1.0
    A, alarm = np.vstack([A_tr, A_ev]), []
    for bid in batches:
        m = batch == bid
        for s in range(16):
            alarm.append({"batch": bid, "sensor": f"S{s + 1:02d}", "alarm_rate": float(A[m][:, s].mean()),
                          "source": "out-of-fold" if bid in train_batches else "evaluation"})
    alarm = pd.DataFrame(alarm)
    alarm.round(4).to_csv(study.dir / "sensor_alarm_rate_by_batch.csv", index=False)

    (study.dir / "figures").mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 4, figsize=(17, 4))
    cmap = plt.get_cmap("viridis")
    for bid in batches:
        m = batch == bid
        ax[0].scatter(u(0)[m], u(1)[m], s=3, alpha=0.4, color=cmap((bid - 1) / 9), label=f"batch {bid}")
    lim = [min(u(0).min(), u(1).min()), max(u(0).max(), u(1).max())]
    ax[0].plot(lim, lim, "k--", lw=0.8)
    ax[0].set(xlabel="S01  log1p|DR|", ylabel="S02  log1p|DR|", title="S01 vs S02, coloured by batch")
    ax[0].legend(markerscale=4, fontsize=6, ncol=2)
    for col, k, label in ((1, "median_offset", "median offset u_a - u_b"), (2, "spearman", "Spearman within batch")):
        for pair, g in tab.groupby("pair"):
            hi = pair == "S01-S02"
            ax[col].plot(g["batch"], g[k], color="C3" if hi else "0.75", lw=2.2 if hi else 1,
                         marker="o" if hi else None, label=pair if hi else None)
        ax[col].axvline(6.5, color="k", ls=":", lw=0.8)
        ax[col].set(xlabel="batch", ylabel=label, title=f"Replicate pairs (grey: others)")
        ax[col].set_xticks(batches)
    ax[1].legend(fontsize=8)
    piv = alarm.pivot(index="batch", columns="sensor", values="alarm_rate")
    for s in piv.columns:
        hi = s in ("S01", "S02")
        ax[3].plot(piv.index, piv[s], color={"S01": "C3", "S02": "C0"}.get(s, "0.75"), lw=2.2 if hi else 1,
                   marker="o" if hi else None, label=s if hi else None)
    ax[3].axvline(6.5, color="k", ls=":", lw=0.8)
    ax[3].set(xlabel="batch", ylabel="alarm rate of the detector", title="Detector alarms per sensor (clean rows)")
    ax[3].set_xticks(batches)
    ax[3].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(study.dir / "figures" / "s01_s02_across_batches_1_10.png", dpi=150)
    print(tab[tab.pair == "S01-S02"].round(3).to_string(index=False))
    print(piv[["S01", "S02"]].round(3).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/final_test.yaml")
    ap.add_argument("--name", default="test")
    a = ap.parse_args()
    main(a.config, a.name)
