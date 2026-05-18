#!/usr/bin/env python3
"""Daily LLM cost alert — closes Launch Gate O4.

Queries the live ``/api/v1/admin/costs`` endpoint, sums LLM spend over a
window (default 24h), and raises an alert when spend crosses a threshold
(default $10/day, gate O4 DoD).

Doctrine (Article 4 — IMMUTABLE):
- This script NEVER sends anything to a customer. It is internal infra
  observability only. It reports to stdout + a gitignored file and signals
  breach via a non-zero exit code.
- The founder wires the exit code to their own alerting (cron ``MAILTO``,
  a CI step, or a Slack incoming-webhook the founder configures). No send
  capability is built in here.

Exit codes:
    0 = spend under threshold (or zero) — all good
    1 = spend AT or OVER threshold — founder should review
    2 = could not reach the costs API — operational error

Usage:
    python3 scripts/daily_cost_alert.py
    python3 scripts/daily_cost_alert.py --window-hours 24 --threshold-usd 10
    python3 scripts/daily_cost_alert.py --format json

Environment:
    DEALIX_API_BASE             default http://127.0.0.1:8000
    DEALIX_API_KEY              value for the X-API-Key header
    DEALIX_ADMIN_API_KEY        value for the X-Admin-API-Key header
    DEALIX_DAILY_COST_ALERT_USD default threshold when --threshold-usd omitted

Cron example (09:00 KSA = 06:00 UTC daily; cron mails on non-zero exit):
    0 6 * * * cd /home/user/dealix && python3 scripts/daily_cost_alert.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = REPO_ROOT / "data" / "cost_alerts"
DEFAULT_THRESHOLD_USD = 10.0


def evaluate_spend(total_usd: float, threshold_usd: float) -> dict[str, Any]:
    """Pure decision function — testable without any network.

    Returns the alert verdict. ``breached`` is True when spend is at or
    above the threshold.
    """
    total_usd = round(float(total_usd), 4)
    threshold_usd = round(float(threshold_usd), 4)
    breached = total_usd >= threshold_usd
    headroom = round(threshold_usd - total_usd, 4)
    return {
        "total_usd": total_usd,
        "threshold_usd": threshold_usd,
        "breached": breached,
        "headroom_usd": headroom,
        "severity": "alert" if breached else "ok",
        "is_estimate": True,  # Article 8 — costs are estimates
    }


def _fetch_costs(
    *,
    api_base: str,
    api_key: str | None,
    admin_key: str | None,
    window_hours: int,
) -> dict[str, Any]:
    """Hit the admin costs endpoint. Raises RuntimeError on any failure."""
    import httpx

    url = f"{api_base.rstrip('/')}/api/v1/admin/costs"
    headers: dict[str, str] = {}
    if api_key:
        headers["X-API-Key"] = api_key
    if admin_key:
        headers["X-Admin-API-Key"] = admin_key
    try:
        resp = httpx.get(
            url,
            params={"window_hours": window_hours, "group_by": "model"},
            headers=headers,
            timeout=15.0,
        )
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()
        return data
    except Exception as exc:
        raise RuntimeError(f"costs API unreachable at {url}: {exc}") from exc


def build_report(
    *,
    window_hours: int,
    threshold_usd: float,
    api_base: str,
    api_key: str | None,
    admin_key: str | None,
) -> dict[str, Any]:
    """Fetch spend and produce the full alert report."""
    costs = _fetch_costs(
        api_base=api_base,
        api_key=api_key,
        admin_key=admin_key,
        window_hours=window_hours,
    )
    total_usd = float(costs.get("totals", {}).get("usd", 0.0))
    verdict = evaluate_spend(total_usd, threshold_usd)
    return {
        "gate": "O4",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "window_hours": window_hours,
        **verdict,
        "by_model": costs.get("by_group", {}),
        "calls": costs.get("totals", {}).get("calls", 0),
    }


def render_markdown(report: dict[str, Any]) -> str:
    icon = "🔴" if report["breached"] else "🟢"
    lines = [
        f"# {icon} Dealix Daily Cost Alert · {report['generated_at']}",
        "",
        f"- Window: last **{report['window_hours']}h**",
        f"- Spend: **${report['total_usd']:.4f}** "
        f"(estimate) · Threshold: **${report['threshold_usd']:.2f}**",
        f"- Headroom: **${report['headroom_usd']:.4f}**",
        f"- LLM calls: {report['calls']}",
        f"- Verdict: **{report['severity'].upper()}**",
        "",
    ]
    if report["by_model"]:
        lines.append("## By model")
        lines.append("")
        lines.append("| Model | USD | Calls |")
        lines.append("|---|---|---|")
        for model, g in sorted(
            report["by_model"].items(),
            key=lambda kv: kv[1].get("usd", 0),
            reverse=True,
        ):
            lines.append(f"| `{model}` | {g.get('usd', 0):.4f} | {g.get('calls', 0)} |")
        lines.append("")
    if report["breached"]:
        lines.append(
            "> ⚠️ Spend crossed the daily threshold. Review "
            "`/api/v1/admin/costs` and the model mix above."
        )
    lines.append("")
    lines.append("_Article 8: spend is an estimate. Article 4: no auto-send._")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--window-hours", type=int, default=24)
    p.add_argument(
        "--threshold-usd",
        type=float,
        default=float(os.getenv("DEALIX_DAILY_COST_ALERT_USD", DEFAULT_THRESHOLD_USD)),
    )
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument(
        "--out",
        default=None,
        help="Write report to this path (default: gitignored data/cost_alerts/).",
    )
    args = p.parse_args()

    api_base = os.getenv("DEALIX_API_BASE", "http://127.0.0.1:8000")
    api_key = os.getenv("DEALIX_API_KEY")
    admin_key = os.getenv("DEALIX_ADMIN_API_KEY")

    try:
        report = build_report(
            window_hours=args.window_hours,
            threshold_usd=args.threshold_usd,
            api_base=api_base,
            api_key=api_key,
            admin_key=admin_key,
        )
    except RuntimeError as exc:
        print(f"ERROR · {exc}", file=sys.stderr)
        return 2

    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(report)
    )

    out_path = (
        Path(args.out)
        if args.out
        else DEFAULT_OUT_DIR / f"{datetime.now(UTC):%Y-%m-%d}.{args.format}"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    print(f"\nWROTE · {out_path}", file=sys.stderr)

    return 1 if report["breached"] else 0


if __name__ == "__main__":
    sys.exit(main())
