#!/usr/bin/env python3
"""Revenue Forecast OS weekly 90-day forecast script.

Tests 3 synthetic open deals in dry-run mode, or calls the live API.
Writes a founder brief markdown file with 30/60/90 day forecast table.

Usage:
  python scripts/run_revenue_forecast.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


_SYNTHETIC_DEALS = [
    {
        "id": "deal_demo_001",
        "company_name": "الرياض للتقنية",
        "stage": "demo",
        "value_sar": 15000,
        "days_in_stage": 5,
        "multi_threaded": False,
    },
    {
        "id": "deal_proposal_002",
        "company_name": "جدة للخدمات",
        "stage": "proposal",
        "value_sar": 4999,
        "days_in_stage": 12,
        "multi_threaded": True,
    },
    {
        "id": "deal_negotiation_003",
        "company_name": "الدمام للأعمال",
        "stage": "negotiation",
        "value_sar": 25000,
        "days_in_stage": 8,
        "multi_threaded": True,
    },
]


def _fmt_sar(amount: float) -> str:
    return f"SAR {amount:,.0f}"


def run(dry_run: bool) -> None:
    today = date.today().isoformat()
    output_dir = ROOT / "data" / "founder_briefs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"REVENUE_FORECAST_{today}.md"

    if dry_run:
        try:
            from auto_client_acquisition.revenue_science.forecast import (
                compute_forecast,
                STAGE_BASE_PROBABILITY,
            )
        except Exception as exc:
            print(f"[Revenue Forecast] Import error: {exc}", file=sys.stderr)
            sys.exit(1)

        horizons = [30, 60, 90]
        rows: list[dict] = []
        for h in horizons:
            forecast = compute_forecast(
                customer_id="founder_portfolio",
                open_deals=_SYNTHETIC_DEALS,
                horizon_days=h,
            )
            rows.append(
                {
                    "horizon": h,
                    "best": forecast.best.revenue_sar,
                    "likely": forecast.likely.revenue_sar,
                    "worst": forecast.worst.revenue_sar,
                    "period": forecast.period_label,
                }
            )
            print(
                f"[Revenue Forecast] {h}d: "
                f"best={_fmt_sar(forecast.best.revenue_sar)} "
                f"likely={_fmt_sar(forecast.likely.revenue_sar)} "
                f"worst={_fmt_sar(forecast.worst.revenue_sar)}"
            )

        # Show stage base probabilities for reference
        stage_probs = "\n".join(
            f"  - {stage}: {prob:.0%}"
            for stage, prob in STAGE_BASE_PROBABILITY.items()
            if stage not in ("won", "lost")
        )

        brief = f"""# Revenue Forecast — توقعات الإيرادات
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: dry-run (synthetic deals)
**Open Deals in Pipeline**: {len(_SYNTHETIC_DEALS)}

---

## 30 / 60 / 90-Day Forecast Table

| Horizon | Best Case | Likely | Worst Case |
|---------|-----------|--------|------------|
"""
        for r in rows:
            brief += (
                f"| {r['horizon']} days | "
                f"{_fmt_sar(r['best'])} | "
                f"{_fmt_sar(r['likely'])} | "
                f"{_fmt_sar(r['worst'])} |\n"
            )

        brief += f"""
## Open Deals Summary

| Deal ID | Company | Stage | Value (SAR) |
|---------|---------|-------|-------------|
"""
        for d in _SYNTHETIC_DEALS:
            brief += (
                f"| {d['id']} | {d['company_name']} | "
                f"{d['stage']} | {_fmt_sar(d['value_sar'])} |\n"
            )

        brief += f"""
## Stage Base Probabilities (Reference)

{stage_probs}

---
_is_estimate=True. All revenue projections are estimates. Require founder review before external sharing._
"""
        output_path.write_text(brief, encoding="utf-8")
        print(f"[Revenue Forecast] Brief written → {output_path}")
        return

    # Live mode
    import urllib.request
    api_base = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me")
    admin_key = os.environ.get("DEALIX_ADMIN_API_KEY", "")

    def _post(path: str, payload: dict) -> dict:
        url = f"{api_base}{path}"
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "X-Admin-API-Key": admin_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())

    try:
        result = _post(
            "/api/v1/revenue-forecast/scenarios",
            {
                "customer_id": "founder_portfolio",
                "open_deals": _SYNTHETIC_DEALS,
                "horizon_days": 90,
            },
        )
    except Exception as exc:
        print(f"[Revenue Forecast] API call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    brief = f"""# Revenue Forecast — توقعات الإيرادات
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: live

---

## Forecast Results
"""
    for scenario in ["best", "likely", "worst"]:
        s = result.get(scenario, {})
        brief += f"- **{scenario.title()}**: {_fmt_sar(s.get('revenue_sar', 0))}\n"

    brief += "\n---\n_is_estimate=True. All revenue projections are estimates. Require founder review before external sharing._\n"
    output_path.write_text(brief, encoding="utf-8")
    print(f"[Revenue Forecast] Brief written → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Revenue Forecast OS")
    parser.add_argument("--dry-run", action="store_true", help="Use local modules; no HTTP calls")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
