#!/usr/bin/env python3
"""Scan Dealix Ultimate Operating Layer files for unsafe phrasing.

This verifier enforces banned guarantee phrases, real-looking emails, and
literal API key / secret patterns inside files that are owned by the
Ultimate Operating Layer (Founder Console, internal API, policy /
registry / eval YAML, and ULO docs). It does **not** police pre-existing
legacy docs under `docs/` — those are owned by other working streams.

The verifier itself, the policy YAML, the eval gate YAML, and the
trust/policy/eval reference docs are allowlisted because their explicit
purpose is to enumerate the banned phrases.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Allowlist: these files legitimately list banned phrases / control text.
ALLOWLIST = {
    REPO / "policies" / "dealix_control_policy.yaml",
    REPO / "evals" / "gates" / "dealix_agent_eval_gate.yaml",
    REPO / "docs" / "trust" / "POLICY_AS_CODE_V1.md",
    REPO / "docs" / "ai" / "EVAL_RED_TEAM_SYSTEM.md",
    REPO / "docs" / "evals" / "EVAL_GATE_V1.md",
    Path(__file__).resolve(),
}

# Files explicitly created by the Ultimate Operating Layer. Any file
# created or owned by ULO must pass this verifier.
ULO_FILES: list[Path] = [
    REPO / "CLAUDE.md",
    REPO / "policies" / "dealix_control_policy.yaml",
    REPO / "registries" / "agent_registry.yaml",
    REPO / "evals" / "gates" / "dealix_agent_eval_gate.yaml",
    REPO / "docs" / "trust" / "POLICY_AS_CODE_V1.md",
    REPO / "docs" / "trust" / "ULTIMATE_TRUST_PLANE.md",
    REPO / "docs" / "trust" / "FOUNDER_CONSOLE_TRUST_GATE.md",
    REPO / "docs" / "ai" / "AGENT_REGISTRY_SYSTEM.md",
    REPO / "docs" / "ai" / "CEO_COPILOT_SYSTEM.md",
    REPO / "docs" / "ai" / "REVENUE_AGENT_SWARM.md",
    REPO / "docs" / "ai" / "TRUST_GUARDIAN_AGENT.md",
    REPO / "docs" / "ai" / "EVAL_RED_TEAM_SYSTEM.md",
    REPO / "docs" / "architecture" / "AI_NATIVE_COMPANY_ARCHITECTURE.md",
    REPO / "docs" / "architecture" / "ULTIMATE_ARCHITECTURE_MAP.md",
    REPO / "docs" / "evals" / "EVAL_GATE_V1.md",
    REPO / "docs" / "founder" / "OPERATING_SCORECARD_V1.md",
    REPO / "docs" / "control_plane" / "DEALIX_CONTROL_PLANE.md",
    REPO / "docs" / "api" / "CONTROL_PLANE_API.md",
    REPO / "docs" / "api" / "ULTIMATE_INTERNAL_API.md",
    REPO / "docs" / "data" / "POSTGRES_PRIMARY_MODE.md",
    REPO / "docs" / "data" / "ULTIMATE_DATA_PLATFORM.md",
    REPO / "docs" / "runtime" / "PRIVATE_OPS_RUNTIME_CONTRACT.md",
    REPO / "docs" / "runtime" / "WORKER_ORCHESTRATOR_V1.md",
    REPO / "docs" / "runtime" / "ULTIMATE_WORKER_MESH.md",
    REPO / "docs" / "company" / "DEALIX_AUTONOMOUS_ENTERPRISE_OS.md",
    REPO / "docs" / "company" / "DEALIX_MATURITY_MODEL.md",
    REPO / "docs" / "frontend" / "ULTIMATE_FOUNDER_CONSOLE.md",
    REPO / "docs" / "revenue" / "ULTIMATE_REVENUE_FACTORY.md",
    REPO / "docs" / "delivery" / "ULTIMATE_DELIVERY_OS.md",
    REPO / "docs" / "finance" / "ULTIMATE_FINANCE_OS.md",
    REPO / "docs" / "product" / "ULTIMATE_PRODUCT_PLATFORM.md",
    REPO / "docs" / "engineering" / "ULTIMATE_OBSERVABILITY_DORA.md",
    REPO / "docs" / "security" / "ULTIMATE_SECURITY_GOVERNANCE.md",
    REPO / "docs" / "security" / "PRODUCTION_SECURITY_GATE.md",
    REPO / "docs" / "security" / "INTERNAL_API_AUTH_GATE.md",
    REPO / "docs" / "security" / "BRANCH_PROTECTION_REQUIRED_CHECKS.md",
]

# Also scan everything under apps/web/app, components/founder, and lib so
# new UI doesn't slip in banned text.
ULO_DIRS = [
    REPO / "apps" / "web" / "app",
    REPO / "apps" / "web" / "components" / "founder",
    REPO / "apps" / "web" / "lib",
]
SCAN_EXTENSIONS = {".md", ".yaml", ".yml", ".tsx", ".ts"}
EXCLUDE_PARTS = {"node_modules", ".next", ".git", "dist", "build"}

BANNED_PHRASES = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed meetings",
    "guaranteed replies",
    "guaranteed conversions",
    "fully compliant",
    "no-risk",
    "zero risk",
    "sent automatically without approval",
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?!example\.com)([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|secret_key|password|access[_-]?token|bearer)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{20,}[\"']?"
)
PLACEHOLDER_DOMAINS = {"example.com", "dealix.local", "placeholder.com"}


def iter_files() -> list[Path]:
    out: list[Path] = []
    for path in ULO_FILES:
        if path.exists():
            out.append(path)
    for entry in ULO_DIRS:
        if not entry.exists():
            continue
        for path in entry.rglob("*"):
            if not path.is_file():
                continue
            if any(part in EXCLUDE_PARTS for part in path.parts):
                continue
            if path.suffix.lower() in SCAN_EXTENSIONS:
                out.append(path)
    return out


def main() -> int:
    failures: list[str] = []
    files = iter_files()

    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        lowered = content.lower()
        if path not in ALLOWLIST:
            for phrase in BANNED_PHRASES:
                if phrase in lowered:
                    failures.append(f"{path.relative_to(REPO)}: banned phrase {phrase!r}")
                    break

        if path.suffix.lower() == ".md":
            for match in EMAIL_RE.finditer(content):
                domain = match.group(1).lower()
                if domain in PLACEHOLDER_DOMAINS or "example" in domain:
                    continue
                failures.append(
                    f"{path.relative_to(REPO)}: non-placeholder email '{match.group(0)}'"
                )
                break

        for match in SECRET_RE.finditer(content):
            failures.append(
                f"{path.relative_to(REPO)}: possible secret literal: {match.group(0)[:40]}…"
            )

    print(f"scanned {len(files)} files (ULO scope)")
    if failures:
        print("FAIL: unsafe phrasing/leak findings:")
        for line in failures[:40]:
            print(f"  - {line}")
        if len(failures) > 40:
            print(f"  …and {len(failures) - 40} more")
        return 1

    print("OK: no banned phrases, non-placeholder emails, or secret literals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
