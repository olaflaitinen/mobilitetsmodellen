"""Loaders for SCB geographic crosswalk tables."""

from __future__ import annotations

import pathlib
from typing import Literal

import polars as pl

from mobilitetsmodellen.paths import CROSSWALK_ROOT

CrosswalkType = Literal["kommun", "lan", "fa_region"]

_CROSSWALK_FILES: dict[CrosswalkType, str] = {
    "kommun": "kommun.csv",
    "lan": "lan.csv",
    "fa_region": "fa_region.csv",
}


def load_crosswalk(
    kind: CrosswalkType,
    root: pathlib.Path = CROSSWALK_ROOT,
) -> pl.DataFrame:
    """Load a geographic crosswalk table from CSV.

    Args:
        kind: Type of crosswalk to load (``"kommun"``, ``"lan"``, or ``"fa_region"``).
        root: Directory containing the crosswalk CSV files.

    Returns:
        A deduplicated Polars DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    csv_path = root / _CROSSWALK_FILES[kind]
    if not csv_path.exists():
        raise FileNotFoundError(f"Crosswalk file not found: {csv_path}")
    df = pl.read_csv(csv_path, infer_schema_length=10_000)
    return df.unique()


def validate_kommun_codes(df: pl.DataFrame, code_column: str = "kommun_code") -> bool:
    """Check that all codes in ``code_column`` fall within valid SCB Kommunkoder range.

    SCB Kommunkoder are 4-digit integers in the range 0114-2584.

    Args:
        df: DataFrame containing municipality codes.
        code_column: Name of the column holding municipality codes.

    Returns:
        ``True`` if all codes are in range; ``False`` otherwise.
    """
    codes = df[code_column].cast(pl.Int32)
    return bool((codes >= 114).all() and (codes <= 2584).all())
