"""Tests for reporting (figures and tables)."""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd
import polars as pl

from mobilitetsmodellen.reporting.figures import FigureBuilder
from mobilitetsmodellen.reporting.tables import to_csv, to_latex_table, to_parquet


def test_figure_builder_rank_rank(tmp_path: pathlib.Path) -> None:
    fb = FigureBuilder(output_dir=tmp_path, formats=["png"])
    rng = np.random.default_rng(1)
    n = 50
    paths = fb.rank_rank_scatter(
        rng.uniform(0, 1, n),
        rng.uniform(0, 1, n),
        slope=0.3,
        intercept=0.35,
        filename="test_rr",
    )
    assert len(paths) == 1
    assert paths[0].exists()


def test_figure_builder_transition_heatmap(tmp_path: pathlib.Path) -> None:
    fb = FigureBuilder(output_dir=tmp_path, formats=["png"])
    matrix = np.full((5, 5), 0.2)
    paths = fb.transition_heatmap(matrix, filename="test_tm")
    assert paths[0].exists()


def test_to_csv_creates_file(tmp_path: pathlib.Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0]})
    p = to_csv(df, tmp_path / "out.csv")
    assert p.exists()
    content = p.read_text()
    assert "a" in content


def test_to_csv_with_bom(tmp_path: pathlib.Path) -> None:
    df = pd.DataFrame({"x": [1]})
    p = to_csv(df, tmp_path / "bom.csv", with_bom=True)
    raw = p.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf"


def test_to_parquet_pandas(tmp_path: pathlib.Path) -> None:
    df = pd.DataFrame({"a": [1, 2, 3]})
    p = to_parquet(df, tmp_path / "out.parquet")
    assert p.exists()


def test_to_parquet_polars(tmp_path: pathlib.Path) -> None:
    df = pl.DataFrame({"a": [1, 2, 3]})
    p = to_parquet(df, tmp_path / "out_pl.parquet")
    assert p.exists()


def test_to_latex_table(tmp_path: pathlib.Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [0.3, 0.4]})
    p = to_latex_table(df, tmp_path / "out.tex", caption="Test table", label="tab:test")
    assert p.exists()
    assert "tabular" in p.read_text()
