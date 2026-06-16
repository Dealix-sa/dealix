#!/usr/bin/env python3
"""
AI Tier Burndown — weekly status of the 12 AI tiers.

Reads `dealix/registers/ai_tier_burndown.yaml`, computes per-tier completion %,
gate readiness, and blocked items, and prints a structured report.

Usage:
  python3 scripts/ai_tier_burndown.py
  python3 scripts/ai_tier_burndown.py --tier 3
  python3 scripts/ai_tier_burndown.py --gate-day 30
  python3 scripts/ai_tier_burndown.py --json   # machine-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REGISTER_PATH = Path(__file__).resolve().parent.parent / "dealix" / "registers" / "ai_tier_burndown.yaml"

STATUS_WEIGHT = {
    "planned": 0,
    "scaffolded": 10,
    "in_progress": 50,
    "verifying": 80,
    "PASS": 100,
}


def load() -> dict[str, Any]:
    if not REGISTER_PATH.exists():
        sys.exit(f"register not found: {REGISTER_PATH}")
    with REGISTER_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def tier_progress(tier: dict[str, Any]) -> int:
    deliverables = tier.get("deliverables", [])
    if not deliverables:
        return 0
    total = sum(STATUS_WEIGHT.get(d.get("status", "planned"), 0) for d in deliverables)
    return total // len(deliverables)


def gate_status(register: dict[str, Any], gate: dict[str, Any]) -> tuple[str, list[int]]:
    required = gate.get("tiers_required", [])
    tier_map = {t["id"]: t for t in register.get("tiers", [])}
    pending: list[int] = []
    for tier_id in required:
        tier = tier_map.get(tier_id, {})
        if tier_progress(tier) < 100:
            pending.append(tier_id)
    if not pending:
        return "READY", []
    return "BLOCKED", pending


def human_report(register: dict[str, Any]) -> str:
    out: list[str] = []
    out.append("═" * 70)
    out.append("DEALIX AI TIER BURNDOWN")
    out.append(f"Plan horizon: {register.get('plan_horizon_days')} days · Mode: {register.get('execution_mode')}")
    out.append(f"Last reviewed: {register.get('last_reviewed')} · AI lead: {register.get('ai_lead')}")
    out.append("═" * 70)
    out.append("")

    out.append("── TIER STATUS ──")
    for tier in register.get("tiers", []):
        pct = tier_progress(tier)
        bar = "█" * (pct // 5) + "·" * (20 - pct // 5)
        out.append(
            f"  T{tier['id']:>2} D{tier['gate_day']:>3}  [{bar}] {pct:>3}%  {tier['name']:<28} status={tier['status']}"
        )
    out.append("")

    out.append("── GATE STATUS ──")
    for gate in register.get("gates", []):
        status, pending = gate_status(register, gate)
        flag = "✓" if status == "READY" else "✗"
        out.append(f"  {flag} Day {gate['day']:>3} — {gate['name']:<48} {status}")
        if pending:
            out.append(f"        pending tiers: {pending}")
    out.append("")

    out.append("── PRIORITY NOTES ──")
    for tier in register.get("tiers", []):
        if tier.get("priority_note"):
            out.append(f"  T{tier['id']}: {tier['priority_note']}")
    out.append("")

    out.append("═" * 70)
    return "\n".join(out)


def json_report(register: dict[str, Any]) -> str:
    tiers = []
    for tier in register.get("tiers", []):
        tiers.append(
            {
                "id": tier["id"],
                "name": tier["name"],
                "gate_day": tier["gate_day"],
                "status": tier["status"],
                "progress_pct": tier_progress(tier),
                "deliverables_count": len(tier.get("deliverables", [])),
            }
        )
    gates = []
    for gate in register.get("gates", []):
        status, pending = gate_status(register, gate)
        gates.append(
            {
                "day": gate["day"],
                "name": gate["name"],
                "status": status,
                "pending_tiers": pending,
            }
        )
    return json.dumps(
        {
            "plan_horizon_days": register.get("plan_horizon_days"),
            "execution_mode": register.get("execution_mode"),
            "last_reviewed": register.get("last_reviewed"),
            "tiers": tiers,
            "gates": gates,
        },
        indent=2,
        ensure_ascii=False,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="AI tier burndown report")
    p.add_argument("--tier", type=int, help="filter to a single tier ID")
    p.add_argument("--gate-day", type=int, help="filter to a single gate day")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args()

    register = load()

    if args.tier is not None:
        register["tiers"] = [t for t in register.get("tiers", []) if t["id"] == args.tier]
    if args.gate_day is not None:
        register["gates"] = [g for g in register.get("gates", []) if g["day"] == args.gate_day]

    if args.json:
        print(json_report(register))
    else:
        print(human_report(register))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
