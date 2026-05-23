"""Internal Finance / Revenue Forecast endpoint."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

from ._common import fallback_envelope, private_ops_dir, read_text


router = APIRouter(prefix="/api/v1/internal/finance", tags=["internal-finance"])


REPO_ROOT = Path(__file__).resolve().parents[3]


def _compute_forecast(ops: Path) -> dict[str, Any]:
    """Direct-import the forecast computer. Defensive against missing script."""
    scripts_dir = REPO_ROOT / "scripts"
    if not (scripts_dir / "generate_revenue_forecast.py").exists():  # pragma: no cover
        return {}
    added_path = False
    try:
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
            added_path = True
        from generate_revenue_forecast import compute  # type: ignore[import-not-found]
        return compute(ops) or {}
    except Exception:  # noqa: BLE001  # pragma: no cover
        return {}
    finally:
        if added_path:
            try:
                sys.path.remove(str(scripts_dir))
            except ValueError:  # pragma: no cover
                pass


@router.get("/forecast", dependencies=[Depends(require_admin_key)])
def get_forecast() -> dict[str, Any]:
    ops = private_ops_dir()
    if not ops:
        out = fallback_envelope("DEALIX_PRIVATE_OPS not configured")
        out["forecast_markdown"] = None
        return out

    forecast_md = read_text(ops / "finance" / "revenue_forecast.md", limit_kb=64)
    data = _compute_forecast(ops)
    return {
        "source": "api",
        "forecast_markdown": forecast_md,
        "cash_collected_sar": data.get("cash_collected_sar"),
        "open_proposal_value_sar": data.get("open_proposal_value_sar"),
        "weighted_pipeline_sar": data.get("weighted_pipeline_sar"),
        "payment_risk_count": data.get("payment_risk_count"),
        "next_cash_action": data.get("next_cash_action"),
        "forecast_confidence": data.get("forecast_confidence"),
    }
