"""The table check of scripts/check_paper_numbers.py must compare every table cell with ITS OWN number, not with any number of the file."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, "scripts")
import check_paper_numbers as c  # noqa: E402

PN_TEXT = """# numbers

| number | value | source |
|---|---|---|
| alpha | 0.8590 | x |
| beta | 0.5354 | x |
"""

TEX = """\\begin{{tabular}}{{lcc}}
\\toprule
Model & Val & Test \\\\
\\midrule
SVM & {a} & {b} \\\\
\\bottomrule
\\end{{tabular}}
"""


def make(tmp_path, monkeypatch, a, b, cells=True):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "results/paper/latex").mkdir(parents=True)
    (tmp_path / "results/paper/PAPER_NUMBERS.md").write_text(PN_TEXT, encoding="utf-8")
    (tmp_path / "results/paper/latex/t.tex").write_text(TEX.format(a=a, b=b), encoding="utf-8")
    if cells:
        sidecar = {"cells": [{"row": 0, "col": 1, "names": ["alpha"]}, {"row": 0, "col": 2, "names": ["beta"]}]}
        (tmp_path / "results/paper/latex/t.cells.json").write_text(json.dumps(sidecar), encoding="utf-8")
    monkeypatch.setattr(c, "PN", Path("results/paper/PAPER_NUMBERS.md"))


def test_correct_table_passes(tmp_path, monkeypatch):
    make(tmp_path, monkeypatch, "0.859", "0.535")
    n, bad = c.check_tables()
    assert n == 2 and bad == []


def test_swapped_cells_are_caught_although_each_value_exists_in_the_file(tmp_path, monkeypatch):
    make(tmp_path, monkeypatch, "0.535", "0.859")            # both numbers exist in PAPER_NUMBERS, but in the wrong cells
    _, bad = c.check_tables()
    assert len(bad) == 2


def test_a_wrong_cell_is_caught(tmp_path, monkeypatch):
    make(tmp_path, monkeypatch, "0.858", "0.535")
    _, bad = c.check_tables()
    assert len(bad) == 1 and "0.858" in bad[0]


def test_a_numeric_cell_without_provenance_is_an_error(tmp_path, monkeypatch):
    make(tmp_path, monkeypatch, "0.859", "0.535", cells=False)
    _, bad = c.check_tables()
    assert bad, "a table without its cell map must not pass"


@pytest.mark.parametrize("text", ["0.8590", "+0.859"])
def test_printed_precision_and_sign_are_respected(tmp_path, monkeypatch, text):
    make(tmp_path, monkeypatch, text, "0.535")
    _, bad = c.check_tables()
    assert bad == []
