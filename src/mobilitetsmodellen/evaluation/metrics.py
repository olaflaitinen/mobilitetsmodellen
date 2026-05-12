"""Evaluation metrics for mobility estimators."""

from __future__ import annotations

import numpy as np
from scipy.stats import spearmanr  # type: ignore[import-untyped]


def rank_correlation(
    y_true: np.ndarray,  # type: ignore[type-arg]
    y_pred: np.ndarray,  # type: ignore[type-arg]
) -> float:
    """Compute Spearman rank correlation between predicted and observed ranks.

    Args:
        y_true: Array of observed values or ranks.
        y_pred: Array of predicted values or ranks.

    Returns:
        Spearman rho in [-1, 1].
    """
    rho, _ = spearmanr(y_true, y_pred)
    return float(rho)


def transition_accuracy(
    true_matrix: np.ndarray,  # type: ignore[type-arg]
    pred_matrix: np.ndarray,  # type: ignore[type-arg]
) -> float:
    """Compute mean absolute deviation between two transition matrices.

    Args:
        true_matrix: (K, K) observed transition probability matrix.
        pred_matrix: (K, K) predicted transition probability matrix.

    Returns:
        Mean absolute deviation (lower is better).
    """
    return float(np.mean(np.abs(true_matrix - pred_matrix)))


def mobility_mse(
    y_true: np.ndarray,  # type: ignore[type-arg]
    y_pred: np.ndarray,  # type: ignore[type-arg]
) -> float:
    """Compute mean-squared error between predicted and observed mobility.

    Args:
        y_true: Array of observed values.
        y_pred: Array of predicted values.

    Returns:
        Mean squared error (lower is better).
    """
    diff = y_true - y_pred
    return float(np.mean(diff**2))


def calibration_score(
    estimates: np.ndarray,  # type: ignore[type-arg]
    ses: np.ndarray,  # type: ignore[type-arg]
    true_values: np.ndarray,  # type: ignore[type-arg]
    level: float = 0.95,
) -> float:
    """Compute empirical coverage of nominal confidence intervals.

    Args:
        estimates: Array of point estimates.
        ses: Array of standard errors corresponding to ``estimates``.
        true_values: Array of true parameter values.
        level: Nominal coverage level (e.g. 0.95 for 95 percent CI).

    Returns:
        Empirical coverage proportion (should approximate ``level`` if calibrated).
    """
    from scipy.stats import norm  # type: ignore[import-untyped]

    z = float(norm.ppf(0.5 + level / 2.0))
    lower = estimates - z * ses
    upper = estimates + z * ses
    covered = (true_values >= lower) & (true_values <= upper)
    return float(np.mean(covered))
