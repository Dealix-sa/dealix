#!/usr/bin/env python3
"""Dealix positioning + claim-safety verifier (Wave 7).

Two jobs:
  1. Positioning truth — the homepage must say what Dealix *is* (an AI
     Business Operating System for Saudi companies) and distinguish it from
     a CRM / chatbot, and the Command Sprint page must exist and name the
     offer.
  2. Claim safety — no unapproved *positive* guaranteed-outcome /
     cold-outreach / scraping language on the public surface.

Why a negation-aware scan (not the token-only allowlist in
tests/test_landing_forbidden_claims.py): the static site has grown well
beyond that hand-curated allowlist, so a pure token scan over-reports —
every page that carries the standard "Estimated outcomes are not
guaranteed / النتائج التقديرية ليست نتائج مضمونة" disclaimer, or the
anti-cold/anti-scraping safety list, would be flagged. This scanner
instead flags a forbidden token only when it is used *positively* — i.e.
NOT inside a negation/disclaimer ("not guaranteed", "ليست مضمونة",
"لا scraping", "صفر cold", "NO scraping", "بدون") and NOT a money-back
refund guarantee ("money-back guarantee", "ضمان استرجاع").

Exit code 0 = PASS, 1 = FAIL. Pure stdlib.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"

FORBIDDEN = [
    ("guaranteed", re.compile(r"\bguarante(e|ed|es)\b", re.IGNORECASE)),
    ("مضمون", re.compile(r"مضمون[ةه]?")),
    ("نضمن", re.compile(r"نضمن")),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scraping", re.compile(r"\bscrap(e|ing)\b", re.IGNORECASE)),
    ("cold outreach", re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging|sequences?)\b", re.IGNORECASE)),
]

# A forbidden token is SAFE if one of these appears in the lookback window.
NEGATORS = [
    "لا", "بدون", "صفر", "ليست", "ليس", "دون", "نرفض", "يرفض", "رفض",
    "no", "not", "never", "without", "zero", "reject", "rejects",
    "anti", "doesn't", "don't", "won't", "no_", "no-",
]
# Qualifiers that legitimize the word "guarantee" (refund guarantee, approved
# in docs/governance/CLAIMS_REGISTER.md #7).
GUARANTEE_QUALIFIERS = ["money-back", "money back", "refund", "استرجاع", "استرداد", "back guarantee"]

WINDOW = 55

FAILURES: list[str] = []
WARNINGS: list[str] = []


def _normalize(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text)


def _safe(text: str, token: str, start: int) -> bool:
    window = text[max(0, start - WINDOW) : start].lower()
    if any(neg in window for neg in NEGATORS):
        return True
    if token == "guaranteed":
        if any(q in window for q in GUARANTEE_QUALIFIERS):
            return True
        # also accept a money-back qualifier *after* the word (e.g. "guarantee — refund")
        tail = text[start : start + WINDOW].lower()
        if any(q in tail for q in GUARANTEE_QUALIFIERS):
            return True
    return False


# Map this scanner's token labels onto the founder-curated allowlist keys in
# tests/test_landing_forbidden_claims.py (which uses 'cold'/'scrape'/'scraping').
ALLOWLIST_KEYS = {
    "cold outreach": {"cold"},
    "scraping": {"scraping", "scrape"},
    "guaranteed": {"guaranteed"},
    "blast": {"blast"},
    "مضمون": {"مضمون"},
    "نضمن": {"نضمن"},
}


def _load_allowlist() -> dict:
    """Founder-reviewed per-file negation/disclaimer allowlist (best-effort)."""
    tests = ROOT / "tests"
    if str(tests) not in sys.path:
        sys.path.insert(0, str(tests))
    try:
        import test_landing_forbidden_claims as guard  # type: ignore

        return guard.ALLOWLIST
    except Exception:
        return {}


def scan_claim_safety() -> None:
    if not LANDING.is_dir():
        FAILURES.append("landing/ directory not found")
        return
    allowlist = _load_allowlist()
    for path in sorted(LANDING.glob("*.html")):
        allowed = set(allowlist.get(path.name, {}).keys())
        text = _normalize(path.read_text(encoding="utf-8"))
        for token, pattern in FORBIDDEN:
            # Skip tokens the founder has already reviewed for this file.
            if ALLOWLIST_KEYS.get(token, {token}) & allowed:
                continue
            for m in pattern.finditer(text):
                if not _safe(text, token, m.start()):
                    snippet = text[max(0, m.start() - 30) : m.start() + 30].strip()
                    FAILURES.append(
                        f"{path.name}: positive unsafe claim {token!r} -> …{snippet}…"
                    )
                    break  # one report per token per file


def check_positioning_truth() -> None:
    home = LANDING / "index.html"
    if not home.is_file():
        FAILURES.append("landing/index.html missing — no homepage to carry positioning")
        return
    html = home.read_text(encoding="utf-8").lower()
    if not (("نظام تشغيل" in html) or ("operating system" in html) or ("business os" in html)):
        FAILURES.append("index.html: missing the AI Business Operating System category statement")
    if "crm" not in html:
        WARNINGS.append("index.html: does not explicitly distinguish Dealix from a CRM")
    if ("chatbot" not in html) and ("شات بوت" not in html) and ("بوت" not in html):
        WARNINGS.append("index.html: does not explicitly distinguish Dealix from a chatbot")


def check_command_sprint_positioning() -> None:
    page = LANDING / "command-sprint.html"
    if not page.is_file():
        FAILURES.append("landing/command-sprint.html missing — Command Sprint has no page")
        return
    low = page.read_text(encoding="utf-8").lower()
    if "command sprint" not in low:
        FAILURES.append("command-sprint.html: does not name the Command Sprint offer")
    if "crm" not in low and "chatbot" not in low:
        WARNINGS.append("command-sprint.html: does not restate the not-a-CRM/chatbot positioning")


def main() -> int:
    print("== Dealix positioning + claim-safety verifier ==")
    scan_claim_safety()
    check_positioning_truth()
    check_command_sprint_positioning()

    for w in WARNINGS:
        print(f"  WARN: {w}")
    for f in FAILURES:
        print(f"  FAIL: {f}")

    if FAILURES:
        print(f"\nRESULT: FAIL ({len(FAILURES)} blocker(s), {len(WARNINGS)} warning(s))")
        return 1
    print(f"\nRESULT: PASS ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
