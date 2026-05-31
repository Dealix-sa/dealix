"""Revenue Hunter Pilot — sourced + scored + drafted opportunities, no external sends."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


REVENUE_HUNTER_PILOT = register_package(
    Package(
        package_id="revenue_hunter_pilot",
        name="Revenue Hunter Pilot",
        buyer="B2B founders and sales leaders selling into KSA enterprise.",
        pain="ICP and outbound research costs weeks; little of it converts.",
        deliverables=(
            "ICP profile and account list",
            "Scored and ranked leads with evidence",
            "Outbound message drafts (3 variants)",
            "Proposal drafts for top accounts",
            "Outcome report with verified revenue tracking",
        ),
        price_range_sar=(7_500, 25_000),
        upsell="Revenue Hunter Managed (monthly retainer)",
        trust_risks=("overclaim", "PDPL scope", "competitor confusion"),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="revenue_hunter_delivery",
        tags=("flagship", "growth"),
    )
)
