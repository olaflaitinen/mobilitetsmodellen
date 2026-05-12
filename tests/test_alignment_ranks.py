"""Tests for rank-construction module including hypothesis property tests."""

from __future__ import annotations

import numpy as np
import polars as pl
from hypothesis import given, settings
from hypothesis import strategies as st

from mobilitetsmodellen.alignment.ranks import compute_country_cohort_ranks, compute_ranks


def _df(incomes: list[float], cohort: int = 1960) -> pl.DataFrame:
    return pl.DataFrame(
        {
            "pid": list(range(1, len(incomes) + 1)),
            "birth_year": [cohort] * len(incomes),
            "income": incomes,
        }
    )


def test_ranks_in_unit_interval() -> None:
    df = _df([100.0, 200.0, 300.0, 400.0, 500.0])
    result = compute_ranks(df)
    ranks = result["rank"].to_numpy()
    assert (ranks >= 0).all() and (ranks <= 1).all()


def test_ranks_monotone_increasing() -> None:
    incomes = [100.0, 200.0, 300.0, 400.0, 500.0]
    df = _df(incomes)
    result = compute_ranks(df)
    sorted_result = result.sort("income")
    ranks = sorted_result["rank"].to_numpy()
    assert (np.diff(ranks) >= 0).all(), "Ranks must be non-decreasing in income"


def test_ranks_ties_deterministic() -> None:
    df = _df([100.0, 100.0, 200.0])
    r1 = compute_ranks(df)
    r2 = compute_ranks(df)
    assert r1["rank"].to_list() == r2["rank"].to_list()


def test_ranks_two_cohorts() -> None:
    df = pl.DataFrame(
        {
            "pid": [1, 2, 3, 4],
            "birth_year": [1960, 1960, 1965, 1965],
            "income": [100.0, 200.0, 150.0, 250.0],
        }
    )
    result = compute_ranks(df)
    assert len(result) == 4


def test_country_cohort_ranks_alias() -> None:
    df = _df([100.0, 300.0, 200.0])
    r1 = compute_ranks(df, rank_col="rank")
    r2 = compute_country_cohort_ranks(df, rank_col="rank")
    assert r1["rank"].to_list() == r2["rank"].to_list()


@given(
    incomes=st.lists(
        st.floats(min_value=1.0, max_value=1_000_000.0, allow_nan=False),
        min_size=2,
        max_size=50,
    )
)
@settings(max_examples=50)
def test_ranks_monotone_property(incomes: list[float]) -> None:
    """Hypothesis: ranks are monotone non-decreasing in income."""
    df = pl.DataFrame(
        {
            "pid": list(range(len(incomes))),
            "birth_year": [1960] * len(incomes),
            "income": incomes,
        }
    )
    result = compute_ranks(df).sort("income")
    ranks = result["rank"].to_numpy()
    assert (np.diff(ranks) >= -1e-10).all()
