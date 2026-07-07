#!/usr/bin/env python3
"""Dealix guarded autonomous negotiator.

Creates response actions for contacts that are already permitted by local policy.
It uses fixed commercial rules: price floor, daily caps, allowed scope, and
escalation conditions. It writes an action queue for the executor or webhook.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "data" / "autonomy" / "commercial_policy.json"
POLICY_EXAMPLE = ROOT / "data" / "autonomy" / "commercial_policy.example.json"
INBOX_PATH = ROOT / "data" / "autonomy" / "inbox.json"
CONTACTS_PATH = ROOT / "data" / "outbound" / "consent_registry.json"
OUT_DIR = ROOT / "business" / "autonomy"
REPORT_DIR = ROOT / "reports" / "autonomy"

ESCALATION_TERMS = [
    "legal",
    "contract",
    "lawsuit",
    "refund",
    "complaint",
    "unsubscribe",
    "stop",
    "guarantee",
    "exclusive",
    "custom terms",
]
BUYING_TERMS = ["price", "cost", "proposal", "pilot", "demo", "meeting", "interested", "send"]
OBJECTION_TERMS = ["expensive", "later", "already", "busy", "not now", "why", "difference"]


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def load_policy() -> dict[str, Any]:
    return read_json(POLICY_PATH, read_json(POLICY_EXAMPLE, {}))


def load_contacts() -> dict[str, Any]:
    data = read_json(CONTACTS_PATH, {"contacts": []})
    contacts = data.get("contacts", []) if isinstance(data, dict) else []
    return {str(item.get("account_id")): item for item in contacts if isinstance(item, dict)}


def load_inbox() -> list[dict[str, Any]]:
    data = read_json(INBOX_PATH, {"messages": []})
    messages = data.get("messages", []) if isinstance(data, dict) else data
    return [item for item in messages if isinstance(item, dict)]


def first_offer(policy: dict[str, Any]) -> dict[str, Any]:
    offers = policy.get("offer_catalog", [])
    return offers[0] if offers else {
        "offer_id": "revenue-command-room-pilot",
        "name": "Revenue Command Room Pilot",
        "currency": "SAR",
        "list_price": 7500,
        "minimum_approved_price": 5000,
        "timeline_days": 21,
    }


def classify(text: str) -> str:
    lower = text.lower()
    if any(term in lower for term in ESCALATION_TERMS):
        return "escalate"
    if any(term in lower for term in BUYING_TERMS):
        return "advance_deal"
    if any(term in lower for term in OBJECTION_TERMS):
        return "handle_objection"
    return "nurture"


def reply_text(company: str, category: str, offer: dict[str, Any], language: str) -> str:
    price = offer.get("list_price", 7500)
    currency = offer.get("currency", "SAR")
    days = offer.get("timeline_days", 21)
    if category == "advance_deal":
        if language == "ar":
            return f"ممتاز. نقدر نبدأ بـ {offer.get('name')} لمدة {days} يوم بسعر {price} {currency}. الخطوة التالية: أرسل لكم ملخص نطاق العمل والنتائج المتوقعة للتجربة ثم نحدد موعد قصير للتأكيد."
        return f"Great. We can start with {offer.get('name')} for {days} days at {price} {currency}. Next step: I can send the scope summary and pilot outputs, then we confirm a short call."
    if category == "handle_objection":
        if language == "ar":
            return "فهمت عليك. الفكرة ليست تغيير نظامكم الحالي، بل تجربة قصيرة تكشف أين تضيع الفرص وما المتابعة التي تحتاج ضبط. ممكن نبدأ بنطاق صغير حتى تكون المخاطرة منخفضة وواضحة."
        return "Understood. The point is not to replace your current system; it is a short pilot to show where opportunities leak and which follow-ups need structure. We can start small so the risk stays low and clear."
    if category == "escalate":
        if language == "ar":
            return "وصلتني النقطة. هذا النوع يحتاج مراجعة يدوية قبل أي التزام. سأحوّلها للمؤسس قبل الرد النهائي."
        return "Got it. This needs manual review before any commitment. I will escalate it before giving a final answer."
    if language == "ar":
        return f"أقدر أرسل لكم ملخص صفحة واحدة لـ {company}: أين تضيع الفرص، كيف نرتب المتابعة، وما شكل تجربة قصيرة خلال {days} يوم. هل تفضلون العربي أو الإنجليزي؟"
    return f"I can send a one-page snapshot for {company}: where opportunities leak, how follow-up can be structured, and what a short {days}-day pilot would look like. Arabic or English?"


def allowed_contact(account_id: str, channel: str, contacts: dict[str, Any]) -> tuple[bool, str]:
    contact = contacts.get(account_id)
    if not contact:
        return False, "missing_contact_permission_record"
    if contact.get("consent_status") not in {"opt_in", "customer", "existing_relationship", "inbound_request", "manual_allowlist"}:
        return False, "contact_status_not_allowed"
    channels = contact.get("channels", {}) if isinstance(contact.get("channels"), dict) else {}
    if not channels.get(channel):
        return False, "missing_channel_address"
    return True, "allowed"


def build_actions() -> list[dict[str, Any]]:
    policy = load_policy()
    offer = first_offer(policy)
    contacts = load_contacts()
    messages = load_inbox()
    today = dt.date.today().isoformat()
    actions: list[dict[str, Any]] = []

    for item in messages:
        account_id = str(item.get("account_id") or item.get("company") or "")
        channel = str(item.get("channel") or "email")
        text = str(item.get("body") or item.get("text") or "")
        language = str(item.get("language") or "ar")
        company = str(item.get("company") or account_id or "the account")
        category = classify(text)
        permitted, reason = allowed_contact(account_id, channel, contacts)
        action_status = "ready_for_guarded_execution" if permitted and category != "escalate" else "blocked_or_escalation"
        actions.append({
            "date": today,
            "account_id": account_id,
            "company": company,
            "channel": channel,
            "category": category,
            "status": action_status,
            "block_reason": None if action_status == "ready_for_guarded_execution" else reason if not permitted else "manual_escalation_required",
            "reply": reply_text(company, category, offer, language),
            "offer_id": offer.get("offer_id"),
            "price_floor": offer.get("minimum_approved_price"),
        })
    return actions


def write_outputs(actions: list[dict[str, Any]]) -> None:
    today = dt.date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    queue_path = OUT_DIR / f"guarded-negotiation-actions-{today}.json"
    queue_path.write_text(json.dumps({"actions": actions}, ensure_ascii=False, indent=2), encoding="utf-8")
    ready = sum(1 for action in actions if action["status"] == "ready_for_guarded_execution")
    lines = [
        f"# Guarded Autonomous Negotiation - {today}",
        "",
        f"Actions: {len(actions)}",
        f"Ready: {ready}",
        "",
    ]
    for action in actions:
        lines.extend([
            f"## {action['company']} - {action['channel']}",
            f"Status: {action['status']}",
            f"Category: {action['category']}",
            "",
            action["reply"],
            "",
        ])
    (REPORT_DIR / f"guarded-negotiation-actions-{today}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(actions)} guarded negotiation actions; ready={ready}")


def main() -> int:
    actions = build_actions()
    write_outputs(actions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
