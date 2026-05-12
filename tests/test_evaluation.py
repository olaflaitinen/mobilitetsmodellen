"""Tests for evaluation metrics and bootstrap modules."""

from __future__ import annotations

import numpy as np
import pandas as pd

from mobilitetsmodellen.evaluation.bootstrap import bootstrap_ci, cluster_bootstrap_ci
from mobilitetsmodellen.evaluation.metrics import (
    calibration_score,
    mobility_mse,
    rank_correlation,
    transition_accuracy,
)


def test_rank_correlation_perfect() -> None:
    x = np.arange(10, dtype=float)
    assert rank_correlation(x, x) == pytest.approx(1.0)


def test_rank_correlation_anti() -> None:
    x = np.arange(10, dtype=float)
    assert rank_correlation(x, x[::-1]) == pytest.approx(-1.0)


def test_mobility_mse_zero() -> None:
    x = np.ones(20)
    assert mobility_mse(x, x) == pytest.approx(0.0)


def test_mobility_mse_positive() -> None:
    x = np.array([0.0, 1.0])
    y = np.array([1.0, 0.0])
    assert mobility_mse(x, y) == pytest.approx(1.0)


def test_transition_accuracy_zero() -> None:
    m = np.eye(5)
    assert transition_accuracy(m, m) == pytest.approx(0.0)


def test_calibration_score_range() -> None:
    rng = np.random.default_rng(1)
    n = 100
    estimates = rng.uniform(0.2, 0.4, n)
    ses = np.full(n, 0.05)
    true_vals = rng.uniform(0.2, 0.4, n)
    score = calibration_score(estimates, ses, true_vals)
    assert 0.0 <= score <= 1.0


def test_bootstrap_ci_returns_tuple() -> None:
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"x": rng.uniform(0, 1, 100)})
    pt, lo, hi = bootstrap_ci(df, lambda d: float(d["x"].mean()), n_bootstrap=50)
    assert lo <= pt <= hi


def test_cluster_bootstrap_ci() -> None:
    rng = np.random.default_rng(2)
    df = pd.DataFrame(
        {
            "x": rng.uniform(0, 1, 100),
            "cluster": rng.integers(0, 10, 100),
        }
    )
    pt, lo, hi = cluster_bootstrap_ci(df, lambda d: float(d["x"].mean()), "cluster", n_bootstrap=30)
    assert lo <= pt <= hi


import pytest  # noqa: E402
