"""Proof ledger for safe internal Dealix runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class ProofEvent:
    event_type: str
    entity_id: str
    evidence: str
    source: str = "company_os_foundation"
    risk_level: str = "low"
    external_action_enabled: bool = False
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if not payload["created_at"]:
            payload["created_at"] = datetime.now(UTC).isoformat()
        return payload


def build_proof_log(
    *,
    opportunities: list[dict[str, Any]],
    drafts: list[dict[str, Any]],
    approvals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for opp in opportunities:
        events.append(
            ProofEvent(
                event_type="opportunity_scored",
                entity_id=opp["id"],
                evidence=f"score={opp['score']} reason={opp['reason']}",
            ).to_dict()
        )
    for draft in drafts:
        events.append(
            ProofEvent(
                event_type="draft_created",
                entity_id=draft["draft_id"],
                evidence="message draft generated in draft-only mode",
            ).to_dict()
        )
    for approval in approvals:
        events.append(
            ProofEvent(
                event_type="approval_required",
                entity_id=approval["approval_id"],
                evidence="founder review required before external action",
            ).to_dict()
        )
    return events
