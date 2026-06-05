"""Compliance gate: rejects violations, holds sensitive sectors, approves clean."""

from __future__ import annotations

from scripts.targeting_compliance_gate import APPROVED, REJECTED, REVIEW, evaluate, run


def _clean() -> dict:
    return {
        "company_name": "Clean Co",
        "sector": "marketing_agency",
        "city": "riyadh",
        "contact_channel": "official_business_email",
        "source_urls": ["https://clean.example.sa", "https://clean.example.sa/clients"],
        "source_type": "official_site",
        "evidence_count": 2,
    }


def test_clean_company_is_approved() -> None:
    v = evaluate(_clean())
    assert v["status"] == APPROVED


def test_personal_phone_is_rejected() -> None:
    c = _clean()
    c["personal_phone"] = True
    v = evaluate(c)
    assert v["status"] == REJECTED
    assert any(r.startswith("red_flag:personal_phone") for r in v["reasons"])


def test_behind_login_source_is_rejected() -> None:
    c = _clean()
    c["source_type"] = "behind_login"
    assert evaluate(c)["status"] == REJECTED


def test_blocked_domain_is_rejected() -> None:
    c = _clean()
    c["source_urls"] = ["https://www.linkedin.com/sales/lead/123"]
    v = evaluate(c)
    assert v["status"] == REJECTED
    assert any(r.startswith("blocked_domain") for r in v["reasons"])


def test_insufficient_evidence_is_rejected() -> None:
    c = _clean()
    c["evidence_count"] = 1
    c["source_urls"] = ["https://clean.example.sa"]
    v = evaluate(c)
    assert v["status"] == REJECTED
    assert any(r.startswith("insufficient_evidence") for r in v["reasons"])


def test_missing_channel_is_rejected() -> None:
    c = _clean()
    c["contact_channel"] = ""
    assert evaluate(c)["status"] == REJECTED


def test_sensitive_sector_is_held_for_review_not_approved() -> None:
    c = _clean()
    c["sector"] = "healthcare"
    v = evaluate(c)
    assert v["status"] == REVIEW
    assert "sensitive_sector_review_required" in v["reasons"]


def test_every_reject_carries_a_reason() -> None:
    companies = [_clean(), {**_clean(), "personal_phone": True}]
    buckets = run(companies)
    for v in buckets[REJECTED]:
        assert v["reasons"], "a reject must always carry an explicit reason"
