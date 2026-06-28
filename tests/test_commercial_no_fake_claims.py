"""No fabricated proof or guaranteed-result claims may leak into artefacts."""

from __future__ import annotations

import json
from pathlib import Path

from app.commercial import safety
from app.commercial.orchestrator import run_growth_os

DATA = Path(__file__).resolve().parents[1] / "data" / "commercial"


def test_claim_guard_detects_guarantees():
    assert safety.contains_blocked_claim("We guarantee 10x ROI") is not None
    assert safety.contains_blocked_claim("نضمن لك زيادة المبيعات") is not None
    assert safety.contains_blocked_claim("risk-free results") is not None


def test_claim_guard_allows_honest_copy():
    assert safety.contains_blocked_claim("We help teams organise follow-up.") is None


def test_no_card_draft_contains_blocked_claim():
    accounts = json.loads((DATA / "accounts.sample.json").read_text())["accounts"]
    result = run_growth_os(accounts, [])
    for card in result.cards:
        assert safety.contains_blocked_claim(card.draft_message_ar) is None
        assert safety.contains_blocked_claim(card.draft_message_en) is None


def test_proof_pack_makes_no_guarantee():
    accounts = json.loads((DATA / "accounts.sample.json").read_text())["accounts"]
    result = run_growth_os(accounts, [])
    proof = result.proof
    assert proof["guarantees"].startswith("none")
    assert proof["claims_policy"] == "factual_only_no_fabrication"
    # Counts are derived only from real artefacts.
    assert proof["produced"]["accounts"] == len(result.accounts)
