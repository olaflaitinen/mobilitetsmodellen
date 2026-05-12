"""Cross-country mobility benchmarking harness."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

BENCHMARK_ESTIMATES: dict[str, dict[str, float]] = {
    "USA": {"rank_rank_slope": 0.45, "ige": 0.47},
    "GBR": {"rank_rank_slope": 0.30, "ige": 0.30},
    "NOR": {"rank_rank_slope": 0.17, "ige": 0.17},
    "DNK": {"rank_rank_slope": 0.15, "ige": 0.15},
    "FIN": {"rank_rank_slope": 0.18, "ige": 0.18},
}


@dataclass
class CrossCountryBenchmark:
    """Container for a cross-country mobility comparison.

    Attributes:
        sweden_slope: Swedish rank-rank slope estimate.
        sweden_ige: Swedish IGE estimate.
        comparisons: DataFrame with benchmark estimates from other countries.
    """

    sweden_slope: float
    sweden_ige: float
    comparisons: pd.DataFrame = field(default_factory=pd.DataFrame)

    def build(self) -> CrossCountryBenchmark:
        """Populate comparison table from built-in benchmark estimates.

        Returns:
            Self, with ``comparisons`` populated.
        """
        records = []
        for country, vals in BENCHMARK_ESTIMATES.items():
            records.append(
                {
                    "country": country,
                    "rank_rank_slope": vals["rank_rank_slope"],
                    "ige": vals["ige"],
                    "source": "literature",
                }
            )
        records.append(
            {
                "country": "SWE",
                "rank_rank_slope": self.sweden_slope,
                "ige": self.sweden_ige,
                "source": "mobilitetsmodellen",
            }
        )
        self.comparisons = (
            pd.DataFrame(records).sort_values("rank_rank_slope").reset_index(drop=True)
        )
        return self

    def summary(self) -> pd.DataFrame:
        """Return the comparison table, building it if necessary.

        Returns:
            DataFrame sorted by rank-rank slope ascending.
        """
        if self.comparisons.empty:
            self.build()
        return self.comparisons
