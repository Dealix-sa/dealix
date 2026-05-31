"""MCP Gateway — no agent talks to MCP directly. Ever."""

from dealix.hermes.mcp.anomaly_detection import AnomalyDetector, AnomalyReport
from dealix.hermes.mcp.descriptor_scan import scan_tool_descriptor, DescriptorScanResult
from dealix.hermes.mcp.gateway import MCPGateway, MCPCall, MCPCallResult
from dealix.hermes.mcp.manifest_review import ManifestReview, review_manifest
from dealix.hermes.mcp.runtime_guardrails import RuntimeGuardrails
from dealix.hermes.mcp.semantic_vetting import SemanticVetting, vet_tool_semantics
from dealix.hermes.mcp.server_registry import MCPServerCard, MCPServerRegistry, ServerState

__all__ = [
    "AnomalyDetector",
    "AnomalyReport",
    "DescriptorScanResult",
    "MCPCall",
    "MCPCallResult",
    "MCPGateway",
    "MCPServerCard",
    "MCPServerRegistry",
    "ManifestReview",
    "RuntimeGuardrails",
    "SemanticVetting",
    "ServerState",
    "review_manifest",
    "scan_tool_descriptor",
    "vet_tool_semantics",
]
