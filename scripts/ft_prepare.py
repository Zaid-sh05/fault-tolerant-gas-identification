"""Final test, step 0: copy the frozen artefacts (models, detectors, reduced SVMs; all fitted on Train) into the run folder.

Usage: python scripts/ft_prepare.py --config configs/final_test.yaml --name test
Every source file is checked against results/FREEZE_HASHES.json (written by ft_freeze.py before the tag) and every copy is
checked again, so the run provably uses the frozen objects. Nothing is trained here. Sensor sets that Validation never
produced are trained on demand from the same Train rows with the frozen parameters (src/strategies.py).
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from src.splits import load_config

SRC = Path("results/overnight/temporal")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(cfg_path, name):
    dest = Path(load_config(cfg_path)["output_root"]) / name
    frozen = json.load(open("results/FREEZE_HASHES.json"))["artifacts"]
    for rel, digest in frozen.items():
        assert sha(SRC / rel) == digest, f"frozen artefact changed: {rel}"
        target = dest / rel
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SRC / rel, target)
        assert sha(target) == digest, f"copy differs from the frozen artefact: {rel}"
    shutil.copy2(SRC / "g2_verdict.json", dest / "frozen_g2_verdict.json")
    print(f"{len(frozen)} frozen artefacts verified and copied to {dest}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/final_test.yaml")
    ap.add_argument("--name", default="test")
    a = ap.parse_args()
    main(a.config, a.name)
