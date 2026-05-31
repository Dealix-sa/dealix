from __future__ import annotations

from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook

AI_TRUST_KIT_PLAYBOOK = DeliveryPlaybook(
    offer_id="ai_trust_kit",
    name="AI Trust Kit",
    inputs_required=(
        "AI usage context",
        "tools used inventory",
        "data sensitivity tier",
        "approval needs",
    ),
    steps=(
        "risk intake interview",
        "agent + tool inventory",
        "permission matrix build",
        "evidence pack assembly",
        "policy authoring",
        "training mini-session",
    ),
    outputs=(
        "policy doc",
        "permission matrix",
        "approval flow doc",
        "risk register",
        "training recording",
    ),
    quality_gates=(
        "no_overclaim",
        "data_scope_defined",
        "approval_flow_documented",
        "risk_register_signed_off",
    ),
    target_delivery_days=21,
)
