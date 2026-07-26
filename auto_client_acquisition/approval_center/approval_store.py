"""Thread-safe in-memory ApprovalStore, and the default-store factory.

The in-memory store below is the reference implementation and remains the
backend for tests and for runs with no database. ``get_default_approval_store``
now prefers the durable Postgres backend whenever ``DATABASE_URL`` is set: the
queue previously lived only in process memory, so every restart or deploy
silently discarded pending approvals.

The public methods (``create``, ``approve``, ``reject``, ``edit``,
``list_pending``, ``list_history``, ``get``, ``bulk_approve``,
``expire_overdue``, ``create_with_founder_rules``, ``clear``) are the contract
both backends implement; ``tests/test_approval_store_durability.py`` pins that
they stay in step.
"""
from __future__ import annotations

import logging
import os
import threading
from collections.abc import Mapping
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

log = logging.getLogger(__name__)


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


# Module-level singleton (process-scoped).
_DEFAULT: Any | None = None


def resolve_backend_name(env: Mapping[str, str] | None = None) -> str:
    """Decide which backend the default store should use.

    Postgres whenever a database is configured, because an approval queue that
    loses its contents on restart is not an approval queue — a founder who
    approved a batch before a deploy would find the queue empty afterwards and
    have no way to tell whether the work went out.

    ``APPROVAL_STORE_BACKEND`` overrides the decision in either direction.

    Test runs stay in memory even with a database configured. The sync URL
    derived from ``DATABASE_URL`` points at a shared file, so a durable default
    would leak approvals between tests and between runs — order-dependent
    failures in the approval path are a poor trade for durability that no test
    is asserting. Tests that need the durable store build it directly.
    """
    e = env if env is not None else os.environ
    explicit = (e.get("APPROVAL_STORE_BACKEND") or "").strip().lower()
    if explicit in {"memory", "in_memory"}:
        return "in_memory"
    if explicit in {"postgres", "postgresql", "sql"}:
        return "postgres"

    if (e.get("APP_ENV") or "").strip().lower() == "test":
        return "in_memory"

    return "postgres" if (e.get("DATABASE_URL") or "").strip() else "in_memory"


def _sync_database_url(raw: str) -> str:
    """Convert an async SQLAlchemy URL to the sync driver this store uses.

    The app runs on asyncpg/aiosqlite, but PostgresApprovalStore is synchronous;
    handing it an async URL raises at connect time.
    """
    for async_driver, sync_driver in (
        ("postgresql+asyncpg", "postgresql+psycopg2"),
        ("sqlite+aiosqlite", "sqlite"),
    ):
        if raw.startswith(async_driver):
            return raw.replace(async_driver, sync_driver, 1)
    return raw


def get_default_approval_store() -> Any:
    """Return the process-wide approval store.

    Falls back to the in-memory store if the Postgres backend cannot be
    constructed. That is a deliberate availability choice: losing durability is
    bad, but refusing to boot the approval surface entirely would be worse —
    and the degraded backend is reported by ``/api/v1/approvals/status`` rather
    than hidden.
    """
    global _DEFAULT
    if _DEFAULT is not None:
        return _DEFAULT

    if resolve_backend_name() == "postgres":
        try:
            from auto_client_acquisition.approval_center.postgres_store import (
                PostgresApprovalStore,
            )

            _DEFAULT = PostgresApprovalStore(
                database_url=_sync_database_url(os.environ.get("DATABASE_URL", ""))
            )
            return _DEFAULT
        except Exception as exc:  # broad by design: must not break the surface
            log.warning(
                "approval_store_postgres_unavailable falling_back_to_memory error=%s",
                exc,
            )

    _DEFAULT = ApprovalStore()
    return _DEFAULT


def reset_default_approval_store() -> None:
    """Drop the cached singleton. Used by tests to simulate a process restart."""
    global _DEFAULT
    _DEFAULT = None


def describe_default_backend() -> str:
    """Report the backend actually in use, not the one that was intended."""
    store = get_default_approval_store()
    return "postgres" if type(store).__name__ == "PostgresApprovalStore" else "in_memory"
