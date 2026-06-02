#!/usr/bin/env python3
"""Draft Quality Gate (Revenue Execution OS) — fails if any draft is unsafe.

Runs deterministic checks (no banned/overclaim phrases, draft-only policy, valid
evidence level, CTA present, Arabic body, length, schema) over the draft ledger
and writes reports/distribution/DRAFT_QUALITY_GATE.md. Exit code 1 on failure.

Usage:
    python scripts/check_draft_quality.py
    python scripts/check_draft_quality.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import quality  # noqa: E402
from dealix.distribution.ledger import now_iso  # noqa: E402
from dealix.distribution.paths import REPORTS_DIR  # noqa: E402


def _write_report(result: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Draft Quality Gate — بوابة جودة المسودات",
        "",
        f"- Generated: {now_iso()}",
        f"- Total: {result['total']} · Passed: {result['passed']} · Failed: {result['failed']}",
        f"- **Verdict: {'PASS' if result['ok'] else 'FAIL'}**",
        "",
    ]
    if result["failures"]:
        lines.append("## Failures")
        lines.append("")
        for f in result["failures"]:
            lines.append(f"- `{f['id']}`: {', '.join(f['errors'])}")
        lines.append("")
    (REPORTS_DIR / "DRAFT_QUALITY_GATE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Draft quality gate.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-persist", action="store_true", help="Do not annotate the ledger.")
    args = p.parse_args(argv)

    result = quality.run_quality_gate(persist=not args.no_persist)
    _write_report(result)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        verdict = "PASS" if result["ok"] else "FAIL"
        print(f"DRAFT_QUALITY_GATE={verdict} ({result['passed']}/{result['total']} passed)")
        for f in result["failures"]:
            print(f"  - {f['id']}: {', '.join(f['errors'])}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DRAFT_QUALITY_GATE: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
