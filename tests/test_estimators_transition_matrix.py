"""Tests for the quintile transition matrix estimator."""

from __future__ import annotations

import numpy as np
import pandas as pd

from mobilitetsmodellen.estimators.transition_matrix import fit_transition


def _dyads(n: int = 500, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = np.exp(rng.normal(12.5, 0.6, n))
    child = np.exp(rng.normal(12.5, 0.6, n))
    return pd.DataFrame(
        {
            "parent_income": parent,
            "child_income": child,
            "birth_year": rng.choice([1960, 1965], size=n),
        }
    )


def test_fit_transition_shape() -> None:
    results = fit_transition(_dyads(), n_bootstrap=10)
    assert len(results) == 1
    assert results[0].matrix.shape == (5, 5)


def test_fit_transition_rows_sum_to_one() -> None:
    results = fit_transition(_dyads(n=1000), n_bootstrap=10)
    row_sums = results[0].matrix.sum(axis=1)
    np.testing.assert_allclose(row_sums, np.ones(5), atol=0.01)


def test_fit_transition_se_shape() -> None:
    results = fit_transition(_dyads(), n_bootstrap=20)
    assert results[0].se.shape == (5, 5)


def test_fit_transition_probabilities_nonneg() -> None:
    results = fit_transition(_dyads(), n_bootstrap=10)
    assert (results[0].matrix >= 0).all()


def test_fit_transition_per_cohort() -> None:
    results = fit_transition(_dyads(), cohort_col="birth_year", n_bootstrap=5)
    assert len(results) == 2


def test_fit_transition_deterministic() -> None:
    d = _dyads()
    r1 = fit_transition(d, n_bootstrap=20, seed=7)
    r2 = fit_transition(d, n_bootstrap=20, seed=7)
    np.testing.assert_array_equal(r1[0].matrix, r2[0].matrix)
