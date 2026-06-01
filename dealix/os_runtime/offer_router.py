"""
Offer Router
============
Routes a company to the most appropriate Dealix offer based on sector.
"""

# Sector → Offer routing table
ROUTES: dict[str, dict] = {
    "facilities_management": {
        "primary_offer": "maintenance_intelligence_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Operations Director / Facilities Director",
        "pain_angle": "SLA, technician reports, repeated failures",
        "tone": "operational_arabic_formal",
    },
    "maintenance": {
        "primary_offer": "maintenance_intelligence_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Maintenance Manager",
        "pain_angle": "tickets, SLA, field reports",
        "tone": "operational_arabic_formal",
    },
    "contracting": {
        "primary_offer": "project_controls_ai_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Project Director / PMO Director",
        "pain_angle": "progress reporting, approvals, risks",
        "tone": "professional_arabic_formal",
    },
    "legal": {
        "primary_offer": "legal_knowledge_document_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Managing Partner / Head of Legal Operations",
        "pain_angle": "document retrieval, matter summaries, confidentiality",
        "tone": "formal_arabic_conservative",
    },
    "consulting": {
        "primary_offer": "consulting_delivery_intelligence_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Managing Partner / Delivery Director",
        "pain_angle": "proposal reuse, delivery reporting, knowledge reuse",
        "tone": "professional_bilingual",
    },
    "real_estate": {
        "primary_offer": "property_operations_ai_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Operations Manager / Property Manager",
        "pain_angle": "tenant requests, maintenance follow-up, owner reports",
        "tone": "professional_arabic_formal",
    },
    "international": {
        "primary_offer": "gcc_international_ai_pilot",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Regional Operations Director / Country Manager",
        "pain_angle": "Arabic-English workflows, regional reporting, controlled adoption",
        "tone": "professional_english_primary",
    },
    "international_company": {
        "primary_offer": "gcc_international_ai_pilot",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Regional Operations Director / Country Manager",
        "pain_angle": "Arabic-English workflows, regional reporting, controlled adoption",
        "tone": "professional_english_primary",
    },
    "b2b_services": {
        "primary_offer": "revenue_ai_os",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Commercial Director / Sales Director",
        "pain_angle": "lead qualification, follow-up leakage, proposal speed",
        "tone": "commercial_bilingual",
    },
    "accounting": {
        "primary_offer": "accounting_audit_workflow_ai",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Managing Partner / Finance Director",
        "pain_angle": "document checklists, client tracking, compliance workflows",
        "tone": "formal_arabic_conservative",
    },
    "healthcare_admin": {
        "primary_offer": "healthcare_admin_workflow_ai",
        "entry_offer": "ai_workflow_audit",
        "buyer": "Admin Manager / Operations Director",
        "pain_angle": "appointment follow-up, admin routing, non-clinical documents",
        "tone": "professional_arabic_formal",
    },
}

# Default route when sector is unknown
_DEFAULT_ROUTE: dict = {
    "primary_offer": "ai_workflow_audit",
    "entry_offer": "ai_workflow_audit",
    "buyer": "Operations / Digital Transformation / CEO Office",
    "pain_angle": "manual workflows, reporting, follow-up, documents",
    "tone": "professional_bilingual",
}


def _normalize_sector(raw: str) -> str:
    """Normalize sector string to a lookup key."""
    return str(raw or "").lower().strip().replace(" ", "_").replace("-", "_")


def route_offer(company: dict) -> dict:
    """
    Route a company dict to the best offer.

    Args:
        company: dict with at least 'sector' key.
                 Also accepts 'company' or 'name' for display.

    Returns:
        dict with: company, sector, primary_offer, entry_offer, buyer,
                   pain_angle, tone, governance_decision
    """
    sector_raw = company.get("sector", "")
    sector = _normalize_sector(sector_raw)
    route = ROUTES.get(sector, _DEFAULT_ROUTE).copy()

    return {
        "company": company.get("company") or company.get("name") or "",
        "country": company.get("country", ""),
        "sector": sector or "unknown",
        **route,
        "governance_decision": {
            "module": "offer_router",
            "version": "1.0",
            "sector_matched": sector in ROUTES,
            "route_used": sector if sector in ROUTES else "default",
        },
    }


def list_supported_sectors() -> list[str]:
    """Return all sectors with explicit routing rules."""
    return sorted(ROUTES.keys())
