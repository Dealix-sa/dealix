"""MCP security registry tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from dealix.hermes.core.schemas import utcnow
from dealix.trust.mcp_security import (
    AllowlistStatus,
    EnforcementDecision,
    MCPRiskHints,
    MCPSecurityRegistry,
    precheck,
)


def test_precheck_flags_http_transport() -> None:
    risks = precheck("http://example.com/mcp", vendor="dealix")
    assert any(r.risk == MCPRiskHints.EXFILTRATION for r in risks)


def test_precheck_flags_unknown_vendor() -> None:
    risks = precheck("https://example.com/mcp", vendor=None)
    assert any(r.risk == MCPRiskHints.RUG_PULL for r in risks)


def test_precheck_flags_wildcard_scope() -> None:
    risks = precheck("https://example.com/mcp/*", vendor="dealix")
    assert any(r.risk == MCPRiskHints.EXCESSIVE_SCOPE for r in risks)


def test_precheck_clean_url() -> None:
    risks = precheck("https://api.dealix.sa/mcp", vendor="dealix")
    # Known vendor + https + no wildcards → no high-severity risks expected
    assert all(r.risk != MCPRiskHints.EXCESSIVE_SCOPE for r in risks)


def test_register_and_get_server() -> None:
    reg = MCPSecurityRegistry()
    entry = reg.register_server(
        server_id="mcp_a",
        url="https://api.dealix.sa/mcp",
        vendor="dealix",
        capabilities=["proposal_render"],
    )
    assert reg.get("mcp_a") is entry
    assert entry.allowlist_status == AllowlistStatus.UNREVIEWED


def test_register_rejects_duplicate() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    with pytest.raises(ValueError):
        reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")


def test_vet_server_passes_with_complete_evidence() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    ok = reg.vet_server(
        "mcp_a",
        evidence={"reviewer": "sami", "checklist_passed": True, "evidence_ref": "ref"},
    )
    assert ok is True
    entry = reg.get("mcp_a")
    assert entry.allowlist_status == AllowlistStatus.APPROVED
    assert entry.semantic_vetting_passed is True


def test_vet_server_blocks_on_failed_checklist() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    ok = reg.vet_server(
        "mcp_a",
        evidence={"reviewer": "sami", "checklist_passed": False, "evidence_ref": "ref"},
    )
    assert ok is False
    assert reg.get("mcp_a").allowlist_status == AllowlistStatus.BLOCKED


def test_vet_server_requires_evidence_keys() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    with pytest.raises(ValueError):
        reg.vet_server("mcp_a", evidence={"reviewer": "x"})


def test_enforce_runtime_denies_unreviewed() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    assert reg.enforce_runtime("mcp_a", {"tool": "proposal_render"}) == EnforcementDecision.DENY


def test_enforce_runtime_allows_approved_within_capabilities() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server(
        "mcp_a",
        "https://api.dealix.sa/mcp",
        "dealix",
        capabilities=["proposal_render"],
    )
    reg.vet_server(
        "mcp_a",
        evidence={"reviewer": "sami", "checklist_passed": True, "evidence_ref": "ref"},
    )
    assert (
        reg.enforce_runtime("mcp_a", {"tool": "proposal_render"})
        == EnforcementDecision.ALLOW
    )


def test_enforce_runtime_escalates_on_capability_drift() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server(
        "mcp_a",
        "https://api.dealix.sa/mcp",
        "dealix",
        capabilities=["proposal_render"],
    )
    reg.vet_server(
        "mcp_a",
        evidence={"reviewer": "sami", "checklist_passed": True, "evidence_ref": "ref"},
    )
    assert (
        reg.enforce_runtime("mcp_a", {"tool": "payment_charge"})
        == EnforcementDecision.ESCALATE
    )


def test_enforce_runtime_escalates_on_stale_review() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    reg.vet_server(
        "mcp_a",
        evidence={"reviewer": "sami", "checklist_passed": True, "evidence_ref": "ref"},
    )
    entry = reg.get("mcp_a")
    entry.last_review_at = utcnow() - timedelta(days=365)
    assert (
        reg.enforce_runtime("mcp_a", {"tool": "proposal_render"})
        == EnforcementDecision.ESCALATE
    )


def test_block_server_denies_subsequently() -> None:
    reg = MCPSecurityRegistry()
    reg.register_server("mcp_a", "https://api.dealix.sa/mcp", "dealix")
    reg.vet_server(
        "mcp_a",
        evidence={"reviewer": "sami", "checklist_passed": True, "evidence_ref": "ref"},
    )
    reg.block("mcp_a", "found vulnerability")
    assert reg.enforce_runtime("mcp_a", {"tool": "x"}) == EnforcementDecision.DENY
