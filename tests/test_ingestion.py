"""Tests for data ingestion modules."""

from __future__ import annotations

import pathlib

import pytest

from mobilitetsmodellen.ingestion.flergen import synthetic_flergen
from mobilitetsmodellen.ingestion.lisa import synthetic_lisa
from mobilitetsmodellen.ingestion.manifest import Manifest
from mobilitetsmodellen.ingestion.tax_registers import synthetic_tax_register


def test_synthetic_flergen_shape() -> None:
    df = synthetic_flergen(n=100, seed=1)
    assert len(df) == 100
    assert "pid" in df.columns
    assert "parent_pid" in df.columns
    assert "birth_year" in df.columns
    assert "kommun_code" in df.columns


def test_synthetic_flergen_deterministic() -> None:
    df1 = synthetic_flergen(n=50, seed=99)
    df2 = synthetic_flergen(n=50, seed=99)
    assert df1.equals(df2)


def test_synthetic_flergen_different_seeds() -> None:
    df1 = synthetic_flergen(n=50, seed=1)
    df2 = synthetic_flergen(n=50, seed=2)
    assert df1["pid"].to_list() != df2["birth_year"].to_list()


def test_synthetic_lisa_shape() -> None:
    import numpy as np

    pids = np.arange(1, 11)
    df = synthetic_lisa(pids, seed=1)
    assert "pid" in df.columns
    assert "income" in df.columns
    assert (df["income"] >= 0).all()


def test_synthetic_lisa_non_negative_income() -> None:
    import numpy as np

    pids = np.arange(1, 51)
    df = synthetic_lisa(pids, seed=7)
    assert (df["income"] >= 0).all()


def test_synthetic_tax_register_shape() -> None:
    import numpy as np

    pids = np.arange(1, 6)
    df = synthetic_tax_register(pids, seed=1)
    assert "pid" in df.columns
    assert "taxable_income" in df.columns
    assert "wealth" in df.columns
    assert len(df) == 5 * 21


def test_manifest_from_path(tmp_path: pathlib.Path) -> None:
    f = tmp_path / "test.txt"
    f.write_bytes(b"hello world")
    m = Manifest.from_path(f, n_rows=1, source="test")
    assert len(m.sha256) == 64
    assert m.n_rows == 1
    assert m.source == "test"


def test_manifest_immutable() -> None:
    import pathlib

    m = Manifest(path=pathlib.Path("x"), sha256="abc", n_rows=0)
    with pytest.raises(Exception):
        m.sha256 = "changed"  # type: ignore[misc]


def test_crosswalk_load_missing(tmp_path: pathlib.Path) -> None:
    from mobilitetsmodellen.ingestion.crosswalks import load_crosswalk

    with pytest.raises(FileNotFoundError):
        load_crosswalk("kommun", root=tmp_path)
