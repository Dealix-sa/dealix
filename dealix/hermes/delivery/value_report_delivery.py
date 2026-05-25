from __future__ import annotations

from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook

VALUE_REPORT_PLAYBOOK = DeliveryPlaybook(
    offer_id="customer_value_report",
    name="Customer Value Report",
    inputs_required=(
        "engagement scope",
        "verified-revenue events",
        "delivered artifacts",
        "customer testimonial (optional)",
    ),
    steps=(
        "verified-revenue reconciliation",
        "attribution breakdown",
        "founder time + delivery margin summary",
        "asset reuse inventory",
        "next-quarter recommendation",
    ),
    outputs=(
        "value report PDF",
        "attribution breakdown chart",
        "delivery margin summary",
        "recommended next offer",
    ),
    quality_gates=(
        "every_revenue_line_traceable",
        "no_overclaim",
        "next_steps_signed_off",
    ),
    target_delivery_days=5,
)
