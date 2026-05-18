#!/usr/bin/env python3
"""Founder evening digest — composes the close-of-day summary and emails
it to the founder.

WS-E (Daily Founder-Approved Autopilot). This is glue only: it reuses the
existing close-of-day scorecard (``scripts/founder_daily_scorecard.py``) and
the existing email client. It introduces no product modules, no API
routers, and no DB tables — it ships under the Commercial Freeze as
automation of the existing daily pipeline.

The evening digest reports:
  - what was approved / sent today (close-of-day scorecard),
  - what closed today (cash received, pilots/growth signed),
  - tomorrow's setup (carried from the scorecard's "tomorrow targets").

Usage:
    python scripts/dealix_evening_digest.py
    python scripts/dealix_evening_digest.py --print   # render, do not send
    python scripts/dealix_evening_digest.py --dry-run # log what would send

Environment:
  RESEND_API_KEY         — required to actually send (skip-gracefully upstream)
  DEALIX_FOUNDER_EMAIL   — recipient (founder only; never a prospect)
  EMAIL_PROVIDER         — "resend" (default), "sendgrid", or "smtp"

Runs via GitHub Actions cron at 16:00 UTC = 19:00 KSA.
Never sends to anyone except the founder.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
from datetime import UTC, datetime

# Adjust path so we can import from repo root when run as a script.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from core.config.settings import get_settings  # noqa: E402
from integrations.email import EmailClient, EmailResult  # noqa: E402


def _today_label() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _build_subject() -> str:
    return f"Dealix · موجز المساء · {_today_label()}"


def _run_scorecard() -> str:
    """Render the existing close-of-day founder scorecard as text.

    Reuses ``scripts/founder_daily_scorecard.py`` verbatim. Falls back to a
    short note if the scorecard tooling is unavailable, so the evening
    digest never crashes the workflow.
    """
    script = os.path.join(REPO_ROOT, "scripts", "founder_daily_scorecard.py")
    try:
        completed = subprocess.run(
            [sys.executable, script, "--date", _today_label()],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
            cwd=REPO_ROOT,
        )
    except Exception as exc:  # noqa: BLE001
        return f"(scorecard unavailable: {type(exc).__name__}: {exc})"
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        return f"(scorecard exited {completed.returncode}: {detail[:300]})"
    return completed.stdout.strip() or "(scorecard produced no output)"


def build_evening_digest() -> str:
    """Compose the founder evening digest as markdown text.

    Pure composition of existing tooling; no external calls beyond the
    reused scorecard subprocess.
    """
    scorecard = _run_scorecard()
    return (
        f"# Dealix — Evening Digest — {_today_label()}\n\n"
        "Close-of-day summary. Approval-first: nothing was auto-sent. Items\n"
        "below reflect only what the founder approved today.\n\n"
        "## Close-of-day scorecard\n\n"
        f"{scorecard}\n\n"
        "## What this covers\n\n"
        "- Approved / sent today: see 'Messages sent' + 'Replies received'.\n"
        "- Closed today: see 'Cash received' + 'Pilots / Growth signed'.\n"
        "- Tomorrow's setup: see 'Tomorrow's 5 targets'.\n\n"
        "## Reminders\n\n"
        "- The morning autopilot will queue tomorrow's drafts at 07:00 KSA.\n"
        "- Review the founder approval queue before close so the morning\n"
        "  run starts from a clean backlog.\n"
    )


async def _build_and_send(args: argparse.Namespace) -> EmailResult:
    settings = get_settings()
    recipient = settings.dealix_founder_email
    if not recipient and not args.print_only and not args.dry_run:
        return EmailResult(
            success=False,
            provider=settings.email_provider,
            error="dealix_founder_email_not_configured",
        )

    body_text = build_evening_digest()

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
    p = argparse.ArgumentParser(description="Founder evening digest")
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
            print(f"OK: evening digest sent via {result.provider} "
                  f"(message_id={result.message_id})")
        return 0
    print(f"FAIL: {result.provider}: {result.error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
