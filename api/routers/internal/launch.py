"""Internal Launch summary endpoint — drives /launch frontend."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

from ._common import (
    fallback_envelope,
    private_ops_dir,
    read_csv,
    read_json,
    read_text,
)


router = APIRouter(prefix="/api/v1/internal/launch", tags=["internal-launch"])


REPO_ROOT = Path(__file__).resolve().parents[3]


def _readiness_score() -> dict[str, Any]:
    """Compute launch-readiness score by direct import of the verifier.

    Direct import is faster than subprocess and easier for coverage to
    track. Any failure is swallowed to ``decision: "error"`` so the
    endpoint never crashes the page.
    """
    scripts_dir = REPO_ROOT / "scripts"
    if not (scripts_dir / "verify_launch_readiness.py").exists():
        return {"score": None, "decision": "unknown"}
    added_path = False
    try:
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
            added_path = True
        import verify_launch_readiness as vlr  # type: ignore[import-not-found]

        checks = vlr.public_checks()
        required_failing = [c for c in checks if not c["ok"]]
        score = sum(1 for c in checks if c["ok"]) / max(1, len(checks))
        return {
            "score": round(score, 3),
            "decision": "PASS" if not required_failing else "HOLD",
            "passing": sum(1 for c in checks if c["ok"]),
            "total": len(checks),
        }
    except Exception:  # noqa: BLE001  # pragma: no cover
        return {"score": None, "decision": "error"}
    finally:
        if added_path:
            try:
                sys.path.remove(str(scripts_dir))
            except ValueError:  # pragma: no cover
                pass


@router.get("/summary", dependencies=[Depends(require_admin_key)])
def get_summary() -> dict[str, Any]:
    ops = private_ops_dir()
    readiness = _readiness_score()

    base: dict[str, Any] = {
        "source": "api" if ops else "fallback",
        "readiness_score": readiness.get("score"),
        "readiness_decision": readiness.get("decision"),
        "launch_blockers": [],
        "next_ceo_action": None,
        "active_campaign": None,
        "target_sector": None,
        "approved_assets": [],
        "distribution_queues": {},
        "trust_risks": [],
        "revenue_forecast": None,
    }

    if not ops:
        base.update(fallback_envelope("DEALIX_PRIVATE_OPS not configured"))
        return base

    blockers = read_csv(ops / "launch" / "blockers.csv")
    base["launch_blockers"] = [
        {
            "id": b.get("id"),
            "description": b.get("description", "")[:200],
            "severity": b.get("severity"),
            "status": b.get("status", "open"),
        }
        for b in blockers if (b.get("status", "open") or "").lower() == "open"
    ][:10]

    brief = read_text(ops / "founder" / "ceo_daily_brief.md", limit_kb=4)
    if brief:
        for chunk in brief.split("\n## ")[1:]:
            if chunk.lower().startswith("top ceo action"):
                lines = [ln for ln in chunk.splitlines()[1:] if ln.strip().startswith("- ")]
                if lines:
                    base["next_ceo_action"] = lines[0].lstrip("- ").strip()
                break

    base["active_campaign"] = read_text(ops / "launch" / "active_campaign.yaml", limit_kb=4)
    base["target_sector"] = read_text(ops / "launch" / "target_sector.yaml", limit_kb=4)
    base["approved_assets"] = [
        {"id": r.get("id"), "name": r.get("name"), "status": r.get("status")}
        for r in read_csv(ops / "launch" / "approved_assets.csv")
    ][:50]
    base["distribution_queues"] = read_json(ops / "distribution" / "queues.json") or {}
    base["trust_risks"] = [
        {"id": r.get("risk_id"), "severity": r.get("severity"),
         "description": (r.get("description") or "")[:200],
         "status": r.get("status")}
        for r in read_csv(ops / "trust" / "open_risks.csv")
        if (r.get("severity") or "").lower() in {"high", "critical"}
    ][:20]
    base["revenue_forecast"] = read_text(ops / "finance" / "revenue_forecast.md", limit_kb=16)
    return base
