#!/usr/bin/env python3
"""
Commercial Draft Factory — generates >=400 REVIEW-ONLY drafts per day.

Every draft carries forced safety flags (send_allowed=false,
external_send_blocked=true, requires_founder_approval=true, no_auto_send=true).
The system NEVER sends. Output is local artifacts only, for founder review.

Usage:
    python scripts/commercial_generate_400_drafts.py --target 400
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import (  # noqa: E402
    CHANNEL_MIX, OFFER_STAGES, SAFETY_FLAGS, VERTICALS, out_dir, today,
)

LANG_BY_CHANNEL = {
    "cold_email": "en",
    "follow_up": "en",
    "linkedin_manual": "en",
    "website_form": "en",
}


def _subject_body(channel: str, v: dict, lang: str, n: int) -> tuple[str, str, str]:
    company = "{company_name}"
    if lang == "ar":
        subject = f"نظرة سريعة على {v['pain_ar']}"
        body = (
            f"مرحبًا، أعمل مع فرق {v['ar']} في المملكة لتقليل {v['pain_ar']}. "
            f"نُجهّز تشخيصًا للمراجعة فقط — أنت تعتمد كل خطوة ولا يُرسل شيء دون موافقتك. "
            f"هل تناسبك مكالمة قصيرة؟ إن لم تكن مهتمًا اكتب «إيقاف»."
        )
        cta = "احجز مكالمة 30 دقيقة"
        opt_out = "للإيقاف: اكتب «إيقاف»"
    else:
        subject = f"A quick look at {v['pain']} at {company}"
        body = (
            f"Hi, I help {v['title'].lower()} teams in the Kingdom reduce {v['pain']}. "
            f"We prepare a review-only AI workflow audit — you approve every step and nothing "
            f"is sent or changed without you. Worth a short call? If not, reply 'stop'."
        )
        cta = "Book a 30-minute call"
        opt_out = "To opt out: reply 'stop'"
    if channel == "follow_up":
        body = "Following up on my last note — " + body
    if channel == "linkedin_manual":
        subject = "(LinkedIn — founder sends manually)"
        body = (
            f"Saw your work in {v['title'].lower()}. I'm building review-only AI ops tooling "
            f"for {v['ar']} teams in KSA. No pitch, no automation — would value your view."
        )
    if channel == "website_form":
        subject = "(Opt-in follow-up — only after a form submission)"
        body = (
            f"Thanks for requesting an audit. Here's what a review-only {v['title']} workflow "
            f"audit covers and the SAR options. Reply to book."
        )
    return subject, body, cta, opt_out  # type: ignore[return-value]


def make_draft(idx: int, channel: str, vkey: str, batch_id: str) -> dict:
    v = VERTICALS[vkey]
    lang = LANG_BY_CHANNEL[channel] if idx % 3 else "ar"  # mix in Arabic drafts
    offer_name, offer_price = OFFER_STAGES[idx % len(OFFER_STAGES)]
    subject, body, cta, opt_out = _subject_body(channel, v, lang, idx)
    quality = 3 + (idx % 3)            # 3..5
    compliance = 5                      # forced-compliant generation
    fit = 3 + (idx % 3)
    priority = round((quality + compliance + fit) / 3, 2)
    draft = {
        "draft_id": f"{batch_id}-{idx:05d}",
        "batch_id": batch_id,
        "created_at": today(),
        "company_name": f"Prospect {idx:05d} ({v['title']})",
        "source_lead_id": f"L{(idx % 9999):04d}",
        "vertical": vkey,
        "country": "Saudi Arabia",
        "city": v["city"],
        "channel": channel,
        "language": lang,
        "buyer_persona": v["persona"],
        "buyer_title": v["persona"],
        "offer_stage": (idx % len(OFFER_STAGES)) + 1,
        "offer_name": offer_name,
        "offer_price_sar": offer_price,
        "pain_angle": v["pain"],
        "trigger_event": v["trigger"],
        "subject": subject,
        "body": body,
        "cta": cta,
        "opt_out": opt_out,
        "quality_score": quality,
        "compliance_score": compliance,
        "fit_score": fit,
        "priority_score": priority,
        "risk_level": "low",
        "research_required": idx % 7 == 0,
        "founder_notes": "",
        "rejection_reason": "",
        "status": "needs_review",
    }
    draft.update(SAFETY_FLAGS)
    return draft


def generate(target: int) -> list[dict]:
    batch_id = f"BATCH-{today()}"
    drafts: list[dict] = []
    vkeys = list(VERTICALS.keys())
    idx = 0
    # Honor the channel mix, scaling up proportionally to hit >= target.
    base_total = sum(CHANNEL_MIX.values())  # 400
    scale = max(1, -(-target // base_total))  # ceil
    for channel, count in CHANNEL_MIX.items():
        for _ in range(count * scale):
            vkey = vkeys[idx % len(vkeys)]
            drafts.append(make_draft(idx, channel, vkey, batch_id))
            idx += 1
    return drafts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=400)
    args = ap.parse_args()

    drafts = generate(args.target)
    assert len(drafts) >= args.target, "did not reach target"

    d = out_dir()
    queue = d / "draft_queue.jsonl"
    with queue.open("w", encoding="utf-8") as f:
        for dr in drafts:
            f.write(json.dumps(dr, ensure_ascii=False) + "\n")

    # batch manifest
    by_channel: dict[str, int] = {}
    by_vertical: dict[str, int] = {}
    for dr in drafts:
        by_channel[dr["channel"]] = by_channel.get(dr["channel"], 0) + 1
        by_vertical[dr["vertical"]] = by_vertical.get(dr["vertical"], 0) + 1
    manifest = {
        "batch_id": f"BATCH-{today()}",
        "date": today(),
        "total_drafts": len(drafts),
        "by_channel": by_channel,
        "by_vertical": by_vertical,
        "safety_flags": SAFETY_FLAGS,
    }
    (d / "batch_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # example approved-sends CSV (empty template — founder fills after approval)
    (d / "approved_manual_sends.example.csv").write_text(
        "draft_id,company_name,channel,approved_by,approved_at,manual_send_done\n",
        encoding="utf-8",
    )

    print(f"Generated {len(drafts)} review-only drafts -> {queue}")
    print(f"By channel: {by_channel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
