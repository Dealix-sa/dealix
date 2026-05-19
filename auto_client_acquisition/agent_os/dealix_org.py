"""In-product seed for the Dealix agent organization.

Registers the 10 agents of the Dealix organization as :class:`AgentCard`
entities in the agent registry so the org is a tracked, in-product set of
identities (not just a doc and gitignored Claude Code config).

The canonical org description is ``docs/AGENT_ORGANIZATION.md``: a pyramid
with ``dealix-pm`` orchestrating an executive layer and an execution layer.

Autonomy ladder (see ``autonomy_levels.py``):
  - executive layer: L1 (analyze) .. L3 (recommend) — advise and brief,
    never auto-execute a strategic decision or write product code.
  - execution layer: L2 (draft) .. L3 (recommend) — produce drafts and
    recommendations; external-facing output is handed back as drafts.
  - no agent is granted L4+ (auto-execute) — every external action stays
    behind the founder's approval tap.

``seed_dealix_org()`` is idempotent: an already-registered agent_id is
left untouched, so the function is safe to call repeatedly (on worker
startup, in tests, or from an admin endpoint).
"""

from __future__ import annotations

from auto_client_acquisition.agent_os.agent_card import AgentCard, new_card
from auto_client_acquisition.agent_os.agent_registry import (
    get_agent,
    register_agent,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel

# The founder owns and operates every kill switch in the MVP.
_FOUNDER = "founder"

# Stable specs for the 10 agents. agent_id values are stable identifiers;
# autonomy_level stays within L1..L3 for every agent (no L4+).
_ORG_SPECS: tuple[dict[str, object], ...] = (
    # ── Executive / strategic layer ──────────────────────────────
    {
        "agent_id": "dealix-pm",
        "name": "Dealix PM",
        "layer": "executive",
        "purpose": (
            "Project management and orchestration: plan execution, "
            "milestones, weekly cadence, delegation, and decision gates."
        ),
        "autonomy_level": AutonomyLevel.L3_RECOMMEND,
    },
    {
        "agent_id": "dealix-strategy",
        "name": "Dealix Strategy",
        "layer": "executive",
        "purpose": (
            "Market and competitive analysis, positioning, offer and "
            "pricing strategy, roadmap sequencing, freeze/build calls."
        ),
        "autonomy_level": AutonomyLevel.L3_RECOMMEND,
    },
    {
        "agent_id": "dealix-finance",
        "name": "Dealix Finance",
        "layer": "executive",
        "purpose": (
            "Unit economics, pricing models, revenue forecasting, cash "
            "runway, and the capital/value ledgers."
        ),
        "autonomy_level": AutonomyLevel.L2_DRAFT,
    },
    {
        "agent_id": "dealix-marketing",
        "name": "Dealix Marketing",
        "layer": "executive",
        "purpose": (
            "Demand-generation strategy, campaign and content-calendar "
            "planning, and lead-magnet strategy."
        ),
        "autonomy_level": AutonomyLevel.L2_DRAFT,
    },
    {
        "agent_id": "dealix-success",
        "name": "Dealix Success",
        "layer": "executive",
        "purpose": (
            "Onboarding, account health scoring, retention, and retainer "
            "expansion."
        ),
        "autonomy_level": AutonomyLevel.L2_DRAFT,
    },
    {
        "agent_id": "dealix-ops",
        "name": "Dealix Ops",
        "layer": "executive",
        "purpose": (
            "System health, verifier scripts, the 8 doctrine gates, "
            "friction-log review, and launch readiness."
        ),
        "autonomy_level": AutonomyLevel.L1_ANALYZE,
    },
    # ── Execution layer ──────────────────────────────────────────
    {
        "agent_id": "dealix-sales",
        "name": "Dealix Sales",
        "layer": "execution",
        "purpose": (
            "Lead qualification, outreach drafts, proposals, and offer "
            "recommendation. External-facing output is handed back as "
            "drafts only."
        ),
        "autonomy_level": AutonomyLevel.L3_RECOMMEND,
    },
    {
        "agent_id": "dealix-content",
        "name": "Dealix Content",
        "layer": "execution",
        "purpose": (
            "Bilingual docs, SOPs, case studies, proposal templates, "
            "posts, and sector reports."
        ),
        "autonomy_level": AutonomyLevel.L2_DRAFT,
    },
    {
        "agent_id": "dealix-delivery",
        "name": "Dealix Delivery",
        "layer": "execution",
        "purpose": (
            "The 7-day Revenue Intelligence Sprint pipeline and Proof "
            "Pack assembly."
        ),
        "autonomy_level": AutonomyLevel.L2_DRAFT,
    },
    {
        "agent_id": "dealix-engineer",
        "name": "Dealix Engineer",
        "layer": "execution",
        "purpose": (
            "Python/FastAPI code, tests, database migrations, and cron "
            "scripts."
        ),
        "autonomy_level": AutonomyLevel.L3_RECOMMEND,
    },
)

# agent_ids of the executive layer, exposed for callers and tests.
EXECUTIVE_LAYER: tuple[str, ...] = tuple(
    str(s["agent_id"]) for s in _ORG_SPECS if s["layer"] == "executive"
)
EXECUTION_LAYER: tuple[str, ...] = tuple(
    str(s["agent_id"]) for s in _ORG_SPECS if s["layer"] == "execution"
)
DEALIX_ORG_AGENT_IDS: tuple[str, ...] = tuple(
    str(s["agent_id"]) for s in _ORG_SPECS
)


def build_org_cards() -> list[AgentCard]:
    """Build (but do not register) the 10 validated org :class:`AgentCard`s.

    Pure function — no registry side effects. ``new_card`` enforces the
    agent-identity non-negotiables (owner, purpose, autonomy bounds).
    """
    cards: list[AgentCard] = []
    for spec in _ORG_SPECS:
        card = new_card(
            agent_id=str(spec["agent_id"]),
            name=str(spec["name"]),
            owner=_FOUNDER,
            purpose=str(spec["purpose"]),
            autonomy_level=int(spec["autonomy_level"]),  # type: ignore[arg-type]
            kill_switch_owner=_FOUNDER,
            notes=f"dealix-org:{spec['layer']}",
        )
        cards.append(card)
    return cards


def seed_dealix_org() -> dict[str, object]:
    """Register the 10 Dealix org agents in the registry. Idempotent.

    Already-registered agent_ids are skipped, so calling this repeatedly
    (worker startup, tests, admin endpoint) is safe and never raises a
    "already registered" error.

    Returns a summary dict: registered ids, skipped ids, and total.
    """
    registered: list[str] = []
    skipped: list[str] = []
    for card in build_org_cards():
        if get_agent(card.agent_id) is not None:
            skipped.append(card.agent_id)
            continue
        register_agent(card)
        registered.append(card.agent_id)
    return {
        "status": "ok",
        "registered": registered,
        "skipped": skipped,
        "total": len(DEALIX_ORG_AGENT_IDS),
        "executive_layer": list(EXECUTIVE_LAYER),
        "execution_layer": list(EXECUTION_LAYER),
    }


__all__ = [
    "DEALIX_ORG_AGENT_IDS",
    "EXECUTION_LAYER",
    "EXECUTIVE_LAYER",
    "build_org_cards",
    "seed_dealix_org",
]
