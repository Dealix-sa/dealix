"""Tests for company.client_delivery — intake, diagnostic, proposal, plan."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from company.client_delivery.intake_flow import create_client, _slugify, VALID_SECTORS, VALID_PACKAGES
from company.client_delivery.diagnostic_generator import (
    generate_diagnostic,
    calculate_leakage,
    _auto_recommend,
)
from company.client_delivery.proposal_generator import generate_proposal
from company.client_delivery.implementation_plan import generate_plan


# ── helpers ───────────────────────────────────────────────────────────────────

def _write_intake(client_dir: Path, slug: str, **overrides) -> dict:
    """Write a minimal intake.json file under client_dir/slug/intake.json."""
    base = {
        "client_slug": slug,
        "company_name": "Test Co",
        "sector": "logistics",
        "contact_name": "علي",
        "contact_phone": "+966501234567",
        "contact_email": "ali@testco.sa",
        "package": "diagnostic_sprint",
        "weekly_leads": 50,
        "notes": "",
        "intake_date": date.today().isoformat(),
        "status": "active",
        "diagnostic_start": None,
        "diagnostic_end": None,
        "pilot_start": None,
        "pilot_end": None,
        "retainer_start": None,
    }
    base.update(overrides)
    slug_dir = client_dir / slug
    slug_dir.mkdir(parents=True, exist_ok=True)
    (slug_dir / "intake.json").write_text(json.dumps(base, ensure_ascii=False))
    return base


# ── _slugify ──────────────────────────────────────────────────────────────────

class TestSlugify:
    def test_basic_ascii(self):
        assert _slugify("Hello World") == "hello-world"

    def test_arabic_chars_pass_through(self):
        slug = _slugify("شركة النور")
        assert len(slug) > 0
        assert " " not in slug

    def test_max_length_40(self):
        long_name = "A" * 100
        assert len(_slugify(long_name)) <= 40

    def test_special_chars_stripped(self):
        slug = _slugify("Test@Co! Ltd.")
        assert "@" not in slug
        assert "!" not in slug


# ── create_client ─────────────────────────────────────────────────────────────

class TestCreateClient:
    def test_valid_client_created(self, tmp_path):
        with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
            intake = create_client(
                name="شركة الأفق",
                sector="logistics",
                contact="أحمد",
                phone="+966501234567",
                email="ahmed@ufq.sa",
                package="diagnostic_sprint",
                weekly_leads=80,
            )
        assert intake["company_name"] == "شركة الأفق"
        assert intake["sector"] == "logistics"
        assert intake["package"] == "diagnostic_sprint"
        assert intake["weekly_leads"] == 80
        assert intake["status"] == "active"

    def test_intake_json_written(self, tmp_path):
        with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
            intake = create_client(
                name="Test Inc",
                sector="technology",
                contact="Sara",
                phone="+966509999999",
                email="sara@test.sa",
                package="micro_sprint",
            )
        slug = intake["client_slug"]
        intake_file = tmp_path / slug / "intake.json"
        assert intake_file.exists()
        loaded = json.loads(intake_file.read_text())
        assert loaded["company_name"] == "Test Inc"

    def test_checklist_written(self, tmp_path):
        with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
            intake = create_client(
                name="Checklist Co",
                sector="retail",
                contact="Omar",
                phone="+966501111111",
                email="omar@co.sa",
                package="data_pack",
            )
        slug = intake["client_slug"]
        checklist = tmp_path / slug / "intake_checklist.md"
        assert checklist.exists()

    def test_invalid_sector_raises(self, tmp_path):
        with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
            with pytest.raises(ValueError, match="sector"):
                create_client(
                    name="Bad Sector",
                    sector="invalid_sector_xyz",
                    contact="X",
                    phone="+966500000000",
                    email="x@y.sa",
                    package="micro_sprint",
                )

    def test_invalid_package_raises(self, tmp_path):
        with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
            with pytest.raises(ValueError, match="package"):
                create_client(
                    name="Bad Package",
                    sector="retail",
                    contact="X",
                    phone="+966500000000",
                    email="x@y.sa",
                    package="unknown_package_xyz",
                )

    def test_all_valid_sectors_accepted(self, tmp_path):
        for i, sector in enumerate(VALID_SECTORS):
            with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
                intake = create_client(
                    name=f"Co {i}",
                    sector=sector,
                    contact="Test",
                    phone="+966500000000",
                    email="t@t.sa",
                    package="free_diagnostic",
                )
            assert intake["sector"] == sector

    def test_all_valid_packages_accepted(self, tmp_path):
        for i, pkg in enumerate(VALID_PACKAGES):
            with patch("company.client_delivery.intake_flow.CLIENTS_DIR", tmp_path):
                intake = create_client(
                    name=f"PkgCo {i}",
                    sector="retail",
                    contact="Test",
                    phone="+966500000000",
                    email="t@t.sa",
                    package=pkg,
                )
            assert intake["package"] == pkg


# ── calculate_leakage ─────────────────────────────────────────────────────────

class TestCalculateLeakage:
    def test_basic_metrics_present(self):
        m = calculate_leakage(
            leads_total=100,
            leads_quoted=60,
            leads_closed=24,
            avg_deal_size=10000,
            followup_delay_days=1,
        )
        assert "quote_rate_pct" in m
        assert "close_rate_pct" in m
        assert "leakage_estimate_sar" in m

    def test_zero_leads_no_crash(self):
        m = calculate_leakage(
            leads_total=0,
            leads_quoted=0,
            leads_closed=0,
            avg_deal_size=10000,
            followup_delay_days=1,
        )
        assert m["leads_total"] == 0
        assert m["leakage_estimate_sar"] >= 0

    def test_no_leakage_at_benchmark(self):
        m = calculate_leakage(
            leads_total=100,
            leads_quoted=60,
            leads_closed=24,
            avg_deal_size=10000,
            followup_delay_days=0,
        )
        assert m["leakage_estimate_sar"] == 0

    def test_leakage_positive_below_benchmark(self):
        m = calculate_leakage(
            leads_total=100,
            leads_quoted=30,  # below 60% benchmark
            leads_closed=5,
            avg_deal_size=10000,
            followup_delay_days=3,
        )
        assert m["leakage_estimate_sar"] > 0

    def test_delay_cost_proportional(self):
        m1 = calculate_leakage(100, 60, 24, 10000, followup_delay_days=1)
        m2 = calculate_leakage(100, 60, 24, 10000, followup_delay_days=2)
        assert m2["delay_cost_sar"] > m1["delay_cost_sar"]


# ── generate_diagnostic ───────────────────────────────────────────────────────

class TestGenerateDiagnostic:
    def test_returns_dict_with_required_keys(self, tmp_path):
        slug = "test-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.diagnostic_generator.CLIENTS_DIR", tmp_path):
            result = generate_diagnostic(
                slug=slug,
                leads_total=100,
                leads_quoted=50,
                leads_closed=20,
                avg_deal_size=8000,
                followup_delay_days=2,
                gaps=["بطء المتابعة", "غياب نظام CRM"],
            )
        assert result["company_name"] == "Test Co"
        assert "metrics" in result
        assert "gaps" in result
        assert "top_priorities" in result

    def test_diagnostic_json_written(self, tmp_path):
        slug = "test-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.diagnostic_generator.CLIENTS_DIR", tmp_path):
            generate_diagnostic(
                slug=slug,
                leads_total=100,
                leads_quoted=50,
                leads_closed=20,
                avg_deal_size=8000,
                followup_delay_days=2,
                gaps=["gap1"],
            )
        diag_file = tmp_path / slug / "diagnostic" / "diagnostic.json"
        assert diag_file.exists()
        data = json.loads(diag_file.read_text())
        assert data["company_name"] == "Test Co"

    def test_report_markdown_written(self, tmp_path):
        slug = "test-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.diagnostic_generator.CLIENTS_DIR", tmp_path):
            generate_diagnostic(
                slug=slug,
                leads_total=80,
                leads_quoted=40,
                leads_closed=10,
                avg_deal_size=5000,
                followup_delay_days=3,
                gaps=["gap"],
            )
        report = tmp_path / slug / "diagnostic" / "DIAGNOSTIC_REPORT.md"
        assert report.exists()


class TestAutoRecommend:
    def test_low_quote_rate_recommends_whatsapp(self):
        m = {"quote_rate_pct": 30, "followup_delay_days": 1}
        rec = _auto_recommend(m, "logistics")
        assert "WhatsApp" in rec

    def test_high_delay_recommends_crm(self):
        m = {"quote_rate_pct": 55, "followup_delay_days": 5}
        rec = _auto_recommend(m, "retail")
        assert "CRM" in rec or "Command" in rec


# ── generate_proposal ─────────────────────────────────────────────────────────

class TestGenerateProposal:
    def test_returns_proposal_with_price(self, tmp_path):
        slug = "prop-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.proposal_generator.CLIENTS_DIR", tmp_path):
            result = generate_proposal(
                slug=slug,
                package="diagnostic_sprint",
                price_sar=7500,
            )
        assert result["price_sar"] == 7500
        assert result["company_name"] == "Test Co"

    def test_proposal_json_written(self, tmp_path):
        slug = "prop-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.proposal_generator.CLIENTS_DIR", tmp_path):
            generate_proposal(slug=slug, package="micro_sprint", price_sar=499)
        proposals_dir = tmp_path / slug / "proposals"
        assert proposals_dir.exists()
        json_files = list(proposals_dir.glob("*.json"))
        assert len(json_files) == 1

    def test_proposal_markdown_written(self, tmp_path):
        slug = "prop-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.proposal_generator.CLIENTS_DIR", tmp_path):
            generate_proposal(slug=slug, package="data_pack", price_sar=1500)
        proposals_dir = tmp_path / slug / "proposals"
        md_files = list(proposals_dir.glob("*.md"))
        assert len(md_files) == 1

    def test_missing_client_raises(self, tmp_path):
        with patch("company.client_delivery.proposal_generator.CLIENTS_DIR", tmp_path):
            with pytest.raises(FileNotFoundError):
                generate_proposal(slug="nonexistent-slug", package="micro_sprint", price_sar=499)

    def test_valid_until_30_days_out(self, tmp_path):
        slug = "prop-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.proposal_generator.CLIENTS_DIR", tmp_path):
            result = generate_proposal(slug=slug, package="managed_ops", price_sar=2999)
        issue = date.fromisoformat(result["issue_date"])
        valid = date.fromisoformat(result["valid_until"])
        assert (valid - issue).days == 30


# ── generate_plan ─────────────────────────────────────────────────────────────

class TestGeneratePlan:
    def test_returns_plan_with_two_weeks(self, tmp_path):
        slug = "plan-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.implementation_plan.CLIENTS_DIR", tmp_path):
            result = generate_plan(
                slug=slug,
                system="whatsapp_revenue_os",
                start_date=date.today(),
            )
        assert "week1_tasks" in result
        assert "week2_tasks" in result
        assert len(result["week1_tasks"]) > 0
        assert len(result["week2_tasks"]) > 0

    def test_plan_dates_sequential(self, tmp_path):
        slug = "plan-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.implementation_plan.CLIENTS_DIR", tmp_path):
            result = generate_plan(slug=slug, system="whatsapp_revenue_os", start_date=date.today())
        assert result["start_date"] < result["end_date"]

    def test_unknown_system_uses_default(self, tmp_path):
        slug = "plan-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.implementation_plan.CLIENTS_DIR", tmp_path):
            result = generate_plan(slug=slug, system="completely_unknown_system_xyz", start_date=date.today())
        assert result["week1_tasks"]

    def test_plan_json_written(self, tmp_path):
        slug = "plan-co"
        _write_intake(tmp_path, slug)
        with patch("company.client_delivery.implementation_plan.CLIENTS_DIR", tmp_path):
            generate_plan(slug=slug, system="whatsapp_revenue_os", start_date=date.today())
        plan_file = tmp_path / slug / "implementation" / "plan.json"
        assert plan_file.exists()

    def test_missing_client_raises(self, tmp_path):
        with patch("company.client_delivery.implementation_plan.CLIENTS_DIR", tmp_path):
            with pytest.raises(FileNotFoundError):
                generate_plan(slug="ghost-client", system="whatsapp_revenue_os", start_date=date.today())
