"""
hermes — Dealix's Production + Growth + Governance Max layer.

Hermes is the Policy-Bounded Agentic Platform: every action proposed by an
agent flows through a control plane that enforces sovereignty, trust,
approvals, data boundaries, and outcome measurement before it touches
the world.

Layers
------
control_plane   — runtime gates: sovereignty / trust / approval / tool / data / audit / outcome / kill switch
identity        — agent / actor / workspace identities, capability scopes, revocation
data            — classification, tenant isolation, context packets, redaction, retention
growth          — verified revenue loop, channels, attribution, GEO/AI search visibility
money           — revenue quality, cost / margin intelligence, pricing engine
products        — productized packages (Revenue Hunter, AI Trust Kit, White-label, ...)
delivery        — delivery playbooks per product
customer        — customer value report generator
partners        — partner program (tiers, claims, revenue share, performance)
assets          — asset store, quality, reuse, commercialization
graphs          — intelligence graphs (opportunity, outcome, revenue, partner, asset, risk, sector)
workflows       — declarative workflow configs (YAML)
api_platform    — public API readiness gate
marketplace     — marketplace readiness gate

Rule of the platform
--------------------
Any request that does not pass through ``hermes.control_plane.runtime`` is
considered illegitimate and MUST be rejected upstream.
"""

__all__ = ["__version__"]
__version__ = "0.1.0"
