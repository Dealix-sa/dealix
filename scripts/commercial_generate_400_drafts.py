#!/usr/bin/env python3
"""
Dealix Commercial Draft Factory — review-only draft generator.

Generates >=400 bilingual (AR/EN) outreach DRAFTS for manual founder review.
Every draft is marked review-only and can NEVER be sent automatically:
  - send_allowed = False
  - external_send_blocked = True
  - no_auto_send = True

Doctrine (non-negotiable):
  - No external sending of any kind happens here.
  - No mail transport, no chat-platform automation, no professional-network automation.
  - Output is an artifact for human review and manual, approved outreach only.

Usage:
    python scripts/commercial_generate_400_drafts.py --target 400
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "outputs" / "commercial_launch" / "latest"

VERTICALS = [
    ("construction_contracting", "Procurement Manager", "مدير المشتريات"),
    ("healthcare_clinics", "Operations Director", "مدير العمليات"),
    ("logistics_supply_chain", "Supply Chain Lead", "مسؤول سلسلة الإمداد"),
    ("retail_fnb_chains", "Regional GM", "المدير الإقليمي"),
    ("professional_services", "Managing Partner", "الشريك التنفيذي"),
]

PAIN_EN = {
    "construction_contracting": "scattered tender and supplier data slowing procurement decisions",
    "healthcare_clinics": "fragmented patient-flow and revenue data across branches",
    "logistics_supply_chain": "low visibility on lane profitability and customer churn signals",
    "retail_fnb_chains": "no single view of branch-level revenue and basket trends",
    "professional_services": "manual pipeline tracking with weak account prioritization",
}
PAIN_AR = {
    "construction_contracting": "تشتت بيانات المناقصات والموردين وتأخر قرارات الشراء",
    "healthcare_clinics": "تجزؤ بيانات تدفق المرضى والإيراد بين الفروع",
    "logistics_supply_chain": "ضعف الرؤية على ربحية المسارات وإشارات تسرب العملاء",
    "retail_fnb_chains": "غياب رؤية موحّدة لإيراد الفروع واتجاهات السلة",
    "professional_services": "تتبع يدوي للفرص وضعف ترتيب أولويات الحسابات",
}

# Neutral, manual-only outreach channels. No platform-automation channels.
CHANNELS = ["email_manual_draft", "call_script_manual", "meeting_request_manual"]


def build_draft(idx: int, rng: random.Random) -> dict:
    vertical, role_en, role_ar = VERTICALS[idx % len(VERTICALS)]
    company = f"Saudi {vertical.split('_')[0].title()} Co {idx:04d}"
    channel = CHANNELS[idx % len(CHANNELS)]
    score = 60 + (idx * 7 + rng.randint(0, 9)) % 40  # 60..99, deterministic-ish

    subject_en = "A 7-day Revenue Intelligence read on your data"
    subject_ar = "قراءة ذكاء إيرادي خلال 7 أيام على بياناتك"
    body_en = (
        f"Hi — at {company}, teams like yours often face "
        f"{PAIN_EN[vertical]}. Dealix runs a 7-day Revenue Intelligence Sprint "
        f"that turns your existing data into a scored, approval-first action list. "
        f"No data leaves without your sign-off, and nothing is sent on your behalf. "
        f"Would a short discovery call this week be useful?"
    )
    body_ar = (
        f"مرحبًا — في {company}، الفرق المشابهة غالبًا تواجه {PAIN_AR[vertical]}. "
        f"ديالكس ينفّذ Sprint ذكاء إيرادي خلال 7 أيام يحوّل بياناتك الحالية إلى "
        f"قائمة إجراءات مرتّبة بالأولوية وبموافقة أولاً. لا تُرسل أي بيانات دون "
        f"موافقتك، ولا يتم إرسال أي رسالة نيابة عنك. هل تناسبك مكالمة استكشاف قصيرة هذا الأسبوع؟"
    )

    return {
        "id": f"DRAFT-{idx:04d}",
        "vertical": vertical,
        "company": company,
        "contact_role_en": role_en,
        "contact_role_ar": role_ar,
        "channel": channel,
        "subject_en": subject_en,
        "subject_ar": subject_ar,
        "body_en": body_en,
        "body_ar": body_ar,
        "priority_score": score,
        "status": "draft_for_review",
        "requires_founder_approval": True,
        # Non-negotiable safety flags — verified by the safety audit and control tower.
        "send_allowed": False,
        "external_send_blocked": True,
        "no_auto_send": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def write_outputs(drafts: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) draft_queue.jsonl
    queue = OUT_DIR / "draft_queue.jsonl"
    with queue.open("w", encoding="utf-8") as f:
        for d in drafts:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    # 2) top_50_priority.md
    top = sorted(drafts, key=lambda d: d["priority_score"], reverse=True)[:50]
    top_md = ["# Top 50 Priority Drafts (review-only)\n",
              "> Manual review required. Nothing here is sent automatically.\n"]
    top_md.append("\n| # | ID | Vertical | Company | Role | Score |\n|---|----|----------|---------|------|-------|")
    for i, d in enumerate(top, 1):
        top_md.append(
            f"| {i} | {d['id']} | {d['vertical']} | {d['company']} | "
            f"{d['contact_role_en']} | {d['priority_score']} |"
        )
    (OUT_DIR / "top_50_priority.md").write_text("\n".join(top_md) + "\n", encoding="utf-8")

    # 3) founder_review.md
    rev = [
        "# Founder Review Queue (review-only)\n",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Total drafts: **{len(drafts)}**",
        "- Send allowed: **0** (every draft is review-only)",
        "- External send: **blocked** for all drafts",
        "",
        "## How to use",
        "1. Review the Top 50 first (`top_50_priority.md`).",
        "2. Approve / edit / reject each draft manually.",
        "3. Send approved messages yourself, manually — never from automation.",
        "",
        "## Sample (first 5 drafts)",
    ]
    for d in drafts[:5]:
        rev.append(f"\n### {d['id']} — {d['company']} ({d['vertical']})")
        rev.append(f"**EN:** {d['body_en']}")
        rev.append(f"\n**AR:** {d['body_ar']}")
    (OUT_DIR / "founder_review.md").write_text("\n".join(rev) + "\n", encoding="utf-8")

    # 4) daily_metrics.json (base — readiness step may enrich)
    by_vertical: dict[str, int] = {}
    for d in drafts:
        by_vertical[d["vertical"]] = by_vertical.get(d["vertical"], 0) + 1
    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "draft_count": len(drafts),
        "send_allowed_true_count": sum(1 for d in drafts if d.get("send_allowed")),
        "external_send_blocked_false_count": sum(
            1 for d in drafts if d.get("external_send_blocked") is False
        ),
        "no_auto_send_false_count": sum(1 for d in drafts if d.get("no_auto_send") is False),
        "by_vertical": by_vertical,
        "top_score": max(d["priority_score"] for d in drafts),
    }
    (OUT_DIR / "daily_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def generate(target: int) -> list[dict]:
    rng = random.Random(20260604)
    return [build_draft(i + 1, rng) for i in range(target)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate >=400 review-only outreach drafts")
    ap.add_argument("--target", type=int, default=400, help="number of drafts to generate")
    args = ap.parse_args()

    target = max(args.target, 400)  # floor at 400 by doctrine
    drafts = generate(target)
    write_outputs(drafts)

    print(f"[draft-factory] generated {len(drafts)} review-only drafts -> {OUT_DIR}")
    print("[draft-factory] send_allowed for all drafts: False (no external send)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
