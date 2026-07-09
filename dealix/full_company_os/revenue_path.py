"""Revenue path controls for the first paid Dealix client.

This module models a manual, evidence-first close path. It never captures
payments and never sends invoices. It only validates whether a provided event
chain is allowed to be considered revenue-ready.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

REQUIRED_FIRST_PAID_SEQUENCE = (
    "lead_selected",
    "offer_drafted",
    "founder_approved",
    "offer_sent_manually",
    "payment_instruction_approved",
    "invoice_sent",
    "payment_received",
    "work_started",
    "proof_pack_delivered",
    "closed_won",
)

REVENUE_RECOGNITION_EVENT = "payment_received"
PROOF_DELIVERY_EVENT = "proof_pack_delivered"

FORBIDDEN_REVENUE_LANGUAGE = (
    "live charge enabled",
    "auto charge enabled",
    "guaranteed revenue",
    "guaranteed roi",
    "payment received assumed",
    "fake payment",
    "fake proof",
)


@dataclass(slots=True)
class RevenueEvent:
    event_type: str
    actor: str
    evidence: str
    source: str
    amount_sar: int | None = None
    timestamp: str = ""

    def normalized(self) -> "RevenueEvent":
        if self.timestamp:
            return self
        return RevenueEvent(
            event_type=self.event_type,
            actor=self.actor,
            evidence=self.evidence,
            source=self.source,
            amount_sar=self.amount_sar,
            timestamp=datetime.now(UTC).isoformat(),
        )


@dataclass(slots=True)
class RevenuePathStatus:
    status: str
    can_count_revenue: bool
    can_mark_closed_won: bool
    next_required_event: str | None
    missing_events: list[str]
    evidence_count: int
    warnings: list[str]


def default_first_paid_events() -> list[RevenueEvent]:
    """Return safe example events that stop before real payment.

    This prevents accidental fake revenue recognition while giving the founder a
    concrete template for the manual close path.
    """

    return [
        RevenueEvent(
            event_type="lead_selected",
            actor="founder",
            evidence="Founder selected a warm/manual candidate for a 499 SAR Revenue Proof Sprint.",
            source="data/commercial/examples/first_paid_client_event.example.json",
        ).normalized(),
        RevenueEvent(
            event_type="offer_drafted",
            actor="dealix_full_company_os",
            evidence="Draft one-page 499 SAR Revenue Proof Sprint offer created for founder review.",
            source="scripts/commercial/run_first_paid_client_path.py",
        ).normalized(),
        RevenueEvent(
            event_type="founder_approved",
            actor="founder",
            evidence="Founder approval placeholder. Replace with actual approval note before manual send.",
            source="manual_review_required",
        ).normalized(),
    ]


def evaluate_revenue_path(events: list[RevenueEvent]) -> RevenuePathStatus:
    normalized = [event.normalized() for event in events]
    event_types = [event.event_type for event in normalized]
    warnings: list[str] = []
    for event in normalized:
        lowered = f"{event.event_type} {event.evidence} {event.source}".lower()
        for phrase in FORBIDDEN_REVENUE_LANGUAGE:
            if phrase in lowered:
                warnings.append(f"forbidden_revenue_language:{phrase}")
    missing = [event_type for event_type in REQUIRED_FIRST_PAID_SEQUENCE if event_type not in event_types]
    next_required = missing[0] if missing else None
    payment_received = REVENUE_RECOGNITION_EVENT in event_types
    proof_delivered = PROOF_DELIVERY_EVENT in event_types
    closed_won = "closed_won" in event_types
    can_count_revenue = payment_received and not warnings
    can_mark_closed_won = payment_received and proof_delivered and closed_won and not warnings
    if closed_won and not proof_delivered:
        warnings.append("closed_won_before_proof_pack_delivered")
    if proof_delivered and not payment_received:
        warnings.append("proof_delivered_before_payment_received")
    if any(event.amount_sar for event in normalized) and not payment_received:
        warnings.append("amount_present_without_payment_received")
    status = "closed_won_verified" if can_mark_closed_won else "revenue_verified" if can_count_revenue else "not_revenue_yet"
    return RevenuePathStatus(
        status=status,
        can_count_revenue=can_count_revenue,
        can_mark_closed_won=can_mark_closed_won,
        next_required_event=next_required,
        missing_events=missing,
        evidence_count=len(normalized),
        warnings=warnings,
    )


def load_events(path: Path) -> list[RevenueEvent]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    events = raw.get("events", raw if isinstance(raw, list) else [])
    return [RevenueEvent(**event).normalized() for event in events]


def write_revenue_path_report(events: list[RevenueEvent], output_root: Path) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    status = evaluate_revenue_path(events)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "policy": {
            "revenue_recognition_event": REVENUE_RECOGNITION_EVENT,
            "proof_delivery_event": PROOF_DELIVERY_EVENT,
            "manual_close_only": True,
            "live_charge_enabled": False,
            "auto_send_enabled": False,
        },
        "required_sequence": list(REQUIRED_FIRST_PAID_SEQUENCE),
        "events": [asdict(event.normalized()) for event in events],
        "status": asdict(status),
    }
    (output_root / "first_paid_client_path.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [
        "# Dealix First Paid Client Revenue Path",
        "",
        f"Generated: {payload['generated_at']}",
        f"Status: **{status.status}**",
        f"Can count revenue: **{status.can_count_revenue}**",
        f"Can mark closed-won: **{status.can_mark_closed_won}**",
        f"Next required event: **{status.next_required_event or 'none'}**",
        "",
        "## Events",
    ]
    for event in events:
        normalized = event.normalized()
        md.append(f"- `{normalized.event_type}` — {normalized.evidence}")
    md.extend(["", "## Missing events"])
    for item in status.missing_events:
        md.append(f"- `{item}`")
    md.extend(["", "## Warnings"])
    if status.warnings:
        for warning in status.warnings:
            md.append(f"- `{warning}`")
    else:
        md.append("- none")
    md.append("")
    (output_root / "first_paid_client_path.md").write_text("\n".join(md), encoding="utf-8")
    return payload
