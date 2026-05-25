"""
assets — the Revenue Asset Store.

Every reusable artifact created by an agent or human is registered here.
Assets that get reused 3+ times and influence verified revenue become
candidates for productization.
"""

from dealix.hermes.assets.asset_commercialization import commercialization_candidates
from dealix.hermes.assets.asset_quality import grade_asset
from dealix.hermes.assets.asset_reuse import record_reuse
from dealix.hermes.assets.asset_store import (
    ASSET_STORE,
    Asset,
    AssetKind,
    register_asset,
)
from dealix.hermes.assets.asset_to_product import propose_product_from_asset

__all__ = [
    "ASSET_STORE",
    "Asset",
    "AssetKind",
    "commercialization_candidates",
    "grade_asset",
    "propose_product_from_asset",
    "record_reuse",
    "register_asset",
]
