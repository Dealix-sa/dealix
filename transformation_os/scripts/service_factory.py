#!/usr/bin/env python3
"""
Dealix Transformation OS Service Factory.

Generates a client proposal pack from transformation_os/catalog/dealix_transformation_services.yaml.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Missing dependency: pyyaml. Install with: pip install pyyaml") from exc


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "transformation_os" / "catalog" / "dealix_transformation_services.yaml"
OUT_DIR = ROOT / "transformation_os" / "proposals"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u0600-\u06FF]+", "-", value)
    return value.strip("-") or "client"


def load_catalog() -> dict[str, Any]:
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_services(catalog: dict[str, Any], service_ids: list[str]) -> list[dict[str, Any]]:
    services = catalog.get("service_lines", [])
    by_id = {s["id"]: s for s in services}
    missing = [sid for sid in service_ids if sid not in by_id]
    if missing:
        valid = ", ".join(sorted(by_id))
        raise SystemExit(f"Unknown service id(s): {', '.join(missing)}\nValid ids: {valid}")
    return [by_id[sid] for sid in service_ids]


def render_proposal(client: str, sector: str, pain: str, services: list[dict[str, Any]]) -> str:
    today = dt.date.today().isoformat()

    lines: list[str] = []
    lines.append(f"# Dealix Transformation Proposal — {client}")
    lines.append("")
    lines.append(f"Generated: {today}")
    lines.append(f"Sector: {sector}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        "Dealix proposes a transformation operating system that turns scattered daily operations "
        "into measurable workflows, executive visibility, automation, and accountable team execution."
    )
    lines.append("")
    lines.append("## Client Pain")
    lines.append("")
    lines.append(pain)
    lines.append("")
    lines.append("## Recommended Transformation Stack")
    lines.append("")

    total_setup_low = 0
    total_monthly_low = 0

    for s in services:
        lines.append(f"### {s['name']}")
        lines.append("")
        lines.append(f"**Category:** {s.get('category','')}")
        lines.append("")
        lines.append(f"**Problem:** {s.get('problem','')}")
        lines.append("")
        lines.append(f"**Transformation:** {s.get('transformation','')}")
        lines.append("")
        lines.append("**Deliverables:**")
        for d in s.get("deliverables", []):
            lines.append(f"- {d}")
        lines.append("")
        lines.append(f"**Setup range:** {s.get('setup_price_sar','—')} SAR")
        lines.append(f"**Monthly range:** {s.get('monthly_price_sar','—')} SAR")
        lines.append(f"**Timeline:** {s.get('timeline_days','—')} days")
        lines.append("")

    lines.append("## Delivery Plan")
    lines.append("")
    lines.append("| Phase | Output |")
    lines.append("|---|---|")
    lines.append("| Diagnostic | Workflow map, leakage map, KPIs, data sources |")
    lines.append("| Prototype | Dashboard wireframe, workflow states, report sample |")
    lines.append("| Build | System, automations, templates, reports, SOPs |")
    lines.append("| Pilot | Live usage, feedback, first weekly report |")
    lines.append("| Scale | More workflows, integrations, governance, SLA |")
    lines.append("")
    lines.append("## Success Metrics")
    lines.append("")
    lines.append("- Lead response time")
    lines.append("- Follow-up completion rate")
    lines.append("- Overdue follow-ups")
    lines.append("- Booking/conversion rate")
    lines.append("- Lost reason visibility")
    lines.append("- Review response rate")
    lines.append("- Executive report consistency")
    lines.append("")
    lines.append("## Commercial Note")
    lines.append("")
    lines.append(
        "Final pricing depends on workflow complexity, integrations, number of users, data sources, "
        "and governance requirements. Enterprise work starts with a paid diagnostic sprint."
    )
    lines.append("")
    lines.append("## Next Step")
    lines.append("")
    lines.append("Schedule a 45-minute transformation diagnostic session.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--pain", required=True)
    parser.add_argument("--services", required=True, help="Comma-separated service ids")
    args = parser.parse_args()

    catalog = load_catalog()
    service_ids = [s.strip() for s in args.services.split(",") if s.strip()]
    selected = find_services(catalog, service_ids)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{slugify(args.client)}_transformation_proposal.md"
    out_path.write_text(render_proposal(args.client, args.sector, args.pain, selected), encoding="utf-8")

    print(f"Generated proposal: {out_path}")


if __name__ == "__main__":
    main()
