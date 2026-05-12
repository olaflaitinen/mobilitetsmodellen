"""Pairs and cluster bootstrap for mobility estimators."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

from mobilitetsmodellen.seeds import BOOTSTRAP_SEED


def bootstrap_ci(
    data: pd.DataFrame,
    statistic: Callable[[pd.DataFrame], float],
    n_bootstrap: int = 1000,
    level: float = 0.95,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float, float]:
    """Compute a bootstrap confidence interval for a scalar statistic.

    Uses the percentile method.

    Args:
        data: Input DataFrame.
        statistic: Function mapping a DataFrame to a scalar estimate.
        n_bootstrap: Number of bootstrap replicates.
        level: Nominal coverage level.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (point_estimate, lower_bound, upper_bound).
    """
    rng = np.random.default_rng(seed)
    n = len(data)
    point = statistic(data)
    boot_stats = np.empty(n_bootstrap)
    for b in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        boot_stats[b] = statistic(data.iloc[idx])
    alpha = (1.0 - level) / 2.0
    lower = float(np.quantile(boot_stats, alpha))
    upper = float(np.quantile(boot_stats, 1.0 - alpha))
    return point, lower, upper


def cluster_bootstrap_ci(
    data: pd.DataFrame,
    statistic: Callable[[pd.DataFrame], float],
    cluster_col: str,
    n_bootstrap: int = 1000,
    level: float = 0.95,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float, float]:
    """Compute a cluster bootstrap confidence interval.

    Resamples whole clusters (e.g. municipalities) with replacement.

    Args:
        data: Input DataFrame.
        statistic: Function mapping a DataFrame to a scalar estimate.
        cluster_col: Column name identifying clusters.
        n_bootstrap: Number of bootstrap replicates.
        level: Nominal coverage level.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (point_estimate, lower_bound, upper_bound).
    """
    rng = np.random.default_rng(seed)
    clusters = data[cluster_col].unique()
    n_clusters = len(clusters)
    point = statistic(data)
    boot_stats = np.empty(n_bootstrap)
    for b in range(n_bootstrap):
        sampled_clusters = rng.choice(clusters, size=n_clusters, replace=True)
        parts = [data[data[cluster_col] == c] for c in sampled_clusters]
        boot_data = pd.concat(parts, ignore_index=True)
        boot_stats[b] = statistic(boot_data)
    alpha = (1.0 - level) / 2.0
    lower = float(np.quantile(boot_stats, alpha))
    upper = float(np.quantile(boot_stats, 1.0 - alpha))
    return point, lower, upper
