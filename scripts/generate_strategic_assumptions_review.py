#!/usr/bin/env python3
"""generate_strategic_assumptions_review.py.

Surface strategic assumptions that need attention: overdue for review,
low-confidence with no evidence_required, or recently invalidated.

Reads the markdown register at docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md.
The register format is a sequence of subsections of the form:

    ### ASM-YYYYMMDD-NN

    - **assumption_en:** ...
    - **confidence:** low|med|high
    - **evidence_required:** ...
    - **owner:** ...
    - **review_date:** YYYY-MM-DD
    - **status:** open|validated|invalidated|retired
    - **linked_decision:** ...
    - **closed_at:** YYYY-MM-DD or "-"

Read-only. Never sends to any external system. No writes unless --out given.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTER = REPO_ROOT / "docs" / "founder" / "STRATEGIC_ASSUMPTIONS_REGISTER.md"

ID_HEADER_RE = re.compile(r"^###\s+(ASM-\d{8}-\d+)\s*$")
FIELD_RE = re.compile(r"^\-\s*\*\*([a-z_]+):\*\*\s*(.*)$")

KNOWN_FIELDS = {
    "assumption_en",
    "assumption_ar",
    "confidence",
    "evidence_required",
    "owner",
    "review_date",
    "status",
    "linked_decision",
    "closed_at",
}


def parse_register(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        header_match = ID_HEADER_RE.match(line)
        if header_match:
            if current is not None:
                rows.append(current)
            current = {"id": header_match.group(1)}
            continue
        if current is None:
            continue
        field_match = FIELD_RE.match(line.strip())
        if field_match:
            key = field_match.group(1).strip()
            value = field_match.group(2).strip()
            if key in KNOWN_FIELDS:
                current[key] = value
    if current is not None:
        rows.append(current)
    return rows


def _parse_date(value: str | None) -> date | None:
    if not value or value in {"-", "—", ""}:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _is_empty(value: str | None) -> bool:
    if value is None:
        return True
    stripped = value.strip()
    return stripped == "" or stripped in {"-", "—"}


def find_overdue(rows: list[dict[str, Any]], as_of: date) -> list[dict[str, Any]]:
    overdue = []
    for row in rows:
        if (row.get("status") or "").lower() != "open":
            continue
        review = _parse_date(row.get("review_date"))
        if review is None:
            continue
        if review < as_of:
            overdue.append(row)
    return overdue


def find_low_confidence_no_evidence(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flagged = []
    for row in rows:
        if (row.get("status") or "").lower() != "open":
            continue
        if (row.get("confidence") or "").lower() != "low":
            continue
        if _is_empty(row.get("evidence_required")):
            flagged.append(row)
    return flagged


def find_recently_invalidated(
    rows: list[dict[str, Any]], as_of: date, window_days: int = 30,
) -> list[dict[str, Any]]:
    cutoff = as_of - timedelta(days=window_days)
    flagged = []
    for row in rows:
        if (row.get("status") or "").lower() != "invalidated":
            continue
        closed = _parse_date(row.get("closed_at"))
        if closed is None:
            continue
        if cutoff <= closed <= as_of:
            flagged.append(row)
    return flagged


def _summary_line(row: dict[str, Any]) -> str:
    rid = row.get("id", "?")
    assumption = (row.get("assumption_en") or "").strip()
    confidence = row.get("confidence", "?")
    review = row.get("review_date", "?")
    return f"- {rid} | confidence={confidence} | review_date={review} | {assumption}"


def render_report(
    rows: list[dict[str, Any]],
    overdue: list[dict[str, Any]],
    low_conf: list[dict[str, Any]],
    invalidated: list[dict[str, Any]],
    as_of: date,
) -> str:
    lines: list[str] = []
    lines.append(f"# Strategic assumptions review - as of {as_of.isoformat()}")
    lines.append("")
    lines.append(f"Total assumptions in register: {len(rows)}")
    lines.append("")
    lines.append("## Overdue for review (status=open, review_date in the past)")
    lines.append("")
    if overdue:
        for row in overdue:
            lines.append(_summary_line(row))
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Low confidence with no evidence_required filled in")
    lines.append("")
    if low_conf:
        for row in low_conf:
            lines.append(_summary_line(row))
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Invalidated in the last 30 days")
    lines.append("")
    if invalidated:
        for row in invalidated:
            lines.append(_summary_line(row))
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Disclosure")
    lines.append("")
    lines.append("Estimated value is not Verified value.")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review strategic assumptions for overdue/weak/invalidated rows.",
    )
    parser.add_argument("--out", type=Path, default=None, help="Output file path.")
    parser.add_argument(
        "--register",
        type=Path,
        default=DEFAULT_REGISTER,
        help="Path to STRATEGIC_ASSUMPTIONS_REGISTER.md.",
    )
    parser.add_argument(
        "--as-of",
        dest="as_of",
        type=str,
        default=None,
        help="ISO date YYYY-MM-DD used as 'today' (default: today).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    register_path: Path = args.register
    if not register_path.exists():
        print(
            f"register not initialized yet at {register_path}. "
            "Create it before running this review.",
        )
        return 0

    if args.as_of is None:
        as_of = date.today()
    else:
        try:
            as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date()
        except ValueError:
            print(f"error: invalid --as-of value: {args.as_of!r} (expected YYYY-MM-DD)", file=sys.stderr)
            return 2

    text = register_path.read_text()
    rows = parse_register(text)
    overdue = find_overdue(rows, as_of)
    low_conf = find_low_confidence_no_evidence(rows)
    invalidated = find_recently_invalidated(rows, as_of)
    report = render_report(rows, overdue, low_conf, invalidated, as_of)

    if args.out is None:
        sys.stdout.write(report)
        if not report.endswith("\n"):
            sys.stdout.write("\n")
        return 0

    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
