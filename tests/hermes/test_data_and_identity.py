"""Tests for the data + identity layers."""

from __future__ import annotations

import pytest

from dealix.hermes.data import (
    ContextPacketBuilder,
    DataBoundary,
    classify_field,
    enforce_isolation,
    get_boundary,
    redact,
    register_boundary,
)
from dealix.hermes.data.classification import DataClassification
from dealix.hermes.data.retention import apply_retention
from dealix.hermes.data.tenant_isolation import TenantIsolationError
from dealix.hermes.identity import (
    AGENT_REGISTRY,
    AgentIdentity,
    CAPABILITY_REGISTRY,
    register_agent,
)
from dealix.hermes.identity.revocation import (
    REVOCATION_LIST,
    RevocationTarget,
    is_revoked,
    revoke,
)


def test_classify_field_sovereign():
    assert classify_field("sovereign_memory") == DataClassification.SOVEREIGN
    assert classify_field("customer_data") == DataClassification.CONFIDENTIAL
    assert classify_field("phone") == DataClassification.REGULATED


def test_redaction_drops_above_regulated_and_masks():
    record = {
        "email": "Alice <alice@example.com>",
        "phone": "+966500000000",
        "sovereign_memory": "should be dropped",
        "workflow": "ok",
    }
    out = redact(record, drop_above=DataClassification.REGULATED)
    assert "sovereign_memory" not in out  # SOVEREIGN > REGULATED
    assert "email" in out and "phone" in out
    assert "***" in out["email"]
    assert "***" in out["phone"]


def test_redaction_strict_drops_regulated_fields():
    record = {"email": "x@y.com", "phone": "+966500000000", "workflow": "ok"}
    out = redact(record, drop_above=DataClassification.CONFIDENTIAL)
    assert "email" not in out and "phone" not in out
    assert "workflow" in out


def test_tenant_isolation_raises_on_cross_tenant():
    records = [{"workspace_id": "customer_a"}, {"workspace_id": "customer_b"}]
    with pytest.raises(TenantIsolationError):
        enforce_isolation(records, "customer_a")


def test_context_packet_excludes_sovereign_by_default():
    builder = ContextPacketBuilder(
        agent_id="revenue_hunter",
        workspace_id="dealix_internal",
        purpose="draft_proposal",
    )
    packet = builder.build(include=("opportunity", "sovereign_memory", "offer"))
    assert "sovereign_memory" not in packet.included_objects
    assert "sovereign_memory" in packet.excluded_objects


def test_data_boundary_registry():
    register_boundary(DataBoundary(
        workspace_id="customer_acme",
        data_boundary="customer_workspace_only",
        allowed_agents=("revenue_hunter",),
    ))
    assert get_boundary("customer_acme") is not None


def test_agent_registry_defaults_loaded():
    for agent_id in ("revenue_hunter", "proposal_factory", "trust_checker", "value_reporter", "growth_engine"):
        assert agent_id in AGENT_REGISTRY


def test_register_agent_rejects_unknown_capability():
    with pytest.raises(ValueError):
        register_agent(AgentIdentity(
            agent_id="bad_agent",
            agent_type="test",
            owner="Sami",
            workspace_scope=("dealix_internal",),
            capabilities=("ghost_capability_does_not_exist",),
            forbidden_capabilities=(),
            max_sovereignty_level=__import__(
                "dealix.hermes.control_plane.sovereignty_gate",
                fromlist=["SovereigntyLevel"],
            ).SovereigntyLevel.S1_INTERNAL,
            max_data_sensitivity=__import__(
                "dealix.classifications", fromlist=["SensitivityClass"],
            ).SensitivityClass.S1,
        ))


def test_revocation_records_and_queries():
    revoke(RevocationTarget.AGENT, "test_agent", reason="test", by="sami")
    assert is_revoked(RevocationTarget.AGENT, "test_agent")
    REVOCATION_LIST.pop((RevocationTarget.AGENT, "test_agent"), None)


def test_retention_buckets():
    from datetime import UTC, datetime, timedelta
    now = datetime.now(UTC)
    records = [
        {"id": 1, "created_at": now - timedelta(days=10)},
        {"id": 2, "created_at": now - timedelta(days=400)},
        {"id": 3, "created_at": now - timedelta(days=2000)},
    ]
    result = apply_retention(records, dataset="audit_log", now=now)
    assert len(result.kept) == 1
    assert len(result.expired) == 1
    assert len(result.purged) == 1
