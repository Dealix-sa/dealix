#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "commercial" / "client_delivery_control_manifest.json"
OUT = ROOT / "reports" / "client_delivery_control"
WEB = ROOT / "apps" / "web" / "lib" / "client-delivery-control-snapshot.ts"


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def check_path(path: str) -> dict[str, str]:
    exists = (ROOT / path).exists()
    return {"path": path, "status": "PASS" if exists else "MISSING"}


def markdown(payload: dict) -> str:
    lines = [
        "# Dealix Client Delivery Control",
        "",
        f"Verdict: `{payload['verdict']}`",
        "",
        "## Delivery method",
        "",
        payload["delivery_method"],
        "",
        "## Stages",
        "",
    ]
    for stage in payload["stages"]:
        lines.append(f"- {stage['name']}: {stage['goal']}")
    lines += ["", "## Required files", ""]
    for item in payload["client_files_status"]:
        lines.append(f"- {item['status']}: `{item['path']}`")
    lines += ["", "## Next actions", ""]
    for item in payload["next_delivery_actions"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    manifest = load_json(MANIFEST, {})
    file_status = [check_path(path) for path in manifest.get("client_files_required", [])]
    has_missing = any(item["status"] != "PASS" for item in file_status)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "company": manifest.get("company", "Dealix"),
        "control_name": manifest.get("control_name", "Client Delivery Control"),
        "delivery_method": manifest.get("delivery_method", "Map, Design, Build, Operate, Scale"),
        "purpose": manifest.get("purpose", "controlled client delivery"),
        "verdict": "CLIENT_DELIVERY_CONTROL_READY" if not has_missing else "CLIENT_DELIVERY_TEMPLATE_REVIEW_NEEDED",
        "stages": manifest.get("stages", []),
        "client_files_status": file_status,
        "delivery_guardrails": manifest.get("delivery_guardrails", []),
        "next_delivery_actions": [
            "Create a workspace from clients/_template for every new client.",
            "Confirm outcome, owner, workflow, and acceptance criteria before build.",
            "Start with one high-value workflow before expanding scope.",
            "Generate proof notes before renewal or expansion.",
            "Keep client delivery visible in the command center."
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown(payload), encoding="utf-8")
    WEB.parent.mkdir(parents=True, exist_ok=True)
    WEB.write_text(
        "export const clientDeliveryControlSnapshot = " + json.dumps(payload, ensure_ascii=False, indent=2) + " as const;\n",
        encoding="utf-8",
    )
    print(f"CLIENT_DELIVERY_CONTROL={payload['verdict']}")
    print("CLIENT_DELIVERY_CONTROL_REPORT=reports/client_delivery_control/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
