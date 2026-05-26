from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "ledgers"
REPORTS = ROOT / "reports" / "revenue_lock"


def load_json(name: str, default):
    path = DATA / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_list(data, key: str = ""):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if key and isinstance(data.get(key), list):
            return data[key]
        for k, v in data.items():
            if isinstance(v, list):
                return v
    return []


def money(x) -> str:
    try:
        return f"SAR {float(x):,.2f}"
    except Exception:
        return "SAR 0.00"


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    prospects = normalize_list(load_json("prospects.json", []), "prospects")
    revenue = normalize_list(load_json("revenue_ledger.json", []), "entries")
    delivery = normalize_list(load_json("delivery_ledger.json", []), "deliveries")

    status_counts = Counter(p.get("status", "unknown") for p in prospects)

    proposal_leads = [
        p for p in prospects
        if p.get("status") in {"proposal_sent", "details_sent", "call_booked", "replied_interested"}
    ]

    invoice_leads = [
        p for p in prospects
        if p.get("status") in {"invoice_sent", "paid"}
    ]

    invoice_entries = [e for e in revenue if e.get("status") in {"invoice_sent", "proposed"}]
    paid_entries = [e for e in revenue if e.get("status") in {"paid", "collected", "won"}]

    proposed_amount = sum(float(e.get("amount", 0)) for e in invoice_entries)
    paid_amount = sum(float(e.get("amount", 0)) for e in paid_entries)

    active_delivery = [
        d for d in delivery
        if d.get("status") not in {"complete", "cancelled"}
    ]

    if invoice_entries:
        next_action = "FOLLOW_UP_INVOICES"
        next_command = "Open reports/collections and send payment follow-ups manually."
    elif proposal_leads:
        next_action = "CREATE_PAYMENT_REQUESTS"
        next_command = 'For each qualified proposal: .\\scripts\\start_paid_delivery.ps1 -Client "Client Name" -Offer "ai-trust" -Amount "5000"'
    elif active_delivery:
        next_action = "COMPLETE_DELIVERY_AND_PROOF"
        next_command = '.\\scripts\\complete_delivery.ps1 -Client "Client Name" -Offer "ai-trust"'
    else:
        next_action = "SEND_MORE_OUTREACH"
        next_command = ".\\scripts\\dealix-operator-day.ps1"

    lines = [
        "# Revenue Execution Lock Dashboard",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"## Next Action: {next_action}",
        "",
        "```powershell",
        next_command,
        "```",
        "",
        "## Revenue",
        "",
        f"- Proposed / invoice pipeline: {money(proposed_amount)}",
        f"- Paid / collected / won: {money(paid_amount)}",
        f"- Invoice/payment entries: {len(invoice_entries)}",
        f"- Paid entries: {len(paid_entries)}",
        "",
        "## Funnel",
        "",
        f"- Proposal / interested leads: {len(proposal_leads)}",
        f"- Invoice / paid leads: {len(invoice_leads)}",
        f"- Active deliveries: {len(active_delivery)}",
        "",
        "## Lead Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]

    for k, v in status_counts.most_common():
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "## Proposal / Collection Candidates",
        "",
        "| Company | Sector | Offer | Status | Suggested Move |",
        "|---|---|---|---|---|",
    ]

    for p in proposal_leads[:30]:
        company = p.get("company", "")
        offer = p.get("offer", "ai-trust")
        status = p.get("status", "")
        sector = p.get("sector", "")
        move = "create payment request" if status == "proposal_sent" else "convert to proposal/payment"
        lines.append(f"| {company} | {sector} | {offer} | {status} | {move} |")

    lines += [
        "",
        "## CEO Rule",
        "",
        "No new build until every proposal_sent lead has either: payment request, follow-up, lost reason, or nurture status.",
    ]

    out = REPORTS / f"revenue-lock-dashboard-{time.strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"REVENUE_LOCK_DASHBOARD={out}")
    print(f"REVENUE_LOCK_NEXT_ACTION={next_action}")
    print("REVENUE_LOCK_DASHBOARD=PASS")


if __name__ == "__main__":
    main()
