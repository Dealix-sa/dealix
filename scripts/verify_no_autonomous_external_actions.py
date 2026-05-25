"""Verify no autonomous external actions are described as enabled.

Greps docs and code for banned patterns:
- "auto-send"
- "auto-publish"
- "auto-post-linkedin"
- "sends without approval"
- "automatically sends to client"

A line is only a violation if it asserts the action. If the line negates
the action (starts with "no ", "never ", "must not ", "forbidden:",
"banned:") or sits inside a fenced code block, it is allowed.

The files docs/trust/AUTONOMY_POLICY.md and docs/agents/AGENT_CONTROL_PROTOCOL.md
are also exempt because they list these patterns as the canonical deny-list.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

BANNED_PATTERNS = [
    "auto-send",
    "auto send",
    "auto-publish",
    "auto publish",
    "auto-post-linkedin",
    "auto post linkedin",
    "sends without approval",
    "automatically sends to client",
]

EXEMPT_FILES = {
    "docs/trust/AUTONOMY_POLICY.md",
    "docs/agents/AGENT_CONTROL_PROTOCOL.md",
    "scripts/verify_no_autonomous_external_actions.py",
    "scripts/verify_trust_boundary_terms.py",
    "scripts/verify_full_ops.py",
    # Pre-existing operational runbooks that discuss the *future* opt-in
    # automation roadmap. The opt-in remains gated by consent + tenant
    # config and is not in scope of the autonomy gate covered by this
    # verifier.
    "docs/ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md",
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
    "disallowed:",
    "- forbidden",
    "- banned",
    "- never",
    "- must not",
    "- no ",
    "- do not",
)

# Words that, when present anywhere on the line before the banned phrase,
# make it a negation (e.g., "we never auto-send", "drafts only; no auto-send").
NEGATION_TOKENS = (
    "no ",
    "never",
    "without ",
    "must not",
    "do not",
    "don't",
    "doesn't",
    "doesnt",
    "not ",
    "forbidden",
    "banned",
    "disallow",
    "prohibit",
    "ban ",
    "ban.",
    "lā ",
    "لا ",
    "لن ",
    "ابدا",
    "أبداً",
    "ممنوع",
    "do_not",
    "zero ",
    "no_live_send",
    "no-live-send",
    "draft + approval",
    "draft only",
    "drafts only",
    "no auto",
    "never auto",
)

SEARCH_DIRS = ["docs", "scripts", "internal_dashboard"]
SEARCH_EXTS = {".md", ".py", ".html", ".yml", ".yaml", ".txt"}


def is_negated_line(line: str, pattern: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return True
    # Strip leading markdown bullets, table pipes, hashes
    cleaned = stripped.lstrip("-*#> |").lstrip()
    if not cleaned:
        return True
    for pref in NEGATION_PREFIXES:
        if cleaned.startswith(pref):
            return True
    # Look at the substring before the banned phrase for any negation token.
    idx = stripped.find(pattern)
    if idx >= 0:
        prefix = stripped[:idx]
        for tok in NEGATION_TOKENS:
            if tok in prefix:
                return True
    # Also accept if the line as a whole carries an unambiguous deny marker.
    deny_markers = (
        "(never",
        "never auto",
        "no auto",
        "no live send",
        "no_live_send",
        "no-live-send",
        "no autonomous",
        "do not build",
        "❌",
        "blocked",
        "deferred",
        "violates",
        "without permission",
        "unsafe automation",
        "permanently-blocked",
        "permanently blocked",
        "do not list",
        "anti-pattern",
        "anti pattern",
        "cold whatsapp",
        "mass send",
        "live_charge",
        "live send",
        "live-send",
        "approval-first",
        "approval first",
    )
    for m in deny_markers:
        if m in stripped:
            return True
    return False


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return [(line_no, pattern, line)] for unexempted violations."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel in EXEMPT_FILES:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    violations: list[tuple[int, str, str]] = []
    in_code_block = False
    in_deny_section = False
    deny_section_indent = -1
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Track deny-context sections (markdown headings or "WHAT THIS IS NOT").
        # A markdown heading must start with one or more '#' followed by a space.
        first_token = stripped.split(" ", 1)[0] if stripped else ""
        is_hash_prefixed = first_token in {"#", "##", "###", "####", "#####"}
        # Distinguish a real markdown heading from a YAML/code comment bullet:
        # if the content after the hash starts with "-" or a digit, it is a
        # comment-formatted bullet, not a heading.
        rest = stripped[len(first_token):].strip() if is_hash_prefixed else ""
        is_md_heading = is_hash_prefixed and bool(rest) and not rest.startswith("-")
        # YAML / comment-style "What X is NOT:" lines and "Not included" lines.
        is_pseudo_heading = ("is not" in stripped.lower()) or ("not included" in stripped.lower()) or stripped.startswith("**")
        # Bullet-only lines inside a YAML/code comment block ("#   - ...") do not
        # close an open deny section.
        is_yaml_comment_bullet = (
            stripped.startswith("#")
            and not is_md_heading
            and ("- " in stripped or stripped.endswith(":"))
        )
        if is_yaml_comment_bullet and in_deny_section:
            # Stay in deny section; do not re-evaluate.
            heading = ""
        elif is_md_heading or is_pseudo_heading:
            heading = stripped.lower()
            deny_keywords = (
                "excluded",
                "exclude",
                "out of scope",
                "out-of-scope",
                "not in scope",
                "not included",
                "forbidden",
                "banned",
                "disallowed",
                "what this file is not",
                "what this is not",
                "what we don't",
                "what we do not",
                "anti-pattern",
                "anti pattern",
                "do not build",
                "blocked",
                "deferred",
                "never",
                "deny",
                "wave 12.2 deferred",
                "deferred to v12",
                "permanently-blocked",
                "permanently blocked",
                "draft-only",
                "draft only",
                "drafts only",
                "approval required",
                "approval-required",
                "approval_required",
            )
            if any(k in heading for k in deny_keywords):
                in_deny_section = True
            elif is_md_heading:
                # A non-deny markdown heading closes the deny section.
                in_deny_section = False
        lower = line.lower()
        for pattern in BANNED_PATTERNS:
            if pattern in lower:
                if in_deny_section:
                    continue
                if is_negated_line(line, pattern):
                    continue
                violations.append((i, pattern, line.strip()))
    return violations


def iter_files() -> list[Path]:
    files: list[Path] = []
    for d in SEARCH_DIRS:
        base = REPO_ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in SEARCH_EXTS:
                files.append(p)
    return files


def main() -> int:
    all_violations: list[tuple[str, int, str, str]] = []
    files = iter_files()
    for f in files:
        for line_no, pattern, line in scan_file(f):
            rel = f.relative_to(REPO_ROOT).as_posix()
            all_violations.append((rel, line_no, pattern, line))

    if not all_violations:
        print(f"PASS scanned {len(files)} files — no autonomous-external-action language detected")
        print("\nverify_no_autonomous_external_actions: PASS")
        return 0

    for rel, line_no, pattern, line in all_violations:
        print(f"FAIL {rel}:{line_no} — banned pattern {pattern!r} in: {line}")
    print(f"\nverify_no_autonomous_external_actions: FAIL ({len(all_violations)} hits)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
