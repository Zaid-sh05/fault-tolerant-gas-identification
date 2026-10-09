"""Consistency check of results/paper/PAPER_NUMBERS.md (reads result files only).

Usage: python scripts/check_paper_numbers.py        (exit code 1 if anything does not match)
1. Every row "| number | value | source |": the value is recomputed from the source named next to it, and must match it at the
   precision it is written with (half a unit of the last printed digit).
   Source forms: `<csv>, key=value, ..., [rows|methods] [list], column C [(mean...)]`; `<json>, key.path` (or `a / b` -> "x of y");
   the reconstruction-skill rows are recomputed with scripts/ft_paper.py skill_table() from the phase-1 files they name.
2. Every number in the body of the LaTeX tables (results/paper/latex/*.tex) must equal a PAPER_NUMBERS value at the printed precision.
   (The figures of scripts/v2_paper.py take their values from PAPER_NUMBERS by name, so they are covered by construction.)
Prints every mismatch and a summary.
"""
import ast
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, "scripts")
PN = Path("results/paper/PAPER_NUMBERS.md")
ALIAS = {"rank": "rank_from_least_reliable"}


def rows():
    for line in PN.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith(("| number", "| quantity")):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 3:
                yield parts[0], parts[1], " | ".join(parts[2:])


def tol(text):
    m = re.search(r"\.(\d+)", text)
    return 0.5 * 10 ** -(len(m.group(1)) if m else 0) + 1e-9


def same(expected, text):
    if text in ("True", "False"):
        return str(bool(expected)) == text
    if " of " in text:
        return str(expected) == text
    return abs(float(expected) - float(text)) <= tol(text)


def split_clauses(rest):
    """Clauses separated by ', ' but not inside [...] or (...)."""
    out, depth, cur = [], 0, ""
    for i, ch in enumerate(rest):
        depth += ch in "[(" and 1 or 0
        depth -= ch in "])" and 1 or 0
        if ch == "," and depth == 0 and rest[i + 1:i + 2] == " ":
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    merged = []
    for c in [c for c in out + [cur.strip()] if c]:                 # "comparison=A-SVM under faults, model (a)": a value with ", "
        if merged and "=" not in c and not c.startswith(("column ", "rows [", "methods [")) and "=" in merged[-1]:
            merged[-1] += ", " + c
        else:
            merged.append(c)
    return merged


NOTES = []


def from_csv(path, clauses, name=""):
    df = pd.read_csv(path)
    if df.columns[0].startswith("Unnamed"):
        df = df.rename(columns={df.columns[0]: "_index"})
    col, mean = None, False
    for c in clauses:
        if c.startswith("column "):
            col = c.split()[1]
            mean = "(mean" in c
        elif c.startswith(("rows [", "methods [")):
            names = ast.literal_eval(c[c.index("["):])
            key = "_index" if c.startswith("rows") else "method"
            df = df[df[key].isin(names)]
        elif "=" in c:
            k, v = c.split("=", 1)
            k = ALIAS.get(k.strip(), k.strip())
            s = df[k]
            try:
                df = df[pd.to_numeric(s) == float(v)] if s.dtype != object else df[s.astype(str) == v]
            except ValueError:
                df = df[s.astype(str) == v]
    assert col is not None, "no column"
    vals = df[col]
    sub = name.rsplit(", ", 1)[-1]
    if len(vals) > 1 and not mean and "subset" in df.columns and sub in set(df["subset"]):    # v1 locator without its subset
        vals = df[df["subset"] == sub][col]
        NOTES.append(f"NOTE      {name}: the locator has no subset filter; the subset '{sub}' was taken from the name")
    if len(vals) != 1 and not mean:
        raise ValueError(f"{len(vals)} rows match")
    return vals.mean() if mean else vals.iloc[0]


def from_json(path, clauses):
    d = json.load(open(path))
    keys = [k for c in clauses for k in c.split(".")]
    if len(clauses) >= 2 and " / " in clauses[-1]:
        sub = d
        for k in clauses[:-1]:
            sub = sub[k]
        a, b = [x.strip() for x in clauses[-1].split("/")]
        return f"{sub[a]} of {sub[b]}"
    for k in keys:
        d = d[k]
    return d


def skill_value(name):
    from ft_paper import skill_table
    w = skill_table()
    m = re.search(r"(ridge|knn)/(raw|slog), twin (missing|available)", name)
    r = w[(w.method == m.group(1)) & (w.space == m.group(2)) & (w.exclude_twin == (m.group(3) == "missing"))].iloc[0]
    if name.startswith("Reconstruction skill"):
        return r[f"skill_median_{'reference' if 'reference protocol' in name else 'temporal'}"]
    if name.startswith("Median R2"):
        return r[f"r2_median_{'reference' if name.endswith('reference') else 'temporal'}"]
    return r["drift_cost_r2"] if name.startswith("Drift cost in R2") else r["drift_cost_skill"]


def check_rows():
    bad, n = [], 0
    for name, value, source in rows():
        n += 1
        try:
            if "skill_table()" in source:
                exp = skill_value(name)
            else:
                path, *clauses = split_clauses(source)
                path = path.replace("\\", "/")
                exp = from_json(path, clauses) if path.endswith(".json") else from_csv(path, clauses, name)
            if not same(exp, value):
                bad.append(f"MISMATCH  {name}: listed {value}, source gives {exp}  [{source}]")
        except Exception as e:                                                       # an unreadable locator is a failure too
            bad.append(f"UNCHECKED {name}: {type(e).__name__}: {e}  [{source}]")
    return n, bad


def check_tables():
    values = []
    for _, v, _ in rows():
        try:
            values.append(float(v))
        except ValueError:
            pass
    bad, n = [], 0
    for tex in sorted(Path("results/paper/latex").glob("*.tex")):
        body = tex.read_text(encoding="utf-8").split("\\midrule")[1].split("\\bottomrule")[0]
        cells = [c for line in body.split("\\\\") for c in line.split("&")[1:]]          # the first cell of a row is its text label
        for cell in re.findall(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?![\w.])", " ".join(cells)):
            n += 1
            x = float(cell)
            if not any(abs(v - x) <= tol(cell) for v in values):
                bad.append(f"TABLE     {tex.name}: {cell} is not a PAPER_NUMBERS value")
    return n, bad


def main():
    n1, b1 = check_rows()
    n2, b2 = check_tables()
    for line in NOTES + b1 + b2:
        print(line)
    print(f"PAPER_NUMBERS rows checked: {n1}, problems: {len(b1)}; LaTeX table numbers checked: {n2}, problems: {len(b2)}")
    return not (b1 or b2)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
