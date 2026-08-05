#!/usr/bin/env python3
"""generate_founder_leverage_report.py.

Emit a weekly founder-leverage markdown report summarizing where founder hours
went and what could have been delegated.

Read-only by default. Writes only when an explicit --out is provided OR when
the input template needs to be seeded (in which case the template path is
inside the repo's data/ directory).
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "founder_time_audit.csv"
DEFAULT_OUT_DIR = REPO_ROOT / "data" / "founder_leverage"

CSV_HEADER = ["date", "category", "hours", "activity", "delegable_yes_no"]

TEMPLATE_ROWS = [
    ["2026-01-01", "sales_calls", "2.0", "discovery call", "no"],
    ["2026-01-01", "admin", "1.0", "expense reconciliation", "yes"],
    ["2026-01-02", "product", "3.5", "spec review", "no"],
]


def _iso_week_of(d: date) -> str:
    year, week, _ = d.isocalendar()
    return f"{year}-{week:02d}"


def _parse_iso_week(token: str) -> tuple[int, int]:
    parts = token.split("-")
    if len(parts) != 2:
        raise ValueError(f"invalid --week value: {token!r} (expected YYYY-WW)")
    return int(parts[0]), int(parts[1])


def _row_in_week(row_date: str, year: int, week: int) -> bool:
    try:
        d = datetime.strptime(row_date, "%Y-%m-%d").date()
    except ValueError:
        return False
    ry, rw, _ = d.isocalendar()
    return ry == year and rw == week


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(CSV_HEADER)
        for row in TEMPLATE_ROWS:
            writer.writerow(row)


def load_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append({k: (v or "").strip() for k, v in raw.items()})
    return rows


def _safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


REVENUE_DIRECT_CATEGORIES = {
    "sales_calls",
    "client_delivery",
    "proof_pack",
    "retention",
}


def build_report(rows: Iterable[dict[str, str]], iso_week: str) -> str:
    rows = list(rows)
    if not rows:
        return (
            f"# Founder leverage report - week {iso_week}\n\n"
            "No rows for this ISO week.\n"
        )

    hours_by_cat: dict[str, float] = defaultdict(float)
    delegable_hours = 0.0
    non_delegable_hours = 0.0
    activity_hours: dict[str, float] = defaultdict(float)
    activity_delegable: dict[str, str] = {}

    for r in rows:
        hours = _safe_float(r.get("hours", "0"))
        cat = r.get("category", "uncategorized") or "uncategorized"
        act = r.get("activity", "(unspecified)") or "(unspecified)"
        deleg = (r.get("delegable_yes_no", "") or "").lower()

        hours_by_cat[cat] += hours
        activity_hours[act] += hours
        activity_delegable[act] = deleg
        if deleg == "yes":
            delegable_hours += hours
        elif deleg == "no":
            non_delegable_hours += hours

    total_hours = sum(hours_by_cat.values())
    delegation_ratio = (
        delegable_hours / total_hours if total_hours > 0 else 0.0
    )

    # leverage = non-delegable (founder-only) activities; rank by hours desc
    leverage_acts = sorted(
        ((a, h) for a, h in activity_hours.items() if activity_delegable.get(a) == "no"),
        key=lambda x: x[1],
        reverse=True,
    )[:3]
    non_leverage_acts = sorted(
        ((a, h) for a, h in activity_hours.items() if activity_delegable.get(a) == "yes"),
        key=lambda x: x[1],
        reverse=True,
    )[:3]

    anti_bottleneck = []
    for cat, hrs in hours_by_cat.items():
        if total_hours > 0 and (hrs / total_hours) > 0.40 and cat not in REVENUE_DIRECT_CATEGORIES:
            pct = (hrs / total_hours) * 100
            anti_bottleneck.append((cat, hrs, pct))

    lines: list[str] = []
    lines.append(f"# Founder leverage report - week {iso_week}")
    lines.append("")
    lines.append(f"Total hours logged: {total_hours:.2f}")
    lines.append(f"Delegation ratio (delegable / total): {delegation_ratio:.2%}")
    lines.append("")
    lines.append("## Hours by category")
    lines.append("")
    lines.append("| Category | Hours | Share |")
    lines.append("|---|---:|---:|")
    for cat, hrs in sorted(hours_by_cat.items(), key=lambda x: x[1], reverse=True):
        share = (hrs / total_hours) if total_hours > 0 else 0.0
        lines.append(f"| {cat} | {hrs:.2f} | {share:.2%} |")
    lines.append("")
    lines.append("## Top 3 leverage activities (founder-only)")
    lines.append("")
    if leverage_acts:
        for a, h in leverage_acts:
            lines.append(f"- {a} ({h:.2f}h)")
    else:
        lines.append("- (none flagged as founder-only)")
    lines.append("")
    lines.append("## Top 3 non-leverage activities (delegable)")
    lines.append("")
    if non_leverage_acts:
        for a, h in non_leverage_acts:
            lines.append(f"- {a} ({h:.2f}h)")
    else:
        lines.append("- (none flagged as delegable)")
    lines.append("")
    lines.append("## Anti-bottleneck signals")
    lines.append("")
    if anti_bottleneck:
        for cat, hrs, pct in anti_bottleneck:
            lines.append(
                f"- Category '{cat}' consumed {hrs:.2f}h ({pct:.1f}%) of the week"
                " and is not revenue-direct."
            )
    else:
        lines.append("- None detected.")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a weekly founder-leverage markdown report.",
    )
    parser.add_argument("--out", type=Path, default=None, help="Output file path.")
    parser.add_argument(
        "--week",
        type=str,
        default=None,
        help="ISO week in YYYY-WW form (default current week).",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Input CSV path.",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=True,
        help="Print to stdout instead of writing (default).",
    )
    parser.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        help="Allow writing the report to --out.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.week is None:
        iso_week = _iso_week_of(date.today())
    else:
        try:
            year, week = _parse_iso_week(args.week)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        iso_week = f"{year}-{week:02d}"

    input_path: Path = args.input
    if not input_path.exists():
        write_template(input_path)
        print(
            f"Input CSV not found. Template seeded at {input_path}. "
            "Populate it and re-run.",
        )
        return 0

    rows = load_rows(input_path)
    year, week = _parse_iso_week(iso_week)
    week_rows = [r for r in rows if _row_in_week(r.get("date", ""), year, week)]
    report = build_report(week_rows, iso_week)

    if args.dry_run or args.out is None:
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
