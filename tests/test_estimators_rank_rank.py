"""Tests for the rank-rank slope estimator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from mobilitetsmodellen.estimators.rank_rank import RankRankResult, fit_rank_rank


def _dyads(n: int = 200, slope: float = 0.3, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = rng.uniform(0, 1, n)
    child = slope * parent + 0.5 * (1 - slope) + rng.normal(0, 0.05, n)
    child = np.clip(child, 0, 1)
    return pd.DataFrame(
        {
            "parent_rank": parent,
            "child_rank": child,
            "birth_year": rng.choice([1960, 1965], size=n),
            "kommun_code": rng.integers(100, 110, size=n),
        }
    )


def test_fit_rank_rank_returns_result() -> None:
    results = fit_rank_rank(_dyads())
    assert len(results) == 1
    assert isinstance(results[0], RankRankResult)


def test_fit_rank_rank_slope_range() -> None:
    results = fit_rank_rank(_dyads(slope=0.3))
    assert 0.1 < results[0].slope < 0.6


def test_fit_rank_rank_se_positive() -> None:
    results = fit_rank_rank(_dyads())
    assert results[0].se > 0


def test_fit_rank_rank_n_correct() -> None:
    df = _dyads(n=150)
    results = fit_rank_rank(df)
    assert results[0].n == 150


def test_fit_rank_rank_cohort_splits() -> None:
    results = fit_rank_rank(_dyads(), cohort_col="birth_year")
    assert len(results) == 2


def test_fit_rank_rank_cluster_robust() -> None:
    df = _dyads()
    results = fit_rank_rank(df, cluster_col="kommun_code")
    assert results[0].se > 0


def test_fit_rank_rank_result_frozen() -> None:
    r = RankRankResult(slope=0.3, se=0.05, n=100)
    with pytest.raises(Exception):
        r.slope = 0.5  # type: ignore[misc]
