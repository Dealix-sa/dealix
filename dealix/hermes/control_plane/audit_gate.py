"""
AuditGate — appends an immutable record of every control-plane decision
to the audit log. Failure to append is a fatal error: the request is
rejected rather than executed un-audited.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class AuditRecord:
    audit_id: str
    request_id: str
    actor_id: str
    capability: str
    sovereignty: str
    approval_status: str
    trust_passed: bool
    data_allowed: bool
    tool_allowed: bool
    executed: bool
    outcome_recorded: bool
    findings: tuple[str, ...] = field(default_factory=tuple)
    extras: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_json(self) -> str:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["findings"] = list(self.findings)
        return json.dumps(d, ensure_ascii=False, sort_keys=True)


class AuditLog:
    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self._records.append(record)

    def all(self) -> list[AuditRecord]:
        return list(self._records)

    def by_request(self, request_id: str) -> list[AuditRecord]:
        return [r for r in self._records if r.request_id == request_id]


LOG = AuditLog()


def write(
    *,
    request_id: str,
    actor_id: str,
    capability: str,
    sovereignty: str,
    approval_status: str,
    trust_passed: bool,
    data_allowed: bool,
    tool_allowed: bool,
    executed: bool,
    outcome_recorded: bool,
    findings: tuple[str, ...] = (),
    extras: dict[str, Any] | None = None,
) -> AuditRecord:
    record = AuditRecord(
        audit_id=f"aud_{uuid.uuid4().hex[:10]}",
        request_id=request_id,
        actor_id=actor_id,
        capability=capability,
        sovereignty=sovereignty,
        approval_status=approval_status,
        trust_passed=trust_passed,
        data_allowed=data_allowed,
        tool_allowed=tool_allowed,
        executed=executed,
        outcome_recorded=outcome_recorded,
        findings=findings,
        extras=dict(extras or {}),
    )
    LOG.append(record)
    return record
