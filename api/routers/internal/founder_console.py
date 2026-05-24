"""Founder Console — read-only views over private_ops, gated by internal token.

Mount in api/main.py with:
    from api.routers.internal.founder_console import router as founder_console_router
    app.include_router(founder_console_router, prefix="/api/v1/internal")

Every endpoint:
    * requires X-Dealix-Internal-Token (production) via auth.require_internal_token
    * reads only from $DEALIX_PRIVATE_OPS
    * never triggers an external send
"""
from __future__ import annotations

try:
    from fastapi import APIRouter, Depends
except Exception:  # pragma: no cover
    APIRouter = None  # type: ignore[assignment]
    Depends = lambda x: x  # type: ignore[assignment]

from api.internal import runtime_reader
from api.internal.auth import require_internal_token

router = APIRouter(tags=["internal", "founder-console"]) if APIRouter else None


if router is not None:

    @router.get("/ceo/summary", dependencies=[Depends(require_internal_token)])
    def ceo_summary() -> dict:
        s = runtime_reader.summary()
        if not s.get("ok"):
            return {"ok": False, "error": s.get("error", "private_ops unavailable")}
        s["counts"] = {sec: len(files) for sec, files in s["sections"].items()}
        return s

    @router.get("/approvals/queue", dependencies=[Depends(require_internal_token)])
    def approvals_queue() -> dict:
        rows = runtime_reader.read_csv("approvals", "approval_queue.csv")
        open_ = [r for r in rows if (r.get("status") or "").lower() in
                 {"", "open", "pending", "awaiting_founder"}]
        return {"total": len(rows), "open": len(open_), "items": open_[:50]}

    @router.get("/finance/forecast", dependencies=[Depends(require_internal_token)])
    def finance_forecast() -> dict:
        md = runtime_reader.read_markdown("finance", "revenue_forecast.md")
        return {"present": bool(md), "markdown": md[:8000]}

    @router.get("/trust/incidents", dependencies=[Depends(require_internal_token)])
    def trust_incidents() -> dict:
        rows = runtime_reader.read_csv("trust", "incidents.csv")
        open_ = [r for r in rows if (r.get("status") or "").lower() in
                 {"", "open", "investigating"}]
        return {"total": len(rows), "open": len(open_), "items": open_[:50]}
