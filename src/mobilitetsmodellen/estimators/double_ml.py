"""Double machine learning estimator for intergenerational mobility."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from mobilitetsmodellen.seeds import CROSSFIT_SEED, derive_seed


@dataclass(frozen=True)
class DoubleMLResult:
    """Result container for the DoubleML estimator.

    Attributes:
        theta: Point estimate of the mobility parameter.
        se: Standard error from orthogonal score.
        n: Number of observations.
        n_folds: Number of cross-fitting folds used.
        learner: Nuisance learner identifier string.
    """

    theta: float
    se: float
    n: int
    n_folds: int
    learner: str


def _sha256_fold(pid: int, n_folds: int, seed: int) -> int:
    """Assign a fold deterministically via SHA-256 of pid and seed.

    This guarantees identical fold assignment across platforms regardless of
    OS random-state initialisation.

    Args:
        pid: Stable individual identifier.
        n_folds: Total number of folds.
        seed: Base seed for fold assignment namespace.

    Returns:
        An integer in [0, n_folds).
    """
    key = f"fold_assignment:{seed}:{pid}".encode()
    h = int.from_bytes(hashlib.sha256(key).digest()[:4], "big")
    return h % n_folds


def _make_fold_assignments(
    pids: np.ndarray,  # type: ignore[type-arg]
    n_folds: int,
    seed: int,
) -> np.ndarray:  # type: ignore[type-arg]
    """Build a fold-assignment array using SHA-256 per individual.

    Args:
        pids: Array of stable individual identifiers.
        n_folds: Number of cross-fitting folds.
        seed: Base seed.

    Returns:
        Integer array of fold indices in [0, n_folds).
    """
    return np.array([_sha256_fold(int(p), n_folds, seed) for p in pids])


def _build_learner(learner: str, seed: int) -> Any:
    """Instantiate a nuisance learner by name.

    Args:
        learner: One of ``"lightgbm"``, ``"xgboost"``, or ``"random-forest"``.
        seed: Random seed for the learner.

    Returns:
        A fitted sklearn-compatible estimator.

    Raises:
        ValueError: If ``learner`` is not recognised.
    """
    if learner == "lightgbm":
        from lightgbm import LGBMRegressor

        return LGBMRegressor(
            n_estimators=50,
            num_leaves=15,
            random_state=seed,
            n_jobs=1,
            verbose=-1,
        )
    if learner == "xgboost":
        from xgboost import XGBRegressor

        return XGBRegressor(
            n_estimators=50,
            max_depth=4,
            random_state=seed,
            n_jobs=1,
            verbosity=0,
        )
    if learner == "random-forest":
        from sklearn.ensemble import RandomForestRegressor

        return RandomForestRegressor(
            n_estimators=50,
            max_depth=6,
            random_state=seed,
            n_jobs=1,
        )
    raise ValueError(f"Unknown learner '{learner}'. Choose lightgbm, xgboost, or random-forest.")


def fit_double_ml(
    dyads: pd.DataFrame,
    child_rank_col: str = "child_rank",
    parent_rank_col: str = "parent_rank",
    controls: list[str] | None = None,
    n_folds: int = 5,
    learner: str = "lightgbm",
    seed: int = CROSSFIT_SEED,
) -> DoubleMLResult:
    """Estimate intergenerational rank persistence via double ML.

    Implements the partially linear regression (PLR) via cross-fitting.
    Fold assignment is deterministic via SHA-256 hashing of individual identifiers.

    Args:
        dyads: DataFrame with child rank, parent rank, and optional controls.
        child_rank_col: Name of the child income rank column.
        parent_rank_col: Name of the parent income rank column.
        controls: List of covariate column names for nuisance regression.
        n_folds: Number of cross-fitting folds.
        learner: Nuisance learner (``"lightgbm"``, ``"xgboost"``, ``"random-forest"``).
        seed: Base seed for fold assignment and nuisance initialisation.

    Returns:
        A :class:`DoubleMLResult` with the mobility estimate.
    """
    if controls is None:
        controls = []
    y = dyads[child_rank_col].to_numpy()
    d = dyads[parent_rank_col].to_numpy()
    n = len(y)
    if "pid" in dyads.columns:
        pids = dyads["pid"].to_numpy()
    else:
        pids = np.arange(n)
    folds = _make_fold_assignments(pids, n_folds, seed)
    x = dyads[controls].to_numpy() if controls else np.zeros((n, 1))
    d_hat = np.zeros(n)
    y_hat = np.zeros(n)
    nuisance_seed = derive_seed("nuisance_init", seed)
    for fold_idx in range(n_folds):
        train = folds != fold_idx
        test = folds == fold_idx
        if train.sum() < 4 or test.sum() < 1:
            continue
        lm_d = _build_learner(learner, derive_seed("nuisance_init", nuisance_seed + fold_idx))
        lm_y = _build_learner(learner, derive_seed("nuisance_init", nuisance_seed + fold_idx + 1))
        lm_d.fit(x[train], d[train])
        lm_y.fit(x[train], y[train])
        d_hat[test] = lm_d.predict(x[test])
        y_hat[test] = lm_y.predict(x[test])
    d_res = d - d_hat
    y_res = y - y_hat
    denom = float(d_res @ d_res)
    if abs(denom) < 1e-12:
        return DoubleMLResult(
            theta=float("nan"), se=float("nan"), n=n, n_folds=n_folds, learner=learner
        )
    theta = float(d_res @ y_res) / denom
    psi = d_res * (y_res - theta * d_res)
    variance = float(np.mean(psi**2)) / max(float(np.mean(d_res**2)) ** 2, 1e-24)
    se = float(np.sqrt(max(variance / n, 0.0)))
    return DoubleMLResult(theta=theta, se=se, n=n, n_folds=n_folds, learner=learner)
