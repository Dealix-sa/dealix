"""Internal Risk Register endpoint."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

from ._common import fallback_envelope, private_ops_dir, read_csv


router = APIRouter(prefix="/api/v1/internal/risks", tags=["internal-risks"])


@router.get("/register", dependencies=[Depends(require_admin_key)])
def get_register() -> dict[str, Any]:
    ops = private_ops_dir()
    if not ops:
        out = fallback_envelope("DEALIX_PRIVATE_OPS not configured")
        out["rows"] = []
        out["total"] = 0
        return out

    rows = read_csv(ops / "risk" / "risk_register.csv")
    return {
        "source": "api",
        "total": len(rows),
        "open": sum(1 for r in rows if (r.get("status") or "open").lower() == "open"),
        "critical_open": sum(
            1 for r in rows
            if (r.get("severity") or "").lower() == "critical"
            and (r.get("status") or "open").lower() == "open"
        ),
        "rows": [
            {
                "risk_id": r.get("risk_id"),
                "category": r.get("category"),
                "description": (r.get("description") or "")[:240],
                "severity": r.get("severity"),
                "likelihood": r.get("likelihood"),
                "owner": r.get("owner"),
                "mitigation": (r.get("mitigation") or "")[:240],
                "status": r.get("status") or "open",
                "next_review": r.get("next_review"),
            }
            for r in rows
        ],
    }
