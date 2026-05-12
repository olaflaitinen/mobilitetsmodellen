"""REUSE compliance and formatting checks: zero U+2013, U+2014, emoji."""

from __future__ import annotations

import pathlib
import re

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
TEXT_EXTENSIONS = {".py", ".md", ".toml", ".yaml", ".yml", ".cfg", ".ini", ".txt", ".cff", ".rst"}
EXCLUDE_DIRS = {".git", ".venv", "venv", ".nox", "site", "htmlcov", "__pycache__", "LICENSES"}

_EMOJI_RE = re.compile(
    "[\U00002702-\U000027b0"
    "\U000024c2-\U0001f251"
    "\U0001f300-\U0001f9ff"
    "\U0001fa00-\U0001fa6f"
    "\U0001fa70-\U0001faff"
    "\U00002600-\U000026ff]",
    flags=re.UNICODE,
)


def _collect_text_files() -> list[pathlib.Path]:
    files = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            files.append(path)
    return files


@pytest.mark.parametrize("path", _collect_text_files())
def test_no_em_dash(path: pathlib.Path) -> None:
    """No U+2014 em-dash in any text file."""
    content = path.read_text(encoding="utf-8", errors="replace")
    assert "\u2014" not in content, f"Em-dash found in {path}"


@pytest.mark.parametrize("path", _collect_text_files())
def test_no_en_dash(path: pathlib.Path) -> None:
    """No U+2013 en-dash in any text file."""
    content = path.read_text(encoding="utf-8", errors="replace")
    assert "\u2013" not in content, f"En-dash found in {path}"


@pytest.mark.parametrize("path", _collect_text_files())
def test_no_emoji(path: pathlib.Path) -> None:
    """No emoji characters in any text file."""
    content = path.read_text(encoding="utf-8", errors="replace")
    found = _EMOJI_RE.findall(content)
    assert not found, f"Emoji found in {path}: {found[:5]}"


def test_no_spdx_headers() -> None:
    """No SPDX header comment in production source files (src/ only)."""
    src_root = REPO_ROOT / "src"
    marker = "-".join(["SPDX", "License", "Identifier"])
    for path in src_root.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        assert marker not in content, f"SPDX header found in {path}"
