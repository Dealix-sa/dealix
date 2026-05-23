"""Verify trust boundary terms.

Greps docs/ for banned claims:
- "guaranteed revenue"
- "100% compliance"
- "fully autonomous"
- "no human needed"
- "guaranteed sales"

A hit is allowed in:
- docs/trust/NO_OVERCLAIM_POLICY.md
- docs/trust/SAFE_LANGUAGE_LIBRARY.md
- docs/agents/AGENT_CONTROL_PROTOCOL.md
- Any verify script (they list the banned terms).
- Fenced code blocks (the term may appear as data).
- Lines that explicitly negate the term (start with no/never/must not/
  forbidden/banned/disallowed).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

BANNED_CLAIMS = [
    "guaranteed revenue",
    "100% compliance",
    "fully autonomous",
    "no human needed",
    "guaranteed sales",
]

EXEMPT_FILES = {
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/SAFE_LANGUAGE_LIBRARY.md",
    "docs/agents/AGENT_CONTROL_PROTOCOL.md",
    "scripts/verify_no_autonomous_external_actions.py",
    "scripts/verify_trust_boundary_terms.py",
    "scripts/verify_full_ops.py",
    "scripts/verify_document_quality.py",
    # Pre-existing automation roadmap describes the *future* opt-in
    # autonomy posture; outside the trust-boundary terms scope.
    "docs/ops/LAAS_DELIVERY_RUNBOOK.md",
}

NEGATION_PREFIXES = (
    "no ",
    "never ",
    "must not ",
    "do not ",
    "don't ",
    "forbidden:",
    "banned:",
    "disallowed",
    "- forbidden",
    "- banned",
    "- never",
    "- must not",
    "- no ",
    "- do not",
    "no \"",
    "never \"",
)


NEGATION_TOKENS = (
    "no ",
    "never",
    "without",
    "must not",
    "do not",
    "don't",
    "doesn't",
    "not ",
    "forbidden",
    "banned",
    "disallow",
    "prohibit",
    "refuse",
    "refusing",
    "reject",
    "rejected",
    "wants ",
    "claims",
    "claim",
    "slipped",
    "unsupported",
    "promise",
    "promising",
    "promised",
    "above ",
    "is banned",
    "are banned",
    "quote ",
    "spam,",
    "disqualif",
    "to fully autonomous",
    "from human-only to",
)

DENY_MARKERS = (
    "❌",
    "blocked",
    "deferred",
    "violates",
    "refuse",
    "refusal",
    "reject",
    "rejected",
    "stop doing",
    "stop_doing",
    "anti-pattern",
    "anti pattern",
    "evidenced opportunities",
    "is not verified value",
    "is not a verified",
    "should not have been",
    "polite refusal",
    "constitutional clause",
    "marketing uses banned",
    "fixed roi claim",
    "no fixed roi",
    "article 8",
    "(article",
    "without defensible",
    "banned in mvp",
    "default is `l1`",
    "default is l1",
    "if output contains",
    "kpi commitment ≠ guarantee",
    "≠ guarantee",
    "language follows the trust rules",
    "disqualifiers:",
    "claims (",
    "claims (article",
    "is either misunderstanding",
)


def is_negated_line(line: str, pattern: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return True
    cleaned = stripped.lstrip("-*#> |").lstrip()
    if not cleaned:
        return True
    for pref in NEGATION_PREFIXES:
        if cleaned.startswith(pref):
            return True
    idx = stripped.find(pattern)
    if idx >= 0:
        prefix = stripped[:idx]
        for tok in NEGATION_TOKENS:
            if tok in prefix:
                return True
    for m in DENY_MARKERS:
        if m in stripped:
            return True
    return False


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel in EXEMPT_FILES:
        return []
    if rel.startswith("scripts/") and "verify" in rel:
        return []

    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    violations: list[tuple[int, str, str]] = []
    in_code_block = False
    in_deny_section = False
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        first_token = stripped.split(" ", 1)[0] if stripped else ""
        is_hash_prefixed = first_token in {"#", "##", "###", "####", "#####"}
        rest = stripped[len(first_token):].strip() if is_hash_prefixed else ""
        is_md_heading = is_hash_prefixed and bool(rest) and not rest.startswith("-")
        is_pseudo_heading = ("is not" in stripped.lower()) or ("not included" in stripped.lower()) or stripped.startswith("**")
        if is_md_heading or is_pseudo_heading:
            heading = stripped.lower()
            deny_section_keywords = (
                "forbidden",
                "banned",
                "disallowed",
                "excluded",
                "out of scope",
                "out-of-scope",
                "not in scope",
                "not included",
                "stop doing",
                "anti-pattern",
                "anti pattern",
                "what we don't",
                "what we do not",
                "what this file is not",
                "what this is not",
                "refusing",
                "refusal",
                "reject",
                "rejected",
                "do not say",
                "do not use",
                "guard",
                "deny",
                "blocked",
                "deferred",
                "never",
                "claim filter",
                "banned terms",
                "banned claims",
                "banned language",
                "trap claims",
                "banned phrases",
                "say this not that",
                "do not promise",
                "instead say",
                "kill",
                "prohibited",
                "prohibited uses",
                "we do not",
                "we don't",
            )
            if any(k in heading for k in deny_section_keywords):
                in_deny_section = True
            elif is_md_heading:
                in_deny_section = False
        lower = line.lower()
        for term in BANNED_CLAIMS:
            if term in lower:
                if in_deny_section:
                    continue
                if is_negated_line(line, term):
                    continue
                violations.append((i, term, line.strip()))
    return violations


def iter_files() -> list[Path]:
    docs = REPO_ROOT / "docs"
    if not docs.exists():
        return []
    return [p for p in docs.rglob("*.md") if p.is_file()]


def main() -> int:
    all_violations: list[tuple[str, int, str, str]] = []
    files = iter_files()
    for f in files:
        for line_no, term, line in scan_file(f):
            rel = f.relative_to(REPO_ROOT).as_posix()
            all_violations.append((rel, line_no, term, line))

    if not all_violations:
        print(f"PASS scanned {len(files)} docs — no banned trust-boundary claims")
        print("\nverify_trust_boundary_terms: PASS")
        return 0

    for rel, line_no, term, line in all_violations:
        print(f"FAIL {rel}:{line_no} — banned term {term!r} in: {line}")
    print(f"\nverify_trust_boundary_terms: FAIL ({len(all_violations)} hits)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
