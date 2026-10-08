"""v2 candidate table (POST-HOC, decisions_log G4-G6). Batches 1-7 only.

Usage: python scripts/v2_dev.py
Outputs in results/v2/: trials.csv (one row per candidate x protocol x evaluation batch, appended), candidates.csv,
candidates.md, choice.json.
  drift_dev : Dev-Train 1-3, Dev-Eval 6 and 7 scored separately, then averaged (selection metric)
  original  : Train 1-6, Validation 7 (condition: clean SVM Macro-F1 >= 0.849, detector G2 statistic >= 0.80)
Transforms of new data use the readings of that batch only, never its labels. M4 is defined from M1-M3 only (G5).
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

sys.path.insert(0, "scripts")
from ov3_detector import auc  # noqa: E402
from src.data import xy  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.drift import BatchEnsemble, BatchRobustNorm, Chain, Coral, Identity  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.preprocessing import fit_preprocessor  # noqa: E402
from src.scenarios import FaultStats, MEDIUM, apply_scenario, build_scenarios  # noqa: E402
from src.splits import get_protocol_data, load_config  # noqa: E402
from src.study import AUG_SEEDS, OVERNIGHT  # noqa: E402

OUT = Path("results/v2")
PROTOCOLS = {"drift_dev": "configs/v2_drift_dev.yaml", "original": "configs/preprocessing.yaml"}
V1_VAL, VAL_MARGIN, G2_MIN, TIE = 0.859, 0.01, 0.80, 0.01
SIMPLICITY = ["M0", "M1", "M2", "M3"]                       # M4 combinations come last
B, BOOT_SEED = 1000, 0


def load(cfg_path):
    proto = get_protocol_data(load_config(cfg_path))
    Xtr, ytr = xy(proto.train)
    evals = {int(b): xy(proto.eval[proto.eval["batch"] == b]) for b in sorted(proto.eval["batch"].unique())}
    return Xtr, ytr, proto.train["batch"].to_numpy(), evals


def make_transform(parts):
    ts = [c() for p, c in (("M1", BatchRobustNorm), ("M2", Coral)) if p in parts]
    return Identity() if not ts else ts[0] if len(ts) == 1 else Chain(*ts)


def build(name, Xtr, ytr, btr):
    """(transform, transformed Train rows, predict(raw batch) -> labels)."""
    fin = json.load(open(OVERNIGHT / "final_pipeline.json"))
    parts = name.split("+")
    T = make_transform(parts).fit(Xtr, btr)
    Xt = T.train_transform(Xtr, btr)
    pre = fit_preprocessor(fin["spec"], Xt, ytr, btr, fill_nan=False)
    Z = pre.transform(Xt)
    if "M3" in parts:
        clf = BatchEnsemble(fin["svm_params"]).fit(Z, ytr, btr)
        return T, Xt, lambda X: clf.predict(pre.transform(T.transform(X)))
    clf = SVC(kernel="rbf", random_state=0, **fin["svm_params"]).fit(fill_nan_zero(Z), ytr)
    return T, Xt, lambda X: fast_svm_predict(clf, fill_nan_zero(pre.transform(T.transform(X))))


def boot_diffs(y, a, b):
    rng = np.random.default_rng(BOOT_SEED)
    out = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, len(y), len(y))
        out[i] = scores(y[idx], a[idx])["macro_f1"] - scores(y[idx], b[idx])["macro_f1"]
    return out


def g2_statistic(T, Xt, btr, Xtr, Xev):
    """v1 G2 statistic for this base: median over fault types of the mean isolation AUROC (k=1, medium, 5 seeds)."""
    det = ReliabilityDetector(normalization="median").fit(Xt, btr)
    stats = FaultStats.fit(Xtr)                                  # faults are injected on raw readings (G7)
    per = {f: [] for f in MEDIUM}
    for sc in build_scenarios(AUG_SEEDS, ("k1",), reduced=True):
        Xf, truth = apply_scenario(Xev, sc, stats)
        R = det.ratio(T.transform(Xf))
        per[sc.fault].append(auc(R[truth], R[~truth & truth.any(1)[:, None]]))
    per = {f: float(np.mean(v)) for f, v in per.items()}
    return float(np.median(list(per.values()))), per


def evaluate(name, data, preds_m0, trials):
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    row = {"candidate": name}
    for proto, (Xtr, ytr, btr, evals) in data.items():
        t0 = time.time()
        T, Xt, predict = build(name, Xtr, ytr, btr)
        diffs = []
        for b, (X, y) in evals.items():
            p = predict(X)
            s = scores(y, p)
            if name == "M0":
                preds_m0[(proto, b)] = p
            d = boot_diffs(y, p, preds_m0[(proto, b)])
            diffs.append(d)
            row[f"{proto}_b{b}"] = s["macro_f1"]
            trials.append({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "commit": commit, "candidate": name, "protocol": proto,
                           "eval_batch": b, "n_rows": len(y), "macro_f1": s["macro_f1"], "accuracy": s["accuracy"],
                           "diff_vs_M0": s["macro_f1"] - scores(y, preds_m0[(proto, b)])["macro_f1"],
                           "ci_low": float(np.percentile(d, 2.5)), "ci_high": float(np.percentile(d, 97.5))})
        if proto == "drift_dev":
            row["drift_dev_mean"] = float(np.mean([row[f"drift_dev_b{b}"] for b in evals]))
            dm = np.mean(diffs, axis=0)
            row["dev_mean_diff_vs_M0_ci"] = f"[{np.percentile(dm, 2.5):+.3f}, {np.percentile(dm, 97.5):+.3f}]"
        else:
            row["g2_val7"], per = g2_statistic(T, Xt, btr, Xtr, evals[7][0])
            row.update({f"auroc_{f}": v for f, v in per.items()})
        print(f"{name} {proto}: done in {time.time() - t0:.0f} s", flush=True)
    return row


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = {p: load(c) for p, c in PROTOCOLS.items()}
    preds_m0, trials, rows = {}, [], []
    for name in SIMPLICITY:
        rows.append(evaluate(name, data, preds_m0, trials))
        if name == "M0":                                       # sanity: M0 on the original split is the v1 model
            assert abs(rows[0]["original_b7"] - V1_VAL) < 5e-4, f"M0 does not reproduce v1 Validation ({rows[0]['original_b7']:.4f})"
    m0 = rows[0]
    top = sorted(rows[1:], key=lambda r: -r["drift_dev_mean"])[:2]
    m4_note = "M4 = " + "+".join(sorted(r["candidate"] for r in top)) + " (two best of M1-M3 on Drift-Dev, both beat M0)"
    if all(r["drift_dev_mean"] > m0["drift_dev_mean"] for r in top):
        rows.append(evaluate("+".join(sorted(r["candidate"] for r in top)), data, preds_m0, trials))
    else:
        m4_note = "M4 not run: the two best of M1-M3 (" + ", ".join(r["candidate"] for r in top) + ") do not both beat M0 on Drift-Dev"
    print(m4_note, flush=True)

    tab = pd.DataFrame(rows)
    tab["eligible"] = (tab["original_b7"] >= V1_VAL - VAL_MARGIN) & (tab["g2_val7"] >= G2_MIN)
    elig = tab[tab["eligible"]]
    best = elig["drift_dev_mean"].max()
    tied = elig[elig["drift_dev_mean"] >= best - TIE]["candidate"].tolist()
    order = SIMPLICITY + [c for c in tab["candidate"] if c not in SIMPLICITY]
    winner = min(tied, key=order.index)
    choice = {"winner": winner, "tied_within_0.01": tied, "best_eligible_dev_mean": best, "m4": m4_note,
              "rule": "decisions_log G6", "post_hoc": True,
              "no_improvement": winner == "M0"}
    pd.DataFrame(trials).to_csv(OUT / "trials.csv", mode="a", header=not (OUT / "trials.csv").exists(), index=False)
    tab.round(4).to_csv(OUT / "candidates.csv", index=False)
    json.dump(choice, open(OUT / "choice.json", "w"), indent=1)
    cols = ["candidate", "drift_dev_b6", "drift_dev_b7", "drift_dev_mean", "dev_mean_diff_vs_M0_ci", "original_b7", "g2_val7",
            "auroc_dropout", "auroc_bias", "auroc_stuck", "auroc_random", "eligible"]
    md = ["# v2 candidates (POST-HOC; decisions_log G4-G6)", "",
          "Clean SVM Macro-F1. Drift-Dev: train 1-3, evaluate 6 and 7. Original: train 1-6, Validation 7. "
          "g2_val7 = median over fault types of the isolation AUROC (k=1, medium) on Validation 7. CI: paired bootstrap over rows "
          "(1000, per batch, averaged), optimistic.", "", tab[cols].round(3).to_markdown(index=False), "",
          f"{m4_note}.", "", f"Choice (G6): **{winner}**" + (" (no candidate improved the base model)" if winner == "M0" else "")
          + f"; tied within 0.01: {', '.join(tied)}."]
    (OUT / "candidates.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
