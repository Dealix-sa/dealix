"""Agency White-Label Kit — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


WHITE_LABEL_PLAYBOOK = Playbook(
    playbook_id="white_label_delivery",
    package_id="agency_white_label_kit",
    steps=(
        PlaybookStep(
            name="Partner intake",
            owner="sami",
            inputs=("agency profile", "target sectors"),
            outputs=("partner_profile",),
            approval_gates=("modify_revenue_share",),
        ),
        PlaybookStep(
            name="Approved claims library",
            owner="agent:trust_checker",
            inputs=("brand voice", "regulatory constraints"),
            outputs=("approved_claims",),
        ),
        PlaybookStep(
            name="Playbook adaptation",
            owner="agent:proposal_factory",
            inputs=("approved_claims", "package shelf"),
            outputs=("adapted_playbooks",),
        ),
        PlaybookStep(
            name="Partner enablement workshop",
            owner="sami",
            inputs=("adapted_playbooks", "evidence_pack"),
            outputs=("enabled_partner",),
        ),
        PlaybookStep(
            name="Quarterly review",
            owner="agent:value_reporter",
            inputs=("partner verified revenue",),
            outputs=("quarterly_review",),
        ),
    ),
    outcome_metrics=(
        "partner_verified_revenue_sar",
        "approved_claims_count",
        "incidents_per_partner",
    ),
    upsell_path="Strategic Partner tier.",
)
