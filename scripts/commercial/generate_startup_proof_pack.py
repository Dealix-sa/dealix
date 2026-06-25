#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STARTUP = ROOT / "reports" / "startup_command_center" / "latest.json"
BRIEF = ROOT / "reports" / "founder_daily_brief" / "latest.json"
OUT = ROOT / "reports" / "startup_proof_pack"


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def markdown(payload: dict) -> str:
    lines = [
        "# Dealix Startup Proof Pack",
        "",
        "## Purpose",
        "",
        "This proof pack documents what the Startup OS generated today and what the founder should review next.",
        "",
        "## Generated assets",
        "",
    ]
    for asset in payload["generated_assets"]:
        lines.append(f"- {asset}")
    lines += ["", "## Proof metrics", ""]
    for key, value in payload["proof_metrics"].items():
        lines.append(f"- {key}: {value}")
    lines += ["", "## Next proof actions", ""]
    for action in payload["next_proof_actions"]:
        lines.append(f"- {action}")
    return "\n".join(lines) + "\n"


def main() -> int:
    startup = load_json(STARTUP, {})
    brief = load_json(BRIEF, {})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "proof_only",
        "generated_assets": [
            "reports/commercial/sales_agent_company_brain/latest.md",
            "reports/commercial/review_actions/latest.md",
            "reports/startup_command_center/latest.md",
            "reports/founder_daily_brief/latest.md",
        ],
        "proof_metrics": {
            "products_ready": len(startup.get("products", [])),
            "targets_loaded": startup.get("targets_loaded", 0),
            "packs_generated": startup.get("packs_generated", 0),
            "review_actions": len(startup.get("review_actions", [])),
            "founder_actions": len(brief.get("founder_actions", [])),
        },
        "next_proof_actions": [
            "Record which accounts were reviewed by the founder.",
            "Record which discovery attempts were prepared.",
            "Attach one scoped proposal when qualified.",
            "Add before/after evidence after each paid sprint.",
            "Summarize what improved and what remains blocked."
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown(payload), encoding="utf-8")
    print("STARTUP_PROOF_PACK=reports/startup_proof_pack/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
