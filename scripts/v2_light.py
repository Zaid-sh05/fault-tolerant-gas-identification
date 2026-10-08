"""Night study, LIGHT part (POST-HOC, decisions_log L7). No fitting; Test never read.

Usage: python scripts/v2_light.py
  LD  detector variants on Validation 7 (saved v1 detectors): isolation AUROC, TPR, clean FAR, masking at k=2 (descriptive)
  LR  routing A -> T for rows with n_flag >= t, on Validation 7 from the saved v1 per-row predictions (selection, rule L4/L7)
  LA  A as partial drift correction: clean A - SVM per batch and per-sensor attribution (Validation 7 and Drift-Dev 6, 7; inference only)
Outputs in results/v2/light/: ld_detector.csv, ld_masking.csv, lr_variants.csv, lr_choice.json, la_clean.csv, la_attribution.csv, LIGHT.md
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, "scripts")
import v2_arbiter as arb  # noqa: E402
from ov3_detector import auc  # noqa: E402
from ov4_strategies import make_kit  # noqa: E402
from v2_dev import PROTOCOLS, load  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.models import scores  # noqa: E402
from src.scenarios import MEDIUM, apply_scenario, build_scenarios  # noqa: E402
from src.strategies import acted_sets  # noqa: E402
from src.study import AUG_SEEDS, Study  # noqa: E402

OUT = Path("results/v2/light")
V1 = Path("results/overnight/temporal")
TS, TARGETS, B_BOOT, MARGIN = (2, 3, 4, 5), ("B", "aug"), 1000, 0.005


def f1(y, p):
    return scores(y, p)["macro_f1"]


def tau(det, pct):
    return np.percentile(det._normalise(det.E_oof_), pct, axis=0)


def variants(R0, Rl, s0, sl):
    """ratios of D0..D3; s0/sl rescale the 95th-percentile ratios to 99th-percentile ones."""
    return {"D0": R0, "D1": np.maximum(R0, Rl), "D2": R0 * s0, "D3": np.maximum(R0 * s0, Rl * sl)}


def strat_boot(diff, kset, rng):
    """Equal-weight mean over k groups of per-scenario differences; bootstrap resamples scenarios inside each k."""
    groups = [np.flatnonzero(kset == k) for k in ("k1", "k2", "k4")]
    point = np.mean([diff[g].mean() for g in groups])
    boots = np.array([np.mean([diff[rng.choice(g, len(g))].mean() for g in groups]) for _ in range(B_BOOT)])
    return point, *np.percentile(boots, [2.5, 97.5])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    study = Study("configs/preprocessing.yaml", "temporal")                      # Train 1-6, Validation 7 (v1 objects)
    X, y = study.Xev, study.yev
    d0, dl = joblib.load(V1 / "detectors" / "median.joblib"), joblib.load(V1 / "detectors" / "median_lpo.joblib")
    s0, sl = tau(d0, 95) / tau(d0, 99), tau(dl, 95) / tau(dl, 99)
    scen = build_scenarios(AUG_SEEDS)
    masks = np.load(V1 / "truth_masks.npz")["masks"]
    sp, bp = np.load(V1 / "strategy_preds.npz"), np.load(V1 / "baseline_preds.npz")
    A_all, B_all = sp["A_det_twin"], sp["B_det"]
    aug_all = [bp[f"svm_aug{s}"] for s in AUG_SEEDS]
    medium = [sc for sc in scen if sc.level == MEDIUM[sc.fault]]

    # ---- alignment check: the saved truth masks must equal the re-applied scenarios ---------------------------------
    for sc in medium[::37]:
        _, truth = apply_scenario(X, sc, study.stats)
        saved = np.unpackbits(masks[sc.sid])[:len(X) * 16].reshape(len(X), 16).astype(bool)
        assert np.array_equal(truth, saved), f"saved outputs are not aligned with scenario {sc.sid}"

    # ---- clean rows ---------------------------------------------------------------------------------------------------
    kit, det = make_kit(study)
    assert det.normalization == "median"
    R0c, Rlc = d0.ratio(X), dl.ratio(X)
    sets_c = acted_sets(R0c, R0c > 1.0)
    missing = [p for p in set(sets_c) if not (V1 / "reduced" / ("B_" + ("none" if not p else "_".join(map(str, p))) + ".joblib")).exists()]
    assert not missing, f"v1 reduced models missing for {missing[:5]}: this script must not fit or write into the v1 folder"
    svm_c = fast_svm_predict(kit.svm, fill_nan_zero(study.pre.transform(X)))
    A_c, B_c = kit.predict_A(X, sets_c, False), kit.predict_B(X, sets_c)
    aug_models = study.models()
    aug_c = [fast_svm_predict(aug_models[f"svm_aug{s}"], fill_nan_zero(study.pre.transform(X))) for s in AUG_SEEDS]
    ref = pd.read_csv(V1 / "strategy_clean_eval.csv").set_index("method")["macro_f1"]
    assert abs(f1(y, A_c) - ref["A_det_twin"]) < 5e-4 and abs(f1(y, svm_c) - ref["clean_svm_no_handling"]) < 5e-4, "clean A/SVM do not reproduce v1"

    # ---- LD + LR over the medium scenarios --------------------------------------------------------------------------
    ld, lr, mask_rows = [], [], []
    nflag_c = (R0c > 1).sum(1)
    for sc in medium:
        Xf, truth = apply_scenario(X, sc, study.stats)
        R0, Rl = d0.ratio(Xf), dl.ratio(Xf)
        affected = truth.any(1)
        healthy = ~truth & affected[:, None]
        for name, R in variants(R0, Rl, s0, sl).items():
            flags = R > 1.0
            ld.append({"variant": name, "sid": sc.sid, "kset": sc.kset, "fault": sc.fault, "auroc": auc(R[truth], R[healthy]),
                       "tpr": float(flags[truth].mean()), "fpr_healthy_same_rows": float(flags[healthy].mean())})
            if sc.kset == "k2":
                pair = list(sc.sensors)
                mask_rows.append({"variant": name, "sid": sc.sid, "fault": sc.fault, "pair_tpr": float(flags[:, pair][truth[:, pair]].mean()),
                                  "healthy_alarm_rate_faulted_rows": float(flags[healthy].mean())})
        n_flag = (R0 > 1).sum(1)
        A, B, augs = A_all[sc.sid], B_all[sc.sid], [a[sc.sid] for a in aug_all]
        row = {"sid": sc.sid, "kset": sc.kset, "fault": sc.fault, "A": f1(y, A)}
        for t in TS:
            route = n_flag >= t
            row[f"B_t{t}"] = f1(y, np.where(route, B, A))
            row[f"aug_t{t}"] = float(np.mean([f1(y, np.where(route, g, A)) for g in augs]))
            row[f"share_routed_t{t}"] = float(route.mean())
        lr.append(row)
    ld, mask_df, lr = pd.DataFrame(ld), pd.DataFrame(mask_rows), pd.DataFrame(lr)

    clean = {"variant": [], "FAR_clean": [], "rows_with_alarm_clean": []}
    for name, R in variants(R0c, Rlc, s0, sl).items():
        clean["variant"].append(name)
        clean["FAR_clean"].append(float((R > 1).mean()))
        clean["rows_with_alarm_clean"].append(float((R > 1).any(1).mean()))
    ld_tab = ld.groupby(["variant", "kset", "fault"])[["auroc", "tpr", "fpr_healthy_same_rows"]].mean().reset_index()
    ld_tab.round(4).to_csv(OUT / "ld_detector.csv", index=False)
    pd.DataFrame(clean).round(4).to_csv(OUT / "ld_clean_far.csv", index=False)
    mask_tab = mask_df.groupby(["variant", "fault"])[["pair_tpr", "healthy_alarm_rate_faulted_rows"]].mean().reset_index()
    mask_tab.round(4).to_csv(OUT / "ld_masking.csv", index=False)

    # ---- LR selection (L4 with roles swapped, L7) -----------------------------------------------------------------------
    rng = np.random.default_rng(0)
    kset = lr["kset"].to_numpy()
    base = {"clean": f1(y, A_c), "faults": float(np.mean([lr[kset == k]["A"].mean() for k in ("k1", "k2", "k4")])),
            "worst": float(min(lr["A"].min(), f1(y, A_c)))}
    rows = [{"variant": "A (v1)", "target": "-", "t": "-", "clean": base["clean"], "faults": base["faults"], "worst": base["worst"],
             "gain": 0.0, "ci_low": 0.0, "ci_high": 0.0, "share_routed_clean": 0.0, "eligible": True}]
    for T in TARGETS:
        for t in TS:
            route_c = nflag_c >= t
            clean_f1 = (f1(y, np.where(route_c, B_c, A_c)) if T == "B"
                        else float(np.mean([f1(y, np.where(route_c, g, A_c)) for g in aug_c])))
            col = f"{T}_t{t}"
            gain, lo, hi = strat_boot((lr[col] - lr["A"]).to_numpy(), kset, rng)
            worst = float(min(lr[col].min(), clean_f1))
            rows.append({"variant": f"A->{T} if n_flag>={t}", "target": T, "t": t, "clean": clean_f1,
                         "faults": float(np.mean([lr[kset == k][col].mean() for k in ("k1", "k2", "k4")])), "worst": worst,
                         "gain": gain, "ci_low": lo, "ci_high": hi, "share_routed_clean": float(route_c.mean()),
                         "eligible": clean_f1 >= base["clean"] - MARGIN and worst >= base["worst"]})
    tab = pd.DataFrame(rows)
    elig = tab[(tab.variant != "A (v1)") & tab.eligible]
    choice = {"rule": "decisions_log L4 with roles swapped (L7): selection on Validation 7, confirmation on Drift-Dev", "post_hoc": True}
    if len(elig) and elig["faults"].max() > base["faults"]:
        best = elig["faults"].max()
        tied = elig[elig["faults"] >= best - MARGIN].copy()
        tied["order"] = -tied["t"].astype(int) * 10 + tied["target"].map({"B": 0, "aug": 1})
        pick = tied.sort_values("order").iloc[0]
        choice.update(selected=pick["variant"], target=pick["target"], t=int(pick["t"]), gain=float(pick["gain"]),
                      ci=[float(pick["ci_low"]), float(pick["ci_high"])], passes_validation_stage=bool(pick["ci_low"] > 0),
                      next="confirmation on Drift-Dev in the heavy run" if pick["ci_low"] > 0 else "fails at the selection stage")
    else:
        choice.update(selected=None, next="no eligible routing variant beats A on Validation 7: LR fails")
    tab.round(4).to_csv(OUT / "lr_variants.csv", index=False)
    lr.round(5).to_csv(OUT / "lr_scenarios.csv", index=False)
    json.dump(choice, open(OUT / "lr_choice.json", "w"), indent=1)

    # ---- LA: A as partial drift correction --------------------------------------------------------------------------------
    la, attr = [], []

    def row_boot(yy, a, b):
        r = np.random.default_rng(0)
        d = [f1(yy[i], a[i]) - f1(yy[i], b[i]) for i in (r.integers(0, len(yy), len(yy)) for _ in range(B_BOOT))]
        return np.percentile(d, [2.5, 97.5])

    def attribution(name, kit_, det_, Xc, yc, svm_pred):
        R = det_.ratio(Xc)
        flags = R > 1
        for s in range(16):
            sets = [((s,) if flags[i, s] else ()) for i in range(len(Xc))]
            attr.append({"protocol": name, "sensor": f"S{s + 1:02d}", "flag_rate_clean": float(flags[:, s].mean()),
                         "gain_vs_svm": f1(yc, kit_.predict_A(Xc, sets, False)) - f1(yc, svm_pred)})

    lo, hi = row_boot(y, A_c, svm_c)
    la.append({"protocol": "original", "batch": 7, "svm": f1(y, svm_c), "A": f1(y, A_c), "gain": f1(y, A_c) - f1(y, svm_c), "ci_low": lo, "ci_high": hi})
    attribution("original b7", kit, d0, X, y, svm_c)
    fdev = arb.fitted("drift_dev", "M0")
    kdev = arb.make_kit(fdev, arb.OUT / "drift_dev" / "reduced")
    for b, (Xb, yb) in load(PROTOCOLS["drift_dev"])[3].items():
        Zb = fill_nan_zero(fdev["pre"].transform(Xb))
        s_pred = fast_svm_predict(fdev["svm"], Zb)
        Rb = fdev["det"].ratio(Xb)
        a_pred = kdev.predict_A(Xb, acted_sets(Rb, Rb > 1), False)
        lo, hi = row_boot(yb, a_pred, s_pred)
        la.append({"protocol": "drift_dev", "batch": b, "svm": f1(yb, s_pred), "A": f1(yb, a_pred), "gain": f1(yb, a_pred) - f1(yb, s_pred),
                   "ci_low": lo, "ci_high": hi})
        attribution(f"drift_dev b{b}", kdev, fdev["det"], Xb, yb, s_pred)
    la, attr = pd.DataFrame(la), pd.DataFrame(attr)
    la.round(4).to_csv(OUT / "la_clean.csv", index=False)
    attr.round(4).to_csv(OUT / "la_attribution.csv", index=False)
    attr_w = attr.pivot(index="sensor", columns="protocol", values="gain_vs_svm")
    flag_w = attr.pivot(index="sensor", columns="protocol", values="flag_rate_clean")

    md = ["# Night study, light part (POST-HOC, decisions_log L7). Test not read.", "",
          "## LR: routing A -> T when n_flag >= t (selection on Validation 7, v1 saved outputs; medium severity, k1/k2/k4 equally weighted)", "",
          tab.round(4).to_markdown(index=False), "", "```", json.dumps(choice, indent=1), "```", "",
          "## LD: detector variants on Validation 7 (descriptive)", "", pd.DataFrame(clean).round(4).to_markdown(index=False), "",
          ld_tab.round(4).to_markdown(index=False), "", "Masking at k=2 (replicate-pair faults):", "", mask_tab.round(4).to_markdown(index=False), "",
          "## LA: A on clean rows (partial drift correction)", "", la.round(4).to_markdown(index=False), "",
          "Gain of A restricted to one sensor's flags (clean rows):", "", attr_w.round(4).to_markdown(), "", "Clean flag rate per sensor:", "",
          flag_w.round(3).to_markdown()]
    (OUT / "LIGHT.md").write_text(chr(10).join(md), encoding="utf-8")
    print(chr(10).join(md))


if __name__ == "__main__":
    main()
