"""Reader and synthetic generator for the LISA panel."""

from __future__ import annotations

import pathlib

import numpy as np
import polars as pl


def read_lisa(path: pathlib.Path) -> pl.DataFrame:
    """Read the LISA longitudinal register from a Parquet file.

    Args:
        path: Path to the Parquet file or directory.

    Returns:
        A Polars DataFrame with columns ``pid``, ``year``, ``income``,
        ``education_level``, ``occupation_code``.
    """
    return pl.read_parquet(path)


def synthetic_lisa(
    pids: np.ndarray,  # type: ignore[type-arg]
    seed: int = 19960307,
    income_mean: float = 300_000.0,
    income_std: float = 150_000.0,
) -> pl.DataFrame:
    """Generate synthetic LISA-compatible income and covariate data.

    Args:
        pids: Array of person identifiers for which to generate records.
        seed: Random seed for reproducibility.
        income_mean: Mean income in SEK.
        income_std: Standard deviation of income in SEK.

    Returns:
        A Polars DataFrame with one row per person per year (ages 30-50).
    """
    rng = np.random.default_rng(seed)
    n = len(pids)
    years_per_person = 21
    all_pids = np.repeat(pids, years_per_person)
    all_ages = np.tile(np.arange(30, 51), n)
    incomes = np.maximum(rng.normal(income_mean, income_std, size=n * years_per_person), 0.0)
    edu_levels = rng.integers(1, 8, size=n * years_per_person)
    occ_codes = rng.integers(1000, 9999, size=n * years_per_person)
    return pl.DataFrame(
        {
            "pid": all_pids.astype(np.int64),
            "age": all_ages.astype(np.int32),
            "income": incomes,
            "education_level": edu_levels.astype(np.int32),
            "occupation_code": occ_codes.astype(np.int32),
        }
    )
