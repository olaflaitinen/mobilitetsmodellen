"""Geographic aggregation of mobility estimates by region type."""

from __future__ import annotations

from typing import Literal

import pandas as pd
import polars as pl

RegionType = Literal["kommun", "lan", "fa_region"]


def aggregate_by_region(
    dyads: pd.DataFrame,
    estimates_col: str,
    region_col: str,
    region_type: RegionType = "kommun",
    weight_col: str | None = None,
) -> pd.DataFrame:
    """Aggregate point estimates by geographic region.

    Args:
        dyads: DataFrame with one row per dyad and mobility estimates.
        estimates_col: Column containing the mobility point estimate.
        region_col: Column containing the region identifier.
        region_type: Type of geographic aggregation (for labelling only).
        weight_col: Optional column of observation weights.

    Returns:
        A DataFrame with columns ``region_col``, ``estimate`` (weighted mean),
        ``n`` (count), and ``se`` (standard error of the mean).
    """
    grouped = dyads.groupby(region_col)
    records = []
    for region, group in grouped:
        vals = group[estimates_col].to_numpy()
        n = len(vals)
        if weight_col is not None and weight_col in group.columns:
            w = group[weight_col].to_numpy()
            w = w / w.sum()
            mean = float(vals @ w)
        else:
            mean = float(vals.mean())
        se = float(vals.std(ddof=1) / max(n**0.5, 1.0))
        records.append(
            {"region": region, "region_type": region_type, "estimate": mean, "n": n, "se": se}
        )
    return pd.DataFrame(records).sort_values("region").reset_index(drop=True)


def polars_aggregate_by_region(
    dyads: pl.DataFrame,
    estimates_col: str,
    region_col: str,
) -> pl.DataFrame:
    """Aggregate mobility estimates by region using Polars.

    Args:
        dyads: Polars DataFrame.
        estimates_col: Column with mobility estimates.
        region_col: Column with region codes.

    Returns:
        Aggregated Polars DataFrame.
    """
    return (
        dyads.group_by(region_col)
        .agg(
            [
                pl.col(estimates_col).mean().alias("estimate"),
                pl.col(estimates_col).count().alias("n"),
                pl.col(estimates_col).std().alias("se_raw"),
            ]
        )
        .with_columns((pl.col("se_raw") / pl.col("n").sqrt()).alias("se"))
        .drop("se_raw")
        .sort(region_col)
    )
