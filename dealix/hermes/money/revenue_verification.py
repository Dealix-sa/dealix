"""
Revenue Verification — يقبل/يرفض حدثًا كـ "verified revenue" بناءً على شواهد
موضوعية. لا حدث يُسجَّل كـ revenue بدون مرور هذا الفلتر.
"""

from __future__ import annotations

from dataclasses import dataclass

from .revenue_events import RevenueEvent, RevenueEventKind


VERIFICATION_KINDS: frozenset[RevenueEventKind] = frozenset(
    {
        RevenueEventKind.PAYMENT_RECEIVED,
        RevenueEventKind.SIGNED_AGREEMENT,
        RevenueEventKind.INVOICE_PAID,
        RevenueEventKind.RETAINER_STARTED,
        RevenueEventKind.RETAINER_RENEWED,
        RevenueEventKind.PARTNER_PAID_CUSTOMER,
    }
)


@dataclass
class VerificationResult:
    accepted: bool
    reason: str
    verification_source: str | None = None


class RevenueVerifier:
    def verify(self, event: RevenueEvent) -> VerificationResult:
        if event.kind not in VERIFICATION_KINDS:
            return VerificationResult(
                accepted=False,
                reason=f"kind `{event.kind.value}` is not a verification source",
            )
        if event.amount_sar <= 0:
            return VerificationResult(
                accepted=False,
                reason="amount_sar must be > 0 for verified revenue",
            )
        if event.kind in {
            RevenueEventKind.PAYMENT_RECEIVED,
            RevenueEventKind.INVOICE_PAID,
        } and not event.payment_reference:
            return VerificationResult(
                accepted=False,
                reason="payment-based revenue requires payment_reference",
            )
        if event.kind == RevenueEventKind.SIGNED_AGREEMENT and not event.deal_id:
            return VerificationResult(
                accepted=False,
                reason="signed_agreement revenue requires deal_id",
            )
        return VerificationResult(
            accepted=True,
            reason="verified",
            verification_source=event.kind.value,
        )


__all__ = ["RevenueVerifier", "VerificationResult", "VERIFICATION_KINDS"]
