"""Spatial-correlation analysis for municipality-level mobility estimates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class MoransIResult:
    """Result of Moran's I spatial-autocorrelation test.

    Attributes:
        statistic: Moran's I statistic.
        expected: Expected value under null of no spatial autocorrelation.
        variance: Variance of the statistic under null.
        z_score: Standardised z-score.
        p_value: Two-tailed p-value under normal approximation.
        n: Number of spatial units.
    """

    statistic: float
    expected: float
    variance: float
    z_score: float
    p_value: float
    n: int


def morans_i(
    values: np.ndarray,  # type: ignore[type-arg]
    weights: np.ndarray,  # type: ignore[type-arg]
) -> MoransIResult:
    """Compute Moran's I spatial-autocorrelation statistic.

    Args:
        values: Array of n observed values (e.g. municipality-level rank-rank slopes).
        weights: (n, n) row-standardised spatial-weights matrix (W[i,i] = 0).

    Returns:
        A :class:`MoransIResult` with the test statistic and inference.
    """
    n = len(values)
    z = values - values.mean()
    w_sum = float(weights.sum())
    if abs(w_sum) < 1e-15 or n < 3:
        return MoransIResult(
            statistic=float("nan"),
            expected=-1.0 / max(n - 1, 1),
            variance=float("nan"),
            z_score=float("nan"),
            p_value=float("nan"),
            n=n,
        )
    numerator = float(z @ weights @ z)
    denominator = float(z @ z)
    mi = (n / w_sum) * (numerator / max(denominator, 1e-30))
    expected = -1.0 / (n - 1)
    s1 = 0.5 * float(np.sum((weights + weights.T) ** 2))
    s2 = float(np.sum((np.sum(weights, axis=1) + np.sum(weights, axis=0)) ** 2))
    n2 = n * n
    var_num = n * ((n2 - 3 * n + 3) * s1 - n * s2 + 3 * w_sum**2)
    var_denom = (n - 1) * (n - 2) * (n - 3) * w_sum**2
    kurtosis = float(n * np.sum(z**4)) / max(float(np.sum(z**2)) ** 2, 1e-30)
    var_num -= kurtosis * ((n2 - n) * s1 - 2 * n * s2 + 6 * w_sum**2)
    variance = (var_num / max(var_denom, 1e-30)) - expected**2
    variance = max(variance, 1e-30)
    z_score = (mi - expected) / np.sqrt(variance)
    from scipy.stats import norm  # type: ignore[import-untyped]

    p_value = float(2.0 * (1.0 - norm.cdf(abs(float(z_score)))))
    return MoransIResult(
        statistic=mi,
        expected=expected,
        variance=variance,
        z_score=float(z_score),
        p_value=p_value,
        n=n,
    )


def row_standardise(w: np.ndarray) -> np.ndarray:  # type: ignore[type-arg]
    """Row-standardise a spatial weights matrix.

    Args:
        w: (n, n) non-negative weights matrix.

    Returns:
        Row-standardised matrix with row sums equal to 1 (or 0 for isolated units).
    """
    row_sums = w.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1.0, row_sums)
    return w / row_sums


def contiguity_weights(df: pd.DataFrame, region_col: str) -> np.ndarray:  # type: ignore[type-arg]
    """Build a simple identity-neighbour weights matrix from a region column.

    This is a placeholder that returns a zero matrix. In production, replace
    with a geopandas-based contiguity computation.

    Args:
        df: DataFrame with a region identifier column.
        region_col: Name of the region column.

    Returns:
        An (n, n) zero-diagonal weights matrix.
    """
    n = df[region_col].nunique()
    return np.zeros((n, n))
