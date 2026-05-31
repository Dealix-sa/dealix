"""Email orchestrator — approval-gated email pipeline.

CONSTITUTIONAL GATES:
- APPROVAL_FIRST: every email is a DRAFT. No email sends without founder.approved_at set.
- NO_AUTO_SEND: process() never calls send() directly. It creates a FounderAlertRecord.
- NO_PII_IN_LOGS: email addresses and contact names never appear in log lines.

All templates are bilingual AR+EN and include a PDPL footer.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, Field

from core.logging import get_logger

log = get_logger(__name__)

_PDPL_FOOTER_AR = (
    "\n\n---\n"
    "تمت معالجة هذه الرسالة وفق أحكام نظام حماية البيانات الشخصية (نظام PDPL) السعودي. "
    "لإلغاء الاشتراك أو ممارسة حقوقك في البيانات، تواصل معنا على privacy@dealix.ai"
)

_PDPL_FOOTER_EN = (
    "\n\n---\n"
    "This message is processed in accordance with Saudi Arabia's Personal Data Protection Law (PDPL). "
    "To unsubscribe or exercise your data rights, contact us at privacy@dealix.ai"
)

_TEMPLATE_TYPES = frozenset(
    {"welcome", "sprint_day3", "sprint_complete", "retainer_pitch", "payment_receipt"}
)


class EmailDraft(BaseModel):
    """A draft email awaiting founder approval before sending."""

    draft_id: str = Field(default_factory=lambda: f"drft_{uuid.uuid4().hex[:12]}")
    to_email: str
    to_name: str
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    template_type: str  # welcome | sprint_day3 | sprint_complete | retainer_pitch | payment_receipt
    account_id: str
    requires_approval: bool = True
    approved_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None

    @property
    def is_approved(self) -> bool:
        """Return True only when an explicit approved_at timestamp is present."""
        return self.approved_at is not None

    @property
    def is_sent(self) -> bool:
        return self.sent_at is not None


class EmailOrchestrator:
    """
    Create approval-gated email drafts.

    Key invariant: this class never calls the email client directly.
    Only send_approved_draft() sends — and only after verifying approved_at is set.
    """

    def create_welcome_draft(
        self,
        account_id: str,
        company_name: str,
        contact_name: str,
        contact_email: str,
        service_tier: str,
    ) -> EmailDraft:
        """Create a bilingual welcome email draft for a new customer."""
        tier_label_ar = _tier_label_ar(service_tier)
        tier_label_en = _tier_label_en(service_tier)

        body_ar = (
            f"مرحباً {contact_name}،\n\n"
            f"أهلاً بكم في Dealix! يسعدنا انضمام {company_name} إلى منصتنا.\n\n"
            f"الباقة المفعّلة: {tier_label_ar}\n\n"
            "الخطوة التالية: سيتواصل معكم فريقنا خلال 24 ساعة لجدولة جلسة الاستلام وبدء رحلتكم."
            + _PDPL_FOOTER_AR
        )
        body_en = (
            f"Hello {contact_name},\n\n"
            f"Welcome to Dealix! We are delighted to have {company_name} on board.\n\n"
            f"Active plan: {tier_label_en}\n\n"
            "Next step: Our team will contact you within 24 hours to schedule the intake session and begin your journey."
            + _PDPL_FOOTER_EN
        )

        draft = EmailDraft(
            to_email=contact_email,
            to_name=contact_name,
            subject_ar=f"مرحباً بكم في Dealix — {company_name}",
            subject_en=f"Welcome to Dealix — {company_name}",
            body_ar=body_ar,
            body_en=body_en,
            template_type="welcome",
            account_id=account_id,
        )
        log.info(
            "email_draft_created",
            template_type="welcome",
            account_id=account_id,
            draft_id=draft.draft_id,
        )
        return draft

    def create_sprint_day3_draft(
        self,
        account_id: str,
        company_name: str,
        day3_findings: str,
    ) -> EmailDraft:
        """Create a day-3 sprint progress update draft."""
        body_ar = (
            f"عزيزنا فريق {company_name}،\n\n"
            "وصلنا إلى اليوم الثالث من السبرنت، وإليكم أبرز ما توصّلنا إليه حتى الآن:\n\n"
            f"{day3_findings}\n\n"
            "سيتواصل فريقنا لمناقشة الخطوات التالية قبل نهاية الأسبوع."
            + _PDPL_FOOTER_AR
        )
        body_en = (
            f"Dear {company_name} team,\n\n"
            "We have reached day 3 of your sprint. Here are the key findings so far:\n\n"
            f"{day3_findings}\n\n"
            "Our team will follow up to discuss next steps before end of the week."
            + _PDPL_FOOTER_EN
        )

        draft = EmailDraft(
            to_email="",  # filled by caller when sending
            to_name=company_name,
            subject_ar=f"تحديث السبرنت — اليوم الثالث | {company_name}",
            subject_en=f"Sprint Day 3 Update | {company_name}",
            body_ar=body_ar,
            body_en=body_en,
            template_type="sprint_day3",
            account_id=account_id,
        )
        log.info(
            "email_draft_created",
            template_type="sprint_day3",
            account_id=account_id,
            draft_id=draft.draft_id,
        )
        return draft

    def create_sprint_complete_draft(
        self,
        account_id: str,
        company_name: str,
        proof_pack_summary: str,
    ) -> EmailDraft:
        """Create a sprint completion email with proof-pack summary."""
        body_ar = (
            f"عزيزنا فريق {company_name}،\n\n"
            "اكتمل السبرنت بنجاح! فيما يلي ملخص الإنجازات والقيمة المحققة:\n\n"
            f"{proof_pack_summary}\n\n"
            "سيتواصل فريقنا قريباً لمناقشة المرحلة التالية من تطوير عملياتكم."
            + _PDPL_FOOTER_AR
        )
        body_en = (
            f"Dear {company_name} team,\n\n"
            "Your sprint has been completed successfully! Here is a summary of the achievements and value delivered:\n\n"
            f"{proof_pack_summary}\n\n"
            "Our team will be in touch shortly to discuss the next phase of your operations evolution."
            + _PDPL_FOOTER_EN
        )

        draft = EmailDraft(
            to_email="",
            to_name=company_name,
            subject_ar=f"اكتمال السبرنت وتقرير القيمة | {company_name}",
            subject_en=f"Sprint Complete — Value Report | {company_name}",
            body_ar=body_ar,
            body_en=body_en,
            template_type="sprint_complete",
            account_id=account_id,
        )
        log.info(
            "email_draft_created",
            template_type="sprint_complete",
            account_id=account_id,
            draft_id=draft.draft_id,
        )
        return draft

    def create_retainer_pitch_draft(
        self,
        account_id: str,
        company_name: str,
        health_score: float,
        expansion_reason_ar: str,
        expansion_reason_en: str,
    ) -> EmailDraft:
        """Create a retainer/expansion pitch draft based on health score analysis."""
        body_ar = (
            f"عزيزنا فريق {company_name}،\n\n"
            f"استناداً إلى تحليل أداء حسابكم (درجة الصحة الحالية: {health_score:.0f}/100)، "
            "نرى فرصة واضحة لتعميق شراكتنا:\n\n"
            f"{expansion_reason_ar}\n\n"
            "نود مناقشة خطة التوسع معكم — هل يناسبكم تحديد موعد قريباً؟"
            + _PDPL_FOOTER_AR
        )
        body_en = (
            f"Dear {company_name} team,\n\n"
            f"Based on your account performance analysis (current health score: {health_score:.0f}/100), "
            "we see a clear opportunity to deepen our partnership:\n\n"
            f"{expansion_reason_en}\n\n"
            "We would like to discuss an expansion plan with you — shall we schedule a call?"
            + _PDPL_FOOTER_EN
        )

        draft = EmailDraft(
            to_email="",
            to_name=company_name,
            subject_ar=f"فرصة توسع شراكتنا | {company_name}",
            subject_en=f"Partnership Expansion Opportunity | {company_name}",
            body_ar=body_ar,
            body_en=body_en,
            template_type="retainer_pitch",
            account_id=account_id,
        )
        log.info(
            "email_draft_created",
            template_type="retainer_pitch",
            account_id=account_id,
            draft_id=draft.draft_id,
        )
        return draft

    def create_payment_receipt_draft(
        self,
        account_id: str,
        company_name: str,
        amount_sar: float,
        service_tier: str,
        payment_id: str,
    ) -> EmailDraft:
        """Create a payment receipt confirmation email draft."""
        tier_label_ar = _tier_label_ar(service_tier)
        tier_label_en = _tier_label_en(service_tier)

        body_ar = (
            f"عزيزنا {company_name}،\n\n"
            "شكراً! تم استلام دفعتكم بنجاح.\n\n"
            f"الباقة: {tier_label_ar}\n"
            f"المبلغ: {amount_sar:.0f} ريال سعودي\n"
            f"رقم العملية: {payment_id}\n\n"
            "سيبدأ فريقنا العمل على حسابكم خلال 24 ساعة."
            + _PDPL_FOOTER_AR
        )
        body_en = (
            f"Dear {company_name},\n\n"
            "Thank you! Your payment has been received successfully.\n\n"
            f"Plan: {tier_label_en}\n"
            f"Amount: {amount_sar:.0f} SAR\n"
            f"Transaction ID: {payment_id}\n\n"
            "Our team will begin working on your account within 24 hours."
            + _PDPL_FOOTER_EN
        )

        draft = EmailDraft(
            to_email="",
            to_name=company_name,
            subject_ar=f"تأكيد استلام الدفعة — {tier_label_ar}",
            subject_en=f"Payment Receipt Confirmed — {tier_label_en}",
            body_ar=body_ar,
            body_en=body_en,
            template_type="payment_receipt",
            account_id=account_id,
        )
        log.info(
            "email_draft_created",
            template_type="payment_receipt",
            account_id=account_id,
            draft_id=draft.draft_id,
        )
        return draft

    async def send_approved_draft(self, draft: EmailDraft) -> bool:
        """
        Send an email draft — only callable after founder approval is confirmed.

        Gate: raises ValueError if approved_at is not set.
        This is the only place in the system that calls the email client.

        Returns True on success, False on send failure.
        """
        if not draft.is_approved:
            raise ValueError(
                f"Draft {draft.draft_id} has not been approved. "
                "Set approved_at before calling send_approved_draft()."
            )
        if not draft.to_email:
            log.warning(
                "email_draft_missing_recipient",
                draft_id=draft.draft_id,
                template_type=draft.template_type,
            )
            return False

        try:
            from integrations.email import EmailClient

            client = EmailClient()
            result = await client.send(
                to=draft.to_email,
                subject=f"{draft.subject_en} | {draft.subject_ar}",
                body_text=f"{draft.body_en}\n\n---\n\n{draft.body_ar}",
            )
            if result.success:
                draft.sent_at = datetime.now(UTC)
                log.info(
                    "email_draft_sent",
                    draft_id=draft.draft_id,
                    template_type=draft.template_type,
                    message_id=result.message_id,
                )
                return True
            log.warning(
                "email_draft_send_failed",
                draft_id=draft.draft_id,
                provider=result.provider,
                error=result.error,
            )
            return False
        except Exception as exc:
            log.warning(
                "email_draft_send_exception",
                draft_id=draft.draft_id,
                error=str(exc),
            )
            return False


# ── private helpers ────────────────────────────────────────────────────────────

_TIER_LABELS_AR: dict[str, str] = {
    "sprint_499": "سبرنت 499 ريال",
    "data_pack_1500": "حزمة البيانات 1,500 ريال",
    "managed_ops_2999": "العمليات المُدارة 2,999 ريال",
    "managed_ops_4999": "العمليات المُدارة 4,999 ريال",
    "custom_ai_15000": "ذكاء اصطناعي مخصص 15,000 ريال",
}

_TIER_LABELS_EN: dict[str, str] = {
    "sprint_499": "499 SAR Sprint",
    "data_pack_1500": "1,500 SAR Data Pack",
    "managed_ops_2999": "2,999 SAR Managed Ops",
    "managed_ops_4999": "4,999 SAR Managed Ops",
    "custom_ai_15000": "15,000 SAR Custom AI",
}


def _tier_label_ar(tier: str) -> str:
    return _TIER_LABELS_AR.get(tier, tier)


def _tier_label_en(tier: str) -> str:
    return _TIER_LABELS_EN.get(tier, tier)
