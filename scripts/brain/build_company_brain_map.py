"""Build a Company Brain Map — a consolidated knowledge snapshot.

The brain map assembles data from every ledger plus an ingested profile into
a single in-memory structure. It is purely descriptive: it reports observed
state, not predicted futures.
"""
from __future__ import annotations

import csv
import os
from datetime import UTC, datetime, timezone
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGERS_DIR = os.path.join(REPO_ROOT, "ledgers")

LEDGER_FILES = {
    "signals": "company_signals.csv",
    "decisions": "decisions_log.csv",
    "assumptions": "assumptions_log.csv",
    "experiments": "experiments_log.csv",
    "risks": "risk_register.csv",
    "opportunities": "opportunity_register.csv",
}


def _read_csv(path: str) -> list[dict[str, Any]]:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build_company_brain_map(profile: dict[str, Any] | None = None, ledgers_dir: str | None = None) -> dict[str, Any]:
    """Assemble a Company Brain Map from all ledgers and an optional profile."""
    base = ledgers_dir or LEDGERS_DIR
    ledgers: dict[str, list[dict[str, Any]]] = {}
    for key, fname in LEDGER_FILES.items():
        ledgers[key] = _read_csv(os.path.join(base, fname))

    brain_map: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "profile": profile or {},
        "ledgers": ledgers,
        "counts": {k: len(v) for k, v in ledgers.items()},
    }
    return brain_map


if __name__ == "__main__":
    import json

    print(json.dumps(build_company_brain_map(), indent=2, default=str))
