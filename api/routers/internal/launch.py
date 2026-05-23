"""Internal Launch summary endpoint — drives /launch frontend."""

from __future__ import annotations

import subprocess
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
    """Run launch_readiness verifier in JSON mode; tolerate any failure."""
    script = REPO_ROOT / "scripts" / "verify_launch_readiness.py"
    if not script.exists():
        return {"score": None, "decision": "unknown", "checks": []}
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--json"],
            capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=30,
        )
        import json as _json
        data = _json.loads(result.stdout or "{}")
        return {
            "score": data.get("readiness_score"),
            "decision": data.get("decision"),
            "passing": data.get("passing"),
            "total": data.get("total"),
        }
    except Exception:  # noqa: BLE001
        return {"score": None, "decision": "error", "checks": []}


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
        # Find Top CEO Action line
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
