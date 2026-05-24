#!/usr/bin/env python3
"""
verify_prompt_output_quality.py — scan founder-facing artifacts for
banned claim phrases (guaranteed/100%/ROI/قطعي/مضمون/...) and any
revenue/sales/meetings guarantee patterns.

Scopes the scan to the NEW Founder Console surface only (so we do not
regress on pre-existing landing/* warnings which v10 already tracks
separately). Existing landing/* sweep stays under v10_master_verify.sh.

Exit: 0 PASS / 1 FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Scope: NEW Founder Console surface only.
# Pre-existing docs (docs/ops/*, landing/*, etc.) have their own sweeps
# under v10_master_verify.sh and verify_no_guaranteed_claims tests;
# rescanning them here would create a noisy false-positive trail because
# doctrine docs intentionally quote banned phrases as negative examples.
SCAN_DIRS = [
    ROOT / "apps" / "web" / "app" / "ceo",
    ROOT / "apps" / "web" / "app" / "capital-allocation",
    ROOT / "apps" / "web" / "app" / "market-attack",
    ROOT / "apps" / "web" / "app" / "ai-governance",
    ROOT / "apps" / "web" / "app" / "trust",
    ROOT / "apps" / "web" / "app" / "audit",
    ROOT / "apps" / "web" / "lib",
    ROOT / "apps" / "web" / "components",
    ROOT / "docs" / "market_attack",
    ROOT / "policies",
    ROOT / "registries",
    ROOT / "evals" / "gates",
]

BANNED = [
    (re.compile(r"\bguaranteed\b", re.I), "guaranteed"),
    (re.compile(r"\b100\s*%\s*(?:roi|return|growth|cash|revenue|leads?)\b", re.I), "100% claim"),
    (re.compile(r"\b(?:roi|return)\s+of\s+\d", re.I), "ROI-of-N"),
    (re.compile(r"\brevenue\s+of\s+\d", re.I), "revenue-of-N"),
    (re.compile(r"\bمضمون\b"), "مضمون"),
    (re.compile(r"\bقطعي\b"), "قطعي"),
    (re.compile(r"\bنضمن\b"), "نضمن"),
    (re.compile(r"\bنعد\s+ب\w*", re.I), "نعد-بـ"),
]


def main() -> int:
    failures: list[str] = []
    files_scanned = 0
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".tsx", ".ts", ".md", ".yaml", ".yml"}:
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            files_scanned += 1
            for pattern, label in BANNED:
                m = pattern.search(text)
                if m:
                    # Doctrine docs may quote the banned phrase as a NEGATIVE
                    # example. Allow when it appears inside an obvious "must
                    # not" / "ban" / "forbidden" context within 60 chars.
                    start = max(0, m.start() - 60)
                    window = text[start:m.end()].lower()
                    safe = any(
                        kw in window
                        for kw in ("forbidden", "banned", "must not", "no_", "block", "refuse", "حظر", "ممنوع", "يُرفض")
                    )
                    if safe:
                        continue
                    rel = p.relative_to(ROOT)
                    failures.append(f"{rel}: banned `{label}` near `{m.group(0)[:40]}`")

    verdict = "PASS" if not failures else "FAIL"
    print(f"PROMPT_OUTPUT_QUALITY={verdict.lower()}")
    print(f"PROMPT_OUTPUT_QUALITY_FILES_SCANNED={files_scanned}")
    print(f"PROMPT_OUTPUT_QUALITY_FAILS={len(failures)}")
    if failures:
        print("\n## Prompt Output Quality FAILURES")
        for f in failures[:50]:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
