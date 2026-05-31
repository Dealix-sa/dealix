"""Daily KPI snapshot — composes existing sources into a single JSON.

Output shape (all numeric fields carry an is_estimate flag where the
number is not a live confirmed payment, per doctrine #8 NO_FAKE_PROOF):

  {
    "date": "2026-05-28",
    "generated_at": "2026-05-28T04:30:00+00:00",
    "revenue": {
      "today_sar":             { value, is_estimate, source },
      "mrr_sar":               { value, is_estimate, source },
      "active_subscriptions":  { value, is_estimate, source }
    },
    "pipeline": {
      "pilots_open":           { ... },
      "drafts_pending":        { ... },
      "approvals_pending":     { ... }
    },
    "trust": {
      "friction_events_7d":    { ... },
      "doctrine_violations":   { ... }
    },
    "fleet": {
      "agent_runs_24h":        { ... },
      "proof_events_24h":      { ... }
    }
  }

Written to data/kpi_snapshots/YYYY-MM-DD.json. Gitignored. Read by
GET /api/v1/metrics/kpi/today and by scripts/weekly_scorecard.py.

Composable — never sends anything externally. No live integrations
beyond what's already wired (Postgres reads, JSONL ledger reads).
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = _REPO / "data" / "kpi_snapshots"


@dataclass
class KPIField:
    value: int | float
    is_estimate: bool
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _revenue_today() -> KPIField:
    try:
        from auto_client_acquisition.payment_ops import orchestrator

        now = datetime.now(UTC)
        cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
        records: Iterable = getattr(orchestrator, "_INDEX", {}).values()
        today = [
            r
            for r in records
            if str(getattr(r, "status", "")) in ("payment_confirmed", "delivery_kickoff")
        ]
        # Filter by confirmed_at if available, else fall back to now (best effort).
        amount = 0
        for r in today:
            ts = getattr(r, "confirmed_at", None)
            if ts:
                try:
                    if datetime.fromisoformat(ts) >= cutoff:
                        amount += int(getattr(r, "amount_sar", 0))
                except Exception:
                    continue
        return KPIField(value=amount, is_estimate=False, source="payment_ops.orchestrator")
    except Exception:
        return KPIField(value=0, is_estimate=True, source="payment_ops_unavailable")


def _mrr_snapshot() -> tuple[KPIField, KPIField]:
    """Returns (mrr_sar, active_subscriptions)."""
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due

        due_iter: Iterable = list_due()  # type: ignore[assignment]
        active = [
            s
            for s in due_iter
            if str(getattr(s, "status", "")).lower() not in ("canceled", "ended", "refunded")
        ]
        unique = {getattr(s, "customer_id", ""): s for s in active}
        mrr = sum(int(getattr(s, "amount_sar", 0)) for s in unique.values())
        return (
            KPIField(value=mrr, is_estimate=True, source="renewal_scheduler.list_due"),
            KPIField(value=len(unique), is_estimate=True, source="renewal_scheduler.list_due"),
        )
    except Exception:
        return (
            KPIField(value=0, is_estimate=True, source="renewal_scheduler_unavailable"),
            KPIField(value=0, is_estimate=True, source="renewal_scheduler_unavailable"),
        )


def _drafts_pending() -> KPIField:
    try:
        from auto_client_acquisition.approval_center.approval_store import (
            get_default_approval_store,
        )

        store = get_default_approval_store()
        items = store.list_pending() if hasattr(store, "list_pending") else []
        return KPIField(
            value=len(items), is_estimate=False, source="approval_center.list_pending"
        )
    except Exception:
        return KPIField(value=0, is_estimate=True, source="approval_center_unavailable")


def _friction_events_7d() -> KPIField:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate

        agg = aggregate(customer_id="dealix_internal", window_days=7)
        return KPIField(
            value=int(getattr(agg, "total", 0)),
            is_estimate=False,
            source="friction_log.aggregator",
        )
    except Exception:
        return KPIField(value=0, is_estimate=True, source="friction_log_unavailable")


def _agent_runs_24h() -> KPIField:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate

        agg = aggregate(customer_id="dealix_internal", window_days=1)
        return KPIField(
            value=int(getattr(agg, "total", 0)),
            is_estimate=True,
            source="friction_log.aggregator (1d window proxy)",
        )
    except Exception:
        return KPIField(value=0, is_estimate=True, source="friction_log_unavailable")


def _proof_events_24h() -> KPIField:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger

        ledger = get_default_ledger()
        events = ledger.list_events(limit=200) if hasattr(ledger, "list_events") else []
        now = datetime.now(UTC)
        cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
        recent = []
        for e in events:
            ts = getattr(e, "created_at", None)
            if ts is None:
                continue
            try:
                if ts >= cutoff:
                    recent.append(e)
            except Exception:
                continue
        return KPIField(
            value=len(recent), is_estimate=False, source="proof_ledger.file_backend"
        )
    except Exception:
        return KPIField(value=0, is_estimate=True, source="proof_ledger_unavailable")


def compute_daily_kpi_snapshot() -> dict[str, Any]:
    """Compose all KPI panels into a single snapshot dict.

    Pure function — no I/O. Used by both write_snapshot() and the
    /api/v1/metrics/kpi/today endpoint.
    """
    mrr, subs = _mrr_snapshot()
    return {
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(UTC).isoformat(),
        "revenue": {
            "today_sar": _revenue_today().to_dict(),
            "mrr_sar": mrr.to_dict(),
            "active_subscriptions": subs.to_dict(),
        },
        "pipeline": {
            "approvals_pending": _drafts_pending().to_dict(),
        },
        "trust": {
            "friction_events_7d": _friction_events_7d().to_dict(),
        },
        "fleet": {
            "agent_runs_24h": _agent_runs_24h().to_dict(),
            "proof_events_24h": _proof_events_24h().to_dict(),
        },
        "doctrine_note": (
            "Drafts only, founder approves. is_estimate=True wherever a "
            "number is not backed by a confirmed Moyasar transaction."
        ),
    }


def write_snapshot(snapshot: dict[str, Any] | None = None) -> Path:
    """Persist a snapshot to data/kpi_snapshots/<date>.json."""
    snapshot = snapshot or compute_daily_kpi_snapshot()
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{snapshot['date']}.json"
    path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def read_latest_snapshot() -> dict[str, Any] | None:
    """Return the most recent snapshot, or None if no snapshot exists."""
    if not SNAPSHOT_DIR.is_dir():
        return None
    files = sorted(SNAPSHOT_DIR.glob("*.json"))
    if not files:
        return None
    try:
        return json.loads(files[-1].read_text(encoding="utf-8"))
    except Exception:
        return None


__all__ = [
    "KPIField",
    "compute_daily_kpi_snapshot",
    "read_latest_snapshot",
    "write_snapshot",
]


if __name__ == "__main__":  # pragma: no cover
    import sys

    snap = compute_daily_kpi_snapshot()
    path = write_snapshot(snap)
    print(f"OK: wrote {path.relative_to(_REPO)}")
    print(json.dumps(snap, indent=2, ensure_ascii=False)[:500])
    sys.exit(0)
