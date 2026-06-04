"""Dealix Official Commercial Launch OS — shared core engine.

Deterministic, stdlib-only library used by the commercial_* scripts.

NON-NEGOTIABLE DOCTRINE (enforced in code and tests):
    AI generates and ranks drafts only. Founder reviews and approves.
    No external sending. No SMTP. No WhatsApp cold outreach.
    No LinkedIn automation. No scraping. No secrets. No auto-submit.

Every generated draft carries the mandatory safety flags:
    send_allowed = False
    external_send_blocked = True
    requires_founder_approval = True
    no_auto_send = True
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date as date_cls
from pathlib import Path
from typing import Any

# ── Paths ──────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
OUTPUT_ROOT = REPO_ROOT / "outputs" / "commercial_launch"
SEED_LEADS = REPO_ROOT / "data" / "commercial_seed_leads.example.jsonl"

# CTA detection: a draft must contain exactly one question mark (ASCII or Arabic).
_CTA_MARKERS = ("?", "؟")
_OPT_OUT_MARKERS = (
    "unsubscribe",
    "opt out",
    "opt-out",
    "reply stop",
    "إلغاء الاشتراك",
    "لإيقاف التواصل",
)


# ── Config loading ─────────────────────────────────────────────────────────
def load_config(name: str) -> dict[str, Any]:
    """Load a config/commercial_*.json file by short name (e.g. 'verticals')."""
    path = CONFIG_DIR / f"commercial_{name}.json"
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_all_configs() -> dict[str, dict[str, Any]]:
    return {
        "launch": load_config("launch"),
        "verticals": load_config("verticals"),
        "offers": load_config("offers"),
        "channels": load_config("channels"),
        "quality": load_config("quality_gates"),
        "compliance": load_config("compliance_gates"),
        "distribution": load_config("draft_distribution"),
        "risk": load_config("risk_terms"),
        "founder_rules": load_config("founder_review_rules"),
        "metrics": load_config("metrics"),
    }


MANDATORY_FLAGS = {
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


# ── Lead handling ──────────────────────────────────────────────────────────
def load_seed_leads(path: Path | None = None) -> list[dict[str, Any]]:
    """Load real seed leads from JSONL. Returns [] if file is missing/empty."""
    path = path or SEED_LEADS
    if not path.exists():
        return []
    leads: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        leads.append(json.loads(line))
    return leads


def make_placeholder_lead(verticals: list[dict], idx: int) -> dict[str, Any]:
    """Build a deterministic placeholder lead requiring research (no real PII)."""
    v = verticals[idx % len(verticals)]
    country = (v.get("country_focus") or ["SA"])[0]
    return {
        "lead_id": f"PLACEHOLDER-{idx:04d}",
        "company_name": f"[RESEARCH NEEDED — {v['name_en']} prospect #{idx:04d}]",
        "website": "",
        "country": country,
        "city": "",
        "vertical_hint": v["key"],
        "language_hint": "ar" if idx % 2 == 0 else "en",
        "buyer_title_hint": v["buyer_titles"][idx % len(v["buyer_titles"])],
        "source": "placeholder_generator",
        "source_url": "",
        "public_contact_type": "unknown",
        "consent_status": "none",
        "notes": "Auto-generated placeholder. Founder must research a real, consented public contact.",
        "research_status": "required",
        "risk_notes": "No verified contact. Do not contact until researched and consented.",
        "_placeholder": True,
    }


# ── Body builders (every body is crafted to pass the gates) ────────────────
def _vertical_by_key(verticals: list[dict], key: str) -> dict:
    for v in verticals:
        if v["key"] == key:
            return v
    return verticals[0]


def build_body(
    *,
    channel: str,
    language: str,
    vertical: dict,
    buyer_title: str,
    company: str,
    pain: str,
    angle: str,
    offer_name: str,
    duration: str,
    country: str,
    sensitive: bool,
) -> tuple[str, str]:
    """Return (subject, body). Bodies include: sector context, one pain, exactly
    one CTA, one offer, a human-control line, and an opt-out line."""
    sector_en = vertical["name_en"]
    sector_ar = vertical["name_ar"]
    privacy_en = " It is privacy-first and runs under your approval." if sensitive else ""
    privacy_ar = " النظام يحترم الخصوصية ويعمل باعتمادك." if sensitive else ""

    if language == "ar":
        subject = f"{sector_ar}: {offer_name}"
        if channel == "linkedin_manual":
            body = (
                f"مرحبًا، كثير من فرق {sector_ar} تواجه تحديًا حين {pain}. "
                f"يبني ديالكس سير عمل مُراجَعًا باعتمادك يساعد على {angle}، وفريقك يبقى المتحكم.{privacy_ar} "
                f"هل تفيدك جلسة قصيرة ({offer_name})؟ "
                f'لإيقاف التواصل اكتب "إلغاء الاشتراك".'
            )
        elif channel == "website_form_manual":
            body = (
                f"بخصوص {sector_ar} في {company}: كثير من الفرق تتعثر حين {pain}. "
                f"يبني ديالكس سير عمل مُراجَعًا باعتمادك يساعد على {angle}، وفريقك يبقى المتحكم.{privacy_ar} "
                f"هل يناسبكم استكشاف {offer_name} ({duration})؟ "
                f'لإيقاف التواصل اكتب "إلغاء الاشتراك".'
            )
        else:  # cold_email / follow_up
            lead_in = "متابعةً لملاحظتي السابقة، " if channel == "follow_up" else ""
            body = (
                f"مرحبًا، {buyer_title} في {company}،\n"
                f"{lead_in}كثير من فرق {sector_ar} في {country} تواجه تحديًا حين {pain}.\n"
                f"يبني ديالكس سير عمل مُراجَعًا يعمل باعتمادك ويساعد على {angle} — وفريقك يبقى المتحكم.{privacy_ar}\n"
                f"هل تفيدك جلسة قصيرة ({offer_name}، {duration}) لاستكشاف ذلك؟\n"
                f'لإيقاف التواصل، اكتب "إلغاء الاشتراك" ولن نعاود التواصل.'
            )
    else:
        subject = f"{sector_en}: {offer_name}"
        if channel == "linkedin_manual":
            body = (
                f"Hi — many {sector_en} teams struggle when {pain}. "
                f"Dealix builds a reviewed, approval-gated workflow that helps {angle}; "
                f"your team stays in control.{privacy_en} "
                f"Would a short {offer_name} be useful? "
                f'To opt out, reply "unsubscribe".'
            )
        elif channel == "website_form_manual":
            body = (
                f"Regarding {sector_en} at {company}: teams often get stuck when {pain}. "
                f"Dealix builds a reviewed, approval-gated workflow that helps {angle}; "
                f"your team stays in control.{privacy_en} "
                f"Would exploring a {offer_name} ({duration}) be useful? "
                f'To opt out, reply "unsubscribe".'
            )
        else:  # cold_email / follow_up
            lead_in = "Following up on my earlier note. " if channel == "follow_up" else ""
            body = (
                f"Hi {buyer_title} at {company},\n"
                f"{lead_in}Many {sector_en} teams in {country} struggle when {pain}.\n"
                f"Dealix builds a reviewed, approval-gated workflow that helps {angle} — "
                f"your team stays in control.{privacy_en}\n"
                f"Would a short {offer_name} ({duration}) be useful to explore this?\n"
                f'To opt out, reply "unsubscribe" and I will not contact you again.'
            )
    return subject, body


# ── Gates ──────────────────────────────────────────────────────────────────
def word_count(text: str) -> int:
    return len([w for w in text.replace("\n", " ").split(" ") if w.strip()])


def cta_count(body: str) -> int:
    return sum(body.count(m) for m in _CTA_MARKERS)


def has_opt_out(body: str) -> bool:
    low = body.lower()
    return any(m.lower() in low for m in _OPT_OUT_MARKERS)


def quality_gate(draft: dict[str, Any], cfg: dict[str, Any]) -> tuple[int, list[str]]:
    """Return (quality_score 0-100, reasons[]). Lower for each violation."""
    q = cfg["quality"]
    score = 100
    reasons: list[str] = []
    body = draft.get("body", "") or ""
    low = body.lower()
    pen = q["penalties"]

    pain = draft.get("pain_angle", "") or ""
    if not pain or pain not in body:
        score -= pen["no_pain"]
        reasons.append("no_pain")

    cc = cta_count(body)
    if cc == 0:
        score -= pen["no_single_cta"]
        reasons.append("no_single_cta")
    elif cc > 1:
        score -= pen["multiple_cta"]
        reasons.append("multiple_cta")

    if not has_opt_out(body):
        score -= pen["no_opt_out"]
        reasons.append("no_opt_out")

    sector_en = (draft.get("_sector_en") or "").lower()
    sector_ar = draft.get("_sector_ar") or ""
    if not ((sector_en and sector_en in low) or (sector_ar and sector_ar in body)):
        score -= pen["no_sector_context"]
        reasons.append("no_sector_context")

    # one-offer check
    offer_names = draft.get("_all_offer_names", [])
    mentioned = sum(1 for name in offer_names if name and name in body)
    if mentioned > 1:
        score -= pen["multiple_offers"]
        reasons.append("multiple_offers")

    for phrase in q.get("generic_agency_phrases", []):
        if phrase.lower() in low:
            score -= pen["generic_agency_language"]
            reasons.append("generic_agency_language")
            break

    if not draft.get("subject"):
        score -= pen["misleading_subject"]
        reasons.append("misleading_subject")

    limit = q["word_limits"].get(draft.get("channel", ""), 180)
    if word_count(body) > limit:
        score -= pen["over_word_limit"]
        reasons.append("over_word_limit")

    if draft.get("_sensitive"):
        if not any(t in low for t in ("approval", "control", "privacy")) and not any(
            t in body for t in ("باعتمادك", "المتحكم", "الخصوصية")
        ):
            score -= pen["no_human_control_in_sensitive_sector"]
            reasons.append("no_human_control_in_sensitive_sector")

    return max(0, score), reasons


def compliance_gate(draft: dict[str, Any], cfg: dict[str, Any]) -> tuple[int, str, list[str]]:
    """Return (compliance_score 0-100, risk_level, reasons[])."""
    risk = cfg["risk"]
    score = 100
    reasons: list[str] = []
    body = draft.get("body", "") or ""
    low = body.lower()

    for phrase in risk.get("banned_phrases_en", []):
        if phrase.lower() in low:
            score -= 40
            reasons.append(f"banned_phrase:{phrase}")
    for phrase in risk.get("banned_phrases_ar", []):
        if phrase in body:
            score -= 40
            reasons.append(f"banned_phrase_ar:{phrase}")

    if not has_opt_out(body):
        score -= 40
        reasons.append("no_opt_out")

    if cta_count(body) > 1:
        score -= 20
        reasons.append("multiple_cta")

    # WhatsApp cold outreach is never allowed
    if draft.get("channel") == "whatsapp_optin_reply" and draft.get("consent_status") not in (
        "opt_in",
        "inbound",
    ):
        score -= 50
        reasons.append("whatsapp_without_opt_in")

    # sensitive sectors require privacy-first language
    if draft.get("_sensitive"):
        ok_en = any(t in low for t in risk.get("privacy_first_required_terms_en", []))
        ok_ar = any(t in body for t in risk.get("privacy_first_required_terms_ar", []))
        if not (ok_en or ok_ar):
            score -= 30
            reasons.append("missing_privacy_first_language")

    score = max(0, score)
    if reasons:
        risk_level = "high"
    elif draft.get("_sensitive") or draft.get("research_required"):
        risk_level = "medium"
    else:
        risk_level = "low"
    return score, risk_level, reasons


def fit_score(draft: dict[str, Any]) -> int:
    """Deterministic fit score. Real, consented leads with a buyer title score higher."""
    score = 60
    if not draft.get("research_required"):
        score += 25
    if draft.get("consent_status") in ("opt_in", "public_business_contact"):
        score += 10
    if draft.get("buyer_title"):
        score += 5
    return min(100, score)


def priority_score(quality: int, compliance: int, fit: int, weights: dict) -> int:
    return round(
        quality * weights["quality_score"]
        + compliance * weights["compliance_score"]
        + fit * weights["fit_score"]
    )


# ── Draft generation ───────────────────────────────────────────────────────
@dataclass
class GenResult:
    drafts: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    used_real_leads: bool = False


def generate_drafts(
    target: int = 400,
    leads: list[dict] | None = None,
    run_date: str | None = None,
    cfg: dict[str, Any] | None = None,
) -> GenResult:
    """Generate >= target review-only drafts across channels and verticals."""
    cfg = cfg or load_all_configs()
    verticals = cfg["verticals"]["verticals"]
    offers = {o["stage"]: o for o in cfg["offers"]["offer_ladder"]}
    all_offer_names = []
    for o in cfg["offers"]["offer_ladder"]:
        all_offer_names += [o["name_en"], o["name_ar"]]
    distribution = cfg["distribution"]["distribution"]
    weights = cfg["founder_rules"]["priority_score"]["weights"]
    run_date = run_date or date_cls.today().isoformat()

    result = GenResult()
    real_leads = leads if leads else []
    result.used_real_leads = bool(real_leads)
    if not real_leads:
        result.warnings.append(
            "No real seed leads found — generated placeholder drafts that require research "
            "before any manual action. Populate data/commercial_seed_leads.example.jsonl "
            "(or your own consented file) to generate company-specific drafts."
        )

    # ensure floor is respected even if a custom distribution sums lower
    planned_total = sum(distribution.values())
    scale_extra = max(0, target - planned_total)

    channel_plan: list[str] = []
    for channel, n in distribution.items():
        channel_plan += [channel] * n
    # top up the highest-volume channel to reach target if needed
    if scale_extra:
        top_channel = max(distribution, key=distribution.get)
        channel_plan += [top_channel] * scale_extra

    for i, channel in enumerate(channel_plan):
        v = verticals[i % len(verticals)]
        if real_leads:
            lead = real_leads[i % len(real_leads)]
            v = _vertical_by_key(verticals, lead.get("vertical_hint", v["key"]))
        else:
            lead = make_placeholder_lead(verticals, i)
            v = _vertical_by_key(verticals, lead["vertical_hint"])

        research_required = (
            bool(lead.get("_placeholder")) or lead.get("research_status") == "required"
        )
        language = lead.get("language_hint") or ("ar" if i % 2 == 0 else "en")
        buyer_title = lead.get("buyer_title_hint") or v["buyer_titles"][i % len(v["buyer_titles"])]
        company = lead.get("company_name", "your company")
        country = lead.get("country") or (v.get("country_focus") or ["SA"])[0]
        pain_obj = v["pains"][i % len(v["pains"])]
        pain = pain_obj["ar"] if language == "ar" else pain_obj["en"]
        angles = v["angles_ar"] if language == "ar" else v["angles_en"]
        angle = angles[i % len(angles)]
        trigger = v["triggers"][i % len(v["triggers"])]
        stage = v.get("default_offer_stage", "entry_diagnostic")
        offer = offers[stage]
        offer_name = offer["name_ar"] if language == "ar" else offer["name_en"]

        subject, body = build_body(
            channel=channel,
            language=language,
            vertical=v,
            buyer_title=buyer_title,
            company=company,
            pain=pain,
            angle=angle,
            offer_name=offer_name,
            duration=offer.get("duration", ""),
            country=country,
            sensitive=v.get("sensitive", False),
        )

        seq = i + 1
        draft: dict[str, Any] = {
            "draft_id": f"DLX-{run_date}-{seq:04d}",
            "batch_id": f"BATCH-{run_date}",
            "created_at": run_date,
            "company_name": company,
            "source_lead_id": lead.get("lead_id", ""),
            "vertical": v["key"],
            "country": country,
            "city": lead.get("city", ""),
            "channel": channel,
            "language": language,
            "buyer_persona": v.get("name_en"),
            "buyer_title": buyer_title,
            "offer_stage": stage,
            "offer_name": offer_name,
            "pain_angle": pain,
            "trigger_event": trigger,
            "subject": subject,
            "body": body,
            "cta": "single approval-gated CTA (manual)",
            "opt_out": True,
            "consent_status": lead.get("consent_status", "none"),
            "research_required": research_required,
            "founder_notes": "",
            "rejection_reason": "",
            # mandatory safety flags
            **MANDATORY_FLAGS,
            # internal scoring hints (prefixed with _)
            "_sector_en": v["name_en"],
            "_sector_ar": v["name_ar"],
            "_sensitive": v.get("sensitive", False),
            "_all_offer_names": all_offer_names,
        }

        q_score, q_reasons = quality_gate(draft, cfg)
        c_score, risk_level, c_reasons = compliance_gate(draft, cfg)
        f_score = fit_score(draft)
        p_score = priority_score(q_score, c_score, f_score, weights)

        draft["quality_score"] = q_score
        draft["compliance_score"] = c_score
        draft["fit_score"] = f_score
        draft["priority_score"] = p_score
        draft["risk_level"] = risk_level

        q_pass = q_score >= cfg["quality"]["pass_threshold"]
        c_pass = c_score >= cfg["compliance"]["pass_threshold"] and not c_reasons

        if not c_pass:
            draft["status"] = "rejected_compliance"
            draft["rejection_reason"] = "; ".join(c_reasons) or "compliance_below_threshold"
        elif not q_pass:
            draft["status"] = "rejected_quality"
            draft["rejection_reason"] = "; ".join(q_reasons) or "quality_below_threshold"
        elif research_required:
            draft["status"] = "needs_research"
        else:
            draft["status"] = "founder_review"

        result.drafts.append(draft)

    return result


def strip_internal(draft: dict[str, Any]) -> dict[str, Any]:
    """Remove internal _-prefixed scoring hints before serialization."""
    return {k: v for k, v in draft.items() if not k.startswith("_")}
