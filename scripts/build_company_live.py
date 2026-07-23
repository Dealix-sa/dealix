#!/usr/bin/env python3
"""build_company_live.py — generate the canonical "Dealix يشتغل الآن / Dealix, Live" snapshot.

This is the operating spine behind the public + founder website surface at
`/[locale]/live`. It runs the REAL governed engines (no mockups) and writes a single
deterministic JSON the Next.js site reads at build time:

    frontend/src/content/company_live.json

It also writes a human-readable founder brief to data/founder_briefs/.

Doctrine (11 non-negotiables) enforced here — NO EXCEPTIONS:
  * Drafts only. Every outreach / call / proposal / diagnostic is approval_required.
  * NO live send, NO cold automation, NO scraping.
  * NO fabricated leads or CRM numbers. Real-vs-seed is labelled honestly; the
    snapshot reports exactly how many REAL leads are loaded (currently driven by the
    founder's own seed CSV — placeholder rows are counted as `seed_placeholder`).
  * Pricing is a band + "approval_required" (gate G03) — never a committed number.

Run:
    python3 scripts/build_company_live.py
    python3 scripts/build_company_live.py --max-drafts 8 --leads <path.csv>
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

OFFERS_YML = REPO_ROOT / "os" / "03_OFFERS.yml"
DEFAULT_LEADS_CSV = (
    REPO_ROOT / "docs" / "commercial" / "operations" / "targeting" / "agency_accounts_seed.csv"
)
OUT_JSON = REPO_ROOT / "frontend" / "src" / "content" / "company_live.json"
BRIEF_DIR = REPO_ROOT / "data" / "founder_briefs"

DOCTRINE_BANNER = [
    "مسودات فقط — كل إجراء خارجي بانتظار موافقة المؤسس (Draft, not Send).",
    "لا إرسال تلقائي، لا تواصل بارد، لا scraping.",
    "لا أرقام عملاء مخترعة — الأرقام الحقيقية تأتي من بيانات المؤسس فقط.",
    "الأسعار نطاقات تقديرية بانتظار موافقة (بوابة G03) — ليست التزاماً.",
]

# Map seed CSV segment -> engine sector (diagnostic_engine.SECTORS keys).
_SEGMENT_TO_SECTOR = {
    "agency_wedge": "agency",
    "marketing_agency": "marketing_agency",
    "agency_partner": "agency",
    "saas": "b2b_saas",
    "crm_partner": "b2b_services",
    "direct_b2b": "b2b_services",
    "hospitality": "b2b_services",
    "real_estate_developer": "real_estate",
    "consulting_firm": "training_consulting",
    "executive_governance": "b2b_services",
}

# Map seed segment -> primary recommended offer id (os/03_OFFERS.yml).
_SEGMENT_TO_OFFER = {
    "agency_wedge": "revenue_ai_os",
    "marketing_agency": "revenue_ai_os",
    "agency_partner": "revenue_ai_os",
    "saas": "ai_workflow_audit",
    "crm_partner": "ai_workflow_audit",
    "direct_b2b": "ai_workflow_audit",
    "hospitality": "ai_workflow_audit",
    "real_estate_developer": "revenue_ai_os",
    "consulting_firm": "ai_governance_pack",
    "executive_governance": "executive_command_center",
}

_PLACEHOLDER_MARKERS = ("REPLACE:", "هدف warm", "هدف استراتيجي", "وكالة مثال", "مثال")


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _is_placeholder(company: str, notes: str) -> bool:
    blob = f"{company} {notes}"
    return any(m in blob for m in _PLACEHOLDER_MARKERS)


def _is_do_not_contact(row: dict[str, str]) -> bool:
    status = (row.get("status") or "").strip().lower()
    notes = row.get("notes") or ""
    return status in {"closed_lost", "closed_won", "do_not_contact"} or "لا ترسل" in notes


# --------------------------------------------------------------------------- offers
def load_offers() -> list[dict[str, Any]]:
    """Load the strongest-services catalog from os/03_OFFERS.yml."""
    import yaml  # available (used by import_seed_leads.py)

    data = yaml.safe_load(OFFERS_YML.read_text(encoding="utf-8")) or {}
    offers_raw = data.get("offers", {})
    # Order = founder ladder (entry -> verticals -> governance -> retainer).
    order = [
        "ai_workflow_audit",
        "revenue_ai_os",
        "maintenance_intelligence_os",
        "project_controls_ai_os",
        "sovereign_knowledge_rag",
        "executive_command_center",
        "ai_governance_pack",
        "ai_ops_retainer",
    ]
    out: list[dict[str, Any]] = []
    for oid in order:
        o = offers_raw.get(oid)
        if not o:
            continue
        price = o.get("price_sar") or {}
        monthly = o.get("price_sar_monthly") or {}
        out.append(
            {
                "id": oid,
                "code": o.get("id", ""),
                "name": o.get("name", ""),
                "name_ar": o.get("name_ar", o.get("name", "")),
                "tagline": o.get("tagline", ""),
                "category": o.get("category", ""),
                "price_min": price.get("min") or monthly.get("min"),
                "price_max": price.get("max") or monthly.get("max"),
                "price_typical": price.get("typical") or monthly.get("typical"),
                "is_monthly": bool(monthly),
                "duration_days": o.get("duration_days") or {},
                "best_for": o.get("best_for", []),
                "deliverables": [
                    d.get("name") if isinstance(d, dict) else d
                    for d in (o.get("deliverables") or [])
                ][:6],
                "next_offer": o.get("natural_next_offer", o.get("natural_upsell", "")),
                "pricing_note": "نطاق تقديري — يُحدَّد بعد التشخيص وبموافقة المؤسس (G03)",
            }
        )
    return out


# --------------------------------------------------------------------------- leads
def load_leads(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        return []
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def score_lead(row: dict[str, str]) -> dict[str, Any]:
    """Transparent 0-100 score faithful to os/01_CLAUDE.md scoring doctrine.

    No hidden ML — every point is explainable to the founder.
    """
    segment = (row.get("segment") or "").strip()
    pain = (row.get("pain_hypothesis") or "").strip()
    motion = (row.get("motion") or "").strip().upper()
    priority = (row.get("priority") or "").strip().lower()

    breakdown: dict[str, int] = {}
    # Operations-heavy / ICP fit by segment.
    ops_heavy = {
        "agency_wedge": 20,
        "marketing_agency": 20,
        "agency_partner": 18,
        "direct_b2b": 18,
        "real_estate_developer": 20,
        "saas": 15,
        "crm_partner": 15,
        "consulting_firm": 14,
        "hospitality": 14,
        "executive_governance": 16,
    }
    breakdown["icp_fit"] = ops_heavy.get(segment, 10)
    # A clear, nameable pain hypothesis.
    breakdown["pain_clarity"] = 18 if pain else 0
    # Motion priority (A warm wedge highest).
    breakdown["motion"] = {"A": 18, "B": 14, "C": 12, "D": 12}.get(motion, 8)
    # Founder-assigned priority.
    breakdown["founder_priority"] = {"high": 20, "medium": 12, "low": 5}.get(priority, 8)
    # Addressable contact present.
    breakdown["contact_addressable"] = 10 if (row.get("contact") or "").strip() else 0
    # Channel realism (warm/manual channels score higher under no-cold doctrine).
    channel = (row.get("channel") or "").strip()
    breakdown["channel_fit"] = {
        "email_warm": 10,
        "partner_intro": 10,
        "inbound": 10,
        "phone_task": 8,
        "linkedin_manual": 7,
    }.get(channel, 5)

    score = min(100, sum(breakdown.values()))
    if score >= 80:
        tier = "أولوية عالية"
    elif score >= 60:
        tier = "أرسل بعد تخصيص"
    elif score >= 40:
        tier = "nurture"
    else:
        tier = "أرشفة"
    return {"score": score, "tier": tier, "breakdown": breakdown}


def build_pipeline(leads: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in leads:
        company = (row.get("company") or "").strip()
        if not company:
            continue
        notes = row.get("notes") or ""
        placeholder = _is_placeholder(company, notes)
        scoring = score_lead(row)
        rows.append(
            {
                "company": company,
                "contact": (row.get("contact") or "").strip(),
                "segment": (row.get("segment") or "").strip(),
                "sector": _SEGMENT_TO_SECTOR.get(
                    (row.get("segment") or "").strip(), "b2b_services"
                ),
                "motion": (row.get("motion") or "").strip().upper(),
                "offer_id": _SEGMENT_TO_OFFER.get(
                    (row.get("segment") or "").strip(), "ai_workflow_audit"
                ),
                "pain": (row.get("pain_hypothesis") or "").strip(),
                "status": (row.get("status") or "").strip(),
                "next_action": (row.get("next_action") or "").strip(),
                "priority": (row.get("priority") or "").strip(),
                "score": scoring["score"],
                "tier": scoring["tier"],
                "score_breakdown": scoring["breakdown"],
                "data_status": "seed_placeholder" if placeholder else "real",
                "do_not_contact": _is_do_not_contact(row),
            }
        )
    rows.sort(key=lambda r: r["score"], reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


# ----------------------------------------------------------------- drafts / calls
def contactable_real_first(pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Contactable leads, real ones first (each sub-group keeps score order).

    When the founder loads real CRM data, their genuine prospects lead every queue;
    seeded strategic targets fall in behind them. Never fabricates ordering by score.
    """
    contactable = [p for p in pipeline if not p["do_not_contact"]]
    real = [p for p in contactable if p["data_status"] == "real"]
    seed = [p for p in contactable if p["data_status"] != "real"]
    return real + seed


def build_drafts(pipeline: list[dict[str, Any]], max_drafts: int) -> list[dict[str, Any]]:
    """Generate governed warm-intro drafts (approval_required) for top contactable leads."""
    from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest

    gen = WarmIntroGenerator()
    out: list[dict[str, Any]] = []
    eligible = contactable_real_first(pipeline)[:max_drafts]
    for p in eligible:
        bundle = gen.generate(
            WarmIntroRequest(
                prospect_name=p["contact"] or "صاحب القرار",
                company_name=p["company"],
                sector=p["sector"],
                pain_context=p["pain"],
                founder_name="بسام",
            )
        )
        # Keep the two strongest variants per channel to keep the snapshot lean.
        for d in bundle.whatsapp_drafts[:2] + bundle.email_drafts[:1]:
            assert d.approval_status == "approval_required", "draft must be approval_required"
            out.append(
                {
                    "company": p["company"],
                    "contact": p["contact"],
                    "channel": d.channel,
                    "tone": d.tone,
                    "subject": d.subject_line,
                    "body_ar": d.body_ar,
                    "body_en": d.body_en,
                    "char_count": d.character_count,
                    "approval_status": d.approval_status,
                    "data_status": p["data_status"],
                }
            )
    return out


def build_call_list(pipeline: list[dict[str, Any]], max_calls: int) -> list[dict[str, Any]]:
    """Build governed call BRIEFS (the founder dials manually — never auto-dial)."""
    out: list[dict[str, Any]] = []
    callable_rows = contactable_real_first(pipeline)[:max_calls]
    for p in callable_rows:
        company = p["company"]
        contact = p["contact"] or "صاحب القرار"
        pain = p["pain"] or "هدر في متابعة الفرص"
        out.append(
            {
                "company": company,
                "contact": contact,
                "objective_ar": f"حجز تشخيص 30 دقيقة لـ {company}",
                "objective_en": f"Book a 30-min diagnostic for {company}",
                "script_ar": (
                    f"الافتتاح: السلام عليكم {contact}، معك بسام من Dealix.\n"
                    f"السبب: نشتغل مع شركات {p['segment'] or 'B2B'} على «{pain}».\n"
                    f"القيمة: نطلّع لكم خريطة فرص + تقرير أدلة على عملياتكم — بدون التزام.\n"
                    f"الطلب: تناسبك مكالمة 30 دقيقة هذا الأسبوع؟"
                ),
                "script_en": (
                    f"Open: Hi {contact}, this is Bassam from Dealix.\n"
                    f"Why: we work with {p['segment'] or 'B2B'} companies on \"{pain}\".\n"
                    f"Value: we map your opportunities + an evidence report on your ops — no commitment.\n"
                    f"Ask: would a 30-min call this week work?"
                ),
                "phone_note": "اتصال يدوي من المؤسس — النظام لا يتصل تلقائياً ولا يخزّن أرقاماً مخترعة",
                "approval_status": "founder_calls_manually",
                "data_status": p["data_status"],
            }
        )
    return out


def build_diagnostic_sample(pipeline: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Generate one governed diagnostic draft for the top prospect."""
    from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest

    ordered = contactable_real_first(pipeline)
    top = ordered[0] if ordered else None
    if not top:
        return None
    report = DiagnosticEngine().generate(
        DiagnosticRequest(
            company_name=top["company"],
            sector=top["sector"],
            pain_points=["lead_gen", "automation", "reporting"],
            notes=top["pain"],
        )
    )
    assert report.approval_status == "approval_required"
    return {
        "company": report.company_name,
        "sector": report.sector,
        "recommended_service": report.recommended_service,
        "approval_status": report.approval_status,
        "llm_used": report.llm_used,
        "sections": [
            {
                "title_ar": s.title_ar,
                "title_en": s.title_en,
                "body_ar": s.body_ar[:600],
                "body_en": s.body_en[:600],
            }
            for s in report.sections[:6]
        ],
    }


def build_proposals(
    pipeline: list[dict[str, Any]], offers: list[dict[str, Any]], max_props: int
) -> list[dict[str, Any]]:
    offer_by_id = {o["id"]: o for o in offers}
    out: list[dict[str, Any]] = []
    for p in contactable_real_first(pipeline)[:max_props]:
        o = offer_by_id.get(p["offer_id"]) or (offers[0] if offers else None)
        if not o:
            continue
        out.append(
            {
                "company": p["company"],
                "offer_id": o["id"],
                "offer_name": o["name"],
                "offer_name_ar": o["name_ar"],
                "scope_summary_ar": o["tagline"],
                "price_band_sar": (
                    f"{o['price_min']:,}–{o['price_max']:,}".replace(",", "٬")
                    if o["price_min"] and o["price_max"]
                    else "حسب النطاق"
                ),
                "pricing_gate": "G03 — لا يُشارك سعر محدد إلا بموافقة المؤسس",
                "approval_status": "approval_required",
                "data_status": p["data_status"],
            }
        )
    return out


# --------------------------------------------------------------------------- main
def build_snapshot(csv_path: Path, max_drafts: int) -> dict[str, Any]:
    offers = load_offers()
    leads = load_leads(csv_path)
    pipeline = build_pipeline(leads)

    real = [p for p in pipeline if p["data_status"] == "real"]
    seed = [p for p in pipeline if p["data_status"] == "seed_placeholder"]
    contactable = [p for p in pipeline if not p["do_not_contact"]]

    drafts = build_drafts(pipeline, max_drafts)
    call_list = build_call_list(pipeline, max_calls=min(8, max_drafts))
    diagnostic = build_diagnostic_sample(pipeline)
    proposals = build_proposals(pipeline, offers, max_props=5)

    return {
        "meta": {
            "generated_at": _now_iso(),
            "doctrine": DOCTRINE_BANNER,
            "counts": {
                "services": len(offers),
                "pipeline_total": len(pipeline),
                "real_leads": len(real),
                "seed_placeholders": len(seed),
                "contactable": len(contactable),
                "drafts_queued": len(drafts),
                "calls_queued": len(call_list),
                "proposals_drafted": len(proposals),
            },
            "intake_hint": (
                "حمّل عملاءك الحقيقيين عبر docs/commercial/operations/targeting/"
                "agency_accounts_seed.csv ثم أعد تشغيل build_company_live.py — "
                "النظام يقيّمهم ويولّد المسودات. لا نخترع أرقاماً."
            ),
        },
        "services": offers,
        "pipeline": pipeline,
        "drafts": drafts,
        "call_list": call_list,
        "diagnostic_sample": diagnostic,
        "proposals": proposals,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the Dealix-Live website snapshot.")
    ap.add_argument("--leads", default=str(DEFAULT_LEADS_CSV), help="leads CSV path")
    ap.add_argument("--max-drafts", type=int, default=10, help="max leads to draft for")
    ap.add_argument("--out", default=str(OUT_JSON), help="output JSON path")
    args = ap.parse_args()

    snapshot = build_snapshot(Path(args.leads), args.max_drafts)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Founder brief (markdown).
    BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    c = snapshot["meta"]["counts"]
    brief = BRIEF_DIR / f"company_live_{datetime.now(UTC).date()}.md"
    brief.write_text(
        "\n".join(
            [
                f"# Dealix يشتغل الآن — {datetime.now(UTC).date()}",
                "",
                "## الحوكمة",
                *[f"- {d}" for d in DOCTRINE_BANNER],
                "",
                "## اللقطة التشغيلية اليوم",
                f"- خدمات معروضة: {c['services']}",
                f"- خط الأنابيب: {c['pipeline_total']} (حقيقي: {c['real_leads']} · seed: {c['seed_placeholders']})",
                f"- مسودات بانتظار موافقتك: {c['drafts_queued']}",
                f"- مكالمات جاهزة (اتصال يدوي): {c['calls_queued']}",
                f"- عروض مُسوّدة: {c['proposals_drafted']}",
                "",
                "> الخطوة التالية: راجع المسودات، وافق يدوياً، ثم أرسل. حمّل عملاءك الحقيقيين في seed CSV.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"company_live snapshot -> {out_path}")
    print(f"founder brief         -> {brief}")
    print("counts: " + json.dumps(snapshot["meta"]["counts"], ensure_ascii=False))
    print("DEALIX_COMPANY_LIVE_BUILD=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
