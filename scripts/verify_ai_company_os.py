"""Verify the Dealix AI Company OS surfaces exist (Founder Console, brand, API).

This script is intentionally tolerant of work-in-progress: it reports
WARN when a surface is missing so the user can see the punch list,
and only FAILs when something exists but is malformed.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    VerifierReport,
    main_cli,
    repo_path,
)

CONSOLE_PAGES = [
    "apps/web/app/page.tsx",
    "apps/web/app/control-plane/page.tsx",
    "apps/web/app/agents/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/safety/page.tsx",
]
TARGET_CONSOLE_PAGES = [
    # punch list — WARN if missing, not FAIL
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/ceo-os/page.tsx",
    "apps/web/app/founder-leverage/page.tsx",
    "apps/web/app/capital-allocation/page.tsx",
    "apps/web/app/strategy/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/deal-desk/page.tsx",
    "apps/web/app/market-attack/page.tsx",
    "apps/web/app/moat/page.tsx",
    "apps/web/app/revenue-intelligence/page.tsx",
    "apps/web/app/ai-governance/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/finance/page.tsx",
    "apps/web/app/customer-success/page.tsx",
    "apps/web/app/company-memory/page.tsx",
    "apps/web/app/legal/page.tsx",
    "apps/web/app/audit/page.tsx",
    "apps/web/app/metrics/page.tsx",
]
INTERNAL_API_FILES = [
    "api/internal/__init__.py",
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/internal/audit_writer.py",
    "api/internal/integration_gate.py",
]


def run() -> VerifierReport:
    r = VerifierReport(verifier="AI Company OS")

    # console — required pages
    for rel in CONSOLE_PAGES:
        if repo_path(rel).exists():
            r.pass_(rel, "present")
        else:
            r.fail(rel, "missing", hint="bootstrap with the next.js scaffold")

    # console — punch list (WARN)
    for rel in TARGET_CONSOLE_PAGES:
        if repo_path(rel).exists():
            r.pass_(rel, "present")
        else:
            r.warn(rel, "not yet implemented (punch list)")

    # internal api scaffold
    for rel in INTERNAL_API_FILES:
        if repo_path(rel).exists():
            r.pass_(rel, "present")
        else:
            r.warn(rel, "internal API scaffold missing — see master prompt §5")

    # policy / registries / gate must exist (hard fail)
    for rel in (
        "policies/dealix_control_policy.yaml",
        "registries/agent_registry.yaml",
        "registries/machine_registry.yaml",
        "registries/integration_registry.yaml",
        "evals/gates/dealix_agent_eval_gate.yaml",
    ):
        if repo_path(rel).exists():
            r.pass_(rel, "present")
        else:
            r.fail(rel, "missing", hint="see master prompt §4 / §5")

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_ai_company_os"))
