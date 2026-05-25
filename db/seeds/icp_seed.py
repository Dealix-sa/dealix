"""Hermes ICP seeds for Saudi / MENA B2B targets."""

from __future__ import annotations

from typing import Any

ICPS: list[dict[str, Any]] = [
    {
        "icp_id": "agency_owners_saudi",
        "name": "Saudi agency owners",
        "sector": "agencies",
        "company_size_min": 5,
        "company_size_max": 50,
        "geography": "SA",
        "primary_pain": (
            "صعوبة تحويل خدمات الوكالة إلى منتجات قابلة للتكرار "
            "مع إثبات أثر تجاري"
        ),
        "buyer_persona": "Agency founder / managing partner",
        "preferred_channels": ["warm_intro", "founder_email", "referrals"],
    },
    {
        "icp_id": "fintech_b2b_riyadh",
        "name": "Riyadh-based B2B fintech",
        "sector": "fintech",
        "company_size_min": 20,
        "company_size_max": 200,
        "geography": "SA-Riyadh",
        "primary_pain": (
            "الحاجة إلى عمليات مبيعات منضبطة ومتوافقة مع متطلبات "
            "البنك المركزي السعودي"
        ),
        "buyer_persona": "Head of Commercial / Chief Revenue Officer",
        "preferred_channels": ["warm_intro", "founder_email", "events"],
    },
    {
        "icp_id": "healthcare_groups_sa",
        "name": "Saudi healthcare groups",
        "sector": "healthcare",
        "company_size_min": 100,
        "company_size_max": 2000,
        "geography": "SA",
        "primary_pain": (
            "ضعف التكامل بين فرق المبيعات والعمليات السريرية وتراخي "
            "دورة العقود مع شركات التأمين"
        ),
        "buyer_persona": "Group COO / Commercial Director",
        "preferred_channels": ["warm_intro", "founder_email"],
    },
    {
        "icp_id": "contractors_saudi",
        "name": "Saudi contractors and Vision 2030 suppliers",
        "sector": "construction",
        "company_size_min": 50,
        "company_size_max": 1000,
        "geography": "SA",
        "primary_pain": (
            "متابعة فرص العقود الكبرى وإثبات الجدارة التجارية أمام "
            "الجهات الحكومية"
        ),
        "buyer_persona": "Business Development Director",
        "preferred_channels": ["warm_intro", "founder_email", "events"],
    },
    {
        "icp_id": "b2b_saas_mena",
        "name": "B2B SaaS scale-ups across MENA",
        "sector": "saas",
        "company_size_min": 20,
        "company_size_max": 300,
        "geography": "MENA",
        "primary_pain": (
            "Building a defensible commercial motion in a fragmented "
            "regional market without burning runway"
        ),
        "buyer_persona": "Founder / Head of Revenue",
        "preferred_channels": ["warm_intro", "founder_email", "linkedin_personal"],
    },
]


__all__ = ["ICPS"]
