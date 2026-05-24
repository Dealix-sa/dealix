"""Canonical Offer Library — the externally visible catalog."""

from __future__ import annotations

from dealix.hermes.products.offer_builder import OfferBuilder


def default_offers() -> list[dict]:
    b = OfferBuilder()
    return [
        b.build(
            offer="AI Trust Kit",
            buyer="Companies using AI internally",
            pain="No permissions, approvals, or audit trail",
            promise="Govern AI usage with clear controls",
            deliverables=[
                "AI use policy",
                "Agent registry",
                "Tool permission matrix",
                "Approval workflow",
                "Evidence pack template",
            ],
            price_range_sar="5,000-25,000",
            delivery_time="7-14 days",
            upsell="AI Governance OS monthly",
            outcome_metric="approved governance workflow",
        ).as_dict(),
        b.build(
            offer="Revenue Hunter Pilot",
            buyer="Founders selling B2B services",
            pain="Inconsistent outbound and lost opportunities",
            promise="Qualified pipeline in 7 days",
            deliverables=[
                "Opportunity inbox",
                "Drafted outreach",
                "Follow-up sequence",
                "Pricing recommendation",
            ],
            price_range_sar="2,999-9,999",
            delivery_time="7 days",
            upsell="Managed Revenue Ops monthly",
            outcome_metric="qualified opportunities delivered",
        ).as_dict(),
        b.build(
            offer="Agency White-label Kit",
            buyer="Agencies serving B2B clients",
            pain="No AI offer for their book of business",
            promise="Resell AI services under your brand",
            deliverables=[
                "White-label pitch template",
                "Pricing playbook",
                "Delivery playbook",
                "Revenue-share addendum",
            ],
            price_range_sar="9,999-25,000",
            delivery_time="14 days",
            upsell="Managed delivery share",
            outcome_metric="white-label revenue share signed",
        ).as_dict(),
        b.build(
            offer="AI Governance Training Workshop",
            buyer="Managers using AI in operations",
            pain="No common language for AI risk",
            promise="Aligned policy and prompts in one workshop",
            deliverables=[
                "Slides",
                "Worksheet",
                "Policy template",
                "Prompt pack",
            ],
            price_range_sar="5,000-15,000",
            delivery_time="3 days",
            upsell="AI Trust Kit",
            outcome_metric="signed policy + 5 vetted prompts",
        ).as_dict(),
    ]
