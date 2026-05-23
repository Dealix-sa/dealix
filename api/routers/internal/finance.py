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


@router.get("/forecast", dependencies=[Depends(require_admin_key)])
def get_forecast() -> dict[str, Any]:
    ops = private_ops_dir()
    if not ops:
        out = fallback_envelope("DEALIX_PRIVATE_OPS not configured")
        out["forecast_markdown"] = None
        return out

    # Reuse the forecast script's compute() if available — fall back to file.
    forecast_md = read_text(ops / "finance" / "revenue_forecast.md", limit_kb=64)

    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from generate_revenue_forecast import compute as compute_forecast  # type: ignore
        data = compute_forecast(ops)
    except Exception:  # noqa: BLE001
        data = {}
    finally:
        try:
            sys.path.remove(str(REPO_ROOT / "scripts"))
        except ValueError:
            pass

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
