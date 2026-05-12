"""Generate a structured CHANGELOG entry from conventional commits.

Usage:
    python scripts/generate_changelog.py --since v0.1.0 --version v0.2.0
"""

from __future__ import annotations

import argparse
import datetime
import subprocess
import sys

COMMIT_TYPES = {
    "feat": "Added",
    "fix": "Fixed",
    "docs": "Documentation",
    "test": "Tests",
    "chore": "Chores",
    "refactor": "Refactored",
    "perf": "Performance",
    "ci": "CI/CD",
}


def get_commits(since: str) -> list[str]:
    """Return commit messages since a given tag or commit.

    Args:
        since: Git ref (tag or commit SHA) to start from.

    Returns:
        List of commit subject lines.
    """
    cmd = ["git", "log", f"{since}..HEAD", "--format=%s"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)  # noqa: S603
    if result.returncode != 0:
        print(f"git log failed: {result.stderr}", file=sys.stderr)
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def classify_commits(commits: list[str]) -> dict[str, list[str]]:
    """Group commits by Conventional Commit type.

    Args:
        commits: List of commit subject lines.

    Returns:
        Dictionary mapping section name to list of messages.
    """
    sections: dict[str, list[str]] = {v: [] for v in COMMIT_TYPES.values()}
    sections["Other"] = []
    for msg in commits:
        matched = False
        for prefix, section in COMMIT_TYPES.items():
            if msg.startswith((f"{prefix}:", f"{prefix}(")):
                body = msg.split(":", 1)[-1].strip()
                sections[section].append(body)
                matched = True
                break
        if not matched:
            sections["Other"].append(msg)
    return {k: v for k, v in sections.items() if v}


def format_entry(version: str, sections: dict[str, list[str]]) -> str:
    """Format a CHANGELOG entry.

    Args:
        version: Version string (e.g. ``0.2.0``).
        sections: Grouped commit messages.

    Returns:
        Formatted markdown string.
    """
    today = datetime.datetime.now(tz=datetime.UTC).date().isoformat()
    lines = [f"## [{version}] - {today}", ""]
    for section, items in sections.items():
        lines.append(f"### {section}")
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CHANGELOG entry.")
    parser.add_argument("--since", required=True, help="Git ref to compare from.")
    parser.add_argument("--version", required=True, help="New version string.")
    args = parser.parse_args()
    commits = get_commits(args.since)
    if not commits:
        print("No commits found.", file=sys.stderr)
        sys.exit(1)
    sections = classify_commits(commits)
    print(format_entry(args.version, sections))


if __name__ == "__main__":
    main()
