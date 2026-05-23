"""Internal Learning Memory summary endpoint."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

from ._common import fallback_envelope, private_ops_dir, read_csv


router = APIRouter(prefix="/api/v1/internal/learning", tags=["internal-learning"])


LOGS = {
    "market": "market_learning.csv",
    "message": "message_learning.csv",
    "offer": "offer_learning.csv",
    "sector": "sector_learning.csv",
}


@router.get("/summary", dependencies=[Depends(require_admin_key)])
def get_summary(limit: int = 10) -> dict[str, Any]:
    ops = private_ops_dir()
    if not ops:
        out = fallback_envelope("DEALIX_PRIVATE_OPS not configured")
        out["logs"] = {k: [] for k in LOGS}
        return out

    limit = max(1, min(int(limit or 10), 100))
    logs: dict[str, Any] = {}
    for key, fname in LOGS.items():
        rows = read_csv(ops / "learning" / fname)
        # Newest first by date if available.
        rows = sorted(rows, key=lambda r: (r.get("date") or ""), reverse=True)
        logs[key] = {
            "total": len(rows),
            "latest": [
                {
                    "date": r.get("date"),
                    "source": r.get("source"),
                    "insight": (r.get("insight") or "")[:240],
                    "decision": r.get("decision"),
                    "next_action": (r.get("next_action") or "")[:200],
                    "owner": r.get("owner"),
                }
                for r in rows[:limit]
            ],
        }
    return {"source": "api", "logs": logs}
