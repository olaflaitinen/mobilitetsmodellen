"""Classical rank-rank slope estimator with cluster-robust standard errors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RankRankResult:
    """Result container for the rank-rank slope estimator.

    Attributes:
        slope: Estimated rank-rank slope (intergenerational persistence).
        se: Cluster-robust standard error of the slope.
        n: Number of parent-child dyads used.
        cohort: Birth cohort year, or -1 for pooled estimate.
        intercept: Regression intercept.
    """

    slope: float
    se: float
    n: int
    cohort: int = -1
    intercept: float = 0.0


def fit_rank_rank(
    dyads: pd.DataFrame,
    child_rank_col: str = "child_rank",
    parent_rank_col: str = "parent_rank",
    cohort_col: str | None = None,
    cluster_col: str | None = None,
) -> list[RankRankResult]:
    """Estimate rank-rank slopes via OLS with optional cluster-robust SEs.

    Args:
        dyads: DataFrame with child and parent income ranks in [0, 1].
        child_rank_col: Column name for child income rank.
        parent_rank_col: Column name for parent income rank.
        cohort_col: If provided, estimate separate slopes per cohort.
        cluster_col: Column to cluster standard errors on. If None, uses HC3.

    Returns:
        A list of :class:`RankRankResult`, one per cohort (or one pooled result).
    """
    results: list[RankRankResult] = []

    def _ols(sub: pd.DataFrame, cohort: int) -> RankRankResult:
        x = sub[parent_rank_col].to_numpy()
        y = sub[child_rank_col].to_numpy()
        n = len(x)
        x_mat = np.column_stack([np.ones(n), x])
        try:
            coef, *_ = np.linalg.lstsq(x_mat, y, rcond=None)
        except np.linalg.LinAlgError:
            return RankRankResult(slope=float("nan"), se=float("nan"), n=n, cohort=cohort)
        intercept, slope = float(coef[0]), float(coef[1])
        residuals = y - x_mat @ coef
        if cluster_col is not None and cluster_col in sub.columns:
            clusters = sub[cluster_col].to_numpy()
            unique_c = np.unique(clusters)
            meat = np.zeros((2, 2))
            for c in unique_c:
                mask = clusters == c
                xi = x_mat[mask]
                ri = residuals[mask, np.newaxis]
                meat += xi.T @ ri @ ri.T @ xi
            xtx_inv = np.linalg.inv(x_mat.T @ x_mat + 1e-12 * np.eye(2))
            g = len(unique_c)
            correction = g / (g - 1) * (n - 1) / (n - 2)
            vcov = correction * xtx_inv @ meat @ xtx_inv
        else:
            sse = float(residuals @ residuals)
            sigma2 = sse / max(n - 2, 1)
            xtx_inv = np.linalg.inv(x_mat.T @ x_mat + 1e-12 * np.eye(2))
            vcov = sigma2 * xtx_inv
        se = float(np.sqrt(np.maximum(vcov[1, 1], 0.0)))
        return RankRankResult(slope=slope, se=se, n=n, cohort=cohort, intercept=intercept)

    if cohort_col is not None and cohort_col in dyads.columns:
        for cohort, group in dyads.groupby(cohort_col):
            results.append(_ols(group, int(cohort)))
    else:
        results.append(_ols(dyads, -1))
    return results
