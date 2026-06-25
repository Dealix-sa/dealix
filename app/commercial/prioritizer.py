from __future__ import annotations

SECTOR_OFFER = {
    "clinics": "Follow-up Recovery OS",
    "real_estate": "Revenue Command Room OS",
    "logistics": "Revenue Command Room OS",
    "training_centers": "Follow-up Recovery OS",
    "marketing_agencies": "Client Delivery OS",
    "b2b_services": "Revenue Command Room OS",
}


def source_ok(value: str) -> bool:
    text = value.strip().lower()
    return text.startswith("https://") or text.startswith("http://")


def prioritize(row: dict[str, str]) -> dict[str, object]:
    sector = (row.get("sector") or "b2b_services").strip()
    value = 0
    reasons = []
    if sector in SECTOR_OFFER:
        value += 25
        reasons.append("sector_fit")
    if source_ok(row.get("source_url", "")):
        value += 25
        reasons.append("source_ok")
    if row.get("pain_hypothesis", "").strip():
        value += 20
        reasons.append("pain_ready")
    if row.get("owner_decision", "").strip() == "review":
        value += 10
        reasons.append("review_ready")
    level = "P1" if value >= 70 else "P2" if value >= 50 else "P3"
    return {
        "company_name": row.get("company_name", "").strip(),
        "sector": sector,
        "priority_value": value,
        "priority": level,
        "recommended_offer": row.get("recommended_offer") or SECTOR_OFFER.get(sector, "Revenue Command Room OS"),
        "reason": ", ".join(reasons),
    }


def queue(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    items = [prioritize(row) for row in rows if row.get("company_name", "").strip()]
    return sorted(items, key=lambda item: int(item["priority_value"]), reverse=True)
