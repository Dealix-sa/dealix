"""Tests for the Hermes trust guardrails + MCP review."""

from __future__ import annotations

from dealix.hermes.trust.guardrails import TrustCheckRequest, trust_check
from dealix.hermes.trust.mcp_security import MCPServerReview, review_mcp_server


def test_overclaim_blocked() -> None:
    result = trust_check(
        TrustCheckRequest(
            content="نضمن لك نتائج مضمونة",
            action_type="external_message",
            target_audience="customer",
        )
    )
    assert result.allowed is False
    assert result.approval_required is True
    assert result.risk_level in {"high", "critical"}


def test_sensitive_data_is_critical() -> None:
    result = trust_check(
        TrustCheckRequest(
            content="Customer NIN: 1234567890",
            action_type="internal_log",
            target_audience="internal",
            contains_sensitive_data=True,
        )
    )
    assert result.risk_level == "critical"
    assert result.approval_required is True


def test_enterprise_pricing_requires_approval() -> None:
    result = trust_check(
        TrustCheckRequest(
            content="Enterprise quote: 50,000 SAR/mo",
            action_type="external_enterprise_quote",
            target_audience="customer",
            contains_pricing=True,
            contains_external_commitment=True,
        )
    )
    assert result.approval_required is True


def test_safe_internal_content_passes() -> None:
    result = trust_check(
        TrustCheckRequest(
            content="Internal note: review pipeline.",
            action_type="internal_note",
            target_audience="internal",
        )
    )
    assert result.allowed is True
    assert result.risk_level == "low"


def test_mcp_broad_scope_is_critical() -> None:
    result = review_mcp_server(
        MCPServerReview(
            server_name="acme-mcp",
            owner="sami",
            requested_tools=["read_all", "write_all"],
            data_access_scope="all",
            external_execution=True,
        )
    )
    assert result.approved is False
    assert result.risk_level == "critical"
    assert any("scope" in c for c in result.required_controls)


def test_mcp_narrow_scope_can_be_approved() -> None:
    result = review_mcp_server(
        MCPServerReview(
            server_name="docs-mcp",
            owner="sami",
            requested_tools=["read_doc"],
            data_access_scope="narrow",
            external_execution=False,
        )
    )
    assert result.risk_level == "medium"
    assert result.approved is True
