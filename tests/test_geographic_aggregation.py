"""Tests for geographic aggregation module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl

from mobilitetsmodellen.geographic.aggregation import (
    aggregate_by_region,
    polars_aggregate_by_region,
)


def _df(n: int = 100, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "pid": np.arange(n),
            "region": rng.integers(1, 6, size=n),
            "estimate": rng.uniform(0.1, 0.5, size=n),
            "weight": rng.uniform(0.5, 2.0, size=n),
        }
    )


def test_aggregate_by_region_returns_dataframe() -> None:
    result = aggregate_by_region(_df(), "estimate", "region")
    assert isinstance(result, pd.DataFrame)


def test_aggregate_by_region_columns() -> None:
    result = aggregate_by_region(_df(), "estimate", "region")
    assert "estimate" in result.columns
    assert "n" in result.columns
    assert "se" in result.columns


def test_aggregate_by_region_n_regions() -> None:
    df = _df()
    result = aggregate_by_region(df, "estimate", "region")
    assert len(result) == df["region"].nunique()


def test_aggregate_by_region_weighted() -> None:
    result = aggregate_by_region(_df(), "estimate", "region", weight_col="weight")
    assert "estimate" in result.columns


def test_polars_aggregate_by_region() -> None:
    df_pd = _df()
    df_pl = pl.from_pandas(df_pd)
    result = polars_aggregate_by_region(df_pl, "estimate", "region")
    assert "estimate" in result.columns
    assert "n" in result.columns
