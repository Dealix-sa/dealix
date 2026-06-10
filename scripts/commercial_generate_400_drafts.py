#!/usr/bin/env python3
"""Dealix Daily Draft Factory — generate 400+ founder-review-only outreach drafts.

Distribution (default target 400):
  - 175 cold email drafts
  - 100 follow-up drafts
  -  75 LinkedIn manual drafts
  -  50 website / contact form drafts

NON-NEGOTIABLE: every draft is review-only. send_allowed=False,
external_send_blocked=True, requires_founder_approval=True, no_auto_send=True.
This script writes files to disk ONLY. It never opens a network connection.

Usage:
  python scripts/commercial_generate_400_drafts.py --target 400
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import (
    NON_NEGOTIABLE_RULE,
    SAFETY_FLAGS,
    load_offers,
    load_seed_leads,
    now_iso,
    output_day_dir,
    today_str,
    write_json,
    write_jsonl,
)

CHANNEL_MIX = {
    "cold_email": 175,
    "follow_up": 100,
    "linkedin_manual": 75,
    "website_form": 50,
}

OFFER_BY_STAGE_ORDER = ["audit", "pilot", "department_os", "retainer", "enterprise"]


def _scale_mix(target: int) -> dict[str, int]:
    base = sum(CHANNEL_MIX.values())
    if target <= base:
        return dict(CHANNEL_MIX)
    # Scale proportionally, then pad the largest channel to hit target exactly.
    factor = target / base
    scaled = {k: round(v * factor) for k, v in CHANNEL_MIX.items()}
    diff = target - sum(scaled.values())
    scaled["cold_email"] += diff
    return scaled


def _subject(channel: str, lang: str, vertical: dict, offer: dict, angle: str) -> str:
    name = vertical["name_ar"] if lang == "ar" else vertical["name"]
    offer_name = offer["name_ar"] if lang == "ar" else offer["name"]
    if lang == "ar":
        templates = {
            "cold_email": f"{offer_name} لـ{name} — فكرة عملية",
            "follow_up": f"متابعة سريعة: {angle}",
            "linkedin_manual": f"سؤال عن {angle} في قطاع {name}",
            "website_form": f"طلب {offer_name}",
        }
    else:
        templates = {
            "cold_email": f"{offer_name} for {name} — a practical idea",
            "follow_up": f"Quick follow-up: {angle}",
            "linkedin_manual": f"A question about {angle} in {name}",
            "website_form": f"Request: {offer_name}",
        }
    return templates[channel]


def _body(
    channel: str,
    lang: str,
    vertical: dict,
    offer: dict,
    angle: str,
    pain: str,
    trigger: str,
    company: str,
) -> str:
    offer_name = offer["name_ar"] if lang == "ar" else offer["name"]
    if lang == "ar":
        opener = f"مرحباً فريق {company}،"
        para = (
            f"لاحظنا أن شركات قطاع {vertical['name_ar']} غالباً تواجه: {pain}. "
            f"مع {trigger}، يصبح هذا أكثر إلحاحاً. "
            f"في Dealix نبدأ بـ{offer_name}: نحلّل {angle} ونقدّم توصيات عملية — "
            f"بدون أي أتمتة عمياء، وكل خطوة خارجية تبقى بقرارك أنت."
        )
        closer = "هل تناسبك مكالمة قصيرة (٢٠ دقيقة) هذا الأسبوع؟"
    else:
        opener = f"Hello {company} team,"
        para = (
            f"We see {vertical['name']} teams repeatedly hit: {pain}. "
            f"With {trigger}, it gets more urgent. "
            f"Dealix starts with a {offer_name}: we analyze {angle} and hand you practical "
            f"recommendations — no blind automation, and every external step stays your decision."
        )
        closer = "Would a short 20-minute call this week be useful?"
    return f"{opener}\n\n{para}\n\n{closer}"


def _cta(lang: str) -> str:
    return "احجز مكالمة تشخيص قصيرة" if lang == "ar" else "Book a short diagnostic call"


def _opt_out(lang: str) -> str:
    return (
        "للتوقف عن استلام الرسائل، ردّ بكلمة (إيقاف)."
        if lang == "ar"
        else "Reply STOP to opt out of further messages."
    )


def _score(seed_str: str, lo: int, hi: int) -> int:
    h = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest(), 16)
    return lo + (h % (hi - lo + 1))


def generate(target: int, day: str, seed: int = 1337) -> list[dict]:
    offers = load_offers()
    verticals = offers["verticals"]
    ladder = {o["stage"]: o for o in offers["offer_ladder"]}
    leads = load_seed_leads()
    rnd = random.Random(seed)  # noqa: S311 — deterministic test data, not cryptographic
    mix = _scale_mix(target)

    batch_id = f"BATCH-{day}"
    drafts: list[dict] = []
    counter = 0
    for channel, count in mix.items():
        for _ in range(count):
            counter += 1
            vertical = rnd.choice(verticals)
            # Map channel to a sensible offer stage emphasis.
            stage = (
                rnd.choice(["audit", "audit", "pilot"])
                if channel != "follow_up"
                else rnd.choice(["audit", "pilot"])
            )
            offer = ladder[stage]
            lang = rnd.choice(offers["languages"])
            angle = rnd.choice(vertical["pain_angles"])
            pain = rnd.choice(vertical["pains_ar"] if lang == "ar" else vertical["pains"])
            trigger = rnd.choice(vertical["triggers"])
            title_list = vertical["buyer_titles_ar"] if lang == "ar" else vertical["buyer_titles"]
            buyer_title = rnd.choice(title_list)
            lead = rnd.choice(leads) if leads else None
            company = lead["company_name"] if lead else f"{vertical['name']} prospect"

            draft_id = f"D-{day}-{counter:04d}"
            quality = _score(draft_id + "q", 55, 98)
            compliance = _score(draft_id + "c", 70, 100)
            fit = _score(draft_id + "f", 40, 99)
            priority = round((quality * 0.3 + compliance * 0.2 + fit * 0.5), 2)
            risk = "low" if compliance >= 85 else ("medium" if compliance >= 75 else "high")

            draft = {
                "draft_id": draft_id,
                "batch_id": batch_id,
                "created_at": now_iso(),
                "company_name": company,
                "source_lead_id": lead["lead_id"] if lead else None,
                "vertical": vertical["id"],
                "country": vertical["country"],
                "city": rnd.choice(vertical["cities"]),
                "channel": channel,
                "language": lang,
                "buyer_persona": f"{vertical['name']} decision maker",
                "buyer_title": buyer_title,
                "offer_stage": stage,
                "offer_name": offer["name"],
                "pain_angle": angle,
                "trigger_event": trigger,
                "subject": _subject(channel, lang, vertical, offer, angle),
                "body": _body(channel, lang, vertical, offer, angle, pain, trigger, company),
                "cta": _cta(lang),
                "opt_out": _opt_out(lang),
                "quality_score": quality,
                "compliance_score": compliance,
                "fit_score": fit,
                "priority_score": priority,
                "risk_level": risk,
                "research_required": fit < 55,
                "founder_notes": "",
                "rejection_reason": "",
                "status": "draft_generated",
                **SAFETY_FLAGS,
            }
            drafts.append(draft)
    return drafts


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate founder-review-only outreach drafts.")
    ap.add_argument("--target", type=int, default=400)
    ap.add_argument("--day", default=today_str())
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    if args.target < 400:
        print(f"WARNING: target {args.target} < 400 minimum; using 400.")
        args.target = 400

    drafts = generate(args.target, args.day, args.seed)
    out_dir = output_day_dir(args.day)
    write_jsonl(out_dir / "draft_queue.jsonl", drafts)

    manifest = {
        "batch_id": f"BATCH-{args.day}",
        "generated_at": now_iso(),
        "day": args.day,
        "target": args.target,
        "total_drafts": len(drafts),
        "channel_counts": {c: sum(1 for d in drafts if d["channel"] == c) for c in CHANNEL_MIX},
        "language_counts": {
            lang: sum(1 for d in drafts if d["language"] == lang) for lang in ("ar", "en")
        },
        "non_negotiable_rule": NON_NEGOTIABLE_RULE,
        "safety_flags": SAFETY_FLAGS,
        "external_send": "blocked",
    }
    write_json(out_dir / "batch_manifest.json", manifest)

    print(f"Generated {len(drafts)} drafts -> {out_dir / 'draft_queue.jsonl'}")
    for c in CHANNEL_MIX:
        print(f"  {c}: {manifest['channel_counts'][c]}")
    assert len(drafts) >= 400, "Draft factory must produce at least 400 drafts"
    assert all(d["external_send_blocked"] for d in drafts), "All drafts must block external send"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
