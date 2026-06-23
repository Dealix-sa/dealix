"""Ingest a company profile into the Company Brain OS.

The profile is a simple mapping of company facts (sector, stage, headcount,
revenue band, key metrics, focus areas). Ingestion normalises the profile and
optionally appends a row to ``ledgers/company_signals.csv``.

This module makes no future predictions — it only records observed facts.
"""
from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from typing import Any

LEDGER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "ledgers",
    "company_signals.csv",
)

REQUIRED_PROFILE_KEYS = ("company_name", "sector", "stage")


def ingest_company_profile(profile: dict[str, Any], ledger_path: str | None = None) -> dict[str, Any]:
    """Normalise and ingest a company profile.

    Returns the normalised profile. When ``profile`` contains a ``signals``
    list, each signal is appended to ``ledgers/company_signals.csv``.
    """
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dict")

    missing = [k for k in REQUIRED_PROFILE_KEYS if not profile.get(k)]
    if missing:
        raise ValueError(f"company profile missing required keys: {missing}")

    normalised: dict[str, Any] = {
        "company_name": str(profile["company_name"]).strip(),
        "sector": str(profile["sector"]).strip(),
        "stage": str(profile["stage"]).strip(),
        "headcount": profile.get("headcount"),
        "revenue_band": profile.get("revenue_band"),
        "focus_areas": list(profile.get("focus_areas", [])),
        "key_metrics": dict(profile.get("key_metrics", {})),
        "ingested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    signals = profile.get("signals", [])
    if signals:
        _append_signals(signals, ledger_path or LEDGER_PATH)

    return normalised


def _append_signals(signals: list[dict[str, Any]], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = [
        "date",
        "company_name",
        "signal_type",
        "signal_source",
        "direction",
        "strength",
        "confidence",
        "notes",
    ]
    write_header = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for sig in signals:
            row = {f: sig.get(f, "") for f in fieldnames}
            if not row.get("date"):
                row["date"] = datetime.now(timezone.utc).date().isoformat()
            writer.writerow(row)


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("usage: python -m scripts.brain.ingest_company_profile <profile.json>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        data = json.load(fh)
    result = ingest_company_profile(data)
    print(json.dumps(result, indent=2, default=str))