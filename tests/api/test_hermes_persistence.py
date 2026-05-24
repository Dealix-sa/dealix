"""Persistence tests for ApprovalQueue + EvidenceStore (Wave 2)."""

from __future__ import annotations

from pathlib import Path

from dealix.hermes.core.decisions import Decision
from dealix.hermes.core.opportunities import (
    Opportunity,
    OpportunityType,
    ScoredOpportunity,
)
from dealix.hermes.core.schemas import Money
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.trust.approvals import ApprovalQueue, ApprovalTicket
from dealix.trust.evidence import EvidenceBuilder, EvidenceStore


def test_approval_queue_round_trips_through_disk(tmp_path: Path) -> None:
    path = tmp_path / "approvals.jsonl"
    queue = ApprovalQueue(persist_path=path)
    ticket = ApprovalTicket(
        decision_id="hdec_xyz",
        plan_id="plan_xyz",
        summary="please approve me",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        evidence_pack_ref="epk_xyz",
    )
    queue.submit(ticket)
    queue.approve(ticket.ticket_id, by="sami", note="ok")

    # New queue from the same path must rehydrate the ticket + status.
    reloaded = ApprovalQueue(persist_path=path)
    recovered = reloaded.get(ticket.ticket_id)
    assert recovered.summary == "please approve me"
    assert recovered.status.value == "approved"
    assert recovered.decided_by == "sami"


def test_evidence_store_round_trips_through_disk(tmp_path: Path) -> None:
    path = tmp_path / "evidence.jsonl"
    store = EvidenceStore(persist_path=path)
    opp = Opportunity(
        signal_id="sig_per",
        opp_type=OpportunityType.REVENUE,
        title="Test opp",
        narrative="testing persistence",
        expected_value=Money.sar(7500),
    )
    scored = ScoredOpportunity(
        opportunity=opp,
        score=3.4,
        rationale="weighted",
        components={"revenue": 1.5},
    )
    decision = Decision(
        opportunity_id=opp.opp_id,
        summary="ship",
        options=["ship", "park"],
        chosen_option="ship",
        rationale="strong score",
    )
    pack = EvidenceBuilder().build_from_decision(decision, scored)
    pack_id = store.save(pack, entity_ref=opp.opp_id)

    reloaded = EvidenceStore(persist_path=path)
    recovered = reloaded.get(pack_id)
    assert recovered.decision == "ship"
    assert recovered.recommendation == "ship"
    assert opp.opp_id in [
        e
        for e in reloaded._by_entity  # type: ignore[attr-defined]
    ]
