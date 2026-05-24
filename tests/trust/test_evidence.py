"""EvidencePack + EvidenceBuilder + EvidenceStore tests."""

from __future__ import annotations

import pytest

from dealix.hermes.core.decisions import DecisionMemoBuilder
from dealix.hermes.core.opportunities import (
    OpportunityMapper,
    ScoredOpportunity,
)
from dealix.hermes.core.signals import (
    Signal,
    SignalClassifier,
    SignalSource,
)
from dealix.trust.evidence import EvidenceBuilder, EvidencePack, EvidenceStore


def _scored_decision():
    signal = Signal(
        source=SignalSource.INBOUND_MESSAGE,
        raw_text="we'd like a proposal",
        channel="email",
    )
    cls = SignalClassifier().classify(signal)
    opp = OpportunityMapper().map(signal, cls)
    scored = ScoredOpportunity(
        opportunity=opp,
        score=3.5,
        rationale="r",
        components={"revenue": 1.0, "urgency": 4.0, "fit": 5.0, "effort_inverse": 3.0},
    )
    decision = DecisionMemoBuilder().build(scored)
    return scored, decision


def test_evidence_pack_requires_recommendation() -> None:
    with pytest.raises(Exception):
        EvidencePack(
            decision="x",
            context="y",
            opportunity_score=2.0,
            alternatives=["a", "b"],
            recommendation="",
        )


def test_evidence_pack_rejects_empty_alternatives() -> None:
    with pytest.raises(Exception):
        EvidencePack(
            decision="x",
            context="y",
            opportunity_score=2.0,
            alternatives=[],
            recommendation="do x",
        )


def test_evidence_builder_round_trip() -> None:
    scored, decision = _scored_decision()
    pack = EvidenceBuilder().build_from_decision(
        decision,
        scored,
        risk_register=["price > 25k"],
        approvals=[{"by": "sami", "ts": "now"}],
    )
    assert pack.recommendation == decision.chosen_option
    assert pack.opportunity_score == scored.score
    assert "price > 25k" in pack.risks
    assert pack.approvals[0]["by"] == "sami"


def test_evidence_store_save_and_get() -> None:
    scored, decision = _scored_decision()
    pack = EvidenceBuilder().build_from_decision(decision, scored)
    store = EvidenceStore()
    pid = store.save(pack, entity_ref="opportunity:opp_1")
    assert store.get(pid) is pack
    assert store.list_for_entity("opportunity:opp_1") == [pack]


def test_evidence_store_rejects_duplicate_save() -> None:
    scored, decision = _scored_decision()
    pack = EvidenceBuilder().build_from_decision(decision, scored)
    store = EvidenceStore()
    store.save(pack)
    with pytest.raises(ValueError):
        store.save(pack)


def test_evidence_store_unknown_pack_raises_key_error() -> None:
    store = EvidenceStore()
    with pytest.raises(KeyError):
        store.get("nope")
