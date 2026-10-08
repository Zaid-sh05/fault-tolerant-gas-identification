"""Final test: reliability detector per evaluation batch and pooled (AUROC, hit and false-alarm rates, ranking).

Usage: python scripts/ft_detector.py --config configs/final_test.yaml --name test
Needs ov2_faults_g1.py (scenarios) and ov3_detector.py run with --frozen-choice (detectors, g2_verdict.json).
Outputs in <output_root>/<name>/: ft_detector_scenarios.csv, ft_detector_summary.csv, ft_g2_by_subset.json,
ft_far_by_gas.csv, ft_reliability_ranking.csv.
The detectors are the Validation-time ones (fitted on Train, thresholds from Train out-of-fold scores) and are not touched.
The primary detector is the frozen choice; the other three variants are reported as sensitivity analyses.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

sys.path.insert(0, "scripts")
from ov3_detector import VARIANTS, auc, load_detectors  # noqa: E402
from src.data import GAS_NAMES  # noqa: E402
from src.scenarios import MEDIUM, apply_scenario, build_scenarios  # noqa: E402
from src.study import AUG_SEEDS, Study  # noqa: E402

CHUNK = 60


def subsets_of(study):
    batch = study.proto.eval["batch"].to_numpy()
    return {"pooled": np.ones(len(batch), dtype=bool), **{f"b{b}": batch == b for b in sorted(set(batch))}}


def run_chunk(cfg_path, name, index, sids):
    study = Study(cfg_path, name)
    path = study.dir / "ft_det_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    dets, scenarios, subsets = load_detectors(study), build_scenarios(AUG_SEEDS), subsets_of(study)
    rows = []
    for sid in sids:
        Xf, truth = apply_scenario(study.Xev, scenarios[sid], study.stats)
        healthy = ~truth & truth.any(1)[:, None]
        for k, det in dets.items():
            R = det.ratio(Xf)
            alarms = R > 1.0
            for sname, sel in subsets.items():
                t, h = truth & sel[:, None], healthy & sel[:, None]
                rows.append({"sid": sid, "detector": k, "subset": sname, "auroc_isolation": auc(R[t], R[h]),
                             "tpr": float(alarms[t].mean()) if t.any() else np.nan,
                             "fpr_healthy_same_rows": float(alarms[h].mean()) if h.any() else np.nan})
    path.parent.mkdir(exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(rows, f)
    return str(path)


def main(cfg_path, name, jobs=6):
    study = Study(cfg_path, name)
    scenarios = build_scenarios(AUG_SEEDS)
    chunks = [list(range(i, min(i + CHUNK, len(scenarios)))) for i in range(0, len(scenarios), CHUNK)]
    Parallel(n_jobs=jobs, verbose=5)(delayed(run_chunk)(cfg_path, name, i, c) for i, c in enumerate(chunks))
    rows = []
    for i in range(len(chunks)):
        with open(study.dir / "ft_det_chunks" / f"chunk_{i:03d}.pkl", "rb") as f:
            rows += pickle.load(f)
    res = pd.DataFrame(rows).merge(pd.read_csv(study.dir / "scenarios.csv"), on="sid")
    res.to_csv(study.dir / "ft_detector_scenarios.csv", index=False)
    keys = ["subset", "detector", "kset", "fault", "level"]
    summ = (res.groupby(keys).agg(n=("sid", "size"), auroc_isolation=("auroc_isolation", "mean"), tpr=("tpr", "mean"),
                                  fpr_healthy_same_rows=("fpr_healthy_same_rows", "mean")).reset_index())
    summ.round(4).to_csv(study.dir / "ft_detector_summary.csv", index=False)

    chosen = json.load(open(study.dir / "g2_verdict.json"))["chosen_normalisation"]
    g2 = {}
    for sname in subsets_of(study):
        per_det = {}
        for k in VARIANTS:
            s = summ[(summ.subset == sname) & (summ.detector == k) & (summ.kset == "k1")]
            per_type = {f: float(s[(s.fault == f) & (s.level == MEDIUM[f])]["auroc_isolation"].iloc[0]) for f in MEDIUM}
            per_det[k] = {"median_auroc": float(np.nanmedian(list(per_type.values()))), "by_fault": per_type}
        g2[sname] = {"primary": chosen, "G2_passes": per_det[chosen]["median_auroc"] >= 0.80, "detectors": per_det}
    json.dump(g2, open(study.dir / "ft_g2_by_subset.json", "w"), indent=1)

    # ---- clean evaluation rows: false alarms per gas (with / without S01, S02) and sensor ranking --------------
    gas = study.proto.eval["gas"].to_numpy()
    far, rank = [], []
    for k, det in load_detectors(study).items():
        R = det.ratio(study.Xev)
        A = R > 1.0
        for sname, sel in subsets_of(study).items():
            for g in [None] + sorted(set(gas[sel])):
                m = sel if g is None else sel & (gas == g)
                for label, cols in (("all sensors", list(range(16))), ("without S01,S02", list(range(2, 16)))):
                    far.append({"subset": sname, "detector": k, "gas": "all" if g is None else GAS_NAMES[g], "sensors": label,
                                "rows": int(m.sum()), "alarm_rate_per_sensor_row": float(A[m][:, cols].mean()),
                                "rows_with_any_alarm": float(A[m][:, cols].any(1).mean())})
            order = np.argsort(-np.median(R[sel], axis=0))
            for pos, s in enumerate(order, 1):
                rank.append({"subset": sname, "detector": k, "rank_from_least_reliable": pos, "sensor": f"S{s + 1:02d}",
                             "median_ratio": float(np.median(R[sel][:, s])), "alarm_rate": float(A[sel][:, s].mean())})
    pd.DataFrame(far).round(4).to_csv(study.dir / "ft_far_by_gas.csv", index=False)
    pd.DataFrame(rank).round(4).to_csv(study.dir / "ft_reliability_ranking.csv", index=False)
    print(json.dumps({s: {"G2": v["G2_passes"], "median_auroc": round(v["detectors"][chosen]["median_auroc"], 4)}
                      for s, v in g2.items()}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/final_test.yaml")
    ap.add_argument("--name", default="test")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    main(a.config, a.name, a.jobs)
