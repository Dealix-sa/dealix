"""The seed offer library Dealix ships with.

These are the only offers we are prepared to present externally today. New
offers must go through the Product Factory + sovereign approval before
being added.
"""

from __future__ import annotations

from dealix.hermes.products.offer_builder import OfferCard, OfferKind, OfferLibrary
from dealix.hermes.sovereignty import SovereigntyLevel


DEFAULT_OFFERS: tuple[OfferCard, ...] = (
    OfferCard(
        offer_name="Revenue Hunter Pilot",
        kind=OfferKind.PILOT,
        buyer="Saudi B2B agencies & consultancies (5–50 staff)",
        pain="منيع المبيعات: متابعات ضائعة + عروض غير منتظمة + لا قياس.",
        promise="نُشغّل دورة إيراد محكومة لأسبوعين بإثبات قابل للتحقق.",
        deliverables=[
            "Cash Scout + Money Dashboard configured for the customer",
            "Top-10 cash actions ranked & queued for approval",
            "Proposal Factory templates aligned with their offers",
            "Follow-up cadence drafts (no live send without approval)",
            "Outcome Log + Evidence Pack at end of pilot",
        ],
        floor_price_sar=999,
        ceiling_price_sar=4999,
        delivery_days=14,
        proof_required=True,
        upsell="Managed Revenue Ops retainer",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        sales_channels=["founder_warm_list", "partner_referral"],
        outcome_metric="cash_collected_sar within 14 days",
    ),
    OfferCard(
        offer_name="AI Trust Kit",
        kind=OfferKind.PACKAGE,
        buyer="Companies running AI internally without governance",
        pain="لا صلاحيات، لا موافقات، لا audit trail لاستخدام الـ AI.",
        promise="نُركّب طبقة حوكمة استخدام AI مُوثّقة وقابلة للمراجعة.",
        deliverables=[
            "AI Use Policy",
            "Agent Registry template",
            "Tool Permission Matrix",
            "Approval Workflow",
            "Evidence Pack template",
            "No-overclaim rule sheet",
            "Team Training Mini-session",
        ],
        floor_price_sar=5000,
        ceiling_price_sar=25000,
        delivery_days=14,
        proof_required=True,
        upsell="Agent Governance OS monthly retainer",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        sales_channels=["founder_warm_list", "linkedin_inbound"],
        outcome_metric="policy_adopted_count + first audit pass",
    ),
    OfferCard(
        offer_name="Agency White-label Kit",
        kind=OfferKind.WHITE_LABEL,
        buyer="Agencies wanting to resell governed AI ops to their clients",
        pain="لا منتج جاهز قابل لإعادة البيع تحت اسم الوكالة.",
        promise="نزوّد الوكالة بـ kit يبيعونه كمنتج وكالة محكوم.",
        deliverables=[
            "Re-brandable Money Dashboard + Cash Scout",
            "Proposal templates + Follow-up drafts",
            "Trust Kit lite (policy + permissions)",
            "Onboarding SOP for their CSMs",
            "Revenue share contract template (S3 memo)",
        ],
        floor_price_sar=1000,
        ceiling_price_sar=10000,
        delivery_days=21,
        proof_required=True,
        upsell="Monthly retainer + revenue share",
        sovereignty_level=SovereigntyLevel.S3_SOVEREIGN_MEMO,
        sales_channels=["partner_referral"],
        outcome_metric="agencies_onboarded + first downstream pilot paid",
    ),
    OfferCard(
        offer_name="Founder OS Setup",
        kind=OfferKind.PACKAGE,
        buyer="Saudi founders running ops in their head",
        pain="القرارات تذوب — لا سجل، لا أولوية، لا تتبع.",
        promise="نُركّب Sovereign Console + قوائم القرار اليومية.",
        deliverables=[
            "Sovereign Console snapshot configured",
            "Decision Journal seeded",
            "Daily 90-minute cockpit ritual SOP",
        ],
        floor_price_sar=2000,
        ceiling_price_sar=8000,
        delivery_days=7,
        proof_required=True,
        upsell="Executive PMO Lite retainer",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        sales_channels=["founder_warm_list"],
        outcome_metric="decisions_logged per week",
    ),
    OfferCard(
        offer_name="Market Radar Report",
        kind=OfferKind.REPORT,
        buyer="Sector leaders preparing GTM in KSA",
        pain="غياب رؤية موحّدة عن المنافسين + اللوائح + الفرص.",
        promise="تقرير قطاع موحّد مبني على إشارات سوق علنية.",
        deliverables=[
            "Sector map (players + share heuristics)",
            "Regulation digest with source links",
            "10 ranked opportunities + recommended offers",
        ],
        floor_price_sar=4000,
        ceiling_price_sar=15000,
        delivery_days=10,
        proof_required=True,
        upsell="Monthly Market Radar subscription",
        sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        sales_channels=["founder_warm_list", "partner_referral"],
        outcome_metric="reports_delivered",
    ),
    OfferCard(
        offer_name="Executive PMO Lite",
        kind=OfferKind.RETAINER,
        buyer="Founders & exec teams without PMO discipline",
        pain="مشاريع تتأخر، قرارات تتأجل، لا حوكمة أسبوعية.",
        promise="حوكمة أسبوعية + cadence + قرارات موثّقة.",
        deliverables=[
            "Weekly governance cycle",
            "Decision memos archive",
            "Outcome log + scale/kill verdicts on running bets",
        ],
        floor_price_sar=2999,
        ceiling_price_sar=4999,
        delivery_days=30,
        proof_required=True,
        upsell="Custom AI integration",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        sales_channels=["founder_warm_list"],
        outcome_metric="renewal_rate + decisions_acted_on",
    ),
)


def install_defaults(library: OfferLibrary) -> OfferLibrary:
    for offer in DEFAULT_OFFERS:
        if library.by_name(offer.offer_name) is None:
            library.upsert(offer)
    return library


__all__ = ["DEFAULT_OFFERS", "install_defaults"]
