"""Rank construction within cohort and country-cohort strata."""

from __future__ import annotations

import polars as pl


def compute_ranks(
    df: pl.DataFrame,
    income_col: str = "income",
    cohort_col: str = "birth_year",
    rank_col: str = "rank",
    method: str = "average",
) -> pl.DataFrame:
    """Compute income ranks within each cohort stratum.

    Ranks are scaled to [0, 1] so that the bottom of the distribution has rank 0
    and the top has rank 1. Ties receive average rank (mid-point of tied range).

    Args:
        df: DataFrame with income and cohort columns.
        income_col: Column name for income.
        cohort_col: Column name for birth cohort.
        rank_col: Name of the new rank column to add.
        method: Rank method passed to :func:`polars.Expr.rank`.

    Returns:
        Input DataFrame with an additional ``rank_col`` column in [0, 1].
    """
    return (
        df.with_columns(
            pl.col(income_col)
            .rank(method=method, descending=False)  # type: ignore[call-arg]
            .over(cohort_col)
            .alias("_raw_rank")
        )
        .with_columns(
            (
                (pl.col("_raw_rank") - 1)
                / (pl.col("_raw_rank").over(cohort_col).max() - 1).clip(1, None)
            ).alias(rank_col)
        )
        .drop("_raw_rank")
    )


def compute_country_cohort_ranks(
    df: pl.DataFrame,
    income_col: str = "income",
    cohort_col: str = "birth_year",
    rank_col: str = "rank",
) -> pl.DataFrame:
    """Compute income ranks pooling all individuals within a cohort nationally.

    Args:
        df: DataFrame with income and cohort columns.
        income_col: Column name for income.
        cohort_col: Column name for birth cohort.
        rank_col: Name of the new rank column to add.

    Returns:
        Input DataFrame with an additional ``rank_col`` column in [0, 1].
    """
    return compute_ranks(
        df,
        income_col=income_col,
        cohort_col=cohort_col,
        rank_col=rank_col,
    )
