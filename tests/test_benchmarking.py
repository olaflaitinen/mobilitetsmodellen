"""Tests for cross-country benchmarking modules."""

from __future__ import annotations

import pandas as pd

from mobilitetsmodellen.benchmarking.cross_country import CrossCountryBenchmark
from mobilitetsmodellen.benchmarking.oecd import OECDHarmonisedResult, harmonise_to_oecd


def test_harmonise_to_oecd_returns_result() -> None:
    result = harmonise_to_oecd(rank_rank_slope=0.25, ige=0.27)
    assert isinstance(result, OECDHarmonisedResult)


def test_harmonise_to_oecd_country_code() -> None:
    result = harmonise_to_oecd(0.25, 0.27)
    assert result.country_code == "SWE"


def test_harmonise_to_oecd_with_transition_matrix() -> None:
    tm = pd.DataFrame([[0.1, 0.2, 0.3, 0.2, 0.2]] * 5)
    result = harmonise_to_oecd(0.25, 0.27, transition_matrix=tm)
    assert result.absolute_upward_mobility > 0


def test_cross_country_benchmark_build() -> None:
    bench = CrossCountryBenchmark(sweden_slope=0.25, sweden_ige=0.27)
    df = bench.build().comparisons
    assert "SWE" in df["country"].values
    assert len(df) > 1


def test_cross_country_benchmark_summary() -> None:
    bench = CrossCountryBenchmark(sweden_slope=0.25, sweden_ige=0.27)
    df = bench.summary()
    assert isinstance(df, pd.DataFrame)
    assert "rank_rank_slope" in df.columns


def test_cross_country_benchmark_sorted() -> None:
    bench = CrossCountryBenchmark(sweden_slope=0.25, sweden_ige=0.27)
    df = bench.summary()
    slopes = df["rank_rank_slope"].tolist()
    assert slopes == sorted(slopes)
