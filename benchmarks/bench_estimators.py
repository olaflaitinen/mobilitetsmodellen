"""Pytest-benchmark suite for estimator performance.

Run with:
    uv run pytest benchmarks/ --benchmark-only
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _dyads(n: int = 5_000, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = rng.uniform(0, 1, n)
    child = 0.3 * parent + 0.5 + rng.normal(0, 0.05, n)
    child = np.clip(child, 0, 1)
    parent_income = np.exp(rng.normal(12.5, 0.6, n))
    child_income = np.exp(rng.normal(12.5, 0.6, n))
    return pd.DataFrame(
        {
            "pid": np.arange(n),
            "parent_rank": parent,
            "child_rank": child,
            "parent_income": parent_income,
            "child_income": child_income,
            "birth_year": rng.choice([1960, 1965, 1970], size=n),
        }
    )


def test_rank_rank_5k(benchmark: object) -> None:
    from mobilitetsmodellen.estimators.rank_rank import fit_rank_rank

    df = _dyads(5_000)
    benchmark(fit_rank_rank, df)  # type: ignore[call-arg]


def test_elasticity_5k(benchmark: object) -> None:
    from mobilitetsmodellen.estimators.elasticity import fit_elasticity

    df = _dyads(5_000)
    benchmark(fit_elasticity, df)  # type: ignore[call-arg]


def test_transition_1k(benchmark: object) -> None:
    from mobilitetsmodellen.estimators.transition_matrix import fit_transition

    df = _dyads(1_000)
    benchmark(fit_transition, df, n_bootstrap=50)  # type: ignore[call-arg]


def test_james_stein_100(benchmark: object) -> None:
    from mobilitetsmodellen.geographic.empirical_bayes import james_stein_shrink

    rng = np.random.default_rng(1)
    est = rng.uniform(0.1, 0.5, 100)
    ses = rng.uniform(0.02, 0.1, 100)
    benchmark(james_stein_shrink, est, ses)  # type: ignore[call-arg]
