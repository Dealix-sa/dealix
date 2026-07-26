#!/usr/bin/env python3
"""CI-safe security smoke gate for Dealix.

This check keeps hard failures for risky committed runtime files while avoiding
false positives from documented/test-only synthetic credentials.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Directory names pruned anywhere in the tree. These hold caches, build output
# or vendored third-party code — never Dealix-authored source — so scanning
# them produces false positives instead of signal.
SKIP_DIR_NAMES = {
    ".eggs",
    ".git",
    ".github",
    ".mypy_cache",
    ".next",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "dist-packages",
    "htmlcov",
    "node_modules",
    "site-packages",
    "venv",
}

# Repo-relative path prefixes pruned from the walk. Unlike SKIP_DIR_NAMES these
# are nested paths, so they need prefix matching rather than a name lookup.
SKIP_PATH_PREFIXES = ("reports/runtime",)

TEXT_SUFFIXES = {
    ".env",
    ".example",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_\-]{12,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

SAFE_CONTEXT_PATHS = (
    "docs/",
    "tests/",
)

SAFE_PLACEHOLDER_WORDS = (
    "example",
    "fixture",
    "fake",
    "dummy",
    "placeholder",
    "redacted",
    "replace",
    "change_me",
    "test",
    "synthetic",
    "sample",
    "xxxxx",
    "xxxx",
    "<fill",
    "<replace",
    "<your",
)

SAFE_TEMPLATE_PATHS = {
    "scripts/generate_production_env.sh",
}


def relpath(path: Path, root: Path = ROOT) -> str:
    return path.relative_to(root).as_posix()


def is_virtualenv(directory: Path) -> bool:
    """Detect a Python virtualenv by its marker file rather than by name.

    Name matching alone only caught ``.venv``/``venv``; any other name
    (``.venv-audit``, ``venv312``, ``env``) leaked vendored dependency code
    into the scan and produced false failures.
    """
    return (directory / "pyvenv.cfg").is_file()


def is_skipped_dir(directory: Path, rel: str) -> bool:
    """Return True when a directory must be pruned from the scan."""
    name = directory.name
    if name in SKIP_DIR_NAMES or name.endswith(".egg-info"):
        return True
    if rel.startswith(SKIP_PATH_PREFIXES):
        return True
    return is_virtualenv(directory)


def iter_candidate_files(root: Path = ROOT) -> Iterator[Path]:
    """Walk the repo, pruning excluded directories instead of descending them."""
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_dir = relpath(current, root)
        kept: list[str] = []
        for name in sorted(dirnames):
            child = current / name
            child_rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            if not is_skipped_dir(child, child_rel):
                kept.append(name)
        dirnames[:] = kept
        for name in sorted(filenames):
            yield current / name


def is_text_candidate(path: Path) -> bool:
    name = path.name
    if name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def is_allowed_env_example(path: Path) -> bool:
    name = path.name
    return name.startswith(".env") and name.endswith((".example", ".template", ".sample"))


def line_is_placeholder(line: str) -> bool:
    lowered = line.lower()
    return any(word in lowered for word in SAFE_PLACEHOLDER_WORDS)


def path_is_safe_context(path: Path, root: Path = ROOT) -> bool:
    rel = relpath(path, root)
    return rel.startswith(SAFE_CONTEXT_PATHS) or rel in SAFE_TEMPLATE_PATHS


def scan(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Scan ``root`` and return ``(failures, warnings)``."""
    failures: list[str] = []
    warnings: list[str] = []

    for path in iter_candidate_files(root):
        if not path.is_file():
            continue

        rel = relpath(path, root)

        if path.name.startswith(".env") and not is_allowed_env_example(path):
            failures.append(f"Do not commit local env file: {rel}")
            continue

        if not is_text_candidate(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for idx, line in enumerate(text.splitlines(), start=1):
            for pattern in SECRET_PATTERNS:
                if not pattern.search(line):
                    continue
                if path_is_safe_context(path, root) or line_is_placeholder(line):
                    warnings.append(f"Synthetic credential example ignored: {rel}:{idx}")
                    continue
                failures.append(f"Potential live secret in {rel}:{idx}: matches {pattern.pattern}")

    return failures, warnings


def main() -> int:
    failures, warnings = scan(ROOT)

    if failures:
        print("CI_SECURITY_SMOKE=FAIL")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("CI_SECURITY_SMOKE=PASS")
    if warnings:
        print(f"Ignored synthetic/test examples: {len(warnings)}")
        for item in warnings[:20]:
            print(f"WARN: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
