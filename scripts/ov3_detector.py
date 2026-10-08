"""Overnight Part 3: reliability detector and gate G2.

Usage: python scripts/ov3_detector.py --config configs/preprocessing.yaml --name temporal
       python scripts/ov3_detector.py --config configs/reference_iid.yaml --name reference_iid --reduced
Outputs: results/overnight/<name>/{detectors/*.joblib, detector_scenarios.csv, detector_summary.csv,
         far_by_gas.csv, reliability_ranking.csv, oof_alarm_rate.csv, g2_verdict.json}
Rules are in results/decisions_log.md (B5-B9). Detectors are fitted on Train only; thresholds come from the Train
out-of-fold scores; the normalisation (a: per sensor, b: median over sensors) is chosen on Validation by the median
isolation AUROC over the four fault types at k=1, medium severity. Dropout is detected by definition (NaN block).
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from sklearn.metrics import roc_auc_score  # noqa: E402

from src.data import GAS_NAMES  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.scenarios import MEDIUM, apply_scenario, build_scenarios  # noqa: E402
from src.study import AUG_SEEDS, Study  # noqa: E402

VARIANTS = {"sensor": dict(normalization="sensor"), "median": dict(normalization="median"),
            "sensor_lpo": dict(normalization="sensor", lpo=True), "median_lpo": dict(normalization="median", lpo=True)}
CHUNK = 60
BIG = 1e30


def auc(pos, neg):
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    s = np.nan_to_num(np.r_[pos, neg], posinf=BIG)
    return roc_auc_score(y, s)


def load_detectors(study):
    return {k: joblib.load(study.dir / "detectors" / f"{k}.joblib") for k in VARIANTS}


def run_chunk(cfg_path, name, reduced, index, sids):
    study = Study(cfg_path, name)
    path = study.dir / "ov3_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    dets = load_detectors(study)
    scenarios = build_scenarios(AUG_SEEDS, ("k1", "k2") if reduced else ("k1", "k2", "k4"), reduced)
    clean = {k: d.ratio(study.Xev) for k, d in dets.items()}
    rows = []
    for sid in sids:
        sc = scenarios[sid]
        Xf, truth = apply_scenario(study.Xev, sc, study.stats)
        affected = truth.any(1)
        sens = list(sc.sensors)
        for k, det in dets.items():
            R = det.ratio(Xf)
            healthy = ~truth & affected[:, None]
            alarms = R > 1.0
            rows.append({"sid": sid, "detector": k,
                         "auroc_isolation": auc(R[truth], R[healthy]),
                         "auroc_vs_clean_copy": auc(R[:, sens][truth[:, sens]], clean[k][:, sens].ravel()),
                         "tpr": float(alarms[truth].mean()),
                         "fpr_healthy_same_rows": float(alarms[healthy].mean()),
                         "any_alarm_unaffected_rows": float(alarms[~affected].any(1).mean()) if (~affected).any() else np.nan})
    path.parent.mkdir(exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(rows, f)
    return str(path)


def main(cfg_path, name, reduced, jobs=6):
    study = Study(cfg_path, name)
    (study.dir / "detectors").mkdir(exist_ok=True)
    for k, kw in VARIANTS.items():
        if not (study.dir / "detectors" / f"{k}.joblib").exists():
            joblib.dump(ReliabilityDetector(**kw).fit(study.Xtr, study.proto.groups), study.dir / "detectors" / f"{k}.joblib")
    dets = load_detectors(study)
    print({k: dict(alpha=d.alpha_.tolist()) for k, d in list(dets.items())[:1]}, flush=True)

    scenarios = build_scenarios(AUG_SEEDS, ("k1", "k2") if reduced else ("k1", "k2", "k4"), reduced)
    sids = list(range(len(scenarios)))
    chunks = [sids[i:i + CHUNK] for i in range(0, len(sids), CHUNK)]
    Parallel(n_jobs=jobs, verbose=5)(delayed(run_chunk)(cfg_path, name, reduced, i, c) for i, c in enumerate(chunks))
    rows = []
    for i in range(len(chunks)):
        with open(study.dir / "ov3_chunks" / f"chunk_{i:03d}.pkl", "rb") as f:
            rows += pickle.load(f)
    res = pd.DataFrame(rows).merge(pd.read_csv(study.dir / "scenarios.csv"), on="sid")
    res.to_csv(study.dir / "detector_scenarios.csv", index=False)

    keys = ["detector", "kset", "fault", "level"]
    summ = (res.groupby(keys).agg(n=("sid", "size"), auroc_isolation=("auroc_isolation", "mean"),
                                  auroc_isolation_std=("auroc_isolation", "std"),
                                  auroc_vs_clean_copy=("auroc_vs_clean_copy", "mean"), tpr=("tpr", "mean"),
                                  fpr_healthy_same_rows=("fpr_healthy_same_rows", "mean")).reset_index())
    summ.round(4).to_csv(study.dir / "detector_summary.csv", index=False)

    # ---- choice of normalisation and G2 ----------------------------------------------------
    def g2_value(det):
        s = summ[(summ.detector == det) & (summ.kset == "k1")]
        per_type = {f: float(s[(s.fault == f) & (s.level == MEDIUM[f])]["auroc_isolation"].iloc[0]) for f in MEDIUM}
        return float(np.median(list(per_type.values()))), per_type
    cand = {k: g2_value(k) for k in ("sensor", "median")}
    chosen = "median" if cand["median"][0] > cand["sensor"][0] else "sensor"
    value, per_type = cand[chosen]
    verdict = {"candidates_median_auroc": {k: v[0] for k, v in cand.items()}, "chosen_normalisation": chosen,
               "isolation_auroc_by_fault_k1_medium": per_type, "median_auroc": value, "G2_passes": value >= 0.80,
               "note": "Dropout is detected by definition (NaN block), so its AUROC is trivial",
               "secondary_leave_pair_out": {k: g2_value(k)[0] for k in ("sensor_lpo", "median_lpo")},
               "rule": "results/decisions_log.md B6, B8"}
    json.dump(verdict, open(study.dir / "g2_verdict.json", "w"), indent=1)
    print(json.dumps(verdict, indent=1))

    # ---- false alarms on the clean evaluation rows, reliability ranking -------------------------------
    far, rank, oof = [], [], []
    gas = study.proto.eval["gas"].to_numpy()
    for k, det in dets.items():
        R = det.ratio(study.Xev)
        A = R > 1.0
        for g in [None] + sorted(set(gas)):
            m = np.ones(len(A), bool) if g is None else gas == g
            for label, cols in (("all sensors", list(range(16))), ("without S01,S02", list(range(2, 16)))):
                far.append({"detector": k, "gas": "all" if g is None else GAS_NAMES[g], "sensors": label, "rows": int(m.sum()),
                            "alarm_rate_per_sensor_row": float(A[m][:, cols].mean()),
                            "rows_with_any_alarm": float(A[m][:, cols].any(1).mean())})
        order = np.argsort(-np.median(R, axis=0))
        for pos, s in enumerate(order, 1):
            rank.append({"detector": k, "rank_from_least_reliable": pos, "sensor": f"S{s + 1:02d}",
                         "median_ratio": float(np.median(R[:, s])), "alarm_rate": float(A[:, s].mean())})
        N_oof = det._normalise(det.E_oof_)
        oof += [{"detector": k, "sensor": f"S{s + 1:02d}", "oof_alarm_rate": float((N_oof[:, s] / det.tau_[s] > 1).mean())}
                for s in range(16)]
    pd.DataFrame(far).round(4).to_csv(study.dir / "far_by_gas.csv", index=False)
    pd.DataFrame(rank).round(4).to_csv(study.dir / "reliability_ranking.csv", index=False)
    pd.DataFrame(oof).round(4).to_csv(study.dir / "oof_alarm_rate.csv", index=False)
    pd.set_option("display.width", 200)
    f = pd.DataFrame(far)
    print(f[(f.detector == chosen) & (f.gas == "all")].round(4).to_string(index=False))
    print(pd.DataFrame(rank)[lambda d: d.detector == chosen].head(6).round(3).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/preprocessing.yaml")
    ap.add_argument("--name", default="temporal")
    ap.add_argument("--reduced", action="store_true")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    main(a.config, a.name, a.reduced, a.jobs)
