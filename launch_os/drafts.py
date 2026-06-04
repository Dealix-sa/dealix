"""The 400+ daily draft factory — review-only, never sends.

Every draft is a *proposal for the founder to review*. The record carries
hard guard flags that the safety audit and verifier assert on:

    send_allowed=False, external_send_blocked=True, no_auto_send=True,
    requires_founder_approval=True

Drafts are written as JSONL (one per line) plus a human-readable founder
review markdown and a top-50 priority list.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .compliance import find_forbidden_claims
from .leads import Lead, generate_leads

# The 5-rung offer ladder (matched to ICP score bands).
OFFERS: tuple[dict[str, str], ...] = (
    {"key": "free_diagnostic", "label_en": "Free Revenue Diagnostic", "label_ar": "تشخيص إيرادات مجاني"},
    {"key": "sprint_499", "label_en": "499 SAR Revenue Sprint", "label_ar": "سبرنت إيرادات 499 ريال"},
    {"key": "data_pack_1500", "label_en": "1,500 SAR Data Pack", "label_ar": "حزمة بيانات 1,500 ريال"},
    {"key": "managed_ops", "label_en": "Managed Ops Retainer", "label_ar": "تشغيل مُدار شهري"},
    {"key": "custom_ai", "label_en": "Custom AI Build", "label_ar": "بناء AI مخصص"},
)


def _offer_for(score: int) -> dict[str, str]:
    if score >= 88:
        return OFFERS[3]
    if score >= 78:
        return OFFERS[2]
    if score >= 65:
        return OFFERS[1]
    return OFFERS[0]


def _priority(lead: Lead) -> int:
    """Founder review priority — higher = review first."""
    return min(100, lead.icp_score + (5 if lead.employees_band in ("201-500", "500+") else 0))


def build_draft(lead: Lead, ts: str) -> dict:
    """Build a single review-only draft for a lead."""
    offer = _offer_for(lead.icp_score)
    prio = _priority(lead)

    subject_en = f"A practical revenue idea for {lead.company.split(' #')[0]}"
    subject_ar = f"فكرة عملية لتحسين الإيراد لدى {lead.company_ar.split(' #')[0]}"

    body_en = (
        f"Hello,\n\n"
        f"I work with {lead.vertical_name_en} companies in {lead.city} on turning "
        f"their existing sales and follow-up data into a practical Revenue OS — "
        f"without replacing anyone on the team. Based on public signals for firms "
        f"of your size, there is usually a concrete follow-up gap worth recovering.\n\n"
        f"Would a short, no-pressure {offer['label_en']} be useful? It is human-led "
        f"and you decide every next step.\n\nBest regards,\nDealix"
    )
    body_ar = (
        f"السلام عليكم،\n\n"
        f"أعمل مع شركات {lead.vertical_name_ar} في {lead.city_ar} على تحويل بيانات "
        f"المبيعات والمتابعة الحالية إلى نظام إيراد عملي — دون استبدال أي شخص في "
        f"الفريق. عادةً توجد فجوة متابعة ملموسة يمكن استرجاعها.\n\n"
        f"هل يناسبك {offer['label_ar']} مختصر وبدون أي ضغط؟ بقيادة بشرية وأنت من "
        f"يقرر كل خطوة.\n\nتحياتي،\nDealix"
    )

    # Defensive: never let an overclaim slip into a generated body.
    overclaim = find_forbidden_claims(body_en + " " + body_ar)

    return {
        "draft_id": f"DRAFT-{lead.lead_id.split('-')[1]}",
        "created_at": ts,
        "lead_id": lead.lead_id,
        "company": lead.company,
        "company_ar": lead.company_ar,
        "vertical": lead.vertical,
        "city": lead.city,
        "channel": "founder_review_queue",
        "offer": offer["key"],
        "offer_label_en": offer["label_en"],
        "offer_label_ar": offer["label_ar"],
        "subject_en": subject_en,
        "subject_ar": subject_ar,
        "body_en": body_en,
        "body_ar": body_ar,
        "priority_score": prio,
        "icp_score": lead.icp_score,
        # ── Hard guard flags (asserted by safety audit + verifier) ──
        "send_allowed": False,
        "external_send_blocked": True,
        "no_auto_send": True,
        "requires_founder_approval": True,
        "status": "queued_for_review",
        "compliance": {
            "pdpl_ok": True,
            "no_sensitive_data": True,
            "no_overclaim": len(overclaim) == 0,
            "consent_required_before_send": True,
            "overclaim_hits": overclaim,
        },
    }


def generate_drafts(target: int = 400) -> list[dict]:
    """Generate at least ``target`` review-only drafts."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Generate a few extra leads to comfortably clear the target.
    leads = generate_leads(max(target + 20, target))
    drafts = [build_draft(lead, ts) for lead in leads]
    return drafts[: max(target + 20, len(drafts))]


def _run_dir(commercial_out: Path, ts_compact: str) -> Path:
    d = commercial_out / ts_compact
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_run(drafts: list[dict], commercial_out: Path, latest_dir: Path) -> dict:
    """Write draft_queue.jsonl, founder_review.md, top_50_priority.md.

    Writes both a timestamped run directory and the stable ``latest`` copy.
    Returns a summary dict.
    """
    ts_compact = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = _run_dir(commercial_out, ts_compact)

    # 1) JSONL queue
    queue_path = run_dir / "draft_queue.jsonl"
    with queue_path.open("w", encoding="utf-8") as fh:
        for d in drafts:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")

    # 2) Founder review markdown
    review_path = run_dir / "founder_review.md"
    review_path.write_text(_render_founder_review(drafts), encoding="utf-8")

    # 3) Top 50 priority
    top_path = run_dir / "top_50_priority.md"
    top_path.write_text(_render_top50(drafts), encoding="utf-8")

    # 4) Mirror to latest/
    latest_dir.mkdir(parents=True, exist_ok=True)
    for name in ("draft_queue.jsonl", "founder_review.md", "top_50_priority.md"):
        shutil.copy2(run_dir / name, latest_dir / name)

    return {
        "run_dir": run_dir,
        "latest_dir": latest_dir,
        "count": len(drafts),
        "queue_path": queue_path,
    }


def _render_founder_review(drafts: list[dict]) -> str:
    by_vertical: dict[str, int] = {}
    for d in drafts:
        by_vertical[d["vertical"]] = by_vertical.get(d["vertical"], 0) + 1
    lines = [
        "# Founder Review Queue — Review-Only Drafts",
        "",
        (
            "> ⛔ **None of these are sent.** Every draft is `send_allowed=false`, "
            + "`no_auto_send=true`, `external_send_blocked=true`. The founder approves "
            + "each one manually before any human-led outreach."
        ),
        "",
        f"- Total drafts: **{len(drafts)}**",
        "- By vertical:",
    ]
    for k, v in sorted(by_vertical.items()):
        lines.append(f"  - `{k}`: {v}")
    lines += ["", "## Sample (first 5)", ""]
    for d in drafts[:5]:
        lines += [
            f"### {d['draft_id']} — {d['company']} ({d['offer_label_en']})",
            f"- Priority: {d['priority_score']} · ICP: {d['icp_score']} · City: {d['city']}",
            f"- Subject (EN): {d['subject_en']}",
            f"- Subject (AR): {d['subject_ar']}",
            "",
        ]
    return "\n".join(lines) + "\n"


def _render_top50(drafts: list[dict]) -> str:
    ranked = sorted(drafts, key=lambda d: d["priority_score"], reverse=True)[:50]
    lines = [
        "# Top 50 Priority — Founder Manual Review First",
        "",
        "> Review-only. Approve manually before any human-led outreach.",
        "",
        "| # | Draft | Company | Vertical | Offer | Priority |",
        "|---|---|---|---|---|---|",
    ]
    for i, d in enumerate(ranked, 1):
        lines.append(
            f"| {i} | {d['draft_id']} | {d['company']} | {d['vertical']} | "
            f"{d['offer_label_en']} | {d['priority_score']} |"
        )
    return "\n".join(lines) + "\n"
