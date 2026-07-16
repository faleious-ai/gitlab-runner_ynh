#!/usr/bin/env python3
"""Fail-closed scan for credential-like literals in the current tracked tree."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


PATTERNS = (
    re.compile(r"\bgl(?:rt|pat|cbt)-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._~-]{12,}"),
    re.compile(r"(?i)(?:private[-_ ]token|access[-_ ]token)\s*[:=]\s*[\"']?(?!TEST_ONLY|PLACEHOLDER|REDACTED)[A-Za-z0-9._~-]{12,}"),
)


def tracked_files(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            check=True,
            capture_output=True,
        )
        names = result.stdout.decode("utf-8").split("\0")
        return [root / name for name in names if name]
    except (OSError, subprocess.CalledProcessError):
        return [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in tracked_files(root):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pattern in PATTERNS:
            if pattern.search(content):
                findings.append(str(path.relative_to(root)))
                break
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    if findings:
        print("credential-like content found in current tree:", file=__import__("sys").stderr)
        for path in findings:
            print(path, file=__import__("sys").stderr)
        return 1
    print("secret scan: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
