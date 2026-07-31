"""Canonical Company Intelligence contracts and compatibility adapters."""

from dealix.company_intelligence.company_brain import (
    CanonicalCompanyBrain,
    build_customer_company_brain,
    build_internal_company_brain,
)
from dealix.company_intelligence.contracts import CompanyBrainSource, ProvenanceRef

__all__ = [
    "CanonicalCompanyBrain",
    "CompanyBrainSource",
    "ProvenanceRef",
    "build_customer_company_brain",
    "build_internal_company_brain",
]
