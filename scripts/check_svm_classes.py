"""Inventory of the number of classes of every saved SVC (decisions_log H1): fast_svm_predict was wrong for two-class models.

Usage: python scripts/check_svm_classes.py [root ...]   (default: results)
Opens every *.joblib under the roots (a model, a list of (cols, model) experts, or a pipeline) and prints per folder the
number of SVC models and the smallest class count; lists every SVC with fewer than 3 classes. Reads models only, no data.
"""
import sys
from collections import defaultdict
from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def svcs(obj):
    if isinstance(obj, SVC):
        yield obj
    elif isinstance(obj, Pipeline):
        yield from (s for _, s in obj.steps if isinstance(s, SVC))
    elif isinstance(obj, (list, tuple)):
        for o in obj:
            yield from svcs(o)
    elif isinstance(obj, dict):
        for o in obj.values():
            yield from svcs(o)


def main(roots):
    per_dir, bad, unreadable = defaultdict(lambda: [0, 99]), [], []
    for root in roots:
        for path in sorted(Path(root).rglob("*.joblib")):
            try:
                obj = joblib.load(path)
            except Exception as e:
                unreadable.append(f"{path} ({type(e).__name__})")
                continue
            for m in svcs(obj):
                n = len(m.classes_)
                d = per_dir[str(path.parent)]
                d[0] += 1
                d[1] = min(d[1], n)
                if n < 3:
                    bad.append(f"{path}: {n} classes")
    for d, (count, low) in sorted(per_dir.items()):
        print(f"{d}: {count} SVC, min classes {low}")
    print(f"TOTAL: {sum(c for c, _ in per_dir.values())} SVC models; with < 3 classes: {len(bad)}; unreadable files: {len(unreadable)}")
    for line in bad + unreadable:
        print("  ", line)
    return not bad


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:] or ["results"]) else 1)
