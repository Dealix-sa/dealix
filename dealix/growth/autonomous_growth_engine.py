"""
Autonomous Growth Engine — self-improving revenue and client acquisition system.
Manages the full growth flywheel: lead gen → qualification → conversion → expansion.
Compliant with Dealix doctrine: no cold WhatsApp, no LinkedIn automation, no spam.
"""

from __future__ import annotations

import math
from datetime import date, timedelta
from typing import Any

# Tier LTV multipliers (24-month horizon)
_TIER_LTV: dict[str, float] = {
    "free_diagnostic": 0,
    "sprint_499": 499 * 1.5,
    "data_pack_1500": 1500 * 2,
    "managed_ops": 3500 * 18,  # mid-range × 18 months avg retention
    "custom_ai": 15000 * 1,    # one-time + 20% annual maintenance
}

_SECTOR_WEIGHTS: dict[str, float] = {
    "logistics": 1.2,
    "retail": 1.0,
    "tech": 1.4,
    "food": 0.9,
    "manufacturing": 1.1,
    "services": 1.0,
    "education": 0.8,
    "healthcare": 1.3,
    "real_estate": 1.1,
    "finance": 1.5,
}

_SIZE_WEIGHTS: dict[str, float] = {
    "micro": 0.5,       # 1-9 employees
    "small": 0.8,       # 10-49
    "medium": 1.2,      # 50-249
    "large": 1.5,       # 250+
}

COMPLIANT_CHANNELS = [
    "warm_referral",
    "inbound_web",
    "linkedin_organic_post",
    "email_to_known_contact",
    "whatsapp_to_known_contact",
    "event_follow_up",
    "content_marketing",
    "seo_aeo",
]


class AutonomousGrowthEngine:
    def generate_weekly_targets(self, current_mrr: float, target_mrr: float) -> dict:
        """Return weekly action plan to close the MRR gap."""
        gap = max(0, target_mrr - current_mrr)
        weeks_to_target = 12  # 90-day sprint default

        # Work backwards from the gap
        weekly_gap = gap / weeks_to_target
        avg_deal_value = 1500  # SAR, mid-ladder estimate

        new_deals_per_week = math.ceil(weekly_gap / avg_deal_value)
        leads_needed = math.ceil(new_deals_per_week / 0.20)  # 20% lead→close rate
        outreach_needed = math.ceil(leads_needed / 0.35)  # 35% outreach→lead rate

        actions: list[dict] = []

        if outreach_needed > 0:
            actions.append({
                "priority": 1,
                "action": "warm_outreach",
                "description_ar": f"التواصل مع {min(outreach_needed, 10)} جهة من قائمة الدفء",
                "description_en": f"Reach out to {min(outreach_needed, 10)} warm contacts",
                "channel": "whatsapp_to_known_contact",
                "count": min(outreach_needed, 10),
            })

        actions.append({
            "priority": 2,
            "action": "content_publish",
            "description_ar": "نشر محتوى LinkedIn يعالج نقطة ألم للقطاع المستهدف",
            "description_en": "Publish sector-specific pain point content on LinkedIn",
            "channel": "linkedin_organic_post",
            "count": 2,
        })

        actions.append({
            "priority": 3,
            "action": "follow_up_pipeline",
            "description_ar": "متابعة 100% من الـ leads في مرحلة التفاوض",
            "description_en": "Follow up on 100% of leads in negotiation stage",
            "channel": "warm_referral",
            "count": 1,
        })

        if new_deals_per_week >= 3:
            actions.append({
                "priority": 4,
                "action": "referral_activation",
                "description_ar": "تفعيل برنامج الإحالة — طلب مراجعة من أفضل 3 عملاء",
                "description_en": "Activate referral program — request review from top 3 clients",
                "channel": "warm_referral",
                "count": 3,
            })

        return {
            "current_mrr_sar": current_mrr,
            "target_mrr_sar": target_mrr,
            "gap_sar": gap,
            "weeks_to_target": weeks_to_target,
            "new_deals_needed_per_week": new_deals_per_week,
            "leads_needed_per_week": leads_needed,
            "weekly_actions": actions,
            "compliant_channels_only": True,
        }

    def score_lead(self, company_name: str, sector: str, size: str,
                   pain_points: list[str]) -> dict:
        """Score a lead 0-100 with recommended next action."""
        base_score = 40
        sector_boost = _SECTOR_WEIGHTS.get(sector.lower(), 1.0)
        size_boost = _SIZE_WEIGHTS.get(size.lower(), 1.0)

        # Pain points boost
        high_value_pains = [
            "data_quality", "manual_reports", "no_crm", "lost_leads",
            "inventory_issues", "cash_flow", "compliance", "growth_stagnant",
        ]
        pain_score = sum(10 for p in pain_points if p.lower() in high_value_pains)
        pain_score = min(pain_score, 30)

        raw = base_score * sector_boost * size_boost + pain_score
        score = int(min(100, max(0, raw)))

        if score >= 75:
            tier = "hot"
            next_action = "Schedule free diagnostic call within 48 hours"
            offer = "free_diagnostic"
        elif score >= 50:
            tier = "warm"
            next_action = "Send case study + diagnostic offer via warm channel"
            offer = "free_diagnostic"
        else:
            tier = "cold"
            next_action = "Add to content nurture sequence; re-evaluate in 30 days"
            offer = None

        return {
            "company": company_name,
            "score": score,
            "tier": tier,
            "sector_weight": sector_boost,
            "size_weight": size_boost,
            "pain_score": pain_score,
            "recommended_next_action": next_action,
            "recommended_offer": offer,
        }

    def generate_outreach_sequence(self, lead_profile: dict) -> list[dict]:
        """
        Return 5-step compliant outreach sequence.
        Doctrine: no cold WhatsApp, no LinkedIn DM automation, no bulk email.
        """
        name = lead_profile.get("company_name", "الشركة")
        sector = lead_profile.get("sector", "عام")
        score = lead_profile.get("score", 50)

        warmth = "warm" if score >= 50 else "nurture"

        steps: list[dict] = [
            {
                "step": 1,
                "day": 0,
                "channel": "linkedin_organic_post" if warmth == "nurture" else "warm_referral",
                "action_ar": f"نشر محتوى يعالج تحديات قطاع {sector}",
                "action_en": f"Publish content addressing {sector} sector challenges",
                "template": "sector_pain_hook",
                "compliant": True,
            },
            {
                "step": 2,
                "day": 3,
                "channel": "email_to_known_contact" if score >= 60 else "content_marketing",
                "action_ar": f"إرسال دراسة حالة مشابهة لـ {name}",
                "action_en": f"Send relevant case study to {name}",
                "template": "case_study_share",
                "compliant": True,
            },
            {
                "step": 3,
                "day": 7,
                "channel": "warm_referral" if score >= 70 else "inbound_web",
                "action_ar": "عرض جلسة تشخيص مجانية (45 دقيقة)",
                "action_en": "Offer free diagnostic session (45 min)",
                "template": "free_diagnostic_offer",
                "compliant": True,
            },
            {
                "step": 4,
                "day": 14,
                "channel": "whatsapp_to_known_contact" if score >= 75 else "email_to_known_contact",
                "action_ar": "متابعة قصيرة + ربط بنتائج التشخيص",
                "action_en": "Short follow-up + connect to diagnostic findings",
                "template": "diagnostic_followup",
                "compliant": True,
            },
            {
                "step": 5,
                "day": 21,
                "channel": "event_follow_up",
                "action_ar": "دعوة لحضور ورشة عمل أو ندوة إلكترونية مجانية",
                "action_en": "Invite to free workshop or webinar",
                "template": "event_invite",
                "compliant": True,
            },
        ]

        return steps

    def calculate_ltv(self, tier: str, months_active: int) -> float:
        """Calculate customer LTV based on service tier and activity."""
        base_ltv = _TIER_LTV.get(tier, 0)
        # Adjust for early/late stage
        if months_active < 3:
            return base_ltv * 0.6
        elif months_active < 12:
            return base_ltv * 0.85
        return base_ltv

    def churn_risk_assessment(self, client_id: str, last_activity_days: int,
                               invoices_paid: int, support_tickets: int) -> dict:
        """Return churn risk score and recommended action."""
        score = 0

        if last_activity_days > 60:
            score += 40
        elif last_activity_days > 30:
            score += 20
        elif last_activity_days > 14:
            score += 10

        if invoices_paid == 0:
            score += 30
        elif invoices_paid < 3:
            score += 10

        if support_tickets >= 3:
            score += 20
        elif support_tickets >= 1:
            score += 5

        score = min(100, score)

        if score >= 70:
            risk_level = "critical"
            action = "Founder direct outreach within 24 hours; offer free strategy session"
        elif score >= 40:
            risk_level = "high"
            action = "Account manager check-in this week; identify value gaps"
        elif score >= 20:
            risk_level = "medium"
            action = "Send value report + NPS survey"
        else:
            risk_level = "low"
            action = "Continue regular cadence; consider expansion offer"

        return {
            "client_id": client_id,
            "churn_risk_score": score,
            "risk_level": risk_level,
            "recommended_action": action,
            "last_activity_days": last_activity_days,
            "invoices_paid": invoices_paid,
            "support_tickets_open": support_tickets,
        }

    def expansion_opportunities(self, client_tier: str, months_active: int) -> list[dict]:
        """Return upsell/cross-sell opportunities for existing client."""
        opportunities: list[dict] = []

        tier_order = ["free_diagnostic", "sprint_499", "data_pack_1500",
                      "managed_ops", "custom_ai"]

        try:
            current_idx = tier_order.index(client_tier)
        except ValueError:
            return []

        # Upsell to next tier
        if current_idx < len(tier_order) - 1:
            next_tier = tier_order[current_idx + 1]
            if months_active >= 1:
                opportunities.append({
                    "type": "upsell",
                    "target_tier": next_tier,
                    "readiness": "high" if months_active >= 3 else "medium",
                    "pitch_ar": "استمر في النمو مع الباقة التالية",
                    "pitch_en": "Continue growing with the next tier",
                    "timing": "Now" if months_active >= 3 else "After month 3",
                })

        # Cross-sell training/workshops
        if client_tier in ("sprint_499", "data_pack_1500"):
            opportunities.append({
                "type": "cross_sell",
                "target_tier": "training_addon",
                "readiness": "medium",
                "pitch_ar": "ورشة تدريبية للفريق على قراءة تقارير الذكاء الاصطناعي",
                "pitch_en": "Team workshop on reading AI reports",
                "timing": "Anytime",
            })

        # Referral program
        if months_active >= 2:
            opportunities.append({
                "type": "referral",
                "target_tier": "referral_program",
                "readiness": "high",
                "pitch_ar": "احصل على 5,000 ريال لكل إحالة مُغلقة",
                "pitch_en": "Earn 5,000 SAR per closed referral",
                "timing": "Now",
            })

        return opportunities
