"""
Hermes — Dealix Production Empire Layer.

The Hermes layer turns Dealix from "another agentic AI tool" into a
sovereign control plane for governed AI execution and verified revenue.

Sub-packages:
- control_plane:    central orchestration entrypoint
- agent_lifecycle:  registry → risk → scope → eval → promote → retire
- identity:         scoped, revocable, capability-bound agent identities
- agent_comms:      sanitization + delegation + cross-agent validation
- provenance:       source/lineage ledger for prompts and outputs
- mcp:              MCP gateway (allowlist + manifest review + guardrails)
- security:         injection defense, output sanitization, claim verification
- growth:           GEO, attribution, entity-data, trust-signal engines
- money:            verified revenue, revenue quality, delivery margin
- sovereignty:      founder-time cost accounting
- products:         offer-market fit + experiment metrics + readiness gates
- assets:           asset → product commercialization
- partners:         tiered partner program with approved-claims policy
- delivery:         per-offer delivery playbooks + quality checklists
- board:            executive metrics + investor / board memos

All sub-packages are pure-Python and side-effect-free at import time so
they can be composed into the existing FastAPI surface without forcing
DB or Redis dependencies on consumers that only need the data shapes.
"""

from __future__ import annotations

__all__ = [
    "control_plane",
    "agent_lifecycle",
    "identity",
    "agent_comms",
    "provenance",
    "mcp",
    "security",
    "growth",
    "money",
    "sovereignty",
    "products",
    "assets",
    "partners",
    "delivery",
    "board",
]

HERMES_VERSION = "0.1.0"
HERMES_TAGLINE = (
    "A sovereign, policy-bounded, revenue-verified agentic platform."
)
