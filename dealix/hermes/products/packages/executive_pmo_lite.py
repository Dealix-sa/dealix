"""Executive PMO Lite — a thin layer of program management with AI."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


EXECUTIVE_PMO_LITE = register_package(
    Package(
        package_id="executive_pmo_lite",
        name="Executive PMO Lite",
        buyer="Executive teams that need a thin program-management layer with AI assistance.",
        pain="Decisions and outcomes are not tracked; meetings repeat without progress.",
        deliverables=(
            "Weekly executive review pack",
            "Decision log and outcome ledger",
            "Risk register and approval queue",
            "Customer value reports for top accounts",
            "Quarterly strategic memo",
        ),
        price_range_sar=(20_000, 60_000),
        upsell="Quarterly Strategic Partner retainer",
        trust_risks=("overclaim on autonomy", "sovereign data exposure"),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="executive_pmo_delivery",
        tags=("executive",),
    )
)
