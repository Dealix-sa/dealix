from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "ledgers"
REPORTS = ROOT / "reports" / "collections"


def load_json(name: str, default):
    path = DATA / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_prospects(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("prospects", "leads", "items"):
            if isinstance(data.get(key), list):
                return data[key]
    return []


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    prospects = normalize_prospects(load_json("prospects.json", []))

    proposals = [
        p for p in prospects
        if p.get("status") in {"proposal_sent", "details_sent", "call_booked", "replied_interested"}
    ]

    lines = [
        "# Proposal to Payment Plan",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Objective",
        "",
        "Convert proposal/interested leads into payment requests or clear lost/nurture reasons.",
        "",
        "| Company | Status | Offer | Amount | Action | Command |",
        "|---|---|---|---:|---|---|",
    ]

    for p in proposals:
        company = p.get("company", "")
        status = p.get("status", "")
        offer = p.get("offer", "ai-trust")
        amount = p.get("value") or p.get("amount") or 5000

        if status == "proposal_sent":
            action = "Start paid delivery / payment request"
            cmd = f'.\\scripts\\start_paid_delivery.ps1 -Client "{company}" -Offer "{offer}" -Amount "{amount}"'
        elif status in {"details_sent", "call_booked", "replied_interested"}:
            action = "Generate proposal first"
            cmd = f'py -3 .\\scripts\\proposal_from_lead.py "{company}"'
        else:
            action = "Review"
            cmd = "—"

        lines.append(f"| {company} | {status} | {offer} | {amount} | {action} | `{cmd}` |")

    lines += [
        "",
        "## Founder Rule",
        "",
        "Do not create more new leads until these proposal/interested leads are moved forward or closed.",
    ]

    out = REPORTS / f"proposal-to-payment-plan-{time.strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"PROPOSAL_TO_PAYMENT_PLAN={out}")
    print(f"PROPOSAL_CANDIDATES={len(proposals)}")
    print("PROPOSAL_TO_PAYMENT_PLAN=PASS")


if __name__ == "__main__":
    main()
