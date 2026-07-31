"""Canonical Company Intelligence contracts and compatibility adapters."""

from dealix.company_intelligence.company_brain import (
    CanonicalCompanyBrain,
    build_customer_company_brain,
    build_internal_company_brain,
)
from dealix.company_intelligence.contracts import CompanyBrainSource, ProvenanceRef
from dealix.company_intelligence.execution_contracts import (
    CanonicalApproval,
    CanonicalDraft,
    CanonicalOpportunity,
    DraftChannel,
    LawfulContactBasis,
    build_draft,
    normalize_approval,
    normalize_opportunity,
)

__all__ = [
    "CanonicalApproval",
    "CanonicalCompanyBrain",
    "CanonicalDraft",
    "CanonicalOpportunity",
    "CompanyBrainSource",
    "DraftChannel",
    "LawfulContactBasis",
    "ProvenanceRef",
    "build_customer_company_brain",
    "build_draft",
    "build_internal_company_brain",
    "normalize_approval",
    "normalize_opportunity",
]
