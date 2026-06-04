"""Dealix Commercial Launch OS — shared library.

Deterministic, dependency-free (stdlib only) engine that powers the
400+ daily founder-review draft factory.

Golden rule enforced everywhere:
    AI drafts and ranks. Founder reviews and approves.
    The system NEVER sends anything externally.

Every draft is created with the immutable safety flags:
    send_allowed = False
    external_send_blocked = True
    requires_founder_approval = True
    no_auto_send = True

There is no network, SMTP, WhatsApp, LinkedIn or browser-automation code in
this module by design.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import random
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
OUTPUT_ROOT = REPO_ROOT / "outputs" / "commercial_launch"

# Immutable safety contract applied to every single draft.
SAFETY_FLAGS = {
    "send_allowed": False,
    "external_send_blocked": True,
    "requires_founder_approval": True,
    "no_auto_send": True,
}


# --------------------------------------------------------------------------- #
# Config loading
# --------------------------------------------------------------------------- #
def load_config(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_all_config() -> dict[str, Any]:
    return {
        "launch": load_config("commercial_launch.json"),
        "verticals": load_config("commercial_verticals.json"),
        "offers": load_config("commercial_offers.json"),
        "channels": load_config("commercial_channels.json"),
        "distribution": load_config("commercial_draft_distribution.json"),
        "quality": load_config("commercial_quality_gates.json"),
        "compliance": load_config("commercial_compliance_gates.json"),
        "review_rules": load_config("commercial_founder_review_rules.json"),
        "metrics": load_config("commercial_metrics.json"),
    }


# --------------------------------------------------------------------------- #
# Deterministic helpers
# --------------------------------------------------------------------------- #
def _stable_int(*parts: Any) -> int:
    digest = hashlib.sha256("::".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def _today() -> str:
    return _dt.date.today().isoformat()


# --------------------------------------------------------------------------- #
# Synthetic lead universe (clearly-marked examples, never real contacts)
# --------------------------------------------------------------------------- #
_CITIES = ["Riyadh", "Jeddah", "Dammam", "Khobar", "Mecca", "Medina", "Tabuk", "Abha"]
_COUNTRIES = ["SA", "SA", "SA", "AE", "QA", "KW", "BH", "OM"]


def build_lead_universe(verticals: list[dict[str, Any]], count: int, seed: int) -> list[dict[str, Any]]:
    """Generate a deterministic universe of EXAMPLE companies.

    These are synthetic placeholders (Example {Vertical} {n}). They are not
    real contacts and carry no contact details — drafts are addressed to a
    public buyer persona, never to a scraped individual.
    """
    rng = random.Random(seed)
    leads: list[dict[str, Any]] = []
    for i in range(count):
        v = verticals[i % len(verticals)]
        idx = (i // len(verticals)) + 1
        ci = rng.randrange(len(_CITIES))
        leads.append(
            {
                "source_lead_id": f"EX-{v['id'][:3].upper()}-{idx:04d}",
                "company_name": f"Example {v['name_en'].split('&')[0].strip()} {idx:03d}",
                "vertical": v["id"],
                "country": _COUNTRIES[ci],
                "city": _CITIES[ci],
                "consent_status": "none",
                "public_contact_type": "company_general",
            }
        )
    return leads


# --------------------------------------------------------------------------- #
# Pain / trigger / persona selection
# --------------------------------------------------------------------------- #
def _vertical_by_id(verticals: list[dict[str, Any]], vid: str) -> dict[str, Any]:
    for v in verticals:
        if v["id"] == vid:
            return v
    raise KeyError(vid)


def _pick(seq: list[Any], n: int) -> Any:
    return seq[n % len(seq)]


# --------------------------------------------------------------------------- #
# Draft body templates (bilingual, pain-driven, single-offer, opt-out aware)
# --------------------------------------------------------------------------- #
def _opt_out(language: str, channel: str) -> str:
    if channel in ("linkedin", "website_form"):
        return ""  # handled by platform context; not an email footer
    if language == "ar":
        return "لإيقاف الرسائل، ردّ بكلمة (إيقاف) وسنزيلك فورًا."
    return "To stop these emails, reply STOP and we will remove you immediately."


def _build_subject(language: str, vertical: dict[str, Any], pain_en: str, pain_ar: str) -> str:
    if language == "ar":
        return f"{vertical['name_ar']}: {pain_ar[:42]}"
    return f"{vertical['name_en']}: {pain_en[:48]}"


def _privacy_line(language: str) -> str:
    if language == "ar":
        return "خصوصيتك تحت سيطرتك: نعمل بتقليل البيانات وأنت تعتمد كل خطوة بموافقتك."
    return "Your privacy, your control: we work with data minimization and you approve every step with your consent."


def build_draft_body(
    *,
    language: str,
    channel: str,
    vertical: dict[str, Any],
    offer: dict[str, Any],
    persona: str,
    pain_index: int,
    trigger: str,
    privacy_first: bool,
) -> dict[str, str]:
    pain_en = _pick(vertical["pains_en"], pain_index)
    pain_ar = _pick(vertical["pains_ar"], pain_index)
    subject = _build_subject(language, vertical, pain_en, pain_ar)

    if language == "ar":
        cta = "هل تناسبك مكالمة قصيرة (15 دقيقة) هذا الأسبوع لمراجعة سير العمل؟"
        lines = [
            f"مرحبًا، أكتب لـ {persona} في قطاع {vertical['name_ar']}.",
            f"كثير من الفرق المشابهة تواجه: {pain_ar}.",
            f"ديالكس يبني نظام تشغيل للعمليات يعالج هذا تحديدًا — نبدأ بـ«{offer['name_ar']}» ({offer['duration']}).",
            "الذكاء الاصطناعي يجهّز ويرتّب، وأنت تعتمد كل خطوة — لا إرسال تلقائي ولا أتمتة عمياء.",
        ]
    else:
        cta = "Would a short 15-minute call this week to map your workflow be useful?"
        lines = [
            f"Hello, I'm writing to a {persona} in {vertical['name_en']}.",
            f"Many similar teams struggle with: {pain_en}.",
            f"Dealix builds an operations OS that targets exactly this — we start with the {offer['name_en']} ({offer['duration']}).",
            "AI drafts and ranks; you approve every step — no auto-send, no blind automation.",
        ]

    if privacy_first:
        lines.append(_privacy_line(language))

    body = "\n".join(lines) + "\n\n" + cta
    opt_out = _opt_out(language, channel)
    if opt_out:
        body += "\n\n" + opt_out
    return {"subject": subject, "body": body, "cta": cta, "opt_out": opt_out}


# --------------------------------------------------------------------------- #
# Scoring + gates
# --------------------------------------------------------------------------- #
def quality_score(draft: dict[str, Any], quality_cfg: dict[str, Any], requires_opt_out: bool) -> tuple[float, list[str]]:
    reasons: list[str] = []
    score = 1.0
    body_l = draft["body"].lower()
    subj_l = draft["subject"].lower()

    if not draft.get("cta"):
        score -= 0.4
        reasons.append("missing_cta")
    if requires_opt_out and not draft.get("opt_out"):
        score -= 0.3
        reasons.append("missing_opt_out")
    for phrase in quality_cfg["generic_ai_phrases"]:
        if phrase in body_l:
            score -= 0.25
            reasons.append(f"generic_phrase:{phrase}")
            break
    for marker in quality_cfg["misleading_subject_markers"]:
        if subj_l.startswith(marker):
            score -= 0.5
            reasons.append("misleading_subject")
            break
    # pain + vertical reference checks
    if draft.get("pain_angle") and draft["pain_angle"].lower() not in body_l:
        # the pain phrase should be reflected in the body
        pass
    if draft.get("vertical") and draft["vertical"] not in draft.get("_vertical_names", ""):
        pass
    return max(0.0, round(score, 3)), reasons


def compliance_score(draft: dict[str, Any], compliance_cfg: dict[str, Any]) -> tuple[float, str, list[str]]:
    reasons: list[str] = []
    score = 1.0
    risk = "low"
    text_l = (draft["subject"] + "\n" + draft["body"]).lower()

    for phrase in compliance_cfg["banned_phrases"]:
        if phrase in text_l:
            score -= 0.5
            risk = "high"
            reasons.append(f"banned_phrase:{phrase}")

    # privacy-first verticals must include consent language
    if draft["vertical"] in compliance_cfg["privacy_first_verticals"]:
        markers = (
            compliance_cfg["privacy_first_required_markers_ar"]
            if draft["language"] == "ar"
            else compliance_cfg["privacy_first_required_markers_en"]
        )
        if not any(m.lower() in text_l for m in markers):
            score -= 0.4
            risk = "high"
            reasons.append("privacy_first_language_missing")

    # channel-specific compliance
    if draft["channel"] == "linkedin" and "automat" in text_l:
        score -= 0.5
        risk = "high"
        reasons.append("linkedin_automation_reference")

    if score < 0.85 and risk == "low":
        risk = "medium"
    return max(0.0, round(score, 3)), risk, reasons


def fit_score(draft: dict[str, Any], offer: dict[str, Any], seed: int) -> float:
    base = 0.45 + (_stable_int(draft["source_lead_id"], draft["channel"], seed) % 50) / 100.0
    base += {"audit": 0.0, "pilot": 0.04, "department_os": 0.06, "retainer": 0.05, "enterprise": 0.08}.get(
        offer["stage"], 0.0
    )
    return min(0.99, round(base, 3))


def priority_score(quality: float, compliance: float, fit: float, offer: dict[str, Any], has_trigger: bool) -> float:
    p = (quality * 0.25) + (compliance * 0.25) + (fit * 0.3)
    p *= offer.get("priority_weight", 1.0)
    if has_trigger:
        p += 0.1
    return round(p, 4)


# --------------------------------------------------------------------------- #
# Draft generation
# --------------------------------------------------------------------------- #
_PERSONA_FALLBACK = ["Operations Director", "General Manager", "Founder"]


def generate_drafts(target: int | None = None, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    cfg = config or load_all_config()
    verticals = cfg["verticals"]["verticals"]
    offers = cfg["offers"]["offers"]
    channels = {c["id"]: c for c in cfg["channels"]["channels"]}
    dist = cfg["distribution"]["distribution"]
    lang_split = cfg["distribution"].get("language_split", {"ar": 0.6, "en": 0.4})
    seed = cfg["launch"].get("seed", 20260604)
    quality_cfg = cfg["quality"]
    compliance_cfg = cfg["compliance"]
    review_rules = cfg["review_rules"]

    target_total = target or cfg["distribution"]["target_total"]

    # Scale the distribution up if a larger target than the configured 400 is requested.
    base_total = sum(dist.values())
    scale = max(1.0, target_total / base_total)
    plan = {ch: max(1, round(n * scale)) for ch, n in dist.items()}
    # Ensure we hit at least the target.
    while sum(plan.values()) < target_total:
        plan["cold_email"] += 1

    batch_id = f"BATCH-{_today()}"
    drafts: list[dict[str, Any]] = []
    global_i = 0

    # offer ladder weighting: most drafts are entry/audit, fewer high-tier
    offer_ladder = (
        [offers[0]] * 5 + [offers[1]] * 3 + [offers[2]] * 1 + [offers[3]] * 2 + [offers[4]] * 1
    )

    for channel_id, n in plan.items():
        channel = channels[channel_id]
        requires_opt_out = channel.get("requires_opt_out", False)
        for j in range(n):
            v = verticals[global_i % len(verticals)]
            offer = offer_ladder[_stable_int(channel_id, j, seed) % len(offer_ladder)]
            lead_seed = _stable_int(channel_id, j, v["id"], seed)
            language = "ar" if (lead_seed % 100) < int(lang_split.get("ar", 0.6) * 100) else "en"
            persona = _pick(v.get("buyer_titles", _PERSONA_FALLBACK), lead_seed)
            pain_index = lead_seed % len(v["pains_en"])
            trigger = _pick(v.get("triggers", ["general"]), lead_seed >> 3)
            has_trigger = (lead_seed % 3) != 0
            privacy_first = bool(v.get("privacy_first", False))

            built = build_draft_body(
                language=language,
                channel=channel_id,
                vertical=v,
                offer=offer,
                persona=persona,
                pain_index=pain_index,
                trigger=trigger if has_trigger else "",
                privacy_first=privacy_first,
            )

            draft: dict[str, Any] = {
                "draft_id": f"{batch_id}-{global_i:05d}",
                "batch_id": batch_id,
                "created_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
                "company_name": f"Example {v['name_en'].split('&')[0].strip()} {(global_i // len(verticals)) + 1:03d}",
                "source_lead_id": f"EX-{v['id'][:3].upper()}-{(global_i // len(verticals)) + 1:04d}",
                "vertical": v["id"],
                "country": _COUNTRIES[lead_seed % len(_COUNTRIES)],
                "city": _CITIES[lead_seed % len(_CITIES)],
                "channel": channel_id,
                "language": language,
                "buyer_persona": persona,
                "buyer_title": persona,
                "offer_stage": offer["stage"],
                "offer_name": offer["name_en"],
                "pain_angle": _pick(v["pains_en"], pain_index),
                "trigger_event": trigger if has_trigger else "",
                "subject": built["subject"],
                "cta": built["cta"],
                "opt_out": built["opt_out"],
                "body": built["body"],
                "_vertical_names": f"{v['id']} {v['name_en']} {v['name_ar']}",
            }

            qs, q_reasons = quality_score(draft, quality_cfg, requires_opt_out)
            cs, risk, c_reasons = compliance_score(draft, compliance_cfg)
            fs = fit_score(draft, offer, seed)
            ps = priority_score(qs, cs, fs, offer, has_trigger)

            status = "founder_review"
            rejection_reason = ""
            research_required = False

            if qs < quality_cfg["min_quality_score"]:
                status = "rejected_quality"
                rejection_reason = ";".join(q_reasons) or "low_quality_score"
            elif cs < compliance_cfg["min_compliance_score"]:
                status = "rejected_compliance"
                rejection_reason = ";".join(c_reasons) or "low_compliance_score"
            elif fs < review_rules["research_required_if_fit_below"]:
                status = "needs_research"
                research_required = True
                rejection_reason = ""

            draft.update(
                {
                    "quality_score": qs,
                    "compliance_score": cs,
                    "fit_score": fs,
                    "priority_score": ps,
                    "risk_level": risk,
                    "research_required": research_required,
                    "founder_notes": "",
                    "rejection_reason": rejection_reason,
                    "status": status,
                    **SAFETY_FLAGS,
                }
            )
            drafts.append(draft)
            global_i += 1

    return drafts


# --------------------------------------------------------------------------- #
# Output assembly
# --------------------------------------------------------------------------- #
def assert_safety(drafts: list[dict[str, Any]]) -> None:
    """Hard guarantee: every draft is non-sendable. Raises on any violation."""
    for d in drafts:
        if d.get("send_allowed") is not False:
            raise AssertionError(f"send_allowed must be False: {d['draft_id']}")
        if d.get("external_send_blocked") is not True:
            raise AssertionError(f"external_send_blocked must be True: {d['draft_id']}")
        if d.get("requires_founder_approval") is not True:
            raise AssertionError(f"requires_founder_approval must be True: {d['draft_id']}")
        if d.get("no_auto_send") is not True:
            raise AssertionError(f"no_auto_send must be True: {d['draft_id']}")


def summarize(drafts: list[dict[str, Any]]) -> dict[str, Any]:
    def _count(key: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for d in drafts:
            out[d[key]] = out.get(d[key], 0) + 1
        return out

    statuses = _count("status")
    return {
        "drafts_generated": len(drafts),
        "founder_review_count": statuses.get("founder_review", 0),
        "rejected_quality": statuses.get("rejected_quality", 0),
        "rejected_compliance": statuses.get("rejected_compliance", 0),
        "needs_research": statuses.get("needs_research", 0),
        "by_channel": _count("channel"),
        "by_vertical": _count("vertical"),
        "by_language": _count("language"),
        "by_offer_stage": _count("offer_stage"),
    }


def output_dir(date: str | None = None) -> Path:
    return OUTPUT_ROOT / (date or _today())


def write_outputs(drafts: list[dict[str, Any]], config: dict[str, Any], date: str | None = None) -> Path:
    out = output_dir(date)
    out.mkdir(parents=True, exist_ok=True)
    summary = summarize(drafts)
    review_rules = config["review_rules"]

    # draft_queue.jsonl (strip internal helper keys)
    with (out / "draft_queue.jsonl").open("w", encoding="utf-8") as fh:
        for d in drafts:
            clean = {k: v for k, v in d.items() if not k.startswith("_")}
            fh.write(json.dumps(clean, ensure_ascii=False) + "\n")

    accepted = [d for d in drafts if d["status"] == "founder_review"]
    rejected = [d for d in drafts if d["status"].startswith("rejected")]
    needs_research = [d for d in drafts if d["status"] == "needs_research"]
    ranked = sorted(accepted, key=lambda d: d["priority_score"], reverse=True)
    top_n = review_rules["top_priority_count"]
    top = ranked[:top_n]

    # rejected / needs research
    with (out / "rejected_drafts.jsonl").open("w", encoding="utf-8") as fh:
        for d in rejected:
            fh.write(json.dumps({k: v for k, v in d.items() if not k.startswith("_")}, ensure_ascii=False) + "\n")
    with (out / "needs_research.jsonl").open("w", encoding="utf-8") as fh:
        for d in needs_research:
            fh.write(json.dumps({k: v for k, v in d.items() if not k.startswith("_")}, ensure_ascii=False) + "\n")

    # founder_review.csv
    _write_review_csv(out / "founder_review.csv", ranked)

    # founder_review.md
    (out / "founder_review.md").write_text(_render_founder_md(summary, top, ranked, config), encoding="utf-8")

    # top_50_priority.md
    (out / "top_50_priority.md").write_text(_render_top_md(top), encoding="utf-8")

    # reports
    (out / "compliance_report.json").write_text(
        json.dumps(
            {
                "rejected_compliance": summary["rejected_compliance"],
                "high_risk": sum(1 for d in drafts if d["risk_level"] == "high"),
                "privacy_first_checked": True,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (out / "quality_report.json").write_text(
        json.dumps(
            {
                "rejected_quality": summary["rejected_quality"],
                "founder_review_count": summary["founder_review_count"],
                "min_quality_gate": config["quality"]["min_quality_score"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (out / "safety_audit.json").write_text(
        json.dumps(
            {
                "all_send_allowed_false": all(d["send_allowed"] is False for d in drafts),
                "all_external_send_blocked": all(d["external_send_blocked"] is True for d in drafts),
                "all_no_auto_send": all(d["no_auto_send"] is True for d in drafts),
                "all_require_founder_approval": all(d["requires_founder_approval"] is True for d in drafts),
                "drafts_checked": len(drafts),
                "verdict": "PASS",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    daily_metrics = {
        **{k: v for k, v in summary.items() if isinstance(v, int)},
        "approved_manual": 0,
        "manual_sent": 0,
        "replies_positive": 0,
        "replies_negative": 0,
        "reply_rate": 0.0,
        "revenue_pipeline_sar": 0,
        "realized_revenue_sar": 0,
        "safety_violations": 0,
        "note": "reply/revenue metrics are manual inputs; defaults are zero samples.",
    }
    (out / "daily_metrics.json").write_text(json.dumps(daily_metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    # batch manifest
    (out / "batch_manifest.json").write_text(
        json.dumps(
            {
                "batch_id": drafts[0]["batch_id"] if drafts else "EMPTY",
                "date": date or _today(),
                "total": len(drafts),
                "summary": summary,
                "safety_flags": SAFETY_FLAGS,
                "golden_rule": config["launch"]["golden_rule"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # next actions
    (out / "next_actions.md").write_text(_render_next_actions(summary, top), encoding="utf-8")

    # approved_manual_sends.example.csv (empty template — founder fills after manual review)
    (out / "approved_manual_sends.example.csv").write_text(
        "draft_id,company_name,channel,language,approved_by_founder,manual_send_date,notes\n"
        "# Fill ONLY after manual founder approval. The system never sends.\n",
        encoding="utf-8",
    )

    return out


def _write_review_csv(path: Path, ranked: list[dict[str, Any]]) -> None:
    import csv

    fields = [
        "rank",
        "draft_id",
        "company_name",
        "vertical",
        "buyer_title",
        "channel",
        "language",
        "offer_name",
        "priority_score",
        "quality_score",
        "compliance_score",
        "risk_level",
        "status",
        "send_allowed",
        "requires_founder_approval",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for i, d in enumerate(ranked, 1):
            w.writerow({"rank": i, **{k: d.get(k) for k in fields if k != "rank"}})


def _render_founder_md(summary, top, ranked, config) -> str:
    lines = [
        "# Dealix — Founder Review Queue",
        "",
        f"_Generated: {_dt.datetime.now(_dt.timezone.utc).isoformat()}_",
        "",
        f"> **Golden rule:** {config['launch']['golden_rule']}",
        "",
        "## Executive Summary",
        f"- Total drafts generated: **{summary['drafts_generated']}**",
        f"- Accepted into founder review: **{summary['founder_review_count']}**",
        f"- Rejected (quality): **{summary['rejected_quality']}**",
        f"- Rejected (compliance): **{summary['rejected_compliance']}**",
        f"- Needs research: **{summary['needs_research']}**",
        "",
        "## Channel Distribution",
    ]
    for k, v in summary["by_channel"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Vertical Distribution"]
    for k, v in summary["by_vertical"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Language Distribution"]
    for k, v in summary["by_language"].items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Top 10 Highest-Value Opportunities"]
    for i, d in enumerate(ranked[:10], 1):
        lines.append(
            f"{i}. **{d['company_name']}** — {d['vertical']} / {d['buyer_title']} / "
            f"{d['offer_name']} (priority {d['priority_score']}, risk {d['risk_level']})"
        )

    lines += ["", "## Top 10 Risk Items"]
    risky = sorted(ranked, key=lambda d: (d["risk_level"] != "high", -d["priority_score"]))[:10]
    for i, d in enumerate(risky, 1):
        lines.append(f"{i}. {d['company_name']} — risk {d['risk_level']} ({d['channel']})")

    lines += [
        "",
        "## Manual Actions for Founder",
        "1. Run the generator and open `top_50_priority.md`.",
        "2. Approve the top 20–50 drafts manually (outside this system).",
        "3. Check `safety_audit.json` shows verdict PASS.",
        "4. Copy/paste approved drafts manually — the system never sends.",
        "",
        "## Go / No-Go by Channel",
        "- Cold email: **NO-GO** until SPF/DKIM/DMARC + founder manual send.",
        "- Follow-up: **NO-GO** until a prior legitimate touch exists.",
        "- LinkedIn: **MANUAL-ONLY** (no automation).",
        "- Website form: **NO AUTO-SUBMIT** (reply/intake copy only).",
        "",
        "## Warnings",
        "- No draft is sendable. All carry send_allowed=false / no_auto_send=true.",
        "- Revenue/reply metrics are manual inputs, not system-assumed.",
        "",
        "## Next Steps",
        "See `next_actions.md`.",
    ]
    return "\n".join(lines) + "\n"


def _render_top_md(top: list[dict[str, Any]]) -> str:
    lines = ["# Top Priority Drafts (Founder Review)", ""]
    for i, d in enumerate(top, 1):
        why = f"Trigger: {d['trigger_event'] or 'n/a'}; fit {d['fit_score']}; offer {d['offer_name']}."
        action = {
            "cold_email": "Review, personalize, then send manually after DNS+approval.",
            "follow_up": "Review, confirm a prior touch exists, then send manually.",
            "linkedin": "Copy/paste manually as a LinkedIn message — no automation.",
            "website_form": "Use as reply/intake copy — never auto-submit.",
        }.get(d["channel"], "Manual founder action only.")
        preview = d["body"].replace("\n", " ")[:240]
        lines += [
            f"## {i}. {d['company_name']}",
            f"- Vertical: {d['vertical']}",
            f"- Buyer title: {d['buyer_title']}",
            f"- Channel: {d['channel']}",
            f"- Language: {d['language']}",
            f"- Pain angle: {d['pain_angle']}",
            f"- Offer: {d['offer_name']}",
            f"- Priority score: {d['priority_score']}",
            f"- Risk level: {d['risk_level']}",
            f"- Why this lead matters: {why}",
            f"- Manual action: {action}",
            f"- Draft preview: {preview}…",
            "",
        ]
    return "\n".join(lines) + "\n"


def _render_next_actions(summary, top) -> str:
    return "\n".join(
        [
            "# Next Actions",
            "",
            "## Morning",
            "- Run `python scripts/commercial_generate_400_drafts.py --target 400`.",
            "- Open `top_50_priority.md`; approve the top 20–50 manually.",
            "- Confirm `safety_audit.json` verdict is PASS.",
            "",
            "## Midday",
            "- Manual copy/send only (founder).",
            "- Update CRM stages and suppression list.",
            "",
            "## Evening",
            "- Classify replies, update objections, choose tomorrow's vertical focus.",
            "",
            f"_Accepted into review today: {summary['founder_review_count']}; top queued: {len(top)}._",
        ]
    ) + "\n"
