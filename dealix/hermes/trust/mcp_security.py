"""MCP-specific defences.

Research on Model Context Protocol risks identifies *tool poisoning* — a
malicious MCP server embedding instructions in a tool's metadata or
description — as a primary client-side threat. The defences here are not
a model call: they are static metadata checks plus a stable hash that the
tool registry pins so a silent metadata swap is detected.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any


_SUSPICIOUS_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\bignore\s+(?:previous|prior|earlier|above)\s+instructions?\b",
        r"\bdisregard\s+(?:previous|prior|earlier)\b",
        r"\b(?:as|act)\s+(?:an|the)\s+(?:admin|system|root)\b",
        r"\b(?:execute|run)\s+(?:rm|sudo|del|format)\b",
        r"\bexfiltrat\w+\b",
        r"\bsend\s+(?:secrets|tokens|keys)\b",
    )
)


@dataclass(slots=True)
class MCPFinding:
    severity: str  # info | warn | block
    rule_id: str
    summary: str


def score_metadata(metadata: dict[str, Any]) -> list[MCPFinding]:
    """Run static checks over an MCP tool's metadata.

    The checks are deliberately conservative: they catch the obvious
    injection patterns and exfiltration verbs that have shown up in
    public MCP advisories. A clean pass does *not* certify a tool — it
    only means the obvious gotchas aren't present.
    """
    findings: list[MCPFinding] = []
    flat = json.dumps(metadata, ensure_ascii=False, default=str).lower()

    for pat in _SUSPICIOUS_PATTERNS:
        if pat.search(flat):
            findings.append(
                MCPFinding(
                    severity="block",
                    rule_id="prompt_injection_in_metadata",
                    summary=f"suspicious phrase matched: {pat.pattern}",
                )
            )

    if not metadata.get("name"):
        findings.append(
            MCPFinding(severity="block", rule_id="missing_name", summary="metadata.name is required")
        )
    if not metadata.get("description"):
        findings.append(
            MCPFinding(
                severity="warn",
                rule_id="missing_description",
                summary="metadata.description is missing — cannot evaluate intent",
            )
        )
    return findings


def metadata_hash(metadata: dict[str, Any]) -> str:
    canonical = json.dumps(metadata, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def metadata_changed(prev_hash: str, metadata: dict[str, Any]) -> bool:
    return metadata_hash(metadata) != prev_hash


__all__ = ["MCPFinding", "score_metadata", "metadata_hash", "metadata_changed"]
