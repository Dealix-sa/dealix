from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = datetime.now().strftime("%Y-%m-%d")

PROSPECTS = ROOT / "ledgers" / "prospects.csv"
OUTBOX = ROOT / "outbox" / TODAY
REPORTS = ROOT / "reports" / "founder"
COMMAND = ROOT / "reports" / "command_room" / "index.html"

OUTBOX.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)
COMMAND.parent.mkdir(parents=True, exist_ok=True)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_message(row: dict[str, str]) -> str:
    company = row.get("company_name", "الفريق")
    sector = row.get("sector", "القطاع")
    angle = row.get("dealix_angle") or "ترتيب المتابعة والإيراد"
    product = row.get("recommended_product") or "Revenue Command Room OS"

    return f"""السلام عليكم فريق {company}،

أنا سامي من Dealix.

لاحظت أن شركات {sector} غالبًا تواجه تحدي في متابعة العملاء والفرص بين واتساب، الإيميل، العروض، والفريق — والنتيجة أن جزء من الفرص لا يظهر للإدارة في الوقت المناسب.

نحن نبني نظام تشغيل عملي باسم {product} يساعد الإدارة على:
- معرفة العملاء الذين يحتاجون متابعة اليوم
- ترتيب الفرص حسب الأولوية
- تجهيز مسودات ردود ومتابعات
- بناء غرفة قيادة يومية
- توثيق كل شيء بدون إرسال عشوائي أو وعود مبالغ فيها

زاوية البداية المقترحة لكم:
{angle}

أقدر أرسل لكم تشخيص سريع من صفحة واحدة يوضح 3 نقاط ممكن تحسن المتابعة والإيراد خلال 7 أيام.

إذا غير مناسب، أقدر أوقف التواصل فورًا.
"""


def main() -> int:
    rows = read_rows(PROSPECTS)
    ready = [
        r for r in rows
        if (r.get("verification_status") or "").lower() in {"ready_for_review", "approved_to_send"}
    ]

    drafts = []
    for idx, row in enumerate(ready[:25], start=1):
        company = row.get("company_name") or f"company_{idx}"
        safe_name = "".join(ch if ch.isalnum() else "_" for ch in company)[:80]
        message = build_message(row)
        path = OUTBOX / f"{idx:02d}_{safe_name}_draft.txt"
        path.write_text(message, encoding="utf-8")
        drafts.append({
            "company": company,
            "path": str(path),
            "product": row.get("recommended_product"),
            "decision": row.get("owner_decision", "review"),
        })

    report = {
        "date": TODAY,
        "prospects_total": len(rows),
        "ready_for_review": len(ready),
        "drafts_generated": len(drafts),
        "recommended_manual_sends_today": min(10, len(drafts)),
        "safety": {
            "external_send": "disabled_by_default",
            "mode": "draft_only_until_controlled_live",
            "approval_required": True,
        },
        "next_actions": [
            "Review first 10 drafts in outbox.",
            "Verify source_url and contact channel.",
            "Send manually only after review.",
            "Log every send in ledgers/outreach_log.csv.",
            "Classify every reply in ledgers/reply_log.csv.",
        ],
        "drafts": drafts,
    }

    (REPORTS / "latest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md = f"""# Dealix Founder Revenue Day — {TODAY}

## Executive Summary

- Prospects total: {len(rows)}
- Ready for review: {len(ready)}
- Drafts generated: {len(drafts)}
- Manual sends recommended today: {min(10, len(drafts))}

## Safety

External send remains disabled by default. Founder review is required before sending.

## Next 10 Actions

1. Open `outbox/{TODAY}`.
2. Review first 10 drafts.
3. Verify source_url for each company.
4. Remove any unsupported claim.
5. Send manually.
6. Log sends in `ledgers/outreach_log.csv`.
7. Track replies in `ledgers/reply_log.csv`.
8. Move warm replies to `ledgers/deals_pipeline.csv`.
9. Prepare 1 proposal brief.
10. Update tomorrow's angle based on replies.
"""
    (REPORTS / "latest.md").write_text(md, encoding="utf-8")

    COMMAND.write_text(f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<title>Dealix Command Room</title>
<style>
body{{font-family:Arial,sans-serif;margin:40px;background:#0b1020;color:#eef2ff}}
.card{{background:#111936;padding:24px;border-radius:16px;margin:16px 0}}
h1,h2{{color:#ffffff}}
.metric{{font-size:32px;font-weight:bold}}
</style>
</head>
<body>
<h1>Dealix Founder Command Room — {TODAY}</h1>
<div class="card"><h2>Prospects</h2><div class="metric">{len(rows)}</div></div>
<div class="card"><h2>Ready for Review</h2><div class="metric">{len(ready)}</div></div>
<div class="card"><h2>Drafts Generated</h2><div class="metric">{len(drafts)}</div></div>
<div class="card"><h2>Manual Sends Recommended</h2><div class="metric">{min(10, len(drafts))}</div></div>
<div class="card"><h2>Safety</h2><p>Draft-only by default. Controlled live outbound requires approval, opt-out, source_url, and rate limits.</p></div>
</body>
</html>
""", encoding="utf-8")

    print("FOUNDER_REVENUE_DAY_READY")
    print(f"Drafts: {len(drafts)}")
    print(f"Report: {REPORTS / 'latest.md'}")
    print(f"Command room: {COMMAND}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
