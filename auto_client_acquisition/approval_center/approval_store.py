"""ApprovalStore — in-memory (default) and Postgres-backed variants.

This is the v6 stopgap before a Redis-backed store ships. The public
methods (``create``, ``create_with_founder_rules``, ``approve``,
``reject``, ``edit``, ``get``, ``list_pending``, ``list_history``,
``expire_overdue``, ``bulk_approve``, ``clear``) form the contract that
both the in-memory and the Postgres backend implement verbatim.

``get_default_approval_store()`` returns :class:`DbApprovalStore` when a
``DATABASE_URL`` is present in the environment so approvals survive a
process restart; tests get the fast, isolated in-memory store.
"""
from __future__ import annotations

import os
import threading
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.approval_center.approval_policy import (
    assert_can_approve,
    assert_can_edit,
    assert_can_reject,
    evaluate_safety,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from core.logging import get_logger

_log = get_logger(__name__)


class ApprovalStore:
    """Thread-safe in-memory store of ApprovalRequests."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, ApprovalRequest] = {}

    # ─── Mutations ───────────────────────────────────────────────

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        """Persist a new request. Runs safety policy at create time."""
        evaluate_safety(req)
        with self._lock:
            self._items[req.approval_id] = req
        return req

    def create_with_founder_rules(
        self,
        req: ApprovalRequest,
        *,
        confidence: float = 1.0,
        content: str = "",
        engine: Any = None,
    ) -> ApprovalRequest:
        """Persist a new request and attempt founder-rule auto-approval
        atomically (the entire safety + match + transition happens under
        the store lock so concurrent readers never observe partial state).

        Channel gates (whatsapp/linkedin/phone) and risk gates remain
        immutable — see founder_rules.py. If no rule matches, the
        request stays pending and behaves identically to ``create()``.
        """
        # Defer import to avoid a hard dependency cycle at module load.
        from auto_client_acquisition.approval_center.founder_rules_integration import (
            try_auto_approve_via_founder_rule,
        )

        evaluate_safety(req)
        with self._lock:
            # Mutate under the lock so external readers see only the
            # final pending-or-approved state, never the intermediate
            # "pending stored, approved next" race window.
            try_auto_approve_via_founder_rule(
                req,
                confidence=confidence,
                content=content,
                engine=engine,
            )
            self._items[req.approval_id] = req
        return req

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        """Mark a request approved. Raises ValueError on illegal transitions."""
        with self._lock:
            req = self._require(approval_id)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(self._audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
        return req

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        """Mark a request rejected with reason. Raises on illegal transitions."""
        with self._lock:
            req = self._require(approval_id)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(
                self._audit_entry(who, "reject", {"reason": reason})
            )
            req.updated_at = datetime.now(UTC)
        return req

    def edit(
        self,
        approval_id: str,
        who: str,
        patch: dict[str, Any],
    ) -> ApprovalRequest:
        """Apply an edit. Records the patch in ``edit_history`` without
        mutating prior entries. Only safe-list fields are patched."""
        with self._lock:
            req = self._require(approval_id)
            assert_can_edit(req)

            # Whitelist: never let an edit flip status / approval_id /
            # created_at / edit_history itself.
            allowed = {
                "summary_ar",
                "summary_en",
                "channel",
                "proof_impact",
                "risk_level",
                "action_mode",
                "expires_at",
            }
            applied: dict[str, Any] = {}
            for key, value in patch.items():
                if key in allowed:
                    setattr(req, key, value)
                    applied[key] = value

            # Re-run safety in case action_mode / risk_level changed.
            evaluate_safety(req)

            req.edit_history.append(
                self._audit_entry(who, "edit", {"patch": applied})
            )
            req.updated_at = datetime.now(UTC)
        return req

    # ─── Reads ───────────────────────────────────────────────────

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._items.get(approval_id)

    def list_pending(self) -> list[ApprovalRequest]:
        with self._lock:
            rows = [
                r for r in self._items.values()
                if ApprovalStatus(r.status) == ApprovalStatus.PENDING
            ]
        rows.sort(key=lambda r: r.created_at)
        return rows

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        """Return most-recent requests in any status, newest first."""
        limit = max(1, min(int(limit), 500))
        with self._lock:
            rows = list(self._items.values())
        rows.sort(key=lambda r: r.updated_at, reverse=True)
        return rows[:limit]

    def expire_overdue(self) -> int:
        """Sweep pending requests whose expires_at has passed.

        Flips status pending → expired. Returns count of expired items.
        Designed to be called by a background job (cron / sleeper).
        """
        now = datetime.now(UTC)
        expired_count = 0
        with self._lock:
            for req in self._items.values():
                if (
                    ApprovalStatus(req.status) == ApprovalStatus.PENDING
                    and req.expires_at is not None
                    and req.expires_at < now
                ):
                    req.status = ApprovalStatus.EXPIRED
                    req.updated_at = now
                    req.edit_history.append(
                        self._audit_entry("system", "expire", {})
                    )
                    expired_count += 1
        return expired_count

    def bulk_approve(
        self,
        *,
        who: str,
        proof_impact_prefix: str | None = None,
        approval_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Bulk-approve all pending requests matching either criterion.

        Either provide approval_ids OR proof_impact_prefix (e.g.
        "leadops:" to approve every draft from one leadops record).

        Returns {'approved': [...ids], 'failed': [{'id', 'reason'}], 'total'}.
        """
        approved: list[str] = []
        failed: list[dict[str, Any]] = []
        with self._lock:
            candidates: list[ApprovalRequest]
            if approval_ids:
                candidates = [r for r in self._items.values() if r.approval_id in approval_ids]
            elif proof_impact_prefix:
                candidates = [
                    r for r in self._items.values()
                    if (r.proof_impact or "").startswith(proof_impact_prefix)
                    and ApprovalStatus(r.status) == ApprovalStatus.PENDING
                ]
            else:
                return {"approved": [], "failed": [], "total": 0,
                        "reason": "either approval_ids or proof_impact_prefix required"}

            for req in candidates:
                try:
                    assert_can_approve(req)
                    req.status = ApprovalStatus.APPROVED
                    req.edit_history.append(
                        self._audit_entry(who, "bulk_approve", {})
                    )
                    req.updated_at = datetime.now(UTC)
                    approved.append(req.approval_id)
                except Exception as e:
                    failed.append({"id": req.approval_id, "reason": str(e)})
        return {
            "approved": approved,
            "failed": failed,
            "total": len(approved) + len(failed),
        }

    # ─── Test helpers ────────────────────────────────────────────

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    # ─── Internal ────────────────────────────────────────────────

    def _require(self, approval_id: str) -> ApprovalRequest:
        req = self._items.get(approval_id)
        if req is None:
            raise ValueError(f"approval {approval_id} not found")
        return req

    @staticmethod
    def _audit_entry(who: str, action: str, extra: dict[str, Any]) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "at": datetime.now(UTC).isoformat(),
            "who": who,
            "action": action,
        }
        entry.update(extra)
        return entry


_APPROVAL_EDIT_ALLOWED: frozenset[str] = frozenset(
    {
        "summary_ar",
        "summary_en",
        "channel",
        "proof_impact",
        "risk_level",
        "action_mode",
        "expires_at",
    }
)

# Columns persisted on ApprovalRequestRecord (the storable subset of the
# ApprovalRequest schema). Kept here so the row<->model mapping is explicit.
_APPROVAL_PERSISTED_FIELDS: tuple[str, ...] = (
    "approval_id",
    "object_type",
    "object_id",
    "action_type",
    "action_mode",
    "channel",
    "summary_ar",
    "summary_en",
    "risk_level",
    "proof_impact",
    "status",
    "reject_reason",
    "edit_history",
    "expires_at",
    "action_id",
    "lead_id",
    "customer_id",
    "due_date",
    "audit_ref",
    "proof_target",
    "created_at",
    "updated_at",
)


def _audit_entry(who: str, action: str, extra: dict[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "at": datetime.now(UTC).isoformat(),
        "who": who,
        "action": action,
    }
    entry.update(extra)
    return entry


class DbApprovalStore:
    """Postgres-backed ApprovalStore.

    Implements the exact same public contract as :class:`ApprovalStore`
    but persists every request to the ``approval_requests`` table, so
    approvals survive a process restart. Methods stay synchronous to
    mirror the in-memory store contract; persistence uses a synchronous
    SQLAlchemy engine derived from the application ``DATABASE_URL``.

    All safety / policy calls (``evaluate_safety``, ``assert_can_*``,
    founder-rule auto-approval) are preserved. Every approve / reject /
    edit also records an ``audit_logs`` row.
    """

    def __init__(self, database_url: str | None = None) -> None:
        self._lock = threading.Lock()
        self._database_url = database_url or os.environ["DATABASE_URL"]
        self._session_factory = self._build_session_factory(self._database_url)

    @staticmethod
    def _build_session_factory(database_url: str):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        from auto_client_acquisition.persistence.db_sync_url import (
            sync_sqlalchemy_url,
        )

        engine = create_engine(
            sync_sqlalchemy_url(database_url),
            pool_pre_ping=True,
        )
        return sessionmaker(engine, expire_on_commit=False)

    # ─── Row <-> schema mapping ──────────────────────────────────

    @staticmethod
    def _to_row(req: ApprovalRequest, record_cls: Any) -> Any:
        data = req.model_dump(mode="json")
        kwargs = {f: data.get(f) for f in _APPROVAL_PERSISTED_FIELDS}
        # Pydantic serialises datetimes to ISO strings via mode="json";
        # hand the ORM the native objects so DB columns get real timestamps.
        for ts_field in ("expires_at", "due_date", "created_at", "updated_at"):
            value = getattr(req, ts_field, None)
            kwargs[ts_field] = value
        kwargs["edit_history"] = list(req.edit_history)
        return record_cls(**kwargs)

    @staticmethod
    def _to_schema(row: Any) -> ApprovalRequest:
        return ApprovalRequest(
            approval_id=row.approval_id,
            object_type=row.object_type,
            object_id=row.object_id,
            action_type=row.action_type,
            action_mode=row.action_mode,
            channel=row.channel,
            summary_ar=row.summary_ar,
            summary_en=row.summary_en,
            risk_level=row.risk_level,
            proof_impact=row.proof_impact,
            status=row.status,
            reject_reason=row.reject_reason,
            edit_history=list(row.edit_history or []),
            expires_at=row.expires_at,
            action_id=row.action_id,
            lead_id=row.lead_id,
            customer_id=row.customer_id,
            due_date=row.due_date,
            audit_ref=row.audit_ref,
            proof_target=row.proof_target,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    @staticmethod
    def _apply_schema_to_row(req: ApprovalRequest, row: Any) -> None:
        for field in _APPROVAL_PERSISTED_FIELDS:
            if field == "edit_history":
                row.edit_history = list(req.edit_history)
            else:
                setattr(row, field, getattr(req, field))

    def _audit(
        self,
        session: Any,
        req: ApprovalRequest,
        who: str,
        action: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        """Record an audit_logs row for an approval lifecycle transition."""
        from auto_client_acquisition.auditability_os.audit_event import (
            persist_audit_event,
        )
        from db.models import AuditLogRecord  # noqa: F401  (ensures model import)

        try:
            from uuid import uuid4

            session.add(
                AuditLogRecord(
                    id=f"audit_{uuid4().hex[:16]}",
                    tenant_id=req.customer_id or "system",
                    user_id=who,
                    action=f"approval.{action}",
                    entity_type="approval_request",
                    entity_id=req.approval_id,
                    diff=extra or None,
                    status="ok",
                )
            )
        except Exception:  # noqa: BLE001 — audit must never break the txn
            _log.warning("approval_audit_write_failed", approval_id=req.approval_id)

    # ─── Mutations ───────────────────────────────────────────────

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        """Persist a new request. Runs safety policy at create time."""
        from db.models import ApprovalRequestRecord

        evaluate_safety(req)
        with self._lock, self._session_factory() as session:
            session.add(self._to_row(req, ApprovalRequestRecord))
            session.commit()
        return req

    def create_with_founder_rules(
        self,
        req: ApprovalRequest,
        *,
        confidence: float = 1.0,
        content: str = "",
        engine: Any = None,
    ) -> ApprovalRequest:
        """Persist a new request and attempt founder-rule auto-approval.

        Channel gates (whatsapp/linkedin/phone) and risk gates remain
        immutable — see founder_rules.py. If no rule matches, the
        request stays pending and behaves identically to ``create()``.
        """
        from auto_client_acquisition.approval_center.founder_rules_integration import (
            try_auto_approve_via_founder_rule,
        )
        from db.models import ApprovalRequestRecord

        evaluate_safety(req)
        with self._lock, self._session_factory() as session:
            try_auto_approve_via_founder_rule(
                req,
                confidence=confidence,
                content=content,
                engine=engine,
            )
            session.add(self._to_row(req, ApprovalRequestRecord))
            session.commit()
        return req

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        """Mark a request approved. Raises ValueError on illegal transitions."""
        with self._lock, self._session_factory() as session:
            row = self._require(session, approval_id)
            req = self._to_schema(row)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(_audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
            self._apply_schema_to_row(req, row)
            self._audit(session, req, who, "approve")
            session.commit()
        return req

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        """Mark a request rejected with reason. Raises on illegal transitions."""
        with self._lock, self._session_factory() as session:
            row = self._require(session, approval_id)
            req = self._to_schema(row)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(_audit_entry(who, "reject", {"reason": reason}))
            req.updated_at = datetime.now(UTC)
            self._apply_schema_to_row(req, row)
            self._audit(session, req, who, "reject", {"reason": reason})
            session.commit()
        return req

    def edit(
        self,
        approval_id: str,
        who: str,
        patch: dict[str, Any],
    ) -> ApprovalRequest:
        """Apply an edit. Records the patch in ``edit_history`` without
        mutating prior entries. Only safe-list fields are patched."""
        with self._lock, self._session_factory() as session:
            row = self._require(session, approval_id)
            req = self._to_schema(row)
            assert_can_edit(req)

            applied: dict[str, Any] = {}
            for key, value in patch.items():
                if key in _APPROVAL_EDIT_ALLOWED:
                    setattr(req, key, value)
                    applied[key] = value

            # Re-run safety in case action_mode / risk_level changed.
            evaluate_safety(req)

            req.edit_history.append(_audit_entry(who, "edit", {"patch": applied}))
            req.updated_at = datetime.now(UTC)
            self._apply_schema_to_row(req, row)
            self._audit(session, req, who, "edit", {"patch": applied})
            session.commit()
        return req

    # ─── Reads ───────────────────────────────────────────────────

    def get(self, approval_id: str) -> ApprovalRequest | None:
        from db.models import ApprovalRequestRecord

        with self._lock, self._session_factory() as session:
            row = session.get(ApprovalRequestRecord, approval_id)
            return self._to_schema(row) if row is not None else None

    def list_pending(self) -> list[ApprovalRequest]:
        from sqlalchemy import select

        from db.models import ApprovalRequestRecord

        with self._lock, self._session_factory() as session:
            rows = (
                session.execute(
                    select(ApprovalRequestRecord)
                    .where(ApprovalRequestRecord.status == ApprovalStatus.PENDING.value)
                    .order_by(ApprovalRequestRecord.created_at)
                )
                .scalars()
                .all()
            )
        return [self._to_schema(r) for r in rows]

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        """Return most-recent requests in any status, newest first."""
        from sqlalchemy import select

        from db.models import ApprovalRequestRecord

        limit = max(1, min(int(limit), 500))
        with self._lock, self._session_factory() as session:
            rows = (
                session.execute(
                    select(ApprovalRequestRecord)
                    .order_by(ApprovalRequestRecord.updated_at.desc())
                    .limit(limit)
                )
                .scalars()
                .all()
            )
        return [self._to_schema(r) for r in rows]

    def expire_overdue(self) -> int:
        """Sweep pending requests whose expires_at has passed.

        Flips status pending → expired. Returns count of expired items.
        """
        from sqlalchemy import select

        from db.models import ApprovalRequestRecord

        now = datetime.now(UTC)
        expired_count = 0
        with self._lock, self._session_factory() as session:
            rows = (
                session.execute(
                    select(ApprovalRequestRecord).where(
                        ApprovalRequestRecord.status == ApprovalStatus.PENDING.value
                    )
                )
                .scalars()
                .all()
            )
            for row in rows:
                if row.expires_at is not None and _as_aware(row.expires_at) < now:
                    req = self._to_schema(row)
                    req.status = ApprovalStatus.EXPIRED
                    req.updated_at = now
                    req.edit_history.append(_audit_entry("system", "expire", {}))
                    self._apply_schema_to_row(req, row)
                    expired_count += 1
            if expired_count:
                session.commit()
        return expired_count

    def bulk_approve(
        self,
        *,
        who: str,
        proof_impact_prefix: str | None = None,
        approval_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Bulk-approve all pending requests matching either criterion.

        Returns {'approved': [...ids], 'failed': [{'id', 'reason'}], 'total'}.
        """
        from sqlalchemy import select

        from db.models import ApprovalRequestRecord

        approved: list[str] = []
        failed: list[dict[str, Any]] = []
        with self._lock, self._session_factory() as session:
            if approval_ids:
                rows = (
                    session.execute(
                        select(ApprovalRequestRecord).where(
                            ApprovalRequestRecord.approval_id.in_(approval_ids)
                        )
                    )
                    .scalars()
                    .all()
                )
            elif proof_impact_prefix:
                rows = [
                    r
                    for r in session.execute(
                        select(ApprovalRequestRecord).where(
                            ApprovalRequestRecord.status == ApprovalStatus.PENDING.value
                        )
                    )
                    .scalars()
                    .all()
                    if (r.proof_impact or "").startswith(proof_impact_prefix)
                ]
            else:
                return {
                    "approved": [],
                    "failed": [],
                    "total": 0,
                    "reason": "either approval_ids or proof_impact_prefix required",
                }

            for row in rows:
                req = self._to_schema(row)
                try:
                    assert_can_approve(req)
                    req.status = ApprovalStatus.APPROVED
                    req.edit_history.append(_audit_entry(who, "bulk_approve", {}))
                    req.updated_at = datetime.now(UTC)
                    self._apply_schema_to_row(req, row)
                    self._audit(session, req, who, "bulk_approve")
                    approved.append(req.approval_id)
                except Exception as e:  # noqa: BLE001
                    failed.append({"id": req.approval_id, "reason": str(e)})
            session.commit()
        return {
            "approved": approved,
            "failed": failed,
            "total": len(approved) + len(failed),
        }

    # ─── Test helpers ────────────────────────────────────────────

    def clear(self) -> None:
        from sqlalchemy import delete

        from db.models import ApprovalRequestRecord

        with self._lock, self._session_factory() as session:
            session.execute(delete(ApprovalRequestRecord))
            session.commit()

    # ─── Internal ────────────────────────────────────────────────

    def _require(self, session: Any, approval_id: str) -> Any:
        from db.models import ApprovalRequestRecord

        row = session.get(ApprovalRequestRecord, approval_id)
        if row is None:
            raise ValueError(f"approval {approval_id} not found")
        return row


def _as_aware(dt: datetime) -> datetime:
    """Treat a naive datetime (SQLite has no tz) as UTC for comparison."""
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=UTC)


# Module-level singleton (process-scoped).
_DEFAULT: ApprovalStore | DbApprovalStore | None = None


def get_default_approval_store() -> ApprovalStore | DbApprovalStore:
    """Return the process-wide approval store.

    Uses :class:`DbApprovalStore` (Postgres-backed, restart-safe) when a
    ``DATABASE_URL`` is configured, and the in-memory :class:`ApprovalStore`
    otherwise so tests stay fast and isolated.
    """
    global _DEFAULT
    if _DEFAULT is None:
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            try:
                _DEFAULT = DbApprovalStore(database_url)
            except Exception:  # noqa: BLE001 — never fail to start on DB hiccup
                _log.warning("db_approval_store_init_failed_using_memory")
                _DEFAULT = ApprovalStore()
        else:
            _DEFAULT = ApprovalStore()
    return _DEFAULT


def reset_default_approval_store() -> None:
    """Drop the cached store singleton — for tests that toggle DATABASE_URL."""
    global _DEFAULT
    _DEFAULT = None
