"""Repository layer for Wave 17 models.

Constitutional constraints:
- NO_PII_IN_LOGS: log lines never contain email addresses, phone numbers, or names.
- Never crash the API: every public method returns None/[] on DB error after logging.
- Use async SQLAlchemy sessions throughout.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger

log = get_logger(__name__)


def _new_id(prefix: str = "id") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# ── HealthSnapshotRepository ──────────────────────────────────────────────────


class HealthSnapshotRepository:
    """Persist and retrieve health score history for an account."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_snapshot(
        self,
        account_id: str,
        report: dict[str, Any],
    ) -> str | None:
        """
        Persist a health snapshot.

        Parameters
        ----------
        account_id:
            Target account.
        report:
            Dict with keys matching HealthSnapshotRecord columns.
            Any unknown keys are silently ignored.

        Returns
        -------
        The saved record id, or None on failure.
        """
        try:
            from db.models import HealthSnapshotRecord  # local import avoids circular at module load

            record = HealthSnapshotRecord(
                id=_new_id("hss"),
                account_id=account_id,
                overall_score=float(report.get("overall_score", 0.0)),
                tier=str(report.get("tier", "unknown")),
                engagement_score=float(report.get("engagement_score", 0.0)),
                delivery_score=float(report.get("delivery_score", 0.0)),
                financial_score=float(report.get("financial_score", 0.0)),
                satisfaction_score=float(report.get("satisfaction_score", 0.0)),
                adoption_score=float(report.get("adoption_score", 0.0)),
                risk_score=float(report.get("risk_score", 0.0)),
                is_churn_risk=bool(report.get("is_churn_risk", False)),
                churn_probability=float(report.get("churn_probability", 0.0)),
                computed_at=report.get("computed_at") or datetime.now(UTC),
            )
            self._session.add(record)
            await self._session.flush()
            log.info("health_snapshot_saved", account_id=account_id, record_id=record.id)
            return record.id
        except Exception as exc:
            log.warning("health_snapshot_save_failed", account_id=account_id, error=str(exc))
            return None

    async def get_latest(self, account_id: str) -> dict[str, Any] | None:
        """Return the most recent health snapshot for an account."""
        try:
            from db.models import HealthSnapshotRecord

            stmt = (
                select(HealthSnapshotRecord)
                .where(HealthSnapshotRecord.account_id == account_id)
                .order_by(HealthSnapshotRecord.computed_at.desc())
                .limit(1)
            )
            result = await self._session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _snapshot_to_dict(row)
        except Exception as exc:
            log.warning("health_snapshot_get_latest_failed", account_id=account_id, error=str(exc))
            return None

    async def get_history(
        self, account_id: str, days: int = 90
    ) -> list[dict[str, Any]]:
        """Return health snapshots for the last N days, oldest first."""
        try:
            from db.models import HealthSnapshotRecord

            since = datetime.now(UTC) - timedelta(days=days)
            stmt = (
                select(HealthSnapshotRecord)
                .where(
                    HealthSnapshotRecord.account_id == account_id,
                    HealthSnapshotRecord.computed_at >= since,
                )
                .order_by(HealthSnapshotRecord.computed_at.asc())
            )
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [_snapshot_to_dict(r) for r in rows]
        except Exception as exc:
            log.warning("health_snapshot_get_history_failed", account_id=account_id, error=str(exc))
            return []


def _snapshot_to_dict(row: Any) -> dict[str, Any]:
    return {
        "id": row.id,
        "account_id": row.account_id,
        "overall_score": row.overall_score,
        "tier": row.tier,
        "engagement_score": row.engagement_score,
        "delivery_score": row.delivery_score,
        "financial_score": row.financial_score,
        "satisfaction_score": row.satisfaction_score,
        "adoption_score": row.adoption_score,
        "risk_score": row.risk_score,
        "is_churn_risk": row.is_churn_risk,
        "churn_probability": row.churn_probability,
        "computed_at": row.computed_at.isoformat() if row.computed_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


# ── FounderAlertRepository ────────────────────────────────────────────────────

_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class FounderAlertRepository:
    """Manage the founder alert queue."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_alert(
        self,
        alert_type: str,
        title_ar: str,
        title_en: str,
        body_ar: str,
        body_en: str,
        priority: str = "medium",
        payment_id: str | None = None,
        account_id: str | None = None,
        amount_sar: float | None = None,
    ) -> str | None:
        """
        Create a new founder alert in pending state.

        Returns the alert_id on success, None on failure.
        NO_PII_IN_LOGS: body/title strings are never logged.
        """
        try:
            from db.models import FounderAlertRecord

            alert_id = _new_id("alrt")
            record = FounderAlertRecord(
                id=_new_id("far"),
                alert_id=alert_id,
                alert_type=alert_type,
                title_ar=title_ar,
                title_en=title_en,
                body_ar=body_ar,
                body_en=body_en,
                priority=priority,
                status="pending",
                payment_id=payment_id,
                account_id=account_id,
                amount_sar=amount_sar,
            )
            self._session.add(record)
            await self._session.flush()
            log.info(
                "founder_alert_created",
                alert_id=alert_id,
                alert_type=alert_type,
                priority=priority,
            )
            return alert_id
        except Exception as exc:
            log.warning(
                "founder_alert_create_failed", alert_type=alert_type, error=str(exc)
            )
            return None

    async def get_pending(self) -> list[dict[str, Any]]:
        """Return all pending alerts sorted by priority (high first) then created_at."""
        try:
            from db.models import FounderAlertRecord

            stmt = (
                select(FounderAlertRecord)
                .where(FounderAlertRecord.status == "pending")
                .order_by(FounderAlertRecord.created_at.asc())
            )
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            sorted_rows = sorted(
                rows,
                key=lambda r: (_PRIORITY_ORDER.get(r.priority, 99), r.created_at or datetime.min),
            )
            return [_alert_to_dict(r) for r in sorted_rows]
        except Exception as exc:
            log.warning("founder_alert_get_pending_failed", error=str(exc))
            return []

    async def get_all(self) -> list[dict[str, Any]]:
        """Return all alerts regardless of status."""
        try:
            from db.models import FounderAlertRecord

            stmt = select(FounderAlertRecord).order_by(FounderAlertRecord.created_at.desc())
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [_alert_to_dict(r) for r in rows]
        except Exception as exc:
            log.warning("founder_alert_get_all_failed", error=str(exc))
            return []

    async def get_by_alert_id(self, alert_id: str) -> dict[str, Any] | None:
        """Fetch a single alert by its business alert_id."""
        try:
            from db.models import FounderAlertRecord

            stmt = select(FounderAlertRecord).where(
                FounderAlertRecord.alert_id == alert_id
            )
            result = await self._session.execute(stmt)
            row = result.scalar_one_or_none()
            return _alert_to_dict(row) if row else None
        except Exception as exc:
            log.warning("founder_alert_get_by_id_failed", alert_id=alert_id, error=str(exc))
            return None

    async def mark_reviewed(
        self,
        alert_id: str,
        action: str,
        reviewed_by: str = "founder",
    ) -> dict[str, Any] | None:
        """
        Mark an alert as approved or dismissed.

        Parameters
        ----------
        alert_id:
            Business alert_id (not the PK id).
        action:
            "approved" or "dismissed".
        reviewed_by:
            Identifier of the reviewer (never a real email — use role/id).
        """
        if action not in ("approved", "dismissed"):
            log.warning("founder_alert_invalid_action", alert_id=alert_id, action=action)
            return None
        try:
            from db.models import FounderAlertRecord

            stmt = select(FounderAlertRecord).where(
                FounderAlertRecord.alert_id == alert_id
            )
            result = await self._session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                log.warning("founder_alert_not_found", alert_id=alert_id)
                return None
            row.status = action
            row.reviewed_at = datetime.now(UTC)
            row.reviewed_by = reviewed_by
            await self._session.flush()
            log.info("founder_alert_reviewed", alert_id=alert_id, action=action)
            return _alert_to_dict(row)
        except Exception as exc:
            log.warning("founder_alert_mark_reviewed_failed", alert_id=alert_id, error=str(exc))
            return None

    async def count_by_status_and_type(self) -> dict[str, Any]:
        """Return aggregate counts keyed by status and type."""
        try:
            from db.models import FounderAlertRecord

            stmt = select(FounderAlertRecord)
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            by_status: dict[str, int] = {}
            by_type: dict[str, int] = {}
            for r in rows:
                by_status[r.status] = by_status.get(r.status, 0) + 1
                by_type[r.alert_type] = by_type.get(r.alert_type, 0) + 1
            return {
                "total": len(rows),
                "by_status": by_status,
                "by_type": by_type,
            }
        except Exception as exc:
            log.warning("founder_alert_count_failed", error=str(exc))
            return {"total": 0, "by_status": {}, "by_type": {}}


def _alert_to_dict(row: Any) -> dict[str, Any]:
    return {
        "id": row.id,
        "alert_id": row.alert_id,
        "alert_type": row.alert_type,
        "title_ar": row.title_ar,
        "title_en": row.title_en,
        "body_ar": row.body_ar,
        "body_en": row.body_en,
        "priority": row.priority,
        "status": row.status,
        "payment_id": row.payment_id,
        "account_id": row.account_id,
        "amount_sar": row.amount_sar,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "reviewed_at": row.reviewed_at.isoformat() if row.reviewed_at else None,
        "reviewed_by": row.reviewed_by,
    }


# ── PaymentRepository ─────────────────────────────────────────────────────────


class PaymentRepository:
    """Persist and retrieve payment events."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_payment(
        self,
        event: Any,
        zatca_result: dict[str, Any] | None = None,
        onboarding_id: str = "",
        alert_id: str = "",
    ) -> str | None:
        """
        Persist a PaymentEvent after processing.

        Returns the record id on success, None on failure.
        NO_PII_IN_LOGS: customer email/name never appear in log lines.
        """
        try:
            from db.models import PaymentRecordDB

            record = PaymentRecordDB(
                id=_new_id("prec"),
                payment_id=event.payment_id,
                invoice_id=event.invoice_id,
                status=event.status,
                amount_sar=float(event.amount_sar),
                amount_halalas=int(event.amount_halalas),
                service_tier=event.service_tier,
                account_id=event.account_id,
                customer_name=event.customer_name,
                customer_email=event.customer_email,
                is_live_mode=event.is_live_mode,
                zatca_status=str((zatca_result or {}).get("status", "pending")),
                onboarding_id=onboarding_id,
                founder_alert_id=alert_id,
                occurred_at=event.occurred_at,
            )
            self._session.add(record)
            await self._session.flush()
            log.info(
                "payment_saved",
                payment_id=event.payment_id,
                status=event.status,
                record_id=record.id,
            )
            return record.id
        except Exception as exc:
            log.warning(
                "payment_save_failed", payment_id=getattr(event, "payment_id", "?"), error=str(exc)
            )
            return None

    async def get_by_account(self, account_id: str) -> list[dict[str, Any]]:
        """Return all payments for an account, newest first."""
        try:
            from db.models import PaymentRecordDB

            stmt = (
                select(PaymentRecordDB)
                .where(PaymentRecordDB.account_id == account_id)
                .order_by(PaymentRecordDB.occurred_at.desc())
            )
            result = await self._session.execute(stmt)
            rows = result.scalars().all()
            return [_payment_to_dict(r) for r in rows]
        except Exception as exc:
            log.warning("payment_get_by_account_failed", account_id=account_id, error=str(exc))
            return []

    async def get_mrr_by_month(self, tiers: list[str] | None = None) -> list[dict[str, Any]]:
        """
        Return paid payment totals grouped by month.

        Parameters
        ----------
        tiers:
            If provided, filter to these service_tier values (substring match).
        """
        try:
            from db.models import PaymentRecordDB

            stmt = select(PaymentRecordDB).where(PaymentRecordDB.status == "paid")
            result = await self._session.execute(stmt)
            rows = result.scalars().all()

            monthly: dict[str, float] = {}
            for r in rows:
                if tiers:
                    if not any(t in r.service_tier for t in tiers):
                        continue
                month_key = r.occurred_at.strftime("%Y-%m") if r.occurred_at else "unknown"
                monthly[month_key] = monthly.get(month_key, 0.0) + r.amount_sar

            return [
                {"month": k, "mrr_sar": round(v, 2), "arr_sar": round(v * 12, 2)}
                for k, v in sorted(monthly.items())
            ]
        except Exception as exc:
            log.warning("payment_get_mrr_failed", error=str(exc))
            return []


def _payment_to_dict(row: Any) -> dict[str, Any]:
    return {
        "id": row.id,
        "payment_id": row.payment_id,
        "invoice_id": row.invoice_id,
        "status": row.status,
        "amount_sar": row.amount_sar,
        "amount_halalas": row.amount_halalas,
        "service_tier": row.service_tier,
        "account_id": row.account_id,
        "is_live_mode": row.is_live_mode,
        "zatca_status": row.zatca_status,
        "onboarding_id": row.onboarding_id,
        "founder_alert_id": row.founder_alert_id,
        "occurred_at": row.occurred_at.isoformat() if row.occurred_at else None,
        "processed_at": row.processed_at.isoformat() if row.processed_at else None,
    }


# ── OnboardingRepository ──────────────────────────────────────────────────────


class OnboardingRepository:
    """Persist onboarding state transitions."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_record(
        self,
        onboarding_id: str,
        account_id: str,
        stage: str,
        tier: str,
    ) -> str | None:
        """
        Insert a new onboarding record.

        Returns the db record id on success, None on failure.
        """
        try:
            from db.models import OnboardingRecordDB

            record = OnboardingRecordDB(
                id=_new_id("obr"),
                onboarding_id=onboarding_id,
                account_id=account_id,
                current_stage=stage,
                service_tier=tier,
            )
            self._session.add(record)
            await self._session.flush()
            log.info(
                "onboarding_record_saved",
                onboarding_id=onboarding_id,
                stage=stage,
                record_id=record.id,
            )
            return record.id
        except Exception as exc:
            log.warning(
                "onboarding_record_save_failed",
                onboarding_id=onboarding_id,
                error=str(exc),
            )
            return None

    async def advance_stage(
        self, onboarding_id: str, stage: str
    ) -> dict[str, Any] | None:
        """
        Move an onboarding record to a new stage and stamp the relevant timestamp.

        Returns the updated record dict, or None on failure.
        """
        _STAGE_TIMESTAMPS = {
            "welcome": "welcome_sent_at",
            "intake": "intake_completed_at",
            "setup": "setup_completed_at",
            "first_value": "first_value_at",
            "anchored": "anchored_at",
        }
        try:
            from db.models import OnboardingRecordDB

            stmt = select(OnboardingRecordDB).where(
                OnboardingRecordDB.onboarding_id == onboarding_id
            )
            result = await self._session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                log.warning("onboarding_record_not_found", onboarding_id=onboarding_id)
                return None
            row.current_stage = stage
            row.updated_at = datetime.now(UTC)
            ts_field = _STAGE_TIMESTAMPS.get(stage)
            if ts_field and getattr(row, ts_field, None) is None:
                setattr(row, ts_field, datetime.now(UTC))
            await self._session.flush()
            log.info("onboarding_stage_advanced", onboarding_id=onboarding_id, stage=stage)
            return _onboarding_to_dict(row)
        except Exception as exc:
            log.warning(
                "onboarding_advance_stage_failed",
                onboarding_id=onboarding_id,
                error=str(exc),
            )
            return None

    async def get_by_onboarding_id(self, onboarding_id: str) -> dict[str, Any] | None:
        """Fetch an onboarding record by its business onboarding_id."""
        try:
            from db.models import OnboardingRecordDB

            stmt = select(OnboardingRecordDB).where(
                OnboardingRecordDB.onboarding_id == onboarding_id
            )
            result = await self._session.execute(stmt)
            row = result.scalar_one_or_none()
            return _onboarding_to_dict(row) if row else None
        except Exception as exc:
            log.warning(
                "onboarding_get_failed", onboarding_id=onboarding_id, error=str(exc)
            )
            return None


def _onboarding_to_dict(row: Any) -> dict[str, Any]:
    return {
        "id": row.id,
        "onboarding_id": row.onboarding_id,
        "account_id": row.account_id,
        "current_stage": row.current_stage,
        "service_tier": row.service_tier,
        "welcome_sent_at": row.welcome_sent_at.isoformat() if row.welcome_sent_at else None,
        "intake_completed_at": (
            row.intake_completed_at.isoformat() if row.intake_completed_at else None
        ),
        "setup_completed_at": (
            row.setup_completed_at.isoformat() if row.setup_completed_at else None
        ),
        "first_value_at": row.first_value_at.isoformat() if row.first_value_at else None,
        "anchored_at": row.anchored_at.isoformat() if row.anchored_at else None,
        "is_overdue": row.is_overdue,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }
