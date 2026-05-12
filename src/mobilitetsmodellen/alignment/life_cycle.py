"""Life-cycle alignment: construct canonical income observations at ages 35-45."""

from __future__ import annotations

import polars as pl

from mobilitetsmodellen.alignment.windows import WindowType, apply_window

DEFAULT_AGES: list[int] = list(range(35, 46))


def align(
    panel: pl.DataFrame,
    ages: list[int] = DEFAULT_AGES,
    window: WindowType = "three",
    income_col: str = "income",
    age_col: str = "age",
    pid_col: str = "pid",
) -> pl.DataFrame:
    """Align income observations to canonical life-cycle ages.

    Filters ``panel`` to the specified ages, then applies an averaging window.
    This addresses life-cycle bias arising from measuring income at non-peak ages.

    Args:
        panel: Panel DataFrame with one row per person per age.
        ages: Canonical age range to retain before windowing.
        window: Averaging window width.
        income_col: Name of the income column.
        age_col: Name of the age column.
        pid_col: Name of the person identifier column.

    Returns:
        A DataFrame with one row per person containing their life-cycle-aligned
        income estimate.
    """
    center_age = ages[len(ages) // 2]
    filtered = panel.filter(pl.col(age_col).is_in(ages))
    return apply_window(
        filtered,
        window=window,
        income_col=income_col,
        age_col=age_col,
        pid_col=pid_col,
        center_age=center_age,
    )
