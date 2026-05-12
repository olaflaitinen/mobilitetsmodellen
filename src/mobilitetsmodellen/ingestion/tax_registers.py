"""Reader and synthetic generator for Swedish tax registers."""

from __future__ import annotations

import pathlib

import numpy as np
import polars as pl


def read_tax_register(path: pathlib.Path) -> pl.DataFrame:
    """Read a Skatteverket income/wealth register from a Parquet file.

    Args:
        path: Path to the Parquet file or directory.

    Returns:
        A Polars DataFrame with columns ``pid``, ``year``, ``taxable_income``,
        ``capital_income``, ``wealth``.
    """
    return pl.read_parquet(path)


def synthetic_tax_register(
    pids: np.ndarray,  # type: ignore[type-arg]
    seed: int = 19960307,
) -> pl.DataFrame:
    """Generate synthetic Skatteverket-compatible register data.

    Args:
        pids: Array of person identifiers.
        seed: Random seed for reproducibility.

    Returns:
        A Polars DataFrame with one row per person per year (2000-2020).
    """
    rng = np.random.default_rng(seed)
    n = len(pids)
    n_years = 21
    years = list(range(2000, 2021))
    all_pids = np.repeat(pids, n_years)
    all_years = np.tile(np.array(years, dtype=np.int32), n)
    taxable = np.maximum(rng.lognormal(12.5, 0.6, size=n * n_years), 0.0)
    capital = np.maximum(rng.lognormal(9.0, 1.2, size=n * n_years), 0.0)
    wealth = np.maximum(rng.lognormal(12.0, 1.5, size=n * n_years), 0.0)
    return pl.DataFrame(
        {
            "pid": all_pids.astype(np.int64),
            "year": all_years,
            "taxable_income": taxable,
            "capital_income": capital,
            "wealth": wealth,
        }
    )
