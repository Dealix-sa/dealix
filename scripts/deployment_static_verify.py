#!/usr/bin/env python3
"""Verify the Deployment Verification OS (V9) — static, non-destructive only.

This never triggers a deploy. It confirms the deployment checklists exist and
that documented deploy config files are present. No secrets are read or printed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/deployment-verification-os/00_DEPLOYMENT_VERIFICATION_OS.md",
    "docs/deployment-verification-os/01_MAIN_SERVER_CHECKLIST.md",
    "docs/deployment-verification-os/02_HEALTHCHECK_POLICY.md",
    "docs/deployment-verification-os/03_FRONTEND_DEPLOY_CHECK.md",
    "docs/deployment-verification-os/04_BACKEND_DEPLOY_CHECK.md",
    "docs/deployment-verification-os/05_ROLLBACK_CHECKLIST.md",
    "docs/deployment-verification-os/06_POST_DEPLOY_SMOKE_TEST.md",
    "docs/deployment-verification-os/99_DEPLOYMENT_VERIFICATION_REPORT.md",
]

# Documented deploy artifacts that should exist in this repo (informational).
DEPLOY_ARTIFACTS = [
    "Dockerfile", "docker-compose.yml", "railway.json", "Procfile",
]


def _artifact_presence() -> dict:
    return {a: (v9_lib.REPO / a).exists() for a in DEPLOY_ARTIFACTS}


def verify() -> dict:
    report = v9_lib.run_system_check("deployment_static", REQUIRED_FILES)
    report["deploy_artifacts_present"] = _artifact_presence()
    (v9_lib.OUTPUT_DIR / "deployment_static.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
