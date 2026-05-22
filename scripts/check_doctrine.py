#!/usr/bin/env python3
"""Doctrine guard — scans the repo for code that would violate the 11 non-negotiables.

Run locally before committing, or as a CI gate.

What it checks (intentionally narrow — false positives waste founder time):
  1. No module performs an HTTP POST/PUT/GET to linkedin.com or graph.facebook.com
     (whatsapp.com) from outside known guardrail modules. The whitelisted modules
     are channel-policy deciders and webhook receivers — they MUST be allowed to
     reference these hosts because their job is to gate them.

  2. No module under `auto_client_acquisition/` or `dealix/` exposes a public
     function whose name starts with `send_cold_` or `auto_send_outreach_`. The
     only allowed outreach surface is `*_draft()` / `*_drafts()` / `*_safe_send()`
     (the safe-send modules are pre-existing and already approval-gated).

  3. No string literal in non-test code contains "100% conversion", "guaranteed sales",
     "ضمان المبيعات", or "نتائج مضمونة" (no-overclaim register).

Exit code 0 = clean. Exit code 2 = at least one violation found. Prints the
violations to stderr so a CI step can capture them.

The 11 non-negotiables are quoted from AGENTS.md inline at the bottom of this file
so that any change to the doctrine forces a change to this file (single source of
truth enforcement).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Modules whose job is to GATE the forbidden channels. They are allowed to mention
# linkedin.com/whatsapp/graph.facebook.com because they enforce the doctrine.
GATE_WHITELIST = {
    "api/routers/autonomous.py",                       # channel_policy decider
    "api/routers/channel_policy_gateway.py",
    "auto_client_acquisition/whatsapp_safe_send.py",   # approval-gated safe send
    "api/routers/whatsapp_decision_bot.py",
    "api/routers/tool_guardrail_gateway.py",
    "scripts/check_doctrine.py",                       # self
    "tests/test_doctrine_enforcement.py",              # paired test
}

FORBIDDEN_HOST_RE = re.compile(
    r"(linkedin\.com|graph\.facebook\.com|wa\.me|api\.whatsapp\.com)",
    re.IGNORECASE,
)
FORBIDDEN_FUNC_RE = re.compile(
    r"^\s*(async\s+)?def\s+(send_cold_\w+|auto_send_outreach_\w+)\s*\(",
    re.MULTILINE,
)
OVERCLAIM_PATTERNS = [
    re.compile(r"100\s*%\s*conversion", re.IGNORECASE),
    re.compile(r"guaranteed\s+sales", re.IGNORECASE),
    re.compile(r"ضمان\s+المبيعات"),
    re.compile(r"نتائج\s+مضمونة"),
    re.compile(r"guaranteed\s+revenue", re.IGNORECASE),
]

# Words/phrases that indicate the surrounding context is REJECTING the overclaim
# (doctrine-enforcement code, disclaimers, block-lists). If any of these appear
# within DOCTRINE_NEGATION_WINDOW chars of a match, the match is suppressed.
DOCTRINE_NEGATION_TOKENS = (
    "not guaranteed", "no guaranteed", "never produced", "never claim",
    "blocked", "forbidden", "rejected", "disclaimer",
    "non-negotiable", "non_negotiable", "no_guaranteed", "no_overclaim",
    "doctrine", "redacted",
    "risky_phrases", "risky phrases", "markers", "what_we_will_not_do",
    "block-list", "block_list", "blocklist", "scope_classifier",
    "ليست", "ليس", "بدون", "محظور", "ممنوع", "يرفض", "يحظر",
    "لا نضمن", "لا تعد", "تقديرية",
)
DOCTRINE_NEGATION_WINDOW = 400  # chars before+after the match

SCAN_ROOTS = ["api", "auto_client_acquisition", "dealix", "scripts", "frontend/src"]
EXCLUDE_DIR_NAMES = {"__pycache__", "node_modules", ".next", "dist", "build", ".venv"}
EXCLUDE_FILE_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".ico", ".svg", ".woff", ".woff2"}


def _iter_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        root_path = REPO_ROOT / root
        if not root_path.exists():
            continue
        for path in root_path.rglob("*"):
            if path.is_dir():
                continue
            if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
                continue
            if path.suffix in EXCLUDE_FILE_SUFFIXES:
                continue
            files.append(path)
    return files


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _is_test_file(rel: str) -> bool:
    return rel.startswith("tests/") or "/tests/" in rel or rel.endswith("_test.py") or "/test_" in rel


def scan() -> list[tuple[str, int, str]]:
    violations: list[tuple[str, int, str]] = []

    for path in _iter_files():
        rel = _rel(path)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        # Rule 1: forbidden hosts in non-whitelisted modules
        if rel not in GATE_WHITELIST and not _is_test_file(rel):
            for lineno, line in enumerate(text.splitlines(), start=1):
                if FORBIDDEN_HOST_RE.search(line):
                    # Allow mentions inside comments/docstrings that are
                    # discussing policy, not making calls. We pick up only
                    # lines that look like network calls.
                    if re.search(r"(httpx|requests|aiohttp|fetch|axios)\.(get|post|put|delete|request)", line, re.IGNORECASE):
                        violations.append((rel, lineno, f"forbidden host outside gate whitelist: {line.strip()[:120]}"))

        # Rule 2: forbidden function names (always — even in tests)
        if path.suffix == ".py":
            for match in FORBIDDEN_FUNC_RE.finditer(text):
                lineno = text[: match.start()].count("\n") + 1
                violations.append((rel, lineno, f"forbidden function name: {match.group(0).strip()}"))

        # Rule 3: overclaim language in non-test, non-doc, non-YAML-rules code,
        # and excluding the doctrine guard itself (self-reference is allowed).
        is_doctrine_guard = rel in {"scripts/check_doctrine.py", "tests/test_doctrine_enforcement.py"}
        if not _is_test_file(rel) and not rel.startswith("docs/") and not rel.endswith(".yaml") and not is_doctrine_guard:
            for pat in OVERCLAIM_PATTERNS:
                for match in pat.finditer(text):
                    # Check the surrounding window for doctrine-negation tokens.
                    # If any are present, this is enforcement code, not overclaim.
                    start = max(0, match.start() - DOCTRINE_NEGATION_WINDOW)
                    end = min(len(text), match.end() + DOCTRINE_NEGATION_WINDOW)
                    window = text[start:end].lower()
                    if any(tok in window for tok in DOCTRINE_NEGATION_TOKENS):
                        continue
                    lineno = text[: match.start()].count("\n") + 1
                    violations.append((rel, lineno, f"overclaim language: {match.group(0)!r}"))

    return violations


def main() -> int:
    violations = scan()
    if not violations:
        print("doctrine_check=PASS (no violations across api/, auto_client_acquisition/, dealix/, scripts/, frontend/src/)")
        return 0
    print(f"doctrine_check=FAIL ({len(violations)} violation(s)):", file=sys.stderr)
    for rel, lineno, msg in violations:
        print(f"  {rel}:{lineno}  {msg}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())


# === 11 non-negotiables (quoted from AGENTS.md / dealix-pm sub-agent) ===
# 1. No scraping systems
# 2. No cold WhatsApp automation
# 3. No LinkedIn automation
# 4. No fake/un-sourced claims
# 5. No guaranteed sales outcomes
# 6. No PII in logs
# 7. No source-less knowledge answers
# 8. No external action without approval
# 9. No agent without identity
# 10. No project without Proof Pack
# 11. No project without Capital Asset
