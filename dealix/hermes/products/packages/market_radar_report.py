"""Market Radar Report — quarterly sector signal pack."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


MARKET_RADAR_REPORT = register_package(
    Package(
        package_id="market_radar_report",
        name="Market Radar Report",
        buyer="GMs and CMOs who need a quarterly sector signal pack.",
        pain="No structured way to monitor AI adoption, channels, and competitors in their sector.",
        deliverables=(
            "Sector signal map",
            "Top 20 buying intent signals",
            "Channel and message quality benchmarks",
            "Competitor visibility snapshot in AI answers",
            "Recommended plays for next quarter",
        ),
        price_range_sar=(12_000, 40_000),
        upsell="Quarterly Market Radar retainer",
        trust_risks=("overclaim", "stale data", "sector misreads"),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="market_report_delivery",
        tags=("research",),
    )
)
