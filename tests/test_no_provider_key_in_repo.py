"""Contract: no live provider API key may live in tracked repository content.

Scans tracked files for live key patterns (DeepSeek, OpenAI project, OpenRouter,
Anthropic, Google, Groq) and fails the build if any match falls outside the
allowlisted paths (.env.example, .gitleaks.toml, tests/fixtures, docs).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

KEY_PATTERNS: dict[str, re.Pattern[str]] = {
    "openai_project": re.compile(r"sk-proj-[A-Za-z0-9_-]{40,}"),
    "openrouter": re.compile(r"sk-or-v1-[a-f0-9]{40,}"),
    "deepseek": re.compile(r"sk-[a-f0-9]{32}\b"),
    "anthropic": re.compile(r"sk-ant-api\d{2}-[A-Za-z0-9_-]{80,}"),
    "google": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    "groq": re.compile(r"gsk_[A-Za-z0-9]{40,}"),
}

ALLOWLISTED_PATHS = {
    ".env.example",
    ".gitleaks.toml",
    ".secrets.baseline",
    "tests/test_no_provider_key_in_repo.py",
}

ALLOWLISTED_PREFIXES = (
    "tests/fixtures/",
    "docs/",
)


def _tracked_files() -> list[Path]:
    """Files tracked by git only — ignores .env.local and other gitignored files."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line.strip()]


def _is_allowlisted(rel: str) -> bool:
    if rel in ALLOWLISTED_PATHS:
        return True
    return any(rel.startswith(p) for p in ALLOWLISTED_PREFIXES)


def test_no_live_provider_key_in_tracked_files() -> None:
    offenders: list[tuple[str, str, str]] = []
    for path in _tracked_files():
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        if _is_allowlisted(rel):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError):
            continue
        for label, pattern in KEY_PATTERNS.items():
            match = pattern.search(content)
            if match:
                offenders.append((rel, label, match.group(0)[:24] + "…"))
    assert not offenders, (
        "Live provider API key detected in tracked files: " + repr(offenders)
    )
