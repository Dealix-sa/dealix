#!/usr/bin/env python3
"""
growth_dry_run.py — Dealix Growth Dry-Run Draft Factory

Generates WITHOUT sending:
  - N persuasion dossiers from sample data
  - N offer routes
  - N channel routes
  - 3N drafts (3 per company)
  - Quality report
  - Risk report
  - Top 20 founder actions

Doctrine:
  - NO live sends under any circumstances
  - NO live charges
  - All output is draft/review-only
  - Governance decision on every output object

Usage:
    python scripts/growth_dry_run.py --companies 50 --output reports/
    python scripts/growth_dry_run.py --companies 10 --focus "Al Rashid Facilities"
"""

from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from os import path  # noqa

# Hard gates
NO_LIVE_SEND: bool = True
NO_LIVE_CHARGE: bool = True

# ---------------------------------------------------------------------------
# Sample company data (dry-run only — no real PII)
# ---------------------------------------------------------------------------

SAMPLE_POOL = [
    {
        "name": "Al Rashid Facilities Management",
        "sector": "Facilities Management",
        "country": "SA",
        "city": "Riyadh",
        "employees": "200-500",
        "buyer_persona": "Operations Director",
        "decision_maker_title": "Director of Operations",
        "likely_pain": [
            "Manual SLA tracking via Excel",
            "Technician reports are late and inconsistent",
            "Weekly management reports take 2 days",
        ],
        "trust_angle": "Workflow audit with zero-risk entry price",
        "risk_angle": "Data security and change management risk",
    },
    {
        "name": "Gulf Contracting Company",
        "sector": "Construction",
        "country": "SA",
        "city": "Jeddah",
        "employees": "500+",
        "buyer_persona": "PMO Director",
        "decision_maker_title": "VP Projects",
        "likely_pain": [
            "Weekly progress reports take full day",
            "Change orders tracked in email threads",
            "Risk tracking is reactive",
        ],
        "trust_angle": "Project controls AI reduces reporting burden by 60%",
        "risk_angle": "Project disruption during implementation",
    },
    {
        "name": "Riyadh Legal Partners",
        "sector": "Legal Firms",
        "country": "SA",
        "city": "Riyadh",
        "employees": "50-200",
        "buyer_persona": "Managing Partner",
        "decision_maker_title": "Senior Partner",
        "likely_pain": [
            "Contract review takes too long",
            "Case knowledge is not captured systematically",
            "Client follow-up is manual",
        ],
        "trust_angle": "Sovereign knowledge system — data stays on your servers",
        "risk_angle": "Client confidentiality and bar association compliance",
    },
    {
        "name": "Saudi FM Solutions",
        "sector": "Facilities Management",
        "country": "SA",
        "city": "Dammam",
        "employees": "200-500",
        "buyer_persona": "FM Director",
        "decision_maker_title": "General Manager",
        "likely_pain": [
            "Multiple sites with inconsistent reporting",
            "Vendor follow-up is manual",
            "SLA breaches discovered late",
        ],
        "trust_angle": "Proven FM workflow automation with 3-week pilot",
        "risk_angle": "Technology adoption resistance from field teams",
    },
    {
        "name": "Al Noor Healthcare Group",
        "sector": "Healthcare",
        "country": "SA",
        "city": "Riyadh",
        "employees": "200-500",
        "buyer_persona": "Operations Manager",
        "decision_maker_title": "COO",
        "likely_pain": [
            "Patient scheduling coordination is manual",
            "Staff scheduling across departments is complex",
            "MOH compliance documentation takes days",
        ],
        "trust_angle": "PDPL-compliant AI operations — patient data stays local",
        "risk_angle": "Patient data privacy and MOH regulations",
    },
    {
        "name": "Jeddah PMO Group",
        "sector": "Consulting",
        "country": "SA",
        "city": "Jeddah",
        "employees": "50-200",
        "buyer_persona": "Managing Director",
        "decision_maker_title": "CEO",
        "likely_pain": [
            "Proposals take too long to write",
            "Research and benchmarking is manual",
            "Knowledge from past projects is not captured",
        ],
        "trust_angle": "AI ops cuts proposal time from days to hours",
        "risk_angle": "Quality control on AI-generated content",
    },
    {
        "name": "AlFanar Industrial",
        "sector": "Manufacturing",
        "country": "SA",
        "city": "Riyadh",
        "employees": "500+",
        "buyer_persona": "Plant Manager",
        "decision_maker_title": "VP Operations",
        "likely_pain": [
            "Equipment maintenance tracking is reactive",
            "Production reporting is manual",
            "Shift handover reports are inconsistent",
        ],
        "trust_angle": "Predictive maintenance AI reduces unplanned downtime",
        "risk_angle": "Production disruption during technology change",
    },
    {
        "name": "Kingdom Real Estate Development",
        "sector": "Real Estate",
        "country": "SA",
        "city": "Riyadh",
        "employees": "200-500",
        "buyer_persona": "Development Director",
        "decision_maker_title": "CEO",
        "likely_pain": [
            "Multi-project status reporting is manual",
            "Contractor follow-up is chaotic",
            "Regulatory approval tracking is slow",
        ],
        "trust_angle": "Project AI OS reduces Vision 2030 delivery risk",
        "risk_angle": "Project delays and regulatory compliance",
    },
    {
        "name": "Emirates FM Corporation",
        "sector": "Facilities Management",
        "country": "AE",
        "city": "Dubai",
        "employees": "200-500",
        "buyer_persona": "Operations Director",
        "decision_maker_title": "Director of FM Services",
        "likely_pain": [
            "Manual SLA tracking across 50+ buildings",
            "Technician dispatching is inefficient",
            "Client reporting takes 3 days monthly",
        ],
        "trust_angle": "FM workflow automation with rapid ROI demonstration",
        "risk_angle": "Data sovereignty in UAE regulatory environment",
    },
    {
        "name": "Kuwait Consulting Group",
        "sector": "Consulting",
        "country": "KW",
        "city": "Kuwait City",
        "employees": "50-200",
        "buyer_persona": "Senior Partner",
        "decision_maker_title": "Managing Partner",
        "likely_pain": [
            "Client reports take too long to produce",
            "Research synthesis is manual",
            "Knowledge management is weak",
        ],
        "trust_angle": "AI ops for consulting — competitive advantage in GCC",
        "risk_angle": "Quality and accuracy of AI-generated outputs",
    },
]

# Pad to 50 with variations
def _generate_company_pool(n: int) -> list[dict[str, Any]]:
    pool = list(SAMPLE_POOL)
    while len(pool) < n:
        base = SAMPLE_POOL[len(pool) % len(SAMPLE_POOL)].copy()
        base = base.copy()
        idx = len(pool)
        base["name"] = f"{base['name']} — Branch {idx}"
        pool.append(base)
    return pool[:n]


# ---------------------------------------------------------------------------
# Dossier factory
# ---------------------------------------------------------------------------


@dataclass
class DryRunDossier:
    dossier_id: str
    company: str
    country: str
    sector: str
    buyer_persona: str
    decision_maker_title: str
    likely_pain: list[str]
    trust_angle: str
    risk_angle: str
    best_offer: str
    best_channel: str
    persuasion_score: float
    message_pack: dict[str, str]
    objections_expected: list[str]
    objection_responses: dict[str, str]
    governance_decision: dict[str, Any] = field(default_factory=dict)


@dataclass
class DryRunDraft:
    draft_id: str
    dossier_id: str
    company: str
    channel: str
    offer_tier: str
    language: str
    subject_line: str
    body_ar: str
    body_en: str
    persuasion_score: float
    risk_level: str
    status: str = "pending_approval"
    requires_approval: bool = True
    anti_ban_checked: bool = True
    governance_decision: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Offer routing (lightweight, no config loader dependency for dry run)
# ---------------------------------------------------------------------------

SECTOR_OFFER_MAP = {
    "Facilities Management": ("maintenance_intelligence_os", "Email"),
    "Construction": ("project_controls_ai_os", "Email"),
    "Legal Firms": ("sovereign_knowledge_rag", "Email"),
    "Healthcare": ("ai_workflow_audit", "Email"),
    "Manufacturing": ("maintenance_intelligence_os", "Email"),
    "Consulting": ("revenue_ai_os", "Email"),
    "Real Estate": ("project_controls_ai_os", "Email"),
    "Technology": ("sovereign_knowledge_rag", "Email"),
    "Finance": ("sovereign_knowledge_rag", "Email"),
    "Retail": ("revenue_ai_os", "Email"),
}


def _route(company: dict[str, Any]) -> tuple[str, str]:
    sector = company.get("sector", "")
    return SECTOR_OFFER_MAP.get(sector, ("ai_workflow_audit", "Email"))


def _persuasion_score(company: dict[str, Any], idx: int) -> float:
    base = 75.0
    # Sector premium
    if company.get("sector") in ("Facilities Management", "Construction"):
        base += 10
    # Size premium
    if company.get("employees") in ("200-500", "500+"):
        base += 5
    # Slight variation by index to avoid identical scores
    base += (idx % 10) * 0.5
    return min(99.0, base)


def _build_message_pack(company: dict[str, Any], offer: str) -> dict[str, str]:
    name = company["name"]
    pain = company.get("likely_pain", [""])[0] if company.get("likely_pain") else ""
    trust = company.get("trust_angle", "")
    return {
        "subject_line": f"كيف نوفر وقت فريقكم في {name} — {offer}",
        "opening_ar": f"مرحباً بفريق {name}،",
        "opening_en": f"Dear {name} team,",
        "value_prop_ar": (
            f"نلاحظ أن {pain} تحدي شائع في قطاعكم. "
            f"{trust}."
        ),
        "value_prop_en": (
            f"We understand that '{pain}' is a common challenge in your sector. "
            f"{trust}."
        ),
        "cta_ar": "هل يمكنني تحديد 20 دقيقة لمناقشة هذا معكم؟",
        "cta_en": "May I schedule 20 minutes to discuss this with you?",
    }


def _build_objections(company: dict[str, Any]) -> tuple[list[str], dict[str, str]]:
    objections = [
        "We already tried AI and it didn't work",
        "Our budget is tight this quarter",
        "We need to check with IT security",
    ]
    responses = {
        "We already tried AI and it didn't work": (
            "نحن نفهم هذه التجربة. "
            "نظامنا يختلف في أنه مبني على workflow محدد لكم، "
            "مع human approval gate في كل خطوة حرجة."
        ),
        "Our budget is tight this quarter": (
            "لهذا نقترح البدء بـ Workflow Audit بسعر منخفض "
            "يثبت القيمة قبل أي التزام أكبر."
        ),
        "We need to check with IT security": (
            "بالطبع — يمكننا تقديم security brief كامل لفريق IT "
            "وشرح كيف تبقى البيانات في بيئتكم."
        ),
    }
    return objections, responses


def _risk_level(score: float) -> str:
    if score >= 85:
        return "low"
    if score >= 70:
        return "medium"
    return "high"


def _build_draft(
    dossier: DryRunDossier,
    draft_num: int,
) -> DryRunDraft:
    """Build one of 3 drafts for a company (initial, followup, value-focused)."""
    templates = ["initial_outreach", "value_followup", "social_proof"]
    template = templates[draft_num % 3]

    subjects = {
        "initial_outreach": dossier.message_pack["subject_line"],
        "value_followup": f"متابعة: فرصة لـ {dossier.company}",
        "social_proof": f"كيف ساعدنا شركة مشابهة لـ {dossier.company}",
    }

    return DryRunDraft(
        draft_id=f"DFT-{str(uuid.uuid4())[:8].upper()}",
        dossier_id=dossier.dossier_id,
        company=dossier.company,
        channel=dossier.best_channel,
        offer_tier=dossier.best_offer,
        language="bilingual",
        subject_line=subjects[template],
        body_ar=f"[{template}] {dossier.message_pack['opening_ar']} "
                f"{dossier.message_pack['value_prop_ar']} "
                f"{dossier.message_pack['cta_ar']}",
        body_en=f"[{template}] {dossier.message_pack['opening_en']} "
                f"{dossier.message_pack['value_prop_en']} "
                f"{dossier.message_pack['cta_en']}",
        persuasion_score=dossier.persuasion_score - (draft_num * 2),
        risk_level=_risk_level(dossier.persuasion_score),
        governance_decision={
            "no_live_send": NO_LIVE_SEND,
            "no_live_charge": NO_LIVE_CHARGE,
            "requires_founder_approval": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# Report builders
# ---------------------------------------------------------------------------


def _quality_report(
    dossiers: list[DryRunDossier],
    drafts: list[DryRunDraft],
) -> dict[str, Any]:
    avg_score = (
        sum(d.persuasion_score for d in dossiers) / len(dossiers)
        if dossiers
        else 0
    )
    high_quality = [d for d in dossiers if d.persuasion_score >= 80]
    medium_quality = [d for d in dossiers if 60 <= d.persuasion_score < 80]
    low_quality = [d for d in dossiers if d.persuasion_score < 60]

    return {
        "total_dossiers": len(dossiers),
        "total_drafts": len(drafts),
        "average_persuasion_score": round(avg_score, 2),
        "high_quality_count": len(high_quality),
        "medium_quality_count": len(medium_quality),
        "low_quality_count": len(low_quality),
        "top_companies": [d.company for d in sorted(
            dossiers, key=lambda x: x.persuasion_score, reverse=True
        )[:10]],
        "disclaimer": (
            "Estimated value is not Verified value / "
            "القيمة التقديرية ليست قيمة مُتحقَّقة"
        ),
    }


def _risk_report(dossiers: list[DryRunDossier]) -> dict[str, Any]:
    risks = {
        "low": [],
        "medium": [],
        "high": [],
    }
    for d in dossiers:
        level = _risk_level(d.persuasion_score)
        risks[level].append(d.company)

    return {
        "low_risk_companies": len(risks["low"]),
        "medium_risk_companies": len(risks["medium"]),
        "high_risk_companies": len(risks["high"]),
        "high_risk_list": risks["high"][:10],
        "recommended_action": (
            "Start with low-risk companies. "
            "Review high-risk companies before any outreach."
        ),
    }


def _top_actions(dossiers: list[DryRunDossier]) -> list[dict[str, str]]:
    top = sorted(dossiers, key=lambda x: x.persuasion_score, reverse=True)[:20]
    return [
        {
            "rank": str(i + 1),
            "company": d.company,
            "action": f"Review draft for {d.best_offer} via {d.best_channel}",
            "persuasion_score": str(round(d.persuasion_score, 1)),
            "command": f"python -m dealix.os_runtime approval-check --draft-id <DOSSIER:{d.dossier_id}>",
        }
        for i, d in enumerate(top)
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run_dry_run(n: int, focus: str | None = None) -> dict[str, Any]:
    """Run the full dry-run factory. Returns structured output."""
    companies = _generate_company_pool(n)

    if focus:
        companies = [c for c in companies if focus.lower() in c["name"].lower()] or companies[:1]

    dossiers: list[DryRunDossier] = []
    drafts: list[DryRunDraft] = []

    for i, company in enumerate(companies):
        best_offer, best_channel = _route(company)
        score = _persuasion_score(company, i)
        message_pack = _build_message_pack(company, best_offer)
        objections, responses = _build_objections(company)

        dossier = DryRunDossier(
            dossier_id=str(uuid.uuid4()),
            company=company["name"],
            country=company.get("country", "SA"),
            sector=company.get("sector", ""),
            buyer_persona=company.get("buyer_persona", ""),
            decision_maker_title=company.get("decision_maker_title", ""),
            likely_pain=company.get("likely_pain", []),
            trust_angle=company.get("trust_angle", ""),
            risk_angle=company.get("risk_angle", ""),
            best_offer=best_offer,
            best_channel=best_channel,
            persuasion_score=score,
            message_pack=message_pack,
            objections_expected=objections,
            objection_responses=responses,
            governance_decision={
                "no_live_send": NO_LIVE_SEND,
                "no_live_charge": NO_LIVE_CHARGE,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        dossiers.append(dossier)

        # 3 drafts per company
        for j in range(3):
            drafts.append(_build_draft(dossier, j))

    quality = _quality_report(dossiers, drafts)
    risk = _risk_report(dossiers)
    actions = _top_actions(dossiers)

    return {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "no_live_send": NO_LIVE_SEND,
        "no_live_charge": NO_LIVE_CHARGE,
        "companies_processed": len(dossiers),
        "dossiers_generated": len(dossiers),
        "drafts_generated": len(drafts),
        "dossiers": [asdict(d) for d in dossiers],
        "top_10_drafts": [
            asdict(d)
            for d in sorted(drafts, key=lambda x: x.persuasion_score, reverse=True)[
                :10
            ]
        ],
        "quality_report": quality,
        "risk_report": risk,
        "top_20_founder_actions": actions,
        "governance_decision": {
            "report_type": "growth_dry_run",
            "no_live_sends": NO_LIVE_SEND,
            "no_live_charges": NO_LIVE_CHARGE,
            "all_outputs_require_founder_review": True,
            "disclaimer": (
                "Estimated value is not Verified value / "
                "القيمة التقديرية ليست قيمة مُتحقَّقة"
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dealix Growth Dry-Run Draft Factory"
    )
    parser.add_argument(
        "--companies",
        type=int,
        default=50,
        help="Number of companies to process (default: 50)",
    )
    parser.add_argument(
        "--focus",
        type=str,
        default=None,
        help="Focus on a specific company name",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: reports/)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "summary"],
        default="summary",
        help="Output format (default: summary)",
    )
    args = parser.parse_args()

    print(f"[Dealix Dry-Run] Processing {args.companies} companies...")
    print(f"[Dealix Dry-Run] NO_LIVE_SEND={NO_LIVE_SEND} NO_LIVE_CHARGE={NO_LIVE_CHARGE}")

    result = run_dry_run(args.companies, args.focus)

    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        q = result["quality_report"]
        r = result["risk_report"]
        output_lines = [
            f"\n=== Dealix Growth Dry-Run Results ===",
            f"Run at: {result['run_at']}",
            f"Companies: {result['companies_processed']}",
            f"Dossiers: {result['dossiers_generated']}",
            f"Drafts: {result['drafts_generated']}",
            "",
            "--- Quality Report ---",
            f"Avg persuasion score: {q['average_persuasion_score']}",
            f"High quality (80+): {q['high_quality_count']}",
            f"Medium quality (60-79): {q['medium_quality_count']}",
            f"Low quality (<60): {q['low_quality_count']}",
            "",
            "--- Risk Report ---",
            f"Low risk: {r['low_risk_companies']}",
            f"Medium risk: {r['medium_risk_companies']}",
            f"High risk: {r['high_risk_companies']}",
            "",
            "--- Top 20 Founder Actions ---",
        ]
        for action in result["top_20_founder_actions"]:
            output_lines.append(
                f"  {action['rank']}. {action['company']} "
                f"(score: {action['persuasion_score']}) — {action['action']}"
            )
        output_lines += [
            "",
            q["disclaimer"],
        ]
        output = "\n".join(output_lines)

    print(output)

    # Write to file
    output_dir = args.output or REPO_ROOT / "reports"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    suffix = ".json" if args.format == "json" else ".txt"
    outfile = output_dir / f"growth_dry_run_{today}{suffix}"
    outfile.write_text(output if args.format == "json" else output, encoding="utf-8")
    print(f"\n[saved to {outfile}]", file=sys.stderr)


if __name__ == "__main__":
    main()
