"""Download UCI #224 (Gas Sensor Array Drift) into data/raw/ and check every file against data/raw/SHA256SUMS.txt.

Usage: python scripts/download_data.py [--dest data/raw] [--verify-only]
The batch files are also committed in data/raw/, so this is only needed for a fresh, independent copy.
Exit code 1 if any file is missing or its SHA-256 does not match.
"""
import argparse
import hashlib
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/224/gas+sensor+array+drift+dataset.zip"
SUMS = Path(__file__).resolve().parent.parent / "data" / "raw" / "SHA256SUMS.txt"


def expected():
    """{file name: sha256} from SHA256SUMS.txt (lines: name, size, sha256)."""
    lines = SUMS.read_text(encoding="utf-8-sig").splitlines()
    return {p[0]: p[-1] for p in (line.split() for line in lines) if p}


def download(dest):
    data = urllib.request.urlopen(URL, timeout=120).read()
    archive = zipfile.ZipFile(io.BytesIO(data))
    inner = [n for n in archive.namelist() if n.endswith(".zip")]       # the UCI archive may wrap a second zip
    if inner:
        archive = zipfile.ZipFile(io.BytesIO(archive.read(inner[0])))
    wanted = set(expected())
    for name in archive.namelist():
        if Path(name).name in wanted:
            (dest / Path(name).name).write_bytes(archive.read(name))


def verify(dest):
    ok = True
    for name, sha in expected().items():
        path = dest / name
        got = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"
        print(f"{'OK ' if got == sha else 'BAD'} {name} {got}")
        ok &= got == sha
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=str(SUMS.parent))
    ap.add_argument("--verify-only", action="store_true")
    a = ap.parse_args()
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    if not a.verify_only:
        download(dest)
    sys.exit(0 if verify(dest) else 1)
