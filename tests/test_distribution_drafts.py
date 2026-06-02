"""Contracts for the Product Distribution OS draft layer.

These lock the doctrine into the new distribution layer: every generated draft
is approval-first, evidence L1, PII-free, and passes the existing
``policy_check_draft`` gate. Forbidden-channel language must force ``needs_edit``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.data_os import pii_flags_for_row
from auto_client_acquisition.governance_os import policy_check_draft
from scripts.generate_distribution_drafts import build_draft, generate_drafts, write_drafts
from scripts.review_draft_queue import read_drafts, render_review

EXAMPLE = Path(__file__).resolve().parents[1] / "data" / "distribution" / "prospects.example.json"

# Statuses a generator must never emit on its own.
_FORBIDDEN_GENERATOR_STATES = {
    "approved",
    "copied_manually",
    "sent_via_integration",
    "replied",
}


def _example_prospects() -> list[dict]:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_prospects_generate_drafts() -> None:
    drafts = generate_drafts(_example_prospects())
    assert len(drafts) == 3  # all example prospects are new/qualified


def test_every_draft_is_approval_first() -> None:
    for draft in generate_drafts(_example_prospects()):
        assert draft["approval_required"] is True
        assert draft["status"] in {"pending_approval", "needs_edit"}
        assert draft["status"] not in _FORBIDDEN_GENERATOR_STATES


def test_every_draft_is_internal_evidence_l1() -> None:
    for draft in generate_drafts(_example_prospects()):
        assert draft["evidence_level"] == "L1"


def test_clean_drafts_pass_policy_and_have_no_pii() -> None:
    for draft in generate_drafts(_example_prospects()):
        if draft["status"] != "pending_approval":
            continue
        verdict = policy_check_draft(f"{draft['subject']}\n{draft['body']}")
        assert verdict.allowed, verdict.issues
        assert not draft["policy_issues"]
        assert pii_flags_for_row(draft) == []


def test_only_eligible_prospects_get_drafts() -> None:
    prospects = [
        {"id": "p1", "company": "A", "sector": "s", "status": "won"},
        {"id": "p2", "company": "B", "sector": "s", "status": "lost"},
        {"id": "p3", "company": "C", "sector": "s", "status": "qualified"},
    ]
    drafts = generate_drafts(prospects)
    assert {d["prospect_id"] for d in drafts} == {"p3"}


def test_forbidden_channel_language_forces_needs_edit() -> None:
    # Injecting forbidden-channel language into the pain hypothesis must trip
    # the existing policy gate and demote the draft to needs_edit.
    hostile = {
        "id": "p_bad",
        "company": "X",
        "sector": "s",
        "pain_hypothesis": "they want cold whatsapp blasting to everyone",
        "status": "qualified",
    }
    draft = build_draft(hostile)
    assert draft["status"] == "needs_edit"
    assert draft["policy_issues"]
    assert draft["approval_required"] is True


def test_email_in_body_is_flagged_as_pii() -> None:
    leaky = {
        "id": "p_leak",
        "company": "Y",
        "sector": "s",
        "pain_hypothesis": "reach us at owner@example.com fast",
        "status": "qualified",
    }
    draft = build_draft(leaky)
    assert draft["status"] == "needs_edit"
    assert "pii_email_in_body" in draft["policy_issues"]


def test_jsonl_roundtrip(tmp_path: Path) -> None:
    drafts = generate_drafts(_example_prospects())
    ledger = tmp_path / "drafts.jsonl"
    write_drafts(drafts, ledger)
    loaded = read_drafts(ledger)
    assert len(loaded) == len(drafts)
    review = render_review(loaded)
    assert "Pending approval" in review


def test_draft_matches_published_schema() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "dealix"
        / "contracts"
        / "schemas"
        / "distribution_draft.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for draft in generate_drafts(_example_prospects()):
        jsonschema.validate(draft, schema)
