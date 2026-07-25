"""Generate the daily Dealix CEO brief from current operating data.

Usage:
    python3 scripts/generate_daily_ceo_brief.py

Outputs:
    business/reports/exports/dealix-daily-ceo-brief-YYYY-MM-DD.txt
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "reports" / "exports"
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
OUTREACH_QUEUE_PATH = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


ACQUISITION_FUNNEL = [
    ("Discover", "اكتشاف", "Identify companies with visible operational leakage."),
    ("Qualify", "تأهيل", "Score against BANT, segment, weakness severity."),
    ("Outreach (Drafts Only)", "تواصل (مسوّدة فقط)", "Generate bilingual drafts."),
    ("Human Review Gate", "بوابة المراجعة البشرية", "Approve/reject every draft."),
    ("Workflow Review Call", "مكالمة مراجعة سير العمل", "20-min diagnostic call."),
    ("Proposal", "عرض رسمي", "Generate bilingual proposal."),
    ("Close", "إغلاق", "Convert to won deal with setup + retainer."),
    ("Deliver", "تسليم", "Run Delivery OS end-to-end."),
    ("Retain & Expand", "احتفاظ وتوسعة", "Monthly review + expansion offer."),
]

DELIVERY_PIPELINE = [
    ("Day 0 — Intake", "0–1", "Signed contract, stakeholder map, channel of truth."),
    ("Workflow Map", "2–4", "End-to-end workflow map, pain points tagged."),
    ("Command Center Setup", "5–8", "URL live, owners assigned, cadence defined."),
    ("Automation Build", "9–14", "Top 3 automations live + fallback + audit log."),
    ("Weekly Executive Review", "15+", "Weekly report, sign-off, proof items logged."),
    ("Expansion", "30+", "Quarterly review, expansion offer, case study draft."),
]

STATIC_KPIS = [
    ("MRR (SAR)", 250000, 42000, "monthly", "watch"),
    ("Active Retainers", 12, 3, "monthly", "on_track"),
    ("Proposal → Close %", 35, 22, "monthly", "watch"),
    ("Proof Items Logged", 20, 7, "monthly", "watch"),
]

PRIORITIES = [
    (1, "Clear the review queue", 1),
    (2, "Ship launch brief + CEO brief", 1),
    (3, "First 100 leads plan", 3),
    (4, "Deployment readiness", 5),
    (5, "First retainer contract", 14),
]


def _read_json(path: Path, fallback: dict) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return fallback
    return data if isinstance(data, dict) else fallback


def load_operating_metrics(date: dt.date) -> dict[str, int]:
    """Return current metrics from generated operating artifacts.

    Missing or malformed files degrade to zero instead of inventing values.
    """
    leads = _read_json(LEADS_PATH, {"accounts": []}).get("accounts", [])
    queue = _read_json(OUTREACH_QUEUE_PATH, {"drafts": []}).get("drafts", [])

    pending = sum(
        1
        for draft in queue
        if "pending" in str(draft.get("reviewStatus", "")).lower()
    )
    due = 0
    upcoming = 0
    for account in leads:
        raw_date = account.get("nextActionDate")
        if not raw_date:
            continue
        try:
            action_date = dt.date.fromisoformat(str(raw_date))
        except ValueError:
            continue
        if action_date <= date:
            due += 1
        elif (action_date - date).days <= 7:
            upcoming += 1

    return {
        "drafts_pending_review": pending,
        "followups_due_today": due,
        "followups_upcoming_7d": upcoming,
    }


def render_brief(date: dt.date, metrics: dict[str, int] | None = None) -> str:
    current = metrics or load_operating_metrics(date)
    kpis = [
        *STATIC_KPIS[:3],
        ("Drafts Pending Review", 0, current["drafts_pending_review"], "daily", "attention"),
        ("Follow-ups Due Today", 0, current["followups_due_today"], "daily", "attention"),
        *STATIC_KPIS[3:],
    ]

    lines: list[str] = []
    lines.append(f"# Dealix Daily CEO Brief — {date.isoformat()}")
    lines.append("")
    lines.append("## 1. Acquisition Moves")
    for title, title_ar, goal in ACQUISITION_FUNNEL[:5]:
        lines.append(f"- **{title}** ({title_ar}): {goal}")
    lines.append("")
    lines.append("## 2. Delivery Moves")
    for title, day_range, deliverable in DELIVERY_PIPELINE[:3]:
        lines.append(f"- **{title}** ({day_range}) — {deliverable}")
    lines.append("")
    lines.append("## 3. KPI Checks")
    for label, target, value, cadence, status in kpis:
        if target == 0:
            indicator = "CLEAR" if value == 0 else "ACTION"
            lines.append(f"- [{indicator}] {label}: current {value} — {cadence} · {status}")
            continue
        gap = round(((value - target) / max(1, target)) * 100)
        indicator = "OK" if gap >= 0 else "GAP"
        lines.append(
            f"- [{indicator}] {label}: target {target}, current {value} ({gap}%) — {cadence} · {status}"
        )
    lines.append("")
    lines.append("## 4. Runtime Truth")
    lines.append(f"- Drafts awaiting human review: {current['drafts_pending_review']}")
    lines.append(f"- Follow-ups due now: {current['followups_due_today']}")
    lines.append(f"- Follow-ups in next 7 days: {current['followups_upcoming_7d']}")
    lines.append("- Source: current leads and canonical outreach review queue; missing data is reported as zero.")
    lines.append("")
    lines.append("## 5. Risks")
    if current["drafts_pending_review"]:
        lines.append("- Review queue not cleared → no outreach should be sent.")
    if current["followups_due_today"]:
        lines.append("- Follow-ups are due → assign an owner before the end of the operating day.")
    lines.append("- Conversion rate below 35% — tighten close criteria and proposal quality.")
    lines.append("- Proof vault underused — coach delivery lead to log proof items weekly.")
    lines.append("- MRR target not met — slow expansion, speed up retainer conversion.")
    lines.append("")
    lines.append("## 6. Operating Focus")
    for rank, title, due in PRIORITIES:
        lines.append(f"- [P{rank}] {title} — due in {due}d")
    lines.append("")
    lines.append("---")
    lines.append("Draft only. Human review required before any external action.")
    return "\n".join(lines) + "\n"


def main() -> None:
    today = dt.date.today()
    out_path = EXPORT_DIR / f"dealix-daily-ceo-brief-{today.isoformat()}.txt"
    out_path.write_text(render_brief(today), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
