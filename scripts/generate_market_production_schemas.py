#!/usr/bin/env python3
"""Generate JSON Schema files for Market Production OS value objects.

Run from the repo root:  python3 scripts/generate_market_production_schemas.py

Writes ``schemas/<name>.schema.json`` for prospect, outreach_draft,
job_signal, company_signal, reply, sending_batch, suppression,
approval_action, and email_account. Kept as a generator so the schemas
stay in lockstep with ``auto_client_acquisition/market_production_os/schemas.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

_BASE = "https://dealix.sa/schemas"

PROSPECT_STATES = [
    "researched", "qualified", "draft_ready", "drafted", "approved", "sent",
    "replied", "meeting_booked", "proposal_needed", "proposal_sent", "won",
    "lost", "nurture", "do_not_contact",
]
DRAFT_KINDS = ["first_touch", "follow_up_1", "follow_up_2", "proposal_intro", "close_loop"]
SEND_STATUS = ["draft", "queued", "sent", "suppressed", "bounced"]
APPROVAL_STATUS = ["pending", "approved", "rejected", "rewrite", "nurture", "do_not_contact"]
COMPLIANCE_STATUS = ["pending", "passed", "failed"]
RISK = ["low", "medium", "high"]
REPLY_CLASSES = [
    "positive", "interested_later", "price_question", "send_more_info",
    "wrong_person", "not_interested", "unsubscribe", "angry", "auto_reply", "bounce",
]
SIGNAL_KINDS = ["job_posting", "website", "content", "campaign_launch", "careers_page"]
APPROVAL_DECISIONS = [
    "approve", "reject", "rewrite", "shorten", "make_formal", "change_offer",
    "move_to_nurture", "do_not_contact",
]


def _schema(name: str, title: str, props: dict, required: list[str]) -> dict:
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f"{_BASE}/{name}.schema.json",
        "title": title,
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": props,
    }


def _str(desc: str = "", enum: list[str] | None = None) -> dict:
    d: dict = {"type": "string"}
    if desc:
        d["description"] = desc
    if enum:
        d["enum"] = enum
    return d


SCHEMAS: dict[str, dict] = {
    "prospect": _schema(
        "prospect", "Prospect",
        {
            "prospect_id": _str("Stable unique id"),
            "company": _str(),
            "sector": _str(),
            "recipient_role": _str(),
            "source": _str("Declared lawful source. Forbidden: scraping, purchased_list, cold_whatsapp, linkedin_automation."),
            "region": _str(),
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "state": _str("Lifecycle state", PROSPECT_STATES),
            "notes": _str(),
            "created_at": _str("ISO-8601"),
        },
        ["prospect_id", "company", "sector", "source"],
    ),
    "outreach_draft": _schema(
        "outreach_draft", "OutreachDraft",
        {
            "draft_id": _str(),
            "prospect_id": _str(),
            "company": _str(),
            "sector": _str(),
            "recipient_role": _str(),
            "source": _str(),
            "kind": _str("Draft kind", DRAFT_KINDS),
            "pain_hypothesis": _str(),
            "personalization_note": _str(),
            "personalization_level": {"type": "integer", "minimum": 0, "maximum": 4, "description": "P0..P4; below P1 is rejected"},
            "offer": _str("Must map to exactly one catalog offer"),
            "subject": _str(),
            "body": _str(),
            "cta": _str(),
            "language": _str("", ["ar", "en"]),
            "evidence_level": {"type": "integer", "minimum": 0, "maximum": 5, "description": "L0..L5"},
            "unsubscribe_included": {"type": "boolean"},
            "risk_level": _str("", RISK),
            "compliance_status": _str("", COMPLIANCE_STATUS),
            "approval_status": _str("", APPROVAL_STATUS),
            "send_status": _str("Factory always sets 'draft'", SEND_STATUS),
            "governance_decision": _str("Set by the quality gate; never empty/PENDING after gating"),
            "gate_reasons": {"type": "array", "items": {"type": "string"}},
            "created_at": _str("ISO-8601"),
        },
        ["draft_id", "prospect_id", "company", "offer", "subject", "body", "send_status", "governance_decision"],
    ),
    "job_signal": _schema(
        "job_signal", "JobSignal",
        {
            "signal_id": _str(),
            "company": _str(),
            "sector": _str(),
            "kind": _str("", SIGNAL_KINDS),
            "role": _str("e.g., Sales Ops, CRM Manager, Marketing Coordinator, Support"),
            "detail": _str(),
            "matched_offer": _str("Offer from the ladder this signal maps to"),
            "source": _str("Public/founder-supplied. No scraping."),
            "detected_at": _str("ISO-8601"),
        },
        ["signal_id", "company", "kind", "source"],
    ),
    "company_signal": _schema(
        "company_signal", "CompanySignal",
        {
            "signal_id": _str(),
            "company": _str(),
            "sector": _str(),
            "kind": _str("", SIGNAL_KINDS),
            "detail": _str("e.g., active careers page, campaign/service launch"),
            "matched_offer": _str(),
            "source": _str(),
            "detected_at": _str("ISO-8601"),
        },
        ["signal_id", "company", "kind", "source"],
    ),
    "reply": _schema(
        "reply", "Reply",
        {
            "reply_id": _str(),
            "draft_id": _str(),
            "prospect_id": _str(),
            "text": _str("Stored only as the founder records it; no PII in derived logs"),
            "reply_class": _str("", REPLY_CLASSES),
            "next_action": _str(),
            "suppress": {"type": "boolean", "description": "true for unsubscribe/angry/bounce"},
            "received_at": _str("ISO-8601"),
        },
        ["reply_id", "draft_id", "reply_class"],
    ),
    "sending_batch": _schema(
        "sending_batch", "SendingBatch",
        {
            "batch_id": _str(),
            "week": {"type": "integer", "minimum": 0},
            "approved_count": {"type": "integer", "minimum": 0},
            "ramp_cap": {"type": "integer", "minimum": 0, "maximum": 250},
            "planned_sends": {"type": "integer", "minimum": 0, "maximum": 250},
            "domain_health_ok": {"type": "boolean"},
            "reasons": {"type": "array", "items": {"type": "string"}},
            "created_at": _str("ISO-8601"),
        },
        ["batch_id", "week", "planned_sends", "domain_health_ok"],
    ),
    "suppression": _schema(
        "suppression", "SuppressionEntry",
        {
            "email": _str("Lowercased address that must never be contacted again"),
            "reason": _str("", ["unsubscribe", "angry", "bounce", "manual", "do_not_contact"]),
            "suppressed_at": _str("ISO-8601"),
        },
        ["email", "reason"],
    ),
    "approval_action": _schema(
        "approval_action", "ApprovalAction",
        {
            "action_id": _str(),
            "draft_id": _str(),
            "decision": _str("Founder decision", APPROVAL_DECISIONS),
            "note": _str(),
            "decided_at": _str("ISO-8601"),
        },
        ["action_id", "draft_id", "decision"],
    ),
    "email_account": _schema(
        "email_account", "EmailAccount",
        {
            "account_id": _str(),
            "from_address": _str(),
            "reply_to": _str(),
            "domain": _str(),
            "spf_ok": {"type": "boolean"},
            "dkim_ok": {"type": "boolean"},
            "dmarc_ok": {"type": "boolean"},
            "tracking_domain": _str(),
            "unsubscribe_endpoint": _str(),
            "postmaster_monitored": {"type": "boolean"},
            "warmup_week": {"type": "integer", "minimum": 0},
            "daily_send_cap": {"type": "integer", "minimum": 0, "maximum": 250},
        },
        ["account_id", "from_address", "domain", "spf_ok", "dkim_ok", "dmarc_ok"],
    ),
}


def main() -> int:
    out_dir = Path(__file__).resolve().parents[1] / "schemas"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, schema in SCHEMAS.items():
        path = out_dir / f"{name}.schema.json"
        path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(out_dir.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
