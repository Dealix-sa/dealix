"""
MCP gateway.

MCP is powerful but ships its own threat model: tool poisoning, descriptor
shadowing, rug pulls, and unsigned manifests. The Hermes MCP gateway
enforces:

    Agent
    → Tool Gateway
    → MCP Gateway
    → Server Allowlist
    → Manifest Review
    → Tool Descriptor Scan
    → Semantic Vetting
    → Data Scope Enforcement
    → Approval (if sensitive)
    → Tool Call
    → Audit
    → Outcome

Rule: no MCP server can be enabled without S4 Sovereign Approval.
"""

from __future__ import annotations

from dealix.hermes.mcp.anomaly_detection import (
    AnomalyReport,
    detect_anomalies,
)
from dealix.hermes.mcp.capability_attestation import (
    CapabilityAttestation,
    attest_capability,
)
from dealix.hermes.mcp.descriptor_scan import DescriptorScan, scan_descriptor
from dealix.hermes.mcp.gateway import MCPGateway, MCPRequest, MCPVerdict
from dealix.hermes.mcp.kill_switch import KillSwitch
from dealix.hermes.mcp.manifest_review import ManifestReview, review_manifest
from dealix.hermes.mcp.runtime_guardrails import (
    RuntimeGuardResult,
    runtime_guard,
)
from dealix.hermes.mcp.semantic_vetting import (
    SemanticVerdict,
    vet_semantics,
)
from dealix.hermes.mcp.server_allowlist import ServerAllowlist

__all__ = [
    "MCPGateway",
    "MCPRequest",
    "MCPVerdict",
    "ServerAllowlist",
    "ManifestReview",
    "review_manifest",
    "DescriptorScan",
    "scan_descriptor",
    "SemanticVerdict",
    "vet_semantics",
    "CapabilityAttestation",
    "attest_capability",
    "RuntimeGuardResult",
    "runtime_guard",
    "AnomalyReport",
    "detect_anomalies",
    "KillSwitch",
]
