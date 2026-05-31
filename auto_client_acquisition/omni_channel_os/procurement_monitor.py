"""Procurement Monitor — monitors tender portals for AI/automation opportunities."""
from __future__ import annotations

import logging
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Language,
    RiskLevel,
)

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True

MONITORED_KEYWORDS = [
    "ذكاء اصطناعي",
    "أتمتة",
    "تحول رقمي",
    "AI",
    "automation",
    "digital transformation",
    "workflow",
    "RPA",
    "اعمل ذكي",
    "حلول رقمية",
    "تقنية المعلومات",
    "الاستشارات التقنية",
    "document management",
    "knowledge management",
    "reporting system",
    "إدارة المستندات",
    "نظام التقارير",
    "قاعدة المعرفة",
]

TENDER_SECTORS_FIT = [
    "government",
    "semi_government",
    "healthcare",
    "education",
    "infrastructure",
    "facilities_management",
]

_COMPANY_ID_PLACEHOLDER = "procurement_monitor"


class ProcurementMonitor:
    """Monitors and scores tender opportunities. Submission is always manual."""

    _NO_AUTO_SEND = True
    _SUBMISSION_ALWAYS_MANUAL = True

    def score_opportunity(self, tender: dict[str, Any]) -> float:
        """Score tender fit 0-100 based on keywords, sector, and budget signals."""
        score = 0.0

        title = (tender.get("title") or "").lower()
        description = (tender.get("description") or "").lower()
        combined_text = f"{title} {description}"

        keyword_hits = sum(
            1 for kw in MONITORED_KEYWORDS if kw.lower() in combined_text
        )
        score += min(40.0, keyword_hits * 8.0)

        sector = (tender.get("sector") or "").lower()
        for fit_sector in TENDER_SECTORS_FIT:
            if fit_sector in sector:
                score += 25.0
                break

        budget = tender.get("budget") or tender.get("estimated_value") or 0
        try:
            budget_val = float(budget)
            if budget_val >= 500_000:
                score += 25.0
            elif budget_val >= 100_000:
                score += 15.0
            elif budget_val >= 50_000:
                score += 8.0
        except (TypeError, ValueError):
            pass

        # Bonus for explicit AI/automation in title
        if any(kw.lower() in title for kw in ["ai", "automation", "ذكاء اصطناعي", "أتمتة"]):
            score += 10.0

        return min(100.0, max(0.0, score))

    def is_relevant(self, tender: dict[str, Any]) -> bool:
        """Return True if the tender passes the relevance threshold (score >= 30)."""
        return self.score_opportunity(tender) >= 30.0

    def draft_expression_of_interest(
        self,
        tender: dict[str, Any],
        language: str = "ar",
    ) -> ChannelAsset:
        """Draft expression of interest. MANUAL SUBMISSION REQUIRED."""
        assert self._SUBMISSION_ALWAYS_MANUAL, "Submission is always manual"

        title = tender.get("title") or "المناقصة"
        issuer = tender.get("issuer") or tender.get("entity") or "الجهة المعنية"
        score = self.score_opportunity(tender)

        if language in ("ar", "arabic"):
            lang = Language.arabic
            body = (
                f"السلام عليكم،\n\n"
                f"نتقدم بهذا التعبير عن اهتمامنا بالمناقصة: {title}\n"
                f"الجهة: {issuer}\n\n"
                f"تقدم شركة Dealix حلول AI Workflow المتخصصة للشركات الخليجية.\n"
                f"لدينا خبرة في تنفيذ مشاريع مماثلة في قطاعات:\n"
                f"• الخدمات الحكومية\n"
                f"• الخدمات الصحية\n"
                f"• إدارة المرافق\n\n"
                f"يسعدنا تقديم نبذة تفصيلية عن قدراتنا التقنية والتشغيلية.\n\n"
                f"مع التحية،\nSami | Dealix\n"
                f"[ملاحظة: هذه المسودة تتطلب مراجعة وموافقة بشرية قبل الإرسال]"
            )
            cta = "احصل على نبذة تفصيلية"
        else:
            lang = Language.english
            body = (
                f"Dear Team,\n\n"
                f"We are pleased to express our interest in the tender: {title}\n"
                f"Issuing entity: {issuer}\n\n"
                f"Dealix provides specialized AI Workflow solutions for GCC organizations.\n"
                f"We have experience delivering similar projects in:\n"
                f"• Government services\n"
                f"• Healthcare operations\n"
                f"• Facilities management\n\n"
                f"We would be happy to provide a detailed overview of our technical capabilities.\n\n"
                f"Best regards,\nSami | Dealix\n"
                f"[Note: This draft requires human review and approval before submission]"
            )
            cta = "Get a detailed capabilities overview"

        return ChannelAsset(
            company_id=_COMPANY_ID_PLACEHOLDER,
            asset_type=AssetType.proposal_seed,
            channel=ChannelType.procurement_portal,
            language=lang,
            subject_or_hook=f"Expression of Interest — {title}",
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=tender.get("sector") or "",
            country=tender.get("country") or "KSA",
        )

    def draft_proposal_skeleton(self, tender: dict[str, Any]) -> ChannelAsset:
        """Generate a proposal skeleton for a relevant tender."""
        assert self._SUBMISSION_ALWAYS_MANUAL, "Submission is always manual"

        title = tender.get("title") or "المناقصة"
        issuer = tender.get("issuer") or "الجهة المعنية"
        requirements = tender.get("requirements") or []
        req_text = (
            "\n".join(f"• {r}" for r in requirements)
            if requirements
            else "• [يرجى استكمال المتطلبات من وثيقة المناقصة]"
        )

        body = (
            f"# مقترح فني — {title}\n"
            f"## الجهة: {issuer}\n\n"
            f"### 1. الفهم التقني للمتطلبات\n{req_text}\n\n"
            f"### 2. المنهجية المقترحة\n"
            f"• مرحلة التشخيص (7 أيام): تحليل workflows الحالية وتحديد الفجوات\n"
            f"• مرحلة الـ Pilot (30 يوم): تنفيذ workflow واحد مع بيانات تجريبية\n"
            f"• مرحلة التوسع: تطبيق تدريجي مع موافقة بشرية في كل مرحلة\n\n"
            f"### 3. الكفاءات التقنية\n"
            f"• أنظمة AI Workflow مخصصة للسوق الخليجي\n"
            f"• امتثال كامل لاشتراطات حماية البيانات\n"
            f"• موافقة بشرية إلزامية قبل أي إجراء تلقائي\n\n"
            f"### 4. التسعير التقديري\n"
            f"• [يرجى استكمال بناءً على نطاق المشروع]\n\n"
            f"[ملاحظة: هذا الهيكل يتطلب تخصيصاً واعتماداً بشرياً قبل الإرسال]"
        )

        return ChannelAsset(
            company_id=_COMPANY_ID_PLACEHOLDER,
            asset_type=AssetType.proposal_seed,
            channel=ChannelType.procurement_portal,
            language=Language.arabic,
            subject_or_hook=f"Proposal Skeleton — {title}",
            body=body,
            cta="احصل على تقييم المناقصات",
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector=tender.get("sector") or "",
            country=tender.get("country") or "KSA",
        )

    def summarize(self, tender: dict[str, Any]) -> dict[str, Any]:
        """Summarize a tender: title, requirements, fit_score, recommended_action."""
        score = self.score_opportunity(tender)
        relevant = self.is_relevant(tender)

        if score >= 70:
            action = "draft_full_proposal"
        elif score >= 50:
            action = "draft_expression_of_interest"
        elif score >= 30:
            action = "monitor_closely"
        else:
            action = "skip"

        return {
            "title": tender.get("title") or "",
            "issuer": tender.get("issuer") or tender.get("entity") or "",
            "sector": tender.get("sector") or "",
            "deadline": tender.get("deadline") or tender.get("closing_date") or "",
            "requirements": tender.get("requirements") or [],
            "fit_score": round(score, 1),
            "is_relevant": relevant,
            "recommended_action": action,
            "submission_note": "All submissions require manual human review and approval.",
        }


__all__ = [
    "MONITORED_KEYWORDS",
    "TENDER_SECTORS_FIT",
    "ProcurementMonitor",
]
