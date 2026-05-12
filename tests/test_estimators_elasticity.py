"""Tests for the intergenerational income elasticity estimator."""

from __future__ import annotations

import numpy as np
import pandas as pd

from mobilitetsmodellen.estimators.elasticity import ElasticityResult, fit_elasticity


def _dyads(n: int = 200, ige: float = 0.3, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    log_parent = rng.normal(12.5, 0.6, n)
    log_child = ige * log_parent + (1 - ige) * 12.5 + rng.normal(0, 0.3, n)
    return pd.DataFrame(
        {
            "parent_income": np.exp(log_parent),
            "child_income": np.exp(log_child),
            "birth_year": rng.choice([1960, 1965], size=n),
        }
    )


def test_fit_elasticity_returns_result() -> None:
    results = fit_elasticity(_dyads())
    assert len(results) == 1
    assert isinstance(results[0], ElasticityResult)


def test_fit_elasticity_range() -> None:
    results = fit_elasticity(_dyads(ige=0.3))
    assert 0.1 < results[0].elasticity < 0.6


def test_fit_elasticity_se_positive() -> None:
    results = fit_elasticity(_dyads())
    assert results[0].se > 0


def test_fit_elasticity_per_cohort() -> None:
    results = fit_elasticity(_dyads(), cohort_col="birth_year")
    assert len(results) == 2


def test_fit_elasticity_attenuation_correction() -> None:
    fit_elasticity(_dyads(), correct_attenuation=False)
    results_corr = fit_elasticity(_dyads(), correct_attenuation=True, n_years_observed=1)
    assert results_corr[0].attenuation_corrected is True
    assert results_corr[0].correction_factor >= 1.0


def test_fit_elasticity_zero_income_filtered() -> None:
    df = _dyads(n=50)
    df.loc[0, "parent_income"] = 0.0
    results = fit_elasticity(df)
    assert results[0].n < 50


def test_fit_elasticity_small_sample() -> None:
    df = pd.DataFrame({"parent_income": [1.0, 2.0], "child_income": [1.0, 2.0]})
    results = fit_elasticity(df)
    assert np.isnan(results[0].elasticity)
