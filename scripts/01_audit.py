"""Step 1: data audit.

Usage: python scripts/01_audit.py --config configs/main.yaml
Outputs: results/01_audit/{audit.md, *.csv, *.png}

Leakage rule: only Train/Val batches are loaded. Test files are never opened (not even to count lines).
"""
import argparse, sys, json
from pathlib import Path
import numpy as np, pandas as pd, yaml
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster

from src.data import (load_batches, FEATURES, FEATURE_KINDS, GAS_NAMES,
                      N_SENSORS, sensor_columns)

# Acquisition periods per batch as reported in the dataset literature (months).
BATCH_MONTHS = {1: "1-2", 2: "3-10", 3: "11-13", 4: "14-15", 5: "16",
                6: "17-20", 7: "21", 8: "22-23", 9: "24,30", 10: "36"}


def sensor_profile(d, s):
    cols = [FEATURES[c] for c in sensor_columns(s)]
    v = d[cols].rank().to_numpy()
    return ((v - v.mean(0)) / v.std(0)).ravel()


def main(cfg_path):
    cfg = yaml.safe_load(open(cfg_path))
    out = Path("results") / Path(cfg_path).stem / "01_audit"; out.mkdir(parents=True, exist_ok=True)
    tr_b, va_b, te_b = (cfg["split"][k] for k in ("train_batches", "val_batches", "test_batches"))
    df = load_batches(cfg["data"]["raw_dir"], tr_b + va_b)
    md = ["# Data audit — UCI Gas Sensor Array Drift Dataset\n"]

    # 1. Integrity
    X = df[FEATURES]
    integ = {"records": len(df), "features": X.shape[1], "nan_values": int(X.isna().sum().sum()),
             "constant_features": int((X.std() == 0).sum()),
             "duplicate_feature_rows": int(X.duplicated().sum()),
             "gas_codes": sorted(df.gas.unique().tolist())}
    md += ["## 1. Integrity", "```", json.dumps(integ, indent=1), "```",
           "Documented total: 13,910 records over 10 batches; only Train+Val are parsed here.\n"]

    # 2. Batch x gas
    ct = pd.crosstab(df.batch, df.gas.map(GAS_NAMES), margins=True, margins_name="Total")
    ct.insert(0, "months", [BATCH_MONTHS.get(b, "") for b in ct.index])
    ct.to_csv(out / "batch_by_gas.csv")
    md += ["## 2. Records per batch and gas", ct.to_markdown(), ""]

    # 3. Feature layout check (documented order; verify sign structure)
    rows = []
    for k in FEATURE_KINDS:
        v = df[[c for c in FEATURES if c.endswith("_" + k)]].to_numpy()
        rows.append({"kind": k, "frac_negative": (v < 0).mean(), "median": np.median(v),
                     "p01": np.percentile(v, 1), "p99": np.percentile(v, 99)})
    lay = pd.DataFrame(rows); lay.to_csv(out / "feature_kinds.csv", index=False)
    md += ["## 3. Feature layout (documented: sensor-major blocks of 8)",
           "Expected: EMAd* (decaying transient) negative, other kinds non-negative.",
           lay.round(3).to_markdown(index=False), ""]

    # 4. Sensor similarity on TRAIN batches only
    d = df[df.batch.isin(tr_b)]
    P = {s: sensor_profile(d, s) for s in range(N_SENSORS)}
    C = np.array([[np.corrcoef(P[a], P[b])[0, 1] for b in range(N_SENSORS)] for a in range(N_SENSORS)])
    names = [f"S{s+1:02d}" for s in range(N_SENSORS)]
    pd.DataFrame(C, index=names, columns=names).round(3).to_csv(out / "sensor_similarity_train.csv")
    clus = fcluster(linkage(1 - C[np.triu_indices(N_SENSORS, 1)], "average"), 4, "maxclust")
    pairs = [(s, int(np.argsort(-C[s])[1])) for s in range(N_SENSORS)]
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(C, vmin=0, vmax=1, cmap="viridis")
    ax.set_xticks(range(16), names, rotation=90, fontsize=7); ax.set_yticks(range(16), names, fontsize=7)
    fig.colorbar(im, label="rank correlation (8-feature profile)")
    ax.set_title(f"Sensor similarity, Train batches {tr_b}")
    fig.tight_layout(); fig.savefig(out / "sensor_similarity_train.png", dpi=150); plt.close(fig)
    md += ["## 4. Sensor grouping (estimated from Train data; NOT documented)",
           "Average-linkage clustering into 4 groups: " +
           ", ".join(f"{n}->{c}" for n, c in zip(names, clus)),
           "Nearest neighbour of each sensor: " +
           ", ".join(f"{names[a]}~{names[b]} ({C[a, b]:.3f})" for a, b in pairs), ""]

    # 5. Per-sensor drift heterogeneity on TRAIN+VAL batches only
    dv = df[df.batch.isin(tr_b + va_b)]
    ref = dv[dv.batch == min(tr_b)]
    drift = pd.DataFrame(index=names, columns=[b for b in tr_b + va_b], dtype=float)
    for s in range(N_SENSORS):
        col = f"S{s+1:02d}_absDR"
        for b in tr_b + va_b:
            cur = dv[dv.batch == b]; ratios = []
            for g in sorted(set(cur.gas) & set(ref.gas)):
                ratios.append(np.log(cur.loc[cur.gas == g, col].median() /
                                     ref.loc[ref.gas == g, col].median()))
            drift.loc[names[s], b] = np.mean(ratios)
    drift.round(3).to_csv(out / "drift_logratio_absDR.csv")
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    lim = np.nanmax(np.abs(drift.values))
    im = ax.imshow(drift.values.astype(float), cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(drift.shape[1]), drift.columns); ax.set_yticks(range(16), names, fontsize=7)
    ax.set_xlabel("batch"); fig.colorbar(im, label="mean log(median |DR| / batch-1 median), per gas")
    ax.set_title("Per-sensor drift (Train+Val only)")
    fig.tight_layout(); fig.savefig(out / "drift_per_sensor.png", dpi=150); plt.close(fig)
    spread = drift.std(axis=0)
    md += ["## 5. Drift differs across sensors (Train+Val only)",
           "Mean over gases of log(median |DR| in batch / median in batch 1).",
           drift.round(2).to_markdown(), "",
           "Across-sensor std per batch: " + ", ".join(f"b{b}={v:.2f}" for b, v in spread.items()), ""]

    # 6. Proposed split
    def cov(bs):
        sub = df[df.batch.isin(bs)]
        c = sub.gas.map(GAS_NAMES).value_counts().reindex(GAS_NAMES.values()).fillna(0).astype(int)
        return {"batches": str(bs), "n": len(sub), **c.to_dict()}
    sp = pd.DataFrame([{"role": "Train", **cov(tr_b)}, {"role": "Val", **cov(va_b)},
                       {"role": "Test", "batches": str(te_b), "n": "not read"}])
    sp.to_csv(out / "split.csv", index=False)
    md += ["## 6. Split in config", sp.to_markdown(index=False), ""]

    (out / "audit.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", default="configs/main.yaml")
    main(ap.parse_args().config)
