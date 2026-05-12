"""Determinism tests: DoubleML and causal forest across two runs with same seed."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from mobilitetsmodellen.estimators.double_ml import fit_double_ml
from mobilitetsmodellen.seeds import derive_seed, set_global_seed


def _dyads(n: int = 200, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    parent = rng.uniform(0, 1, n)
    child = 0.3 * parent + 0.5 + rng.normal(0, 0.05, n)
    child = np.clip(child, 0, 1)
    return pd.DataFrame(
        {
            "pid": np.arange(n),
            "parent_rank": parent,
            "child_rank": child,
        }
    )


def test_double_ml_theta_deterministic() -> None:
    df = _dyads()
    r1 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    r2 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    assert abs(r1.theta - r2.theta) < 1e-6, "DoubleML theta must be deterministic given same seed"


def test_double_ml_se_deterministic() -> None:
    df = _dyads()
    r1 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    r2 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    assert abs(r1.se - r2.se) < 1e-6


def test_double_ml_different_seeds_differ() -> None:
    df = _dyads()
    r1 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=13)
    r2 = fit_double_ml(df, n_folds=2, learner="random-forest", seed=99)
    assert abs(r1.theta - r2.theta) > 0 or abs(r1.se - r2.se) > 0


def test_derive_seed_deterministic() -> None:
    s1 = derive_seed("fold_assignment", 42)
    s2 = derive_seed("fold_assignment", 42)
    assert s1 == s2


def test_derive_seed_different_namespace() -> None:
    s1 = derive_seed("fold_assignment", 42)
    s2 = derive_seed("nuisance_init", 42)
    assert s1 != s2


def test_derive_seed_unknown_namespace() -> None:
    with pytest.raises(ValueError, match="Unknown namespace"):
        derive_seed("invalid_namespace", 42)


def test_set_global_seed_reproducible() -> None:
    set_global_seed(42)
    x1 = np.random.uniform(0, 1, 5)
    set_global_seed(42)
    x2 = np.random.uniform(0, 1, 5)
    np.testing.assert_array_equal(x1, x2)
