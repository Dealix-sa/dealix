#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "out",
    "dist",
    "build",
    ".next",
}

ALLOWED_ENV_EXAMPLES = {
    ".env.example",
    ".env.prod.example",
    ".env.railway.example",
    ".env.staging.example",
}

SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_\-]{12,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

ALLOW_WORDS = (
    "placeholder",
    "example",
    "dummy",
    "fake",
    "redacted",
    "test",
    "sample",
    "not_a_secret",
    "invalid",
    "mock",
    "SAFE_",
    "<",
)

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_DIRS)

def is_text_file(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False

issues: list[str] = []

for path in ROOT.rglob("*"):
    if path.is_dir() or should_skip(path):
        continue

    rel = path.relative_to(ROOT).as_posix()
    name = path.name

    # Do not allow real local env files, but allow committed templates.
    if name.startswith(".env") and name not in ALLOWED_ENV_EXAMPLES:
        issues.append(f"Do not commit local env file: {rel}")

    if not is_text_file(path):
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")
    for lineno, line in enumerate(text.splitlines(), 1):
        lowered = line.lower()
        if any(word.lower() in lowered for word in ALLOW_WORDS):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                issues.append(f"Potential live secret in {rel}:{lineno}: matches {pattern.pattern}")

if issues:
    print("Repository security smoke check failed:")
    print("")
    for issue in issues:
        print(f"- {issue}")
    raise SystemExit(1)

print("Repository security smoke check passed")
