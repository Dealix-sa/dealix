#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "dealix" / "hermes" / "agents.yaml",
    ROOT / "dealix" / "hermes" / "policy.yaml",
    ROOT / "scripts" / "hermes_report.py",
    ROOT / "docs" / "ops" / "HERMES_AGENT_OS.md",
]
REQUIRED_IDS = [
    "hermes_founder_chief_of_staff",
    "hermes_revenue_operator",
    "hermes_trust_guardian",
    "hermes_platform_sre",
    "hermes_security_auditor",
    "hermes_product_strategist",
    "hermes_ai_quality_evaluator",
]

errors = []
for path in FILES:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")

agents_path = FILES[0]
if agents_path.exists():
    text = agents_path.read_text(encoding="utf-8")
    for agent_id in REQUIRED_IDS:
        if agent_id not in text:
            errors.append(f"missing agent {agent_id}")

policy_path = FILES[1]
if policy_path.exists():
    text = policy_path.read_text(encoding="utf-8")
    for marker in ["default_mode", "approval_classes", "stop_rules"]:
        if marker not in text:
            errors.append(f"missing policy marker {marker}")

if errors:
    print("Hermes config check failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Hermes config OK")
