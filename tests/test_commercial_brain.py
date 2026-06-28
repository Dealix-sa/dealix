"""The Commercial Brain makes sensible, deterministic, claim-safe decisions."""

from __future__ import annotations

import pytest

from app.commercial import safety
from app.commercial.reasoning import HeuristicBrain, LLMBrain, get_brain


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.delenv("COMMERCIAL_LLM_ENABLED", raising=False)
    yield


def _ctx(**kw):
    base = {
        "account_id": "a1",
        "conversation_id": "c1",
        "motion": "sales_prospecting",
        "channel": "whatsapp",
        "stage": "opener",
        "last_intent": "",
        "icp_score": 80.0,
        "company_name": "Acme",
        "pain_hypothesis": "lead follow-up",
    }
    base.update(kw)
    return base


def test_default_brain_is_heuristic():
    assert isinstance(get_brain(), HeuristicBrain)


def test_llm_brain_when_enabled(monkeypatch):
    monkeypatch.setenv("COMMERCIAL_LLM_ENABLED", "true")
    assert isinstance(get_brain(), LLMBrain)


def test_opener_for_high_icp_is_high_priority():
    rec = HeuristicBrain().recommend_action(_ctx(icp_score=85))
    assert rec.recommended_action == "send_opener"
    assert rec.priority == 1
    assert rec.next_stage == "qualifying"
    assert rec.rationale


def test_low_icp_is_deprioritised():
    rec = HeuristicBrain().recommend_action(_ctx(icp_score=20))
    assert rec.priority >= 4


def test_interested_routes_to_booking():
    rec = HeuristicBrain().recommend_action(_ctx(last_intent="interested"))
    assert rec.recommended_action == "propose_booking"
    assert rec.next_stage == "booking"


def test_price_objection_routes_to_negotiation():
    rec = HeuristicBrain().recommend_action(_ctx(last_intent="price_objection"))
    assert rec.recommended_action == "handle_objection"
    assert rec.next_stage == "negotiation"
    assert rec.risk_level == "medium"


def test_contract_request_escalates_high_risk():
    rec = HeuristicBrain().recommend_action(_ctx(last_intent="contract_request"))
    assert rec.recommended_action == "escalate_to_founder"
    assert rec.risk_level == "high"


def test_unsubscribe_honoured_no_approval_needed():
    rec = HeuristicBrain().recommend_action(_ctx(last_intent="unsubscribe"))
    assert rec.recommended_action == "honour_optout"
    assert rec.next_stage == "opted_out"
    assert rec.requires_approval is False


def test_determinism():
    b = HeuristicBrain()
    a = b.recommend_action(_ctx(last_intent="interested"))
    c = b.recommend_action(_ctx(last_intent="interested"))
    assert a.to_dict() == c.to_dict()


def test_drafts_are_claim_safe():
    b = HeuristicBrain()
    for action in ("send_opener", "handle_objection", "propose_booking", "escalate_to_founder"):
        d = b.draft_reply(_ctx(recommended_action=action))
        assert safety.contains_blocked_claim(d["ar"]) is None
        assert safety.contains_blocked_claim(d["en"]) is None
