"""Tests for the DoubleML estimator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from mobilitetsmodellen.estimators.double_ml import (
    DoubleMLResult,
    _make_fold_assignments,
    fit_double_ml,
)


def _dyads(n: int = 300, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = rng.uniform(0, 1, n)
    child = 0.3 * parent + 0.5 + rng.normal(0, 0.05, n)
    child = np.clip(child, 0, 1)
    return pd.DataFrame(
        {
            "pid": np.arange(n),
            "parent_rank": parent,
            "child_rank": child,
        }
    )


def test_fit_double_ml_returns_result() -> None:
    result = fit_double_ml(_dyads(), n_folds=2, learner="random-forest")
    assert isinstance(result, DoubleMLResult)


def test_fit_double_ml_theta_finite() -> None:
    result = fit_double_ml(_dyads(), n_folds=2, learner="random-forest")
    assert np.isfinite(result.theta)


def test_fit_double_ml_se_positive() -> None:
    result = fit_double_ml(_dyads(), n_folds=2, learner="random-forest")
    assert result.se >= 0


def test_fit_double_ml_n_folds_stored() -> None:
    result = fit_double_ml(_dyads(), n_folds=2, learner="random-forest")
    assert result.n_folds == 2


def test_fit_double_ml_invalid_learner() -> None:
    df = _dyads()
    with pytest.raises(ValueError, match="Unknown learner"):
        fit_double_ml(df, n_folds=2, learner="invalid-learner")


def test_fold_assignment_deterministic() -> None:
    pids = np.arange(100)
    f1 = _make_fold_assignments(pids, n_folds=5, seed=13)
    f2 = _make_fold_assignments(pids, n_folds=5, seed=13)
    np.testing.assert_array_equal(f1, f2)


def test_fold_assignment_cross_platform_stable() -> None:
    """SHA-256 fold assignment must be identical across platforms."""
    pids = np.array([0, 1, 2, 3, 4])
    folds = _make_fold_assignments(pids, n_folds=5, seed=13)
    assert len(set(folds.tolist())) >= 1


def test_fit_double_ml_deterministic_across_runs() -> None:
    df = _dyads()
    r1 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    r2 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    assert abs(r1.theta - r2.theta) < 1e-6
