"""
Seed offers + ICPs into a Revenue Marketing OS store on first run.

This is opt-in (called by the router/CLI, not by the store
constructor) so tests get an empty store unless they ask for the
seed explicitly.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from dealix.revenue_marketing_os.schemas import ICPRecord, OfferRecord
from dealix.revenue_marketing_os.store import RevenueMarketingStore, uid


def _seed_path() -> Path:
    return Path(__file__).resolve().parent / "seed_offers.yaml"


def seed_if_empty(store: RevenueMarketingStore) -> dict[str, int]:
    """
    Load seed offers + ICPs if the store has none. Returns the
    counts of records added so the caller can audit.
    """
    existing_offers = store.list_offers()
    existing_icps = store.list_icps()
    if existing_offers and existing_icps:
        return {"offers_added": 0, "icps_added": 0}

    raw = yaml.safe_load(_seed_path().read_text(encoding="utf-8"))
    offers_added = 0
    icps_added = 0

    if not existing_offers:
        for row in raw.get("offers") or []:
            row_id = str(row.get("id") or uid("offer"))
            store.upsert_offer(
                OfferRecord(
                    id=row_id,
                    name=row.get("name") or row_id,
                    tier=row.get("tier") or "core",
                    ladder_step=int(row.get("ladder_step") or 2),
                    starting_price_sar=float(row.get("starting_price_sar") or 0),
                    repeatability=float(row.get("repeatability") or 0.5),
                    margin=float(row.get("margin") or 0.5),
                    retainer_potential=float(row.get("retainer_potential") or 0.5),
                    data_moat=float(row.get("data_moat") or 0.3),
                    partner_potential=float(row.get("partner_potential") or 0.3),
                    delivery_burden=float(row.get("delivery_burden") or 0.3),
                )
            )
            offers_added += 1

    if not existing_icps:
        for row in raw.get("icps") or []:
            row_id = str(row.get("id") or uid("icp"))
            store.upsert_icp(
                ICPRecord(
                    id=row_id,
                    name=row.get("name") or row_id,
                    buyer=row.get("buyer") or "",
                    pain=row.get("pain") or "",
                    ability_to_pay=row.get("ability_to_pay") or "medium",
                    urgency=row.get("urgency") or "medium",
                    best_offer_id=row.get("best_offer_id") or "",
                    best_channel=row.get("best_channel") or "direct_outreach",
                    message_angle=row.get("message_angle") or "",
                    entry_offer_id=row.get("entry_offer_id") or "",
                    expansion_offer_id=row.get("expansion_offer_id") or "",
                )
            )
            icps_added += 1

    return {"offers_added": offers_added, "icps_added": icps_added}
