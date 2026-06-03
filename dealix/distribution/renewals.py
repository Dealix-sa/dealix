"""Renewal & Upsell Engine — the real revenue is the second sale.

Builds renewal/upsell opportunities for **delivered** clients (won prospects).
The next rung is read from the canonical offers ladder
(``natural_next_offer``). Doctrine: **no upsell before proof** — a client with
evidence_level < L1 is skipped (you can't upsell value you haven't shown).
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from dealix.distribution import offers as offers_mod
from dealix.distribution import sectors as sectors_mod
from dealix.distribution.ledger import append_record, new_id, now_iso, read_records, update_status
from dealix.distribution.paths import RENEWALS_LEDGER
from dealix.distribution.prospects import load_prospects

RENEWAL_LEAD_DAYS = 90
MIN_PROOF_LEVEL = 1  # L1 — no upsell before proof


def build_renewal(client: dict[str, Any], *, today: date | None = None) -> dict[str, Any] | None:
    """Build a renewal/upsell record for a delivered client, or None if not eligible."""
    level = int(client.get("evidence_level") or 0)
    if level < MIN_PROOF_LEVEL:
        return None
    day = today or datetime.now(UTC).date()
    sector = sectors_mod.get_sector(str(client.get("sector") or "")) or {}
    current = str(client.get("current_offer") or sector.get("offer_ref") or "ai_workflow_audit")
    nxt = offers_mod.next_offer_ref(current) or "ai_ops_retainer"
    return {
        "id": new_id("renewal"),
        "client": str(client.get("company") or client.get("client") or "").strip(),
        "current_offer": current,
        "delivered_value": str(client.get("delivered_value") or "تم تسليم أول workflow محكوم"),
        "next_offer": nxt,
        "evidence_level": level,
        "due_date": (day + timedelta(days=RENEWAL_LEAD_DAYS)).isoformat(),
        "status": "upcoming",
        "created_at": now_iso(),
    }


def run_generation(
    prospects_path: Path | None = None,
    *,
    today: date | None = None,
    ledger: Path | None = None,
) -> dict[str, Any]:
    """Create renewal records for won clients without one (dedupe per client)."""
    led = ledger or RENEWALS_LEDGER
    prospects = load_prospects(prospects_path)
    won = [p for p in prospects if str(p.get("status") or "") == "won"]
    existing = read_records(led)
    have = {str(r.get("client")) for r in existing}
    new_items: list[dict[str, Any]] = []
    skipped_no_proof = 0
    for client in won:
        rec = build_renewal(client, today=today)
        if rec is None:
            skipped_no_proof += 1
            continue
        if rec["client"] in have:
            continue
        new_items.append(rec)
    for r in new_items:
        append_record(led, r)
    return {
        "won_clients": len(won),
        "new_renewals": len(new_items),
        "skipped_no_proof": skipped_no_proof,
        "ids": [r["id"] for r in new_items],
    }


def mark_renewed(renewal_id: str, ledger: Path | None = None) -> dict[str, Any] | None:
    return update_status(ledger or RENEWALS_LEDGER, renewal_id, "renewed")


def all_renewals(ledger: Path | None = None) -> list[dict[str, Any]]:
    return read_records(ledger or RENEWALS_LEDGER)


__all__ = [
    "MIN_PROOF_LEVEL",
    "RENEWAL_LEAD_DAYS",
    "all_renewals",
    "build_renewal",
    "mark_renewed",
    "run_generation",
]
