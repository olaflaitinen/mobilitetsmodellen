"""Tests for spatial analysis module."""

from __future__ import annotations

import numpy as np

from mobilitetsmodellen.geographic.spatial import MoransIResult, morans_i, row_standardise


def _random_w(n: int = 10, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    w = rng.uniform(0, 1, (n, n))
    np.fill_diagonal(w, 0)
    return row_standardise(w)


def test_morans_i_returns_result() -> None:
    n = 15
    values = np.random.default_rng(1).uniform(0, 1, n)
    w = _random_w(n)
    result = morans_i(values, w)
    assert isinstance(result, MoransIResult)


def test_morans_i_statistic_finite() -> None:
    n = 15
    values = np.random.default_rng(1).uniform(0, 1, n)
    w = _random_w(n)
    result = morans_i(values, w)
    assert np.isfinite(result.statistic)


def test_morans_i_p_value_range() -> None:
    n = 20
    values = np.random.default_rng(2).uniform(0, 1, n)
    w = _random_w(n)
    result = morans_i(values, w)
    assert 0.0 <= result.p_value <= 1.0


def test_row_standardise_rows_sum_one() -> None:
    w = np.array([[0.0, 1.0, 1.0], [0.5, 0.0, 0.5], [1.0, 1.0, 0.0]])
    ws = row_standardise(w)
    np.testing.assert_allclose(ws.sum(axis=1), np.ones(3), atol=1e-10)


def test_morans_i_small_sample_nan() -> None:
    values = np.array([0.1, 0.5])
    w = np.zeros((2, 2))
    result = morans_i(values, w)
    assert np.isnan(result.statistic)


def test_morans_i_n_stored() -> None:
    n = 10
    values = np.random.default_rng(3).uniform(0, 1, n)
    w = _random_w(n)
    result = morans_i(values, w)
    assert result.n == n
