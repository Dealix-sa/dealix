"""Seed-lead validation enforces schema, consent, and a no-scraping source rule."""

from __future__ import annotations

import json

from scripts.commercial_launch_core import SEED_LEADS
from scripts.commercial_seed_leads_validate import validate_leads


def test_example_file_is_valid():
    report = validate_leads(SEED_LEADS)
    assert report["exists"] is True
    assert report["valid"] is True
    assert report["count"] >= 5


def test_missing_file_is_tolerated(tmp_path):
    report = validate_leads(tmp_path / "nope.jsonl")
    assert report["valid"] is True
    assert any("placeholder" in w.lower() for w in report["warnings"])


def test_forbidden_source_is_rejected(tmp_path):
    bad = tmp_path / "bad.jsonl"
    bad.write_text(
        json.dumps(
            {
                "lead_id": "B1",
                "company_name": "X",
                "country": "SA",
                "vertical_hint": "facilities_management",
                "language_hint": "en",
                "source": "scraped",
                "consent_status": "none",
                "research_status": "required",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    report = validate_leads(bad)
    assert report["valid"] is False
    assert any("forbidden source" in e for e in report["errors"])


def test_missing_required_key_is_rejected(tmp_path):
    bad = tmp_path / "bad2.jsonl"
    bad.write_text(json.dumps({"lead_id": "B2"}) + "\n", encoding="utf-8")
    report = validate_leads(bad)
    assert report["valid"] is False
