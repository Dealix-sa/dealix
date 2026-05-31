"""Agency White-label Kit — package + brand + playbook + revenue share."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


AGENCY_WHITE_LABEL_KIT = register_package(
    Package(
        package_id="agency_white_label_kit",
        name="Agency White-Label Kit",
        buyer="Agencies that want to sell AI services under their own brand.",
        pain="No governance, runtime, or evidence packs to back the AI offer.",
        deliverables=(
            "Brand-applied offer set",
            "Approved claims library",
            "Delivery playbooks (3 packages)",
            "Approval workflow integration",
            "Revenue-share contract",
            "Quarterly performance review",
        ),
        price_range_sar=(15_000, 75_000),
        upsell="Strategic Partner tier",
        trust_risks=("unapproved claims", "scope creep", "support overflow"),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="white_label_delivery",
        tags=("partner", "scale"),
    )
)
