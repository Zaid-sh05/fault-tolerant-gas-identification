"""v2 fault-layer check and hybrid arbiter H1-H3 on the winning base model (POST-HOC, decisions_log G7, G8, I1-I5). Batches 1-7 only.

Usage: python scripts/v2_arbiter.py [--jobs 3]
Reads results/v2/choice.json (winner of the candidate table). Outputs in results/v2/arbiter/: scenarios.csv (one row per protocol x batch x
scenario, Macro-F1 of every method and the branch shares), settings.csv, worst_case.csv, choice.json, ARBITER.md.
Fitted objects are cached in results/v2/arbiter/<protocol>/; scenario chunks are checkpointed (safe to resume).
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
from lightgbm import LGBMClassifier  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

sys.path.insert(0, "scripts")
from v2_dev import PROTOCOLS, load, make_transform  # noqa: E402
from src.detector import ReliabilityDetector  # noqa: E402
from src.evaluate import fill_nan_zero  # noqa: E402
from src.fastsvm import fast_svm_predict  # noqa: E402
from src.faults import augment_with_faults  # noqa: E402
from src.models import scores  # noqa: E402
from src.preprocessing import fit_preprocessor  # noqa: E402
from src.scenarios import FaultStats, apply_scenario, build_scenarios  # noqa: E402
from src.strategies import StrategyKit, acted_sets, group_by_set  # noqa: E402
from src.study import AUG_SEEDS, OVERNIGHT  # noqa: E402

OUT = Path("results/v2/arbiter")
CHUNK = 40
H3_WEIGHTS = {0: (0.8, 0.0, 0.2), 1: (0.2, 0.6, 0.2), 2: (0.1, 0.5, 0.4), 3: (0.0, 0.4, 0.6)}     # (SVM, A, Aug), G8
SINGLE = ["svm", "A", "B", "svm_aug", "lgbm_aug"]
ARBITERS = ["H1", "H2", "H3"]
MARGIN = 0.01


def scenario_list():
    return [None] + build_scenarios(AUG_SEEDS, ("k1", "k2"), reduced=True)          # None = clean


def atomic(path, write):
    """Write through a temporary file and rename, so a kill in the middle never leaves a truncated file to be reused."""
    tmp = Path(f"{path}.{os.getpid()}.tmp")
    write(tmp)
    os.replace(tmp, path)


def fitted(proto, winner):
    """Fit (once, cached) everything on the transformed Train rows of the protocol."""
    assert "M3" not in winner.split("+"), "a batch-ensemble base (M3) needs its own A/B/augmentation (G7); not implemented"
    d = OUT / proto
    path = d / "fitted.joblib"
    if path.exists():
        return joblib.load(path)
    d.mkdir(parents=True, exist_ok=True)
    fin = json.load(open(OVERNIGHT / "final_pipeline.json"))
    Xtr, ytr, btr, _ = load(PROTOCOLS[proto])
    T = make_transform(winner.split("+")).fit(Xtr, btr)
    Xt = T.train_transform(Xtr, btr)
    pre = fit_preprocessor(fin["spec"], Xt, ytr, btr, fill_nan=False)
    params = {**fin["svm_params"], "probability": True}

    def svm_on(X, y):
        return SVC(kernel="rbf", random_state=0, **params).fit(fill_nan_zero(pre.transform(X)), y)

    sigma_t = FaultStats.fit(Xt).sigma                                         # augmentation in the transformed space (G7)
    aug = [augment_with_faults(Xt, ytr, sigma_t, np.random.default_rng(s), 1) for s in AUG_SEEDS]
    svms = Parallel(n_jobs=3)(delayed(svm_on)(X, y) for X, y in [(Xt, ytr)] + aug)
    lgbm = [LGBMClassifier(random_state=0, deterministic=True, n_jobs=3, verbose=-1, **fin["lgbm_params"]).fit(pre.transform(X), y)
            for X, y in aug]
    for m in lgbm:
        m.set_params(n_jobs=1)
    obj = {"T": T, "Xt": Xt, "ytr": ytr, "pre": pre, "svm": svms[0], "svm_aug": svms[1:], "lgbm_aug": lgbm, "params": params,
           "det": ReliabilityDetector(normalization="median").fit(Xt, btr), "raw_stats": FaultStats.fit(Xtr)}
    atomic(path, lambda p: joblib.dump(obj, p))
    return obj


def combine(classes, P):
    return classes[np.argmax(P, axis=1)]


def run_chunk(proto, winner, batch, index, sids):
    path = OUT / proto / f"b{batch}_chunks" / f"chunk_{index:03d}.pkl"
    if path.exists():
        return str(path)
    f = fitted(proto, winner)
    X, y = load(PROTOCOLS[proto])[3][batch]
    kit = StrategyKit(f["pre"], f["svm"], f["Xt"], f["ytr"], f["det"], f["params"], str(OUT / proto / "reduced"))
    pre, svm, classes = f["pre"], f["svm"], f["svm"].classes_
    Z = lambda A: fill_nan_zero(pre.transform(A))                                  # noqa: E731
    scen = scenario_list()
    rows = []
    for sid in sids:
        sc = scen[sid]
        Xf, truth = (X, np.zeros((len(X), 16), bool)) if sc is None else apply_scenario(X, sc, f["raw_stats"])
        Xb = f["T"].transform(Xf)                                                 # statistics of this (faulted) batch, no labels
        R = f["det"].ratio(Xb)
        flags = R > 1.0
        n_flag = flags.sum(1)
        sets, orc = acted_sets(R, flags), acted_sets(truth.astype(float), truth)
        Xr = kit.reconstruct(Xb, group_by_set(sets), False)
        Zb, Zr = Z(Xb), Z(Xr)
        P = {"svm": svm.predict_proba(Zb), "A": svm.predict_proba(Zr),
             "aug": np.mean([m.predict_proba(Zb) for m in f["svm_aug"]], axis=0), "B": np.zeros((len(X), len(classes)))}
        lab = {"svm": fast_svm_predict(svm, Zb), "A": fast_svm_predict(svm, Zr), "B": np.empty(len(X), int)}
        for pattern, r in group_by_set(sets).items():
            m, keep = kit.reduced_model(pattern), kit.keep_columns(pattern)
            lab["B"][r] = fast_svm_predict(m, Zb[r][:, keep])
            P["B"][r] = m.predict_proba(Zb[r][:, keep])
        lab["A_oracle"] = fast_svm_predict(svm, Z(kit.reconstruct(Xb, group_by_set(orc), False)))
        lab["B_oracle"] = kit.predict_B(Xb, orc)
        h1 = np.where(n_flag[:, None] == 0, P["svm"], np.where(n_flag[:, None] <= 2, P["A"], (P["B"] + P["aug"]) / 2))
        h2 = np.where(n_flag[:, None] == 0, P["svm"], np.where(n_flag[:, None] == 1, P["A"], (P["A"] + P["B"] + P["aug"]) / 3))
        w = np.array([H3_WEIGHTS[min(n, 3)] for n in n_flag])
        h3 = w[:, :1] * P["svm"] + w[:, 1:2] * P["A"] + w[:, 2:] * P["aug"]
        lab.update(H1=combine(classes, h1), H2=combine(classes, h2), H3=combine(classes, h3))
        row = {"protocol": proto, "batch": batch, "sid": sid, "setting": "clean" if sc is None else sc.kset,
               "fault": "none" if sc is None else sc.fault, "sensors": "" if sc is None else "-".join(str(s + 1) for s in sc.sensors),
               "seed": -1 if sc is None else sc.seed, "mean_n_flag": float(n_flag.mean())}
        row.update({f"share_nflag_{k}": float(np.mean(np.minimum(n_flag, 3) == k)) for k in range(4)})
        for m, p in lab.items():
            row[m] = scores(y, p)["macro_f1"]
        for kind in ("svm_aug", "lgbm_aug"):
            row[kind] = float(np.mean([scores(y, (fast_svm_predict(m, Zb) if kind == "svm_aug" else m.predict(pre.transform(Xb))))["macro_f1"]
                                       for m in f[kind]]))
        rows.append(row)
    path.parent.mkdir(exist_ok=True)
    atomic(path, lambda p: pickle.dump(rows, open(p, "wb")))
    return str(path)


def summarise(df):
    methods = SINGLE + ARBITERS + ["A_oracle", "B_oracle"]
    per_batch = df.groupby(["protocol", "batch", "setting"])[methods].mean().reset_index()
    settings = per_batch.groupby(["protocol", "setting"])[methods].mean().reset_index()       # Drift-Dev: mean of batches 6 and 7
    settings["best_aug"] = settings[["svm_aug", "lgbm_aug"]].max(axis=1)
    settings["best_single"] = settings[["svm", "A", "B", "best_aug"]].max(axis=1)
    overall = df.groupby(["protocol", "batch"])[methods].mean().groupby("protocol").mean()          # all 481 scenarios
    choice = {}
    for h in ARBITERS:
        gaps = (settings[h] - settings["best_single"]).tolist()
        choice[h] = {"mean_all_scenarios_avg_protocols": float(overall[h].mean()),
                     "setting_balanced_mean": float(settings[h].mean()),
                     "worst_gap_to_best_single": float(min(gaps)), "passes_condition": min(gaps) >= -MARGIN}
    ok = [h for h in ARBITERS if choice[h]["passes_condition"]]
    winner = max(ok, key=lambda h: choice[h]["mean_all_scenarios_avg_protocols"]) if ok else None
    worst = df.groupby(["protocol", "batch"])[methods].min().reset_index()
    fault_tab = (df.groupby(["protocol", "batch", "setting", "fault"])[methods].mean().reset_index()
                 .groupby(["protocol", "setting", "fault"])[methods].mean().reset_index())
    shares = (df.groupby(["protocol", "setting"])[[f"share_nflag_{k}" for k in range(4)] + ["mean_n_flag"]].mean().reset_index())
    return settings, overall, worst, fault_tab, shares, {"variants": choice, "winner": winner, "post_hoc": True,
                                                        "single_methods_overall": {m: float(overall[m].mean()) for m in SINGLE},
                                                        "rule": "decisions_log G8, I4"}


def main(jobs):
    winner = json.load(open("results/v2/choice.json"))["winner"]
    print("base model:", winner, flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    marker = OUT / "base_model.txt"                     # cached fits and chunks belong to this base model only
    if marker.exists():
        assert marker.read_text().strip() == winner, f"cache in {OUT} was computed for {marker.read_text().strip()}, not {winner}"
    marker.write_text(winner)
    n = len(scenario_list())
    for proto in PROTOCOLS:
        fitted(proto, winner)
        print(f"{proto}: fitted", flush=True)
    tasks = [(p, b, i, list(range(a, min(a + CHUNK, n)))) for p in PROTOCOLS for b in (load(PROTOCOLS[p])[3])
             for i, a in enumerate(range(0, n, CHUNK))]
    paths = Parallel(n_jobs=jobs, verbose=5)(delayed(run_chunk)(p, winner, b, i, s) for p, b, i, s in tasks)
    df = pd.DataFrame([r for p in paths for r in pickle.load(open(p, "rb"))])
    df.round(5).to_csv(OUT / "scenarios.csv", index=False)
    settings, overall, worst, fault_tab, shares, choice = summarise(df)
    choice["base_model"] = winner
    settings.round(4).to_csv(OUT / "settings.csv", index=False)
    worst.round(4).to_csv(OUT / "worst_case.csv", index=False)
    fault_tab.round(4).to_csv(OUT / "by_fault.csv", index=False)
    shares.round(4).to_csv(OUT / "branch_shares.csv", index=False)
    json.dump(choice, open(OUT / "choice.json", "w"), indent=1)
    cols = ["protocol", "setting", "svm", "A", "B", "svm_aug", "lgbm_aug", "H1", "H2", "H3", "A_oracle", "B_oracle"]
    md = [f"# Hybrid arbiter on {winner} (POST-HOC; decisions_log G7, G8, I1-I5)", "",
          "Mean Macro-F1 per setting (clean = no fault; k1/k2 = medium severity, 5 seeds; Drift-Dev = mean of batches 6 and 7).", "",
          settings[cols].round(3).to_markdown(index=False), "", "## Per fault type", "", fault_tab[cols[:1] + ["setting", "fault"] + cols[2:]]
          .round(3).to_markdown(index=False), "", "## Worst case (lowest per-scenario Macro-F1)", "",
          worst.round(3).to_markdown(index=False), "", "## Share of rows per n_flag (H1: 0 -> SVM, 1-2 -> A, >=3 -> B+Aug; "
          "H2: 0 -> SVM, 1 -> A, >=2 -> A+B+Aug; H3 weights by n_flag)", "", shares.round(3).to_markdown(index=False), "",
          "## Choice (G8)", "", "```", json.dumps(choice, indent=1), "```"]
    (OUT / "ARBITER.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    main(ap.parse_args().jobs)
