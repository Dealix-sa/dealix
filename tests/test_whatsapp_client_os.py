"""WhatsApp Client OS — unit + integration tests.

Covers schemas, intent routing, readiness scan, recommendation, action cards,
permission OS, policy guard, human handoff, support triage, flows, the brain
pipeline, the JSONL stores, and metrics. Stores are redirected to a tmp path
so tests never touch real data.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.whatsapp_client_os import (
    action_cards,
    brain,
    metrics,
)
from auto_client_acquisition.whatsapp_client_os import (
    session_store as store,
)
from auto_client_acquisition.whatsapp_client_os.flows import (
    FLOWS,
    flow_for_intent,
    flows_as_data,
    next_flow,
)
from auto_client_acquisition.whatsapp_client_os.human_handoff import (
    build_handoff_brief,
    should_handoff,
)
from auto_client_acquisition.whatsapp_client_os.intent_router import classify_intent
from auto_client_acquisition.whatsapp_client_os.permission_os import (
    can_perform,
    looks_like_secret,
    required_level_for,
    requires_secure_portal,
    secret_guard,
)
from auto_client_acquisition.whatsapp_client_os.policy_guard import (
    guard_outbound,
    has_pricing_commitment,
)
from auto_client_acquisition.whatsapp_client_os.readiness_scan import (
    QUICK_TRIAGE_QUESTIONS,
    READINESS_AXES,
    quick_triage,
    score_assessment,
)
from auto_client_acquisition.whatsapp_client_os.recommendation import (
    OFFER_FREE_DIAGNOSTIC,
    OFFER_SPRINT,
    recommend_offer,
)
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ActionCard,
    FlowId,
    Intent,
    PermissionLevel,
    hash_wa_id,
    permission_rank,
)
from auto_client_acquisition.whatsapp_client_os.support_triage import triage

# Synthetic credential-shaped values, assembled from fragments so no contiguous
# secret literal exists in source (keeps secret scanners quiet) while still
# exercising the detector at runtime.
_FAKE_KEY = "sk-" + "A1B2C3D4E5F6G7H8I9J0"
_FAKE_AWS = "AKIA" + "EXAMPLE123456789"


@pytest.fixture()
def tmp_stores(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_WHATSAPP_SESSIONS_PATH", str(tmp_path / "s.jsonl"))
    monkeypatch.setenv("DEALIX_WHATSAPP_MESSAGES_PATH", str(tmp_path / "m.jsonl"))
    monkeypatch.setenv("DEALIX_WHATSAPP_CARDS_PATH", str(tmp_path / "c.jsonl"))
    monkeypatch.setenv("DEALIX_WHATSAPP_ASSESSMENTS_PATH", str(tmp_path / "a.jsonl"))
    monkeypatch.setenv("DEALIX_WHATSAPP_PERMISSIONS_PATH", str(tmp_path / "p.jsonl"))
    store.clear_for_test()
    yield
    store.clear_for_test()


# --- schemas ---------------------------------------------------------------


def test_hash_wa_id_is_stable_and_non_raw() -> None:
    h = hash_wa_id("+966500000000")
    assert h.startswith("wa_") and "966" not in h
    assert h == hash_wa_id("+966500000000")


def test_permission_rank_ordering() -> None:
    assert permission_rank(PermissionLevel.L0_CHAT_ONLY) == 0
    assert permission_rank(PermissionLevel.L5_SENSITIVE) == 5
    assert permission_rank("L3") == 3


# --- intent router ---------------------------------------------------------


def test_menu_numbers_route() -> None:
    assert classify_intent("1")[0] == Intent.START_SCAN
    assert classify_intent("6")[0] == Intent.RECOMMEND_ME
    assert classify_intent("5")[0] == Intent.REQUEST_SUPPORT


def test_recommend_me_keyword() -> None:
    assert classify_intent("ما أعرف اقترح علي")[0] == Intent.RECOMMEND_ME


def test_unsafe_outreach_blocked() -> None:
    intent, conf = classify_intent("ابغى ارسل واتساب لكل الارقام المشتراة")
    assert intent == Intent.BLOCKED_UNSAFE and conf == 1.0


def test_first_turn_welcomes() -> None:
    assert classify_intent("", is_first_turn=True)[0] == Intent.WELCOME


def test_human_request_keyword() -> None:
    assert classify_intent("ابغى اكلم شخص")[0] == Intent.REQUEST_HUMAN


# --- readiness scan + recommendation ---------------------------------------


def test_quick_triage_has_four_questions() -> None:
    assert len(QUICK_TRIAGE_QUESTIONS) == 4


def test_scan_axes_count_is_ten() -> None:
    assert len(READINESS_AXES) == 10


def test_score_assessment_full_high_readiness() -> None:
    answers = {a.id: a.options[-1].value for a in READINESS_AXES}
    asmt = score_assessment(answers=answers, company="Acme", session_id="s1")
    assert asmt.revenue_readiness >= 80
    assert asmt.risk == "low"
    assert asmt.recommended_offer_id
    assert asmt.governance_decision == GovernanceDecision.ALLOW.value


def test_score_assessment_low_readiness_recommends_diagnostic() -> None:
    answers = {a.id: a.options[0].value for a in READINESS_AXES}
    asmt = score_assessment(answers=answers, session_id="s2")
    assert asmt.risk == "high"
    assert asmt.recommended_offer_id == OFFER_FREE_DIAGNOSTIC


def test_recommend_sprint_when_leads_but_weak_followup() -> None:
    rec = recommend_offer(
        axis_scores={"lead_flow": 85, "follow_up_maturity": 30, "data_readiness": 80},
        risk="medium",
    )
    assert rec.offer_id == OFFER_SPRINT
    assert rec.plan_steps_ar


def test_quick_triage_recommends_offer() -> None:
    asmt = quick_triage(
        {"has_leads": "نعم", "biggest_problem": "المتابعة", "nearest_goal": "زيادة الردود"}
    )
    assert asmt.recommended_offer_id == OFFER_SPRINT


# --- permission OS ---------------------------------------------------------


def test_looks_like_secret_detects_token() -> None:
    assert looks_like_secret(f"my key is {_FAKE_KEY}")
    assert looks_like_secret(_FAKE_AWS)
    assert not looks_like_secret("ابغى اربط hubspot")


def test_secret_guard_routes_integration_to_portal() -> None:
    res = secret_guard("ابغى اربط hubspot")
    assert res.route_to_portal and not res.contains_secret


def test_secret_guard_flags_pasted_secret() -> None:
    res = secret_guard(f"هذا المفتاح {_FAKE_KEY}")
    assert res.contains_secret and res.route_to_portal


def test_permission_levels_and_portal() -> None:
    assert required_level_for("read_crm") == PermissionLevel.L2_CRM_READ
    assert can_perform(PermissionLevel.L3_CREATE_DRAFTS, "create_draft")
    assert not can_perform(PermissionLevel.L1_CLIENT_UPLOAD, "read_crm")
    assert requires_secure_portal("payment")


# --- policy guard ----------------------------------------------------------


def test_guard_blocks_cold_whatsapp() -> None:
    res = guard_outbound("نرسل cold whatsapp للجميع")
    assert not res.allowed and res.governance_decision == GovernanceDecision.BLOCK.value


def test_guard_blocks_secret_in_text() -> None:
    res = guard_outbound(f"المفتاح {_FAKE_KEY}")
    assert not res.allowed


def test_guard_pricing_commitment_requires_human() -> None:
    assert has_pricing_commitment("السعر النهائي هو كذا")
    res = guard_outbound("نلتزم بسعر نهائي لك")
    assert res.governance_decision == GovernanceDecision.REQUIRE_APPROVAL.value


def test_guard_allows_clean_text() -> None:
    assert guard_outbound("أهلًا، كيف أقدر أساعدك اليوم؟").allowed


# --- action cards ----------------------------------------------------------


def test_recommendation_card_options() -> None:
    asmt = score_assessment(
        answers={a.id: a.options[-1].value for a in READINESS_AXES}, session_id="s"
    )
    card = action_cards.recommendation_card("s", asmt)
    assert isinstance(card, ActionCard)
    assert {o["id"] for o in card.options} >= {"start", "book_call"}
    assert card.governance_decision == GovernanceDecision.ALLOW.value


def test_approval_card_blocks_unsafe_draft() -> None:
    card = action_cards.approval_card("s", draft_text_ar="نرسل cold whatsapp للجميع")
    assert card.governance_decision == GovernanceDecision.BLOCK.value
    assert all(o["id"] != "approve" for o in card.options)


def test_approval_card_clean_requires_approval() -> None:
    card = action_cards.approval_card("s", draft_text_ar="السلام عليكم، نتابع طلبكم.")
    assert card.governance_decision == GovernanceDecision.REQUIRE_APPROVAL.value
    assert any(o["id"] == "approve" for o in card.options)


def test_permission_card_routes_to_portal_not_text() -> None:
    card = action_cards.permission_card("s", integration="HubSpot")
    ids = {o["id"] for o in card.options}
    assert "open_portal" in ids
    assert "لا ترسل أي مفتاح" in card.body_ar


def test_proposal_card_from_catalog() -> None:
    card = action_cards.proposal_card("s", offer_id=OFFER_SPRINT)
    assert "ر.س" in card.body_ar or "Free" in card.body_en
    assert card.governance_decision == GovernanceDecision.ALLOW.value


def test_payment_card_never_charges_in_chat() -> None:
    card = action_cards.payment_handoff_card("s", offer_id=OFFER_SPRINT)
    assert "واتساب" in card.body_ar
    assert card.governance_decision == GovernanceDecision.REQUIRE_APPROVAL.value


# --- human handoff + support ----------------------------------------------


def test_handoff_on_pricing_and_legal() -> None:
    assert should_handoff("ابغى السعر النهائي").needed
    assert should_handoff("ابغى عقد قانوني").needed


def test_handoff_on_loop_limit() -> None:
    assert should_handoff("ok", turn_count=3).needed


def test_handoff_brief_high_risk_on_legal() -> None:
    brief = build_handoff_brief(
        session_id="s",
        company="X",
        reasons=("legal_contract",),
        last_text_redacted="...",
    )
    assert brief["risk"] == "high"


def test_support_triage_billing_needs_human() -> None:
    res = triage("عندي مشكلة في الفاتورة")
    assert res.needs_human


def test_support_triage_technical_no_human() -> None:
    res = triage("النظام ما يشتغل")
    assert res.category == "technical" and not res.needs_human


# --- flows -----------------------------------------------------------------


def test_flow_map_has_twelve_flows() -> None:
    assert len(FLOWS) == 12
    assert len(flows_as_data()) == 12


def test_flow_for_intent_and_next() -> None:
    assert flow_for_intent(Intent.START_SCAN) == FlowId.READINESS_SCAN.value
    assert next_flow(FlowId.READINESS_SCAN) == FlowId.SERVICE_RECOMMENDATION.value


# --- brain pipeline + stores + metrics -------------------------------------


def test_brain_welcome_first_turn(tmp_stores) -> None:
    resp = brain.handle_message(wa_id="+966500000001", text="")
    assert resp.intent == Intent.WELCOME.value
    assert "Dealix" in resp.reply_ar
    assert resp.governance_decision == GovernanceDecision.ALLOW.value


def test_brain_blocks_unsafe(tmp_stores) -> None:
    resp = brain.handle_message(wa_id="+966500000002", text="ارسل واتساب لكل القائمة المشتراة")
    assert resp.intent == Intent.BLOCKED_UNSAFE.value
    assert resp.governance_decision == GovernanceDecision.BLOCK.value


def test_brain_secret_routes_to_portal(tmp_stores) -> None:
    resp = brain.handle_message(wa_id="+966500000003", text=f"مفتاحي {_FAKE_KEY}")
    assert resp.card is not None and resp.card["kind"] == "permission"
    assert resp.governance_decision == GovernanceDecision.REQUIRE_APPROVAL.value


def test_brain_handoff_on_human_request(tmp_stores) -> None:
    resp = brain.handle_message(wa_id="+966500000004", text="ابغى اكلم شخص")
    assert resp.handoff_brief is not None
    assert resp.governance_decision == GovernanceDecision.ESCALATE.value


def test_brain_support_builds_card(tmp_stores) -> None:
    resp = brain.handle_message(wa_id="+966500000005", text="عندي مشكلة في الفاتورة")
    assert resp.card is not None and resp.card["kind"] == "support_escalation"


def test_brain_persists_and_no_raw_pii(tmp_stores) -> None:
    brain.handle_message(wa_id="+966500000006", text="ايميلي test@example.com")
    msgs = store.list_messages()
    assert msgs
    assert all("test@example.com" not in m.text_redacted for m in msgs)
    sessions = store.list_sessions()
    assert sessions and all("966500000006" not in s.wa_id_hash for s in sessions)


def test_metrics_counts(tmp_stores) -> None:
    brain.handle_message(wa_id="+966500000007", text="")
    brain.handle_message(wa_id="+966500000007", text="ابغى دعم بالفاتورة")
    m = metrics.compute_metrics()
    assert m["new_sessions"] >= 1
    assert m["support_tickets"] >= 1
    assert m["governance_decision"] == GovernanceDecision.ALLOW.value
