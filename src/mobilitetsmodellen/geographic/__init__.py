"""Geographic aggregation, empirical-Bayes shrinkage, and spatial analysis."""

from __future__ import annotations

from mobilitetsmodellen.geographic.aggregation import aggregate_by_region
from mobilitetsmodellen.geographic.empirical_bayes import james_stein_shrink
from mobilitetsmodellen.geographic.spatial import morans_i

__all__ = ["aggregate_by_region", "james_stein_shrink", "morans_i"]
