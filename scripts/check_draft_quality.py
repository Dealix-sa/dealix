#!/usr/bin/env python3
"""Draft Quality Gate — scan draft bodies and fail on forbidden claims.

Reads drafts from a JSONL file (each line a JSON object with a ``body`` or
``text`` field), or from the live draft store when ``--input`` is omitted.
Writes a bilingual report to reports/distribution/DRAFT_QUALITY_GATE.md and
exits non-zero when any draft is BLOCKED — so CI can gate PRs that introduce a
guaranteed-outcome claim or forbidden-channel language.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import draft_factory, draft_quality  # noqa: E402

_REPORT = ROOT / "reports" / "distribution" / "DRAFT_QUALITY_GATE.md"


def _bodies_from_file(path: Path) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        body = str(rec.get("body") or rec.get("text") or "")
        ident = str(rec.get("id") or f"line_{i + 1}")
        if body:
            out.append((ident, body))
    return out


def _bodies_from_store() -> list[tuple[str, str]]:
    return [(d.id, d.body) for d in draft_factory.list_drafts()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, help="JSONL file of drafts (default: live draft store)"
    )
    parser.add_argument(
        "--json", action="store_true", help="print JSON instead of writing the report"
    )
    args = parser.parse_args()

    items = _bodies_from_file(args.input) if args.input else _bodies_from_store()
    results = [(ident, draft_quality.check_draft(text=body)) for ident, body in items]
    report = draft_quality.quality_gate_report([body for _, body in items])

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        lines = [
            "# Draft Quality Gate — بوابة جودة المسودات",
            "",
            f"- drafts_checked: {report['drafts_checked']}",
            f"- violations: {report['violations']}",
            f"- blocked_drafts: {report['blocked_drafts']}",
            f"- needs_edit: {report['needs_edit']}",
            f"- approved_for_review: {report['approved_for_review']}",
            "",
            "## Findings",
        ]
        if not results:
            lines.append("- (no drafts to check)")
        for ident, res in results:
            if res.issues:
                lines.append(f"- `{ident}` → **{res.decision}** — {', '.join(res.issues)}")
        _REPORT.parent.mkdir(parents=True, exist_ok=True)
        _REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {_REPORT.relative_to(ROOT)}")
        print(f"blocked_drafts={report['blocked_drafts']} needs_edit={report['needs_edit']}")

    return 1 if report["blocked_drafts"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
