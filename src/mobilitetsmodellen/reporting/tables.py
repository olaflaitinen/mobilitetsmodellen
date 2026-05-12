"""Table export utilities: CSV, Parquet, and LaTeX."""

from __future__ import annotations

import pathlib

import pandas as pd
import polars as pl


def to_csv(
    df: pd.DataFrame,
    path: pathlib.Path,
    with_bom: bool = False,
) -> pathlib.Path:
    """Write a DataFrame to CSV, optionally with UTF-8 BOM for Excel compatibility.

    Args:
        df: DataFrame to export.
        path: Destination path.
        with_bom: If ``True``, prepend a UTF-8 BOM byte sequence.

    Returns:
        The resolved output path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if with_bom else "utf-8"
    df.to_csv(path, index=False, encoding=encoding)
    return path


def to_parquet(
    df: pd.DataFrame | pl.DataFrame,
    path: pathlib.Path,
) -> pathlib.Path:
    """Write a DataFrame to Parquet.

    Args:
        df: Pandas or Polars DataFrame to export.
        path: Destination path.

    Returns:
        The resolved output path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(df, pl.DataFrame):
        df.write_parquet(path)
    else:
        df.to_parquet(path, index=False)
    return path


def to_latex_table(
    df: pd.DataFrame,
    path: pathlib.Path,
    caption: str = "",
    label: str = "",
    float_format: str = "{:.3f}",
) -> pathlib.Path:
    """Export a DataFrame to a LaTeX table file.

    Args:
        df: DataFrame to format as LaTeX.
        path: Destination ``.tex`` file path.
        caption: Table caption.
        label: LaTeX label for cross-references.
        float_format: Format string for floating-point values.

    Returns:
        The resolved output path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    latex = df.to_latex(
        index=False,
        float_format=float_format.format,
        caption=caption or None,
        label=label or None,
        escape=True,
    )
    path.write_text(latex, encoding="utf-8")
    return path
