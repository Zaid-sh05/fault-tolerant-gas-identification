"""Impact estimate of the v2 interval issue (audit only; reads results/final_test_v2/test/scores.csv, faults_ci.csv, clean_ci.csv).

Usage: python results/audit/ci_impact.py -> results/audit/ci_impact.md
Reported intervals average INDEPENDENT bootstrap replicates of the 5 calibration seeds (ft_v2_recal.py:229-238, ft_v2_tables.py:16-24).
Shown next to them:
  clean  : 95% t-interval over the 5 per-seed (b)-(a) differences (calibration-draw variance only; row-sampling variance needs the Test
           labels, which are not read again)
  faults : scenario bootstrap with ONE resample index per replicate shared by all seeds (k-stratified, 1000, seed 0)
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t

D = Path("results/final_test_v2/test")
df = pd.read_csv(D / "scores.csv")
L = ["# Impact of the v2 interval issue (audit estimate)", "", "## Clean (b)-(a)", "",
     "| subset | method | diff | reported CI | t-interval over 5 seeds | seed range |", "|---|---|---|---|---|---|"]
cci = pd.read_csv(D / "clean_ci.csv").set_index(["subset", "method"])
c = df[df.setting == "clean"].pivot_table(index=["subset", "cal_seed", "method"], columns="model", values="f1").reset_index()
c["d"] = c.b - c.a
for (sub, m), g in c.groupby(["subset", "method"]):
    d = g["d"].to_numpy()
    h = t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d))
    r = cci.loc[(sub, m)]
    L.append(f"| {sub} | {m} | {d.mean():.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] | [{d.mean() - h:.4f}, {d.mean() + h:.4f}] | {d.min():.4f} .. {d.max():.4f} |")

L += ["", "## Under faults", "", "| subset | comparison | diff | reported CI | shared-index CI |", "|---|---|---|---|---|"]
fci = pd.read_csv(D / "faults_ci.csv")
f = df[df.setting != "clean"]
for _, r in fci.iterrows():
    if r.comparison.startswith("(b)-(a)"):
        m = r.comparison.split()[1]
        x, y = ("b", m), ("a", m)
    else:
        mod = r.comparison[-2]
        x, y = (mod, "A"), (mod, "svm")
    s = f[f.subset == r.subset]
    seeds = sorted(s.cal_seed.unique())
    get = lambda mod, meth, sd: s[(s.model == mod) & (s.method == meth) & (s.cal_seed == sd)].sort_values("sid")  # noqa: E731
    D_ = np.stack([get(*x, sd)["f1"].to_numpy() - get(*y, sd)["f1"].to_numpy() for sd in seeds])
    k = get(*x, seeds[0])["setting"].to_numpy()
    groups = [np.flatnonzero(k == g) for g in ("k1", "k2")]
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(1000):
        idx = [rng.choice(g, len(g)) for g in groups]
        bs.append(np.mean([np.mean([D_[j][i].mean() for i in idx]) for j in range(len(seeds))]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    L.append(f"| {r.subset} | {r.comparison} | {r['diff']:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] | [{lo:.4f}, {hi:.4f}] |")
Path("results/audit/ci_impact.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
