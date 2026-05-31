"""
Canonical entity-data schemas — keep AI-search consumers consistent.
"""

from __future__ import annotations

from dealix.hermes.growth.entity_data.company_profile_schema import (
    CompanyProfile,
    company_profile_jsonld,
)
from dealix.hermes.growth.entity_data.faq_schema import FAQItem, faq_jsonld
from dealix.hermes.growth.entity_data.offer_schema import OfferEntity, offer_jsonld
from dealix.hermes.growth.entity_data.product_schema import (
    ProductEntity,
    product_jsonld,
)
from dealix.hermes.growth.entity_data.review_schema import ReviewEntity, review_jsonld
from dealix.hermes.growth.entity_data.source_consistency import (
    SourceConsistencyReport,
    check_source_consistency,
)

__all__ = [
    "CompanyProfile",
    "company_profile_jsonld",
    "ProductEntity",
    "product_jsonld",
    "OfferEntity",
    "offer_jsonld",
    "FAQItem",
    "faq_jsonld",
    "ReviewEntity",
    "review_jsonld",
    "SourceConsistencyReport",
    "check_source_consistency",
]
