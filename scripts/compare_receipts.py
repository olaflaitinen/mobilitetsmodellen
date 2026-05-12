"""Compare replication receipts against expected checksums.

Usage:
    python scripts/compare_receipts.py
    python scripts/compare_receipts.py --expected replication/expected_receipts.json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

RECEIPTS_FILE = pathlib.Path("replication/expected_receipts.json")
ACTUAL_DIR = pathlib.Path("replication/actual_receipts")


def load_receipts(path: pathlib.Path) -> dict[str, str]:
    """Load receipts from a JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        Dictionary mapping receipt name to hex checksum.
    """
    if not path.exists():
        return {}
    return dict(json.loads(path.read_text(encoding="utf-8")))  # type: ignore[return-value]


def compare(
    expected: dict[str, str],
    actual: dict[str, str],
) -> list[str]:
    """Compare expected and actual checksums.

    Args:
        expected: Expected checksums.
        actual: Actual checksums.

    Returns:
        List of mismatch messages (empty if all match).
    """
    mismatches = []
    for key, exp_val in expected.items():
        if key not in actual:
            mismatches.append(f"MISSING actual receipt: {key}")
        elif actual[key] != exp_val:
            mismatches.append(
                f"MISMATCH {key}: expected {exp_val[:16]}... got {actual[key][:16]}..."
            )
    for key in actual:
        if key not in expected:
            mismatches.append(f"UNEXPECTED actual receipt: {key}")
    return mismatches


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare replication receipts.")
    parser.add_argument(
        "--expected",
        default=str(RECEIPTS_FILE),
        help="Path to expected_receipts.json",
    )
    args = parser.parse_args()
    expected = load_receipts(pathlib.Path(args.expected))
    actual = load_receipts(ACTUAL_DIR / "receipts.json")
    if not expected:
        print("No expected receipts found. Skipping comparison.")
        sys.exit(0)
    mismatches = compare(expected, actual)
    if mismatches:
        for m in mismatches:
            print(f"FAIL: {m}", file=sys.stderr)
        sys.exit(1)
    print(f"All {len(expected)} receipts match.")


if __name__ == "__main__":
    main()
