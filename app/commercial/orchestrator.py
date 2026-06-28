"""Orchestrator — runs the full Commercial Growth OS pipeline.

Lead → source validation → ICP scoring → growth cards → reply classification
→ negotiation drafts → booking options → proposal briefs → follow-up tasks →
pipeline events → delivery handoffs → command-room snapshot + proof pack.

The orchestrator is pure: it takes data in and returns a result object. It
performs no network I/O and never sends anything. Persistence (writing report
files) is the caller's job — see scripts/commercial/run_commercial_growth_os.py.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from app.commercial import (
    booking_desk,
    command_snapshot,
    delivery_handoff,
    followup_engine,
    growth_cards,
    icp_scoring,
    lead_sourcing,
    negotiation_desk,
    pipeline,
    proof_pack,
    proposal_factory,
    reply_classifier,
)
from app.commercial.safety import is_safe_default_environment, safe_defaults
from app.commercial.schemas import CommandRoomSnapshot


@dataclass
class GrowthOSResult:
    accounts: list[Any] = field(default_factory=list)
    cards: list[Any] = field(default_factory=list)
    replies: list[Any] = field(default_factory=list)
    negotiation_drafts: list[Any] = field(default_factory=list)
    booking_options: list[Any] = field(default_factory=list)
    proposals: list[Any] = field(default_factory=list)
    followups: list[Any] = field(default_factory=list)
    pipeline_events: list[Any] = field(default_factory=list)
    delivery_handoffs: list[Any] = field(default_factory=list)
    snapshot: CommandRoomSnapshot | None = None
    proof: dict[str, Any] = field(default_factory=dict)
    safety_ok: bool = True
    safety_violations: list[str] = field(default_factory=list)

    @property
    def decisions_required(self) -> int:
        return len(self.snapshot.decision_queue) if self.snapshot else 0

    def counts(self) -> dict[str, int]:
        return {
            "accounts": len(self.accounts),
            "cards": len(self.cards),
            "replies": len(self.replies),
            "booking_options": len(self.booking_options),
            "proposals": len(self.proposals),
            "followups": len(self.followups),
            "decisions_required": self.decisions_required,
        }


def _validate_safety() -> tuple[bool, list[str]]:
    """The OS must run safe-by-default. Any live flag is a violation here.

    This guards the *default* run path. Controlled-live is enabled deliberately
    elsewhere via the safety gates, not by the orchestrator.
    """
    violations: list[str] = []
    s = safe_defaults()
    if not is_safe_default_environment():
        for key, val in s.items():
            if key == "outbound_mode" and val != "draft_only":
                violations.append(f"outbound_mode={val}")
            elif key != "outbound_mode" and val:
                violations.append(f"{key}=true")
    return (not violations, violations)


def run_growth_os(
    account_records: list[Mapping[str, Any]],
    reply_records: list[Mapping[str, Any]] | None = None,
    *,
    icp_rules: Mapping[str, Any] | None = None,
    client_rules: Mapping[str, Any] | None = None,
    pricing_guardrails: Mapping[str, Any] | None = None,
    enforce_safe_defaults: bool = True,
    max_proposals: int | None = 5,
) -> GrowthOSResult:
    reply_records = reply_records or []
    result = GrowthOSResult()

    safety_ok, violations = _validate_safety()
    result.safety_ok = safety_ok
    result.safety_violations = violations
    if enforce_safe_defaults and not safety_ok:
        # Surface the failure but do not build live artefacts.
        return result

    # 1–3. Source, validate, score.
    accounts = lead_sourcing.load_accounts(account_records)
    for acc in accounts:
        icp_scoring.apply_score(acc, icp_rules)
    result.accounts = accounts

    # Pipeline entry events.
    result.pipeline_events = [
        pipeline.initial_event(acc, i) for i, acc in enumerate(accounts)
    ]

    # 4. Growth cards.
    cards = growth_cards.build_cards_for_accounts(accounts, client_rules)
    result.cards = cards

    # 5–6. Replies → classify.
    replies = reply_classifier.classify_replies(reply_records)
    result.replies = replies

    # 7. Negotiation drafts.
    result.negotiation_drafts = negotiation_desk.build_negotiation_drafts(replies)

    # 8. Booking options.
    result.booking_options = booking_desk.build_booking_options(cards)

    # 9. Proposal briefs.
    result.proposals = proposal_factory.build_proposal_briefs(
        cards, pricing_guardrails, limit=max_proposals
    )

    # 10. Follow-up tasks.
    accounts_by_id = {a.account_id: a for a in accounts}
    result.followups = followup_engine.build_followups_for_cards(cards, accounts_by_id)

    # 11. Delivery handoff stubs.
    card_to_account = {c.card_id: c.account_id for c in cards}
    result.delivery_handoffs = delivery_handoff.build_delivery_handoffs(
        result.proposals, card_to_account
    )

    # 12. Command-room snapshot.
    result.snapshot = command_snapshot.build_snapshot(
        accounts=accounts,
        cards=cards,
        replies=replies,
        negotiation_drafts=result.negotiation_drafts,
        booking_options=result.booking_options,
        proposals=result.proposals,
        followups=result.followups,
        delivery_handoffs=result.delivery_handoffs,
    )

    # Proof pack.
    result.proof = proof_pack.build_proof_pack(
        accounts=accounts,
        cards=cards,
        replies=replies,
        booking_options=result.booking_options,
        proposals=result.proposals,
        followups=result.followups,
        decisions_required=result.snapshot.decision_queue,
    )
    return result


def write_reports(result: GrowthOSResult, out_dir: str | Path) -> dict[str, str]:
    """Write latest.json and latest.md. Returns the written paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    snapshot = result.snapshot
    payload = {
        "snapshot": snapshot.to_dict() if snapshot else {},
        "proof_pack": result.proof,
        "pipeline_events": [e.to_dict() for e in result.pipeline_events],
        "safety_ok": result.safety_ok,
        "safety_violations": result.safety_violations,
    }
    json_path = out / "latest.json"
    md_path = out / "latest.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(
        command_snapshot.render_markdown(snapshot) if snapshot else "# No snapshot\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "md": str(md_path)}
