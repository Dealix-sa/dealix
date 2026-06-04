#!/usr/bin/env python3
"""Dealix 400+ Daily Draft Factory.

Generates at least 400 review-only outreach drafts per day across four manual
channels (cold email, follow-up, LinkedIn manual, website/contact form), scores
and gates them, and writes the founder review queue plus reports.

GOVERNING RULE (enforced on every draft):
    AI drafts, ranks, and recommends.
    Founder reviews, approves, and sends manually.
    The system never sends externally.

Every draft carries the mandatory safety flags:
    send_allowed = False
    external_send_blocked = True
    requires_founder_approval = True
    no_auto_send = True

This script NEVER sends anything. It only writes local artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    DATA_DIR,
    GOVERNING_RULE,
    MANDATORY_SAFETY_FLAGS,
    load_config,
    read_jsonl,
    today_str,
    write_csv,
    write_json,
    write_jsonl,
    write_text,
)
from commercial_compliance_gate import evaluate_compliance
from commercial_quality_gate import evaluate_quality
from commercial_score_drafts import score_draft

OPT_OUT_EN = "If this isn't relevant, reply 'unsubscribe' and you won't hear from me again."
OPT_OUT_AR = "إن لم يكن هذا مناسبًا، الرجاء الرد بكلمة (إلغاء) ولن نعاود التواصل."


def _cta_for_stage(offer: dict[str, Any], lang: str) -> str:
    stage = offer.get("stage")
    table = {
        "audit": ("Request an AI Workflow Audit", "اطلب تدقيق سير العمل بالذكاء الاصطناعي"),
        "pilot": ("Start a Paid Pilot", "ابدأ تجربة مدفوعة"),
        "department_os": ("Book a Diagnostic", "احجز جلسة تشخيص"),
        "retainer": ("Book a Diagnostic", "احجز جلسة تشخيص"),
        "enterprise": ("Book a Diagnostic", "احجز جلسة تشخيص"),
    }
    en, ar = table.get(stage, ("Book a Diagnostic", "احجز جلسة تشخيص"))
    return ar if lang == "ar" else en


def _price_label(offer: dict[str, Any]) -> str:
    lo, hi = offer.get("price_min"), offer.get("price_max")
    if hi is None:
        return f"{lo:,}+ SAR"
    return f"{lo:,}–{hi:,} SAR"


def _build_email(lead, vert, offer, pain, lang, channel) -> tuple[str, str]:
    company = lead["company_name"]
    city = lead["city"]
    cta = _cta_for_stage(offer, lang)
    price = _price_label(offer)
    is_follow = channel == "follow_up"
    if lang == "ar":
        vname = vert["name_ar"]
        pang = pain["ar"]
        oname = offer["name_ar"]
        opener = (
            f"أتابع رسالتي السابقة إلى {company} في {city}."
            if is_follow
            else f"أتواصل مع {company} في {city}."
        )
        subject = f"متابعة: {pang} في {company}" if is_follow else f"{pang} في {company}؟"
        body = (
            f"مرحبًا فريق {company}،\n\n"
            f"{opener} فرق {vname} غالبًا ما تفقد وقتًا في {pang}. "
            f"ديليكس هو نظام تشغيل للإيرادات والعمليات بالذكاء الاصطناعي يصيغ العمل ويرتّبه حسب الأولوية، "
            f"بينما يراجع فريقكم ويعتمد كل خطوة — ولا يُرسل شيء دون قرار بشري.\n\n"
            f"هل يفيدكم {oname} ({price}) لرسم فرصتين أو ثلاث فرص سريعة في عملياتكم؟ "
            f"نحترم خصوصية بياناتكم ولا نعالجها قبل اتفاق واضح.\n\n"
            f"{cta}\n\n"
            f"{OPT_OUT_AR}\n— فريق ديليكس"
        )
    else:
        vname = vert["name_en"]
        pang = pain["en"]
        oname = offer["name_en"]
        opener = (
            f"Following up on my earlier note to {company} in {city}."
            if is_follow
            else f"I'm reaching out to {company} in {city}."
        )
        subject = f"Re: {pang} at {company}" if is_follow else f"{pang} at {company}?"
        body = (
            f"Hi {company} team,\n\n"
            f"{opener} {vname} teams here often lose hours on {pang}. "
            f"Dealix is an AI revenue & operations OS that drafts and ranks the work while your team "
            f"reviews and approves every step — nothing goes out without a human.\n\n"
            f"Would a short {oname} ({price}) help us map two or three quick wins for your operations? "
            f"We keep your data private and never process it before a clear agreement.\n\n"
            f"{cta}\n\n"
            f"{OPT_OUT_EN}\n— The Dealix team"
        )
    return subject, body


def _build_linkedin(lead, vert, offer, pain, lang) -> tuple[str, str]:
    company = lead["company_name"]
    cta = _cta_for_stage(offer, lang)
    if lang == "ar":
        pang = pain["ar"]
        subject = f"رسالة لينكدإن — {company}"
        body = (
            f"مرحبًا، لاحظت عمل {company} في {lead['city']}. "
            f"كثير من فرق {vert['name_ar']} تتعامل مع {pang}. "
            f"في ديليكس نصيغ ونرتّب العمل بالذكاء الاصطناعي، ويبقى الاعتماد والإرسال بيد فريقكم دائمًا. "
            f"{cta}؟ (هذه مسودة يدوية للمراجعة — لا أتمتة على لينكدإن.)"
        )
    else:
        pang = pain["en"]
        subject = f"LinkedIn note — {company}"
        body = (
            f"Hi — saw the work {company} is doing in {lead['city']}. "
            f"Many {vert['name_en']} teams wrestle with {pang}. "
            f"Dealix drafts and ranks the work with AI while your team keeps approval and sending. "
            f"Open to a quick chat? {cta}. (Manual draft for review — no LinkedIn automation.)"
        )
    return subject, body


def _build_contact_form(lead, vert, offer, pain, lang) -> tuple[str, str]:
    company = lead["company_name"]
    cta = _cta_for_stage(offer, lang)
    if lang == "ar":
        pang = pain["ar"]
        subject = f"نقاط نموذج التواصل — {company}"
        body = (
            f"ملاحظات يدوية للمؤسس قبل ملء نموذج التواصل الخاص بـ {company}:\n"
            f"- القطاع: {vert['name_ar']} في {lead['city']}.\n"
            f"- الزاوية: {pang}.\n"
            f"- العرض المقترح: {offer['name_ar']} ({_price_label(offer)}).\n"
            f"- الدعوة: {cta}.\n"
            f"ملاحظة: لا إرسال تلقائي للنماذج — يقوم المؤسس بالتعبئة يدويًا."
        )
    else:
        pang = pain["en"]
        subject = f"Contact-form talking points — {company}"
        body = (
            f"Manual talking points for the founder before filling {company}'s contact form:\n"
            f"- Vertical: {vert['name_en']} in {lead['city']}.\n"
            f"- Angle: {pang}.\n"
            f"- Suggested offer: {offer['name_en']} ({_price_label(offer)}).\n"
            f"- CTA: {cta}.\n"
            f"Note: no form auto-submit — the founder fills this manually."
        )
    return subject, body


def _make_draft(
    seq, batch_id, created_at, lead, vert, offer, pain, lang, channel
) -> dict[str, Any]:
    if channel in ("cold_email", "follow_up"):
        subject, body = _build_email(lead, vert, offer, pain, lang, channel)
        opt_out = OPT_OUT_AR if lang == "ar" else OPT_OUT_EN
    elif channel == "linkedin_manual":
        subject, body = _build_linkedin(lead, vert, offer, pain, lang)
        opt_out = ""
    else:
        subject, body = _build_contact_form(lead, vert, offer, pain, lang)
        opt_out = ""

    # Privacy-sensitive verticals (e.g. legal) must always carry privacy-first language.
    if vert.get("privacy_sensitive"):
        if lang == "ar":
            body += "\n\nنلتزم بحماية الخصوصية ولا نعالج أي بيانات شخصية قبل موافقتك واتفاق مكتوب."
        else:
            body += "\n\nWe are privacy-first: we don't process any personal data before your consent and a written agreement."

    raw_id = f"{batch_id}:{channel}:{seq}:{lead['lead_id']}:{offer['id']}:{lang}"
    draft_id = "drf_" + hashlib.sha1(raw_id.encode()).hexdigest()[:16]  # noqa: S324 - non-crypto id
    cta = _cta_for_stage(offer, lang)

    opt_in = lead.get("opt_in_status", "unknown")
    research_required = opt_in == "unknown"
    triggers = vert.get("triggers", ["general outreach"])
    trigger_event = random.choice(triggers)  # noqa: S311

    draft: dict[str, Any] = {
        "draft_id": draft_id,
        "batch_id": batch_id,
        "created_at": created_at,
        "company_name": lead["company_name"],
        "source_lead_id": lead["lead_id"],
        "vertical": vert["id"],
        "country": lead["country"],
        "city": lead["city"],
        "channel": channel,
        "language": lang,
        "buyer_persona": lead.get("buyer_persona", ""),
        "buyer_title": lead.get("buyer_title", ""),
        "offer_stage": offer["stage"],
        "offer_name": offer["name_en"],
        "pain_angle": pain["en"],
        "trigger_event": trigger_event,
        "subject": subject,
        "body": body,
        "cta": cta,
        "opt_out": opt_out,
        "opt_in_status": opt_in,
        "quality_score": 0,
        "compliance_score": 0,
        "fit_score": 0,
        "priority_score": 0.0,
        "risk_level": "low",
        "research_required": research_required,
        "founder_notes": "",
        "rejection_reason": "",
        "status": "ready_for_founder_review",
        **MANDATORY_SAFETY_FLAGS,
    }
    return draft


def generate(target: int, day: str, seed_path: Path) -> dict[str, Any]:
    rng = random.Random(f"dealix-{day}")  # noqa: S311 - deterministic, non-crypto draft variety
    random.seed(f"dealix-trigger-{day}")

    verticals = load_config("commercial_verticals.json")["verticals"]
    vert_by_id = {v["id"]: v for v in verticals}
    offers = load_config("commercial_offers.json")["offers"]
    offer_by_id = {o["id"]: o for o in offers}
    distribution = load_config("commercial_draft_distribution.json")["distribution"]
    quality_cfg = load_config("commercial_quality_gates.json")
    compliance_cfg = load_config("commercial_compliance_gates.json")
    risk_cfg = load_config("commercial_risk_terms.json")
    weights = load_config("commercial_founder_review_rules.json").get("priority_weights", {})

    leads = read_jsonl(seed_path)
    if not leads:
        raise SystemExit(f"No seed leads found at {seed_path}")

    # Scale distribution up proportionally if a higher target is requested.
    base_total = sum(distribution.values()) or 1
    scale = max(1, -(-target // base_total))  # ceil division
    plan = {ch: count * scale for ch, count in distribution.items()}

    created_at = datetime.now(UTC).isoformat()
    batch_id = f"batch_{day}"
    langs = ["en", "ar"]

    drafts: list[dict[str, Any]] = []
    for channel, count in plan.items():
        for i in range(count):
            lead = leads[(i * 7 + len(drafts)) % len(leads)]
            vert = vert_by_id.get(lead["vertical"], verticals[0])
            offer = offer_by_id.get(vert.get("recommended_offer", "ai_workflow_audit"), offers[0])
            # Mix in a higher-tier offer occasionally for variety.
            if i % 5 == 4:
                offer = rng.choice(offers[:3])
            pain = rng.choice(vert["pain_angles"])
            lang = langs[(i + len(drafts)) % 2]
            draft = _make_draft(i, batch_id, created_at, lead, vert, offer, pain, lang, channel)
            drafts.append(draft)

    # Score + gate every draft.
    for d in drafts:
        q = evaluate_quality(d, quality_cfg)
        c = evaluate_compliance(d, compliance_cfg)
        d["quality_score"] = q["score"]
        d["compliance_score"] = c["score"]
        score_draft(d, risk_cfg, weights)
        reasons = q["reasons"] + c["reasons"]
        if not (q["passed"] and c["passed"]):
            d["status"] = "rejected"
            d["rejection_reason"] = "; ".join(reasons) or "failed_gate"

    return {
        "drafts": drafts,
        "batch_id": batch_id,
        "day": day,
        "plan": plan,
        "leads_used": len(leads),
    }


def _verify_safety(drafts: list[dict[str, Any]]) -> None:
    for d in drafts:
        assert d["send_allowed"] is False, d["draft_id"]
        assert d["external_send_blocked"] is True, d["draft_id"]
        assert d["requires_founder_approval"] is True, d["draft_id"]
        assert d["no_auto_send"] is True, d["draft_id"]


def write_outputs(result: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    drafts = result["drafts"]
    _verify_safety(drafts)
    review_rules = load_config("commercial_founder_review_rules.json")

    approved = [d for d in drafts if d["status"] == "ready_for_founder_review"]
    rejected = [d for d in drafts if d["status"] == "rejected"]
    needs_research = [d for d in drafts if d.get("research_required")]
    ranked = sorted(approved, key=lambda d: d["priority_score"], reverse=True)

    write_jsonl(out_dir / "draft_queue.jsonl", drafts)
    write_jsonl(out_dir / "rejected_drafts.jsonl", rejected)
    write_jsonl(out_dir / "needs_research.jsonl", needs_research)

    # Founder review CSV + MD
    cols = review_rules["review_columns"]
    rows = [[d.get(c, "") for c in cols] for d in ranked]
    write_csv(out_dir / "founder_review.csv", cols, rows)

    md = [
        f"# Founder Review Queue — {result['day']}",
        "",
        f"> {GOVERNING_RULE}",
        "",
        f"- Total drafts: **{len(drafts)}**",
        f"- Ready for review: **{len(approved)}**",
        f"- Rejected by gates: **{len(rejected)}**",
        f"- Needs research: **{len(needs_research)}**",
        "",
        "All drafts are review-only. `send_allowed=false`, `no_auto_send=true`. "
        + "The founder approves and sends manually; the system never sends.",
        "",
        "| # | Priority | Company | Vertical | Channel | Lang | Offer | Subject |",
        "|---|----------|---------|----------|---------|------|-------|---------|",
    ]
    for idx, d in enumerate(ranked[:100], 1):
        subj = d["subject"].replace("|", "/")
        md.append(
            f"| {idx} | {d['priority_score']} | {d['company_name']} | {d['vertical']} | "
            f"{d['channel']} | {d['language']} | {d['offer_name']} | {subj} |"
        )
    write_text(out_dir / "founder_review.md", "\n".join(md) + "\n")

    # Top 50 priority
    top_n = review_rules.get("top_priority_count", 50)
    top = [
        "# Top {} Priority Drafts — {}".format(top_n, result["day"]),
        "",
        f"> {GOVERNING_RULE}",
        "",
    ]
    for idx, d in enumerate(ranked[:top_n], 1):
        top += [
            f"## {idx}. {d['company_name']} — {d['vertical']} ({d['channel']}, {d['language']})",
            f"- Priority: {d['priority_score']} | Fit: {d['fit_score']} | Quality: {d['quality_score']} | Compliance: {d['compliance_score']} | Risk: {d['risk_level']}",
            f"- Offer: {d['offer_name']} | Buyer: {d['buyer_title']}",
            f"- Subject: {d['subject']}",
            "",
            "```",
            d["body"],
            "```",
            "",
        ]
    write_text(out_dir / "top_50_priority.md", "\n".join(top) + "\n")

    # Reports
    by_channel: dict[str, int] = {}
    by_vertical: dict[str, int] = {}
    for d in drafts:
        by_channel[d["channel"]] = by_channel.get(d["channel"], 0) + 1
        by_vertical[d["vertical"]] = by_vertical.get(d["vertical"], 0) + 1

    quality_report = {
        "total": len(drafts),
        "passed": len(approved),
        "failed": len(rejected),
        "avg_quality_score": round(sum(d["quality_score"] for d in drafts) / len(drafts), 2),
        "min_quality_score": min(d["quality_score"] for d in drafts),
    }
    compliance_report = {
        "total": len(drafts),
        "compliant": sum(1 for d in drafts if d["compliance_score"] >= 80),
        "rejections": len(rejected),
        "avg_compliance_score": round(sum(d["compliance_score"] for d in drafts) / len(drafts), 2),
        "forbidden_phrase_hits": sum(
            1 for d in rejected if "forbidden_phrase" in d.get("rejection_reason", "")
        ),
    }
    write_json(out_dir / "quality_report.json", quality_report)
    write_json(out_dir / "compliance_report.json", compliance_report)

    metrics = {
        "date": result["day"],
        "batch_id": result["batch_id"],
        "drafts_generated": len(drafts),
        "ready_for_review": len(approved),
        "rejected": len(rejected),
        "needs_research": len(needs_research),
        "by_channel": by_channel,
        "by_vertical": by_vertical,
        "leads_used": result["leads_used"],
        "target_met": len(drafts) >= 400,
    }
    write_json(out_dir / "daily_metrics.json", metrics)

    manifest = {
        "batch_id": result["batch_id"],
        "date": result["day"],
        "generated_at": datetime.now(UTC).isoformat(),
        "governing_rule": GOVERNING_RULE,
        "distribution_plan": result["plan"],
        "counts": {"total": len(drafts), "by_channel": by_channel},
        "safety_flags": MANDATORY_SAFETY_FLAGS,
        "external_send_blocked": True,
        "files": [
            "draft_queue.jsonl",
            "founder_review.csv",
            "founder_review.md",
            "top_50_priority.md",
            "rejected_drafts.jsonl",
            "needs_research.jsonl",
            "quality_report.json",
            "compliance_report.json",
            "daily_metrics.json",
            "batch_manifest.json",
            "next_actions.md",
            "approved_manual_sends.example.csv",
        ],
    }
    write_json(out_dir / "batch_manifest.json", manifest)

    next_actions = [
        f"# Next Actions — {result['day']}",
        "",
        f"> {GOVERNING_RULE}",
        "",
        "1. Open `founder_review.md` and `top_50_priority.md`.",
        "2. For each draft you approve, copy it and **send manually** from your own inbox/account.",
        "3. Log approved sends in `approved_manual_sends.example.csv` (copy it without `.example`).",
        "4. Review `needs_research.jsonl` — enrich leads before contacting.",
        "5. Move CRM stages manually (no push-send).",
        "",
        "The system did not and will not send any of these. No SMTP, no WhatsApp, "
        + "no LinkedIn automation, no form auto-submit.",
    ]
    write_text(out_dir / "next_actions.md", "\n".join(next_actions) + "\n")

    # Example (blank) manual-send log — founder copies this, removes .example, fills after sending.
    write_csv(
        out_dir / "approved_manual_sends.example.csv",
        ["draft_id", "company_name", "channel", "sent_by_founder", "sent_at", "outcome", "notes"],
        [
            [
                "drf_example",
                "Example Company (synthetic)",
                "cold_email",
                "no",
                "",
                "",
                "Founder fills after manual send",
            ]
        ],
    )

    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate 400+ review-only outreach drafts.")
    parser.add_argument("--target", type=int, default=400)
    parser.add_argument("--date", default=today_str())
    parser.add_argument(
        "--seed-file", default=str(DATA_DIR / "commercial_seed_leads.example.jsonl")
    )
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    result = generate(args.target, args.date, Path(args.seed_file))
    out_dir = Path(args.out) if args.out else COMMERCIAL_OUTPUTS / args.date
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics = write_outputs(result, out_dir)

    print(f"Generated {metrics['drafts_generated']} drafts -> {out_dir}")
    print(
        f"  ready_for_review={metrics['ready_for_review']} rejected={metrics['rejected']} "
        f"needs_research={metrics['needs_research']}"
    )
    print(f"  target_met(>=400)={metrics['target_met']}")
    if metrics["drafts_generated"] < args.target:
        print(f"ERROR: produced fewer than target ({args.target}).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
