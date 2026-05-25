from __future__ import annotations

from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook

REVENUE_HUNTER_PLAYBOOK = DeliveryPlaybook(
    offer_id="revenue_hunter_pilot",
    name="Revenue Hunter Pilot",
    inputs_required=(
        "ideal customer profile",
        "current pipeline list",
        "founder calendar for review slots",
    ),
    steps=(
        "ICP refinement workshop",
        "qualified-pipeline list build",
        "message-bank drafting (3 angles)",
        "founder review + approval",
        "first outreach window setup (no live send)",
    ),
    outputs=(
        "qualified-pipeline list",
        "message bank",
        "intent map",
        "next-step recommendations",
    ),
    quality_gates=(
        "no_overclaim",
        "no_unverified_personal_data",
        "approval_flow_documented",
    ),
    target_delivery_days=14,
)
