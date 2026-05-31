"""Training — generic delivery playbook for workshops."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


TRAINING_PLAYBOOK = Playbook(
    playbook_id="training_delivery",
    package_id="founder_os_setup",
    steps=(
        PlaybookStep(
            name="Audience and outcome",
            owner="sami",
            inputs=("audience profile", "desired outcome"),
            outputs=("training_brief",),
        ),
        PlaybookStep(
            name="Workshop deck",
            owner="agent:proposal_factory",
            inputs=("training_brief", "approved claims"),
            outputs=("workshop_deck",),
            quality_gates=("no overclaim", "PDPL-safe examples"),
        ),
        PlaybookStep(
            name="Run workshop",
            owner="sami",
            inputs=("workshop_deck",),
            outputs=("workshop_recording", "feedback"),
        ),
        PlaybookStep(
            name="Post-workshop follow-up",
            owner="agent:value_reporter",
            inputs=("feedback", "next steps"),
            outputs=("followup_pack",),
            approval_gates=("deliver_customer_report",),
        ),
    ),
    outcome_metrics=("nps", "next_step_conversion", "verified_revenue_sar"),
    upsell_path="Founder OS Setup or Executive PMO Lite.",
)
