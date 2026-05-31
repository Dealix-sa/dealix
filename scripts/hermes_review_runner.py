#!/usr/bin/env python3
"""Hermes review-only runner.

Generates founder-reviewable local artifacts from the Hermes manifest.
No network calls. No provider calls. No production calls.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "hermes" / "agents" / "manifest.json"
DEFAULT_OUT_DIR = ROOT / "data" / "hermes"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def build_review_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    created_at = utc_now()
    records: list[dict[str, Any]] = []
    for agent in manifest.get("agents", []):
        agent_id = agent.get("id", "unknown_agent")
        records.append(
            {
                "review_id": f"hermes-{created_at}-{agent_id}",
                "agent_id": agent_id,
                "run_id": f"dry-run-{created_at}",
                "created_at": created_at,
                "mode": manifest.get("default_mode", "dry_run"),
                "risk_level": "low",
                "input_scope": "manifest_bootstrap",
                "finding": f"{agent.get('role', agent_id)} is registered for review-only operation.",
                "confidence": "high",
                "recommended_next_step": "Review role outputs and connect to a real data source in a future PR.",
                "evidence": ["hermes/agents/manifest.json"],
                "owner": "founder",
                "status": "new",
            }
        )
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_digest(path: Path, manifest: dict[str, Any], records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Hermes Founder Digest",
        "",
        f"Generated: {utc_now()}",
        f"Mode: {manifest.get('default_mode', 'dry_run')}",
        f"Agents: {len(records)}",
        "",
        "## Registered agents",
        "",
    ]
    for record in records:
        lines.append(f"- **{record['agent_id']}** — {record['finding']}")
    lines.extend(
        [
            "",
            "## Recommended next steps",
            "",
            "1. Run `make hermes-verify` after every Hermes change.",
            "2. Review generated records before connecting external data sources.",
            "3. Add one data connector per PR, starting with read-only sources.",
            "4. Keep founder review before any customer-facing workflow.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Hermes review-only artifacts")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args()

    manifest = load_manifest()
    records = build_review_records(manifest)
    out_dir = Path(args.out_dir)
    write_jsonl(out_dir / "review_records.jsonl", records)
    write_digest(out_dir / "founder_digest.md", manifest, records)
    print(f"HERMES_REVIEW_RUNNER_OK records={len(records)} out_dir={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
