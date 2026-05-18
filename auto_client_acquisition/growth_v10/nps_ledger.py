"""NPS ledger — JSONL-backed store for the NPS-1/2/3 single-question survey.

Doctrine: NPS sends are draft-only / founder-triggered. This module ONLY
records responses the founder has manually collected (e.g. a WhatsApp
reply). It never sends a survey and never escalates automatically.

Mirrors the JSONL pattern of :mod:`auto_client_acquisition.capital_os.capital_ledger`.
Comment verbatim is PII-redacted on write — no raw customer text is stored.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

VALID_ROUNDS: frozenset[str] = frozenset(
    {"sprint_d14", "partner_m1", "partner_m3"},
)

_DEFAULT_PATH = "var/nps-ledger.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_NPS_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def nps_band(score: int) -> str:
    """Promoter (9-10) / Passive (7-8) / Detractor (0-6)."""
    if score >= 9:
        return "promoter"
    if score >= 7:
        return "passive"
    return "detractor"


@dataclass(frozen=True, slots=True)
class NpsResponse:
    """A single NPS response, recorded by the founder after a manual send."""

    response_id: str
    customer_handle: str
    nps_round: str
    score: int
    band: str
    verbatim_redacted: str = ""
    recorded_by: str = "founder"
    recorded_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def record_response(
    *,
    customer_handle: str,
    nps_round: str,
    score: int,
    verbatim: str = "",
    recorded_by: str = "founder",
) -> NpsResponse:
    """Append a founder-collected NPS response to the JSONL ledger.

    `verbatim` is PII-redacted before storage. No survey is sent here.
    """
    if not customer_handle or not customer_handle.strip():
        raise ValueError("customer_handle is required")
    if nps_round not in VALID_ROUNDS:
        raise ValueError(
            f"nps_round must be one of {sorted(VALID_ROUNDS)}",
        )
    if not isinstance(score, int) or not 0 <= score <= 10:
        raise ValueError("score must be an int in 0..10")
    response = NpsResponse(
        response_id=f"nps_{uuid.uuid4().hex[:12]}",
        customer_handle=customer_handle.strip(),
        nps_round=nps_round,
        score=score,
        band=nps_band(score),
        verbatim_redacted=redact_text(verbatim) if verbatim else "",
        recorded_by=recorded_by or "founder",
        recorded_at=datetime.now(timezone.utc).isoformat(),
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(response.to_dict(), ensure_ascii=False) + "\n")
    return response


def list_responses(
    *,
    customer_handle: str | None = None,
    nps_round: str | None = None,
    limit: int = 200,
) -> list[NpsResponse]:
    """List recorded NPS responses, optionally filtered."""
    path = _path()
    if not path.exists():
        return []
    out: list[NpsResponse] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    response = NpsResponse(**json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
                if customer_handle is not None and response.customer_handle != customer_handle:
                    continue
                if nps_round is not None and response.nps_round != nps_round:
                    continue
                out.append(response)
    return out[-limit:] if limit else out


def aggregate(*, nps_round: str | None = None) -> dict[str, Any]:
    """Compute the NPS score = %promoters - %detractors over recorded responses."""
    rows = list_responses(nps_round=nps_round, limit=100_000)
    total = len(rows)
    promoters = sum(1 for r in rows if r.band == "promoter")
    passives = sum(1 for r in rows if r.band == "passive")
    detractors = sum(1 for r in rows if r.band == "detractor")
    nps_score = (
        round((promoters / total) * 100 - (detractors / total) * 100, 1)
        if total
        else None
    )
    return {
        "responses_count": total,
        "promoters": promoters,
        "passives": passives,
        "detractors": detractors,
        "nps_score": nps_score,
    }


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "VALID_ROUNDS",
    "NpsResponse",
    "aggregate",
    "clear_for_test",
    "list_responses",
    "nps_band",
    "record_response",
]
