"""
Runtime guardrails — per-call enforcement at MCP tool invocation time.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuntimeGuardResult:
    allowed: bool
    must_request_approval: bool
    findings: list[str]


_SENSITIVE_TOOLS = frozenset(
    {
        "send_external",
        "issue_refund",
        "approve_price",
        "sign_contract",
        "export_data",
        "modify_production_config",
    }
)


def runtime_guard(
    *,
    tool_name: str,
    payload_size_bytes: int,
    max_payload_bytes: int = 64 * 1024,
    call_rate_per_minute: int,
    max_call_rate_per_minute: int = 30,
    target_record_count: int = 1,
    max_records_per_call: int = 200,
) -> RuntimeGuardResult:
    findings: list[str] = []
    if payload_size_bytes > max_payload_bytes:
        findings.append(
            f"payload_size_exceeds:{payload_size_bytes}>{max_payload_bytes}"
        )
    if call_rate_per_minute > max_call_rate_per_minute:
        findings.append(
            f"call_rate_exceeds:{call_rate_per_minute}>{max_call_rate_per_minute}"
        )
    if target_record_count > max_records_per_call:
        findings.append(
            f"record_count_exceeds:{target_record_count}>{max_records_per_call}"
        )
    must_approve = tool_name in _SENSITIVE_TOOLS or bool(findings)
    return RuntimeGuardResult(
        allowed=not findings,
        must_request_approval=must_approve,
        findings=findings,
    )
