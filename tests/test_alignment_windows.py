"""Tests for income averaging window module."""

from __future__ import annotations

import numpy as np
import polars as pl

from mobilitetsmodellen.alignment.windows import apply_window


def _panel(n: int = 20, seed: int = 1) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    n_ages = 11
    pids = np.repeat(np.arange(1, n + 1), n_ages)
    ages = np.tile(np.arange(35, 46), n)
    income = rng.uniform(100_000, 500_000, n * n_ages)
    return pl.DataFrame(
        {"pid": pids.astype(np.int64), "age": ages.astype(np.int32), "income": income}
    )


def test_apply_window_single_one_row_per_pid() -> None:
    panel = _panel(n=15)
    result = apply_window(panel, window="single", center_age=40)
    assert len(result) == 15


def test_apply_window_three_one_row_per_pid() -> None:
    panel = _panel(n=15)
    result = apply_window(panel, window="three", center_age=40)
    assert len(result) == 15


def test_apply_window_five_one_row_per_pid() -> None:
    panel = _panel(n=15)
    result = apply_window(panel, window="five", center_age=40)
    assert len(result) == 15


def test_apply_window_income_is_average() -> None:
    panel = pl.DataFrame(
        {
            "pid": [1, 1, 1],
            "age": [39, 40, 41],
            "income": [100_000.0, 200_000.0, 300_000.0],
        }
    )
    result = apply_window(panel, window="three", center_age=40)
    assert abs(result["income"][0] - 200_000.0) < 1.0


def test_apply_window_sorted_output() -> None:
    panel = _panel(n=10)
    result = apply_window(panel, window="three", center_age=40)
    pids = result["pid"].to_list()
    assert pids == sorted(pids)
