"""Persuasion playbooks — honest, guardrailed influence.

Persuasion here means *clear value framing and a relevant call to action* — it
is never manipulation, false scarcity, fabricated proof, or guaranteed
outcomes. Every proof point must be truthful and sourced; the claim guard in
:mod:`app.commercial.safety` is the backstop.
"""

from __future__ import annotations

from app.commercial.engagement_schemas import PersuasionStrategy

# Things we will never say, regardless of motion.
ALWAYS_AVOID = (
    "guaranteed results / ROI",
    "false urgency or fake scarcity",
    "invented clients, testimonials or case studies",
    "final price, discount or contract commitment",
    "disparaging competitors with unverified claims",
)

# Motion → persuasion angle and honest message points.
_PLAYBOOK: dict[str, PersuasionStrategy] = {
    "sales_prospecting": PersuasionStrategy(
        angle="cost_of_inaction_vs_organised_followup",
        message_points=[
            "Leads you already pay to generate go cold without a follow-up system.",
            "We organise qualification, drafts and follow-up so fewer opportunities slip.",
            "You stay in control — every message is a draft until you approve it.",
        ],
        proof_points=[
            "We show you the exact drafts and a command room before anything is sent.",
        ],
        avoid=list(ALWAYS_AVOID),
        cta="A 20-minute call to map your current lead flow — no obligation.",
    ),
    "partnership_outreach": PersuasionStrategy(
        angle="shared_clients_mutual_value",
        message_points=[
            "Your clients get added value; you don't build the system yourselves.",
            "We start with a small, defined pilot before any wider commitment.",
        ],
        proof_points=["Pilot scope and success metrics are agreed in writing first."],
        avoid=list(ALWAYS_AVOID),
        cta="A short call to pick one pilot account together.",
    ),
    "proposal_push": PersuasionStrategy(
        angle="clarity_reduces_decision_risk",
        message_points=[
            "A clear brief: scope, deliverables, a pricing range and out-of-scope.",
            "You decide the final price — the brief is a starting point, not a bill.",
        ],
        proof_points=["Acceptance criteria are defined before any work begins."],
        avoid=list(ALWAYS_AVOID),
        cta="Walk through the brief together and adjust scope to your budget.",
    ),
    "revival": PersuasionStrategy(
        angle="timing_changed_low_pressure",
        message_points=[
            "Circumstances change; we're checking if the timing is better now.",
            "If not, we'll close the loop respectfully — no pressure.",
        ],
        proof_points=[],
        avoid=list(ALWAYS_AVOID),
        cta="Worth a quick check-in, or should we revisit next quarter?",
    ),
    "upsell": PersuasionStrategy(
        angle="expand_on_proven_value",
        message_points=[
            "Based on what we've actually delivered, here's a logical next step.",
            "We expand only where the data shows it's worth it.",
        ],
        proof_points=["We reference your real results to date — nothing invented."],
        avoid=list(ALWAYS_AVOID),
        cta="A short review of results, then decide on expansion together.",
    ),
    "retention": PersuasionStrategy(
        angle="ensure_value_realisation",
        message_points=[
            "We want to make sure you're getting full value from what you have.",
        ],
        proof_points=["We review your actual usage and outcomes openly."],
        avoid=list(ALWAYS_AVOID),
        cta="A 15-minute value review.",
    ),
    "renewal": PersuasionStrategy(
        angle="scope_and_results_review",
        message_points=[
            "Renewal is a good moment to re-confirm scope and what mattered most.",
        ],
        proof_points=["We bring the real numbers from the engagement."],
        avoid=list(ALWAYS_AVOID),
        cta="A scope-and-results review before renewal.",
    ),
}

_DEFAULT = PersuasionStrategy(
    angle="honest_value_fit",
    message_points=[
        "We help commercial teams organise opportunities and follow up reliably.",
        "Everything is a draft for your review — nothing is sent without approval.",
    ],
    proof_points=[],
    avoid=list(ALWAYS_AVOID),
    cta="A short call to see if there's a fit.",
)

# Objection → honest reframe (no discounts, no guarantees, no final price).
_OBJECTION_REFRAME: dict[str, str] = {
    "price_objection": (
        "Acknowledge the budget honestly, then offer a smaller scope (pilot / "
        "diagnostic-first) that fits it. Never offer a discount or a final price."
    ),
    "not_now": (
        "Respect the timing. Offer a low-effort proof-first step or a scheduled "
        "check-in. Keep the relationship warm without pressure."
    ),
    "no_interest": (
        "Thank them, ask (once) if a future check-in is welcome, and respect a no."
    ),
    "wrong_person": (
        "Apologise briefly and ask for the right contact — do not re-target "
        "anyone without a fresh, lawful source."
    ),
    "support_question": (
        "Answer factually. If the answer implies a delivery commitment, flag it "
        "for human approval before promising anything."
    ),
}


def strategy_for(motion: str) -> PersuasionStrategy:
    """Return the persuasion strategy for a motion (a fresh copy)."""
    base = _PLAYBOOK.get(motion, _DEFAULT)
    return PersuasionStrategy(
        angle=base.angle,
        message_points=list(base.message_points),
        proof_points=list(base.proof_points),
        avoid=list(base.avoid),
        cta=base.cta,
    )


def reframe_objection(objection_type: str) -> str:
    return _OBJECTION_REFRAME.get(
        objection_type,
        "Clarify the concern, restate value honestly, and propose a low-risk next step.",
    )
