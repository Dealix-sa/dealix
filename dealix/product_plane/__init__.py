"""
Dealix Product Plane — Section 46.

This package is the structural surface the front-end consumes. It does NOT
implement business logic — it composes Hermes services into workspace-shaped
views:

    sovereign_console/   ─ founder command + approvals + money + risk + decisions
    internal_workspace/  ─ signals, opportunities, offers, proposals, outcomes
    growth_workspace/    ─ campaigns, leads, experiments, attribution, funnel
    trust_workspace/     ─ agents, tools, permissions, evidence, audit, incidents
    customer_workspace/  ─ per-customer actions, leads, proposals, outcomes
    partner_workspace/   ─ per-partner clients, lead packs, revenue share, perf

The modules here expose `summarize(...)` functions that return JSON-shaped
dicts ready for the front-end. Keeping them thin avoids the front-end coupling
itself to dataclasses.
"""

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "sovereign_console",
    "internal_workspace",
    "growth_workspace",
    "trust_workspace",
    "customer_workspace",
    "partner_workspace",
]
