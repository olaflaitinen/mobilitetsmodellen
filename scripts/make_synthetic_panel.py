"""Generate synthetic parent-child panel fixtures for testing and development.

Usage:
    python scripts/make_synthetic_panel.py
    python scripts/make_synthetic_panel.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

import numpy as np
import polars as pl

SYNTHETIC_SEED: int = 19960307
N_DYADS: int = 100_000
N_COHORTS: int = 5
N_KOMMUNER: int = 50
OUTPUT_DIR: pathlib.Path = pathlib.Path("data/synthetic")

EXPECTED_CHECKSUMS: dict[str, str] = {}


def make_parents(rng: np.random.Generator, n: int) -> pl.DataFrame:
    """Generate parent panel records."""
    cohort_years = [1930 + i * 5 for i in range(N_COHORTS)]
    birth_years = rng.choice(cohort_years, size=n).astype(np.int32)
    incomes = np.maximum(rng.lognormal(12.5, 0.6, size=n), 0.0)
    wealth = np.maximum(rng.lognormal(12.0, 1.5, size=n), 0.0)
    edu = rng.integers(1, 8, size=n).astype(np.int32)
    kommuner = rng.integers(100, 100 + N_KOMMUNER, size=n).astype(np.int32)
    return pl.DataFrame(
        {
            "pid": np.arange(1, n + 1, dtype=np.int64),
            "birth_year": birth_years,
            "income": incomes,
            "wealth": wealth,
            "education_level": edu,
            "kommun_code": kommuner,
        }
    )


def make_children(rng: np.random.Generator, parents: pl.DataFrame, n: int) -> pl.DataFrame:
    """Generate child panel records correlated with parents."""
    parent_income = parents["income"].to_numpy()
    log_parent = np.log(np.maximum(parent_income, 1.0))
    noise = rng.normal(0, 0.4, size=n)
    log_child = 0.28 * log_parent + 0.72 * 12.5 + noise
    child_income = np.exp(log_child)
    child_birth = parents["birth_year"].to_numpy() + rng.integers(25, 35, size=n).astype(np.int32)
    edu = rng.integers(1, 8, size=n).astype(np.int32)
    kommuner = parents["kommun_code"].to_numpy()
    return pl.DataFrame(
        {
            "pid": np.arange(n + 1, 2 * n + 1, dtype=np.int64),
            "birth_year": child_birth.astype(np.int32),
            "income": child_income,
            "education_level": edu,
            "kommun_code": kommuner,
        }
    )


def make_dyads(parents: pl.DataFrame, children: pl.DataFrame) -> pl.DataFrame:
    """Build parent-child dyad table with income ranks."""
    parent_rank = _fractional_rank(parents["income"].to_numpy())
    child_rank = _fractional_rank(children["income"].to_numpy())
    return pl.DataFrame(
        {
            "child_pid": children["pid"],
            "parent_pid": parents["pid"],
            "child_birth_year": children["birth_year"],
            "parent_birth_year": parents["birth_year"],
            "child_income": children["income"],
            "parent_income": parents["income"],
            "child_rank": parent_rank,
            "parent_rank": child_rank,
            "child_education": children["education_level"],
            "parent_education": parents["education_level"],
            "parent_wealth": parents["wealth"],
            "kommun_code": parents["kommun_code"],
        }
    )


def _fractional_rank(x: np.ndarray) -> np.ndarray:  # type: ignore[type-arg]
    """Compute fractional ranks in [0, 1]."""
    n = len(x)
    order = np.argsort(x)
    ranks = np.empty(n)
    ranks[order] = np.arange(1, n + 1)
    return (ranks - 1) / max(n - 1, 1)


def sha256_file(path: pathlib.Path) -> str:
    """Return the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def generate(output_dir: pathlib.Path = OUTPUT_DIR) -> dict[str, str]:
    """Generate and save synthetic fixtures.

    Args:
        output_dir: Directory to write Parquet files into.

    Returns:
        Mapping of filename to SHA-256 hex digest.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SYNTHETIC_SEED)
    n = N_DYADS
    parents = make_parents(rng, n)
    children = make_children(rng, parents, n)
    dyads = make_dyads(parents, children)
    checksums: dict[str, str] = {}
    for name, df in [("parents", parents), ("children", children), ("dyads", dyads)]:
        path = output_dir / f"{name}.parquet"
        df.write_parquet(path)
        checksums[name] = sha256_file(path)
        print(f"Wrote {path} ({len(df)} rows, sha256={checksums[name][:16]}...)")
    return checksums


def check(output_dir: pathlib.Path = OUTPUT_DIR) -> bool:
    """Verify that synthetic fixtures exist and are bit-stable.

    Args:
        output_dir: Directory containing the Parquet files.

    Returns:
        True if all files exist and checksums are stable across two regenerations.
    """
    required = ["parents.parquet", "children.parquet", "dyads.parquet"]
    for name in required:
        if not (output_dir / name).exists():
            print(f"MISSING: {output_dir / name}", file=sys.stderr)
            return False
    print("All synthetic fixture files present.")
    print("Re-generating to verify bit-stability...")
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        c1 = generate(output_dir=tmp_path)
        c2 = generate(output_dir=tmp_path)
        for key in c1:
            if c1[key] != c2[key]:
                print(f"CHECKSUM MISMATCH for {key}: {c1[key]} != {c2[key]}", file=sys.stderr)
                return False
    print("Bit-stability verified.")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic mobility panel.")
    parser.add_argument("--check", action="store_true", help="Verify bit-stability only.")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="Output directory.")
    args = parser.parse_args()
    output_dir = pathlib.Path(args.output)
    if args.check:
        ok = check(output_dir)
        sys.exit(0 if ok else 1)
    else:
        generate(output_dir)


if __name__ == "__main__":
    main()
