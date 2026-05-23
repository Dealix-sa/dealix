#!/usr/bin/env python3
"""Scan prompts/outputs for forbidden phrases and risky patterns.

Hard failures (exit 1):
- secret-looking literals (AKIA*, ghp_*, sk-*) anywhere in tracked
  markdown/YAML.
- forbidden marketing phrases ("guaranteed revenue" etc.) in agent
  prompt/output files (under ``prompts/`` or files matching
  ``*agent_output*`` / ``*agent_prompt*``).

Soft warnings (no exit):
- the same forbidden phrases appearing inside `docs/` are treated as
  references / definitions and reported as warnings only, because the
  Dealix doc tree intentionally enumerates banned phrases (governance,
  responsible-AI, forbidden-actions, etc.).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PHRASES = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed meetings",
    "guaranteed replies",
    "fully compliant",
    "no-risk",
    "sent automatically",
]

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

# Files that may *mention* the forbidden phrases because they define
# them as forbidden (policy / eval / verifier / CLAUDE.md).
POLICY_DEFINING_FILES = {
    "policies/dealix_control_policy.yaml",
    "evals/gates/dealix_agent_eval_gate.yaml",
    "scripts/verify_prompt_output_quality.py",
    "scripts/verify_policy_as_code.py",
    "scripts/verify_eval_gate.py",
    "scripts/verify_ultimate_operating_layer.py",
    "CLAUDE.md",
}

HARD_SCAN_DIRS = ["prompts", "registries", "evals/gates"]
SOFT_SCAN_DIRS = ["docs", "policies"]


def iter_files(roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for sub in roots:
        root = REPO_ROOT / sub
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".txt"}:
                files.append(path)
    return files


def main() -> int:
    hard_fail: list[str] = []
    warnings: list[str] = []

    # Hard scan: anything in prompts/, registries/, evals/gates/.
    for path in iter_files(HARD_SCAN_DIRS):
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        if rel not in POLICY_DEFINING_FILES:
            for phrase in FORBIDDEN_PHRASES:
                if phrase in lower:
                    hard_fail.append(f"{rel}: forbidden phrase '{phrase}'")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hard_fail.append(f"{rel}: secret-looking literal {pat.pattern}")

    # Soft scan: docs/ may mention forbidden phrases (forbidden actions
    # docs, governance, trust pack, etc.) — warnings only.
    for path in iter_files(SOFT_SCAN_DIRS):
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        if rel not in POLICY_DEFINING_FILES:
            for phrase in FORBIDDEN_PHRASES:
                if phrase in lower:
                    warnings.append(f"{rel}: forbidden phrase '{phrase}' (informational)")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hard_fail.append(f"{rel}: secret-looking literal {pat.pattern}")

    for w in warnings[:50]:
        print(f"[verify_prompt_output_quality] WARN: {w}")
    if len(warnings) > 50:
        print(f"[verify_prompt_output_quality] ... {len(warnings) - 50} more warnings suppressed")

    if hard_fail:
        for f in hard_fail:
            print(f"[verify_prompt_output_quality] FAIL: {f}")
        return 1
    print(f"[verify_prompt_output_quality] PASS  warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
