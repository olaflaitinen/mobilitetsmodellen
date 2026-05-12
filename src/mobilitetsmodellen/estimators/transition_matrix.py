"""Quintile-to-quintile transition matrix estimator."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from mobilitetsmodellen.seeds import BOOTSTRAP_SEED


@dataclass(frozen=True)
class TransitionResult:
    """Result container for transition matrix estimation.

    Attributes:
        matrix: (5, 5) array of transition probabilities; rows = parent quintile,
            columns = child quintile.
        se: (5, 5) array of bootstrap standard errors.
        n: Total number of dyads.
        cohort: Birth cohort year, or -1 for pooled.
        n_bootstrap: Number of bootstrap replicates used.
    """

    matrix: np.ndarray  # type: ignore[type-arg]
    se: np.ndarray  # type: ignore[type-arg]
    n: int
    cohort: int = -1
    n_bootstrap: int = 200
    labels: list[str] = field(default_factory=lambda: ["Q1", "Q2", "Q3", "Q4", "Q5"])


def _quintile(x: np.ndarray) -> np.ndarray:  # type: ignore[type-arg]
    """Assign quintile labels 0-4 to an array of values."""
    quantiles = np.quantile(x, [0.2, 0.4, 0.6, 0.8])
    return np.searchsorted(quantiles, x, side="right")


def fit_transition(
    dyads: pd.DataFrame,
    child_income_col: str = "child_income",
    parent_income_col: str = "parent_income",
    cohort_col: str | None = None,
    n_bootstrap: int = 200,
    seed: int = BOOTSTRAP_SEED,
) -> list[TransitionResult]:
    """Estimate quintile-to-quintile transition matrices.

    Args:
        dyads: DataFrame with child and parent income columns.
        child_income_col: Column name for child income.
        parent_income_col: Column name for parent income.
        cohort_col: If provided, estimate separate matrices per cohort.
        n_bootstrap: Number of bootstrap replicates for standard errors.
        seed: Random seed for bootstrap sampling.

    Returns:
        A list of :class:`TransitionResult`.
    """
    results: list[TransitionResult] = []

    def _fit(sub: pd.DataFrame, cohort: int) -> TransitionResult:
        child = sub[child_income_col].to_numpy()
        parent = sub[parent_income_col].to_numpy()
        n = len(child)
        cq = _quintile(child)
        pq = _quintile(parent)
        mat = np.zeros((5, 5))
        for p in range(5):
            mask = pq == p
            if mask.sum() > 0:
                for c in range(5):
                    mat[p, c] = (cq[mask] == c).mean()
        rng = np.random.default_rng(seed)
        boot_mats = np.zeros((n_bootstrap, 5, 5))
        for b in range(n_bootstrap):
            idx = rng.integers(0, n, size=n)
            bc, bp = cq[idx], pq[idx]
            for p in range(5):
                mask = bp == p
                if mask.sum() > 0:
                    for c in range(5):
                        boot_mats[b, p, c] = (bc[mask] == c).mean()
        se = boot_mats.std(axis=0)
        return TransitionResult(matrix=mat, se=se, n=n, cohort=cohort, n_bootstrap=n_bootstrap)

    if cohort_col is not None and cohort_col in dyads.columns:
        for cohort, group in dyads.groupby(cohort_col):
            results.append(_fit(group, int(cohort)))
    else:
        results.append(_fit(dyads, -1))
    return results
