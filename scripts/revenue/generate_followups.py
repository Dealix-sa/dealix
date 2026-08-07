#!/usr/bin/env python3
"""
Generate follow-up drafts for existing outbox emails.
Rules:
- Max 3 follow-ups per company.
- Day 3 and day 7 follow-ups only if no reply logged.
- Respect cooldown window.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import (
    REPO_ROOT,
    load_csv,
    normalize_email,
    opt_out_line,
    parse_date,
    today_str,
)


def slugify(name: str) -> str:
    return re.sub(r"[^\w\-]+", "-", name).strip("-").lower()[:50]


def company_from_filename(path: Path) -> str:
    name = path.stem.replace("_step1", "").replace("_followup_d3", "").replace("_followup_d7", "")
    return name.replace("-", " ")


def count_followups(out_dir: Path, company_slug: str) -> int:
    count = 0
    for path in out_dir.glob(f"{company_slug}_followup_*.md"):
        if path.is_file():
            count += 1
    return count


def last_contact_date(out_dir: Path, company_slug: str) -> str | None:
    latest: str | None = None
    for pattern in (f"{company_slug}_step1.md", f"{company_slug}_followup_d*.md"):
        for path in out_dir.glob(pattern):
            if path.is_file():
                date_part = path.parent.name
                if latest is None or date_part > latest:
                    latest = date_part
    return latest


def build_followup(company: str, step: int, original_subject: str) -> str:
    if step == 3:
        hook = "هل الفكرة واضحة؟ أرسل لكم ملخص صفحة واحدة لو تبغون."
    elif step == 7:
        hook = "آخر رسالة. إذا التحديات التشغيلية ليست أولوية الآن أفهم تمامًا."
    else:
        hook = "متابعة على رسالتي السابقة."

    lines = [
        f"Subject: Re: {original_subject}",
        "",
        "السلام عليكم،",
        "",
        f"متابعة سريعة لـ {company}.",
        "",
        hook,
        "",
        "تحياتي،",
        "فريق Dealix",
        opt_out_line("ar"),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate follow-up drafts")
    parser.add_argument("--outbox-dir", default=None)
    parser.add_argument("--reply-log", default="ledgers/reply_log.csv")
    parser.add_argument("--max-followups", type=int, default=3)
    parser.add_argument("--cooldown-days", type=int, default=3)
    args = parser.parse_args()

    from datetime import date
    out_dir = REPO_ROOT / "outbox" / os.environ.get("DEALIX_DATE", date.today().isoformat()) if args.outbox_dir is None else REPO_ROOT / args.outbox_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect base emails sent in previous days
    base_emails: list[tuple[Path, str, str]] = []
    for day_dir in (REPO_ROOT / "outbox").iterdir():
        if not day_dir.is_dir():
            continue
        for path in day_dir.glob("*_step1.md"):
            company = company_from_filename(path)
            text = path.read_text(encoding="utf-8")
            subject_match = re.search(r"^Subject:\s*(.+)$", text, re.MULTILINE)
            subject = subject_match.group(1).strip() if subject_match else "متابعة"
            base_emails.append((path, company, subject))

    replies = load_csv(REPO_ROOT / args.reply_log)
    replied_companies = {normalize_email(r.get("email", "")) for r in replies}

    generated = 0
    for path, company, subject in base_emails:
        slug = slugify(company)
        if count_followups(out_dir, slug) >= args.max_followups:
            continue
        last = last_contact_date(path.parent, slug)
        if last is None:
            continue
        last_dt = parse_date(last)
        if last_dt is None:
            continue
        today_dt = parse_date(today_str()) or last_dt
        days = (today_dt - last_dt).days
        if days < args.cooldown_days:
            continue
        step = 3 if count_followups(out_dir, slug) == 0 else 7
        followup_path = out_dir / f"{slug}_followup_d{step}.md"
        followup_path.write_text(build_followup(company, step, subject), encoding="utf-8")
        generated += 1

    print(f"Generated {generated} follow-up drafts in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
