#!/usr/bin/env python3
"""Verify Hermes Agent OS files and safety gates."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "dealix/hermes/__init__.py",
    "dealix/hermes/agents.yaml",
    "dealix/hermes/policies.yaml",
    "dealix/hermes/tools.yaml",
    "requirements-hermes.txt",
    "scripts/hermes_generate_reports.py",
    "scripts/install_hermes_systemd.sh",
    "ops/systemd/dealix-hermes.service",
    "ops/systemd/dealix-hermes.timer",
    "docs/hermes/HERMES_AGENT_OS_AR.md",
    "docs/hermes/runtime/.gitkeep",
]
FORBIDDEN = [
    "send_without_approval",
    "external_side_effects: enabled",
    "allowed_without_approval: true\n    examples:\n      - production deploy",
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
]


def fail(message: str) -> None:
    raise SystemExit(f"HERMES_VERIFY_FAIL: {message}")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    combined = []
    for path in REQUIRED:
        combined.append(read(path))
    text = "\n".join(combined)
    for marker in FORBIDDEN:
        if marker in text:
            fail(f"forbidden marker found: {marker}")
    agents = read("dealix/hermes/agents.yaml")
    for required_agent in [
        "founder-chief-of-staff",
        "revenue-pipeline-agent",
        "reliability-sre-agent",
        "security-compliance-agent",
        "ai-governance-agent",
        "hermes-orchestrator",
    ]:
        if required_agent not in agents:
            fail(f"missing required agent {required_agent}")
    policies = read("dealix/hermes/policies.yaml")
    if "external_side_effects: disabled" not in policies:
        fail("Hermes must default external side effects to disabled")
    print("HERMES_AGENT_OS_OK")


if __name__ == "__main__":
    main()
