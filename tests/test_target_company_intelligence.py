"""Tests for target_company_intelligence — deterministic, no network, no DB."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_os.target_company_intelligence import (
    WEAKNESS_CATALOG,
    build_company_dossier,
    build_target_company_draft,
    declared_weaknesses_to_signals,
    detect_structural_weaknesses,
    split_declared_weaknesses,
)


def _codes(weaknesses: list[dict]) -> set[str]:
    return {w["code"] for w in weaknesses}


def test_detect_untracked_source_when_no_source() -> None:
    weaknesses = detect_structural_weaknesses({"company_name": "Acme"})
    assert "untracked_source" in _codes(weaknesses)
    untracked = next(w for w in weaknesses if w["code"] == "untracked_source")
    assert untracked["is_hypothesis"] is False
    assert untracked["evidence"]


def test_detect_stale_relationship_at_90_days() -> None:
    weaknesses = detect_structural_weaknesses(
        {"company_name": "Acme", "source": "founder_network", "last_contact_days": 90}
    )
    assert "stale_relationship" in _codes(weaknesses)


def test_detect_sector_outside_icp_via_mismatch() -> None:
    company = {
        "company_name": "Acme",
        "sector": "mining",
        "city": "Riyadh",
        "source": "founder_network",
    }
    weaknesses = detect_structural_weaknesses(
        company, icp_sectors=frozenset({"ecommerce", "retail"})
    )
    assert "sector_outside_icp" in _codes(weaknesses)


def test_dossier_estimate_flags_and_ranges() -> None:
    company = {
        "company_name": "شركة مثال",
        "sector": "ecommerce",
        "city": "Riyadh",
        "source": "founder_network",
        "manual_priority": True,
        "relationship_status": "warm_intro",
        "last_contact_days": 90,
    }
    dossier = build_company_dossier(
        company, icp_sectors=frozenset({"ecommerce"})
    )
    assert dossier["icp_fit"]["is_estimate"] is True
    assert dossier["data_quality"]["is_estimate"] is True
    assert 0 <= dossier["priority_score"] <= 100
    assert dossier["priority_band"] in ("P0", "P1", "P2", "P3")
    assert dossier["recommended_offer"] in {
        e["implied_offer"] for e in WEAKNESS_CATALOG.values()
    } | {"diagnostic"}
    assert dossier["assumptions"]
    assert dossier["governance"]["draft_only"] is True


def test_priority_band_thresholds() -> None:
    strong = build_company_dossier(
        {
            "company_name": "Strong",
            "sector": "ecommerce",
            "city": "Riyadh",
            "source": "founder_network",
            "manual_priority": True,
            "relationship_status": "contracted",
            "employee_count": 250,
            "notes": "x" * 50,
            "last_contact_days": 5,
        },
        icp_sectors=frozenset({"ecommerce"}),
        icp_cities=frozenset({"riyadh"}),
    )
    assert strong["priority_score"] >= 60
    assert strong["priority_band"] in ("P0", "P1")


def test_recommended_offer_derived_from_highest_severity() -> None:
    company = {
        "company_name": "Acme",
        "sector": "ecommerce",
        "city": "Riyadh",
        "source": "founder_network",
        "declared_weaknesses": ["no_followup_owner"],
    }
    dossier = build_company_dossier(company)
    # no_followup_owner is high severity -> managed_ops
    assert dossier["recommended_offer"] == "managed_ops"


def test_declared_weaknesses_marked_hypothesis() -> None:
    signals = declared_weaknesses_to_signals(
        {"company_name": "Acme", "declared_weaknesses": ["no_proof"]}
    )
    assert signals
    assert all(s["is_hypothesis"] is True for s in signals)
    assert all(s["evidence"] == "declared_by_operator" for s in signals)


def test_split_declared_weaknesses_ignores_unknown() -> None:
    known, ignored = split_declared_weaknesses(
        {"company_name": "Acme", "declared_weaknesses": ["no_proof", "bogus_code"]}
    )
    assert _codes(known) == {"no_proof"}
    assert ignored == ["bogus_code"]


def test_draft_raises_on_scraping() -> None:
    company = {"company_name": "Acme"}
    dossier = build_company_dossier(company)
    with pytest.raises(ValueError):
        build_target_company_draft(company, dossier, request_scraping=True)


def test_draft_raises_on_cold_whatsapp() -> None:
    company = {"company_name": "Acme"}
    dossier = build_company_dossier(company)
    with pytest.raises(ValueError):
        build_target_company_draft(company, dossier, request_cold_whatsapp=True)


def test_draft_default_is_draft_only() -> None:
    company = {
        "company_name": "Acme",
        "sector": "ecommerce",
        "city": "Riyadh",
        "source": "founder_network",
    }
    dossier = build_company_dossier(company)
    draft = build_target_company_draft(company, dossier)
    assert draft["draft_only"] is True
    assert draft["approval_required"] is True
    assert draft["angle_ar"]
    assert draft["angle_en"]


def test_no_fabricated_numbers_for_minimal_company() -> None:
    dossier = build_company_dossier({"company_name": "Acme"})
    # completeness reflects missing fields (1 of 4 keys) — not an invented high number.
    assert dossier["data_quality"]["completeness_pct"] == 25.0
    assert "missing_source" in dossier["icp_fit"]["risks"]


def test_unsourced_public_observations_dropped() -> None:
    company = {
        "company_name": "Acme",
        "source": "founder_network",
        "public_observations": [
            {"observation": "expanding", "source": ""},
            {"observation": "hiring", "source": "company blog"},
        ],
    }
    dossier = build_company_dossier(company)
    obs = dossier["public_observations"]
    assert len(obs) == 1
    assert obs[0]["source"] == "company blog"
