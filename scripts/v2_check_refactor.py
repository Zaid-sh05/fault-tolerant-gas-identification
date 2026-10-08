"""The refactored scenario code (predict_scenario + score_row) must reproduce a chunk written by the original arbiter code.

Usage: python scripts/v2_check_refactor.py   (recomputes drift_dev batch 6 chunk 0 in memory; exits 1 on any difference > 1e-12)
"""
import pickle
import sys

sys.path.insert(0, "scripts")
import v2_arbiter as arb  # noqa: E402
from v2_dev import PROTOCOLS, load  # noqa: E402


def main():
    saved = pickle.load(open(arb.OUT / "drift_dev" / "b6_chunks" / "chunk_000.pkl", "rb"))
    f = arb.fitted("drift_dev", "M0")
    X, y = load(PROTOCOLS["drift_dev"])[3][6]
    kit, scen = arb.make_kit(f, arb.OUT / "drift_dev" / "reduced"), arb.scenario_list()
    worst = 0.0
    for old in saved:
        lab, n_flag = arb.predict_scenario(f, kit, X, scen[old["sid"]])
        new = arb.score_row(lab, n_flag, y)
        for k, v in new.items():
            worst = max(worst, abs(v - old[k]))
    ok = worst <= 1e-12
    print(f"refactor check on {len(saved)} scenarios: {'IDENTICAL' if ok else 'MISMATCH'} (max difference {worst:.1e})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
