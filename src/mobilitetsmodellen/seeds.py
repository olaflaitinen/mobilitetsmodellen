"""Seed management for reproducible random number generation.

All randomness in the pipeline must be derived from seeds via :func:`derive_seed`.
Direct calls to ``random.seed`` or ``numpy.random.seed`` outside this module are
prohibited; use :func:`set_global_seed` instead.
"""

from __future__ import annotations

import hashlib
import random

import numpy as np

SYNTHETIC_SEED: int = 19960307
MODEL_SEED: int = 20251008
CROSSFIT_SEED: int = 13
FOREST_SEED: int = 123
BOOTSTRAP_SEED: int = 7
ATLAS_SEED: int = 31

_NAMESPACES: frozenset[str] = frozenset(
    [
        "fold_assignment",
        "nuisance_init",
        "forest_init",
        "bootstrap_sample",
        "atlas_jitter",
    ]
)


def set_global_seed(seed: int) -> None:
    """Set the global random state for :mod:`random` and :mod:`numpy`.

    Args:
        seed: Integer seed value.
    """
    random.seed(seed)
    np.random.seed(seed)  # noqa: NPY002


def derive_seed(namespace: str, base: int) -> int:
    """Derive a deterministic child seed from a namespace string and a base seed.

    Uses SHA-256 to produce a platform-independent 32-bit integer.

    Args:
        namespace: One of the canonical namespaces defined in ``_NAMESPACES``.
        base: Parent seed value.

    Returns:
        A 32-bit unsigned integer derived deterministically from inputs.

    Raises:
        ValueError: If ``namespace`` is not in the canonical set.
    """
    if namespace not in _NAMESPACES:
        raise ValueError(
            f"Unknown namespace '{namespace}'. Valid namespaces: {sorted(_NAMESPACES)}"
        )
    digest = hashlib.sha256(f"{namespace}:{base}".encode()).digest()
    return int.from_bytes(digest[:4], byteorder="big")
