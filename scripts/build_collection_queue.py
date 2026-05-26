from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "ledgers"
OUT = ROOT / "local_ai" / "collections"
REPORTS = ROOT / "reports" / "collections"


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


def safe(x: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_ " else "-" for ch in str(x)).strip().replace(" ", "-")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    prospects = normalize_list(load_json("prospects.json", []), "prospects")
    revenue = normalize_list(load_json("revenue_ledger.json", []), "entries")

    candidates = []

    for p in prospects:
        if p.get("status") in {"proposal_sent", "invoice_sent"}:
            candidates.append({
                "client": p.get("company", ""),
                "offer": p.get("offer", "ai-trust"),
                "source": "prospects",
                "status": p.get("status"),
                "amount": p.get("value") or p.get("amount") or 5000,
                "next": p.get("next_step", "follow up payment")
            })

    for e in revenue:
        if e.get("status") in {"invoice_sent", "proposed"}:
            candidates.append({
                "client": e.get("client", ""),
                "offer": e.get("offer", "ai-trust"),
                "source": "revenue_ledger",
                "status": e.get("status"),
                "amount": e.get("amount", 5000),
                "next": e.get("next_step", "confirm payment")
            })

    # De-duplicate by client/status
    seen = set()
    unique = []
    for c in candidates:
        key = (c["client"].lower(), c["status"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)

    queue_lines = [
        "# Dealix Collection Queue",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Use these manually. Do not auto-send.",
        "",
    ]

    for c in unique:
        client = c["client"] or "Client"
        amount = c["amount"] or 5000
        offer = c["offer"] or "ai-trust"
        queue_lines += [
            "---",
            "",
            f"## {client}",
            "",
            f"- Offer: {offer}",
            f"- Amount: SAR {amount}",
            f"- Current status: {c['status']}",
            f"- Source: {c['source']}",
            "",
            "### Payment follow-up draft",
            "",
            "السلام عليكم،",
            "",
            f"أرسل تذكير بسيط بخصوص عرض {offer} لـ {client}.",
            "",
            f"للبدء في التنفيذ، نحتاج تأكيد الدفعة الأولى حسب النطاق المتفق عليه. بعد التأكيد نفتح intake ونبدأ مباشرة بخطوات التشخيص والتسليم.",
            "",
            "هل مناسب نثبت البدء اليوم؟",
            "",
            "### Command after payment confirmation",
            "",
            "```powershell",
            f'.\\scripts\\confirm_payment.ps1 -Client "{client}"',
            "```",
            "",
        ]

    stamp = time.strftime("%Y%m%d-%H%M%S")
    queue_path = OUT / f"collection-queue-{stamp}.md"
    queue_path.write_text("\n".join(queue_lines), encoding="utf-8")

    report_path = REPORTS / f"collection-summary-{stamp}.md"
    report_path.write_text(
        "\n".join([
            "# Collection Summary",
            "",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"- Candidates: {len(unique)}",
            f"- Queue: {queue_path}",
            "",
            "## Rule",
            "",
            "Every proposal must become one of: invoice_sent, paid, nurture, lost.",
        ]),
        encoding="utf-8",
    )

    print(f"COLLECTION_QUEUE={queue_path}")
    print(f"COLLECTION_SUMMARY={report_path}")
    print(f"COLLECTION_CANDIDATES={len(unique)}")
    print("BUILD_COLLECTION_QUEUE=PASS")


if __name__ == "__main__":
    main()
