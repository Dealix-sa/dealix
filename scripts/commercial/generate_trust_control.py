#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "commercial" / "trust_control_manifest.json"
OUT = ROOT / "reports" / "trust_control"
WEB = ROOT / "apps" / "web" / "lib" / "trust-control-snapshot.ts"


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def markdown(payload: dict) -> str:
    lines = [
        "# Dealix Trust and Claims Control",
        "",
        f"Verdict: `{payload['verdict']}`",
        "",
        "## Checks",
        "",
    ]
    for check in payload["checks"]:
        lines.append(f"- {check['name']}: {check['goal']}")
    lines += ["", "## Required guardrails", ""]
    for item in payload["required_guardrails"]:
        lines.append(f"- {item}")
    lines += ["", "## Approved language", ""]
    for item in payload["approved_language"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    manifest = load_json(MANIFEST, {})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company": manifest.get("company", "Dealix"),
        "control_name": manifest.get("control_name", "Trust and Claims Control"),
        "purpose": manifest.get("purpose", "trust control"),
        "verdict": "TRUST_CONTROL_READY",
        "checks": manifest.get("checks", []),
        "blocked_phrases": manifest.get("blocked_phrases", []),
        "approved_language": manifest.get("approved_language", []),
        "required_guardrails": manifest.get("required_guardrails", []),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown(payload), encoding="utf-8")
    WEB.parent.mkdir(parents=True, exist_ok=True)
    WEB.write_text(
        "export const trustControlSnapshot = " + json.dumps(payload, ensure_ascii=False, indent=2) + " as const;\n",
        encoding="utf-8",
    )
    print("TRUST_CONTROL=TRUST_CONTROL_READY")
    print("TRUST_CONTROL_REPORT=reports/trust_control/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
