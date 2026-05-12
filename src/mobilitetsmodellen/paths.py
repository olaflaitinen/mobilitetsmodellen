"""Canonical filesystem paths used across the pipeline."""

from __future__ import annotations

import pathlib

DATA_ROOT: pathlib.Path = pathlib.Path("data")
SYNTHETIC_ROOT: pathlib.Path = DATA_ROOT / "synthetic"
CROSSWALK_ROOT: pathlib.Path = DATA_ROOT / "crosswalks"
REPORTS_ROOT: pathlib.Path = pathlib.Path("reports")
