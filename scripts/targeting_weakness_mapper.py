#!/usr/bin/env python3
"""Weakness mapper — answers "what problem can Dealix actually solve here?".

Scoring tells us a company is worth pursuing. Weakness mapping tells us *why* and
*with which OS*. It reads the observable pain signals on a company profile and
infers ranked weaknesses, each tied to a Dealix OS angle.

Weakness types → OS angle:
    revenue_leakage    → revenue_os
    proof_gap          → proof_os
    command_fog        → command_os
    delivery_blindness → delivery_os
    client_memory_gap  → client_os
    support_recurrence → support_os
    data_fragmentation → data_os
    governance_risk    → governance_os
    partner_potential  → partner_os

Usage:
    python scripts/targeting_weakness_mapper.py --in data/targeting/company_master.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.targeting_common import COMPANY_MASTER, load_companies, load_sectors, load_signals

# Canonical weakness → OS angle map (the spine of the offer router too).
WEAKNESS_TO_OS = {
    "revenue_leakage": "revenue_os",
    "proof_gap": "proof_os",
    "command_fog": "command_os",
    "delivery_blindness": "delivery_os",
    "client_memory_gap": "client_os",
    "support_recurrence": "support_os",
    "data_fragmentation": "data_os",
    "governance_risk": "governance_os",
    "partner_potential": "partner_os",
}

WEAKNESS_LABEL_AR = {
    "revenue_leakage": "تسرّب إيراد",
    "proof_gap": "فجوة إثبات",
    "command_fog": "ضبابية قيادة",
    "delivery_blindness": "عمى تسليم",
    "client_memory_gap": "فجوة ذاكرة عميل",
    "support_recurrence": "تكرار دعم",
    "data_fragmentation": "تشظّي بيانات",
    "governance_risk": "مخاطرة حوكمة",
    "partner_potential": "إمكانية شراكة",
}


def map_weaknesses(
    company: dict[str, Any],
    *,
    signals: dict[str, Any] | None = None,
    sectors: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return ranked weaknesses for a company.

    Each weakness has: type, os_angle, weight (sum of triggering signal points),
    evidence (the signal field names that fired), and a label.
    """
    signals = signals or load_signals()
    sectors = sectors or load_sectors()

    tally: dict[str, dict[str, Any]] = {}

    def add(weakness: str, points: float, evidence: str) -> None:
        slot = tally.setdefault(
            weakness,
            {"type": weakness, "os_angle": WEAKNESS_TO_OS.get(weakness, "command_os"),
             "weight": 0.0, "evidence": [], "label_ar": WEAKNESS_LABEL_AR.get(weakness, weakness)},
        )
        slot["weight"] += points
        slot["evidence"].append(evidence)

    # Pain + partner signals carry weakness mappings in signals.yml.
    for group in ("pain_signals", "partner_signal"):
        for sig_name, sig in signals.get(group, {}).items():
            weakness = sig.get("weakness")
            if weakness and company.get(sig_name):
                add(weakness, float(sig.get("points", 0)), sig_name)

    ranked = sorted(tally.values(), key=lambda w: w["weight"], reverse=True)

    # Fallback: no observable weakness → lean on the sector's default angle, but
    # mark it as a hypothesis (low confidence) so drafts stay honest.
    if not ranked:
        sector = sectors.get(company.get("sector") or "", {})
        angle = sector.get("default_angle", "command_os")
        weakness = next((w for w, os in WEAKNESS_TO_OS.items() if os == angle), "command_fog")
        ranked = [{
            "type": weakness, "os_angle": angle, "weight": 0.0,
            "evidence": [], "label_ar": WEAKNESS_LABEL_AR.get(weakness, weakness),
            "hypothesis": True,
        }]

    return {
        "company_name": company.get("company_name"),
        "primary_weakness": ranked[0]["type"],
        "primary_os_angle": ranked[0]["os_angle"],
        "weaknesses": ranked,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix weakness mapper")
    ap.add_argument("--in", dest="infile", default=str(COMPANY_MASTER))
    args = ap.parse_args(argv)

    companies = load_companies(Path(args.infile))
    mapped = [map_weaknesses(c) for c in companies]
    print(json.dumps(mapped, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
