#!/usr/bin/env python3
"""Customer Health OS weekly churn scan script.

Tests 3 synthetic customers in dry-run mode, or calls the live API.
Writes a founder brief markdown file.

Usage:
  python scripts/run_customer_health_scan.py [--dry-run]
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


_SYNTHETIC_CUSTOMERS = [
    {
        "customer_id": "cust_critical_001",
        "days_since_last_login": 45,
        "monthly_engagement_drop_pct": 0.75,
        "support_tickets_open": 4,
        "billing_failures_last_90d": 2,
        "nps": 4,
        "months_as_customer": 8,
    },
    {
        "customer_id": "cust_at_risk_002",
        "days_since_last_login": 20,
        "monthly_engagement_drop_pct": 0.40,
        "support_tickets_open": 2,
        "billing_failures_last_90d": 1,
        "nps": 6,
        "months_as_customer": 5,
    },
    {
        "customer_id": "cust_safe_003",
        "days_since_last_login": 2,
        "monthly_engagement_drop_pct": 0.05,
        "support_tickets_open": 0,
        "billing_failures_last_90d": 0,
        "nps": 9,
        "months_as_customer": 14,
    },
]


def run(dry_run: bool) -> None:
    today = date.today().isoformat()
    output_dir = ROOT / "data" / "founder_briefs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"CUSTOMER_HEALTH_{today}.md"

    if dry_run:
        try:
            from auto_client_acquisition.revenue_science.churn_model import predict_churn
        except Exception as exc:
            print(f"[Customer Health] Import error: {exc}", file=sys.stderr)
            sys.exit(1)

        results = []
        for c in _SYNTHETIC_CUSTOMERS:
            prediction = predict_churn(
                customer_id=c["customer_id"],
                days_since_last_login=c["days_since_last_login"],
                monthly_engagement_drop_pct=c["monthly_engagement_drop_pct"],
                support_tickets_open=c["support_tickets_open"],
                billing_failures_last_90d=c["billing_failures_last_90d"],
                nps=c.get("nps"),
                months_as_customer=c["months_as_customer"],
            )
            results.append(prediction)
            print(
                f"[Customer Health] {prediction.customer_id}: "
                f"score={prediction.score:.2f} band={prediction.band}"
            )

        brief = f"""# Customer Health Scan — نظام صحة العملاء
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: dry-run (synthetic customers)

---

## Churn Scan Results

| Customer ID | Score | Band | Drivers |
|-------------|-------|------|---------|
"""
        for r in results:
            drivers_str = "; ".join(r.drivers[:2]) or "—"
            brief += f"| {r.customer_id} | {r.score:.0%} | {r.band} | {drivers_str} |\n"

        brief += "\n## Recommended Actions\n\n"
        for r in results:
            brief += f"**{r.customer_id}** ({r.band}):\n"
            brief += f"> {r.recommended_action_ar}\n\n"

        critical = [r for r in results if r.band == "critical"]
        at_risk = [r for r in results if r.band == "at_risk"]
        if critical:
            brief += f"\n**P0 Alert**: {len(critical)} customer(s) in CRITICAL band — immediate action required.\n"
        if at_risk:
            brief += f"**P1 Alert**: {len(at_risk)} customer(s) AT RISK — schedule calls this week.\n"

        brief += "\n---\n_is_estimate=True. All scores are estimates. Require human review before any external action._\n"
        output_path.write_text(brief, encoding="utf-8")
        print(f"[Customer Health] Brief written → {output_path}")
        return

    # Live mode
    import urllib.request
    api_base = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me")
    admin_key = os.environ.get("DEALIX_ADMIN_API_KEY", "")
    api_key = os.environ.get("DEALIX_API_KEY", "")

    def _post(path: str, payload: dict) -> dict:
        url = f"{api_base}{path}"
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key,
                "X-Admin-API-Key": admin_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())

    brief = f"""# Customer Health Scan — نظام صحة العملاء
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: live

---

"""
    for c in _SYNTHETIC_CUSTOMERS:
        try:
            result = _post("/api/v1/customer-health/churn-predict", c)
            brief += (
                f"- **{result.get('customer_id', c['customer_id'])}**: "
                f"score={result.get('score', 0):.2f} "
                f"band={result.get('band', '—')}\n"
            )
        except Exception as exc:
            print(f"[Customer Health] API call failed for {c['customer_id']}: {exc}", file=sys.stderr)

    brief += "\n---\n_is_estimate=True. All scores are estimates. Require human review before any external action._\n"
    output_path.write_text(brief, encoding="utf-8")
    print(f"[Customer Health] Brief written → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Customer Health OS scan")
    parser.add_argument("--dry-run", action="store_true", help="Use local modules; no HTTP calls")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
