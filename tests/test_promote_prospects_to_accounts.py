"""Doctrine + correctness tests for the prospect-promotion intake script.

These lock the non-negotiable guarantees of
``scripts/promote_prospects_to_accounts.py``:

  • forbidden sources (scraping / purchased lists) are rejected
  • empty email/phone cells are NEVER turned into fabricated contacts
  • status is ``enriched`` only when a real contact method exists
  • the account id is deterministic (idempotent re-runs)
  • DQ reflects real-field completeness, not invented data

The pure helpers are import-safe (no DB), so these run offline.
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.promote_prospects_to_accounts import (
    ALLOWED_SOURCES,
    BLOCKED_SOURCE_TOKENS,
    _compute_dq,
    _load_plan,
    _plan_row,
    _source_ok,
    _stable_suffix,
)


def test_forbidden_sources_rejected():
    for token in BLOCKED_SOURCE_TOKENS:
        ok, reason = _source_ok(token)
        assert ok is False, f"{token!r} must be rejected"
        assert "forbidden" in reason or "unknown" in reason


def test_scraping_and_purchased_explicitly_blocked():
    for src in ("linkedin_scrape", "scraped_list", "purchased", "bought_leads", "data_broker"):
        ok, _ = _source_ok(src)
        assert ok is False, f"{src!r} must never be admitted"


def test_lawful_sources_allowed():
    for src in ("public_directory", "google_places", "inbound_form", "warm_intro", "referral", "manual"):
        ok, _ = _source_ok(src)
        assert ok is True, f"{src!r} should be allowed"
        assert src in ALLOWED_SOURCES


def test_empty_source_rejected():
    ok, reason = _source_ok("")
    assert ok is False
    assert "required" in reason


def test_never_fabricates_contact():
    """Empty email/phone cells must stay None — no synthetic ceo@domain."""
    row = {
        "company_name": "شركة بلا تواصل",
        "domain": "no-contact.sa",
        "sector": "saas",
        "source": "public_directory",
        # email + phone intentionally absent
    }
    plan = _plan_row(row)
    assert plan is not None and not plan.get("_error")
    assert plan["email"] is None
    assert plan["phone"] is None
    assert plan["reachable"] is False
    assert plan["status"] == "new"  # not enriched without a contact method


def test_reachable_row_is_enriched():
    row = {
        "company_name": "وكالة فيها تواصل",
        "domain": "has-contact.sa",
        "sector": "marketing_agency",
        "email": "real@has-contact.sa",
        "source": "business_directory",
    }
    plan = _plan_row(row)
    assert plan["reachable"] is True
    assert plan["status"] == "enriched"
    assert plan["email"] == "real@has-contact.sa"


def test_missing_company_name_is_error():
    plan = _plan_row({"domain": "x.sa", "source": "manual"})
    assert plan is not None
    assert plan.get("_error")


def test_phone_normalized_to_e164():
    row = {
        "company_name": "شركة هاتف",
        "domain": "phone.sa",
        "phone": "0501234567",
        "source": "manual",
    }
    plan = _plan_row(row)
    assert plan["phone"] is not None
    assert plan["phone"].startswith("+966")


def test_account_id_is_deterministic():
    """Same place_id/domain → same id (idempotent re-run)."""
    a = _stable_suffix("ChIJ_x", "foo.sa", "foo")
    b = _stable_suffix("ChIJ_x", "different.sa", "different")  # place_id wins
    assert a == b
    c = _stable_suffix("", "foo.sa", "foo")
    d = _stable_suffix("", "foo.sa", "bar")  # domain wins over name
    assert c == d


def test_dq_reflects_real_completeness():
    bare = _compute_dq(domain=None, email=None, phone=None, city=None, sector=None, contact_name=None)
    full = _compute_dq(
        domain="x.sa", email="a@x.sa", phone="+966500000000",
        city="Riyadh", sector="saas", contact_name="Sami",
    )
    assert bare < full
    assert 0 < bare <= 100
    assert full <= 100


def test_load_plan_mixed(tmp_path: Path):
    csv_path = tmp_path / "p.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company_name", "domain", "email", "source"])
        w.writerow(["Good Co", "good.sa", "x@good.sa", "public_directory"])
        w.writerow(["Scraped Co", "bad.sa", "y@bad.sa", "linkedin_scrape"])
        w.writerow(["", "z.sa", "", "manual"])  # empty company_name → rejected
    accepted, rejected = _load_plan(csv_path)
    assert len(accepted) == 1
    assert accepted[0]["company_name"] == "Good Co"
    assert len(rejected) == 2  # scraped + empty-name


def test_template_csv_exists_and_is_valid():
    template = Path(__file__).resolve().parents[1] / "data" / "prospects.csv.template"
    assert template.is_file(), "data/prospects.csv.template must exist"
    text = template.read_text(encoding="utf-8")
    assert "company_name" in text
    assert "source" in text
    # The template must warn against fabricating contacts.
    assert "never" in text.lower() or "NEVER" in text


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
