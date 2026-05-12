"""Tests for life-cycle alignment module."""

from __future__ import annotations

import numpy as np
import polars as pl

from mobilitetsmodellen.alignment.life_cycle import DEFAULT_AGES, align


def _panel(n: int = 50, seed: int = 1) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    n_ages = 21
    pids = np.repeat(np.arange(1, n + 1), n_ages)
    ages = np.tile(np.arange(30, 51), n)
    income = np.maximum(rng.normal(300_000, 100_000, n * n_ages), 0.0)
    return pl.DataFrame(
        {"pid": pids.astype(np.int64), "age": ages.astype(np.int32), "income": income}
    )


def test_align_returns_one_row_per_person() -> None:
    panel = _panel(n=30)
    result = align(panel)
    assert len(result) == 30
    assert "pid" in result.columns
    assert "income" in result.columns


def test_align_income_non_negative() -> None:
    panel = _panel(n=20)
    result = align(panel)
    assert (result["income"] >= 0).all()


def test_align_single_window() -> None:
    panel = _panel(n=10)
    r1 = align(panel, window="single")
    r3 = align(panel, window="three")
    assert len(r1) == len(r3)


def test_align_five_window() -> None:
    panel = _panel(n=10)
    result = align(panel, window="five")
    assert len(result) == 10


def test_align_default_ages_range() -> None:
    assert min(DEFAULT_AGES) == 35
    assert max(DEFAULT_AGES) == 45


def test_align_missing_ages_returns_subset(tmp_path: pathlib.Path) -> None:
    import polars as pl

    panel = pl.DataFrame(
        {
            "pid": [1, 1, 2, 2],
            "age": [40, 41, 40, 41],
            "income": [300_000.0, 310_000.0, 200_000.0, 210_000.0],
        }
    )
    result = align(panel, ages=[40, 41], window="single")
    assert len(result) >= 1


import pathlib  # noqa: E402
