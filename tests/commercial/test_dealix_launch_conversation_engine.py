"""Tests for the Dealix Launch Conversation & Negotiation Engine (draft-only)."""

from __future__ import annotations

import json

import pytest

from dealix.conversation_engine import (
    company_brain,
    engine,
    message_generator,
    negotiation_planner,
    objection_handler,
    offer_matcher,
    proof_builder,
    safety_guard,
    target_profile,
)
from dealix.conversation_engine.channel_adapter import EMAIL, WHATSAPP
from dealix.conversation_engine.company_brain import CANONICAL_FOUNDER_EMAIL


# --- safety guard -----------------------------------------------------------

@pytest.mark.parametrize(
    "flag",
    [
        "EXTERNAL_SEND_ENABLED",
        "EMAIL_SEND_ENABLED",
        "WHATSAPP_SEND_ENABLED",
        "AUTO_WHATSAPP_ENABLED",
        "AUTO_EMAIL_ENABLED",
        "AUTO_LINKEDIN_ENABLED",
        "AUTO_PAYMENT_CAPTURE_ENABLED",
        "AUTO_MERGE_ENABLED",
        "PRODUCTION_MUTATION_ENABLED",
    ],
)
def test_safety_guard_blocks_unsafe_flags(flag):
    result = safety_guard.evaluate_environment({flag: "true"})
    assert result.safe is False
    assert result.verdict == "BLOCKED_BY_SAFETY_GUARD"


def test_safety_guard_blocks_non_draft_outbound_mode():
    result = safety_guard.evaluate_environment({"OUTBOUND_MODE": "live"})
    assert result.safe is False


def test_safety_guard_allows_draft_only():
    result = safety_guard.evaluate_environment({"OUTBOUND_MODE": "draft_only"})
    assert result.safe is True
    assert result.verdict == "SAFE_TO_RUN_INTERNAL_DRAFT_ONLY"


def test_engine_blocked_produces_no_opportunities():
    payload = engine.run(env={"EXTERNAL_SEND_ENABLED": "true"})
    assert payload["verdict"] == "BLOCKED_BY_SAFETY_GUARD"
    assert payload["opportunities"] == []


# --- founder email ----------------------------------------------------------

def test_founder_email_is_canonical():
    assert company_brain.founder_email() == CANONICAL_FOUNDER_EMAIL
    assert company_brain.founder_profile()["canonical_email"] == CANONICAL_FOUNDER_EMAIL


def test_email_draft_uses_canonical_email():
    target = company_brain.seed_targets()[0]
    offer = company_brain.offers()[0]
    draft = message_generator.build_email(target, offer)
    assert draft["from_email"] == CANONICAL_FOUNDER_EMAIL
    assert CANONICAL_FOUNDER_EMAIL in draft["detailed_version"]


# --- message generation -----------------------------------------------------

def test_message_generation_returns_drafts_with_cta():
    target = company_brain.seed_targets()[0]
    offer = company_brain.offers()[0]
    channels = message_generator.build_all_channels(target, offer)
    assert channels[EMAIL]["cta"].strip()
    assert channels[WHATSAPP]["permission_cta"].strip()
    assert channels["linkedin"]["connection_note"].strip()
    assert channels["call"]["close_next_step"].strip()


def test_whatsapp_is_not_auto_send():
    target = company_brain.seed_targets()[0]
    offer = company_brain.offers()[0]
    wa = message_generator.build_whatsapp(target, offer)
    assert wa["cold_send_forbidden"] is True
    assert "warm_only_no_cold" in wa["risk_flags"]


# --- objections -------------------------------------------------------------

def test_objection_handler_returns_response():
    resp = objection_handler.handle_objection("price_high")
    assert resp is not None
    assert resp["short_ar"]
    assert resp["negotiation_move"]


def test_objection_handler_covers_trust_questions():
    for oid in ("send_on_our_behalf", "data_permissions", "guarantee_results"):
        assert objection_handler.handle_objection(oid) is not None


# --- negotiation ------------------------------------------------------------

def test_negotiation_plan_includes_next_action():
    target = target_profile.score_target(company_brain.seed_targets()[0])
    match = offer_matcher.match_offer(target)
    plan = negotiation_planner.build_plan(target, match)
    assert plan["next_best_action"]
    assert plan["close_question"]
    assert plan["approval_required"] is True
    # Concessions never drop price first.
    assert any("النطاق" in r for r in plan["concession_rules"])


# --- approval queue ---------------------------------------------------------

def test_approval_queue_required_for_all_external_channels():
    payload = engine.run(limit=5)
    approvals = payload["approval_queue"]
    assert approvals
    assert all(a["approval_required"] for a in approvals)
    assert all(a["status"] == "pending_founder_approval" for a in approvals)
    assert {a["channel"] for a in approvals} <= {EMAIL, WHATSAPP}


# --- proof ------------------------------------------------------------------

def test_proof_pack_does_not_claim_fake_revenue():
    target = target_profile.score_target(company_brain.seed_targets()[0])
    match = offer_matcher.match_offer(target)
    pack = proof_builder.build_proof_pack(target, match)
    assert pack["safe"] is True
    assert pack["violations"] == []


def test_proof_validator_catches_forbidden_claim():
    bad = {"expected_outcome": "we guarantee ROI and guaranteed revenue"}
    assert proof_builder.validate_proof_pack(bad)


# --- runner outputs ---------------------------------------------------------

def test_runner_creates_expected_files(tmp_path, monkeypatch):
    import scripts.commercial.run_dealix_launch_conversation_engine as runner

    monkeypatch.setattr(runner, "REPORT_DIR", tmp_path)
    rc = runner.main(["--mode", "draft-only", "--limit", "5"])
    assert rc == 0
    for name in (
        "latest.json", "latest.md", "approval_queue.csv", "opportunity_graph.csv",
        "email_drafts.csv", "whatsapp_drafts.csv", "negotiation_playbooks.csv", "proof_pack.md",
        "slack_brief.md",
    ):
        assert (tmp_path / name).is_file(), name

    payload = json.loads((tmp_path / "latest.json").read_text(encoding="utf-8"))
    assert payload["summary"]["live_send"] is False
    assert payload["verdict"] == "SAFE_TO_RUN_INTERNAL_DRAFT_ONLY"

    # Slack brief is a draft only — it must state nothing is sent.
    brief = (tmp_path / "slack_brief.md").read_text(encoding="utf-8")
    assert "draft" in brief.lower()
    assert "Nothing is sent" in brief
