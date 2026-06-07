#!/usr/bin/env python3
"""Dealix Day-0 Company Activation — one command that stands the company up.

محرّك التشغيل اليومي: أمر واحد يولّد حزمة المُشغّل الكاملة لليوم.

What it produces (under ``data/day0/<date>/``):

  1. ``prospects.csv`` / ``prospects.md`` — your prospect list, ICP-scored and
     ranked, each with a deterministic qualification verdict + recommended
     offer from the 5-rung ladder.
  2. ``call_list.md`` — the prioritized "who to contact today" list with
     bilingual talking points + objection notes. **You** make the contact;
     the system never dials, emails, or messages anyone.
  3. ``draft_pack.md`` — ready-to-edit bilingual outreach drafts, each
     pre-screened through the qualification engine. Queued for your approval.
  4. ``scorecard.md`` — today's founder scorecard template.
  5. ``OPERATOR_PACK.md`` — the single index that ties it all together.

Honors the doctrine (enforced by tests):
  - No external send. Every artifact is a file you read, edit, and act on.
  - No scraping. Prospects come from the CSV you control (a clearly-labelled
    sample seed ships so the command runs out-of-the-box on a fresh clone).
  - No guaranteed outcomes / no invented metrics. Estimates are labelled.
  - Every recommended action carries a ``governance_decision`` and the
    bilingual disclaimer.

Usage:
    python scripts/dealix_day0.py                      # uses the sample seed
    python scripts/dealix_day0.py --prospects data/prospects.csv
    python scripts/dealix_day0.py --warm-list data/warm_list.csv
    python scripts/dealix_day0.py --top 8 --date 2026-06-07
    python scripts/dealix_day0.py --json               # machine-readable summary

Exit codes:
    0  operator pack generated
    1  no prospect rows found (seed missing or empty)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score  # noqa: E402
from auto_client_acquisition.sales_os.qualification import qualify  # noqa: E402

DISCLAIMER = (
    "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة. "
    "Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة."
)

# The 5-rung commercial ladder (priced, wired). Keep in sync with docs/pricing.
OFFER_LADDER = {
    "revenue_intelligence_sprint": (
        "7-Day Revenue Intelligence Sprint",
        "Sprint إيرادات 7 أيام",
        "499 SAR",
    ),
    "data_to_revenue_diagnostic": (
        "Data-to-Revenue Pack",
        "حزمة البيانات إلى الإيراد",
        "1,500 SAR",
    ),
    "data_to_revenue_pack": ("Data-to-Revenue Pack", "حزمة البيانات إلى الإيراد", "1,500 SAR"),
    "capability_diagnostic": ("Free AI Ops Diagnostic", "تشخيص العمليات المجاني", "0 SAR"),
    "managed_revenue_ops": ("Managed Revenue Ops", "تشغيل الإيرادات المُدار", "2,999–4,999 SAR/mo"),
    "refer_out_governance_not_accepted": (
        "Refer out — governance not accepted",
        "إحالة — لم تُقبل الحوكمة",
        "—",
    ),
    "refer_out_not_enough_fit": ("Refer out — insufficient fit", "إحالة — ملاءمة غير كافية", "—"),
    "not_a_fit_decline_politely": (
        "Decline politely — doctrine risk",
        "اعتذار مهذّب — مخالفة دكترين",
        "—",
    ),
}

OWNER_TITLES = {"CEO", "COO", "GM", "FOUNDER", "MD", "VP", "MANAGING PARTNER", "OWNER", "DIRECTOR"}

# Sector → b2b-service fit (0–100). Deterministic, conservative.
SECTOR_FIT = {
    "b2b_services": 92,
    "consulting": 90,
    "agency": 88,
    "saas": 88,
    "it_services": 86,
    "financial_services": 80,
    "logistics": 76,
    "distribution": 74,
    "manufacturing": 70,
    "real_estate": 68,
    "healthcare": 66,
    "retail": 64,
    "education": 62,
    "events": 58,
    "agritech": 60,
}

INBOUND_SOURCES = {"inbound_form", "inbound_whatsapp", "inbound_email", "demo_request"}
WARM_SOURCES = {"warm_intro", "partner_referral", "referral"}


@dataclass(slots=True)
class Prospect:
    name: str
    sector: str
    city: str = ""
    country: str = "SA"
    domain: str = ""
    contact_name: str = ""
    contact_title: str = ""
    source: str = "manual_research"
    locale: str = "ar-SA"
    annual_turnover_sar: int = 0
    notes: str = ""

    @classmethod
    def from_row(cls, row: dict[str, str]) -> Prospect:
        def s(key: str, default: str = "") -> str:
            return (row.get(key) or default).strip()

        turnover_raw = s("annual_turnover_sar", "0").replace(",", "")
        try:
            turnover = int(float(turnover_raw)) if turnover_raw else 0
        except ValueError:
            turnover = 0
        return cls(
            name=s("name"),
            sector=s("sector").lower(),
            city=s("city"),
            country=s("country", "SA"),
            domain=s("domain"),
            contact_name=s("contact_name"),
            contact_title=s("contact_title"),
            source=s("source", "manual_research").lower(),
            locale=s("locale", "ar-SA"),
            annual_turnover_sar=turnover,
            notes=s("notes"),
        )


@dataclass(slots=True)
class ScoredProspect:
    prospect: Prospect
    icp: int
    dimensions: dict[str, int]
    decision: str
    qual_score: int
    recommended_offer: str
    reasons: list[str] = field(default_factory=list)
    doctrine_violations: list[str] = field(default_factory=list)

    @property
    def is_owner(self) -> bool:
        return self.prospect.contact_title.upper() in OWNER_TITLES


# ── Deterministic scoring ───────────────────────────────────────────────────


def _budget_signal(turnover: int) -> int:
    if turnover <= 0:
        return 35
    if turnover < 500_000:
        return 35
    if turnover < 1_000_000:
        return 55
    if turnover < 3_000_000:
        return 75
    if turnover < 7_000_000:
        return 85
    return 90


def _decision_velocity(source: str, is_owner: bool) -> int:
    if source in INBOUND_SOURCES:
        base = 85
    elif source in WARM_SOURCES:
        base = 72
    else:
        base = 40
    if is_owner:
        base += 8
    return min(100, base)


def _governance_posture(country: str, notes: str) -> int:
    base = 62 if country.upper() == "SA" else 50
    hay = notes.lower()
    if any(
        k in hay
        for k in (
            "pdpl",
            "zatca",
            "compliance",
            "governance",
            "audit",
            "data-sensitive",
            "data sensitive",
        )
    ):
        base += 18
    return min(100, base)


def _data_maturity(p: Prospect) -> int:
    base = 40
    if p.domain:
        base += 18
    if p.annual_turnover_sar > 0:
        base += 18
    if p.sector in {"saas", "it_services", "financial_services"}:
        base += 12
    if any(
        k in p.notes.lower()
        for k in ("existing data", "crm", "pipeline", "data-mature", "data mature")
    ):
        base += 10
    return min(100, base)


def derive_dimensions(p: Prospect) -> ICPDimensions:
    is_owner = p.contact_title.upper() in OWNER_TITLES
    return ICPDimensions(
        b2b_service_fit=SECTOR_FIT.get(p.sector, 55),
        data_maturity=_data_maturity(p),
        governance_posture=_governance_posture(p.country, p.notes),
        budget_signal=_budget_signal(p.annual_turnover_sar),
        decision_velocity=_decision_velocity(p.source, is_owner),
    )


def score_prospect(p: Prospect) -> ScoredProspect:
    dims = derive_dimensions(p)
    icp = icp_score(dims)
    is_owner = p.contact_title.upper() in OWNER_TITLES

    verdict = qualify(
        pain_clear=p.source in INBOUND_SOURCES
        or "struggl" in p.notes.lower()
        or "wants" in p.notes.lower(),
        owner_present=is_owner,
        data_available=dims.data_maturity >= 60,
        accepts_governance=True,  # pre-screen assumption; confirmed on the call
        has_budget=dims.budget_signal >= 55,
        wants_safe_methods=True,
        proof_path_visible=True,
        retainer_path_visible=dims.budget_signal >= 75,
        raw_request_text=p.notes,
        sector=p.sector,
        city=p.city,
    )
    return ScoredProspect(
        prospect=p,
        icp=icp,
        dimensions=asdict(dims),
        decision=verdict.decision,
        qual_score=verdict.score,
        recommended_offer=verdict.recommended_offer,
        reasons=list(verdict.reasons),
        doctrine_violations=list(verdict.doctrine_violations),
    )


# ── Talking points ──────────────────────────────────────────────────────────

DECISION_BADGE = {
    "accept": "✅ accept — reach out today",
    "diagnostic_only": "🔵 diagnostic-only — lead with the free diagnostic",
    "reframe": "🟡 reframe — book a short scope call",
    "reject": "🔴 reject — doctrine risk, decline politely",
    "refer_out": "⚪ refer-out — not enough fit",
}


def _offer_label(key: str) -> str:
    en, ar, price = OFFER_LADDER.get(key, (key, key, "—"))
    return f"{en} / {ar} · {price}"


def talking_points(sp: ScoredProspect) -> tuple[list[str], list[str]]:
    p = sp.prospect
    offer_en, offer_ar, price = OFFER_LADDER.get(
        sp.recommended_offer, (sp.recommended_offer, sp.recommended_offer, "—")
    )
    ar = [
        f"الافتتاح: «لاحظت أن {p.name} في قطاع {p.sector} — نساعد شركات مثلكم على ترتيب الفرص وتنظيف البيانات تحت حوكمة AI واضحة.»",
        f"الربط بالألم: استند إلى ملاحظتك ({p.notes or 'تحديات متابعة العملاء'}).",
        f"العرض المقترح: {offer_ar} ({price}) — ابدأ صغير، أثبت القيمة، بدون وعود.",
        "الحوكمة كميزة: لا scraping، لا رسائل باردة، موافقتك قبل أي إجراء خارجي + Proof Pack.",
        "الخطوة التالية: احجز 20 دقيقة، أو ابدأ بالتشخيص المجاني خلال 24 ساعة.",
    ]
    en = [
        f"Open: “I noticed {p.name} in {p.sector} — we help similar Saudi B2B teams rank opportunities and clean their data under explicit AI governance.”",
        f"Tie to pain: anchor on your note ({p.notes or 'lead follow-up gaps'}).",
        f"Recommend: {offer_en} ({price}) — start small, prove value, no promises.",
        "Governance as the edge: no scraping, no cold messaging, your approval before any external action + a Proof Pack.",
        "Next step: book 20 minutes, or start the free 24h diagnostic.",
    ]
    if sp.decision in ("reject", "refer_out"):
        ar = ["هذا المُرشّح غير ملائم الآن — اعتذر بلطف أو أحِله لشريك. لا تتابع."]
        en = ["Not a fit right now — decline politely or refer to a partner. Do not pursue."]
    return ar, en


# ── Renderers ───────────────────────────────────────────────────────────────


def _gov_block(decision_summary: str) -> str:
    return (
        "> **governance_decision:** `internal_artifact` · no external action taken · "
        f"{decision_summary}\n>\n> _{DISCLAIMER}_\n"
    )


def render_prospects_md(scored: list[ScoredProspect], generated: str) -> str:
    lines = [
        "# Prospect shortlist — قائمة العملاء المحتملين (مُقيّمة ومرتّبة)\n",
        f"_Generated: {generated}_\n",
        (
            "\n> **Source:** the prospect CSV you control. The shipped seed is a "
            "clearly-labelled **SAMPLE** — replace it with your real list "
            "(`data/prospects.csv`). No data was scraped.\n"
        ),
        _gov_block("ranking is a deterministic estimate from the fields you provided"),
        "\n| # | Company | Sector | City | ICP | Verdict | Recommended offer |\n",
        "|---|---|---|---|---|---|---|\n",
    ]
    for i, sp in enumerate(scored, 1):
        p = sp.prospect
        lines.append(
            f"| {i} | {p.name} | {p.sector} | {p.city or '—'} | **{sp.icp}** | "
            f"{sp.decision} | {_offer_label(sp.recommended_offer)} |\n"
        )
    lines.append("\n## Dimension detail\n")
    for i, sp in enumerate(scored, 1):
        d = sp.dimensions
        lines.append(
            f"\n**{i}. {sp.prospect.name}** — ICP **{sp.icp}/100** · qual {sp.qual_score}/100 · "
            f"`{sp.decision}`\n"
            f"- fit={d['b2b_service_fit']} · data={d['data_maturity']} · "
            f"gov={d['governance_posture']} · budget={d['budget_signal']} · "
            f"velocity={d['decision_velocity']}\n"
            f"- reasons: {', '.join(sp.reasons) or '—'}\n"
        )
        if sp.doctrine_violations:
            lines.append(f"- ⚠ doctrine: {', '.join(sp.doctrine_violations)}\n")
    lines.append(f"\n---\n_{DISCLAIMER}_\n")
    return "".join(lines)


def render_prospects_csv(scored: list[ScoredProspect], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank",
                "name",
                "sector",
                "city",
                "contact_name",
                "contact_title",
                "icp_score",
                "qualification_score",
                "decision",
                "recommended_offer",
                "b2b_service_fit",
                "data_maturity",
                "governance_posture",
                "budget_signal",
                "decision_velocity",
                "source",
            ]
        )
        for i, sp in enumerate(scored, 1):
            p, d = sp.prospect, sp.dimensions
            w.writerow(
                [
                    i,
                    p.name,
                    p.sector,
                    p.city,
                    p.contact_name,
                    p.contact_title,
                    sp.icp,
                    sp.qual_score,
                    sp.decision,
                    sp.recommended_offer,
                    d["b2b_service_fit"],
                    d["data_maturity"],
                    d["governance_posture"],
                    d["budget_signal"],
                    d["decision_velocity"],
                    p.source,
                ]
            )


def render_call_list_md(scored: list[ScoredProspect], top: int, generated: str) -> str:
    actionable = [s for s in scored if s.decision in ("accept", "diagnostic_only", "reframe")][:top]
    lines = [
        "# Today's call list — قائمة الاتصال اليوم\n",
        f"_Generated: {generated}_\n",
        (
            "\n> **You make every contact.** This is a prioritized list with talking "
            "points. The system never dials, emails, or messages anyone. "
            "هذه قائمة أولويات بنقاط حوار — أنت من يتواصل.\n"
        ),
        _gov_block(
            "contact prioritization is an estimate; the founder approves and executes every touch"
        ),
        f"\nTop {len(actionable)} of {len(scored)} prospects, ranked by ICP fit.\n",
    ]
    for i, sp in enumerate(actionable, 1):
        p = sp.prospect
        ar_points, en_points = talking_points(sp)
        lines.append(
            f"\n## {i}. {p.name} — {p.contact_title or 'contact'} "
            f"({p.contact_name or '—'})\n"
            f"- **ICP {sp.icp}/100** · {DECISION_BADGE.get(sp.decision, sp.decision)}\n"
            f"- Sector `{p.sector}` · City `{p.city or '—'}` · Source `{p.source}`\n"
            f"- Recommended: **{_offer_label(sp.recommended_offer)}**\n"
            f"- Channel: < LinkedIn DM / phone / email — your call >\n\n"
            "### نقاط الحوار (عربي)\n"
        )
        for pt in ar_points:
            lines.append(f"  - {pt}\n")
        lines.append("\n### Talking points (English)\n")
        for pt in en_points:
            lines.append(f"  - {pt}\n")
        lines.append("\n- Contacted: [ ]  · Reply: [ ]  · Booked: [ ]  · Next: ____\n\n---\n")
    if not actionable:
        lines.append("\n_No actionable prospects in this batch — add real rows to your CSV._\n")
    lines.append(f"\n_{DISCLAIMER}_\n")
    return "".join(lines)


def render_scorecard_md(generated: str, date_str: str, n_actionable: int) -> str:
    return (
        "# Founder daily scorecard — السجل اليومي للمؤسس\n"
        f"_Generated: {generated}_\n\n"
        f"- Date: {date_str}\n"
        "- Segment focus today:        ____\n"
        f"- Prospects queued for contact: {n_actionable}\n"
        "- Messages sent:               ____ / 5\n"
        "- Replies received:            ____\n"
        "- Diagnostics booked:          ____\n"
        "- Diagnostics held:            ____\n"
        "- Sprints cleared (499 SAR):   ____\n"
        "- Managed Ops signed:          ____\n"
        "- Cash received today (SAR):   ____\n"
        "- Hours building:              ____\n"
        "- Tomorrow's 5 targets:        ____\n\n"
        f"{_gov_block('scorecard is a self-reported template; fill it at 18:00 KSA')}\n"
        f"_{DISCLAIMER}_\n"
    )


def render_operator_pack_md(date_str: str, generated: str, counts: dict, files: list[str]) -> str:
    return (
        f"# Dealix — Operator Pack · حزمة المُشغّل · {date_str}\n\n"
        f"_Generated: {generated}_\n\n"
        "**One command stood the day up.** Work this pack top-to-bottom. "
        "Nothing here was sent externally — every artifact is yours to review, "
        "edit, and act on. أمر واحد جهّز يومك — راجع، عدّل، ونفّذ.\n\n"
        "## Today at a glance\n"
        f"- Prospects scored: **{counts['total']}**\n"
        f"- Actionable (accept / diagnostic / reframe): **{counts['actionable']}**\n"
        f"- Accept now: **{counts['accept']}** · Diagnostic-first: "
        f"**{counts['diagnostic']}** · Refer-out / decline: **{counts['declined']}**\n\n"
        "## Run this pack in order\n"
        "1. **`prospects.md`** — review the ranked shortlist + why each scored as it did.\n"
        "2. **`call_list.md`** — your contact list for today with bilingual talking points.\n"
        "3. **`draft_pack.md`** — edit the pre-screened outreach drafts, then send them *yourself*.\n"
        "4. **`scorecard.md`** — fill at 18:00 KSA; paste into your daily log.\n\n"
        "## Files\n" + "".join(f"- `{f}`\n" for f in files) + "\n## Doctrine reminders\n"
        "- No external action without **your** approval (rung 8).\n"
        "- No guaranteed outcomes, no invented metrics (rungs 4, 5).\n"
        "- No scraping, no cold WhatsApp/LinkedIn automation (rungs 1–3).\n"
        "- The 5-rung ladder: Free Diagnostic → 499 Sprint → 1,500 Data Pack → "
        "2,999–4,999/mo Managed Ops → 5K–25K Custom AI.\n\n"
        f"{_gov_block('operator pack assembled from internal deterministic engines')}\n"
        f"_{DISCLAIMER}_\n"
    )


# ── Draft pack (reuse warm_list_outreach renderer) ──────────────────────────


def _warm_list_drafts(rows: list[dict[str, str]]) -> str | None:
    """Render warm-list drafts via the dedicated generator; None if unavailable."""
    try:
        from scripts.warm_list_outreach import _qualify_contact, _render_contact
    except Exception:
        return None
    parts = []
    for r in rows:
        q = _qualify_contact(
            role=r.get("role", ""),
            sector=r.get("sector", ""),
            relationship=r.get("relationship", "cold"),
            notes=r.get("notes", ""),
        )
        parts.append(_render_contact(r, q))
    return "".join(parts)


def render_draft_pack(
    scored: list[ScoredProspect], warm_list_path: Path | None, generated: str
) -> str:
    """Generate the outreach draft pack.

    Prefers a founder-maintained warm list; otherwise derives drafts from the
    actionable prospects so the pack is never empty on a fresh clone.
    """
    header = [
        "# Outreach draft pack — حزمة المسوّدات\n",
        f"_Generated: {generated}_\n",
        (
            "\n> Each draft is **queued for your approval** — copy/edit, then send "
            "yourself. The system sends nothing. كل مسوّدة بانتظار موافقتك.\n"
        ),
        _gov_block(
            "drafts are pre-screened estimates; the founder approves and sends every message"
        ),
        "\n---\n\n",
    ]

    rows: list[dict[str, str]] = []
    if warm_list_path and warm_list_path.exists():
        with warm_list_path.open("r", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if (r.get("name") or "").strip()]

    if rows:
        warm = _warm_list_drafts(rows)
        if warm is not None:
            return "".join(header) + warm + f"\n_{DISCLAIMER}_\n"

    # Fall back to prospect-derived drafts (actionable only).
    actionable = [s for s in scored if s.decision in ("accept", "diagnostic_only", "reframe")]
    body = []
    for sp in actionable:
        p = sp.prospect
        offer_en, offer_ar, price = OFFER_LADDER.get(
            sp.recommended_offer, (sp.recommended_offer, "", "—")
        )
        ar = (
            f"السلام عليكم {p.contact_name or 'فريق ' + p.name}،\n\n"
            f"نساعد شركات B2B سعودية في قطاع {p.sector} على ترتيب الفرص وتنظيف "
            "البيانات وتجهيز رسائل عربية — تحت حوكمة AI واضحة (لا scraping، لا "
            "رسائل باردة، لا وعود).\n\n"
            f"المقترح لكم: {offer_ar} ({price}). نبدأ صغير ونثبت القيمة عبر Proof Pack.\n\n"
            "هل نحجز 20 دقيقة هذا الأسبوع؟"
        )
        en = (
            f"Hi {p.contact_name or p.name + ' team'},\n\n"
            f"We help Saudi B2B companies in {p.sector} rank opportunities, clean "
            "data, and prepare Arabic outreach — under explicit AI governance "
            "(no scraping, no cold messaging, no promises).\n\n"
            f"Suggested for you: {offer_en} ({price}). We start small and prove "
            "value with a Proof Pack.\n\n"
            "Could we book 20 minutes this week?"
        )
        body.append(
            f"## {p.name} — {p.contact_title or 'contact'}\n"
            f"- Pre-screen: {DECISION_BADGE.get(sp.decision, sp.decision)} · ICP {sp.icp}/100\n"
            f"- Recommended: {_offer_label(sp.recommended_offer)}\n\n"
            f"### Arabic (primary)\n```\n{ar}\n```\n\n"
            f"### English (secondary)\n```\n{en}\n```\n\n"
            "- Channel: < choose >  · Sent: [ ]  · Replied: [ ]\n\n---\n\n"
        )
    note = (
        ""
        if rows
        else "\n> _Tip: fill `data/warm_list.csv` (from the template) for richer, "
        "relationship-aware drafts._\n"
    )
    return "".join(header) + "".join(body) + note + f"\n_{DISCLAIMER}_\n"


# ── Orchestration ───────────────────────────────────────────────────────────


def load_prospects(path: Path) -> list[Prospect]:
    out: list[Prospect] = []
    with path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row.get("name") or "").strip():
                out.append(Prospect.from_row(row))
    return out


def run_day0(
    prospects_path: Path,
    out_dir: Path,
    warm_list_path: Path | None,
    top: int,
    date_str: str,
) -> dict:
    prospects = load_prospects(prospects_path)
    if not prospects:
        return {"ok": False, "error": "no_prospects", "path": str(prospects_path)}

    scored = sorted((score_prospect(p) for p in prospects), key=lambda s: s.icp, reverse=True)
    generated = datetime.now(UTC).isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    counts = {
        "total": len(scored),
        "accept": sum(1 for s in scored if s.decision == "accept"),
        "diagnostic": sum(1 for s in scored if s.decision == "diagnostic_only"),
        "reframe": sum(1 for s in scored if s.decision == "reframe"),
        "declined": sum(1 for s in scored if s.decision in ("reject", "refer_out")),
    }
    counts["actionable"] = counts["accept"] + counts["diagnostic"] + counts["reframe"]

    (out_dir / "prospects.md").write_text(render_prospects_md(scored, generated), encoding="utf-8")
    render_prospects_csv(scored, out_dir / "prospects.csv")
    (out_dir / "call_list.md").write_text(
        render_call_list_md(scored, top, generated), encoding="utf-8"
    )
    (out_dir / "draft_pack.md").write_text(
        render_draft_pack(scored, warm_list_path, generated), encoding="utf-8"
    )
    (out_dir / "scorecard.md").write_text(
        render_scorecard_md(generated, date_str, counts["actionable"]), encoding="utf-8"
    )

    files = ["prospects.md", "prospects.csv", "call_list.md", "draft_pack.md", "scorecard.md"]
    (out_dir / "OPERATOR_PACK.md").write_text(
        render_operator_pack_md(date_str, generated, counts, files), encoding="utf-8"
    )

    return {"ok": True, "out_dir": str(out_dir), "counts": counts, "generated": generated}


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Day-0 Company Activation")
    parser.add_argument(
        "--prospects", default="", help="Prospect CSV (default: data/prospects.csv or seed)"
    )
    parser.add_argument(
        "--warm-list", default="data/warm_list.csv", help="Optional warm-list CSV for drafts"
    )
    parser.add_argument("--out-dir", default="", help="Output dir (default: data/day0/<date>)")
    parser.add_argument("--top", type=int, default=8, help="How many to put on the call list")
    parser.add_argument("--date", default="", help="Date stamp YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--json", action="store_true", help="Print machine-readable summary")
    args = parser.parse_args()

    date_str = args.date or datetime.now(UTC).strftime("%Y-%m-%d")

    if args.prospects:
        prospects_path = REPO_ROOT / args.prospects
    else:
        real = REPO_ROOT / "data" / "prospects.csv"
        prospects_path = real if real.exists() else REPO_ROOT / "data" / "prospects.seed.csv"

    if not prospects_path.exists():
        print(f"❌ Prospect CSV not found: {prospects_path}")
        print("   Copy the seed:  cp data/prospects.seed.csv data/prospects.csv")
        return 1

    out_dir = REPO_ROOT / (args.out_dir or f"data/day0/{date_str}")
    warm_list_path = REPO_ROOT / args.warm_list if args.warm_list else None

    result = run_day0(prospects_path, out_dir, warm_list_path, args.top, date_str)

    if not result.get("ok"):
        print(f"⚠ {result.get('error')}: {result.get('path')}")
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    c = result["counts"]
    using_seed = prospects_path.name == "prospects.seed.csv"
    print("✓ Dealix Day-0 operator pack generated")
    print(
        f"  source     : {prospects_path.relative_to(REPO_ROOT)}"
        + ("  (SAMPLE seed — replace with your real list)" if using_seed else "")
    )
    print(f"  out dir    : {Path(result['out_dir']).relative_to(REPO_ROOT)}")
    print(f"  prospects  : {c['total']} scored")
    print(
        f"  actionable : {c['actionable']} (accept={c['accept']}, diagnostic={c['diagnostic']}, reframe={c['reframe']})"
    )
    print(f"  declined   : {c['declined']} (refer-out / decline)")
    print(f"  → open     : {Path(result['out_dir']).relative_to(REPO_ROOT)}/OPERATOR_PACK.md")
    print(f"  {DISCLAIMER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
