"""Customer onboarding triggered by a paid Moyasar webhook.

Pure-logic engine for engine #5. Given a parsed paid MoyasarWebhookEvent
and an engagement root directory, this module materializes the artifacts
the founder needs to deliver the Sprint:

  1. engagement folder under <engagement_root>/<engagement_id>/
  2. manifest.json  — engagement record (customer, amount, payment_id, paid_at)
  3. receipt.md     — ZATCA-format stub (structure only; not a real e-invoice)
  4. welcome_draft.md  — bilingual welcome email DRAFT (not sent)
  5. approval_required.json — explicit human-approval gate for any external send

Doctrine compliance:
- #2/#3/#8 — no external send happens here. The welcome email is a draft;
  the approval_required.json file gates any future send through the
  Approval Center.
- #4 — no fabricated numbers; only the values from the actual webhook are
  recorded.
- #11 — registers the Sprint's capital asset on the engagement record.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from auto_client_acquisition.payment_ops.moyasar_harness import MoyasarWebhookEvent


class OnboardingError(ValueError):
    """Raised when onboarding inputs are invalid (e.g. event not paid)."""


@dataclass(frozen=True, slots=True)
class OnboardingArtifacts:
    """The files materialized on disk for a newly paid engagement."""

    engagement_id: str
    engagement_dir: Path
    manifest_path: Path
    receipt_path: Path
    welcome_draft_path: Path
    approval_gate_path: Path
    customer_name: str
    amount_sar: float
    capital_asset: str = field(default="Sprint engagement record")

    def to_dict(self) -> dict[str, object]:
        return {
            "engagement_id": self.engagement_id,
            "engagement_dir": str(self.engagement_dir),
            "manifest_path": str(self.manifest_path),
            "receipt_path": str(self.receipt_path),
            "welcome_draft_path": str(self.welcome_draft_path),
            "approval_gate_path": str(self.approval_gate_path),
            "customer_name": self.customer_name,
            "amount_sar": self.amount_sar,
            "capital_asset": self.capital_asset,
        }


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe_engagement_id(event: MoyasarWebhookEvent) -> str:
    candidate = event.metadata.get("engagement_id", "").strip()
    if candidate:
        return "".join(c for c in candidate if c.isalnum() or c in ("-", "_"))[:64]
    return f"ENG-{event.payment_id[:16]}"


def _receipt_stub(
    *,
    engagement_id: str,
    customer_name: str,
    amount_sar: float,
    payment_id: str,
    paid_at_iso: str,
) -> str:
    return (
        "# Receipt — ZATCA-format stub\n\n"
        "**This is a stub structure, not a registered ZATCA e-invoice. "
        "A real invoice is issued separately through ZATCA-compliant tooling.**\n\n"
        f"- Engagement: `{engagement_id}`\n"
        f"- Customer: {customer_name}\n"
        f"- Amount: {amount_sar:.2f} SAR\n"
        f"- Payment ID: `{payment_id}`\n"
        f"- Paid at (UTC): {paid_at_iso}\n"
        "- VAT: to be applied per ZATCA regulations on the formal invoice.\n"
    )


def _welcome_draft(*, customer_name: str, engagement_id: str) -> str:
    return (
        "# Welcome — DRAFT (requires founder approval before sending)\n\n"
        "## القسم العربي\n\n"
        f"السلام عليكم {customer_name}،\n\n"
        f"تأكّد قبول العرض ودفع الدفعة الأولى لسبرنت ذكاء الإيرادات "
        f"(رقم المشروع `{engagement_id}`). نبدأ يوم العمل التالي بـ "
        "اليوم الأول: كيك أوف وتوقيع جواز المصدر، ثم استلام ملف "
        "الحسابات (CSV). الجدولة الكاملة في خطة السبرنت.\n\n"
        "النتائج التقديرية ليست نتائج مضمونة.\n\n"
        "---\n\n"
        "## English Section\n\n"
        f"Hi {customer_name},\n\n"
        f"Acceptance + first payment received for the Revenue Intelligence "
        f"Sprint (engagement `{engagement_id}`). Day 1 starts the next "
        "business day with kickoff + Source Passport signing, then the "
        "accounts CSV import. Full schedule in the Sprint plan.\n\n"
        "Estimated outcomes are not guaranteed outcomes.\n"
    )


def onboard_on_payment(
    *,
    event: MoyasarWebhookEvent,
    engagement_root: Path | str,
    customer_name: str,
) -> OnboardingArtifacts:
    """Materialize the engagement folder for a newly paid Sprint.

    Idempotent: re-running with the same paid event overwrites the manifest
    (allowing the founder to re-process if the file system was rolled
    back during testing) but the engagement_id stays stable.
    """
    if not event.is_paid:
        raise OnboardingError("event is not a paid event")
    if not customer_name.strip():
        raise OnboardingError("customer_name is required")
    if event.amount_halalas <= 0:
        raise OnboardingError("event has non-positive amount")

    root = Path(engagement_root)
    root.mkdir(parents=True, exist_ok=True)
    engagement_id = _safe_engagement_id(event)
    engagement_dir = root / engagement_id
    engagement_dir.mkdir(parents=True, exist_ok=True)

    amount_sar = event.amount_halalas / 100.0
    paid_at_iso = _utc_now_iso()

    manifest = {
        "engagement_id": engagement_id,
        "customer_name": customer_name,
        "payment_id": event.payment_id,
        "amount_sar": amount_sar,
        "currency": event.currency,
        "paid_at_utc": paid_at_iso,
        "metadata": dict(event.metadata),
        "capital_asset": "Sprint engagement record",
        "approval_required_for_external_send": True,
        "doctrine_notes": [
            "no_external_send_without_approval",
            "estimated_outcomes_not_guaranteed",
        ],
    }
    manifest_path = engagement_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    receipt_path = engagement_dir / "receipt.md"
    receipt_path.write_text(
        _receipt_stub(
            engagement_id=engagement_id,
            customer_name=customer_name,
            amount_sar=amount_sar,
            payment_id=event.payment_id,
            paid_at_iso=paid_at_iso,
        ),
        encoding="utf-8",
    )

    welcome_path = engagement_dir / "welcome_draft.md"
    welcome_path.write_text(
        _welcome_draft(customer_name=customer_name, engagement_id=engagement_id),
        encoding="utf-8",
    )

    approval_gate_path = engagement_dir / "approval_required.json"
    approval_gate_path.write_text(
        json.dumps(
            {
                "engagement_id": engagement_id,
                "artifact": "welcome_draft.md",
                "state": "draft_only",
                "requires_approval_before_send": True,
                "created_at_utc": paid_at_iso,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return OnboardingArtifacts(
        engagement_id=engagement_id,
        engagement_dir=engagement_dir,
        manifest_path=manifest_path,
        receipt_path=receipt_path,
        welcome_draft_path=welcome_path,
        approval_gate_path=approval_gate_path,
        customer_name=customer_name,
        amount_sar=amount_sar,
    )


__all__ = ["OnboardingArtifacts", "OnboardingError", "onboard_on_payment"]
