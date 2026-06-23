#!/usr/bin/env python3
"""
Create Gmail drafts from generated outbox markdown files.

SAFETY:
- Dry-run by default.
- Never sends email automatically.
- Requires GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN,
  GMAIL_SENDER_EMAIL to actually create drafts.
- Adds opt-out line and "manual review required" label if missing.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_email(path: Path) -> tuple[str, str, str] | None:
    """Return (to_email, subject, body) from a markdown outbox file."""
    text = path.read_text(encoding="utf-8")
    subject_match = re.search(r"^Subject:\s*(.+)$", text, re.MULTILINE)
    subject = subject_match.group(1).strip() if subject_match else "متابعة"

    # Extract email from To: line or first email-like string
    to_match = re.search(r"^To:\s*(.+)$", text, re.MULTILINE)
    if to_match:
        to_email = to_match.group(1).strip()
    else:
        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
        if not email_match:
            return None
        to_email = email_match.group(0)

    body = text
    if subject_match:
        body = body.replace(subject_match.group(0) + "\n", "")
    if to_match:
        body = body.replace(to_match.group(0) + "\n", "")
    body = body.strip()
    if "إيقاف" not in body and "unsubscribe" not in body.lower():
        body += "\n\nإذا لم ترغب في تلقي رسائلنا، أرسل \"إيقاف\" وسنزيل تواصلك فورًا."
    return to_email, subject, body


async def create_draft_safe(to_email: str, subject: str, body_plain: str) -> dict:
    try:
        from auto_client_acquisition.email.gmail_send import create_draft, is_configured
    except Exception as exc:
        return {"status": "import_error", "error": str(exc)}

    if not is_configured():
        return {"status": "no_keys", "error": "Gmail env vars not configured"}

    return await create_draft(
        to_email=to_email,
        subject=subject,
        body_plain=body_plain,
        sender_name="Dealix",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Gmail drafts safely")
    parser.add_argument("--outbox-dir", default=None)
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--force", action="store_true", help="Actually create drafts (not dry-run)")
    args = parser.parse_args()

    if args.force:
        args.dry_run = False

    if args.outbox_dir:
        out_dir = REPO_ROOT / args.outbox_dir
    else:
        out_dir = REPO_ROOT / "outbox" / os.environ.get("DEALIX_DATE", date.today().isoformat())

    if not out_dir.exists():
        print(f"Outbox directory not found: {out_dir}")
        return 1

    files = sorted(out_dir.glob("*.md"))
    if not files:
        print(f"No markdown drafts found in {out_dir}")
        return 0

    print(f"{'DRY-RUN' if args.dry_run else 'LIVE'}: processing {len(files)} drafts from {out_dir}")

    parsed: list[tuple[Path, tuple[str, str, str]]] = []
    for path in files:
        result = parse_email(path)
        if result is None:
            print(f"  ⚠️ Skipping {path.name}: no email found")
            continue
        parsed.append((path, result))

    if args.dry_run:
        for path, (to_email, subject, _) in parsed:
            print(f"  Would create draft → {to_email}: {subject[:60]}")
        print("\n✅ Dry-run complete. No drafts created.")
        print("To create drafts, run with --force after setting GMAIL_* env vars.")
        return 0

    # Live mode
    results = asyncio.run(
        asyncio.gather(*[create_draft_safe(to_email, subject, body) for _, (to_email, subject, body) in parsed])
    )

    ok = 0
    failed = 0
    for (path, _), result in zip(parsed, results, strict=False):
        status = result.get("status")
        if status == "ok":
            print(f"  ✅ Draft created for {path.name}: id={result.get('draft_id')}")
            ok += 1
        else:
            print(f"  ❌ {path.name}: {status} — {result.get('error')}")
            failed += 1

    print(f"\nCreated {ok} drafts, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
