"""Income averaging window application for life-cycle bias reduction."""

from __future__ import annotations

from typing import Literal

import polars as pl

WindowType = Literal["single", "three", "five"]

_WINDOW_WIDTHS: dict[WindowType, int] = {
    "single": 1,
    "three": 3,
    "five": 5,
}


def apply_window(
    panel: pl.DataFrame,
    window: WindowType = "three",
    income_col: str = "income",
    age_col: str = "age",
    pid_col: str = "pid",
    center_age: int = 40,
) -> pl.DataFrame:
    """Average income over a symmetric window around a center age.

    Args:
        panel: Panel DataFrame with one row per person per age.
        window: Width of the averaging window (``"single"``, ``"three"``, ``"five"``).
        income_col: Name of the income column.
        age_col: Name of the age column.
        pid_col: Name of the person identifier column.
        center_age: Age around which to centre the window.

    Returns:
        A DataFrame with one row per person, columns ``pid_col`` and
        ``income_col`` (averaged over the window).
    """
    width = _WINDOW_WIDTHS[window]
    half = width // 2
    low = center_age - half
    high = center_age + half
    filtered = panel.filter((pl.col(age_col) >= low) & (pl.col(age_col) <= high))
    return filtered.group_by(pid_col).agg(pl.col(income_col).mean().alias(income_col)).sort(pid_col)
