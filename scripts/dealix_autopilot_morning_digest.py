#!/usr/bin/env python3
"""Consolidated founder morning digest — WS-E (Daily Founder-Approved Autopilot).

This is glue only. It aggregates the founder's daily approval workload from
the existing API surfaces and emails ONE consolidated digest to the founder.
It introduces no product modules, no API routers, and no DB tables — it ships
under the Commercial Freeze as automation of the already-built daily pipeline.

The digest summarizes:
  - drafts generated today (from the daily revenue-machine run),
  - follow-ups due,
  - the count pending in the founder approval queue,
  - overdue approvals,
  - revenue-vs-target.

Approval-queue note: the founder queue is not a single endpoint today (see
``docs/ops/WS-E_AUTOPILOT_NOTES.md`` section 2). This script aggregates from
both existing endpoints and labels each source explicitly:
  - ``GET /api/v1/approvals/pending``                    -> approval_center
  - ``GET /api/v1/dashboard/revenue-machine/today``      -> per-channel drafts

Nothing in this script sends an external message to anyone. It emails the
founder only (``DEALIX_FOUNDER_EMAIL``) and never a prospect.

Usage:
    python scripts/dealix_autopilot_morning_digest.py
    python scripts/dealix_autopilot_morning_digest.py --print     # render only
    python scripts/dealix_autopilot_morning_digest.py --dry-run   # log only

Environment:
  DEALIX_API_BASE        — API base URL (skip-gracefully upstream if unset)
  DEALIX_API_KEY         — API bearer token
  RESEND_API_KEY         — required to actually send
  DEALIX_FOUNDER_EMAIL   — recipient (founder only)
  EMAIL_PROVIDER         — "resend" (default), "sendgrid", or "smtp"

Runs via GitHub Actions cron at 04:00 UTC = 07:00 KSA, after the daily
revenue-machine draft/follow-up/report steps.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import UTC, datetime
from typing import Any

import requests

# Adjust path so we can import from repo root when run as a script.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from core.config.settings import get_settings  # noqa: E402
from integrations.email import EmailClient, EmailResult  # noqa: E402

_HTTP_TIMEOUT = 30


def _today_label() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _build_subject() -> str:
    return f"Dealix · موجز الصباح · اعتمادات اليوم · {_today_label()}"


def _get_json(base: str, path: str, api_key: str) -> dict[str, Any]:
    """GET a JSON endpoint; never raises — returns an error dict instead so
    the digest always renders."""
    url = f"{base.rstrip('/')}{path}"
    try:
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=_HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, dict) else {"_value": data}
    except Exception as exc:  # noqa: BLE001
        return {"_error": f"{type(exc).__name__}: {exc}"}


def _post_json(base: str, path: str, api_key: str) -> dict[str, Any]:
    url = f"{base.rstrip('/')}{path}"
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={},
            timeout=_HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, dict) else {"_value": data}
    except Exception as exc:  # noqa: BLE001
        return {"_error": f"{type(exc).__name__}: {exc}"}


def _count_overdue(pending: dict[str, Any]) -> int:
    """Count approval_center rows whose ``expires_at`` is in the past."""
    rows = pending.get("pending") or pending.get("rows") or pending.get("items") or []
    if not isinstance(rows, list):
        return 0
    now = datetime.now(UTC)
    overdue = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        expires = row.get("expires_at")
        if not expires:
            continue
        try:
            ts = datetime.fromisoformat(str(expires).replace("Z", "+00:00"))
        except Exception:  # noqa: BLE001
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        if ts < now:
            overdue += 1
    return overdue


def collect_digest_data(base: str, api_key: str) -> dict[str, Any]:
    """Aggregate the founder's morning workload from existing endpoints.

    Pure aggregation: no endpoint here sends anything. Returns a dict the
    renderer turns into markdown.
    """
    pending = _get_json(base, "/api/v1/approvals/pending", api_key)
    today = _get_json(base, "/api/v1/dashboard/revenue-machine/today", api_key)
    daily_report = _post_json(base, "/api/v1/automation/daily-report/generate", api_key)

    pending_rows = pending.get("pending") or pending.get("rows") or pending.get("items") or []
    pending_center = (
        pending.get("count")
        if isinstance(pending.get("count"), int)
        else (len(pending_rows) if isinstance(pending_rows, list) else 0)
    )
    pending_drafts = today.get("approval_queue_open")
    pending_drafts = pending_drafts if isinstance(pending_drafts, int) else 0
    overdue = _count_overdue(pending)

    gmail = today.get("gmail_drafts", {}) if isinstance(today.get("gmail_drafts"), dict) else {}
    linkedin = (
        today.get("linkedin_drafts", {})
        if isinstance(today.get("linkedin_drafts"), dict)
        else {}
    )
    metrics = daily_report.get("metrics", {}) if isinstance(daily_report.get("metrics"), dict) else {}

    return {
        "date": _today_label(),
        "drafts": {
            "gmail_total": gmail.get("total", 0),
            "gmail_remaining": gmail.get("remaining_to_review", 0),
            "linkedin_total": linkedin.get("total", 0),
        },
        "followups_due": metrics.get("followups_due", metrics.get("followups", "n/a")),
        "approval_queue": {
            "pending_approval_center": pending_center,
            "pending_drafts": pending_drafts,
            "pending_total": pending_center + pending_drafts,
            "overdue": overdue,
        },
        "revenue": {
            "actual": metrics.get("revenue_actual", metrics.get("revenue", "n/a")),
            "target": metrics.get("revenue_target", "n/a"),
        },
        "_errors": {
            "approvals_pending": pending.get("_error"),
            "revenue_machine_today": today.get("_error"),
            "daily_report": daily_report.get("_error"),
        },
    }


def render_digest(data: dict[str, Any]) -> str:
    """Render the aggregated data as the consolidated founder digest."""
    drafts = data["drafts"]
    queue = data["approval_queue"]
    revenue = data["revenue"]
    errors = {k: v for k, v in data.get("_errors", {}).items() if v}

    lines = [
        f"# Dealix — Morning Autopilot Digest — {data['date']}",
        "",
        "One consolidated view of everything that needs founder approval",
        "today. Approval-first: nothing was auto-sent. The autopilot prepared",
        "and queued the work below; an explicit approval is required to send.",
        "",
        "## Drafts generated today",
        f"- Gmail drafts: {drafts['gmail_total']} "
        f"({drafts['gmail_remaining']} awaiting review)",
        f"- LinkedIn drafts: {drafts['linkedin_total']}",
        "",
        "## Follow-ups",
        f"- Follow-ups due: {data['followups_due']}",
        "",
        "## Founder approval queue",
        "The founder queue spans two existing surfaces (see "
        "docs/ops/WS-E_AUTOPILOT_NOTES.md section 2):",
        f"- approval_center pending: {queue['pending_approval_center']}",
        f"- per-channel drafts pending: {queue['pending_drafts']}",
        f"- TOTAL pending approval: {queue['pending_total']}",
        f"- Overdue approvals (expired): {queue['overdue']}",
        "",
        "## Revenue vs target",
        f"- Actual: {revenue['actual']}",
        f"- Target: {revenue['target']}",
        "",
        "## Next action",
        "- Open the approval surface and clear the pending queue (~30 min).",
        "- Prioritise overdue approvals first.",
        "",
    ]
    if errors:
        lines.append("## Data warnings")
        for key, err in errors.items():
            lines.append(f"- {key}: {err}")
        lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)


def build_morning_digest() -> str:
    """Compose the consolidated morning digest as markdown text.

    Reads ``DEALIX_API_BASE`` / ``DEALIX_API_KEY`` from the environment. If
    they are unset the digest still renders with a clear note (the workflow
    skips this step upstream when secrets are missing).
    """
    base = os.environ.get("DEALIX_API_BASE", "").strip()
    api_key = os.environ.get("DEALIX_API_KEY", "").strip()
    if not base or not api_key:
        return (
            f"# Dealix — Morning Autopilot Digest — {_today_label()}\n\n"
            "API credentials not configured (DEALIX_API_BASE / DEALIX_API_KEY).\n"
            "No approval-queue data available for this digest.\n"
        )
    data = collect_digest_data(base, api_key)
    return render_digest(data)


async def _build_and_send(args: argparse.Namespace) -> EmailResult:
    settings = get_settings()
    recipient = settings.dealix_founder_email
    if not recipient and not args.print_only and not args.dry_run:
        return EmailResult(
            success=False,
            provider=settings.email_provider,
            error="dealix_founder_email_not_configured",
        )

    body_text = build_morning_digest()

    if args.print_only:
        print(body_text)
        return EmailResult(success=True, provider="print_only")

    if args.dry_run:
        print(f"[dry-run] would send to: {recipient}")
        print(f"[dry-run] subject: {_build_subject()}")
        print(f"[dry-run] body length: {len(body_text)} chars")
        print("--- body preview (first 600 chars) ---")
        print(body_text[:600])
        print("---")
        return EmailResult(success=True, provider="dry_run")

    client = EmailClient()
    return await client.send(
        to=recipient,
        subject=_build_subject(),
        body_text=body_text,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Consolidated founder morning digest")
    p.add_argument(
        "--print", dest="print_only", action="store_true",
        help="render the digest to stdout without sending email",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="render + print + log what WOULD be sent (no actual send)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = asyncio.run(_build_and_send(args))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if result.success:
        if not (args.print_only or args.dry_run):
            print(f"OK: morning digest sent via {result.provider} "
                  f"(message_id={result.message_id})")
        return 0
    print(f"FAIL: {result.provider}: {result.error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
