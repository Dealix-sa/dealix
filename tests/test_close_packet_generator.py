"""Tests for the unified founder Close Packet generator.

Offline: the core builder is a pure function over a dict (no network, no
subprocess). detect_stack is never invoked here.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.dealix_close_packet_generator import (
    build_close_packet,
    build_close_packet_markdown,
    main,
)


def _accept_prospect() -> dict:
    return {
        "company": "Demo Saudi Realty",
        "sector": "real_estate",
        "decision_maker": "Ahmad Al-Zaini",
        "role": "CEO",
        "city": "Riyadh",
        "channel": "whatsapp",
        "relationship": "warm",
        "warm_intro_notes": "Met at a Riyadh proptech event",
        # All 8 flags true => score 100 => ACCEPT.
        "signals": {
            "pain_clear": True,
            "owner_present": True,
            "data_available": True,
            "accepts_governance": True,
            "has_budget": True,
            "wants_safe_methods": True,
            "proof_path_visible": True,
            "retainer_path_visible": True,
        },
    }


def _reject_prospect() -> dict:
    # Declines safe methods => non-negotiable reject, no proposal/outreach.
    return {
        "company": "No-Governance Co",
        "sector": "agencies",
        "decision_maker": "Sara K",
        "role": "Owner",
        "channel": "email",
        "relationship": "warm",
        "signals": {
            "pain_clear": True,
            "owner_present": True,
            "wants_safe_methods": False,
        },
    }


def _doctrine_prospect() -> dict:
    # Requests a cold WhatsApp blast => doctrine violation => channel refused.
    return {
        "company": "Blast Marketing",
        "sector": "agencies",
        "decision_maker": "Khalid",
        "role": "CMO",
        "channel": "whatsapp",
        "relationship": "warm",
        "raw_request_text": "I want to blast leads via cold whatsapp to everyone",
        "signals": {
            "pain_clear": True,
            "owner_present": True,
            "data_available": True,
            "accepts_governance": True,
            "has_budget": True,
            "wants_safe_methods": True,
            "proof_path_visible": True,
            "retainer_path_visible": True,
        },
    }


# ── (a) ACCEPT-grade prospect: full packet with every section ──
def test_accept_packet_contains_all_sections() -> None:
    packet = build_close_packet(_accept_prospect())
    assert packet["decision"] == "accept"
    md = packet["markdown"]

    # Qualification verdict
    assert "Qualification verdict" in md
    assert "ACCEPT" in md
    assert "/ 100" in md
    # Diagnostic section (reused generator output)
    assert "Free diagnostic" in md
    assert "AI Ops Diagnostic" in md
    assert "Bottlenecks" in md
    # Proposal section
    assert "Matched proposal" in md
    assert "Revenue Intelligence Sprint" in md
    # Outreach DRAFT section, clearly labelled and not auto-sent
    assert "Outreach DRAFT" in md
    assert "never auto-sent" in md
    # Checklist
    assert "pre-send checklist" in md
    assert "Exactly one CTA" in md
    # Disclaimer (bilingual)
    assert "Estimated value is not Verified value" in md
    assert "النتائج التقديرية ليست نتائج مضمونة" in md


def test_accept_packet_emits_bilingual_outreach_draft() -> None:
    packet = build_close_packet(_accept_prospect())
    outreach = packet["outreach"]
    assert outreach["produced"] is True
    assert outreach["ar"].strip()
    assert outreach["en"].strip()
    # The draft must pass the canonical governance guard.
    assert outreach["reason"] == ""
    assert outreach["policy_issues"] == []


# ── (b) Proposal motion matches the decision (ACCEPT -> 499 sprint) ──
def test_accept_proposal_motion_and_price() -> None:
    packet = build_close_packet(_accept_prospect())
    proposal = packet["proposal"]
    assert proposal["produced"] is True
    assert proposal["motion"] == "revenue_intelligence_sprint"
    assert proposal["price_sar"] == 499
    assert "499" in proposal["markdown"]


def test_reframe_decision_maps_to_mid_tier_proposal() -> None:
    # Score 80 with data_available => reframe => scoped discovery (mid-tier).
    prospect = {
        "company": "Mid Fit Co",
        "sector": "services",
        "decision_maker": "Lina",
        "role": "GM",
        "relationship": "warm",
        "signals": {
            "pain_clear": True,
            "owner_present": True,
            "data_available": True,
            "accepts_governance": True,
            "has_budget": False,
            "wants_safe_methods": True,
            "proof_path_visible": True,
            "retainer_path_visible": False,
        },
    }
    packet = build_close_packet(prospect)
    assert packet["decision"] == "reframe"
    assert packet["proposal"]["motion"] == "scoped_discovery"
    assert packet["proposal"]["price_sar"] == 249


def test_diagnostic_only_decision_maps_to_diagnostic_offer() -> None:
    prospect = {
        "company": "Low Signal Co",
        "sector": "training",
        "relationship": "warm",
        "signals": {
            "pain_clear": True,
            "owner_present": True,
            "accepts_governance": True,
            "wants_safe_methods": True,
            "proof_path_visible": True,
        },
    }
    packet = build_close_packet(prospect)
    assert packet["decision"] == "diagnostic_only"
    assert packet["proposal"]["motion"] == "capability_diagnostic"
    assert packet["proposal"]["price_sar"] == 0


# ── (c) REJECT-grade prospect: no proposal, no outreach, clear refusal ──
def test_reject_packet_has_no_proposal_or_outreach() -> None:
    packet = build_close_packet(_reject_prospect())
    assert packet["decision"] == "reject"
    assert packet["proposal"]["produced"] is False
    assert packet["outreach"]["produced"] is False
    md = packet["markdown"]
    assert "No proposal produced" in md
    assert "No outreach draft produced" in md
    # refer-out guidance present
    assert "refer" in md.lower()


# ── (d) Doctrine violation: flagged + offending channel refused ──
def test_doctrine_violation_flagged_and_channel_refused() -> None:
    packet = build_close_packet(_doctrine_prospect())
    assert packet["decision"] == "reject"
    assert "cold_whatsapp" in packet["doctrine_violations"]
    assert packet["channel_refused"] is True
    assert packet["outreach"]["produced"] is False
    md = packet["markdown"]
    assert "DOCTRINE VIOLATION" in md
    assert "REFUSED" in md
    # A safe alternative is recommended instead of the offending channel.
    assert packet["safe_channel_alternative"] in md


def test_cold_relationship_refuses_outreach_but_keeps_proposal() -> None:
    # Cold basis must not auto-draft outreach, but qualification can still run.
    prospect = {
        "company": "Cold Co",
        "sector": "logistics",
        "decision_maker": "Omar",
        "role": "COO",
        "channel": "whatsapp",
        "relationship": "cold",
        "signals": {
            "pain_clear": True,
            "owner_present": True,
            "data_available": True,
            "accepts_governance": True,
            "has_budget": True,
            "wants_safe_methods": True,
            "proof_path_visible": True,
            "retainer_path_visible": True,
        },
    }
    packet = build_close_packet(prospect)
    assert packet["channel_refused"] is True
    assert "cold_relationship_basis" in packet["channel_refusal_reasons"]
    assert packet["outreach"]["produced"] is False


# ── Public-function coverage ──
def test_build_close_packet_markdown_wrapper_returns_str() -> None:
    md = build_close_packet_markdown(_accept_prospect())
    assert isinstance(md, str)
    assert md.startswith("# Close Packet — Demo Saudi Realty")


def test_build_close_packet_requires_company_and_sector() -> None:
    with pytest.raises(ValueError):
        build_close_packet({"sector": "real_estate"})
    with pytest.raises(ValueError):
        build_close_packet({"company": "X"})


def test_detected_stack_summary_enriches_diagnostic() -> None:
    stack = {
        "domain": "demo.sa",
        "status": "ok",
        "tools": [{"name": "WordPress"}, {"name": "HubSpot"}],
        "signals": [{"name": "has_crm"}],
    }
    packet = build_close_packet(_accept_prospect(), detected_stack=stack)
    assert packet["detected_stack"]["available"] is True
    assert "WordPress" in packet["markdown"]


def test_main_writes_packet_file(tmp_path: Path) -> None:
    out = tmp_path / "close_packet_cli.md"
    rc = main(
        [
            "--company",
            "CLI Demo Co",
            "--sector",
            "real_estate",
            "--decision-maker",
            "Test Person",
            "--role",
            "CEO",
            "--channel",
            "whatsapp",
            "--relationship",
            "warm",
            "--signals",
            "pain_clear,owner_present,data_available,accepts_governance,"
            "has_budget,wants_safe_methods,proof_path_visible,retainer_path_visible",
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "Close Packet — CLI Demo Co" in text
    assert "ACCEPT" in text
