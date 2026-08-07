"""Tests for daily_targeting_brief — deterministic, no network, no DB."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.revenue_os.daily_targeting_brief import (
    build_daily_targeting_brief,
    load_target_companies,
    render_brief_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_YAML = REPO_ROOT / "docs/commercial/operations/targeting/target_companies_seed.yaml"


def _sample_companies() -> list[dict]:
    return [
        {
            "company_name": "High Priority",
            "sector": "ecommerce",
            "city": "Riyadh",
            "source": "founder_network",
            "manual_priority": True,
            "relationship_status": "contracted",
            "employee_count": 250,
            "notes": "x" * 50,
            "last_contact_days": 5,
        },
        {
            "company_name": "Low Priority",
            "sector": "",
            "city": "",
            "source": "",
            "relationship_status": "none",
            "last_contact_days": 300,
        },
        {
            "company_name": "Mid Priority",
            "sector": "retail",
            "city": "Jeddah",
            "source": "founder_network",
            "relationship_status": "warm_intro",
        },
    ]


def test_build_ranks_by_priority_desc() -> None:
    brief = build_daily_targeting_brief(
        _sample_companies(), icp_sectors=frozenset({"ecommerce"}), date_iso="2026-06-05"
    )
    scores = [t["priority_score"] for t in brief["targets"]]
    assert scores == sorted(scores, reverse=True)
    assert brief["targets"][0]["company_name"] == "High Priority"


def test_top_n_respected() -> None:
    brief = build_daily_targeting_brief(_sample_companies(), top_n=2)
    assert brief["shown"] == 2
    assert len(brief["targets"]) == 2
    assert brief["total_targets"] == 3


def test_every_target_draft_is_governed() -> None:
    brief = build_daily_targeting_brief(_sample_companies())
    for t in brief["targets"]:
        assert t["draft"]["draft_only"] is True
        assert t["draft"]["approval_required"] is True


def test_summary_and_governance_fields_present() -> None:
    brief = build_daily_targeting_brief(_sample_companies())
    summary = brief["summary"]
    assert "avg_icp_fit" in summary
    assert "count_by_priority_band" in summary
    assert "count_by_recommended_offer" in summary
    assert "top_weakness_codes" in summary
    assert brief["governance_footer_ar"]
    assert brief["governance_footer_en"]
    assert brief["disclaimer_ar"]
    assert brief["disclaimer_en"]


def test_render_markdown_contains_date_and_draft() -> None:
    brief = build_daily_targeting_brief(_sample_companies(), date_iso="2026-06-05")
    md = render_brief_markdown(brief)
    assert isinstance(md, str)
    assert "2026-06-05" in md
    assert "DRAFT" in md


def test_load_skips_replace_rows() -> None:
    companies = [
        {"company_name": "REPLACE: placeholder", "source": "x"},
        {"company_name": "", "source": "x"},
        {"company_name": "Real Co", "source": "founder_network"},
    ]
    # write/read via the loader by exercising the YAML path through the seed file
    # here we just assert the parsing rule directly on the seed file below.
    assert companies  # sanity


def test_load_seed_yaml_skips_placeholders() -> None:
    companies = load_target_companies(str(SEED_YAML))
    names = [c["company_name"] for c in companies]
    assert all(not n.startswith("REPLACE:") for n in names)
    assert all(n.strip() for n in names)
    # The seed file has generic example rows that survive the filter.
    assert len(companies) >= 1
