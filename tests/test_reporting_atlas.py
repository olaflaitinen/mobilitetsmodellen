"""Tests for the interactive mobility atlas."""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd
import pytest

from mobilitetsmodellen.reporting.atlas import build_atlas, export_atlas_html


def _region_df(n: int = 20, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "region": [f"K{i:04d}" for i in range(1, n + 1)],
            "estimate": rng.uniform(0.1, 0.5, n),
            "se": rng.uniform(0.02, 0.1, n),
        }
    )


def test_build_atlas_returns_figure() -> None:
    pytest.importorskip("plotly")
    fig = build_atlas(_region_df())
    assert fig is not None


def test_export_atlas_html_creates_file(tmp_path: pathlib.Path) -> None:
    pytest.importorskip("plotly")
    fig = build_atlas(_region_df())
    out = export_atlas_html(fig, tmp_path / "atlas.html")
    assert out.exists()


def test_export_atlas_html_contains_aria(tmp_path: pathlib.Path) -> None:
    pytest.importorskip("plotly")
    fig = build_atlas(_region_df())
    out = export_atlas_html(fig, tmp_path / "atlas.html")
    content = out.read_text(encoding="utf-8")
    assert "aria-label" in content


def test_export_atlas_html_valid_html(tmp_path: pathlib.Path) -> None:
    pytest.importorskip("plotly")
    fig = build_atlas(_region_df())
    out = export_atlas_html(fig, tmp_path / "atlas.html")
    content = out.read_text(encoding="utf-8")
    assert "<html" in content.lower()
    assert "</html>" in content.lower()


def test_build_atlas_deterministic() -> None:
    pytest.importorskip("plotly")
    df = _region_df()
    f1 = build_atlas(df, seed=31)
    f2 = build_atlas(df, seed=31)
    import json

    j1 = json.loads(f1.to_json())
    j2 = json.loads(f2.to_json())
    assert j1["data"][0]["y"] == j2["data"][0]["y"]
