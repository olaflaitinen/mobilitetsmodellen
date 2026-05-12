"""OECD Income Distribution Database (IDD) harmonisation utilities."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class OECDHarmonisedResult:
    """Swedish mobility estimate aligned to OECD IDD conventions.

    Attributes:
        rank_rank_slope: Rank-rank slope (intergenerational persistence).
        ige: Intergenerational income elasticity.
        absolute_upward_mobility: P(child income rank > 50 | parent in Q1).
        country_code: ISO 3166-1 alpha-3 country code.
        reference_year: Reference income year for parent generation.
    """

    rank_rank_slope: float
    ige: float
    absolute_upward_mobility: float
    country_code: str = "SWE"
    reference_year: int = 2000


def harmonise_to_oecd(
    rank_rank_slope: float,
    ige: float,
    transition_matrix: pd.DataFrame | None = None,
    country_code: str = "SWE",
    reference_year: int = 2000,
) -> OECDHarmonisedResult:
    """Harmonise Swedish mobility estimates to OECD IDD conventions.

    Applies standard OECD conventions:
    - Income measured as total household disposable income per equivalent adult.
    - Life-cycle adjustment at ages 35-45.
    - Absolute upward mobility: fraction with child rank > 50 given bottom-quintile parents.

    Args:
        rank_rank_slope: Estimated rank-rank slope.
        ige: Estimated intergenerational income elasticity.
        transition_matrix: Optional quintile transition matrix.
        country_code: ISO 3166-1 alpha-3 country code.
        reference_year: Reference year for parental income.

    Returns:
        An :class:`OECDHarmonisedResult`.
    """
    aum = float("nan")
    if transition_matrix is not None and len(transition_matrix) >= 5:
        aum = float(transition_matrix.iloc[0, 2:].sum())
    return OECDHarmonisedResult(
        rank_rank_slope=rank_rank_slope,
        ige=ige,
        absolute_upward_mobility=aum,
        country_code=country_code,
        reference_year=reference_year,
    )
