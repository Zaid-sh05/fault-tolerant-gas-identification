"""Audit point 9: 30 random rows of PAPER_NUMBERS.md (seed 2026) traced to their source file; prints listed value, source value, verdict.
Usage: python results/audit/trace_30.py -> results/audit/trace_30.md
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
import check_paper_numbers as c  # noqa: E402  (its locator parser; the comparison is printed for inspection)

rows = list(c.rows())
sample = random.Random(2026).sample(rows, 30)
L = ["# 30 random PAPER_NUMBERS rows traced to their source (seed 2026)", "", "| # | number | listed | from source | match |", "|---|---|---|---|---|"]
ok = 0
for i, (name, value, source) in enumerate(sample, 1):
    if "skill_table()" in source:
        exp = c.skill_value(name)
    else:
        path, *cl = c.split_clauses(source)
        path = path.replace("\\", "/")
        exp = c.from_json(path, cl) if path.endswith(".json") else c.from_csv(path, cl, name)
    m = c.same(exp, value)
    ok += m
    L.append(f"| {i} | {name} | {value} | {exp if isinstance(exp, str) else round(float(exp), 6)} | {'yes' if m else 'NO'} |")
L += ["", f"{ok} of 30 match."]
Path("results/audit/trace_30.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
