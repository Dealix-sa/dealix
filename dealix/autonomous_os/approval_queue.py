"""
Approval Queue — founder-gated queue for every external / high-risk action.

External-channel drafts (WhatsApp, email, ...) and any step above the risk
ceiling are placed here as PENDING. The Autonomous OS never decides them; the
founder approves or rejects, and only *after* approval may a downstream,
separately-audited executor act. This module holds no send capability.

Mirrors the semantics of dealix/governance/approvals.py but is file-backed so
it runs offline in cron/CI without Redis.
"""

from __future__ import annotations

import datetime as dt
import json
import uuid
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class ApprovalState(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class ApprovalItem:
    id: str
    created_at: str
    strategy_id: str
    action: str
    channel: str | None
    offer: str | None
    risk: float
    reason: str
    draft: str
    state: str = ApprovalState.PENDING.value
    decided_by: str = ""
    decided_at: str | None = None
    note: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ApprovalQueue:
    def __init__(self, root: Path | str, proof_logger: Any = None) -> None:
        self.root = Path(root) / "approvals"
        self.root.mkdir(parents=True, exist_ok=True)
        self.store = self.root / "approval_queue.json"
        # Optional ProofLogger so founder decisions become learning signal.
        # Kept as a duck-typed dependency to avoid an import cycle.
        self._proof_logger = proof_logger

    def _read(self) -> list[dict[str, Any]]:
        if not self.store.exists():
            return []
        data = json.loads(self.store.read_text(encoding="utf-8"))
        return list(data.get("items", []))

    def _write(self, items: list[dict[str, Any]]) -> None:
        self.store.write_text(
            json.dumps({"items": items}, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def submit(
        self,
        *,
        strategy_id: str,
        action: str,
        draft: str,
        reason: str,
        risk: float = 0.0,
        channel: str | None = None,
        offer: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> ApprovalItem:
        item = ApprovalItem(
            id=str(uuid.uuid4()),
            created_at=dt.datetime.now(dt.UTC).isoformat(),
            strategy_id=strategy_id,
            action=action,
            channel=channel,
            offer=offer,
            risk=risk,
            reason=reason,
            draft=draft,
            payload=payload or {},
        )
        items = self._read()
        items.append(item.to_dict())
        self._write(items)
        return item

    def list_pending(self) -> list[dict[str, Any]]:
        return [i for i in self._read() if i.get("state") == ApprovalState.PENDING.value]

    def decide(self, item_id: str, *, approved: bool, decided_by: str, note: str = "") -> bool:
        items = self._read()
        changed = False
        decided_item: dict[str, Any] | None = None
        for i in items:
            if i.get("id") == item_id and i.get("state") == ApprovalState.PENDING.value:
                i["state"] = (
                    ApprovalState.APPROVED.value if approved else ApprovalState.REJECTED.value
                )
                i["decided_by"] = decided_by
                i["decided_at"] = dt.datetime.now(dt.UTC).isoformat()
                i["note"] = note
                changed = True
                decided_item = i
                break
        if changed:
            self._write(items)
            # Emit a proof event so LearningLoop can count real outcomes.
            if self._proof_logger is not None and decided_item is not None:
                self._proof_logger.log(
                    "approval_decided",
                    {
                        "id": item_id,
                        "strategy_id": decided_item.get("strategy_id", ""),
                        "action": decided_item.get("action", ""),
                        "approved": approved,
                        "decided_by": decided_by,
                    },
                )
        return changed

    def stats(self) -> dict[str, int]:
        items = self._read()
        out = {s.value: 0 for s in ApprovalState}
        for i in items:
            out[i.get("state", ApprovalState.PENDING.value)] = (
                out.get(i.get("state", ApprovalState.PENDING.value), 0) + 1
            )
        return out
