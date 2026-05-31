"""Revenue Hunter Pilot — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


REVENUE_HUNTER_PLAYBOOK = Playbook(
    playbook_id="revenue_hunter_delivery",
    package_id="revenue_hunter_pilot",
    steps=(
        PlaybookStep(
            name="ICP research",
            owner="agent:revenue_hunter",
            inputs=("buyer brief", "offer constraints"),
            outputs=("icp_profile",),
            quality_gates=("trust_signal_count>=2",),
        ),
        PlaybookStep(
            name="Lead scoring",
            owner="agent:revenue_hunter",
            inputs=("icp_profile", "target accounts"),
            outputs=("ranked_leads",),
            quality_gates=("PDPL-safe data only",),
        ),
        PlaybookStep(
            name="Message drafting",
            owner="agent:revenue_hunter",
            inputs=("ranked_leads", "approved claims"),
            outputs=("message_drafts",),
            quality_gates=("no overclaim phrases",),
        ),
        PlaybookStep(
            name="Proposal drafting",
            owner="agent:proposal_factory",
            inputs=("top accounts", "pricing recommendation"),
            outputs=("proposal_drafts",),
            quality_gates=("pricing_engine confidence >= 0.6",),
            approval_gates=("approve_pricing",),
        ),
        PlaybookStep(
            name="Outcome report",
            owner="agent:value_reporter",
            inputs=("touches", "verified_revenue"),
            outputs=("outcome_report",),
            quality_gates=("verified revenue logged",),
            approval_gates=("deliver_customer_report",),
        ),
    ),
    outcome_metrics=(
        "qualified_leads",
        "proposals_drafted",
        "verified_revenue_sar",
        "retainer_conversion",
    ),
    upsell_path="Revenue Hunter Managed (monthly retainer).",
)
