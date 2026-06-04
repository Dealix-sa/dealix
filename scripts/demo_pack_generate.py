#!/usr/bin/env python3
"""Generate a safe, sandbox-only demo pack for a founder-led demo.

Reads config/demo_scenarios.json and data/demo_companies.example.jsonl (sample
data only — never real customer data) and writes a dated pack under
outputs/demo_packs/YYYY-MM-DD/:
  * demo_script.md
  * demo_companies.jsonl
  * vertical_demo_map.md
  * founder_demo_notes.md

No external sending, no secrets, no live customer integration.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = REPO / "config" / "demo_scenarios.json"
COMPANIES_PATH = REPO / "data" / "demo_companies.example.jsonl"


def load_scenarios() -> dict:
    return json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))


def load_companies() -> list[dict]:
    rows: list[dict] = []
    for line in COMPANIES_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def build_demo_script(scenarios: dict) -> str:
    lines = ["# Demo Script (AR/EN) — Sandbox Only", ""]
    lines.append("> Sample/sandbox data only. Not connected to any real customer data.")
    lines.append("> بيانات عينة فقط. غير متصلة بأي بيانات عميل حقيقية.")
    lines.append("")
    for s in scenarios["scenarios"]:
        lines.append(f"## {s['title_en']} / {s['title_ar']}")
        lines.append("")
        lines.append(f"- Sector: {s['sector']}")
        lines.append(f"- Pain (EN): {s['pain_en']}")
        lines.append(f"- Pain (AR): {s['pain_ar']}")
        lines.append(f"- Workflow: {s['workflow']}")
        lines.append(f"- Next step: {s['next_step']} (founder-confirmed)")
        lines.append("")
    lines.append("---")
    lines.append("Close every demo on the paid diagnostic. Founder confirms manually.")
    return "\n".join(lines) + "\n"


def build_vertical_map(scenarios: dict, companies: list[dict]) -> str:
    by_sector: dict[str, list[str]] = {}
    for c in companies:
        by_sector.setdefault(c["sector"], []).append(c["name"])
    lines = ["# Vertical Demo Map", ""]
    for s in scenarios["scenarios"]:
        sector = s["sector"]
        names = by_sector.get(sector, [])
        lines.append(f"- **{sector}** → scenario `{s['id']}` → samples: {', '.join(names) or 'n/a'}")
    return "\n".join(lines) + "\n"


def build_founder_notes(scenarios: dict) -> str:
    lines = ["# Founder Demo Notes", ""]
    lines.append("- Use sandbox data only; never load real customer data.")
    lines.append("- Frame value as expected and measured — never guaranteed.")
    lines.append("- Do not auto-book; confirm the next step manually.")
    lines.append(f"- Scenarios available: {len(scenarios['scenarios'])}")
    lines.append("- After the demo, queue any follow-up draft for your own approval.")
    return "\n".join(lines) + "\n"


def generate(out_root: Path | None = None, pack_date: str | None = None) -> Path:
    scenarios = load_scenarios()
    companies = load_companies()
    day = pack_date or date.today().isoformat()
    out_dir = (out_root or (REPO / "outputs" / "demo_packs")) / day
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "demo_script.md").write_text(build_demo_script(scenarios), encoding="utf-8")
    (out_dir / "demo_companies.jsonl").write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in companies) + "\n",
        encoding="utf-8",
    )
    (out_dir / "vertical_demo_map.md").write_text(
        build_vertical_map(scenarios, companies), encoding="utf-8")
    (out_dir / "founder_demo_notes.md").write_text(
        build_founder_notes(scenarios), encoding="utf-8")
    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a sandbox demo pack.")
    parser.add_argument("--date", default=None, help="Override pack date (YYYY-MM-DD).")
    args = parser.parse_args()
    out_dir = generate(pack_date=args.date)
    print(f"demo pack generated at {out_dir}")
    for f in sorted(out_dir.iterdir()):
        print(f"  - {f.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
