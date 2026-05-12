"""Causal forest estimator for heterogeneous intergenerational mobility."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from mobilitetsmodellen.seeds import FOREST_SEED, derive_seed


@dataclass(frozen=True)
class CausalForestResult:
    """Result container for the causal forest estimator.

    Attributes:
        ate: Average treatment effect estimate.
        ate_se: Standard error of the ATE.
        cate: Array of conditional average treatment effects per observation.
        n: Number of observations.
        n_estimators: Number of trees in the forest.
    """

    ate: float
    ate_se: float
    cate: np.ndarray  # type: ignore[type-arg]
    n: int
    n_estimators: int


def fit_causal_forest(
    dyads: pd.DataFrame,
    child_rank_col: str = "child_rank",
    parent_rank_col: str = "parent_rank",
    heterogeneity_cols: list[str] | None = None,
    n_estimators: int = 100,
    seed: int = FOREST_SEED,
) -> CausalForestResult:
    """Estimate heterogeneous intergenerational mobility via causal forests.

    Uses EconML's :class:`~econml.grf.CausalForest` with honest splitting and
    cross-fitting for heterogeneous-treatment-effect estimation across
    municipality or cohort strata.

    Args:
        dyads: DataFrame with child rank, parent rank, and optional covariates.
        child_rank_col: Column for child income rank (outcome).
        parent_rank_col: Column for parent income rank (treatment).
        heterogeneity_cols: Covariate columns for CATE estimation.
        n_estimators: Number of trees in the causal forest.
        seed: Random seed for forest initialisation.

    Returns:
        A :class:`CausalForestResult` with ATE, SE, and CATE array.
    """
    from econml.grf import CausalForest  # type: ignore[import-untyped]

    forest_seed = derive_seed("forest_init", seed)
    y = dyads[child_rank_col].to_numpy().reshape(-1, 1)
    t = dyads[parent_rank_col].to_numpy()
    if heterogeneity_cols:
        x = dyads[heterogeneity_cols].to_numpy()
    else:
        x = np.ones((len(y), 1))
    cf = CausalForest(
        n_estimators=n_estimators,
        honest=True,
        random_state=forest_seed,
        n_jobs=1,
    )
    cf.fit(x, t, y)
    cate = cf.predict(x).flatten()
    ate = float(np.mean(cate))
    ate_se_val = cf.prediction_stderr(x)
    if ate_se_val is not None:
        ate_se = float(np.mean(ate_se_val))
    else:
        ate_se = float(np.std(cate) / max(np.sqrt(len(cate)), 1.0))
    return CausalForestResult(
        ate=ate,
        ate_se=ate_se,
        cate=cate,
        n=len(y),
        n_estimators=n_estimators,
    )
