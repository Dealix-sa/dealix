#!/usr/bin/env python3
"""Verify Dealix positioning & claims discipline in customer-facing surfaces.

Asserts:
  1. The canonical Platform Truth docs exist.
  2. No forbidden claim (EN/AR) appears in customer-facing copy
     (sales kit + wave3 website content/components).

Governance/claims docs that legitimately *document* forbidden phrases are
excluded from the scan (they are allowed to quote what we do NOT say).

Dependency-free. Prints KEY=value lines. Exit 0 on pass, 1 on fail.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/00_platform_truth/PLATFORM_TRUTH.md",
    "docs/00_platform_truth/MODULE_STATUS.md",
    "docs/00_platform_truth/CTA_MAP.md",
    "docs/governance/CLAIMS_REGISTER.md",
]

# Surfaces that face customers — these must be clean.
SCAN_DIRS = [
    "sales",
    "frontend/src/content/wave3",
    "frontend/src/components/wave3",
]
SCAN_SUFFIXES = {".md", ".ts", ".tsx", ".mdx", ".json"}

# Files allowed to *quote* forbidden phrases because they document the policy.
ALLOWLIST_NAMES = {
    "CLAIMS_REGISTER.md",
    "FORBIDDEN_ACTIONS.md",
    "PLATFORM_TRUTH.md",
    "MODULE_STATUS.md",
}

# Affirmative guarantee/fake CLAIMS — never acceptable, even negated.
# Sourced from auto_client_acquisition/governance_os/draft_gate.py + saudi_layer/forbidden_claims.py.
ALWAYS_FORBIDDEN = [
    "guaranteed sales",
    "guaranteed results",
    "guaranteed roi",
    "guarantee roi",
    "guarantee revenue",
    "guaranteed revenue",
    "fake proof",
    "fake testimonial",
    "نضمن",
    "ربح مؤكد",
]

# Dual-use phrases — fine in the negative ("no cold whatsapp"), bad as a claim.
# Flagged only when the SAME LINE has no negation marker.
DUAL_USE = [
    "cold whatsapp",
    "linkedin automation",
    "auto-send",
    "auto send",
    "scraping",
    "purchased list",
    "blast",
    "مضمون",
    "ضمان مبيعات",
    "بدون أي مخاطرة",
]

NEGATION = [
    "no ", "not ", "never", "without", "don't", "doesn't", "no-",
    "لا ", "بدون", "دون ", "ليس", "ممنوع", "يمنع", "نحن لا", "لا نرسل",
    "blocks", "block ",
]


def _has_negation(line: str) -> bool:
    return any(n in line for n in NEGATION)


def _iter_files():
    for rel in SCAN_DIRS:
        root = REPO / rel
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SCAN_SUFFIXES:
                continue
            if path.name in ALLOWLIST_NAMES:
                continue
            yield path


def main() -> int:
    failures: list[str] = []

    missing = [d for d in REQUIRED_DOCS if not (REPO / d).exists()]
    for d in missing:
        failures.append(f"missing required doc: {d}")

    scanned = 0
    for path in _iter_files():
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = path.relative_to(REPO)
        for lineno, raw in enumerate(text.splitlines(), start=1):
            line = raw.lower()
            for phrase in ALWAYS_FORBIDDEN:
                if phrase.lower() in line:
                    failures.append(f"forbidden claim '{phrase}' in {rel}:{lineno}")
            if not _has_negation(line):
                for phrase in DUAL_USE:
                    if phrase.lower() in line:
                        failures.append(f"forbidden claim '{phrase}' in {rel}:{lineno}")

    docs_ok = not missing
    claims_ok = not any(f.startswith("forbidden claim") for f in failures)

    print(f"POSITIONING_DOCS_PASS={'true' if docs_ok else 'false'}")
    print(f"POSITIONING_CLAIMS_PASS={'true' if claims_ok else 'false'}")
    print(f"POSITIONING_FILES_SCANNED={scanned}")

    if failures:
        print("POSITIONING_PASS=false")
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("POSITIONING_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
