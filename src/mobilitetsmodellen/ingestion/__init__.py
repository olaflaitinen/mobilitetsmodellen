"""Data ingestion utilities for register and crosswalk data."""

from __future__ import annotations

from mobilitetsmodellen.ingestion.crosswalks import load_crosswalk
from mobilitetsmodellen.ingestion.flergen import read_flergen, synthetic_flergen
from mobilitetsmodellen.ingestion.lisa import read_lisa, synthetic_lisa
from mobilitetsmodellen.ingestion.manifest import Manifest
from mobilitetsmodellen.ingestion.tax_registers import read_tax_register, synthetic_tax_register

__all__ = [
    "load_crosswalk",
    "read_flergen",
    "synthetic_flergen",
    "read_lisa",
    "synthetic_lisa",
    "read_tax_register",
    "synthetic_tax_register",
    "Manifest",
]
