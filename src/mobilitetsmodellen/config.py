"""Pydantic v2 configuration model for the mobility pipeline."""

from __future__ import annotations

import pathlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Config(BaseModel):
    """Pipeline configuration.

    Attributes:
        data_root: Root directory for all data inputs and outputs.
        seed: Master random seed (MODEL_SEED = 20251008 by default).
        alignment_window: Income averaging window for life-cycle alignment.
        estimator: Primary mobility estimator to run.
        nuisance_learner: Learner for nuisance functions in double ML.
        n_folds: Number of cross-fitting folds.
        shrinkage: Empirical-Bayes shrinkage strategy for municipality estimates.
        n_jobs: Number of parallel jobs (-1 uses all available cores).
    """

    model_config = ConfigDict(frozen=True)

    data_root: pathlib.Path = pathlib.Path("data")
    seed: int = 20251008
    alignment_window: Literal["single", "three", "five"] = "three"
    estimator: Literal["rank-rank", "elasticity", "transition", "double-ml", "causal-forest"] = (
        "double-ml"
    )
    nuisance_learner: Literal["xgboost", "lightgbm", "random-forest"] = "lightgbm"
    n_folds: int = Field(default=5, ge=2, le=20)
    shrinkage: Literal["none", "james-stein", "spatial"] = "james-stein"
    n_jobs: int = Field(default=1, ge=-1)
