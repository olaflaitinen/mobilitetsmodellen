"""Mobilitetsmodellen: machine-learning estimators of intergenerational mobility in Sweden."""

from __future__ import annotations

from mobilitetsmodellen._version import __version__
from mobilitetsmodellen.config import Config
from mobilitetsmodellen.seeds import set_global_seed

__author__ = "Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov"
__license__ = "EUPL-1.2"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Config",
    "set_global_seed",
]
