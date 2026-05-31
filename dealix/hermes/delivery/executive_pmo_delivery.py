"""Executive PMO Lite — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


EXECUTIVE_PMO_PLAYBOOK = Playbook(
    playbook_id="executive_pmo_delivery",
    package_id="executive_pmo_lite",
    steps=(
        PlaybookStep(
            name="Onboarding",
            owner="sami",
            inputs=("executive team brief",),
            outputs=("pmo_charter",),
        ),
        PlaybookStep(
            name="Weekly review cadence",
            owner="agent:value_reporter",
            inputs=("decisions", "outcomes"),
            outputs=("weekly_review_pack",),
        ),
        PlaybookStep(
            name="Risk and approval register",
            owner="agent:trust_checker",
            inputs=("risk events", "approval tickets"),
            outputs=("risk_register", "approval_queue"),
        ),
        PlaybookStep(
            name="Customer value reports",
            owner="agent:value_reporter",
            inputs=("top accounts",),
            outputs=("value_reports",),
            approval_gates=("deliver_customer_report",),
        ),
        PlaybookStep(
            name="Quarterly strategic memo",
            owner="sami",
            inputs=("verified_revenue", "graph insights"),
            outputs=("strategic_memo",),
        ),
    ),
    outcome_metrics=("verified_revenue_sar", "decision_log_rate", "approval_pass_rate"),
    upsell_path="Strategic Partner retainer.",
)
