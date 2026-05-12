"""Reader and synthetic generator for the Flergenerationsregistret."""

from __future__ import annotations

import pathlib

import numpy as np
import polars as pl


def read_flergen(path: pathlib.Path) -> pl.DataFrame:
    """Read the multi-generational register from a Parquet file.

    Args:
        path: Path to the Parquet file or directory.

    Returns:
        A Polars DataFrame with columns ``pid``, ``parent_pid``, ``birth_year``,
        ``parent_birth_year``, ``kommun_code``.
    """
    return pl.read_parquet(path)


def synthetic_flergen(
    n: int = 100_000,
    seed: int = 19960307,
    n_cohorts: int = 5,
    n_kommuner: int = 50,
) -> pl.DataFrame:
    """Generate a synthetic Flergenerationsregistret dataset.

    No real personal data is used. All identifiers are random integers.

    Args:
        n: Number of parent-child dyads to generate.
        seed: Random seed for reproducibility.
        n_cohorts: Number of birth cohorts (starting 1960, step 5 years).
        n_kommuner: Number of synthetic municipality codes.

    Returns:
        A Polars DataFrame with synthetic register-compatible columns.
    """
    rng = np.random.default_rng(seed)
    base_year = 1960
    cohort_years = [base_year + i * 5 for i in range(n_cohorts)]
    child_cohorts = rng.choice(cohort_years, size=n)
    parent_cohorts = child_cohorts - rng.integers(25, 35, size=n)
    kommun_codes = rng.integers(100, 100 + n_kommuner, size=n)
    return pl.DataFrame(
        {
            "pid": np.arange(1, n + 1, dtype=np.int64),
            "parent_pid": np.arange(n + 1, 2 * n + 1, dtype=np.int64),
            "birth_year": child_cohorts.astype(np.int32),
            "parent_birth_year": parent_cohorts.astype(np.int32),
            "kommun_code": kommun_codes.astype(np.int32),
        }
    )
