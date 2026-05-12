"""Tests for empirical-Bayes shrinkage module."""

from __future__ import annotations

import numpy as np
import pandas as pd

from mobilitetsmodellen.geographic.empirical_bayes import james_stein_shrink, shrink_dataframe


def _estimates(n: int = 30, seed: int = 1) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    ns = rng.integers(20, 200, size=n).astype(float)
    estimates = rng.uniform(0.1, 0.5, size=n)
    ses = rng.uniform(0.02, 0.15, size=n)
    return estimates, ses, ns


def test_shrinkage_output_shape() -> None:
    estimates, ses, ns = _estimates()
    result = james_stein_shrink(estimates, ses, ns)
    assert len(result.shrunken) == len(estimates)


def test_shrinkage_factors_in_unit_interval() -> None:
    estimates, ses, ns = _estimates()
    result = james_stein_shrink(estimates, ses, ns)
    assert (result.shrinkage_factors >= 0).all()
    assert (result.shrinkage_factors <= 1).all()


def test_shrinkage_factors_monotone_in_sample_size() -> None:
    """Shrinkage factors decrease as within-municipality sample size increases."""
    rng = np.random.default_rng(42)
    n = 20
    estimates = rng.uniform(0.1, 0.5, size=n)
    small_ses = np.full(n, 0.15)
    large_ses = np.full(n, 0.02)
    r_small = james_stein_shrink(estimates, small_ses)
    r_large = james_stein_shrink(estimates, large_ses)
    assert r_small.shrinkage_factors.mean() > r_large.shrinkage_factors.mean()


def test_shrinkage_increases_in_between_variance() -> None:
    """Larger between-group variance reduces shrinkage."""
    rng = np.random.default_rng(7)
    n = 30
    ses = np.full(n, 0.05)
    low_var = rng.uniform(0.24, 0.26, size=n)
    high_var = rng.uniform(0.0, 0.5, size=n)
    r_low = james_stein_shrink(low_var, ses)
    r_high = james_stein_shrink(high_var, ses)
    assert r_high.shrinkage_factors.mean() <= r_low.shrinkage_factors.mean()


def test_shrink_dataframe() -> None:
    estimates, ses, ns = _estimates()
    df = pd.DataFrame({"estimate": estimates, "se": ses, "n": ns})
    out = shrink_dataframe(df, "estimate", "se", "n")
    assert "shrunken_estimate" in out.columns
    assert "shrinkage_factor" in out.columns


def test_shrink_without_ns() -> None:
    estimates, ses, _ = _estimates()
    result = james_stein_shrink(estimates, ses)
    assert len(result.shrunken) == len(estimates)
