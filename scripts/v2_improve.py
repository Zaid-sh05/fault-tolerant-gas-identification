"""Night study, HEAVY part (POST-HOC, decisions_log L2-L4, L7). Runs only after recalibration stage 2; Test never read.

Usage: python scripts/v2_improve.py [--jobs 3] [--limit-scenarios N]   (N: smoke test on the first N scenarios, writes to results/v2/improve_smoke)
Variants of A on the M0 base (fits of the arbiter run, results/v2/arbiter/<protocol>/fitted.joblib):
  V0 v1 detector (95th)        V1 max(v1, leave-pair-out) ratios (95th)    V2 v1 detector, 99th-percentile thresholds
  V3 V1 at 99th                V5 V0 + guarded reconstruction (sensors with ratio > 0.5 are also excluded from the predictors)
plus SVM, SVM+Aug (5 seeds), B with the v1 detector and the routing rules A -> {B, Aug} for n_flag >= t (confirmation of LR on Drift-Dev).
Scenarios: clean + k1, k2, k4 at medium severity, 5 seeds (561 per batch); Drift-Dev batches 6, 7 and Validation 7.
Outputs in results/v2/improve/: scenarios.csv, detector.csv, choice.json, IMPROVE.md (+ cached leave-pair-out detectors, chunks).
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402
from collections import defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

sys.path.insert(0, "scripts")
import v2_arbiter as arb  # noqa: E402
from ov3_detector import auc  # noqa: E402
from v2_dev import PROTOCOLS, load  # noqa: E402
from src.data import sensor_columns  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.scenarios import MEDIUM, apply_scenario, build_scenarios  # noqa: E402
from src.strategies import StrategyKit, acted_sets, group_by_set  # noqa: E402
from src.study import AUG_SEEDS  # noqa: E402

OUT = Path("results/v2/improve")
CHUNK, TS, B_BOOT, MARGIN = 20, (2, 3, 4, 5), 1000, 0.005
VARIANTS = ["V0", "V1", "V2", "V3", "V5"]
ORDER = ["V0", "V2", "V1", "V3", "V5"]                      # simplicity order of L4
SUSPECT = 0.5


def scenario_list():
    return [None] + [sc for sc in build_scenarios(AUG_SEEDS) if sc.level == MEDIUM[sc.fault]]


class Kit(StrategyKit):
    """Reduced B models: the arbiter cache first (Platt models, same decisions), else fitted without probability in our own cache."""

    def __init__(self, f, proto, out):
        params = {k: v for k, v in f["params"].items() if k != "probability"}
        super().__init__(f["pre"], f["svm"], f["Xt"], f["ytr"], f["det"], params, str(out / proto / "reduced"))
        self.arb_cache = arb.OUT / proto / "reduced"

    def reduced_model(self, pattern):
        if pattern not in self._reduced:
            p = self.arb_cache / ("B_" + ("none" if not pattern else "_".join(map(str, pattern))) + ".joblib")
            if p.exists():
                self._reduced[pattern] = joblib.load(p)
        return super().reduced_model(pattern)


def lpo_detector(proto, out):
    """Leave-pair-out detector on the protocol's Train rows. Validation 7: the saved v1 one (same Train rows and groups)."""
    if proto == "original":
        return joblib.load("results/overnight/temporal/detectors/median_lpo.joblib")
    path = out / proto / "det_lpo.joblib"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        Xtr, _, btr, _ = load(PROTOCOLS[proto])
        f = arb.fitted(proto, "M0")
        arb.atomic(path, lambda p: joblib.dump(ReliabilityDetector(normalization="median", lpo=True).fit(f["Xt"], btr), p))
    return joblib.load(path)


def rescale(det):
    n = det._normalise(det.E_oof_)
    return np.percentile(n, 95, axis=0) / np.percentile(n, 99, axis=0)


def guarded_reconstruct(det, Xf, R, sets):
    """A's reconstruction, but sensors with ratio > SUSPECT are also excluded from the predictors of every flagged block (V5)."""
    Zf = np.nan_to_num(det.to_z(Xf))
    Xr = Xf.copy()
    keys = defaultdict(list)
    for i, s in enumerate(sets):
        if s:
            keys[(s, tuple(np.flatnonzero(R[i] > SUSPECT)))].append(i)
    for (pattern, suspects), rows in keys.items():
        rows = np.array(rows)
        for s in pattern:
            z = det.block_prediction(Zf[rows], s, tuple(sorted((set(pattern) | set(suspects)) - {s})))
            Xr[np.ix_(rows, sensor_columns(s))] = det.from_z_block(z, sensor_columns(s))
    return Xr


def run_chunk(proto, batch, index, sids, out, light=False, routing=False):
    path = out / proto / f"b{batch}_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    f, dl = arb.fitted(proto, "M0"), lpo_detector(proto, out)
    d0, svm, pre = f["det"], f["svm"], f["pre"]
    s0, sl = rescale(d0), rescale(dl)
    X, y = load(PROTOCOLS[proto])[3][batch]
    kit = Kit(f, proto, out)
    Z = lambda A: fill_nan_zero(pre.transform(A))                                    # noqa: E731
    f1 = lambda p: scores(y, p)["macro_f1"]                                           # noqa: E731
    scen = scenario_list()
    rows = []
    for sid in sids:
        sc = scen[sid]
        Xf, truth = (X, np.zeros((len(X), 16), bool)) if sc is None else apply_scenario(X, sc, f["raw_stats"])
        R0, Rl = d0.ratio(Xf), dl.ratio(Xf)
        ratios = {"V0": R0, "V1": np.maximum(R0, Rl), "V2": R0 * s0, "V3": np.maximum(R0 * s0, Rl * sl), "V5": R0}
        Zf = Z(Xf)
        row = {"protocol": proto, "batch": batch, "sid": sid, **arb.scenario_info(sc), "svm": f1(fast_svm_predict(svm, Zf))}
        affected, healthy = truth.any(1), ~truth & truth.any(1)[:, None]
        for v, R in ratios.items():
            if routing and v != "V0":
                continue
            flags = R > 1.0
            sets = acted_sets(R, flags)
            Xr = guarded_reconstruct(d0, Xf, R, sets) if v == "V5" else kit.reconstruct(Xf, group_by_set(sets), False)
            row[v] = f1(fast_svm_predict(svm, Z(Xr)))
            row[f"{v}_far_clean_or_fpr"] = float(flags.mean() if sc is None else flags[healthy].mean())
            row[f"{v}_rows_with_alarm"] = float(flags.any(1).mean()) if sc is None else float("nan")
            if sc is not None and v != "V5":
                row[f"{v}_auroc"], row[f"{v}_tpr"] = auc(R[truth], R[healthy]), float(flags[truth].mean())
            if v == "V0":
                A0, n_flag, sets0 = fast_svm_predict(svm, Z(Xr)), flags.sum(1), sets
        if light:                                                                  # decisions_log L8: A variants only
            rows.append(row)
            continue
        B = kit.predict_B(Xf, sets0)
        augs = [fast_svm_predict(m, Zf) for m in f["svm_aug"]]
        row["B"], row["svm_aug"] = f1(B), float(np.mean([f1(g) for g in augs]))
        for t in TS:
            route = n_flag >= t
            row[f"B_t{t}"] = f1(np.where(route, B, A0))
            row[f"aug_t{t}"] = float(np.mean([f1(np.where(route, g, A0)) for g in augs]))
        rows.append(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    arb.atomic(path, lambda p: pickle.dump(rows, open(p, "wb")))
    return str(path)


def summary(df, methods):
    """per protocol: clean F1, mean under faults (k1, k2, k4 equal weight; Drift-Dev = mean of batches), worst case."""
    out = {}
    for proto, d in df.groupby("protocol"):
        per_b = []
        for _, db in d.groupby("batch"):
            fault = db[db.setting != "clean"]
            per_b.append({m: (float(db[db.setting == "clean"][m].iloc[0]),
                              float(np.mean([fault[fault.setting == k][m].mean() for k in ("k1", "k2", "k4")])),
                              float(db[m].min())) for m in methods})
        out[proto] = {m: tuple(float(np.mean([p[m][i] for p in per_b])) for i in range(3)) for m in methods}
    return out


def boot_gain(df, proto, m, ref="V0"):
    """Scenario bootstrap (inside each k and batch) of the gain of m over ref in the primary metric."""
    rng = np.random.default_rng(0)
    d = df[(df.protocol == proto) & (df.setting != "clean")]
    groups = [(b, k, np.flatnonzero(((d.batch == b) & (d.setting == k)).to_numpy())) for b in sorted(d.batch.unique()) for k in ("k1", "k2", "k4")]
    diff = (d[m] - d[ref]).to_numpy()

    def stat(idx_of):
        per_b = defaultdict(list)
        for (b, _, g), idx in zip(groups, idx_of):
            per_b[b].append(diff[idx].mean())
        return np.mean([np.mean(v) for v in per_b.values()])
    point = stat([g for _, _, g in groups])
    boots = [stat([rng.choice(g, len(g)) for _, _, g in groups]) for _ in range(B_BOOT)]
    return point, *np.percentile(boots, [2.5, 97.5])


def decide(df, light=False):
    methods = VARIANTS + ["svm"] + ([] if light else [f"{T}_t{t}" for T in ("B", "aug") for t in TS] + ["B", "svm_aug"])
    s = summary(df, methods)
    dev, val = s["drift_dev"], s["original"]
    base = dev["V0"]
    elig = [v for v in VARIANTS if dev[v][0] >= base[0] - MARGIN and dev[v][2] >= base[2]]
    best = max(dev[v][1] for v in elig)
    pick = min([v for v in elig if dev[v][1] >= best - MARGIN], key=ORDER.index)
    res = {"rule": "decisions_log L4 (select on Drift-Dev, confirm on Validation 7)", "post_hoc": True, "selected": pick}
    if pick != "V0":
        g, lo, hi = boot_gain(df, "drift_dev", pick)
        gv, lov, hiv = boot_gain(df, "original", pick)
        res.update(dev_gain=[g, lo, hi], val_gain=[gv, lov, hiv], val_clean_drop=val["V0"][0] - val[pick][0],
                   success=bool(lo > 0 and gv > 0 and lov > 0 and val["V0"][0] - val[pick][0] <= MARGIN))
    else:
        res.update(success=False, note="no variant beat V0 on Drift-Dev (within the tie margin)")
    lr = json.load(open("results/v2/light/lr_choice.json")) if Path("results/v2/light/lr_choice.json").exists() else {}
    if light:
        res["lr_confirmation"] = {"note": "not part of the light run (needs new reduced B models, L8)"}
    elif lr.get("selected") and lr.get("passes_validation_stage"):
        col = f"{lr['target']}_t{lr['t']}"
        g, lo, hi = boot_gain(df, "drift_dev", col)
        res["lr_confirmation"] = {"rule": col, "dev_gain_vs_A": [g, lo, hi], "dev_clean_drop": dev["V0"][0] - dev[col][0],
                                  "confirmed": bool(lo > 0 and dev["V0"][0] - dev[col][0] <= MARGIN)}
    else:
        res["lr_confirmation"] = {"confirmed": False, "note": "LR had no variant passing the Validation-7 stage"}
    return s, res


def confirm_routing(df):
    lr = json.load(open("results/v2/light/lr_choice.json"))
    if not (lr.get("selected") and lr.get("passes_validation_stage")):
        return {"confirmed": False, "note": "LR had no variant passing the Validation-7 stage"}
    col = f"{lr['target']}_t{lr['t']}"
    s = summary(df, ["V0", col, "B", "svm_aug", "svm"])["drift_dev"]
    g, lo, hi = boot_gain(df, "drift_dev", col)
    return {"rule": col, "dev_summary_clean_faults_worst": s, "dev_gain_vs_A": [g, lo, hi], "dev_clean_drop": s["V0"][0] - s[col][0],
            "confirmed": bool(lo > 0 and s["V0"][0] - s[col][0] <= MARGIN), "criteria": "decisions_log L7", "post_hoc": True}


def main(jobs, limit, only, light, routing=False):
    out = (Path("results/v2/improve_smoke") if limit else Path("results/v2/improve_light") if light
           else Path("results/v2/improve_routing") if routing else OUT)
    n = len(scenario_list()) if not limit else limit
    protos = [only] if only else ["drift_dev"] if routing else list(PROTOCOLS)
    for p in protos:
        lpo_detector(p, out)
        print(f"{p}: leave-pair-out detector ready", flush=True)
    tasks = [delayed(run_chunk)(p, b, i, list(range(a, min(a + CHUNK, n))), out, light, routing)
             for p in protos for b in load(PROTOCOLS[p])[3] for i, a in enumerate(range(0, n, CHUNK))]
    paths = Parallel(n_jobs=jobs, verbose=5)(tasks)
    df = pd.DataFrame([r for p in paths for r in pickle.load(open(p, "rb"))])
    df.round(5).to_csv(out / "scenarios.csv", index=False)
    if limit:
        print(df.head().to_string())
        return
    if routing:                                                                    # LR confirmation on Drift-Dev only (L7)
        res = confirm_routing(df)
        json.dump(res, open(out / "choice.json", "w"), indent=1)
        print(json.dumps(res, indent=1))
        return
    s, res = decide(df, light)
    json.dump(res, open(out / "choice.json", "w"), indent=1)
    tab = pd.DataFrame([{"protocol": p, "method": m, "clean": v[0], "mean_under_faults": v[1], "worst": v[2]}
                        for p, d in s.items() for m, v in d.items()])
    tab.round(4).to_csv(out / "summary.csv", index=False)
    det_cols = [c for c in df.columns if c.endswith(("_auroc", "_tpr"))]
    det = df[df.setting != "clean"].groupby(["protocol", "setting", "fault"])[det_cols].mean().reset_index()
    far = df[df.setting == "clean"].groupby("protocol")[[f"{v}_far_clean_or_fpr" for v in VARIANTS] + [f"{v}_rows_with_alarm" for v in VARIANTS]].mean()
    det.round(4).to_csv(out / "detector.csv", index=False)
    md = ["# Night study, heavy part (POST-HOC, decisions_log L2-L4, L7)", "", tab.round(4).to_markdown(index=False), "",
          "Clean false alarms (share of sensor-rows) and rows with an alarm:", "", far.round(4).to_markdown(), "",
          "Detector (isolation AUROC, TPR):", "", det.round(3).to_markdown(index=False), "", "```", json.dumps(res, indent=1), "```"]
    (out / "IMPROVE.md").write_text(chr(10).join(md), encoding="utf-8")
    print(chr(10).join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--limit-scenarios", type=int, default=0)
    ap.add_argument("--only", choices=list(PROTOCOLS), default=None, help="smoke tests only")
    ap.add_argument("--light", action="store_true", help="A variants only, no B / augmentation / routing (decisions_log L8)")
    ap.add_argument("--routing", action="store_true", help="LR confirmation on Drift-Dev only: V0, B, augmentation, routing (heavy)")
    a = ap.parse_args()
    assert not a.only or a.limit_scenarios, "--only is for smoke tests"
    main(a.jobs, a.limit_scenarios, a.only, a.light, a.routing)
