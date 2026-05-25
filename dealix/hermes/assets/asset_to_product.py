"""AssetToProduct — propose a Package draft from a high-performing asset."""

from __future__ import annotations

from dealix.hermes.assets.asset_store import Asset
from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package


def propose_product_from_asset(asset: Asset, *, package_id: str | None = None) -> Package:
    return Package(
        package_id=package_id or f"asset_pkg_{asset.asset_id}",
        name=f"Productized: {asset.title}",
        buyer="Customers matching the asset's prior usage profile.",
        pain=f"Repeated demand for {asset.kind.value} of this kind.",
        deliverables=(asset.title, "Tailored adaptation", "Outcome report"),
        price_range_sar=(5_000, 20_000),
        upsell="Recurring retainer to maintain and apply the asset.",
        trust_risks=("overgeneralisation from one-off success",),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="training_delivery",
        tags=("asset_derived",),
    )
