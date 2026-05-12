"""Tests for the causal forest estimator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def _dyads(n: int = 200, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = rng.uniform(0, 1, n)
    child = 0.3 * parent + 0.5 + rng.normal(0, 0.05, n)
    child = np.clip(child, 0, 1)
    edu = rng.uniform(0, 1, n)
    return pd.DataFrame(
        {
            "parent_rank": parent,
            "child_rank": child,
            "education_level": edu,
        }
    )


def test_causal_forest_returns_result() -> None:
    pytest.importorskip("econml")
    from mobilitetsmodellen.estimators.causal_forest import CausalForestResult, fit_causal_forest

    result = fit_causal_forest(_dyads(), n_estimators=20, seed=123)
    assert isinstance(result, CausalForestResult)
    assert np.isfinite(result.ate)


def test_causal_forest_cate_shape() -> None:
    pytest.importorskip("econml")
    from mobilitetsmodellen.estimators.causal_forest import fit_causal_forest

    df = _dyads(n=100)
    result = fit_causal_forest(df, n_estimators=20, seed=123)
    assert len(result.cate) == 100


def test_causal_forest_with_heterogeneity_cols() -> None:
    pytest.importorskip("econml")
    from mobilitetsmodellen.estimators.causal_forest import fit_causal_forest

    df = _dyads(n=100)
    result = fit_causal_forest(df, heterogeneity_cols=["education_level"], n_estimators=20)
    assert np.isfinite(result.ate)


def test_causal_forest_n_estimators_stored() -> None:
    pytest.importorskip("econml")
    from mobilitetsmodellen.estimators.causal_forest import fit_causal_forest

    result = fit_causal_forest(_dyads(n=100), n_estimators=20, seed=123)
    assert result.n_estimators == 20
