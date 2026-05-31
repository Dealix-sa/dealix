"""Founder OS Setup — install a founder-led operating cadence."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


FOUNDER_OS_SETUP = register_package(
    Package(
        package_id="founder_os_setup",
        name="Founder OS Setup",
        buyer="Founders running everything by hand and losing leverage.",
        pain="No weekly review, no decision log, no outcome ledger.",
        deliverables=(
            "Weekly review cadence template",
            "Decision log seed",
            "Outcome ledger seed",
            "Daily kill-switch and approval queue",
            "Sovereign memory setup",
        ),
        price_range_sar=(8_000, 18_000),
        upsell="Executive PMO Lite",
        trust_risks=("over-promise on autonomy",),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="founder_os_delivery",
        tags=("founder",),
    )
)
