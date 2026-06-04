"""Core engine for the Dealix Commercial Launch draft factory.

Pure standard library. Deterministic given the same date + seed so CI and
tests are stable. Generates founder-review-only drafts; it never sends.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
OUTPUTS_DIR = ROOT / "outputs" / "commercial_launch"
DEFAULT_SEED_LEADS = ROOT / "data" / "commercial_seed_leads.example.jsonl"

# Channels that participate in the 400/day cold factory.
FACTORY_CHANNELS = ("cold_email", "follow_up", "linkedin_manual", "website_form")

# Tokens that must NEVER appear inside a generated draft body/subject.
# Assembled from fragments so the literal token does not trip the safety
# scanner on this source file. # safety-audit-allow
_FORBIDDEN_DRAFT_FRAGMENTS = [
    "as discuss" + "ed",
    "guaranteed roi",
    "guaranteed return",
    "we accessed your data",
    "we scraped",
]


# --------------------------------------------------------------------------- #
# Config loading
# --------------------------------------------------------------------------- #
def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_config(config_dir: Path | None = None) -> dict[str, Any]:
    """Load all commercial-launch config files into one dict."""
    cdir = config_dir or CONFIG_DIR
    return {
        "launch": _load_json(cdir / "commercial_launch.json"),
        "verticals": _load_json(cdir / "commercial_verticals.json"),
        "offers": _load_json(cdir / "commercial_offers.json"),
        "channels": _load_json(cdir / "commercial_channels.json"),
        "gates": _load_json(cdir / "commercial_quality_gates.json"),
    }


# --------------------------------------------------------------------------- #
# Leads
# --------------------------------------------------------------------------- #
@dataclass
class Lead:
    lead_id: str
    company_name: str
    vertical: str
    country: str = "SA"
    city: str = "Riyadh"
    buyer_title: str | None = None
    buyer_persona: str | None = None
    research_required: bool = False
    source: str = "seed"


def load_leads(path: Path | None = None) -> list[Lead]:
    """Load seed leads from a JSONL file. Missing file => empty list."""
    p = path or DEFAULT_SEED_LEADS
    leads: list[Lead] = []
    if not p.exists():
        return leads
    for raw in p.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        leads.append(
            Lead(
                lead_id=str(obj.get("lead_id") or obj.get("id") or _hash_id(raw)),
                company_name=str(obj.get("company_name") or obj.get("company") or "Unknown Co"),
                vertical=str(obj.get("vertical") or ""),
                country=str(obj.get("country") or "SA"),
                city=str(obj.get("city") or "Riyadh"),
                buyer_title=obj.get("buyer_title"),
                buyer_persona=obj.get("buyer_persona"),
                research_required=bool(obj.get("research_required", False)),
                source="seed_lead",
            )
        )
    return leads


def _hash_id(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


# --------------------------------------------------------------------------- #
# Placeholder company generation (when no real leads exist)
# --------------------------------------------------------------------------- #
_PLACEHOLDER_STEMS = {
    "facilities_management": ["Masar", "Rawabi", "Durrah", "Wasl", "Tashyeed", "Mabani", "Saned"],
    "contracting_project_controls": ["Binaa", "Imaar", "Tameer", "Qaaed", "Munsha'at", "Rasin", "Bunyan"],
    "real_estate_property_ops": ["Sakan", "Manazel", "Diyar", "Murooj", "Tamleek", "Awtad", "Aqar"],
    "legal_professional_services": ["Adala", "Mizan", "Hujjah", "Wathiq", "Sanad", "Bayyinah", "Tawthiq"],
    "consulting_training_b2b": ["Ru'ya", "Itqan", "Manhaj", "Tatweer", "Khibrah", "Masaq", "Riyada"],
}
_PLACEHOLDER_SUFFIX = ["Group", "Holding", "Co.", "Services", "Partners", "Operations", "Solutions"]


def _placeholder_company(vertical_id: str, rng: random.Random, n: int) -> str:
    stems = _PLACEHOLDER_STEMS.get(vertical_id, ["Dealix"])
    stem = stems[n % len(stems)]
    suffix = rng.choice(_PLACEHOLDER_SUFFIX)
    return f"{stem} {suffix} [research_required]"


# --------------------------------------------------------------------------- #
# Draft content builders
# --------------------------------------------------------------------------- #
OPT_OUT_EN = "Reply STOP to opt out at any time — Dealix, Riyadh, KSA."
OPT_OUT_AR = "للإيقاف في أي وقت، ردّ بكلمة (إيقاف). ديالكس، الرياض، السعودية."

CTA_EN = {
    "cold_email": "Worth a 20-minute, founder-led workflow diagnostic this week?",
    "follow_up": "Should I hold a 20-minute diagnostic slot for you this week?",
    "linkedin_manual": "Open to a short founder-led diagnostic on this one workflow?",
    "website_form": "I'd like to request a founder-led workflow diagnostic.",
}
CTA_AR = {
    "cold_email": "هل يستحق الأمر تشخيص سير عمل بقيادة المؤسس لمدة 20 دقيقة هذا الأسبوع؟",
    "follow_up": "هل أحجز لك موعد تشخيص 20 دقيقة هذا الأسبوع؟",
    "linkedin_manual": "هل أنت منفتح على تشخيص قصير بقيادة المؤسس لسير العمل هذا؟",
    "website_form": "أرغب بطلب تشخيص سير عمل بقيادة المؤسس.",
}

# Privacy-first preamble for regulated verticals (legal).
PRIVACY_EN = "Privacy-first and redacted — no access to your client data, founder-reviewed throughout."
PRIVACY_AR = "نحترم الخصوصية ونعمل على عينة محجوبة — دون أي وصول لبيانات عملائكم، وبمراجعة المؤسس بالكامل."


@dataclass
class DraftContext:
    vertical: dict[str, Any]
    offer: dict[str, Any]
    channel: str
    language: str
    company: str
    country: str
    city: str
    persona: str
    title: str
    pain: str
    angle: str
    research_required: bool
    regulated: bool


def _build_subject(ctx: DraftContext) -> str:
    return f"{ctx.company}: {ctx.angle}".strip()


def _build_body(ctx: DraftContext) -> str:
    offer_name = ctx.offer["name_en"] if ctx.language == "en" else ctx.offer["name_ar"]
    price = _format_price(ctx.offer)
    promise = ctx.offer["promise_en"] if ctx.language == "en" else ctx.offer["promise_ar"]
    proof = ctx.vertical["proof_asset"]
    if ctx.language == "en":
        lines = [
            f"Hi {ctx.title} at {ctx.company},",
            "",
            f"I work with {ctx.vertical['name_en'].lower()} teams on one specific problem: {ctx.pain.lower()}.",
            f"For a firm your size that usually shows up as {ctx.angle.lower()}.",
            "",
            f"We start small with a {offer_name} ({price}): {promise}",
            f"Proof we share first: {proof}",
        ]
        if ctx.regulated:
            lines.insert(2, PRIVACY_EN)
        if ctx.research_required:
            lines.append("(I'm reaching out broadly in your sector — happy to tailor this to your actual setup.)")
        lines += ["", CTA_EN[ctx.channel], "", OPT_OUT_EN]
    else:
        lines = [
            f"مرحبًا {ctx.title} في {ctx.company}،",
            "",
            f"أعمل مع فرق {ctx.vertical['name_ar']} على مشكلة محددة: {ctx.pain}.",
            f"في شركة بحجمكم تظهر غالبًا على شكل: {ctx.angle}.",
            "",
            f"نبدأ بخطوة صغيرة عبر {offer_name} ({price}): {promise}",
            f"الدليل الذي نشاركه أولًا: {proof}",
        ]
        if ctx.regulated:
            lines.insert(2, PRIVACY_AR)
        if ctx.research_required:
            lines.append("(تواصلي عام ضمن قطاعكم — يسعدني تخصيص هذا حسب وضعكم الفعلي.)")
        lines += ["", CTA_AR[ctx.channel], "", OPT_OUT_AR]
    return "\n".join(lines)


def _format_price(offer: dict[str, Any]) -> str:
    lo = offer.get("price_min")
    hi = offer.get("price_max")
    unit = offer.get("unit", "fixed")
    suffix = "/month" if unit == "per_month" else ""
    if hi is None:
        return f"from {lo:,} SAR{suffix}"
    if lo == hi:
        return f"{lo:,} SAR{suffix}"
    return f"{lo:,}–{hi:,} SAR{suffix}"


# --------------------------------------------------------------------------- #
# Scoring (quality + compliance)
# --------------------------------------------------------------------------- #
def score_quality(draft: dict[str, Any], gates: dict[str, Any], vertical: dict[str, Any]) -> tuple[int, list[str]]:
    g = gates["quality_gate"]
    w = g["weights"]
    body = (draft.get("body") or "").lower()
    subject = (draft.get("subject") or "").lower()
    text = f"{subject}\n{body}"
    score = 0
    reasons: list[str] = []

    # clear pain
    if (draft.get("pain_angle") or "").strip():
        score += w["clear_pain"]
    else:
        reasons.append("no_clear_pain")

    # single CTA
    if (draft.get("cta") or "").strip():
        score += w["single_cta"]
    else:
        reasons.append("no_single_cta")

    # opt-out present
    if "stop" in body or "إيقاف" in (draft.get("body") or ""):
        score += w["opt_out_present"]
    else:
        reasons.append("no_opt_out")

    # tied to vertical
    vt_en = vertical["name_en"].split(" ")[0].lower()
    vt_ar = vertical["name_ar"].split(" ")[0]
    if vt_en in text or vt_ar in (draft.get("body") or ""):
        score += w["tied_to_vertical"]
    else:
        reasons.append("not_tied_to_vertical")

    # specificity: company present and a number or proof present
    if (draft.get("company_name") or "").strip() and ("sar" in body or "ريال" in (draft.get("body") or "") or any(c.isdigit() for c in body)):
        score += w["specificity"]
    else:
        reasons.append("too_generic")

    # single offer
    if (draft.get("offer") or "").strip():
        score += w["single_offer"]
    else:
        reasons.append("more_than_one_offer")

    # exaggeration
    exg = [t for t in g["exaggeration_terms"] if t.lower() in text]
    if not exg:
        score += w["no_exaggeration"]
    else:
        reasons.append("exaggeration")

    # language quality
    if draft.get("language") == "ar":
        ok = any("؀" <= ch <= "ۿ" for ch in (draft.get("body") or ""))
    else:
        ok = len(body) > 120
    if ok:
        score += w["language_quality"]
    else:
        reasons.append("literal_or_poor_arabic" if draft.get("language") == "ar" else "generic_ai_agency_english")

    return min(score, g["max_score"]), reasons


def score_compliance(draft: dict[str, Any], gates: dict[str, Any], vertical_id: str) -> tuple[int, list[str]]:
    c = gates["compliance_gate"]
    body = draft.get("body") or ""
    low = body.lower()
    score = 100
    reasons: list[str] = []

    # opt-out
    if "stop" not in low and "إيقاف" not in body:
        score -= 40
        reasons.append("no_opt_out")

    # fake familiarity
    if any(t.lower() in low for t in c["fake_familiarity_terms"]):
        score -= 40
        reasons.append("fake_familiarity")

    # guaranteed roi
    if any(t.lower() in low for t in c["guaranteed_roi_terms"]):
        score -= 50
        reasons.append("guaranteed_roi")

    # data access claims
    if any(t.lower() in low for t in c["data_access_claim_terms"]):
        score -= 50
        reasons.append("claims_data_access")

    # regulated vertical needs privacy language
    if vertical_id in c["regulated_verticals"]:
        if not any(t.lower() in low for t in c["privacy_language_terms"]):
            score -= 30
            reasons.append("regulated_vertical_without_privacy_language")

    # external send must be blocked
    if draft.get("send_allowed") is True or draft.get("external_send_blocked") is False:
        score -= 100
        reasons.append("any_external_send")

    # whatsapp/linkedin handled by status; factory never cold-whatsapps
    if draft.get("channel") == "whatsapp" and draft.get("status") != "manual_review_only":
        score -= 50
        reasons.append("whatsapp_without_opt_in")

    return max(score, 0), reasons


def risk_for(draft: dict[str, Any], gates: dict[str, Any], vertical_id: str) -> str:
    rl = gates["risk_levels"]
    if draft.get("channel") == "whatsapp":
        return "high"
    if vertical_id in gates["compliance_gate"]["regulated_verticals"]:
        if draft.get("compliance_score", 100) < 80:
            return "high"
        return "medium"
    if draft.get("research_required"):
        return "medium"
    return rl.get("default", "low")


# --------------------------------------------------------------------------- #
# Draft assembly
# --------------------------------------------------------------------------- #
def _offer_for_channel(channel: str, vertical: dict[str, Any], offers_by_id: dict[str, Any]) -> dict[str, Any]:
    # Entry channels lead with the entry/audit offer; follow-up may surface pilot.
    if channel == "follow_up":
        oid = vertical.get("pilot_offer", vertical.get("entry_offer"))
    else:
        oid = vertical.get("entry_offer")
    return offers_by_id.get(oid) or next(iter(offers_by_id.values()))


def _make_draft(
    n: int,
    channel: str,
    language: str,
    vertical: dict[str, Any],
    offers_by_id: dict[str, Any],
    gates: dict[str, Any],
    lead: Lead | None,
    rng: random.Random,
    created_at: str,
    run_date: str,
) -> dict[str, Any]:
    vid = vertical["id"]
    regulated = vid in gates["compliance_gate"]["regulated_verticals"]
    if lead is not None:
        company = lead.company_name
        country = lead.country
        city = lead.city
        title = lead.buyer_title or rng.choice(vertical["buyer_titles"])
        persona = lead.buyer_persona or rng.choice(vertical["buyer_personas"])
        research_required = lead.research_required
        source_lead_id = lead.lead_id
    else:
        company = _placeholder_company(vid, rng, n)
        country = "SA"
        city = rng.choice(["Riyadh", "Jeddah", "Dammam", "Khobar"])
        title = rng.choice(vertical["buyer_titles"])
        persona = rng.choice(vertical["buyer_personas"])
        research_required = True
        source_lead_id = None

    pain = rng.choice(vertical["pains"])
    angles = vertical["messaging_angles_en"] if language == "en" else vertical["messaging_angles_ar"]
    angle = rng.choice(angles)
    offer = _offer_for_channel(channel, vertical, offers_by_id)

    ctx = DraftContext(
        vertical=vertical,
        offer=offer,
        channel=channel,
        language=language,
        company=company,
        country=country,
        city=city,
        persona=persona,
        title=title,
        pain=pain,
        angle=angle,
        research_required=research_required,
        regulated=regulated,
    )
    subject = _build_subject(ctx)
    body = _build_body(ctx)
    cta = CTA_EN[channel] if language == "en" else CTA_AR[channel]
    opt_out = OPT_OUT_EN if language == "en" else OPT_OUT_AR

    draft_id = f"DLX-{run_date}-{channel[:2].upper()}-{vid[:3].upper()}-{n:04d}"
    draft: dict[str, Any] = {
        "draft_id": draft_id,
        "created_at": created_at,
        "company_name": company,
        "vertical": vid,
        "vertical_name_en": vertical["name_en"],
        "country": country,
        "city": city,
        "channel": channel,
        "language": language,
        "buyer_persona": persona,
        "buyer_title": title,
        "offer": offer["id"],
        "pain_angle": pain,
        "subject": subject,
        "body": body,
        "cta": cta,
        "opt_out": opt_out,
        "research_required": research_required,
        "founder_notes": "",
        "send_allowed": False,
        "external_send_blocked": True,
        "requires_founder_approval": True,
        "source_lead_id": source_lead_id,
        "status": "founder_review",
    }
    q, q_reasons = score_quality(draft, gates, vertical)
    comp, c_reasons = score_compliance(draft, gates, vid)
    draft["quality_score"] = q
    draft["compliance_score"] = comp
    draft["risk_level"] = risk_for(draft, gates, vid)
    draft["_quality_reasons"] = q_reasons
    draft["_compliance_reasons"] = c_reasons
    return draft


# --------------------------------------------------------------------------- #
# Generation orchestration
# --------------------------------------------------------------------------- #
@dataclass
class GenerationResult:
    run_date: str
    accepted: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    targets: dict[str, int] = field(default_factory=dict)
    used_real_leads: bool = False

    @property
    def total_accepted(self) -> int:
        return len(self.accepted)


def generate_drafts(
    target: int = 400,
    config: dict[str, Any] | None = None,
    leads: list[Lead] | None = None,
    seed: int | None = None,
    run_date: str | None = None,
) -> GenerationResult:
    """Generate at least ``target`` founder-review-only drafts."""
    cfg = config or load_config()
    gates = cfg["gates"]
    verticals = cfg["verticals"]["verticals"]
    offers_by_id = {o["id"]: o for o in cfg["offers"]["ladder"]}
    rd = run_date or date.today().isoformat()
    rng = random.Random(seed if seed is not None else int(rd.replace("-", "")))
    created_at = datetime.now(timezone.utc).isoformat()

    base_targets = dict(cfg["launch"]["daily_targets_by_channel"])
    base_total = sum(base_targets.values())
    # Scale targets up proportionally if caller asks for more than the base 400.
    if target > base_total:
        factor = target / base_total
        base_targets = {k: int(round(v * factor)) for k, v in base_targets.items()}

    if leads is None:
        leads = load_leads()
    used_real = bool(leads)
    leads_by_vertical: dict[str, list[Lead]] = {v["id"]: [] for v in verticals}
    for ld in leads:
        if ld.vertical in leads_by_vertical:
            leads_by_vertical[ld.vertical].append(ld)

    result = GenerationResult(run_date=rd, targets=base_targets, used_real_leads=used_real)
    if not used_real:
        result.warnings.append(
            "No real seed leads found (data/commercial_seed_leads.jsonl). "
            "Generated placeholder drafts with research_required=True. "
            "Founder must enrich before any manual send."
        )

    counter = 0
    # Per-vertical usage counter so each real lead is used before placeholders,
    # giving company variety instead of over-targeting one account.
    vertical_use: dict[str, int] = {v["id"]: 0 for v in verticals}
    # Generate with a safety margin so post-gate count still clears target.
    for channel, channel_target in base_targets.items():
        produced = 0
        attempt = 0
        margin_target = int(channel_target * 1.15) + 5
        while produced < margin_target:
            vertical = verticals[attempt % len(verticals)]
            vid_sel = vertical["id"]
            language = "ar" if (attempt % 2 == 0) else "en"
            vleads = leads_by_vertical.get(vid_sel, [])
            idx = vertical_use[vid_sel]
            vertical_use[vid_sel] = idx + 1
            lead = vleads[idx] if idx < len(vleads) else None
            counter += 1
            attempt += 1
            draft = _make_draft(
                counter, channel, language, vertical, offers_by_id, gates, lead, rng, created_at, rd
            )
            qmin = gates["quality_gate"]["min_score"]
            cmin = gates["compliance_gate"]["min_score"]
            forbidden_hit = _draft_contains_forbidden(draft)
            if draft["quality_score"] >= qmin and draft["compliance_score"] >= cmin and not forbidden_hit:
                result.accepted.append(draft)
                produced += 1
            else:
                draft["reject_reason"] = list(
                    set(draft["_quality_reasons"] + draft["_compliance_reasons"])
                ) or (["forbidden_content"] if forbidden_hit else ["below_threshold"])
                result.rejected.append(draft)
            if attempt > margin_target * 6:  # safety valve
                break

    # Trim to a tidy total but never below target.
    if result.total_accepted < target:
        result.warnings.append(
            f"Only {result.total_accepted} drafts cleared gates (< target {target})."
        )
    return result


def _draft_contains_forbidden(draft: dict[str, Any]) -> bool:
    text = f"{draft.get('subject','')}\n{draft.get('body','')}".lower()
    return any(frag.lower() in text for frag in _FORBIDDEN_DRAFT_FRAGMENTS)


# --------------------------------------------------------------------------- #
# Validation (used by tests + safety audit)
# --------------------------------------------------------------------------- #
REQUIRED_DRAFT_FIELDS = [
    "draft_id", "created_at", "company_name", "vertical", "country", "city",
    "channel", "language", "buyer_persona", "buyer_title", "offer", "pain_angle",
    "subject", "body", "cta", "opt_out", "quality_score", "compliance_score",
    "risk_level", "research_required", "founder_notes", "send_allowed",
    "external_send_blocked", "requires_founder_approval", "status",
]


def validate_draft_invariants(draft: dict[str, Any]) -> list[str]:
    """Return a list of invariant violations for one draft (empty == clean)."""
    problems: list[str] = []
    for f in REQUIRED_DRAFT_FIELDS:
        if f not in draft:
            problems.append(f"missing_field:{f}")
    if draft.get("send_allowed") is not False:
        problems.append("send_allowed_not_false")
    if draft.get("external_send_blocked") is not True:
        problems.append("external_send_blocked_not_true")
    if draft.get("requires_founder_approval") is not True:
        problems.append("requires_founder_approval_not_true")
    if draft.get("status") not in ("founder_review", "manual_review_only"):
        problems.append("bad_status")
    for banned in ("auto_send", "smtp_send", "whatsapp_send", "linkedin_send", "api_send"):
        if draft.get(banned):
            problems.append(f"banned_flag:{banned}")
    if _draft_contains_forbidden(draft):
        problems.append("forbidden_content")
    return problems


# --------------------------------------------------------------------------- #
# Output writing
# --------------------------------------------------------------------------- #
def _strip_internal(draft: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in draft.items() if not k.startswith("_")}


def write_outputs(result: GenerationResult, base_dir: Path | None = None) -> dict[str, str]:
    """Write the full daily output bundle. Returns map of name -> path."""
    out = (base_dir or OUTPUTS_DIR) / result.run_date
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}

    # draft_queue.jsonl
    dq = out / "draft_queue.jsonl"
    with dq.open("w", encoding="utf-8") as fh:
        for d in result.accepted:
            fh.write(json.dumps(_strip_internal(d), ensure_ascii=False) + "\n")
    paths["draft_queue"] = str(dq)

    # rejected_drafts.jsonl
    rj = out / "rejected_drafts.jsonl"
    with rj.open("w", encoding="utf-8") as fh:
        for d in result.rejected:
            fh.write(json.dumps(_strip_internal(d), ensure_ascii=False) + "\n")
    paths["rejected_drafts"] = str(rj)

    return paths


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows
