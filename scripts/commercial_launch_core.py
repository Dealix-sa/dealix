"""Dealix Commercial Launch OS — deterministic core library.

Doctrine: AI recommends and drafts. Deterministic workflows verify.
Founder approves. Nothing is sent automatically.

This module is PURE STDLIB on purpose so the Daily Draft Factory and its
tests run with zero third-party dependencies and zero network access. It
NEVER sends anything externally — it only generates review-only drafts and
writes them to the daily output folder for founder review.

Every generated draft carries immutable safety flags:
    send_allowed            = False
    external_send_blocked   = True
    requires_founder_approval = True
    no_auto_send            = True
"""

from __future__ import annotations

import csv
import json
import re
from datetime import date as _date
from pathlib import Path
from typing import Any

# ── Paths ──────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
OUTPUT_ROOT = REPO_ROOT / "outputs" / "commercial_launch"

CONFIG_FILES = {
    "launch": "commercial_launch.json",
    "verticals": "commercial_verticals.json",
    "offers": "commercial_offers.json",
    "channels": "commercial_channels.json",
    "quality": "commercial_quality_gates.json",
    "compliance": "commercial_compliance_gates.json",
    "distribution": "commercial_draft_distribution.json",
}

# Immutable safety flags applied to every draft, every time.
SAFETY_FLAGS = {
    "send_allowed": False,
    "external_send_blocked": True,
    "requires_founder_approval": True,
    "no_auto_send": True,
}

ALLOWED_STATUSES = {
    "founder_review",
    "needs_research",
    "rejected_quality",
    "rejected_compliance",
    "ready_for_manual_copy",
    "archived",
}
FORBIDDEN_STATUSES = {
    "sent",
    "auto_sent",
    "queued_for_send",
    "smtp_ready",
    "whatsapp_ready",
    "linkedin_auto_ready",
}
IN_QUEUE_STATUSES = {"founder_review", "needs_research", "ready_for_manual_copy"}

DRAFT_FIELDS = [
    "draft_id", "batch_id", "created_at", "company_name", "source_lead_id",
    "vertical", "country", "city", "channel", "language", "buyer_persona",
    "buyer_title", "offer_stage", "offer_name", "pain_angle", "trigger_event",
    "subject", "body", "cta", "opt_out", "quality_score", "compliance_score",
    "risk_level", "research_required", "founder_notes", "rejection_reason",
    "status", "send_allowed", "external_send_blocked",
    "requires_founder_approval", "no_auto_send",
]


# ── Config / data loading ──────────────────────────────────────────────────
def load_config(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / CONFIG_FILES[name]
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_all_configs() -> dict[str, Any]:
    return {key: load_config(key) for key in CONFIG_FILES}


def load_seed_leads(path: Path | str | None = None) -> list[dict[str, Any]]:
    """Load seed leads from a JSONL file. Missing file → empty list (case 1)."""
    if path is None:
        path = REPO_ROOT / load_config("launch")["seed_leads_path"]
    path = Path(path)
    leads: list[dict[str, Any]] = []
    if not path.exists():
        return leads
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            leads.append(json.loads(line))
    return leads


def today_str(d: _date | None = None) -> str:
    return (d or _date.today()).isoformat()


def output_dir_for(date_str: str) -> Path:
    return OUTPUT_ROOT / date_str


# ── Helpers ────────────────────────────────────────────────────────────────
def _word_count(*parts: str) -> int:
    return len([w for w in re.split(r"\s+", " ".join(parts).strip()) if w])


def _question_count(text: str) -> int:
    return text.count("?") + text.count("؟")


def _vertical_by_id(configs: dict, vid: str) -> dict:
    for v in configs["verticals"]["verticals"]:
        if v["id"] == vid:
            return v
    return configs["verticals"]["verticals"][0]


def _offer_by_stage(configs: dict, stage: str) -> dict:
    for o in configs["offers"]["ladder"]:
        if o["stage"] == stage:
            return o
    return configs["offers"]["ladder"][0]


# ── Message composition (compliant by construction) ────────────────────────
def _compose(channel: str, language: str, ctx: dict) -> dict[str, str]:
    """Return {subject, body, cta, opt_out} for a channel/language.

    Bodies intentionally contain ZERO question marks; the single CTA (the
    only question) lives in the `cta` field so each draft has exactly one CTA.
    """
    company = ctx["company"]
    title = ctx["title"]
    vname = ctx["vertical_name"]
    pain = ctx["pain"]
    offer = ctx["offer_name"]
    deliverable = ctx["deliverable"]

    if language == "ar":
        approval = "تحت إشرافكم الكامل — الذكاء يقترح ويصيغ، وأنتم من يقرر، وبياناتكم تبقى لديكم"
        opt_out = "للتوقف عن استقبال رسائلنا، ردوا بكلمة (إيقاف)."
        if channel == "cold_email":
            return {
                "subject": f"{vname}: معالجة {pain}",
                "body": (
                    f"مرحبًا {title} في {company}. نساعد جهات {vname} على معالجة "
                    f"{pain} عبر نظام تشغيل بالذكاء الاصطناعي يعمل {approval}. "
                    f"نبدأ عادةً بـ{offer}: {deliverable} خلال أيام."
                ),
                "cta": "هل تناسبكم مكالمة قصيرة 15 دقيقة هذا الأسبوع لمراجعة سير عملكم",
                "opt_out": opt_out,
            }
        if channel == "follow_up":
            return {
                "subject": f"متابعة — {vname} و{pain}",
                "body": (
                    f"{title} الكريم في {company}، أتابع رسالتي السابقة. مازلنا "
                    f"نرى أن معالجة {pain} ممكنة عبر نظام يعمل {approval}، بدءًا بـ{offer}."
                ),
                "cta": "هل أرسل لكم نبذة قصيرة من صفحة واحدة لمراجعتها",
                "opt_out": opt_out,
            }
        if channel == "linkedin":
            return {
                "subject": "",
                "body": (
                    f"{title} في {company}، نبني أنظمة تشغيل بالذكاء الاصطناعي لقطاع "
                    f"{vname} تعالج {pain}، {approval}. بدأنا مع جهات مشابهة عبر {offer}."
                ),
                "cta": "هل أشارك نبذة قصيرة عن طريقة العمل",
                "opt_out": "",
            }
        # website_form
        return {
            "subject": "",
            "body": (
                f"نمثل Dealix، نظام تشغيل تجاري بالذكاء الاصطناعي. نساعد جهات {vname} "
                f"على معالجة {pain} {approval}، بدءًا بـ{offer}."
            ),
            "cta": "يسعدنا ترتيب مكالمة قصيرة لمراجعة سير عملكم",
            "opt_out": "",
        }

    # English
    approval = (
        "fully under your control — the AI recommends and drafts, you decide, "
        "and your data stays with you"
    )
    opt_out = "Reply STOP to opt out of further messages."
    if channel == "cold_email":
        return {
            "subject": f"{vname}: tackling {pain}",
            "body": (
                f"Hi {title} at {company}. We help {vname} teams tackle {pain} with "
                f"an AI operations system that runs {approval}. We usually start with "
                f"the {offer}: {deliverable} within days."
            ),
            "cta": "Would a short 15-minute call this week to review your workflow work for you",
            "opt_out": opt_out,
        }
    if channel == "follow_up":
        return {
            "subject": f"Following up — {vname} and {pain}",
            "body": (
                f"Hi {title} at {company}, following up on my earlier note. We still see "
                f"a clear path to tackle {pain} with a system that runs {approval}, "
                f"starting with the {offer}."
            ),
            "cta": "Should I send a short one-page brief for your review",
            "opt_out": opt_out,
        }
    if channel == "linkedin":
        return {
            "subject": "",
            "body": (
                f"{title} at {company} — we build AI operations systems for {vname} that "
                f"tackle {pain}, {approval}. We have started with similar teams via the {offer}."
            ),
            "cta": "Happy to share a short overview of how it works",
            "opt_out": "",
        }
    # website_form
    return {
        "subject": "",
        "body": (
            f"This is Dealix, an AI revenue & operations system. We help {vname} teams "
            f"tackle {pain} {approval}, starting with the {offer}."
        ),
        "cta": "We would welcome a short call to review your workflow",
        "opt_out": "",
    }


# ── Scoring + gates ────────────────────────────────────────────────────────
def score_quality(draft: dict, configs: dict) -> tuple[int, list[str]]:
    rules = configs["quality"]
    reasons: list[str] = []
    score = 100
    text = f"{draft['subject']} {draft['body']} {draft['cta']}".lower()
    channel = draft["channel"]
    sensitive = _vertical_by_id(configs, draft["vertical"]).get("sensitive", False)

    # must mention vertical or pain
    pain = draft["pain_angle"].lower()
    if pain not in draft["body"].lower():
        score -= 40
        reasons.append("missing_pain_or_vertical")
    # single CTA (exactly one question across body+cta)
    qn = _question_count(draft["body"]) + _question_count(draft["cta"])
    if qn != 1:
        score -= 25
        reasons.append("not_single_cta")
    # opt-out where required
    ch_cfg = configs["channels"]["channels"][channel]
    if ch_cfg.get("requires_opt_out") and not draft["opt_out"].strip():
        score -= 25
        reasons.append("missing_opt_out")
    # human approval language for sensitive verticals
    if sensitive:
        markers = ("إشراف", "أنتم من يقرر", "control", "you decide", "approval")
        if not any(m.lower() in text for m in markers):
            score -= 20
            reasons.append("sensitive_missing_human_approval")
    # length limit
    limit = rules["max_words_by_channel"].get(channel, 180)
    if _word_count(draft["body"], draft["cta"]) > limit:
        score -= 20
        reasons.append("overlength")
    # generic agency language
    for phrase in rules["generic_agency_phrases"]:
        if phrase.lower() in text:
            score -= 30
            reasons.append("generic_agency_language")
            break
    # single offer
    offer_hits = sum(
        1 for o in configs["offers"]["ladder"]
        if o["name_en"].split(" — ")[0].lower() in text or o["name_ar"].split(" — ")[0] in draft["body"]
    )
    if offer_hits > 1:
        score -= 20
        reasons.append("multiple_offer")

    return max(0, min(100, score)), reasons


def score_compliance(draft: dict, configs: dict) -> tuple[int, list[str]]:
    cfg = configs["compliance"]
    reasons: list[str] = []
    score = 100
    text = f"{draft['subject']} {draft['body']} {draft['cta']}".lower()
    channel = draft["channel"]

    for phrase in cfg["banned_phrases"]:
        if phrase.lower() in text:
            score -= 50
            reasons.append("banned_phrase")
    ch_cfg = configs["channels"]["channels"][channel]
    if ch_cfg.get("requires_opt_out") and not draft["opt_out"].strip():
        score -= 40
        reasons.append("no_opt_out")
    # sensitive vertical needs privacy-first language
    if draft["vertical"] in cfg["sensitive_verticals"]:
        markers = cfg["privacy_first_markers_en"] + cfg["privacy_first_markers_ar"]
        if not any(m.lower() in text or m in draft["body"] for m in markers):
            score -= 30
            reasons.append("sensitive_no_privacy_language")
    # multiple CTA
    qn = _question_count(draft["body"]) + _question_count(draft["cta"])
    if qn > 1:
        score -= 25
        reasons.append("multiple_cta")
    # whatsapp needs opt-in (only if a whatsapp draft is ever produced)
    if channel == "whatsapp" and draft.get("research_required"):
        score -= 30
        reasons.append("whatsapp_no_optin")

    return max(0, min(100, score)), reasons


def quality_gate(draft: dict, configs: dict) -> tuple[bool, int, list[str]]:
    score, reasons = score_quality(draft, configs)
    passed = score >= configs["quality"]["min_quality_score"] and not reasons
    return passed, score, reasons


def compliance_gate(draft: dict, configs: dict) -> tuple[bool, int, list[str]]:
    score, reasons = score_compliance(draft, configs)
    passed = score >= configs["compliance"]["min_compliance_score"] and not reasons
    return passed, score, reasons


def finalize_draft(draft: dict, configs: dict) -> dict:
    """Score, gate, set status / risk / notes, and lock safety flags."""
    q_pass, q_score, q_reasons = quality_gate(draft, configs)
    c_pass, c_score, c_reasons = compliance_gate(draft, configs)
    draft["quality_score"] = q_score
    draft["compliance_score"] = c_score

    sensitive = _vertical_by_id(configs, draft["vertical"]).get("sensitive", False)

    if not c_pass:
        draft["status"] = "rejected_compliance"
        draft["rejection_reason"] = ";".join(c_reasons) or "compliance_below_threshold"
        draft["risk_level"] = "high"
    elif not q_pass:
        draft["status"] = "rejected_quality"
        draft["rejection_reason"] = ";".join(q_reasons) or "quality_below_threshold"
        draft["risk_level"] = "high"
    elif draft["research_required"]:
        draft["status"] = "needs_research"
        draft["rejection_reason"] = ""
        draft["risk_level"] = "medium"
    elif draft.get("_consent") == "opt_in" and q_score >= 90 and c_score >= 90:
        draft["status"] = "ready_for_manual_copy"
        draft["rejection_reason"] = ""
        draft["risk_level"] = "medium" if sensitive else "low"
    else:
        draft["status"] = "founder_review"
        draft["rejection_reason"] = ""
        draft["risk_level"] = "medium" if sensitive else "low"

    # Founder notes
    notes = []
    if draft["research_required"]:
        notes.append("Verify company + public contact before any manual send.")
    if sensitive:
        notes.append("Sensitive sector: keep privacy-first, human-in-the-loop language.")
    if draft["status"].startswith("rejected"):
        notes.append("Rejected by gate — do not send; fix or archive.")
    if draft["status"] == "ready_for_manual_copy":
        notes.append("Founder approval still required before any manual copy/send.")
    draft["founder_notes"] = " ".join(notes) or "Founder review required."

    draft.pop("_consent", None)
    draft.update(SAFETY_FLAGS)
    return draft


# ── Draft building ─────────────────────────────────────────────────────────
def _distribution_for(target: int, configs: dict) -> dict[str, int]:
    base = configs["distribution"]["distribution"]
    base_total = sum(base.values())
    if target == base_total:
        return dict(base)
    counts: dict[str, int] = {}
    for ch, n in base.items():
        counts[ch] = round(n * target / base_total)
    diff = target - sum(counts.values())
    counts["cold_email"] += diff  # absorb rounding remainder
    return counts


def _placeholder_lead(idx: int, vertical_id: str, configs: dict) -> dict:
    v = _vertical_by_id(configs, vertical_id)
    return {
        "lead_id": f"PH-{idx:05d}",
        "company_name": f"[Prospect] {v['name_en']} #{idx:03d}",
        "country": "SA",
        "city": "Riyadh",
        "vertical_hint": vertical_id,
        "language_hint": "ar" if idx % 20 < 11 else "en",
        "buyer_title_hint": "",
        "consent_status": "none",
        "source": "placeholder",
        "_placeholder": True,
    }


def build_primary_drafts(target: int, leads: list[dict], configs: dict, date_str: str,
                         batch_id: str) -> list[dict]:
    verticals = configs["verticals"]["verticals"]
    counts = _distribution_for(target, configs)
    drafts: list[dict] = []
    seq = 0

    for channel, n in counts.items():
        ch_cfg = configs["channels"]["channels"][channel]
        for _ in range(n):
            vertical = verticals[seq % len(verticals)]
            vid = vertical["id"]
            # use a real lead if available, else placeholder
            if seq < len(leads):
                lead = leads[seq]
                vid = lead.get("vertical_hint") or vid
                vertical = _vertical_by_id(configs, vid)
            else:
                lead = _placeholder_lead(seq, vid, configs)

            language = lead.get("language_hint") or ("ar" if seq % 20 < 11 else "en")
            consent = lead.get("consent_status", "none")
            research_required = bool(lead.get("_placeholder")) or consent != "opt_in"

            titles = vertical[f"buyer_titles_{language}"]
            title = lead.get("buyer_title_hint") or titles[seq % len(titles)]
            pains = vertical[f"pain_angles_{language}"]
            pain = pains[seq % len(pains)]
            triggers = vertical[f"trigger_events_{language}"]
            trigger = triggers[seq % len(triggers)]

            offer_stage = "paid_pilot" if seq % 11 == 0 else vertical["default_offer_stage"]
            offer = _offer_by_stage(configs, offer_stage)
            offer_name = offer[f"name_{language}"].split(" — ")[0]
            deliverable = offer[f"deliverable_{language}"]
            vname = vertical[f"name_{language}"]

            msg = _compose(channel, language, {
                "company": lead["company_name"], "title": title,
                "vertical_name": vname, "pain": pain,
                "offer_name": offer_name, "deliverable": deliverable,
            })
            # The single CTA must be the only question in the draft.
            mark = "؟" if language == "ar" else "?"
            if msg["cta"] and not msg["cta"].rstrip().endswith(mark):
                msg["cta"] = msg["cta"].rstrip() + mark

            seq += 1
            draft = {
                "draft_id": f"{batch_id}-{seq:05d}",
                "batch_id": batch_id,
                "created_at": date_str,
                "company_name": lead["company_name"],
                "source_lead_id": lead.get("lead_id", ""),
                "vertical": vid,
                "country": lead.get("country", "SA"),
                "city": lead.get("city", ""),
                "channel": channel,
                "language": language,
                "buyer_persona": f"{vname} decision maker",
                "buyer_title": title,
                "offer_stage": offer_stage,
                "offer_name": offer_name,
                "pain_angle": pain,
                "trigger_event": trigger,
                "subject": msg["subject"],
                "body": msg["body"],
                "cta": msg["cta"],
                "opt_out": msg["opt_out"],
                "quality_score": 0,
                "compliance_score": 0,
                "risk_level": "medium",
                "research_required": research_required,
                "founder_notes": "",
                "rejection_reason": "",
                "status": "founder_review",
                "_consent": consent,
            }
            drafts.append(finalize_draft(draft, configs))
    return drafts


def build_stress_drafts(configs: dict, date_str: str, batch_id: str) -> list[dict]:
    """A small fixed set of intentionally non-compliant / low-quality drafts so
    the quality and compliance gates are always exercised and the rejected
    buckets are never empty. Every one still carries the safety flags."""
    verticals = configs["verticals"]["verticals"]
    samples = [
        # (channel, language, body, cta, opt_out) crafted to trip a gate
        ("cold_email", "en", "Hi team, we guarantee 100% results and can replace your team with no human needed.", "Book now", "Reply STOP to opt out."),
        ("cold_email", "en", "As discussed, we found your data from our database and want to talk.", "Call us?", "Reply STOP to opt out."),
        ("cold_email", "ar", "نضمن لكم نتائج 100% ونستبدل فريقكم بالكامل.", "اتصلوا الآن", "للتوقف ردوا (إيقاف)."),
        ("cold_email", "en", "We do everything, best-in-class solutions, synergy and cutting-edge solutions.", "Reply?", "Reply STOP to opt out."),
        ("cold_email", "en", "Hi, quick generic note with no opt out and two questions? Want a call?", "Want a call?", ""),
        ("linkedin", "en", "We automate everything and no human needed in your firm.", "Connect?", ""),
    ]
    drafts = []
    for i, (channel, language, body, cta, opt_out) in enumerate(samples, start=1):
        vertical = verticals[i % len(verticals)]
        draft = {
            "draft_id": f"{batch_id}-STRESS-{i:03d}",
            "batch_id": batch_id,
            "created_at": date_str,
            "company_name": f"[Stress Test] Sample #{i}",
            "source_lead_id": "",
            "vertical": vertical["id"],
            "country": "SA", "city": "Riyadh",
            "channel": channel, "language": language,
            "buyer_persona": "stress-test", "buyer_title": "Manager",
            "offer_stage": "entry_diagnostic",
            "offer_name": "Entry Diagnostic",
            "pain_angle": vertical[f"pain_angles_{language}"][0],
            "trigger_event": vertical[f"trigger_events_{language}"][0],
            "subject": "Stress test", "body": body, "cta": cta, "opt_out": opt_out,
            "quality_score": 0, "compliance_score": 0, "risk_level": "high",
            "research_required": True, "founder_notes": "", "rejection_reason": "",
            "status": "founder_review", "_consent": "none",
        }
        drafts.append(finalize_draft(draft, configs))
    return drafts


def generate_drafts(target: int = 400, leads: list[dict] | None = None,
                    configs: dict | None = None, date_str: str | None = None) -> list[dict]:
    configs = configs or load_all_configs()
    if leads is None:
        leads = load_seed_leads()
    date_str = date_str or today_str()
    batch_id = f"DLX-{date_str.replace('-', '')}"
    primary = build_primary_drafts(target, leads, configs, date_str, batch_id)
    stress = build_stress_drafts(configs, date_str, batch_id)
    return primary + stress


# ── Output writers ─────────────────────────────────────────────────────────
def _ordered(draft: dict) -> dict:
    return {k: draft.get(k) for k in DRAFT_FIELDS}


def write_outputs(drafts: list[dict], configs: dict, date_str: str) -> Path:
    out = output_dir_for(date_str)
    out.mkdir(parents=True, exist_ok=True)

    accepted = [d for d in drafts if d["status"] in IN_QUEUE_STATUSES]
    rejected = [d for d in drafts if d["status"].startswith("rejected")]
    needs_research = [d for d in drafts if d["status"] == "needs_research"]

    # draft_queue.jsonl (everything)
    with (out / "draft_queue.jsonl").open("w", encoding="utf-8") as fh:
        for d in drafts:
            fh.write(json.dumps(_ordered(d), ensure_ascii=False) + "\n")

    # rejected / needs_research
    with (out / "rejected_drafts.jsonl").open("w", encoding="utf-8") as fh:
        for d in rejected:
            fh.write(json.dumps(_ordered(d), ensure_ascii=False) + "\n")
    with (out / "needs_research.jsonl").open("w", encoding="utf-8") as fh:
        for d in needs_research:
            fh.write(json.dumps(_ordered(d), ensure_ascii=False) + "\n")

    # founder_review.csv
    with (out / "founder_review.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["rank", "draft_id", "company_name", "vertical", "channel",
                         "language", "buyer_title", "offer_name", "status",
                         "risk_level", "quality_score", "compliance_score", "pain_angle"])
        for i, d in enumerate(_rank(accepted), start=1):
            writer.writerow([i, d["draft_id"], d["company_name"], d["vertical"],
                             d["channel"], d["language"], d["buyer_title"],
                             d["offer_name"], d["status"], d["risk_level"],
                             d["quality_score"], d["compliance_score"], d["pain_angle"]])

    metrics = compute_metrics(drafts)
    _write_json(out / "daily_metrics.json", metrics)
    _write_json(out / "quality_report.json", _gate_report(drafts, "quality"))
    _write_json(out / "compliance_report.json", _gate_report(drafts, "compliance"))
    _write_json(out / "batch_manifest.json", {
        "date": date_str,
        "batch_id": drafts[0]["batch_id"] if drafts else "",
        "total_drafts": len(drafts),
        "distribution": _distribution_for(metrics["drafts_generated"] - len_stress(drafts), configs)
        if drafts else {},
        "channels": _count_by(drafts, "channel"),
        "verticals": _count_by(drafts, "vertical"),
        "languages": _count_by(drafts, "language"),
        "doctrine": configs["launch"]["doctrine"],
        "safety_flags": SAFETY_FLAGS,
    })

    write_founder_review_md(drafts, configs, date_str, out)
    write_top_50(drafts, date_str, out)
    write_next_actions(drafts, configs, date_str, out)
    return out


def len_stress(drafts: list[dict]) -> int:
    return sum(1 for d in drafts if "STRESS" in d["draft_id"])


def _write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def _count_by(drafts: list[dict], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for d in drafts:
        out[d[key]] = out.get(d[key], 0) + 1
    return out


def _rank(drafts: list[dict]) -> list[dict]:
    risk_order = {"low": 0, "medium": 1, "high": 2}
    return sorted(
        drafts,
        key=lambda d: (
            0 if d["status"] == "ready_for_manual_copy" else
            1 if d["status"] == "founder_review" else 2,
            risk_order.get(d["risk_level"], 1),
            -d["quality_score"],
            -d["compliance_score"],
        ),
    )


def compute_metrics(drafts: list[dict]) -> dict[str, Any]:
    return {
        "drafts_generated": len(drafts),
        "founder_review_count": sum(1 for d in drafts if d["status"] in IN_QUEUE_STATUSES),
        "ready_for_manual_copy": sum(1 for d in drafts if d["status"] == "ready_for_manual_copy"),
        "founder_review": sum(1 for d in drafts if d["status"] == "founder_review"),
        "needs_research": sum(1 for d in drafts if d["status"] == "needs_research"),
        "rejected_quality": sum(1 for d in drafts if d["status"] == "rejected_quality"),
        "rejected_compliance": sum(1 for d in drafts if d["status"] == "rejected_compliance"),
        "by_channel": _count_by(drafts, "channel"),
        "by_vertical": _count_by(drafts, "vertical"),
        "by_language": _count_by(drafts, "language"),
        "by_risk": _count_by(drafts, "risk_level"),
        "all_send_blocked": all(d["external_send_blocked"] for d in drafts),
        "all_send_disallowed": all(not d["send_allowed"] for d in drafts),
    }


def _gate_report(drafts: list[dict], gate: str) -> dict[str, Any]:
    field = f"{gate}_score"
    status = f"rejected_{gate}"
    rejected = [d for d in drafts if d["status"] == status]
    scores = [d[field] for d in drafts]
    reasons: dict[str, int] = {}
    for d in rejected:
        for r in (d["rejection_reason"] or "").split(";"):
            if r:
                reasons[r] = reasons.get(r, 0) + 1
    return {
        "gate": gate,
        "total": len(drafts),
        "rejected": len(rejected),
        "passed": len(drafts) - len(rejected),
        "min_score": min(scores) if scores else 0,
        "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "rejection_reasons": reasons,
    }


def write_founder_review_md(drafts: list[dict], configs: dict, date_str: str, out: Path) -> None:
    m = compute_metrics(drafts)
    ranked = _rank([d for d in drafts if d["status"] in IN_QUEUE_STATUSES])
    top50 = ranked[:50]
    high_value = [d for d in ranked if d["offer_stage"] != "entry_diagnostic"][:10] or ranked[:10]
    risk_items = [d for d in drafts if d["risk_level"] == "high"][:10]
    research = [d for d in drafts if d["status"] == "needs_research"]
    rej_reasons = {}
    for d in drafts:
        if d["status"].startswith("rejected"):
            for r in (d["rejection_reason"] or "").split(";"):
                if r:
                    rej_reasons[r] = rej_reasons.get(r, 0) + 1

    L = []
    L.append(f"# Dealix — Founder Review ({date_str})\n")
    L.append("> **Review-only.** This system does not send external messages. "
             "AI recommends and drafts. Founder approves. Nothing is sent automatically.\n")
    L.append("## Executive summary\n")
    L.append(f"- Total drafts generated: **{m['drafts_generated']}**")
    L.append(f"- Accepted into founder review queue: **{m['founder_review_count']}**")
    L.append(f"- Ready for manual copy: **{m['ready_for_manual_copy']}**")
    L.append(f"- Needs research: **{m['needs_research']}**")
    L.append(f"- Rejected (quality): **{m['rejected_quality']}** | Rejected (compliance): **{m['rejected_compliance']}**")
    L.append(f"- Safety: all external send blocked = **{m['all_send_blocked']}**, all send disallowed = **{m['all_send_disallowed']}**\n")

    L.append("## Channel distribution\n")
    for k, v in m["by_channel"].items():
        L.append(f"- {k}: {v}")
    L.append("\n## Vertical distribution\n")
    for k, v in m["by_vertical"].items():
        L.append(f"- {k}: {v}")
    L.append("\n## Language distribution\n")
    for k, v in m["by_language"].items():
        L.append(f"- {k}: {v}")

    L.append("\n## Top 50 priority drafts\n")
    L.append("| # | Company | Vertical | Channel | Lang | Title | Offer | Status | Risk | Q | C |")
    L.append("|---|---------|----------|---------|------|-------|-------|--------|------|---|---|")
    for i, d in enumerate(top50, 1):
        L.append(f"| {i} | {d['company_name']} | {d['vertical']} | {d['channel']} | "
                 f"{d['language']} | {d['buyer_title']} | {d['offer_name']} | {d['status']} | "
                 f"{d['risk_level']} | {d['quality_score']} | {d['compliance_score']} |")

    L.append("\n## Top 10 highest-value opportunities\n")
    for i, d in enumerate(high_value, 1):
        L.append(f"{i}. {d['company_name']} — {d['offer_name']} ({d['vertical']}, {d['channel']})")

    L.append("\n## Top 10 risk items\n")
    if risk_items:
        for i, d in enumerate(risk_items, 1):
            L.append(f"{i}. {d['company_name']} — {d['status']} — {d['rejection_reason'] or d['risk_level']}")
    else:
        L.append("- None flagged high risk.")

    L.append(f"\n## Drafts requiring research: {len(research)}\n")
    for d in research[:15]:
        L.append(f"- {d['company_name']} ({d['vertical']}, {d['channel']}) — verify before any manual send")

    L.append("\n## Rejection reasons\n")
    if rej_reasons:
        for k, v in sorted(rej_reasons.items(), key=lambda x: -x[1]):
            L.append(f"- {k}: {v}")
    else:
        L.append("- None.")

    L.append("\n## Manual actions for founder\n")
    L.append("1. Review the Top 50 table above; pick only 20–50 to act on.")
    L.append("2. Manually copy approved drafts; never use automation.")
    L.append("3. Verify every `needs_research` draft before any contact.")
    L.append("4. Update the suppression list and log every reply.")

    L.append("\n## Today's recommended focus\n")
    top_verts = sorted(m["by_vertical"].items(), key=lambda x: -x[1])[:3]
    L.append("- Focus verticals: " + ", ".join(f"{k} ({v})" for k, v in top_verts))

    L.append("\n## Go / No-Go by channel\n")
    for ch, cfg in configs["channels"]["channels"].items():
        L.append(f"- {ch}: GO for **draft only**; NO-GO for automated/bulk sending.")

    (out / "founder_review.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_top_50(drafts: list[dict], date_str: str, out: Path) -> None:
    ranked = _rank([d for d in drafts if d["status"] in IN_QUEUE_STATUSES])[:50]
    L = [f"# Top 50 Priority — {date_str}\n",
         "> Review-only. Founder approves. Nothing is sent automatically.\n"]
    for i, d in enumerate(ranked, 1):
        manual = ("Copy & send manually after approval" if d["status"] == "ready_for_manual_copy"
                  else "Research, then founder review" if d["status"] == "needs_research"
                  else "Founder review, then manual copy")
        preview = (d["body"][:160] + "…") if len(d["body"]) > 160 else d["body"]
        L.append(f"## {i}. {d['company_name']}")
        L.append(f"- Vertical: {d['vertical']}")
        L.append(f"- Buyer title: {d['buyer_title']}")
        L.append(f"- Channel: {d['channel']} | Language: {d['language']}")
        L.append(f"- Pain angle: {d['pain_angle']}")
        L.append(f"- Offer: {d['offer_name']} ({d['offer_stage']})")
        L.append(f"- Rationale: fit on {d['vertical']} pain '{d['pain_angle']}' via {d['channel']}.")
        L.append(f"- Risk level: {d['risk_level']}")
        L.append(f"- Manual action: {manual}")
        L.append(f"- Draft preview: {preview}\n")
    (out / "top_50_priority.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_next_actions(drafts: list[dict], configs: dict, date_str: str, out: Path) -> None:
    m = compute_metrics(drafts)
    ranked = _rank([d for d in drafts if d["status"] in IN_QUEUE_STATUSES])
    top_verts = sorted(m["by_vertical"].items(), key=lambda x: -x[1])[:3]
    top_companies = ranked[:10]
    L = [f"# Next Actions — {date_str}\n",
         "> Review-only. No external sending occurs in this repository.\n",
         "## Review first\n",
         "- Open `founder_review.md` and `top_50_priority.md`.",
         "- Pick only the 20–50 highest-quality drafts to act on today.\n",
         "## Send manually (after approval)\n",
         "- Copy approved drafts by hand. No mail server, no automation, no bulk send.\n",
         "## Defer\n",
         "- Anything below the top 50 or with weak fit.\n",
         "## Needs research\n",
         f"- {m['needs_research']} drafts require company/contact verification before any contact.\n",
         "## Do not touch\n",
         "- Any `rejected_quality` / `rejected_compliance` draft. Fix or archive.\n",
         "## Best 3 verticals today\n"]
    for k, v in top_verts:
        L.append(f"- {k} ({v} drafts)")
    L.append("\n## Best 10 companies today\n")
    for i, d in enumerate(top_companies, 1):
        L.append(f"{i}. {d['company_name']} — {d['vertical']} — {d['channel']}")
    L.append("\n## Suggested message of the day\n")
    if top_companies:
        d = top_companies[0]
        L.append(f"> {d['body']}\n>\n> CTA: {d['cta']}")
    (out / "next_actions.md").write_text("\n".join(L) + "\n", encoding="utf-8")
