"""End-to-end pipeline: weakness → offer → draft (no auto-send) → brief → learning."""

from __future__ import annotations

from scripts.targeting_daily_brief import build_brief
from scripts.targeting_draft_lab import build_draft, validate_draft
from scripts.targeting_learning_loop import analyze
from scripts.targeting_offer_router import route_offer
from scripts.targeting_weakness_mapper import WEAKNESS_TO_OS, map_weaknesses


def _agency() -> dict:
    return {
        "company_name": "Manar Performance Agency",
        "website": "https://manar.example.sa",
        "city": "riyadh",
        "sector": "marketing_agency",
        "b2b": True,
        "contact_channel": "official_business_email",
        "no_case_studies": True,
        "weak_cta": True,
        "many_clients_no_memory": True,
        "growth_signal": True,
        "serves_many_clients": True,
        "source_urls": ["https://manar.example.sa", "https://manar.example.sa/clients"],
        "evidence_count": 2,
    }


def test_weakness_maps_to_a_known_os_angle() -> None:
    m = map_weaknesses(_agency())
    assert m["primary_weakness"] in WEAKNESS_TO_OS
    assert m["primary_os_angle"] == WEAKNESS_TO_OS[m["primary_weakness"]]


def test_offer_router_returns_a_catalog_offer() -> None:
    r = route_offer(_agency())
    assert r["offer_id"]
    assert r["offer"]["price_sar"] >= 0
    assert r["draft_type"]


def test_draft_is_valid_and_never_auto_sends() -> None:
    d = build_draft(_agency())
    assert d["auto_send"] is False
    assert d["approval_required"] == "founder"
    assert d["validation"]["ok"], d["validation"]["issues"]
    assert "APPROVAL_REQUIRED" in d["markdown"]


def test_draft_rejects_exaggerated_promises() -> None:
    d = build_draft(_agency())
    d["body"] += " نضمن لك زيادة مؤكدة 100%"
    v = validate_draft(d, _agency())
    assert v["ok"] is False
    assert any(i.startswith("banned_phrase") for i in v["issues"])


def test_draft_requires_evidence() -> None:
    company = {**_agency(), "source_urls": []}
    d = build_draft(company)
    assert "missing_evidence" in d["validation"]["issues"]


def test_daily_brief_runs_full_pipeline() -> None:
    companies = [
        _agency(),
        {**_agency(), "company_name": "Sensitive Clinic", "sector": "healthcare"},
        {**_agency(), "company_name": "Bad Lead", "personal_phone": True},
    ]
    result = build_brief(companies)
    names = {s["company_name"] for s in result["scored"]}
    assert "Manar Performance Agency" in names
    # Bad Lead is a compliance reject → excluded from scored eligible pool.
    assert "Bad Lead" not in names
    assert result["best_sector"]
    assert "Daily Targeting Brief" in result["brief_md"]


def test_learning_loop_aggregates_outcomes() -> None:
    outcomes = [
        {
            "sector": "marketing_agency",
            "score": 86,
            "stage": "paid",
            "message_angle": "proof_gap",
            "offer": "command_sprint",
            "source_type": "official_site",
        },
        {
            "sector": "tech_software",
            "score": 79,
            "stage": "no_reply",
            "message_angle": "delivery_blindness",
            "source_type": "directory",
        },
        {
            "sector": "consulting",
            "score": 88,
            "stage": "diagnostic",
            "message_angle": "command_fog",
            "source_type": "official_site",
        },
    ]
    report = analyze(outcomes)
    assert report["best_offer"] == "command_sprint"
    assert report["totals"]["paid"] == 1
    assert report["best_message_angle"] == "command_fog"
