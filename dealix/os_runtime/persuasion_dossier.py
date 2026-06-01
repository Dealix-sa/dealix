"""
Persuasion Dossier
==================
Generates a per-company persuasion intelligence dossier.
Each dossier includes buyer psychology, offer fit, channel fit,
proof asset, objection map, and a scored message pack.
Minimum persuasion score to execute: 82/100.
"""

MIN_SCORE_TO_EXECUTE = 82

SCORING_RUBRIC: dict[str, int] = {
    "company_understanding": 15,
    "pain_clarity": 15,
    "offer_fit": 15,
    "buyer_fit": 10,
    "channel_fit": 10,
    "first_line_strength": 10,
    "risk_reversal": 10,
    "cta_clarity": 5,
    "no_exaggeration": 5,
    "language_fit": 5,
}

SECTOR_PROOF_ASSETS: dict[str, str] = {
    "facilities_management": "SLA dashboard demo showing ticket closure rate improvement",
    "legal": "Document retrieval time reduction with human-approved summaries",
    "contracting": "Progress report generation from site data in under 2 minutes",
    "consulting": "Proposal reuse tool that cuts drafting time by 60%",
    "real_estate": "Tenant request routing and owner report automation",
    "international": "Bilingual Arabic-English workflow pilot with approval gates",
    "accounting": "Client document checklist tracker with deadline alerts",
    "healthcare_admin": "Admin request routing with human handoff on clinical matters",
    "b2b_services": "Lead qualification scoring with follow-up sequence automation",
}

SECTOR_TRUST_ANGLES: dict[str, str] = {
    "legal": "Sample data first. Human lawyer approves all outputs. Full confidentiality.",
    "facilities_management": "Starts with your exported data. No system integration needed in pilot.",
    "international": "Controlled 30-day pilot. Arabic and English. Approval gates on all outputs.",
    "contracting": "Dry-run on historical project data. No live system access until approved.",
}

SECTOR_RISK_ANGLES: dict[str, str] = {
    "legal": "Risk of missing obligation deadlines or delayed matter summaries.",
    "facilities_management": "Risk of SLA breaches going undetected until client escalation.",
    "contracting": "Risk of management having no real-time view of project status.",
    "international": "Risk of regional reporting fragmentation causing decision delays.",
}


def build_dossier(company: dict) -> dict:
    """Build a persuasion dossier for a company profile dict."""
    sector = str(company.get("sector", "")).lower().replace(" ", "_")
    country = str(company.get("country", ""))
    language = company.get("language", "ar" if "saudi" in country.lower() else "en")

    proof_asset = SECTOR_PROOF_ASSETS.get(sector, "AI workflow pilot on sample data")
    trust_angle = SECTOR_TRUST_ANGLES.get(sector, "Sample data first. Human approval on all outputs.")
    risk_angle = SECTOR_RISK_ANGLES.get(sector, "Manual workflows creating delays and errors.")

    score = _compute_score(company, sector, language)
    ready = score >= MIN_SCORE_TO_EXECUTE

    return {
        "company": company.get("company") or company.get("name") or "",
        "country": country,
        "language": language,
        "sector": sector,
        "buyer": company.get("buyer", "Operations Director"),
        "likely_pain": company.get("likely_pain", "Manual workflows and repeated reporting"),
        "trust_angle": trust_angle,
        "risk_angle": risk_angle,
        "proof_asset": proof_asset,
        "best_offer": company.get("best_offer", "ai_workflow_audit"),
        "best_channel": company.get("best_channel", "email"),
        "backup_channels": company.get("backup_channels", ["website_form", "linkedin_assisted"]),
        "objections_expected": company.get("objections_expected", [
            "We already have a system",
            "We are worried about data",
            "Not the right time",
        ]),
        "persuasion_score": score,
        "ready_to_execute": ready,
        "message_pack": _build_message_pack(company, sector, language),
    }


def _compute_score(company: dict, sector: str, language: str) -> int:
    score = 0
    if company.get("company"): score += SCORING_RUBRIC["company_understanding"]
    if company.get("likely_pain"): score += SCORING_RUBRIC["pain_clarity"]
    if company.get("best_offer"): score += SCORING_RUBRIC["offer_fit"]
    if company.get("buyer"): score += SCORING_RUBRIC["buyer_fit"]
    if company.get("best_channel"): score += SCORING_RUBRIC["channel_fit"]
    if company.get("first_line"): score += SCORING_RUBRIC["first_line_strength"]
    if company.get("trust_angle") or sector in SECTOR_TRUST_ANGLES: score += SCORING_RUBRIC["risk_reversal"]
    if company.get("cta"): score += SCORING_RUBRIC["cta_clarity"]
    if not company.get("exaggerated"): score += SCORING_RUBRIC["no_exaggeration"]
    if language in ("ar", "en", "bilingual"): score += SCORING_RUBRIC["language_fit"]
    return min(score, 100)


def _build_message_pack(company: dict, sector: str, language: str) -> dict:
    name = company.get("company") or company.get("name") or "your company"
    pain = company.get("likely_pain") or "manual workflows and repeated reporting"
    offer = company.get("best_offer") or "AI Workflow Audit"

    if language == "ar":
        email = (
            f"السلام عليكم،\n\n"
            f"نعمل مع شركات في قطاع {sector.replace('_', ' ')} على تحويل "
            f"{pain} إلى workflow آلي وسريع.\n\n"
            f"هل يناسبك جلسة قصيرة لعرض كيف يمكن تطبيق ذلك في {name}؟"
        )
    else:
        email = (
            f"Hi,\n\n"
            f"We work with {sector.replace('_', ' ')} companies to automate "
            f"{pain} — starting with a 30-day pilot on sample data.\n\n"
            f"Would a short call to explore how this fits {name} make sense?"
        )

    return {
        "email": email,
        "linkedin": f"Exploring how {sector.replace('_', ' ')} teams handle {pain}. "
                    f"Happy to share what we've seen work — would a quick call make sense?",
        "website_form": f"Interested in {offer} for {sector.replace('_', ' ')} workflow automation.",
        "call_script": (
            f"Quick intro: we help {sector.replace('_', ' ')} teams automate {pain}. "
            f"Curious — how are you currently handling this in {name}?"
        ),
    }
