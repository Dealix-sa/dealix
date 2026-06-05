#!/usr/bin/env python3
"""Dealix website positioning gate.

Fails (exit 1) if customer-facing surfaces contain *positive assertions* of unsafe
claims that violate the Dealix constitution (CLAUDE.md / docs/00_constitution):
guaranteed revenue, fake proof, auto-send, cold WhatsApp/LinkedIn automation, or
reducing Dealix to a CRM/chatbot.

Design notes
------------
- Scans only customer-facing surfaces by default (landing/, frontend/src, README*),
  not the whole docs/ tree — governance docs *describe* these prohibitions and must
  not trip the gate.
- Skips lines that are negations / policy statements (e.g. "never enable auto-send",
  "لا نضمن المبيعات", "no cold WhatsApp"), because mentioning a rule is safe; only
  asserting the unsafe thing is not.
- Dependency-free; safe to run in CI and locally.

Usage:
    python scripts/verify_website_positioning.py [--all] [path ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Customer-facing surfaces (default scope).
DEFAULT_ROOTS = ["README.md", "README.ar.md", "landing", "frontend/src"]

# Wider scope used with --all: every customer-facing/product surface.
# The docs/ doctrine tree is intentionally EXCLUDED — it exists to *enumerate*
# prohibitions (NON_NEGOTIABLES, FORBIDDEN_ACTIONS, STOP_DOING, governance
# registries), so scanning it for prohibition keywords is noise, not signal.
WIDE_ROOTS = DEFAULT_ROOTS + ["apps/web/src", "apps/web/app", "apps/web/components"]

SCAN_SUFFIXES = {".md", ".mdx", ".tsx", ".ts", ".jsx", ".js", ".html"}

# Directories never worth scanning.
SKIP_DIR_PARTS = {"node_modules", ".next", ".git", "dist", "build", "__pycache__"}

# Unsafe *assertions* (the thing itself, not a rule about it).
BAD_PATTERNS = [
    (r"نضمن\s+(?:لك\s+)?(?:زيادة\s+)?(?:ال)?مبيعات", "guaranteed sales (AR)"),
    (r"نضمن\s+(?:لك\s+)?(?:ال)?(?:إيراد|ايراد|دخل|أرباح|ارباح)", "guaranteed revenue (AR)"),
    (r"guaranteed\s+revenue", "guaranteed revenue"),
    (r"guarantee[d]?\s+(?:you\s+)?(?:more\s+)?sales", "guaranteed sales"),
    (r"auto[-\s]?send", "auto-send"),
    (r"cold\s+whatsapp\s+automation", "cold WhatsApp automation"),
    (r"cold\s+linkedin\s+automation", "cold LinkedIn automation"),
    (r"\bDealix\s+is\s+a\s+CRM\b", "Dealix-is-a-CRM positioning"),
    (r"\bDealix\s+is\s+a\s+chatbot\b", "Dealix-is-a-chatbot positioning"),
    (r"fake\s+(?:proof|testimonial|review)", "fake proof/testimonial"),
]

# If any of these appear on the same line, the match is a rule/negation/policy
# statement — skip it. Mentioning a prohibition is safe; only *asserting* the
# unsafe thing is not. This list is deliberately broad on negation words because
# a genuine unsafe marketing claim ("we guarantee revenue") carries none of them.
NEGATION_MARKERS = [
    # English negation / policy
    "no ", "not", "never", "without", "avoid", "ban", "block", "prohibit",
    "forbid", "exclud", "don't", "doesn't", "won't", "can't", "cannot",
    "refus", "disable", "stop", "zero", "must not", "may not", "rather than",
    "instead of", "no-spam", "no_spam", "violation", "breach", "penalt",
    "red-team", "red team", "redteam", "governance-check", "governance check",
    "rewrite", "polite refusal", "anti-", "blocked", "❌", "🚫", "⛔",
    # Arabic negation / policy
    "لا ", "لن", "بدون", "ممنوع", "نرفض", "يمنع", "يُمنع", "منع", "تجنّب",
    "تجنب", "عدم", "غير قابل", "زائف", "بدل", "وعود", "مبالغ", "نلتزم",
]

COMPILED = [(re.compile(p, re.IGNORECASE), label) for p, label in BAD_PATTERNS]


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in SKIP_DIR_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in SCAN_SUFFIXES:
            yield path


def is_negated(line: str) -> bool:
    # Screaming-snake negation constants, e.g. NO_LIVE_SEND, NO_COLD_WHATSAPP.
    if "NO_" in line:
        return True
    # Comparison "no" cells / cross marks (competitor-attribute rows).
    if any(sym in line for sym in ("✗", "✕", "cmp-no", "cmp-partial")):
        return True
    low = line.lower()
    # Glued negations like noAutoSend / no-auto-send / noAutoSendNotice.
    normalized = re.sub(r"[^a-z0-9]", "", low)
    if "noauto" in normalized:
        return True
    return any(marker in low for marker in NEGATION_MARKERS)


def scan(roots: list[str]) -> list[str]:
    errors: list[str] = []
    for root_name in roots:
        root = Path(root_name)
        if not root.exists():
            continue
        for f in iter_files(root):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if is_negated(line):
                    continue
                for rx, label in COMPILED:
                    if rx.search(line):
                        snippet = line.strip()[:160]
                        errors.append(f"{f}:{lineno}: unsafe claim [{label}] -> {snippet}")
    return errors


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("-")]
    use_all = "--all" in argv[1:]
    if args:
        roots = args
    else:
        roots = WIDE_ROOTS if use_all else DEFAULT_ROOTS

    errors = scan(roots)
    if errors:
        print("FAIL: unsafe positioning/claims found:\n")
        print("\n".join(errors))
        print(f"\n{len(errors)} issue(s). Fix or rewrite safely (see CLAUDE.md hard rules).")
        return 1
    print(f"OK: website positioning check passed (scanned: {', '.join(roots)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
