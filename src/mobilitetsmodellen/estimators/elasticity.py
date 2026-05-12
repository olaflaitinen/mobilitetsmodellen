"""Intergenerational income elasticity (IGE) estimator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ElasticityResult:
    """Result container for the IGE estimator.

    Attributes:
        elasticity: Log-log slope (intergenerational income elasticity).
        se: Standard error of the elasticity estimate.
        n: Number of dyads used.
        cohort: Birth cohort year, or -1 for pooled.
        attenuation_corrected: Whether attenuation-bias correction was applied.
        correction_factor: The attenuation correction factor applied (1.0 if none).
    """

    elasticity: float
    se: float
    n: int
    cohort: int = -1
    attenuation_corrected: bool = False
    correction_factor: float = 1.0


def fit_elasticity(
    dyads: pd.DataFrame,
    child_income_col: str = "child_income",
    parent_income_col: str = "parent_income",
    cohort_col: str | None = None,
    correct_attenuation: bool = False,
    n_years_observed: int = 1,
) -> list[ElasticityResult]:
    """Estimate the intergenerational income elasticity via log-log OLS.

    Args:
        dyads: DataFrame with child and parent income (positive values).
        child_income_col: Column name for child income.
        parent_income_col: Column name for parent income.
        cohort_col: If provided, estimate separate elasticities per cohort.
        correct_attenuation: Apply attenuation-bias correction for transitory shocks.
        n_years_observed: Number of years of income averaged; used for correction.

    Returns:
        A list of :class:`ElasticityResult`.
    """
    results: list[ElasticityResult] = []

    def _fit(sub: pd.DataFrame, cohort: int) -> ElasticityResult:
        mask = (sub[child_income_col] > 0) & (sub[parent_income_col] > 0)
        sub = sub[mask]
        n = len(sub)
        if n < 4:
            return ElasticityResult(elasticity=float("nan"), se=float("nan"), n=n, cohort=cohort)
        log_child = np.log(sub[child_income_col].to_numpy())
        log_parent = np.log(sub[parent_income_col].to_numpy())
        x_mat = np.column_stack([np.ones(n), log_parent])
        coef, *_ = np.linalg.lstsq(x_mat, log_child, rcond=None)
        ige = float(coef[1])
        residuals = log_child - x_mat @ coef
        sse = float(residuals @ residuals)
        sigma2 = sse / max(n - 2, 1)
        xtx_inv = np.linalg.inv(x_mat.T @ x_mat + 1e-12 * np.eye(2))
        se = float(np.sqrt(max(sigma2 * xtx_inv[1, 1], 0.0)))
        correction = 1.0
        if correct_attenuation:
            var_perm = np.var(log_parent, ddof=1)
            var_trans = var_perm / max(n_years_observed, 1)
            correction = max((var_perm + var_trans) / max(var_perm, 1e-12), 1.0)
            ige = ige * correction
            se = se * correction
        return ElasticityResult(
            elasticity=ige,
            se=se,
            n=n,
            cohort=cohort,
            attenuation_corrected=correct_attenuation,
            correction_factor=correction,
        )

    if cohort_col is not None and cohort_col in dyads.columns:
        for cohort, group in dyads.groupby(cohort_col):
            results.append(_fit(group, int(cohort)))
    else:
        results.append(_fit(dyads, -1))
    return results
