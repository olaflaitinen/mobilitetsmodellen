"""Shared pytest fixtures for the mobilitetsmodellen test suite."""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl
import pytest

from mobilitetsmodellen.ingestion.flergen import synthetic_flergen
from mobilitetsmodellen.ingestion.lisa import synthetic_lisa


@pytest.fixture(scope="session")
def flergen_df() -> pl.DataFrame:
    """Synthetic Flergenerationsregistret (200 dyads, fast)."""
    return synthetic_flergen(n=200, seed=42, n_cohorts=3, n_kommuner=10)


@pytest.fixture(scope="session")
def lisa_df(flergen_df: pl.DataFrame) -> pl.DataFrame:
    """Synthetic LISA panel for child pids from flergen_df."""
    pids = flergen_df["pid"].to_numpy()
    return synthetic_lisa(pids, seed=42)


@pytest.fixture(scope="session")
def dyads_pd() -> pd.DataFrame:
    """Small synthetic dyads DataFrame for estimator tests."""
    rng = np.random.default_rng(7)
    n = 300
    parent_rank = rng.uniform(0, 1, n)
    child_rank = 0.3 * parent_rank + 0.5 + rng.normal(0, 0.1, n)
    child_rank = np.clip(child_rank, 0, 1)
    parent_income = np.exp(rng.normal(12.5, 0.6, n))
    child_income = np.exp(rng.normal(12.5, 0.6, n))
    birth_year = rng.choice([1960, 1965, 1970], size=n)
    education = rng.integers(1, 8, size=n)
    return pd.DataFrame(
        {
            "pid": np.arange(n),
            "parent_rank": parent_rank,
            "child_rank": child_rank,
            "parent_income": parent_income,
            "child_income": child_income,
            "birth_year": birth_year,
            "education_level": education,
            "kommun_code": rng.integers(100, 110, size=n),
        }
    )
