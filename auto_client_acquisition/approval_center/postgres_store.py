"""Postgres JSONB snapshot store for approval center (Wave 1 cutover)."""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

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


class _ApprovalStoreBase(DeclarativeBase):
    pass


class ApprovalCenterSnapshotORM(_ApprovalStoreBase):
    __tablename__ = "approval_center_snapshots"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default="default")
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PostgresApprovalStore:
    """JSONB blob backing store — same public contract as :class:`ApprovalStore`."""

    SNAPSHOT_ID = "default"

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        self._lock = threading.Lock()
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True, pool_pre_ping=True)
        self._engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        if create_tables:
            _ApprovalStoreBase.metadata.create_all(self._engine)

    def _read_items(self) -> dict[str, ApprovalRequest]:
        with self._sessionmaker() as session:
            row = session.get(ApprovalCenterSnapshotORM, self.SNAPSHOT_ID)
            if row is None or not isinstance(row.data, dict):
                return {}
            raw = row.data.get("items") or {}
        items: dict[str, ApprovalRequest] = {}
        for aid, payload in raw.items():
            if isinstance(payload, dict):
                items[aid] = ApprovalRequest.model_validate(payload)
        return items

    def _write_items(self, items: dict[str, ApprovalRequest]) -> None:
        now = datetime.now(UTC)
        blob = {
            "items": {aid: req.model_dump(mode="json") for aid, req in items.items()},
        }
        with self._sessionmaker() as session:
            row = session.get(ApprovalCenterSnapshotORM, self.SNAPSHOT_ID)
            if row is None:
                row = ApprovalCenterSnapshotORM(
                    id=self.SNAPSHOT_ID,
                    data=blob,
                    updated_at=now,
                )
                session.add(row)
            else:
                row.data = blob
                row.updated_at = now
            session.commit()

    def create(self, req: ApprovalRequest) -> ApprovalRequest:
        evaluate_safety(req)
        with self._lock:
            items = self._read_items()
            items[req.approval_id] = req
            self._write_items(items)
        return req

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._read_items().get(approval_id)

    def list_pending(self) -> list[ApprovalRequest]:
        with self._lock:
            rows = [
                r
                for r in self._read_items().values()
                if ApprovalStatus(r.status) == ApprovalStatus.PENDING
            ]
        rows.sort(key=lambda r: r.created_at)
        return rows

    def list_history(self, limit: int = 50) -> list[ApprovalRequest]:
        limit = max(1, min(int(limit), 500))
        with self._lock:
            rows = list(self._read_items().values())
        rows.sort(key=lambda r: r.updated_at, reverse=True)
        return rows[:limit]

    def approve(self, approval_id: str, who: str) -> ApprovalRequest:
        with self._lock:
            items = self._read_items()
            req = self._require(items, approval_id)
            assert_can_approve(req)
            req.status = ApprovalStatus.APPROVED
            req.edit_history.append(self._audit_entry(who, "approve", {}))
            req.updated_at = datetime.now(UTC)
            items[approval_id] = req
            self._write_items(items)
        return req

    def reject(self, approval_id: str, who: str, reason: str) -> ApprovalRequest:
        with self._lock:
            items = self._read_items()
            req = self._require(items, approval_id)
            assert_can_reject(req)
            req.status = ApprovalStatus.REJECTED
            req.reject_reason = reason
            req.edit_history.append(self._audit_entry(who, "reject", {"reason": reason}))
            req.updated_at = datetime.now(UTC)
            items[approval_id] = req
            self._write_items(items)
        return req

    def edit(
        self,
        approval_id: str,
        who: str,
        patch: dict[str, Any],
    ) -> ApprovalRequest:
        allowed = {
            "summary_ar",
            "summary_en",
            "channel",
            "proof_impact",
            "risk_level",
            "action_mode",
            "expires_at",
        }
        with self._lock:
            items = self._read_items()
            req = self._require(items, approval_id)
            assert_can_edit(req)
            applied: dict[str, Any] = {}
            for key, value in patch.items():
                if key in allowed:
                    setattr(req, key, value)
                    applied[key] = value
            evaluate_safety(req)
            req.edit_history.append(self._audit_entry(who, "edit", {"patch": applied}))
            req.updated_at = datetime.now(UTC)
            items[approval_id] = req
            self._write_items(items)
        return req

    def expire_overdue(self) -> int:
        """Sweep pending requests whose expires_at has passed (pending → expired).

        Contract parity with :class:`ApprovalStore.expire_overdue`. Returns the
        count of expired items; persists only when something changed.
        """
        now = datetime.now(UTC)
        expired_count = 0
        with self._lock:
            items = self._read_items()
            for req in items.values():
                if (
                    ApprovalStatus(req.status) == ApprovalStatus.PENDING
                    and req.expires_at is not None
                    and req.expires_at < now
                ):
                    req.status = ApprovalStatus.EXPIRED
                    req.updated_at = now
                    req.edit_history.append(self._audit_entry("system", "expire", {}))
                    expired_count += 1
            if expired_count:
                self._write_items(items)
        return expired_count

    def bulk_approve(
        self,
        *,
        who: str,
        proof_impact_prefix: str | None = None,
        approval_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Bulk-approve pending requests by ids or proof_impact prefix.

        Contract parity with :class:`ApprovalStore.bulk_approve`.
        """
        approved: list[str] = []
        failed: list[dict[str, Any]] = []
        with self._lock:
            items = self._read_items()
            if approval_ids:
                candidates = [r for r in items.values() if r.approval_id in approval_ids]
            elif proof_impact_prefix:
                candidates = [
                    r
                    for r in items.values()
                    if (r.proof_impact or "").startswith(proof_impact_prefix)
                    and ApprovalStatus(r.status) == ApprovalStatus.PENDING
                ]
            else:
                return {
                    "approved": [],
                    "failed": [],
                    "total": 0,
                    "reason": "either approval_ids or proof_impact_prefix required",
                }
            for req in candidates:
                try:
                    assert_can_approve(req)
                    req.status = ApprovalStatus.APPROVED
                    req.edit_history.append(self._audit_entry(who, "bulk_approve", {}))
                    req.updated_at = datetime.now(UTC)
                    approved.append(req.approval_id)
                except Exception as e:  # noqa: BLE001 — surface per-item reason
                    failed.append({"id": req.approval_id, "reason": str(e)})
            if approved:
                self._write_items(items)
        return {"approved": approved, "failed": failed, "total": len(approved) + len(failed)}

    def clear(self) -> None:
        """Test helper — wipe all stored approvals (contract parity)."""
        with self._lock:
            self._write_items({})

    @staticmethod
    def _require(items: dict[str, ApprovalRequest], approval_id: str) -> ApprovalRequest:
        req = items.get(approval_id)
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
