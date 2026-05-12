"""Causal mediation analysis for intergenerational mobility channels."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class MediationResult:
    """Result container for causal mediation analysis.

    Attributes:
        total_effect: Total intergenerational persistence.
        direct_effect: Average controlled direct effect (ACDE).
        indirect_effect: Average causal mediation effect (ACME).
        proportion_mediated: Fraction of total effect running through mediator.
        mediator: Name of the mediator variable.
        n: Number of observations.
    """

    total_effect: float
    direct_effect: float
    indirect_effect: float
    proportion_mediated: float
    mediator: str
    n: int


def fit_mediation(
    dyads: pd.DataFrame,
    outcome_col: str = "child_rank",
    treatment_col: str = "parent_rank",
    mediator_col: str = "education_level",
    controls: list[str] | None = None,
) -> MediationResult:
    """Estimate direct and indirect intergenerational mobility effects.

    Implements a product-of-coefficients approach for linear mediation.
    For nonlinear settings, replace with a simulation-based approach.

    Args:
        dyads: DataFrame with outcome, treatment, and mediator columns.
        outcome_col: Child income rank (outcome).
        treatment_col: Parent income rank (treatment).
        mediator_col: Mediator variable (e.g. education level).
        controls: Additional covariates to condition on.

    Returns:
        A :class:`MediationResult` with decomposed effects.
    """
    if controls is None:
        controls = []
    n = len(dyads)
    y = dyads[outcome_col].to_numpy()
    t = dyads[treatment_col].to_numpy()
    m = dyads[mediator_col].to_numpy().astype(float)
    cov_cols = [treatment_col] + controls
    x_total = np.column_stack([np.ones(n), dyads[cov_cols].to_numpy()])
    coef_total, *_ = np.linalg.lstsq(x_total, y, rcond=None)
    total = float(coef_total[1])
    x_med = np.column_stack([np.ones(n), t] + [dyads[c].to_numpy() for c in controls])
    coef_med, *_ = np.linalg.lstsq(x_med, m, rcond=None)
    alpha = float(coef_med[1])
    x_full = np.column_stack([np.ones(n), t, m] + [dyads[c].to_numpy() for c in controls])
    coef_full, *_ = np.linalg.lstsq(x_full, y, rcond=None)
    direct = float(coef_full[1])
    beta = float(coef_full[2])
    indirect = alpha * beta
    proportion = indirect / total if abs(total) > 1e-12 else float("nan")
    return MediationResult(
        total_effect=total,
        direct_effect=direct,
        indirect_effect=indirect,
        proportion_mediated=proportion,
        mediator=mediator_col,
        n=n,
    )
