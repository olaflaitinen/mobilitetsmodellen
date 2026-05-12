"""Bump the project version in pyproject.toml and _version.py.

Usage:
    python scripts/bump_version.py patch
    python scripts/bump_version.py minor
    python scripts/bump_version.py major
    python scripts/bump_version.py --set 1.0.0
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

PYPROJECT = pathlib.Path("pyproject.toml")
VERSION_FILE = pathlib.Path("src/mobilitetsmodellen/_version.py")


def current_version() -> str:
    """Read the current version from _version.py.

    Returns:
        Version string (e.g. ``"0.1.0"``).
    """
    text = VERSION_FILE.read_text(encoding="utf-8")
    m = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if not m:
        raise ValueError(f"Cannot parse version from {VERSION_FILE}")
    return m.group(1)


def bump(version: str, part: str) -> str:
    """Compute the next version by incrementing a part.

    Args:
        version: Current version string.
        part: One of ``"major"``, ``"minor"``, ``"patch"``.

    Returns:
        New version string.
    """
    major, minor, patch = (int(x) for x in version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def update_files(new_version: str) -> None:
    """Update version string in all relevant files.

    Args:
        new_version: New version string.
    """
    vf = VERSION_FILE.read_text(encoding="utf-8")
    vf = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{new_version}"', vf)
    VERSION_FILE.write_text(vf, encoding="utf-8")
    pt = PYPROJECT.read_text(encoding="utf-8")
    pt = re.sub(r'^version\s*=\s*"[^"]+"', f'version = "{new_version}"', pt, flags=re.MULTILINE)
    PYPROJECT.write_text(pt, encoding="utf-8")
    print(f"Bumped version to {new_version}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump project version.")
    parser.add_argument("part", nargs="?", choices=["major", "minor", "patch"])
    parser.add_argument("--set", dest="set_version", help="Set version explicitly.")
    args = parser.parse_args()
    old = current_version()
    if args.set_version:
        new = args.set_version
    elif args.part:
        new = bump(old, args.part)
    else:
        print(f"Current version: {old}")
        sys.exit(0)
    update_files(new)


if __name__ == "__main__":
    main()
