#!/usr/bin/env python3
"""Founder daily digest — composes the daily growth loop and emails
it to the founder.

Usage:
    python scripts/dealix_morning_digest.py
    python scripts/dealix_morning_digest.py --print   # don't send, just print

Environment:
  RESEND_API_KEY         — required (or another configured email provider)
  DEALIX_FOUNDER_EMAIL   — recipient (defaults to sami.assiri11@gmail.com)
  EMAIL_PROVIDER         — "resend" (default), "sendgrid", or "smtp"

Designed to run via GitHub Actions cron at 4AM UTC = 7AM KSA.
Idempotent: subject includes today's date; running twice in one day
produces two emails with the same subject (founder can spot duplicates).

Never sends to anyone except the founder.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Adjust path so we can import from repo root when run as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auto_client_acquisition.self_growth_os import daily_growth_loop
from core.config.settings import get_settings
from integrations.email import EmailClient, EmailResult

DASHBOARD_SECTION_HEADER = "## Live Dashboard Snapshot"
DASHBOARD_STUB_MESSAGE = (
    "dashboard producer not wired — see V5_COMPLETION_ROADMAP M-3 follow-up"
)


def _load_dashboard_inline() -> dict[str, Any]:
    """Produce the dashboard snapshot in-process.

    Uses ``scripts/dealix_snapshot.build_snapshot`` (the local, no-HTTP
    producer mirroring ``/api/v1/founder/dashboard``). On any failure we
    return a deterministic stub so the digest still renders and the test
    stays offline.
    """
    try:
        scripts_dir = Path(__file__).resolve().parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        import dealix_snapshot  # type: ignore[import-not-found]

        return dealix_snapshot.build_snapshot()
    except BaseException as exc:
        return {
            "status": DASHBOARD_STUB_MESSAGE,
            "_error_type": type(exc).__name__,
            "_error_message": str(exc)[:200],
        }


def _load_dashboard_from_file(path: Path) -> dict[str, Any]:
    """Read a pre-rendered dashboard JSON file. Used for back-compat."""
    return json.loads(path.read_text(encoding="utf-8"))


def render_dashboard_section(payload: dict[str, Any]) -> str:
    """Render the dashboard JSON inside a fenced markdown section."""
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    return "\n".join(
        [
            "",
            DASHBOARD_SECTION_HEADER,
            "",
            "```json",
            body,
            "```",
            "",
        ]
    )


def _today_label() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _build_subject() -> str:
    return f"Dealix · موجز اليوم · {_today_label()}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Founder morning digest")
    p.add_argument(
        "--print", dest="print_only", action="store_true",
        help="render the digest to stdout without sending email",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="render + print + log what WOULD be sent (no actual send)",
    )
    p.add_argument(
        "--dashboard-file", dest="dashboard_file", type=Path, default=None,
        help=(
            "read dashboard JSON from this file instead of producing it"
            " in-process (back-compat)"
        ),
    )
    return p.parse_args()


async def _build_and_send(args: argparse.Namespace) -> EmailResult:
    settings = get_settings()
    recipient = settings.dealix_founder_email
    if not recipient and not args.print_only and not args.dry_run:
        return EmailResult(
            success=False,
            provider=settings.email_provider,
            error="dealix_founder_email_not_configured",
        )

    loop = daily_growth_loop.build_today()
    body_text = daily_growth_loop.to_markdown(loop)

    # M-3: embed live dashboard snapshot inline in the digest body so
    # the founder receives a single email with everything (no link, no
    # attachment). --dashboard-file overrides for back-compat.
    dashboard_file = getattr(args, "dashboard_file", None)
    if dashboard_file is not None:
        dashboard_payload = _load_dashboard_from_file(dashboard_file)
    else:
        dashboard_payload = _load_dashboard_inline()
    body_text = body_text + "\n" + render_dashboard_section(dashboard_payload)

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


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # UTF-8 reconfigure is optional; default stream is fine.
        pass

    args = parse_args()
    try:
        result = asyncio.run(_build_and_send(args))
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if result.success:
        if not (args.print_only or args.dry_run):
            print(f"OK: digest sent via {result.provider} (message_id={result.message_id})")
        return 0
    print(f"FAIL: {result.provider}: {result.error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
