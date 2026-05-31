from __future__ import annotations

from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook

AGENCY_WHITE_LABEL_PLAYBOOK = DeliveryPlaybook(
    offer_id="agency_white_label_kit",
    name="Agency White-label Kit",
    inputs_required=(
        "partner brand kit",
        "partner approved-claims acknowledgement",
        "partner delivery capacity declaration",
    ),
    steps=(
        "partner positioning workshop",
        "approved-claims onboarding",
        "delivery playbook adaptation",
        "partner enablement quiz",
        "first co-marketing asset review",
    ),
    outputs=(
        "partner-branded playbook",
        "approved-claims library",
        "enablement completion record",
        "first co-marketing asset",
    ),
    quality_gates=(
        "approved_claims_quiz_passed",
        "no_unsupported_channels",
        "delivery_capacity_documented",
    ),
    target_delivery_days=28,
)
