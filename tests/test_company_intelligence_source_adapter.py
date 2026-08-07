"""Tests for the normalize_source_passport adapter.

Verifies that operational SourcePassport records are correctly bridged to
CanonicalSource without escalating authority.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalSource,
    SourcePolicyStatus,
    SourceStatus,
    SourceType,
)
from dealix.company_intelligence.source_adapter import normalize_source_passport


def _passport(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed SourcePassport-like object."""
    values: dict[str, object] = {
        "source_id": "SRC-001",
        "source_type": "client_upload",
        "owner": "client",
        "allowed_use": ["internal_analysis", "draft_only"],
        "contains_pii": True,
        "sensitivity": "medium",
        "relationship_status": "existing_relationship",
        "retention_policy": "project_duration",
        "ai_access_allowed": True,
        "external_use_allowed": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Basic normalization
# ---------------------------------------------------------------------------


class TestNormalizeSourcePassportBasic:
    """Core normalization behavior."""

    def test_produces_canonical_source(self) -> None:
        source = normalize_source_passport(
            _passport(), tenant_id="tenant-a"
        )
        assert isinstance(source, CanonicalSource)
        assert source.tenant_id == "tenant-a"
        assert source.source_type == SourceType.CLIENT_PROVIDED
        assert source.name == "client_upload:client"

    def test_description_contains_source_id(self) -> None:
        source = normalize_source_passport(
            _passport(), tenant_id="t"
        )
        assert "SRC-001" in source.description

    def test_confidence_starts_neutral(self) -> None:
        source = normalize_source_passport(
            _passport(), tenant_id="t"
        )
        assert source.confidence == 0.5

    def test_deduplication_key_from_source_id(self) -> None:
        source = normalize_source_passport(
            _passport(), tenant_id="t"
        )
        assert source.deduplication_key == "SRC-001"

    def test_frozen_immutability(self) -> None:
        source = normalize_source_passport(
            _passport(), tenant_id="t"
        )
        with pytest.raises(Exception):
            source.name = "tampered"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Source type mapping
# ---------------------------------------------------------------------------


class TestSourceTypeMapping:
    """Verify operational source type → canonical SourceType mapping."""

    @pytest.mark.parametrize(
        ("raw_type", "expected"),
        [
            ("client_upload", SourceType.CLIENT_PROVIDED),
            ("client_provided", SourceType.CLIENT_PROVIDED),
            ("client_data", SourceType.CLIENT_PROVIDED),
            ("crm", SourceType.CRM),
            ("crm_export", SourceType.CRM),
            ("hubspot", SourceType.CRM),
            ("salesforce", SourceType.CRM),
            ("pipedrive", SourceType.CRM),
            ("email", SourceType.EMAIL),
            ("email_inbox", SourceType.EMAIL),
            ("internal", SourceType.INTERNAL_SYSTEM),
            ("internal_system", SourceType.INTERNAL_SYSTEM),
            ("dealix", SourceType.INTERNAL_SYSTEM),
            ("owned", SourceType.OWNED),
            ("google_api", SourceType.PUBLIC_REGISTRY),
            ("google_places", SourceType.PUBLIC_REGISTRY),
            ("google_maps", SourceType.PUBLIC_REGISTRY),
            ("government_registry", SourceType.PUBLIC_REGISTRY),
            ("cr_registry", SourceType.PUBLIC_REGISTRY),
            ("company_website", SourceType.COMPANY_WEBSITE),
            ("website", SourceType.COMPANY_WEBSITE),
            ("open_data", SourceType.OPEN_DATA),
            ("public", SourceType.OPEN_DATA),
            ("news", SourceType.NEWS),
            ("news_feed", SourceType.NEWS),
            ("jobs", SourceType.JOBS),
            ("job_board", SourceType.JOBS),
            ("event", SourceType.EVENT),
            ("conference", SourceType.EVENT),
            ("partner", SourceType.PARTNER),
            ("referral", SourceType.PARTNER),
            ("warm_intro", SourceType.PARTNER),
            ("manual", SourceType.MANUAL),
            ("csv", SourceType.MANUAL),
            ("form", SourceType.MANUAL),
            ("api", SourceType.INTERNAL_SYSTEM),
            ("whatsapp", SourceType.OWNED),
        ],
    )
    def test_source_type_mapping(self, raw_type: str, expected: SourceType) -> None:
        source = normalize_source_passport(
            _passport(source_type=raw_type), tenant_id="t"
        )
        assert source.source_type == expected

    def test_unknown_type_fallback_to_manual(self) -> None:
        source = normalize_source_passport(
            _passport(source_type="magic_crystal_ball"), tenant_id="t"
        )
        assert source.source_type == SourceType.MANUAL

    def test_case_insensitive_mapping(self) -> None:
        source = normalize_source_passport(
            _passport(source_type="CRM_Export"), tenant_id="t"
        )
        assert source.source_type == SourceType.CRM


# ---------------------------------------------------------------------------
# Policy status derivation
# ---------------------------------------------------------------------------


class TestPolicyStatus:
    """Verify policy status is derived correctly from passport fields."""

    def test_ai_access_blocked_produces_blocked(self) -> None:
        source = normalize_source_passport(
            _passport(ai_access_allowed=False), tenant_id="t"
        )
        assert source.policy_status == SourcePolicyStatus.BLOCKED
        assert source.status == SourceStatus.BLOCKED

    def test_pii_with_no_external_produces_review_required(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=True,
                external_use_allowed=False,
                allowed_use=["draft_only"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.REVIEW_REQUIRED

    def test_pii_with_analysis_no_external_produces_research_only(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=True,
                external_use_allowed=False,
                allowed_use=["internal_analysis"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.RESEARCH_ONLY

    def test_pii_with_approval_no_external_still_research_only(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=True,
                external_use_allowed=False,
                allowed_use=["approved"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.RESEARCH_ONLY

    def test_no_pii_with_approval_and_external_produces_approved(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=False,
                external_use_allowed=True,
                allowed_use=["approved"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.APPROVED

    def test_no_pii_with_analysis_and_external_produces_research_only(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=False,
                external_use_allowed=True,
                allowed_use=["internal_analysis"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.RESEARCH_ONLY

    def test_pii_with_approval_and_external_capped_at_research_only(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=True,
                external_use_allowed=True,
                allowed_use=["approved"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.RESEARCH_ONLY

    def test_no_pii_no_approval_with_external_produces_review_required(self) -> None:
        source = normalize_source_passport(
            _passport(
                contains_pii=False,
                external_use_allowed=True,
                allowed_use=["draft_only"],
            ),
            tenant_id="t",
        )
        assert source.policy_status == SourcePolicyStatus.REVIEW_REQUIRED


# ---------------------------------------------------------------------------
# Sensitivity → freshness mapping
# ---------------------------------------------------------------------------


class TestFreshnessMapping:
    """Verify sensitivity → freshness_days mapping."""

    def test_high_sensitivity_short_freshness(self) -> None:
        source = normalize_source_passport(
            _passport(sensitivity="high"), tenant_id="t"
        )
        assert source.freshness_days == 30

    def test_medium_sensitivity_default_freshness(self) -> None:
        source = normalize_source_passport(
            _passport(sensitivity="medium"), tenant_id="t"
        )
        assert source.freshness_days == 90

    def test_low_sensitivity_long_freshness(self) -> None:
        source = normalize_source_passport(
            _passport(sensitivity="low"), tenant_id="t"
        )
        assert source.freshness_days == 180

    def test_unknown_sensitivity_default_freshness(self) -> None:
        source = normalize_source_passport(
            _passport(sensitivity="unknown"), tenant_id="t"
        )
        assert source.freshness_days == 90


# ---------------------------------------------------------------------------
# Retention policy mapping
# ---------------------------------------------------------------------------


class TestRetentionMapping:
    """Verify retention_policy → retention_days mapping."""

    def test_project_duration(self) -> None:
        source = normalize_source_passport(
            _passport(retention_policy="project_duration"), tenant_id="t"
        )
        assert source.retention_days == 90

    def test_one_year(self) -> None:
        source = normalize_source_passport(
            _passport(retention_policy="1_year"), tenant_id="t"
        )
        assert source.retention_days == 365

    def test_permanent(self) -> None:
        source = normalize_source_passport(
            _passport(retention_policy="permanent"), tenant_id="t"
        )
        assert source.retention_days == 730

    def test_unknown_retention_default(self) -> None:
        source = normalize_source_passport(
            _passport(retention_policy="custom"), tenant_id="t"
        )
        assert source.retention_days == 365


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestSourceDeterminism:
    """Verify deterministic source_id generation."""

    def test_same_passport_same_id(self) -> None:
        a = normalize_source_passport(_passport(), tenant_id="t")
        b = normalize_source_passport(_passport(), tenant_id="t")
        assert a.source_id == b.source_id

    def test_different_tenant_different_id(self) -> None:
        a = normalize_source_passport(_passport(), tenant_id="t1")
        b = normalize_source_passport(_passport(), tenant_id="t2")
        assert a.source_id != b.source_id

    def test_different_source_type_different_id(self) -> None:
        a = normalize_source_passport(
            _passport(source_type="crm"), tenant_id="t"
        )
        b = normalize_source_passport(
            _passport(source_type="email"), tenant_id="t"
        )
        assert a.source_id != b.source_id


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestSourceValidation:
    """Verify input validation."""

    def test_rejects_empty_source_id(self) -> None:
        with pytest.raises(ValueError, match="source_id"):
            normalize_source_passport(
                _passport(source_id=""), tenant_id="t"
            )

    def test_rejects_none_source_id(self) -> None:
        with pytest.raises(ValueError, match="source_id"):
            normalize_source_passport(
                _passport(source_id=None), tenant_id="t"
            )


# ---------------------------------------------------------------------------
# Allowed use derivation
# ---------------------------------------------------------------------------


class TestAllowedUseDerivation:
    """Verify allowed_use list → single canonical string."""

    def test_full_use_produces_approved(self) -> None:
        source = normalize_source_passport(
            _passport(
                allowed_use=["full_use"],
                contains_pii=False,
                external_use_allowed=True,
            ),
            tenant_id="t",
        )
        assert source.allowed_use == "approved"

    def test_internal_analysis_produces_internal_analysis(self) -> None:
        source = normalize_source_passport(
            _passport(allowed_use=["internal_analysis"]), tenant_id="t"
        )
        assert source.allowed_use == "internal_analysis"

    def test_draft_only_produces_draft_only(self) -> None:
        source = normalize_source_passport(
            _passport(allowed_use=["draft_only"]), tenant_id="t"
        )
        assert source.allowed_use == "draft_only"

    def test_empty_allowed_use_produces_research_only(self) -> None:
        source = normalize_source_passport(
            _passport(allowed_use=[]), tenant_id="t"
        )
        assert source.allowed_use == "research_only"

    def test_name_with_no_owner(self) -> None:
        source = normalize_source_passport(
            _passport(owner=""), tenant_id="t"
        )
        assert source.name == "client_upload"
