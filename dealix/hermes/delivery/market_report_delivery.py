"""Market Radar Report — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


MARKET_REPORT_PLAYBOOK = Playbook(
    playbook_id="market_report_delivery",
    package_id="market_radar_report",
    steps=(
        PlaybookStep(
            name="Sector scoping",
            owner="sami",
            inputs=("buyer context",),
            outputs=("sector_brief",),
        ),
        PlaybookStep(
            name="Signal collection",
            owner="agent:growth_engine",
            inputs=("sector_brief", "channel sources"),
            outputs=("raw_signals",),
            quality_gates=("source diversity >= 5",),
        ),
        PlaybookStep(
            name="Visibility snapshot",
            owner="agent:growth_engine",
            inputs=("sector_brief",),
            outputs=("ai_visibility_snapshots",),
        ),
        PlaybookStep(
            name="Report drafting",
            owner="agent:proposal_factory",
            inputs=("raw_signals", "ai_visibility_snapshots"),
            outputs=("market_report_draft",),
            quality_gates=("trust_signal_count>=3", "no overclaim"),
        ),
        PlaybookStep(
            name="Delivery",
            owner="agent:value_reporter",
            inputs=("market_report_draft",),
            outputs=("market_report_final",),
            approval_gates=("deliver_customer_report",),
        ),
    ),
    outcome_metrics=("report_nps", "follow_on_engagements", "verified_revenue_sar"),
    upsell_path="Quarterly Market Radar retainer.",
)
