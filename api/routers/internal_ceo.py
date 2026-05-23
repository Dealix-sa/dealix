from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/internal/ceo", tags=["internal-ceo"])


@router.get("/summary")
def ceo_summary() -> dict[str, object]:
    return {
        "top_action": "Approve outreach batch",
        "status": "C3 Revenue Partial",
        "risk_flags": 0,
        "cash_collected_sar": 0,
        "approved_outreach": 0,
        "positive_replies": 0,
        "proposals_due": 0,
        "payment_followups_due": 0,
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
