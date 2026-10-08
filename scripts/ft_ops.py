"""Operational helpers for the final-test run (no computation of results).

Usage: python scripts/ft_ops.py verify-chunks   [--name test]   # move unreadable (truncated) chunk files aside
       python scripts/ft_ops.py determinism     [--name test] [--chunk 5] [--jobs 3]
`determinism` recomputes ONE finished Part-2 chunk with the real worker code (scripts/ov2_faults_g1.py run_chunk) in a worker pool of
`--jobs` and compares it with the original: row values within 1e-9 and identical predictions. It prints only the verdict,
never the scores. The original chunk is always kept; the recomputed one is saved next to it as chunk_XXX.recomputed.pkl.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import pickle  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402

sys.path.insert(0, "scripts")
CONFIG = "configs/final_test.yaml"
ROOT = Path("results/final_test")


def verify_chunks(name):
    bad = 0
    for path in sorted((ROOT / name).glob("*_chunks/chunk_*.pkl")):
        try:
            with open(path, "rb") as f:
                pickle.load(f)
        except Exception as e:                                         # truncated by a kill in the middle of a write
            path.rename(path.with_suffix(".corrupt"))
            print(f"unreadable, moved aside: {path} ({type(e).__name__})")
            bad += 1
    n = len(list((ROOT / name).glob("*_chunks/chunk_*.pkl")))
    print(f"{n} readable chunk files, {bad} moved aside")


def determinism(name, index, jobs):
    from ov2_faults_g1 import CHUNK, run_chunk
    from src.scenarios import build_scenarios
    from src.study import AUG_SEEDS
    chunk_dir = ROOT / name / "g1_chunks"
    orig = chunk_dir / f"chunk_{index:03d}.pkl"
    assert orig.exists(), "chunk to compare does not exist"
    kept = chunk_dir / f"chunk_{index:03d}.original"
    orig.rename(kept)
    try:
        sids = list(range(index * CHUNK, min((index + 1) * CHUNK, len(build_scenarios(AUG_SEEDS)))))
        Parallel(n_jobs=jobs)(delayed(run_chunk)(CONFIG, name, False, index, sids) for _ in range(1))
        new = chunk_dir / f"chunk_{index:03d}.pkl"
        a, b = pickle.load(open(kept, "rb")), pickle.load(open(new, "rb"))
        same_preds = all(np.array_equal(a["preds"][m], b["preds"][m]) for m in a["preds"]) and set(a["preds"]) == set(b["preds"])
        diffs = [abs(ra[k] - rb[k]) for ra, rb in zip(a["rows"], b["rows"]) for k in ra if k != "sid"]
        max_diff = max(diffs)
        ok = same_preds and len(a["rows"]) == len(b["rows"]) and max_diff < 1e-9 and all(ra["sid"] == rb["sid"] for ra, rb in zip(a["rows"], b["rows"]))
        new.rename(chunk_dir / f"chunk_{index:03d}.recomputed.pkl")
        print(f"determinism chunk {index}, {jobs} workers: {'IDENTICAL' if ok else 'MISMATCH'} "
              f"(predictions equal: {same_preds}, max row difference {max_diff:.1e})")
        return ok
    finally:
        kept.rename(orig)                                               # the original always stays in place


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["verify-chunks", "determinism"])
    ap.add_argument("--name", default="test")
    ap.add_argument("--chunk", type=int, default=5)
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    if a.cmd == "verify-chunks":
        verify_chunks(a.name)
    else:
        sys.exit(0 if determinism(a.name, a.chunk, a.jobs) else 1)
