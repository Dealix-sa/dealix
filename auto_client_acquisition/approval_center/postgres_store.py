"""Postgres-backed ApprovalStore.

Mirrors :class:`auto_client_acquisition.approval_center.approval_store.ApprovalStore`
at the public-API level so call sites swap backends without behavioural
change. The in-memory store loses the pending queue on restart; this one
survives restarts — the precondition for a credible governed autopilot.

Storage: one row per :class:`ApprovalRequest`. The full pydantic model is
persisted as a JSON ``payload`` column; a handful of scalar columns are
mirrored out for indexed querying (status, proof_impact, timestamps).

SQLAlchemy 2.0; works with sqlite for tests and Postgres in production.
The table lives on a dedicated declarative base and is auto-created
(``CREATE TABLE IF NOT EXISTS`` semantics) — it is a new, isolated table
with no foreign keys into the app schema, so this is safe on Postgres.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Engine,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

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

_EDIT_ALLOWED = {
    "summary_ar",
    "summary_en",
    "channel",
    "proof_impact",
    "risk_level",
    "action_mode",
    "expires_at",
}


class ApprovalCenterBase(DeclarativeBase):
    """Dedicated base so the approval table can bootstrap independently."""


class ApprovalRequestORM(ApprovalCenterBase):
    """Row storage for one :class:`ApprovalRequest`."""

    __tablename__ = "approval_requests"

    approval_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[str] = mapped_column(String(32), index=True, default="pending")
    proof_impact: Mapped[str] = mapped_column(String(255), index=True, default="")
    customer_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, default=lambda: datetime.now(UTC)
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    payload: Mapped[dict] = mapped_column("payload_json", JSON, default=dict)


def _audit_entry(who: str, action: str, extra: dict) -> dict:
    entry: dict = {
        "at": datetime.now(UTC).isoformat(),
        "who": who,
        "action": action,
    }
    entry.update(extra)
    return entry


def _row_from_request(req: ApprovalRequest) -> dict:
    return {
        "approval_id": req.approval_id,
        "status": str(req.status),
        "proof_impact": req.proof_impact or "",
        "customer_id": req.customer_id,
        "created_at": req.created_at,
        "updated_at": req.updated_at,
        "expires_at": req.expires_at,
        "payload": req.model_dump(mode="json"),
    }


def _request_from_row(row: ApprovalRequestORM) -> ApprovalRequest:
    return ApprovalRequest.model_validate(row.payload)


class PostgresApprovalStore:
    """SQLAlchemy-backed ApprovalStore. Same public surface as ApprovalStore."""

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True)
        self._engine: Engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        self._lock = threading.Lock()
        if create_tables:
            ApprovalCenterBase.metadata.create_all(self._engine)

    # ─── Mutations ───────────────────────────────────────────────

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        evaluate_safety(req)
        with self._lock, self._sessionmaker() as session:
            session.merge(ApprovalRequestORM(**_row_from_request(req)))
            session.commit()
        return req

    def create_with_founder_rules(
        self,
        req: ApprovalRequest,
        *,
        confidence: float = 1.0,
        content: str = "",
        engine: object = None,
    ) -> ApprovalRequest:
        from auto_client_acquisition.approval_center.founder_rules_integration import (
            try_auto_approve_via_founder_rule,
        )

        evaluate_safety(req)
        with self._lock, self._sessionmaker() as session:
            try_auto_approve_via_founder_rule(
                req, confidence=confidence, content=content, engine=engine
            )
            session.merge(ApprovalRequestORM(**_row_from_request(req)))
            session.commit()
        return req

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        with self._lock, self._sessionmaker() as session:
            row = self._require(session, approval_id)
            req = _request_from_row(row)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(_audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
            self._write(session, row, req)
            session.commit()
        return req

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        with self._lock, self._sessionmaker() as session:
            row = self._require(session, approval_id)
            req = _request_from_row(row)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(_audit_entry(who, "reject", {"reason": reason}))
            req.updated_at = datetime.now(UTC)
            self._write(session, row, req)
            session.commit()
        return req

    def edit(self, approval_id: str, who: str, patch: dict) -> ApprovalRequest:
        with self._lock, self._sessionmaker() as session:
            row = self._require(session, approval_id)
            req = _request_from_row(row)
            assert_can_edit(req)
            applied: dict = {}
            for key, value in patch.items():
                if key in _EDIT_ALLOWED:
                    setattr(req, key, value)
                    applied[key] = value
            evaluate_safety(req)
            req.edit_history.append(_audit_entry(who, "edit", {"patch": applied}))
            req.updated_at = datetime.now(UTC)
            self._write(session, row, req)
            session.commit()
        return req

    # ─── Reads ───────────────────────────────────────────────────

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock, self._sessionmaker() as session:
            row = session.get(ApprovalRequestORM, approval_id)
            return _request_from_row(row) if row is not None else None

    def list_pending(self) -> list[ApprovalRequest]:
        stmt = (
            select(ApprovalRequestORM)
            .where(ApprovalRequestORM.status == ApprovalStatus.PENDING.value)
            .order_by(ApprovalRequestORM.created_at)
        )
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_request_from_row(r) for r in rows]

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        limit = max(1, min(int(limit), 500))
        stmt = (
            select(ApprovalRequestORM)
            .order_by(ApprovalRequestORM.updated_at.desc())
            .limit(limit)
        )
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_request_from_row(r) for r in rows]

    def expire_overdue(self) -> int:
        now = datetime.now(UTC)
        stmt = select(ApprovalRequestORM).where(
            ApprovalRequestORM.status == ApprovalStatus.PENDING.value
        )
        expired = 0
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
            for row in rows:
                req = _request_from_row(row)
                if req.expires_at is not None and _aware(req.expires_at) < now:
                    req.status = ApprovalStatus.EXPIRED
                    req.updated_at = now
                    req.edit_history.append(_audit_entry("system", "expire", {}))
                    self._write(session, row, req)
                    expired += 1
            session.commit()
        return expired

    def bulk_approve(
        self,
        *,
        who: str,
        proof_impact_prefix: str | None = None,
        approval_ids: list[str] | None = None,
    ) -> dict:
        approved: list[str] = []
        failed: list[dict] = []
        with self._lock, self._sessionmaker() as session:
            if approval_ids:
                stmt = select(ApprovalRequestORM).where(
                    ApprovalRequestORM.approval_id.in_(approval_ids)
                )
            elif proof_impact_prefix:
                stmt = select(ApprovalRequestORM).where(
                    ApprovalRequestORM.status == ApprovalStatus.PENDING.value,
                    ApprovalRequestORM.proof_impact.startswith(proof_impact_prefix),
                )
            else:
                return {
                    "approved": [],
                    "failed": [],
                    "total": 0,
                    "reason": "either approval_ids or proof_impact_prefix required",
                }
            rows = session.execute(stmt).scalars().all()
            for row in rows:
                req = _request_from_row(row)
                try:
                    assert_can_approve(req)
                    req.status = ApprovalStatus.APPROVED
                    req.edit_history.append(_audit_entry(who, "bulk_approve", {}))
                    req.updated_at = datetime.now(UTC)
                    self._write(session, row, req)
                    approved.append(req.approval_id)
                except Exception as e:  # noqa: BLE001 — collected per-item
                    failed.append({"id": req.approval_id, "reason": str(e)})
            session.commit()
        return {"approved": approved, "failed": failed, "total": len(approved) + len(failed)}

    # ─── Test helpers ────────────────────────────────────────────

    def clear(self) -> None:
        with self._lock:
            ApprovalCenterBase.metadata.drop_all(self._engine)
            ApprovalCenterBase.metadata.create_all(self._engine)

    # ─── Internal ────────────────────────────────────────────────

    @staticmethod
    def _require(session: object, approval_id: str) -> ApprovalRequestORM:
        row = session.get(ApprovalRequestORM, approval_id)  # type: ignore[attr-defined]
        if row is None:
            raise ValueError(f"approval {approval_id} not found")
        return row

    @staticmethod
    def _write(session: object, row: ApprovalRequestORM, req: ApprovalRequest) -> None:
        data = _row_from_request(req)
        for key, value in data.items():
            setattr(row, key, value)
        session.add(row)  # type: ignore[attr-defined]


def _aware(dt: datetime) -> datetime:
    """Treat a naive datetime as UTC for safe comparison."""
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=UTC)


__all__ = [
    "ApprovalCenterBase",
    "ApprovalRequestORM",
    "PostgresApprovalStore",
]
