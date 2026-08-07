"""Tests for the canonical Source provenance contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence and quality score bounds
  - Policy enforcement (blocked sources)
  - Source scoring formula
  - Staleness detection
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.source_contracts import (
    CanonicalSource,
    SourcePolicyStatus,
    SourceStatus,
    SourceType,
    build_source,
    compute_source_score,
    is_source_stale,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _source(**overrides: object) -> CanonicalSource:
    """Build a minimal valid source, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        deduplication_key="dedup-1",
        name="Company Registry",
        source_type=SourceType.PUBLIC_REGISTRY,
    )
    defaults.update(overrides)
    return build_source(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _source()
        b = _source()
        assert a.source_id == b.source_id

    def test_different_deduplication_key_produces_different_id(self) -> None:
        a = _source(deduplication_key="dedup-1")
        b = _source(deduplication_key="dedup-2")
        assert a.source_id != b.source_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _source(tenant_id="tenant-a")
        b = _source(tenant_id="tenant-b")
        assert a.source_id != b.source_id

    def test_different_source_type_produces_different_id(self) -> None:
        a = _source(source_type=SourceType.PUBLIC_REGISTRY)
        b = _source(source_type=SourceType.CRM)
        assert a.source_id != b.source_id

    def test_source_id_format(self) -> None:
        a = _source()
        assert a.source_id.startswith("source_")
        assert len(a.source_id) == 7 + 16  # "source_" + 16 hex chars

    def test_whitespace_in_deduplication_key_is_stripped(self) -> None:
        a = _source(deduplication_key="  dedup-1  ")
        b = _source(deduplication_key="dedup-1")
        assert a.source_id == b.source_id

    def test_name_does_not_affect_id(self) -> None:
        """Source name is mutable metadata — it must not affect the stable ID."""
        a = _source(name="Company Registry")
        b = _source(name="Saudi Companies DB")
        assert a.source_id == b.source_id


# ---------------------------------------------------------------------------
# Quality scores
# ---------------------------------------------------------------------------


class TestQualityScores:
    def test_default_scores(self) -> None:
        a = _source()
        assert a.authority_score == 50
        assert a.verifiability_score == 50

    def test_authority_above_100_rejected(self) -> None:
        with pytest.raises(ValueError):
            _source(authority_score=101)

    def test_authority_below_0_rejected(self) -> None:
        with pytest.raises(ValueError):
            _source(authority_score=-1)

    def test_verifiability_above_100_rejected(self) -> None:
        with pytest.raises(ValueError):
            _source(verifiability_score=101)

    def test_confidence_bounds(self) -> None:
        a = _source(confidence=0.0)
        assert a.confidence == 0.0
        b = _source(confidence=1.0)
        assert b.confidence == 1.0
        with pytest.raises(ValueError):
            _source(confidence=1.5)
        with pytest.raises(ValueError):
            _source(confidence=-0.1)


# ---------------------------------------------------------------------------
# Policy enforcement
# ---------------------------------------------------------------------------


class TestPolicyEnforcement:
    def test_default_policy_is_review_required(self) -> None:
        a = _source()
        assert a.policy_status == SourcePolicyStatus.REVIEW_REQUIRED

    def test_blocked_source_cannot_be_active(self) -> None:
        a = _source()
        data = a.model_dump()
        data["policy_status"] = SourcePolicyStatus.BLOCKED
        data["status"] = SourceStatus.ACTIVE
        with pytest.raises(ValueError, match="blocked sources"):
            CanonicalSource(**data)

    def test_blocked_source_can_be_blocked_status(self) -> None:
        a = _source(
            policy_status=SourcePolicyStatus.BLOCKED,
            status=SourceStatus.BLOCKED,
        )
        assert a.policy_status == SourcePolicyStatus.BLOCKED
        assert a.status == SourceStatus.BLOCKED

    def test_approved_source_can_be_active(self) -> None:
        a = _source(policy_status=SourcePolicyStatus.APPROVED)
        assert a.status == SourceStatus.ACTIVE


# ---------------------------------------------------------------------------
# Source scoring
# ---------------------------------------------------------------------------


class TestSourceScoring:
    def test_blocked_source_scores_zero(self) -> None:
        a = _source(
            policy_status=SourcePolicyStatus.BLOCKED,
            status=SourceStatus.BLOCKED,
        )
        assert compute_source_score(a) == 0

    def test_approved_with_reviewed_terms(self) -> None:
        now = datetime.now(UTC)
        a = _source(
            policy_status=SourcePolicyStatus.APPROVED,
            authority_score=80,
            verifiability_score=70,
            terms_reviewed_at=now - timedelta(days=30),
        )
        # (80*0.35) + (70*0.30) + (100*0.25) + (100*0.10)
        # = 28 + 21 + 25 + 10 = 84
        assert compute_source_score(a, now=now) == 84

    def test_research_only_without_terms_review(self) -> None:
        a = _source(
            policy_status=SourcePolicyStatus.RESEARCH_ONLY,
            authority_score=60,
            verifiability_score=60,
        )
        # (60*0.35) + (60*0.30) + (70*0.25) + (40*0.10)
        # = 21 + 18 + 17.5 + 4 = 60.5 → 60
        assert compute_source_score(a) == 60

    def test_stale_terms_reduce_score(self) -> None:
        now = datetime.now(UTC)
        a = _source(
            policy_status=SourcePolicyStatus.APPROVED,
            authority_score=80,
            verifiability_score=70,
            terms_reviewed_at=now - timedelta(days=400),
        )
        # (80*0.35) + (70*0.30) + (100*0.25) + (60*0.10)
        # = 28 + 21 + 25 + 6 = 80
        assert compute_source_score(a, now=now) == 80


# ---------------------------------------------------------------------------
# Staleness detection
# ---------------------------------------------------------------------------


class TestStalenessDetection:
    def test_fresh_source_is_not_stale(self) -> None:
        now = datetime.now(UTC)
        a = _source(retrieved_at=now, freshness_days=90)
        assert is_source_stale(a, now=now) is False

    def test_old_source_is_stale(self) -> None:
        now = datetime.now(UTC)
        a = _source(
            retrieved_at=now - timedelta(days=100),
            freshness_days=90,
        )
        assert is_source_stale(a, now=now) is True

    def test_exact_boundary_is_not_stale(self) -> None:
        now = datetime.now(UTC)
        a = _source(
            retrieved_at=now - timedelta(days=90),
            freshness_days=90,
        )
        # Exactly at boundary — not stale (> not >=)
        assert is_source_stale(a, now=now) is False

    def test_freshness_days_minimum(self) -> None:
        with pytest.raises(ValueError):
            _source(freshness_days=0)


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _source()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalSource(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_active(self) -> None:
        a = _source()
        assert a.status == SourceStatus.ACTIVE

    def test_default_freshness_and_retention(self) -> None:
        a = _source()
        assert a.freshness_days == 90
        assert a.retention_days == 365

    def test_default_allowed_use(self) -> None:
        a = _source()
        assert a.allowed_use == "research_only"

    def test_builder_with_full_context(self) -> None:
        now = datetime.now(UTC)
        a = build_source(
            tenant_id="tenant-a",
            deduplication_key="dedup-full",
            name="Saudi Company Registry",
            source_type=SourceType.PUBLIC_REGISTRY,
            source_url="https://registry.sa",
            description="Official Saudi company registry",
            policy_status=SourcePolicyStatus.APPROVED,
            allowed_use="research_and_qualification",
            authority_score=90,
            verifiability_score=85,
            freshness_days=30,
            retention_days=730,
            confidence=0.9,
            terms_reviewed_at=now,
            retrieved_at=now,
        )
        assert a.name == "Saudi Company Registry"
        assert a.source_type == SourceType.PUBLIC_REGISTRY
        assert a.policy_status == SourcePolicyStatus.APPROVED
        assert a.authority_score == 90
        assert a.confidence == 0.9


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_source_is_frozen(self) -> None:
        a = _source()
        with pytest.raises(Exception):
            a.status = SourceStatus.RETIRED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the Source entity."""

    def test_required_fields_present(self) -> None:
        a = _source()
        # Required: tenant_id, source_type, source_url, retrieved_at, confidence
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "source_type") and a.source_type
        assert hasattr(a, "source_url")  # may be empty but field must exist
        assert hasattr(a, "retrieved_at") and a.retrieved_at
        assert hasattr(a, "confidence") and isinstance(a.confidence, float)

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_source(
                tenant_id="",
                deduplication_key="dedup-1",
                name="Registry",
                source_type=SourceType.PUBLIC_REGISTRY,
            )

    def test_empty_name_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_source(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                name="",
                source_type=SourceType.PUBLIC_REGISTRY,
            )

    def test_empty_deduplication_key_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_source(
                tenant_id="tenant-a",
                deduplication_key="",
                name="Registry",
                source_type=SourceType.PUBLIC_REGISTRY,
            )
