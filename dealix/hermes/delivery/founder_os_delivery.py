"""Founder OS Setup — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


FOUNDER_OS_PLAYBOOK = Playbook(
    playbook_id="founder_os_delivery",
    package_id="founder_os_setup",
    steps=(
        PlaybookStep(
            name="Founder intake",
            owner="sami",
            inputs=("founder profile", "current rituals"),
            outputs=("founder_charter",),
        ),
        PlaybookStep(
            name="Decision log seed",
            owner="agent:value_reporter",
            inputs=("founder_charter",),
            outputs=("decision_log",),
        ),
        PlaybookStep(
            name="Outcome ledger seed",
            owner="agent:value_reporter",
            inputs=("founder_charter",),
            outputs=("outcome_ledger",),
        ),
        PlaybookStep(
            name="Daily approval queue + kill switch",
            owner="agent:trust_checker",
            inputs=("decision_log",),
            outputs=("approval_queue", "kill_switch_setup"),
        ),
        PlaybookStep(
            name="Sovereign memory setup",
            owner="sami",
            inputs=("founder_charter",),
            outputs=("sovereign_memory",),
        ),
    ),
    outcome_metrics=("weekly_review_completion_rate", "decision_log_rate", "approval_pass_rate"),
    upsell_path="Executive PMO Lite.",
)
