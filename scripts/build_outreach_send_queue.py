#!/usr/bin/env python3
"""build_outreach_send_queue.py — Compile an APPROVED-only send queue.

Reads the batch CSV and only includes rows where:
    - approval_status == "Approved"
    - verification_status == "URL_VERIFIED"
    - public website is filled
    - the lead appears in contact_discovery_queue.csv with a recorded path

Output is a markdown checklist the founder uses to create Gmail drafts
manually. No auto-send. Default channel: "Manual/Gmail Draft".
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_contact_paths() -> dict[str, dict[str, str]]:
    path = REPO_ROOT / "acquisition" / "contact_discovery_queue.csv"
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["company"]: row for row in csv.DictReader(handle)}


def build_queue(batch_path: Path, channel: str) -> int:
    if not batch_path.exists():
        print(f"batch missing: {batch_path}", file=sys.stderr)
        return 1
    with batch_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    contacts = load_contact_paths()
    eligible: list[dict[str, str]] = []
    skipped: list[tuple[str, str]] = []
    for row in rows:
        if row.get("approval_status") != "Approved":
            skipped.append((row["company"], "not approved"))
            continue
        if row.get("verification_status") != "URL_VERIFIED":
            skipped.append((row["company"], "url not verified"))
            continue
        if not row.get("website"):
            skipped.append((row["company"], "no website"))
            continue
        contact_row = contacts.get(row["company"])
        if not contact_row or not contact_row.get("contact_found"):
            skipped.append((row["company"], "no contact path recorded"))
            continue
        eligible.append({**row, "contact": contact_row.get("contact_found", "")})
    out_dir = REPO_ROOT / "acquisition" / "send_queues"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{batch_path.stem}.md"
    lines = [
        f"# Send Queue — {batch_path.stem}",
        "",
        f"Channel: **{channel}** (founder creates drafts manually).",
        "",
        f"Eligible: {len(eligible)}. Skipped: {len(skipped)}.",
        "",
        "## To Draft (check each box after the Gmail draft is created)",
        "",
    ]
    for row in eligible:
        lines.append(
            f"- [ ] **{row['company']}** — {row.get('contact', '')} — "
            f"msg `{row.get('suggested_message_id', '')}` — "
            f"website {row.get('website', '')}"
        )
    if skipped:
        lines.extend(["", "## Skipped", ""])
        for company, reason in skipped:
            lines.append(f"- {company}: {reason}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote send queue: {out_path}")
    print(f"  eligible: {len(eligible)}  skipped: {len(skipped)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to batch CSV.")
    parser.add_argument("--channel", default="Manual/Gmail Draft")
    args = parser.parse_args()
    return build_queue(Path(args.file), args.channel)


if __name__ == "__main__":
    sys.exit(main())
