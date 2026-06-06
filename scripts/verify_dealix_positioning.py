#!/usr/bin/env python3
"""Verify Dealix positioning is present, coherent, and free of unsafe claims.

Dependency-free (stdlib only). Part of the Dealix launch gates.

PASS criteria:
  1. Platform Source of Truth exists and states the operating equation +
     the strategic wedge (Revenue Intelligence Sprint).
  2. Claims Register exists.
  3. Command Sprint one-pager exists.
  4. No unsafe claims (guaranteed revenue, auto-send, cold WhatsApp,
     LinkedIn automation, scraping, fake proof) anywhere in the
     customer-facing surfaces.

Exit 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files that must exist and carry positioning truth.
TRUTH = ROOT / "docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md"
CLAIMS = ROOT / "docs/03_governance/CLAIMS_REGISTER.md"
SPRINT = ROOT / "sales/COMMAND_SPRINT_ONE_PAGER.md"

# Phrases the Source of Truth must contain (doctrine anchors).
REQUIRED_PHRASES = [
    "Revenue Intelligence Sprint",
    "Proof",
    "approval",  # founder approval gate
]

# Unsafe claim patterns. Each is (regex, human label).
UNSAFE_PATTERNS = [
    (r"guaranteed\s+revenue", "guaranteed revenue"),
    (r"نضمن[^\n]{0,20}(مبيعات|إيراد|زيادة)", "Arabic revenue guarantee"),
    (r"auto[- ]?send", "auto-send"),
    (r"cold\s+whatsapp", "cold WhatsApp"),
    (r"linkedin\s+automation", "LinkedIn automation"),
    (r"\bscrap(e|ing)\b", "scraping"),
    (r"fake\s+proof", "fake proof"),
]

# Surfaces to scan for unsafe claims (customer-facing only).
SCAN_TARGETS = [
    ROOT / "README.md",
    ROOT / "README.ar.md",
    ROOT / "sales",
    ROOT / "docs/00_platform_truth",
    ROOT / "docs/03_governance",
    ROOT / "docs/04_delivery",
    ROOT / "docs/06_growth",
]

# Allow-list: docs that legitimately mention an unsafe term to FORBID it.
# Such mentions are negated (e.g. "no auto-send", "we refuse scraping").
NEGATION_CONTEXT = re.compile(
    r"(no|never|not|without|refus|forbid|reject|ban|prohibit|بدون|لا\s|نرفض|يُمنع|ممنوع)",
    re.IGNORECASE,
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"PASS: {msg}")


def iter_md(target: Path):
    if target.is_file():
        yield target
    elif target.is_dir():
        yield from sorted(target.rglob("*.md"))


def main() -> int:
    print("== Dealix Positioning Verifier ==")
    failures = 0

    # 1-3: required files exist.
    for label, path in [
        ("Platform Source of Truth", TRUTH),
        ("Claims Register", CLAIMS),
        ("Command Sprint one-pager", SPRINT),
    ]:
        if path.is_file():
            ok(f"{label} present ({path.relative_to(ROOT)})")
        else:
            fail(f"{label} missing ({path.relative_to(ROOT)})")
            failures += 1

    # Required phrases in the Source of Truth.
    if TRUTH.is_file():
        text = TRUTH.read_text(encoding="utf-8", errors="ignore")
        for phrase in REQUIRED_PHRASES:
            if phrase.lower() in text.lower():
                ok(f"Source of Truth states: {phrase!r}")
            else:
                fail(f"Source of Truth missing required phrase: {phrase!r}")
                failures += 1

    # Unsafe claim scan.
    # A match is allowed only when a negation/forbidding word appears within a
    # short context window (current line + the 3 preceding non-empty lines).
    # This keeps real unsafe claims caught while letting policy docs *list* the
    # forbidden phrasings (e.g. "You are NOT ready if ... auto-send").
    print("-- unsafe claim scan --")
    unsafe_hits = 0
    for target in SCAN_TARGETS:
        for md in iter_md(target):
            lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()
            for i, line in enumerate(lines, 1):
                for pattern, label in UNSAFE_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        window = "\n".join(lines[max(0, i - 4):i])
                        if NEGATION_CONTEXT.search(window):
                            continue  # negated / forbidden context is allowed
                        rel = md.relative_to(ROOT)
                        fail(f"unsafe claim '{label}' @ {rel}:{i}: {line.strip()[:90]}")
                        unsafe_hits += 1
    if unsafe_hits == 0:
        ok("no unsafe claims found in customer-facing surfaces")
    else:
        failures += unsafe_hits

    print()
    if failures:
        print(f"RESULT: FAIL ({failures} issue(s))")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
