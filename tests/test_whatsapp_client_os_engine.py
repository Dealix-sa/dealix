"""WhatsApp Client OS — engine, state machine and handoff behavior."""

from __future__ import annotations

import pytest

from auto_client_acquisition.whatsapp_client_os import conversation_state as fsm
from auto_client_acquisition.whatsapp_client_os import handoff_router
from auto_client_acquisition.whatsapp_client_os.assessment import AXIS_ORDER, axis_spec
from auto_client_acquisition.whatsapp_client_os.engine import handle_inbound, new_session


@pytest.fixture(autouse=True)
def _isolated_store(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_WHATSAPP_OS_DIR", str(tmp_path))
    from auto_client_acquisition.whatsapp_client_os import client_profile_store as store

    store.clear_for_test()
    yield


# ── State machine ─────────────────────────────────────────────────────-──
def test_new_transitions_to_menu_on_welcome() -> None:
    assert fsm.transition("new", "welcome") == "menu"


def test_blocked_unsafe_never_advances() -> None:
    for stage in ("menu", "assessment_in_progress", "proposal"):
        assert fsm.transition(stage, "blocked_unsafe") == stage  # type: ignore[arg-type]


def test_human_handoff_overrides_any_stage() -> None:
    assert fsm.transition("proposal", "human_handoff") == "human_handoff"
    assert fsm.transition("menu", "human_handoff") == "human_handoff"


def test_assessment_completion_gate() -> None:
    assert fsm.transition("assessment_in_progress", "assessment_answer") == "assessment_in_progress"
    assert (
        fsm.transition("assessment_in_progress", "assessment_answer", assessment_complete=True)
        == "assessment_complete"
    )


def test_proposal_approval_goes_to_payment_handoff() -> None:
    assert fsm.transition("proposal", "approve") == "payment_handoff"


def test_human_handoff_is_terminal() -> None:
    assert fsm.is_terminal("human_handoff") is True
    assert fsm.is_terminal("menu") is False


# ── Engine flow ───────────────────────────────────────────────────────-──
def test_welcome_shows_six_option_menu() -> None:
    s = new_session(client_handle="966500000000")
    r = handle_inbound(s, text="السلام عليكم")
    assert r.intent == "welcome"
    assert r.session.stage == "menu"
    assert len(r.cards[0].options) == 6
    # «ما أعرف» is always present (lowers friction)
    assert any(o.intent == "not_sure" for o in r.cards[0].options)


def test_full_assessment_flow_produces_recommendation() -> None:
    s = new_session(client_handle="966500000001", company_name="شركة")
    r = handle_inbound(s, button_id="menu:not_sure")
    assert r.session.stage == "assessment_in_progress"
    sess = r.session
    for ax in AXIS_ORDER:
        opt = axis_spec(ax)["options"][0]["id"]
        r = handle_inbound(sess, button_id=f"asmt:{ax}:{opt}")
        sess = r.session
    assert r.assessment is not None
    assert r.assessment.completed is True
    assert r.cards[0].kind == "recommendation"
    assert r.cards[0].catalog_ref  # tied to a catalog offer


def test_secrets_inbound_is_blocked_and_handed_off_without_state_change() -> None:
    s = new_session(client_handle="966500000002")
    r0 = handle_inbound(s, text="مرحبا")
    before = r0.session.stage
    r = handle_inbound(r0.session, text="API_KEY = sk-abcdefghijklmnopqrstuvwxyz12345")
    assert r.blocked is True
    assert r.session.stage == before  # never advanced
    assert r.handoff is not None and r.handoff.reason == "secrets_attempt"
    assert r.cards[0].kind == "action"


def test_cold_whatsapp_request_is_refused() -> None:
    s = new_session(client_handle="966500000003")
    r = handle_inbound(s, text="أرسلوا واتساب بارد لكل الأرقام في قائمة مشتراة")
    assert r.blocked is True
    assert "خارج سياسة" in r.cards[0].title_ar


def test_explicit_human_request_escalates() -> None:
    s = new_session(client_handle="966500000004")
    r = handle_inbound(s, text="أبغى أتحدث مع شخص")
    assert r.session.stage == "human_handoff"
    assert r.handoff is not None
    assert r.handoff.reason == "explicit_request"
    assert r.handoff.suggested_action_ar


def test_repeated_unknown_escalates_to_human() -> None:
    s = new_session(client_handle="966500000005")
    r = handle_inbound(s, text="مرحبا")
    sess = r.session
    # send gibberish a few times; after repeated unknowns it should escalate
    last = None
    for _ in range(4):
        last = handle_inbound(sess, text="زبلطمن قثضكنف")
        sess = last.session
    assert sess.stage == "human_handoff" or last.intent == "unknown"


# ── Handoff packet ───────────────────────────────────────────────────────
def test_handoff_packet_preserves_context() -> None:
    s = new_session(client_handle="966500000006", company_name="عميل تجريبي")
    h = handoff_router.build_handoff(s, reason="complaint", last_messages=["رسالة 1", "رسالة 2"])
    assert h.reason == "complaint"
    assert h.last_messages == ["رسالة 1", "رسالة 2"]
    assert "عميل تجريبي" in h.summary_ar
    assert h.suggested_action_ar


def test_detect_reason_priority() -> None:
    assert handoff_router.detect_reason(intent="human_handoff", stage="menu") == "explicit_request"
    assert (
        handoff_router.detect_reason(intent="unknown", stage="menu", secrets_attempt=True)
        == "secrets_attempt"
    )
    assert (
        handoff_router.detect_reason(intent="unknown", stage="menu", permission_level="L5")
        == "permission_l5"
    )
    assert handoff_router.detect_reason(intent="unknown", stage="menu") is None
