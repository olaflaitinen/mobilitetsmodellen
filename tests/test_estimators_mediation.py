"""Tests for the causal mediation analysis estimator."""

from __future__ import annotations

import numpy as np
import pandas as pd

from mobilitetsmodellen.estimators.mediation import MediationResult, fit_mediation


def _dyads(n: int = 300, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = rng.uniform(0, 1, n)
    edu = 0.5 * parent + rng.normal(0, 0.1, n)
    child = 0.2 * parent + 0.15 * edu + rng.normal(0, 0.05, n)
    child = np.clip(child, 0, 1)
    return pd.DataFrame(
        {
            "parent_rank": parent,
            "child_rank": child,
            "education_level": edu,
        }
    )


def test_fit_mediation_returns_result() -> None:
    result = fit_mediation(_dyads())
    assert isinstance(result, MediationResult)


def test_fit_mediation_total_effect_finite() -> None:
    result = fit_mediation(_dyads())
    assert np.isfinite(result.total_effect)


def test_fit_mediation_indirect_direct_sum() -> None:
    result = fit_mediation(_dyads())
    total_reconstructed = result.direct_effect + result.indirect_effect
    assert abs(total_reconstructed - result.total_effect) < 0.1


def test_fit_mediation_proportion_mediated_range() -> None:
    result = fit_mediation(_dyads())
    assert np.isfinite(result.proportion_mediated)


def test_fit_mediation_mediator_label() -> None:
    result = fit_mediation(_dyads(), mediator_col="education_level")
    assert result.mediator == "education_level"


def test_fit_mediation_n_correct() -> None:
    df = _dyads(n=200)
    result = fit_mediation(df)
    assert result.n == 200


def test_fit_mediation_with_controls() -> None:
    df = _dyads(n=200)
    result = fit_mediation(df, controls=[])
    assert np.isfinite(result.total_effect)
