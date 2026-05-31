"""
MCP gateway — composes allowlist + descriptor scan + semantic vetting +
runtime guardrails + kill switch into a single decision.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.mcp.descriptor_scan import DescriptorScan, scan_descriptor
from dealix.hermes.mcp.kill_switch import KillSwitch
from dealix.hermes.mcp.runtime_guardrails import RuntimeGuardResult, runtime_guard
from dealix.hermes.mcp.semantic_vetting import SemanticVerdict, vet_semantics
from dealix.hermes.mcp.server_allowlist import ServerAllowlist


@dataclass
class MCPRequest:
    server_id: str
    manifest_sha256: str
    tool_name: str
    tool_descriptor: str
    domain: str
    payload_size_bytes: int
    call_rate_per_minute: int
    target_record_count: int
    declared_data_scope: tuple[str, ...] = ()
    required_data_scope: tuple[str, ...] = ()


@dataclass
class MCPVerdict:
    allowed: bool
    must_request_approval: bool
    reasons: list[str]
    descriptor: DescriptorScan
    semantic: SemanticVerdict
    runtime: RuntimeGuardResult


class MCPGateway:
    def __init__(self, allowlist: ServerAllowlist, kill_switch: KillSwitch | None = None):
        self.allowlist = allowlist
        self.kill_switch = kill_switch or KillSwitch()

    def evaluate(self, request: MCPRequest) -> MCPVerdict:
        reasons: list[str] = []
        if self.kill_switch.tripped:
            reasons.append(f"kill_switch_tripped:{self.kill_switch.reason}")
        if not self.allowlist.is_allowed(request.server_id, request.manifest_sha256):
            reasons.append("server_not_allowlisted_or_manifest_mismatch")

        descriptor = scan_descriptor(request.tool_descriptor)
        if not descriptor.ok:
            reasons.append(f"descriptor_findings:{descriptor.findings}")

        semantic = vet_semantics(
            request.domain,
            request.tool_descriptor,
            required_data_scope=list(request.required_data_scope) or None,
            declared_data_scope=request.declared_data_scope,
        )
        if not semantic.ok:
            reasons.append(f"semantic_findings:{semantic.findings}")

        runtime = runtime_guard(
            tool_name=request.tool_name,
            payload_size_bytes=request.payload_size_bytes,
            call_rate_per_minute=request.call_rate_per_minute,
            target_record_count=request.target_record_count,
        )
        if runtime.findings:
            reasons.append(f"runtime_findings:{runtime.findings}")

        return MCPVerdict(
            allowed=not reasons,
            must_request_approval=runtime.must_request_approval and not reasons,
            reasons=reasons,
            descriptor=descriptor,
            semantic=semantic,
            runtime=runtime,
        )
