"""Tests for the commercial orchestrator — the daily prospects→drafts loop.

These lock the doctrine-critical behaviour: company-level drafts only, every
draft approval-required and never auto-sent, durable queue round-trips, and the
ICP min-band gate.
"""
from __future__ import annotations

import importlib

import pytest

from auto_client_acquisition.commercial_orchestrator import (
    OutreachContext,
    render_outreach_draft,
    run_acquisition_to_drafts,
)
from auto_client_acquisition.commercial_orchestrator import draft_queue


@pytest.fixture()
def temp_queue(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_DRAFT_QUEUE_PATH", str(tmp_path / "q.jsonl"))
    importlib.reload(draft_queue)
    yield draft_queue
    monkeypatch.delenv("DEALIX_DRAFT_QUEUE_PATH", raising=False)
    importlib.reload(draft_queue)


SAMPLE = [
    {"company_name": "Acme Real Estate", "name_ar": "أكمي العقارية",
     "sector": "real_estate", "city": "Riyadh", "region": "Central",
     "size_band": "mid", "website": "", "source_type": "sector_frame",
     "source_url": "https://example.gov.sa", "consent_status": "required_before_contact",
     "pain_hypothesis_en": "scattered follow-up", "pain_hypothesis_ar": "متابعة مبعثرة"},
    {"company_name": "", "sector": "logistics", "city": "Jeddah",
     "region": "Western", "size_band": "mid"},  # missing name → skipped
]


def test_outreach_draft_is_bilingual_and_safe():
    out = render_outreach_draft(OutreachContext(
        company_name="Acme Co", sector="logistics", city="Dammam"))
    body = out["body_md"]
    assert "Outreach Draft" in body            # EN section
    assert "مسوّدة تواصل" in body               # AR section
    assert "not guaranteed" in body            # disclaimer present
    assert "ليست نتائج مضمونة" in body
    # no personal-PII tokens injected
    assert "@" not in out["subject_en"]


def test_run_generates_company_level_drafts(temp_queue):
    res = run_acquisition_to_drafts(SAMPLE)
    assert res.generated == 1            # one valid, one skipped (no name)
    assert res.skipped == 1
    d = res.drafts[0]
    assert d["company_name"] == "Acme Real Estate"
    assert d["approval_required"] is True
    assert d["no_live_send"] is True
    assert d["consent_status"] == "required_before_contact"
    assert d["icp_band"] in {"warm", "hot"}
    assert d["offer"] == "free_ai_ops_diagnostic"


def test_drafts_persist_to_queue_and_round_trip(temp_queue):
    res = run_acquisition_to_drafts(SAMPLE)
    assert temp_queue.stats()["pending"] == res.generated
    did = res.drafts[0]["id"]
    temp_queue.set_status(did, "approved", who="founder", note="ok")
    assert temp_queue.get(did)["status"] == "approved"
    assert temp_queue.get(did)["approver"] == "founder"
    assert temp_queue.stats()["pending"] == 0


def test_min_band_gate_filters(temp_queue):
    # An unmatched sector/region scores below warm and earns no draft.
    off_icp = [{"company_name": "Nowhere Co", "sector": "unknown_sector",
                "city": "Nowhere", "region": "Nowhere", "size_band": "unknown"}]
    res = run_acquisition_to_drafts(off_icp, min_band="warm")
    assert res.generated == 0
    assert res.skipped == 1


def test_invalid_status_rejected(temp_queue):
    res = run_acquisition_to_drafts(SAMPLE)
    with pytest.raises(ValueError):
        temp_queue.set_status(res.drafts[0]["id"], "bogus")


def test_no_guaranteed_claim_outside_disclaimer(temp_queue):
    res = run_acquisition_to_drafts(SAMPLE)
    body = res.drafts[0]["body_md"]
    # The only occurrence of "guarantee" is the negated disclaimer line.
    for line in body.splitlines():
        if "guarantee" in line.lower() or "مضمون" in line:
            assert "not guaranteed" in line or "ليست نتائج مضمونة" in line
