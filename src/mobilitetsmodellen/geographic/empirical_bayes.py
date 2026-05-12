"""Empirical-Bayes shrinkage for municipality-level mobility estimates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ShrinkageResult:
    """Result of applying James-Stein shrinkage to group-level estimates.

    Attributes:
        shrunken: Array of shrunken estimates.
        shrinkage_factors: Per-group shrinkage factors in (0, 1].
        grand_mean: Prior grand mean used for shrinkage.
        between_variance: Estimated between-group variance.
        within_variances: Per-group within-group variance (se^2).
    """

    shrunken: np.ndarray  # type: ignore[type-arg]
    shrinkage_factors: np.ndarray  # type: ignore[type-arg]
    grand_mean: float
    between_variance: float
    within_variances: np.ndarray  # type: ignore[type-arg]


def james_stein_shrink(
    estimates: np.ndarray,  # type: ignore[type-arg]
    ses: np.ndarray,  # type: ignore[type-arg]
    ns: np.ndarray | None = None,  # type: ignore[type-arg]
) -> ShrinkageResult:
    """Apply James-Stein shrinkage to municipality-level estimates.

    The shrinkage factor for group j is:

        B_j = sigma2_j / (sigma2_j + tau2)

    where sigma2_j = se_j^2 is the within-group variance and tau2 is the
    between-group variance estimated by method of moments.

    Args:
        estimates: Array of group-level point estimates.
        ses: Array of standard errors corresponding to ``estimates``.
        ns: Optional array of group sizes (used for weighted grand mean).

    Returns:
        A :class:`ShrinkageResult` with shrunken estimates and shrinkage factors.
    """
    within_vars = ses**2
    if ns is not None and len(ns) == len(estimates):
        weights = ns.astype(float)
        weights /= weights.sum()
        grand_mean = float(np.dot(weights, estimates))
    else:
        grand_mean = float(np.mean(estimates))
    total_var = float(np.var(estimates, ddof=1))
    mean_within = float(np.mean(within_vars))
    between_var = max(total_var - mean_within, 0.0)
    shrinkage_factors = within_vars / np.maximum(within_vars + between_var, 1e-30)
    shrunken = (1.0 - shrinkage_factors) * estimates + shrinkage_factors * grand_mean
    return ShrinkageResult(
        shrunken=shrunken,
        shrinkage_factors=shrinkage_factors,
        grand_mean=grand_mean,
        between_variance=between_var,
        within_variances=within_vars,
    )


def shrink_dataframe(
    df: pd.DataFrame,
    estimate_col: str,
    se_col: str,
    n_col: str | None = None,
    output_col: str = "shrunken_estimate",
) -> pd.DataFrame:
    """Apply James-Stein shrinkage to a DataFrame of group estimates.

    Args:
        df: DataFrame with one row per group.
        estimate_col: Column with point estimates.
        se_col: Column with standard errors.
        n_col: Optional column with group sizes.
        output_col: Name of the output shrunken-estimate column.

    Returns:
        Input DataFrame with ``output_col`` and ``shrinkage_factor`` columns added.
    """
    estimates = df[estimate_col].to_numpy()
    ses = df[se_col].to_numpy()
    ns = df[n_col].to_numpy() if n_col is not None and n_col in df.columns else None
    result = james_stein_shrink(estimates, ses, ns)
    out = df.copy()
    out[output_col] = result.shrunken
    out["shrinkage_factor"] = result.shrinkage_factors
    return out
