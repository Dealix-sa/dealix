#!/usr/bin/env python3
"""
Dealix Daily Gmail Drafts — حقيقي يومي في Gmail.

يقوم كل صباح بـ:
  1. تشغيل Revenue Machine لإنتاج Gmail drafts + LinkedIn drafts + call scripts.
  2. دفع Gmail drafts إلى Drafts folder فعلياً (إذا مُفعّل OAuth).
  3. طباعة/إرسال ملخص عربي للمؤسس.

Usage:
    python scripts/run_dealix_daily_gmail_drafts.py
    python scripts/run_dealix_daily_gmail_drafts.py --dry-run
    python scripts/run_dealix_daily_gmail_drafts.py --no-digest

Env:
    DEALIX_API_BASE          — e.g. http://localhost:8000
    DEALIX_ADMIN_API_KEY     — admin key
    GMAIL_CLIENT_ID          — Gmail OAuth (optional but recommended)
    GMAIL_CLIENT_SECRET
    GMAIL_REFRESH_TOKEN
    GMAIL_SENDER_EMAIL
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import httpx

from auto_client_acquisition.email.gmail_send import is_configured as gmail_is_configured

API_TIMEOUT = 120.0


def _today_label() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _api_base() -> str:
    return (os.getenv("DEALIX_API_BASE") or "http://localhost:8000").rstrip("/")


def _admin_key() -> str:
    return os.getenv("DEALIX_ADMIN_API_KEY") or os.getenv("DEALIX_API_KEY") or ""


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if callable(reconf):
            try:
                reconf(encoding="utf-8")
            except Exception:
                pass


def _headers() -> dict[str, str]:
    key = _admin_key()
    h: dict[str, str] = {"Content-Type": "application/json"}
    if key:
        h["X-Admin-API-Key"] = key
        h["Authorization"] = f"Bearer {key}"
    return h


async def _run_revenue_machine(
    *,
    gmail_drafts: int = 15,
    linkedin_drafts: int = 8,
    call_scripts: int = 5,
    create_in_gmail: bool = True,
) -> dict[str, Any]:
    payload = {
        "gmail_drafts": gmail_drafts,
        "linkedin_drafts": linkedin_drafts,
        "call_scripts": call_scripts,
        "approval_mode": "draft_only",
        "create_gmail_drafts_in_inbox": create_in_gmail,
    }
    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        resp = await client.post(
            f"{_api_base()}/api/v1/automation/revenue-machine/run",
            json=payload,
            headers=_headers(),
        )
        resp.raise_for_status()
        return resp.json()


async def _fetch_gmail_drafts_today() -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            f"{_api_base()}/api/v1/gmail/drafts/today",
            headers=_headers(),
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        return data.get("drafts") or data.get("items") or []


def _render_report(machine_result: dict[str, Any], gmail_drafts: list[dict[str, Any]]) -> str:
    gmail_count = len(gmail_drafts)
    linkedin_count = len(machine_result.get("linkedin_drafts") or [])
    call_count = len(machine_result.get("call_scripts") or [])
    created_in_inbox = machine_result.get("created_in_gmail_inbox", 0)
    errors = machine_result.get("errors") or []

    lines = [
        f"# Dealix · ملخص drafts اليوم · {_today_label()}",
        "",
        f"- Gmail drafts: {gmail_count} (تم إنشاء {created_in_inbox} في inbox)",
        f"- LinkedIn drafts: {linkedin_count}",
        f"- Call scripts: {call_count}",
    ]

    if gmail_drafts:
        lines.extend(["", "## أهم Gmail drafts اليوم"])
        for i, d in enumerate(gmail_drafts[:10], start=1):
            company = d.get("company") or d.get("account_name") or "—"
            subject = d.get("subject") or "—"
            lines.append(f"{i}. {company} — {subject}")

    if errors:
        lines.extend(["", "## أخطاء", ""])
        for err in errors[:5]:
            lines.append(f"- {err}")

    lines.extend([
        "",
        "## خطوة تالية",
        "افتح Gmail → Drafts و راجع المسودات قبل الإرسال.",
    ])
    return "\n".join(lines)


async def _send_digest(report: str, *, dry_run: bool) -> None:
    if dry_run:
        print("\n[dry-run] would send digest:\n")
        print(report[:800])
        print("\n...")
        return

    # Import here to avoid heavy deps when running in API-only mode.
    try:
        from integrations.email import EmailClient

        client = EmailClient()
        settings_module = __import__("core.config.settings", fromlist=["get_settings"])
        settings = settings_module.get_settings()
        recipient = settings.dealix_founder_email
        if not recipient:
            print("WARN: DEALIX_FOUNDER_EMAIL not configured; skipping digest send", file=sys.stderr)
            print(report)
            return
        result = await client.send(
            to=recipient,
            subject=f"Dealix · drafts اليوم · {_today_label()}",
            body_text=report,
        )
        if result.success:
            print(f"OK: digest sent via {result.provider}")
        else:
            print(f"WARN: digest send failed: {result.error}", file=sys.stderr)
    except Exception as exc:
        print(f"WARN: digest send failed: {exc}", file=sys.stderr)
        print(report)


async def main() -> int:
    ap = argparse.ArgumentParser(description="Dealix daily Gmail drafts runner")
    ap.add_argument("--dry-run", action="store_true", help="No side effects; print plan")
    ap.add_argument("--no-digest", action="store_true", help="Skip sending the digest email")
    ap.add_argument("--gmail-drafts", type=int, default=15, help="Number of Gmail drafts")
    ap.add_argument("--linkedin-drafts", type=int, default=8, help="Number of LinkedIn drafts")
    ap.add_argument("--call-scripts", type=int, default=5, help="Number of call scripts")
    ap.add_argument("--no-create-in-gmail", action="store_true", help="Do not push drafts to Gmail inbox")
    args = ap.parse_args()
    _ensure_utf8_stdio()

    create_in_gmail = not args.no_create_in_gmail
    if create_in_gmail and not gmail_is_configured():
        print(
            "WARN: Gmail OAuth not configured; drafts will be stored locally only. "
            "Set GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN, GMAIL_SENDER_EMAIL.",
            file=sys.stderr,
        )

    if args.dry_run:
        print("[dry-run] would run revenue machine with:")
        print(f"  gmail_drafts={args.gmail_drafts}")
        print(f"  linkedin_drafts={args.linkedin_drafts}")
        print(f"  call_scripts={args.call_scripts}")
        print(f"  create_gmail_drafts_in_inbox={create_in_gmail}")
        print(f"  api_base={_api_base()}")
        return 0

    print(f"Running revenue machine at {_api_base()} ...")
    machine_result = await _run_revenue_machine(
        gmail_drafts=args.gmail_drafts,
        linkedin_drafts=args.linkedin_drafts,
        call_scripts=args.call_scripts,
        create_in_gmail=create_in_gmail,
    )
    print("Revenue machine OK.")

    gmail_drafts = await _fetch_gmail_drafts_today()
    report = _render_report(machine_result, gmail_drafts)

    print("\n" + report)

    if not args.no_digest:
        await _send_digest(report, dry_run=False)

    print("\nDONE")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
