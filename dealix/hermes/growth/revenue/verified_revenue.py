"""Verified revenue ledger — every record MUST carry an evidence_pack_id."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

_LEDGER_PATH_ENV = "DEALIX_HERMES_VERIFIED_REVENUE_PATH"
_DEFAULT_PATH = Path("data/hermes/verified_revenue.jsonl")


@dataclass(frozen=True)
class VerifiedRevenueRecord:
    record_id: str
    account_id: str
    amount_sar: float
    evidence_pack_id: str
    recognized_at: float
    notes: str = ""


def _path() -> Path:
    raw = os.environ.get(_LEDGER_PATH_ENV)
    p = Path(raw) if raw else _DEFAULT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def record(account_id: str, amount_sar: float, evidence_pack_id: str, notes: str = "") -> VerifiedRevenueRecord:
    """Record verified revenue; raises ValueError when evidence_pack_id is missing."""
    if not evidence_pack_id:
        raise ValueError("evidence_pack_id required: vanity revenue is rejected")
    rec = VerifiedRevenueRecord(
        record_id=f"vrr_{uuid.uuid4().hex[:10]}",
        account_id=account_id,
        amount_sar=float(amount_sar),
        evidence_pack_id=evidence_pack_id,
        recognized_at=time.time(),
        notes=notes,
    )
    with _path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(rec), sort_keys=True) + "\n")
    return rec


def list_records(account_id: str | None = None) -> list[VerifiedRevenueRecord]:
    """Return verified revenue records, optionally filtered by account_id."""
    p = _path()
    if not p.exists():
        return []
    out: list[VerifiedRevenueRecord] = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = VerifiedRevenueRecord(**json.loads(line))
            if account_id is None or r.account_id == account_id:
                out.append(r)
    return out


def total(account_id: str | None = None) -> float:
    """Return total verified revenue, optionally filtered by account_id."""
    return sum(r.amount_sar for r in list_records(account_id))
