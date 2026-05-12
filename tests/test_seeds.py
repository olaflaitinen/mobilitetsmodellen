"""Additional seeds module tests (for coverage of config + paths)."""

from __future__ import annotations

import pathlib

from mobilitetsmodellen.config import Config
from mobilitetsmodellen.paths import CROSSWALK_ROOT, DATA_ROOT, REPORTS_ROOT, SYNTHETIC_ROOT


def test_config_defaults() -> None:
    cfg = Config()
    assert cfg.seed == 20251008
    assert cfg.n_folds == 5
    assert cfg.estimator == "double-ml"
    assert cfg.shrinkage == "james-stein"


def test_config_custom() -> None:
    cfg = Config(estimator="rank-rank", n_folds=3, seed=1)
    assert cfg.estimator == "rank-rank"
    assert cfg.n_folds == 3


def test_config_frozen() -> None:
    import pytest

    cfg = Config()
    with pytest.raises(Exception):
        cfg.seed = 999  # type: ignore[misc]


def test_paths_are_path_objects() -> None:
    assert isinstance(DATA_ROOT, pathlib.Path)
    assert isinstance(SYNTHETIC_ROOT, pathlib.Path)
    assert isinstance(CROSSWALK_ROOT, pathlib.Path)
    assert isinstance(REPORTS_ROOT, pathlib.Path)


def test_synthetic_root_under_data() -> None:
    assert SYNTHETIC_ROOT.parts[-1] == "synthetic"
    assert DATA_ROOT in SYNTHETIC_ROOT.parents
