from __future__ import annotations

from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook

MARKET_RADAR_PLAYBOOK = DeliveryPlaybook(
    offer_id="market_radar",
    name="Market Radar",
    inputs_required=(
        "target industry list",
        "target geography list",
        "competitor watchlist",
    ),
    steps=(
        "industry signal harvest (trusted sources only)",
        "competitor positioning snapshot",
        "intent-signal scoring",
        "opportunity packs assembly",
        "founder review",
    ),
    outputs=(
        "weekly opportunity packs",
        "competitor positioning snapshot",
        "intent-signal scoring file",
    ),
    quality_gates=(
        "sources_traceable",
        "no_personal_data_in_packs",
        "approved_claims_only",
    ),
    target_delivery_days=7,
)
