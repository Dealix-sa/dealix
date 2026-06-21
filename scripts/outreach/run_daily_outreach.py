#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import date
from pathlib import Path

import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.outreach.policy import can_send_email, can_send_whatsapp
from app.outreach.render import (
    render_company_brief,
    render_email,
    render_whatsapp_buttons_payload,
    render_whatsapp_text,
)


ROOT = Path(__file__).resolve().parents[2]


def slugify(value: str) -> str:
    keep = []
    for ch in value.strip():
        if ch.isalnum() or ch in {"-", "_"}:
            keep.append(ch)
        elif ch.isspace():
            keep.append("-")
    return "".join(keep).strip("-") or "company"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def append_log(path: Path, row: dict[str, str]) -> None:
    exists = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as f:
        fields = [
            "date",
            "company",
            "channel",
            "contact",
            "status",
            "action",
            "reasons",
            "artifact",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", default="data/outreach/target_accounts.example.csv")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--send", action="store_true", help="Attempt live sending if env gates allow it")
    args = parser.parse_args()

    targets_path = ROOT / args.targets
    rows = read_rows(targets_path)

    outbox = ROOT / "outbox" / args.date
    report_dir = ROOT / "reports" / "outreach" / args.date
    approval_dir = ROOT / "data" / "outreach" / "approval_queue" / args.date

    outbox.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    approval_dir.mkdir(parents=True, exist_ok=True)

    summary: list[dict] = []

    for row in rows:
        company = row.get("company", "company")
        slug = slugify(company)

        email_text = render_email(row)
        whatsapp_text = render_whatsapp_text(row)
        whatsapp_payload = render_whatsapp_buttons_payload(row)
        brief_text = render_company_brief(row)

        email_file = outbox / f"{slug}_email_step1.md"
        whatsapp_file = outbox / f"{slug}_whatsapp_step1.md"
        whatsapp_json = outbox / f"{slug}_whatsapp_buttons.json"
        brief_file = report_dir / f"{slug}_one_page_brief.md"
        approval_file = approval_dir / f"{slug}_approval.json"

        email_file.write_text(email_text, encoding="utf-8")
        whatsapp_file.write_text(whatsapp_text, encoding="utf-8")
        whatsapp_json.write_text(json.dumps(whatsapp_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        brief_file.write_text(brief_text, encoding="utf-8")

        email_decision = can_send_email(row)
        whatsapp_decision = can_send_whatsapp(row)

        approval = {
            "date": args.date,
            "company": company,
            "email": row.get("email", ""),
            "phone": row.get("phone", ""),
            "source_url": row.get("source_url", ""),
            "email_allowed_now": email_decision.allowed,
            "email_reasons": email_decision.reasons,
            "whatsapp_allowed_now": whatsapp_decision.allowed,
            "whatsapp_reasons": whatsapp_decision.reasons,
            "artifacts": {
                "email": str(email_file),
                "whatsapp_text": str(whatsapp_file),
                "whatsapp_buttons_payload": str(whatsapp_json),
                "brief": str(brief_file),
            },
            "founder_decision": "pending",
        }
        approval_file.write_text(json.dumps(approval, ensure_ascii=False, indent=2), encoding="utf-8")

        summary.append(approval)

        append_log(
            ROOT / "data" / "outreach" / "send_log.csv",
            {
                "date": args.date,
                "company": company,
                "channel": "email",
                "contact": row.get("email", ""),
                "status": "drafted" if not args.send else ("allowed" if email_decision.allowed else "blocked"),
                "action": "email_step1",
                "reasons": "; ".join(email_decision.reasons),
                "artifact": str(email_file),
            },
        )

        append_log(
            ROOT / "data" / "outreach" / "send_log.csv",
            {
                "date": args.date,
                "company": company,
                "channel": "whatsapp",
                "contact": row.get("phone", ""),
                "status": "drafted" if not args.send else ("allowed" if whatsapp_decision.allowed else "blocked"),
                "action": "whatsapp_step1",
                "reasons": "; ".join(whatsapp_decision.reasons),
                "artifact": str(whatsapp_file),
            },
        )

    (report_dir / "daily_outreach_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md = [
        f"# Dealix Daily Outreach Summary — {args.date}\n",
        f"Targets: {len(rows)}\n\n",
        "## Safety\n\n",
        "- Email send requires EMAIL_SEND_ENABLED=true and email_opt_in=true.\n",
        "- WhatsApp send requires WHATSAPP_SEND_ENABLED=true, WHATSAPP_ALLOW_LIVE_SEND=true, and whatsapp_opt_in=true.\n",
        "- Default behavior is draft/approval queue only.\n\n",
        "## Generated artifacts\n\n",
    ]

    for item in summary:
        md.append(f"### {item['company']}\n")
        md.append(f"- Email allowed now: `{item['email_allowed_now']}` — {', '.join(item['email_reasons']) or 'ok'}\n")
        md.append(f"- WhatsApp allowed now: `{item['whatsapp_allowed_now']}` — {', '.join(item['whatsapp_reasons']) or 'ok'}\n")
        for name, path in item["artifacts"].items():
            md.append(f"- {name}: `{path}`\n")
        md.append("\n")

    (report_dir / "daily_outreach_summary.md").write_text("".join(md), encoding="utf-8")

    print(f"Generated daily outreach for {len(rows)} targets")
    print(f"Outbox: {outbox}")
    print(f"Report: {report_dir / 'daily_outreach_summary.md'}")
    print("Mode:", "send-gated" if args.send else "draft-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
