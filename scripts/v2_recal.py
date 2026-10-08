"""Few-shot recalibration with n labeled samples per gas (POST-HOC, decisions_log J0-J7). Batches 1-7 only.

Usage: python scripts/v2_recal.py --stage clean            # J4: clean scores for n in {5, 10}, 5 seeds; choice of n
       python scripts/v2_recal.py --stage faults [--jobs 3] # J5: fault layer + arbiters on the calibrated model (chosen n), 5 seeds
Outputs in results/v2/recal/. For every evaluation batch: per gas min(n, count // 2) rows of the CLEAN batch are drawn (seed, keyed by
batch and n), added to the Train rows (one extra detector group) and removed from scoring for good; the uncalibrated M0 is scored on
the same remaining rows. Faults are applied to the full batch matrix, exactly as in the uncalibrated runs.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

sys.path.insert(0, "scripts")
import v2_arbiter as arb  # noqa: E402
from v2_dev import PROTOCOLS, build, load  # noqa: E402
from src.models import scores  # noqa: E402
from src.scenarios import FaultStats  # noqa: E402

OUT = Path("results/v2/recal")
NS, SEEDS, BASE = (5, 10), (0, 1, 2, 3, 4), "M0"
CAL_GROUP = 1000                                      # detector group id of the calibration rows (+ batch)


def calib_rows(y, n, seed, batch):
    """Indices of the calibration rows: per gas min(n, count // 2), drawn without replacement."""
    rng = np.random.default_rng([seed, n, batch])
    idx = [rng.choice(np.flatnonzero(y == g), min(n, int((y == g).sum()) // 2), replace=False) for g in np.unique(y)]
    return np.sort(np.concatenate(idx)).astype(int)


def adapted(Xtr, ytr, btr, X, y, cal, batch):
    return (np.vstack([Xtr, X[cal]]), np.r_[ytr, y[cal]], np.r_[btr, np.full(len(cal), CAL_GROUP + batch)])


# ---- stage 1 (J4) ------------------------------------------------------------------------------------
def clean_task(proto, batch, n, seed):
    Xtr, ytr, btr, evals = load(PROTOCOLS[proto])
    X, y = evals[batch]
    cal = calib_rows(y, n, seed, batch)
    keep = np.ones(len(y), bool)
    keep[cal] = False
    _, _, p_cal = build(BASE, *adapted(Xtr, ytr, btr, X, y, cal, batch))
    _, _, p_unc = build(BASE, Xtr, ytr, btr)
    pc, pu = p_cal(X), p_unc(X)
    return {"protocol": proto, "batch": batch, "n": n, "cal_seed": seed, "n_cal_rows": len(cal), "n_scored": int(keep.sum()),
            "calibrated": scores(y[keep], pc[keep])["macro_f1"], "uncalibrated": scores(y[keep], pu[keep])["macro_f1"]}


def stage_clean(jobs):
    tasks = [(p, b, n, s) for p in PROTOCOLS for b in load(PROTOCOLS[p])[3] for n in NS for s in SEEDS]
    df = pd.DataFrame(Parallel(n_jobs=jobs, verbose=5)(delayed(clean_task)(*t) for t in tasks))
    df["gain"] = df["calibrated"] - df["uncalibrated"]
    per = df.groupby(["protocol", "batch", "n"]).agg(calibrated=("calibrated", "mean"), calibrated_std=("calibrated", "std"),
                                                     uncalibrated=("uncalibrated", "mean"), gain=("gain", "mean"),
                                                     gain_std=("gain", "std"), n_cal_rows=("n_cal_rows", "mean")).reset_index()
    gain = {n: float(per[per.n == n].groupby("protocol")["gain"].mean().mean()) for n in NS}   # Drift-Dev mean of 6, 7; then with Val 7
    if gain[10] <= 0:
        n_star, verdict = None, "calibration does not help (gain(10) <= 0): no fault layer (J4)"
    else:
        n_star = 5 if gain[5] >= 0.9 * gain[10] else 10
        verdict = f"n* = {n_star}: gain(5) = {gain[5]:.4f}, 0.9 * gain(10) = {0.9 * gain[10]:.4f}"
    OUT.mkdir(parents=True, exist_ok=True)
    df.round(5).to_csv(OUT / "clean_trials.csv", index=False)
    per.round(4).to_csv(OUT / "clean_summary.csv", index=False)
    json.dump({"gain": gain, "n_star": n_star, "verdict": verdict, "rule": "decisions_log J4", "post_hoc": True},
              open(OUT / "choice.json", "w"), indent=1)
    print(per.round(3).to_markdown(index=False))
    print(verdict)


# ---- stage 2 (J5) ------------------------------------------------------------------------------------
def config_dir(proto, batch, n, seed):
    return OUT / f"{proto}_b{batch}_n{n}_s{seed}"


def fit_config(proto, batch, n, seed):
    path = config_dir(proto, batch, n, seed) / "fitted.joblib"
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    Xtr, ytr, btr, evals = load(PROTOCOLS[proto])
    X, y = evals[batch]
    f = arb.fit_layer(BASE, *adapted(Xtr, ytr, btr, X, y, calib_rows(y, n, seed, batch), batch), FaultStats.fit(Xtr))
    arb.atomic(path, lambda p: joblib.dump(f, p))


def keep_mask(y, n, seed, batch):
    keep = np.ones(len(y), bool)
    keep[calib_rows(y, n, seed, batch)] = False
    return keep


def calibrated_chunk(proto, batch, n, seed, index, sids):
    d = config_dir(proto, batch, n, seed)
    path = d / "chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    f = joblib.load(d / "fitted.joblib")
    X, y = load(PROTOCOLS[proto])[3][batch]
    kit, scen, keep = arb.make_kit(f, d / "reduced"), arb.scenario_list(), keep_mask(y, n, seed, batch)
    rows = []
    for sid in sids:
        lab, n_flag = arb.predict_scenario(f, kit, X, scen[sid])
        rows.append({"model": "calibrated", "protocol": proto, "batch": batch, "n": n, "cal_seed": seed, "sid": sid,
                     **arb.scenario_info(scen[sid]), **arb.score_row(lab, n_flag, y, keep)})
    path.parent.mkdir(exist_ok=True)
    arb.atomic(path, lambda p: pickle.dump(rows, open(p, "wb")))
    return str(path)


def uncalibrated_chunk(proto, batch, n, index, sids):
    """The uncalibrated M0 (fits and reduced models of the arbiter run), predicted once per scenario, scored on each seed's rows."""
    path = OUT / f"uncal_{proto}_b{batch}_n{n}" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    f = arb.fitted(proto, BASE)
    X, y = load(PROTOCOLS[proto])[3][batch]
    kit, scen = arb.make_kit(f, arb.OUT / proto / "reduced"), arb.scenario_list()
    rows = []
    for sid in sids:
        lab, n_flag = arb.predict_scenario(f, kit, X, scen[sid])
        for seed in SEEDS:
            rows.append({"model": "uncalibrated", "protocol": proto, "batch": batch, "n": n, "cal_seed": seed, "sid": sid,
                         **arb.scenario_info(scen[sid]), **arb.score_row(lab, n_flag, y, keep_mask(y, n, seed, batch))})
    path.parent.mkdir(parents=True, exist_ok=True)
    arb.atomic(path, lambda p: pickle.dump(rows, open(p, "wb")))
    return str(path)


def stage_faults(jobs):
    n_star = json.load(open(OUT / "choice.json"))["n_star"]
    assert n_star, "J4: calibration did not help; no fault layer"
    assert (arb.OUT / "base_model.txt").read_text().strip() == BASE
    batches = {p: list(load(PROTOCOLS[p])[3]) for p in PROTOCOLS}
    for p in PROTOCOLS:
        for b in batches[p]:
            for s in SEEDS:
                fit_config(p, b, n_star, s)
                print(f"fitted {p} b{b} n{n_star} seed {s}", flush=True)
    n_sc = len(arb.scenario_list())
    starts = list(enumerate(range(0, n_sc, arb.CHUNK)))
    tasks = [delayed(calibrated_chunk)(p, b, n_star, s, i, list(range(a, min(a + arb.CHUNK, n_sc))))
             for p in PROTOCOLS for b in batches[p] for s in SEEDS for i, a in starts]
    tasks += [delayed(uncalibrated_chunk)(p, b, n_star, i, list(range(a, min(a + arb.CHUNK, n_sc))))
              for p in PROTOCOLS for b in batches[p] for i, a in starts]
    paths = Parallel(n_jobs=jobs, verbose=5)(tasks)
    df = pd.DataFrame([r for p in paths for r in pickle.load(open(p, "rb"))])
    df.round(5).to_csv(OUT / "scenarios.csv", index=False)
    report(df, n_star)


def report(df, n_star):
    df = arb.add_retention(df, ["model", "protocol", "batch", "cal_seed"])
    m = arb.METHODS
    r = [f"retention_{x}" for x in m]
    per_seed = df.groupby(["model", "protocol", "batch", "cal_seed", "setting"])[m + r].mean().reset_index()
    per_seed = per_seed.groupby(["model", "protocol", "cal_seed", "setting"])[m + r].mean().reset_index()   # Drift-Dev: mean of 6, 7
    mean = per_seed.groupby(["model", "protocol", "setting"])[m + r].mean().reset_index()
    std = per_seed.groupby(["model", "protocol", "setting"])[m].std().reset_index()
    by_fault = (df.groupby(["model", "protocol", "batch", "cal_seed", "setting", "fault"])[m + r].mean().reset_index()
                .groupby(["model", "protocol", "setting", "fault"])[m + r].mean().reset_index())
    worst = df.groupby(["model", "protocol", "batch", "cal_seed"])[m].min().reset_index().groupby(["model", "protocol"])[m].mean().reset_index()
    for name, tab in (("settings_mean", mean), ("settings_std", std), ("by_fault", by_fault), ("worst_case", worst)):
        tab.round(4).to_csv(OUT / f"{name}.csv", index=False)
    cols = ["model", "protocol", "setting"] + m
    fmt = mean[cols].round(3).astype(str)
    for x in m:                                                               # mean +- std over the 5 calibration seeds
        fmt[x] = mean[x].map("{:.3f}".format) + " ± " + std[x].map("{:.3f}".format)
    ret = mean[["model", "protocol", "setting"] + r].rename(columns=lambda c: c.replace("retention_", ""))
    md = [f"# Few-shot recalibration, n = {n_star} labeled samples per gas (POST-HOC, decisions_log J)", "",
          "Setting: 'with n labeled calibration samples per gas'. Both models are scored on the SAME rows (calibration rows removed). "
          "Mean ± std over 5 calibration seeds; Drift-Dev = mean of batches 6 and 7.", "", fmt.to_markdown(index=False), "",
          "## Retention (Macro-F1 with the fault / clean Macro-F1, same method, model, batch and seed)", "",
          ret[ret.setting != "clean"].round(3).to_markdown(index=False), "", "## Worst case (lowest per-scenario Macro-F1, mean over seeds)", "",
          worst.round(3).to_markdown(index=False)]
    (OUT / "RECAL.md").write_text(chr(10).join(md), encoding="utf-8")
    print(chr(10).join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["clean", "faults", "report"], required=True)
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    if a.stage == "clean":
        stage_clean(a.jobs)
    elif a.stage == "faults":
        stage_faults(a.jobs)
    else:
        report(pd.read_csv(OUT / "scenarios.csv"), json.load(open(OUT / "choice.json"))["n_star"])
