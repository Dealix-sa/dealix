#!/usr/bin/env python3
"""
os_daily_brief.py
=================
Generates the founder daily brief for the OS.
Wrapper around dealix.os_runtime.daily_brief.

Usage:
    python scripts/os_daily_brief.py
    python scripts/os_daily_brief.py --output data/daily_brief/
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.os_runtime.daily_brief import generate_brief


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix Founder Daily Brief")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for brief (default: print to stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)"
    )
    args = parser.parse_args()

    brief = generate_brief()
    today = date.today().isoformat()

    if args.format == "json":
        output = json.dumps(brief, ensure_ascii=False, indent=2)
    else:
        output = format_brief_text(brief, today)

    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        ext = "json" if args.format == "json" else "md"
        output_path = output_dir / f"{today}.{ext}"
        output_path.write_text(output, encoding="utf-8")
        print(f"Brief written to: {output_path}")
    else:
        print(output)

    return 0


def format_brief_text(brief: dict, today: str) -> str:
    lines = [
        f"# Dealix Founder Daily Brief — {today}",
        "",
        f"**Summary:** {brief.get('summary', 'No summary available')}",
        "",
        "## Top 3 Actions",
    ]
    for i, action in enumerate(brief.get("top_3_actions", []), 1):
        lines.append(f"{i}. {action}")

    lines.extend([
        "",
        "## Top Opportunities",
    ])
    for opp in brief.get("top_opportunities", []):
        lines.append(f"- {opp}")

    lines.extend([
        "",
        "## Approval Queue",
    ])
    for item in brief.get("approval_queue", []):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "---",
        "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
