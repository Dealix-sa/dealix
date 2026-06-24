#!/usr/bin/env python3
"""Generate Dealix commercial readiness report."""

from __future__ import annotations

from pathlib import Path

from app.commercial.readiness import build_founder_led_readiness_report

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "reports" / "go_live" / "COMMERCIAL_READINESS_REPORT.md"


def main() -> int:
    report = build_founder_led_readiness_report()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(report.to_markdown(), encoding="utf-8")
    print(report.verdict)
    print(OUTPUT)
    return 0 if report.is_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
