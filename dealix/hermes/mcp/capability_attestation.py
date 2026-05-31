"""
Capability attestation — records that a specific (server, tool, version)
triple was attested for a given capability by a specific reviewer.
"""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class CapabilityAttestation:
    server_id: str
    tool_name: str
    tool_version: str
    capability: str
    attested_by: str
    attested_at: float
    notes: str = ""


def attest_capability(
    server_id: str,
    tool_name: str,
    tool_version: str,
    capability: str,
    *,
    attested_by: str,
    notes: str = "",
) -> CapabilityAttestation:
    if not all([server_id, tool_name, tool_version, capability, attested_by]):
        raise ValueError(
            "attest_capability requires server_id, tool_name, tool_version, "
            "capability, attested_by"
        )
    return CapabilityAttestation(
        server_id=server_id,
        tool_name=tool_name,
        tool_version=tool_version,
        capability=capability,
        attested_by=attested_by,
        attested_at=time.time(),
        notes=notes,
    )
