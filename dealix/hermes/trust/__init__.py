"""Trust & Governance — the layer that makes Hermes safe to plug into the
outside world.

The trust layer is two things at once:
    1. an *internal guard* that prevents agents from executing dangerous
       actions, and
    2. an *external product* (Dealix AI Trust Kit / Governance OS) that we
       sell to customers who need to govern their own AI usage.

Components:
    * agent_registry   — every agent has an Agent Card (mission, tools, KPIs)
    * tool_registry    — every tool is declared with permissions + risk
    * permissions      — matrix tying agents → allowed tools / actions
    * approvals        — adapter to the existing approval centre + memos
    * guardrails       — no-overclaim, no-cold-channel, PII checks
    * evidence         — evidence pack builder for outcomes + audits
    * audit            — append-only audit log
    * mcp_security     — MCP-specific defences (tool-poisoning, metadata)
"""

from __future__ import annotations
