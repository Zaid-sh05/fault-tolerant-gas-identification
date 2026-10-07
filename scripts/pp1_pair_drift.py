"""Does the relation between replicate sensors survive drift? (documents the S01-S02 result of phase 1)

Usage: python scripts/pp1_pair_drift.py --config configs/preprocessing.yaml
Outputs: results/preprocessing/phase1/pair_consistency_by_batch.csv, figures/s01_s02_across_batches.png

For every replicate pair and batch 1-7 (Train + Validation only), on u = log1p(|DR|) (the signed-log
of the normalised steady-state response): Spearman correlation, and the median/IQR of the offset
u_a - u_b. A pair whose offset moves between batches has a broken relation, so a model fitted on
earlier batches mispredicts one sensor from the other.
"""
import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.data import FEATURE_KINDS, load_batches  # noqa: E402
from src.splits import load_config  # noqa: E402

KIND = FEATURE_KINDS.index("absDR")


def main(cfg_path):
    cfg = load_config(cfg_path)
    sp = cfg["split"]
    batches = sp["train_batches"] + sp["val_batches"]
    df = load_batches(cfg["data"]["raw_dir"], batches)
    out = Path("results/preprocessing/phase1")
    (out / "figures").mkdir(parents=True, exist_ok=True)

    u = lambda s: np.log1p(df[f"S{s + 1:02d}_absDR"].to_numpy())
    rows = []
    for pair in range(8):
        a, b = 2 * pair, 2 * pair + 1
        d = u(a) - u(b)
        for bid in batches:
            m = (df["batch"] == bid).to_numpy()
            rows.append({"pair": f"S{a + 1:02d}-S{b + 1:02d}", "batch": bid, "n": int(m.sum()),
                         "spearman": spearmanr(u(a)[m], u(b)[m])[0],
                         "median_offset": np.median(d[m]),
                         "iqr_offset": np.subtract(*np.percentile(d[m], [75, 25]))})
    tab = pd.DataFrame(rows)
    tab.round(4).to_csv(out / "pair_consistency_by_batch.csv", index=False)

    train_b = sp["train_batches"]
    summ = []
    for pair, g in tab.groupby("pair"):
        tr = g[g["batch"].isin(train_b)]
        v = g[g["batch"] == sp["val_batches"][0]].iloc[0]
        spread = max(tr["iqr_offset"].mean(), 1e-9)
        summ.append({"pair": pair, "train_offset_mean": tr["median_offset"].mean(),
                     "val_offset": v["median_offset"],
                     "offset_shift_in_train_iqr": (v["median_offset"] - tr["median_offset"].mean()) / spread,
                     "val_spearman": v["spearman"], "train_spearman_mean": tr["spearman"].mean()})
    pd.DataFrame(summ).round(3).to_csv(out / "pair_consistency_summary.csv", index=False)
    print(pd.DataFrame(summ).round(3).to_string(index=False))

    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    cmap = plt.get_cmap("viridis")
    for bid in batches:
        m = (df["batch"] == bid).to_numpy()
        ax[0].scatter(u(0)[m], u(1)[m], s=4, alpha=0.5, color=cmap((bid - 1) / 6), label=f"batch {bid}")
    lim = [min(u(0).min(), u(1).min()), max(u(0).max(), u(1).max())]
    ax[0].plot(lim, lim, "k--", lw=0.8)
    ax[0].set(xlabel="S01  log1p|DR|", ylabel="S02  log1p|DR|", title="S01 vs S02, coloured by batch")
    ax[0].legend(markerscale=3, fontsize=7)
    for pair, g in tab.groupby("pair"):
        hi = pair == "S01-S02"
        ax[1].plot(g["batch"], g["median_offset"], color="C3" if hi else "0.7", lw=2.2 if hi else 1,
                   label=pair if hi else None, marker="o" if hi else None)
        ax[2].plot(g["batch"], g["spearman"], color="C3" if hi else "0.7", lw=2.2 if hi else 1,
                   label=pair if hi else None, marker="o" if hi else None)
    ax[1].axvline(6.5, color="k", ls=":", lw=0.8)
    ax[1].set(xlabel="batch", ylabel="median of (u_a - u_b)", title="Replicate offset by batch (grey: other pairs)")
    ax[2].axvline(6.5, color="k", ls=":", lw=0.8)
    ax[2].set(xlabel="batch", ylabel="Spearman within batch", title="Replicate rank correlation by batch")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "figures" / "s01_s02_across_batches.png", dpi=150)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    main(ap.parse_args().config)
