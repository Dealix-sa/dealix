"""Tests for the normalize_sector_playbook adapter.

Verifies that operational SectorPlaybook records are correctly bridged
to CanonicalPlaybookVersion without escalating authority.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalPlaybookVersion,
    PlaybookApprovalStatus,
)
from dealix.company_intelligence.playbook_adapter import normalize_sector_playbook


def _playbook(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed SectorPlaybook-like object."""
    values: dict[str, object] = {
        "sector_id": "b2b_saas",
        "sector_ar": "برمجيات B2B",
        "sector_en": "B2B SaaS",
        "pain_points_ar": (
            "صعوبة جلب عملاء بدون فريق مبيعات",
            "عدم وجود نظام CRM فعّال",
        ),
        "top_objections": ("OBJ_TRUST_001", "OBJ_PRICE_001"),
        "opening_lines_ar": (
            "لاحظنا أنكم تبحثون عن حلول لإدارة العلاقات مع العملاء",
        ),
        "best_offer_angle_ar": "نظام يدير العمليات التجارية بالكامل",
        "buying_committee": ("CEO", "VP Sales"),
        "seasonal_peaks_ar": ("Q1", "Q3"),
        "benchmarks": {
            "reply_rate_p50": 0.074,
            "meeting_rate_p50": 0.32,
            "win_rate_p50": 0.18,
            "cycle_days_p50": 45,
        },
        "recommended_channel_mix": {
            "whatsapp": 0.55,
            "email": 0.25,
            "linkedin": 0.10,
            "phone": 0.10,
        },
        "whatsapp_tone": "warm",
        "case_study_template_ar": "شركة {brand} استخدمت Dealix لمدة {months} شهر",
        "avg_deal_value_sar": 50_000,
        "avg_cycle_days": 45,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Basic normalization
# ---------------------------------------------------------------------------


class TestNormalizeSectorPlaybookBasic:
    """Core normalization behavior."""

    def test_produces_canonical_playbook(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="tenant-a"
        )
        assert isinstance(result, CanonicalPlaybookVersion)
        assert result.tenant_id == "tenant-a"

    def test_always_proposed_status(self) -> None:
        """The adapter never auto-approves a playbook."""
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        assert result.approval_status == PlaybookApprovalStatus.PROPOSED

    def test_frozen_immutability(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        with pytest.raises(Exception):
            result.approval_status = PlaybookApprovalStatus.APPROVED  # type: ignore[misc]

    def test_version_default_is_1(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        assert result.version == 1

    def test_version_override(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t", version=2
        )
        assert result.version == 2

    def test_source_id_default(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        assert result.source_id == "sector_playbooks"

    def test_source_id_override(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t", source_id="manual"
        )
        assert result.source_id == "manual"


# ---------------------------------------------------------------------------
# Playbook name
# ---------------------------------------------------------------------------


class TestPlaybookName:
    """Verify playbook name construction from sector identifiers."""

    def test_includes_sector_id(self) -> None:
        result = normalize_sector_playbook(
            _playbook(sector_id="logistics"), tenant_id="t"
        )
        assert "logistics" in result.playbook_name

    def test_includes_sector_en(self) -> None:
        result = normalize_sector_playbook(
            _playbook(sector_en="Real Estate"), tenant_id="t"
        )
        assert "Real Estate" in result.playbook_name

    def test_without_sector_en(self) -> None:
        result = normalize_sector_playbook(
            _playbook(sector_en=""), tenant_id="t"
        )
        assert result.playbook_name.startswith("sector:")


# ---------------------------------------------------------------------------
# Evidence references
# ---------------------------------------------------------------------------


class TestEvidenceRefs:
    """Verify evidence reference derivation from playbook data."""

    def test_benchmarks_included(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        benchmark_refs = [r for r in result.evidence_refs if r.startswith("benchmark:")]
        assert len(benchmark_refs) == 4

    def test_objection_coverage(self) -> None:
        result = normalize_sector_playbook(
            _playbook(top_objections=("OBJ_1", "OBJ_2", "OBJ_3")),
            tenant_id="t",
        )
        assert "objection_coverage:3" in result.evidence_refs

    def test_case_study_present(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        assert "case_study_template:present" in result.evidence_refs

    def test_channel_mix_included(self) -> None:
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        channel_refs = [r for r in result.evidence_refs if r.startswith("channel_mix:")]
        assert len(channel_refs) == 1

    def test_minimal_playbook_gets_manual_observation(self) -> None:
        """A playbook with no data still gets at least one evidence ref."""
        minimal = SimpleNamespace(
            sector_id="unknown",
            sector_ar="",
            sector_en="",
            benchmarks={},
            top_objections=(),
            case_study_template_ar="",
            recommended_channel_mix={},
        )
        result = normalize_sector_playbook(minimal, tenant_id="t")
        assert "manual_observation" in result.evidence_refs


# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------


class TestConfidence:
    """Verify confidence derivation from data quality signals."""

    def test_full_playbook_high_confidence(self) -> None:
        """A complete playbook should have ≥ 0.8 confidence."""
        result = normalize_sector_playbook(
            _playbook(), tenant_id="t"
        )
        assert result.confidence >= 0.8

    def test_minimal_playbook_low_confidence(self) -> None:
        minimal = SimpleNamespace(
            sector_id="empty",
            sector_ar="",
            sector_en="",
            benchmarks={},
            top_objections=(),
            case_study_template_ar="",
            recommended_channel_mix={},
        )
        result = normalize_sector_playbook(minimal, tenant_id="t")
        assert result.confidence <= 0.3

    def test_partial_benchmarks_moderate_confidence(self) -> None:
        partial = SimpleNamespace(
            sector_id="partial",
            sector_ar="",
            sector_en="",
            benchmarks={"reply_rate_p50": 0.05, "win_rate_p50": 0.1},
            top_objections=("OBJ_1",),
            case_study_template_ar="",
            recommended_channel_mix={},
        )
        result = normalize_sector_playbook(partial, tenant_id="t")
        assert 0.3 < result.confidence < 0.8


# ---------------------------------------------------------------------------
# Description and changes summary
# ---------------------------------------------------------------------------


class TestDescription:
    """Verify description and changes summary composition."""

    def test_description_includes_sector_en(self) -> None:
        result = normalize_sector_playbook(
            _playbook(sector_en="Hospitality"), tenant_id="t"
        )
        assert "Hospitality" in result.description

    def test_description_includes_sector_ar(self) -> None:
        result = normalize_sector_playbook(
            _playbook(sector_ar="فنادق"), tenant_id="t"
        )
        assert "فنادق" in result.description

    def test_changes_summary_includes_pain_points_count(self) -> None:
        result = normalize_sector_playbook(
            _playbook(pain_points_ar=("point 1", "point 2", "point 3")),
            tenant_id="t",
        )
        assert "3 pain points" in result.changes_summary

    def test_changes_summary_includes_primary_channel(self) -> None:
        result = normalize_sector_playbook(
            _playbook(recommended_channel_mix={"whatsapp": 0.7, "email": 0.3}),
            tenant_id="t",
        )
        assert "whatsapp" in result.changes_summary

    def test_changes_summary_includes_avg_deal(self) -> None:
        result = normalize_sector_playbook(
            _playbook(avg_deal_value_sar=120_000), tenant_id="t"
        )
        assert "120000 SAR" in result.changes_summary

    def test_change_reason_includes_sector_id(self) -> None:
        result = normalize_sector_playbook(
            _playbook(sector_id="logistics"), tenant_id="t"
        )
        assert "logistics" in result.change_reason


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Verify deterministic playbook_version_id generation."""

    def test_same_inputs_same_id(self) -> None:
        a = normalize_sector_playbook(_playbook(), tenant_id="t")
        b = normalize_sector_playbook(_playbook(), tenant_id="t")
        assert a.playbook_version_id == b.playbook_version_id

    def test_different_tenant_different_id(self) -> None:
        a = normalize_sector_playbook(_playbook(), tenant_id="t1")
        b = normalize_sector_playbook(_playbook(), tenant_id="t2")
        assert a.playbook_version_id != b.playbook_version_id

    def test_different_version_different_id(self) -> None:
        a = normalize_sector_playbook(_playbook(), tenant_id="t", version=1)
        b = normalize_sector_playbook(_playbook(), tenant_id="t", version=2)
        assert a.playbook_version_id != b.playbook_version_id


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    """Verify input validation."""

    def test_rejects_empty_sector_id(self) -> None:
        with pytest.raises(ValueError, match="sector_id"):
            normalize_sector_playbook(
                _playbook(sector_id=""), tenant_id="t"
            )

    def test_accepts_missing_optional_fields(self) -> None:
        """Only sector_id is required — other fields gracefully degrade."""
        minimal = SimpleNamespace(sector_id="test")
        result = normalize_sector_playbook(minimal, tenant_id="t")
        assert isinstance(result, CanonicalPlaybookVersion)
