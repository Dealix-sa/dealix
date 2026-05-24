"""MCP security — defend against tool poisoning, shadowing, rug-pulls.

Recent research on Model Context Protocol attacks (tool poisoning,
metadata shadowing, manifest rug-pulls) consistently recommends:
    1. Static metadata analysis of every tool descriptor before it is
       made available to agents.
    2. A signed/hashed manifest so a tool cannot mutate behaviour after
       registration.
    3. Behavioural anomaly detection on calls.
    4. Transparency: surface to the operator every sensitive call.
    5. Runtime guardrails that scope arguments, redact secrets, and
       block unknown tools.

This module implements the static + manifest layers; runtime calls go
through `Orchestrator.execute()` which logs to the audit ledger.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MCPRiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


# Patterns inside tool descriptors that strongly suggest poisoning.
POISON_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"<!--\s*ignore\s+previous", re.IGNORECASE),
    re.compile(r"system\s*:\s*you\s+must", re.IGNORECASE),
    re.compile(r"exfiltrate", re.IGNORECASE),
    re.compile(r"ssh\s+private\s+key", re.IGNORECASE),
    re.compile(r"\.aws/credentials", re.IGNORECASE),
    re.compile(r"export\s+all\s+data", re.IGNORECASE),
    re.compile(r"override\s+user\s+intent", re.IGNORECASE),
)

# Tool name / behaviour patterns that imply high-risk side effects.
HIGH_RISK_NAMES: tuple[re.Pattern[str], ...] = (
    re.compile(r"send_email", re.IGNORECASE),
    re.compile(r"transfer", re.IGNORECASE),
    re.compile(r"delete", re.IGNORECASE),
    re.compile(r"deploy", re.IGNORECASE),
    re.compile(r"publish", re.IGNORECASE),
    re.compile(r"sign", re.IGNORECASE),
)


@dataclass
class MCPToolDescriptor:
    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    server: str = "unknown"
    version: str = "0.0.0"


@dataclass
class MCPVettingResult:
    name: str
    risk: MCPRiskLevel
    findings: list[str]
    manifest_hash: str
    approved: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "risk": self.risk.value,
            "findings": self.findings,
            "manifest_hash": self.manifest_hash,
            "approved": self.approved,
        }


def _scan_descriptor(desc: MCPToolDescriptor) -> tuple[list[str], MCPRiskLevel]:
    text = json.dumps(
        {
            "name": desc.name,
            "description": desc.description,
            "input_schema": desc.input_schema,
        },
        sort_keys=True,
    )
    findings: list[str] = []

    for pat in POISON_PATTERNS:
        if pat.search(text):
            findings.append(f"poison_pattern:{pat.pattern}")

    high_risk = any(pat.search(desc.name) for pat in HIGH_RISK_NAMES)
    if high_risk:
        findings.append(f"high_risk_name:{desc.name}")

    if not desc.description or len(desc.description) < 12:
        findings.append("description_missing_or_too_short")

    if findings and any(f.startswith("poison_pattern") for f in findings):
        return findings, MCPRiskLevel.BLOCKED
    if high_risk:
        return findings, MCPRiskLevel.HIGH
    if findings:
        return findings, MCPRiskLevel.MEDIUM
    return findings, MCPRiskLevel.LOW


def manifest_hash(desc: MCPToolDescriptor) -> str:
    """Stable hash of the descriptor — change of hash = re-vet required."""
    blob = json.dumps(
        {
            "name": desc.name,
            "description": desc.description,
            "input_schema": desc.input_schema,
            "server": desc.server,
            "version": desc.version,
        },
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def vet_tool(desc: MCPToolDescriptor) -> MCPVettingResult:
    """Static analysis of a tool descriptor before registration."""
    findings, risk = _scan_descriptor(desc)
    approved = risk in {MCPRiskLevel.LOW, MCPRiskLevel.MEDIUM}
    return MCPVettingResult(
        name=desc.name,
        risk=risk,
        findings=findings,
        manifest_hash=manifest_hash(desc),
        approved=approved,
    )


class MCPRegistry:
    """In-process MCP allowlist with hash pinning.

    A tool is callable only if its current descriptor hash matches the
    hash recorded at allow time. Any drift = quarantined until re-vetted.
    """

    def __init__(self) -> None:
        self._allowed: dict[str, str] = {}
        self._risk: dict[str, MCPRiskLevel] = {}

    def allow(self, desc: MCPToolDescriptor) -> MCPVettingResult:
        vetted = vet_tool(desc)
        if vetted.approved:
            self._allowed[desc.name] = vetted.manifest_hash
            self._risk[desc.name] = vetted.risk
        return vetted

    def is_allowed(self, desc: MCPToolDescriptor) -> bool:
        expected = self._allowed.get(desc.name)
        if expected is None:
            return False
        return manifest_hash(desc) == expected

    def risk_of(self, name: str) -> MCPRiskLevel | None:
        return self._risk.get(name)

    def snapshot(self) -> dict[str, dict[str, str]]:
        return {
            name: {"hash": h, "risk": self._risk.get(name, MCPRiskLevel.LOW).value}
            for name, h in self._allowed.items()
        }


_default_registry = MCPRegistry()


def default_registry() -> MCPRegistry:
    return _default_registry
