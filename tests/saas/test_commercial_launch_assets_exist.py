from pathlib import Path


def test_commercial_launch_assets_exist():
    required = [
        "reports/go_live/FOUNDER_LAUNCH_COMMAND_CENTER.md",
        "reports/go_live/GO_LIVE_72_HOUR_PLAN.md",
        "sales/PROPOSAL_TEMPLATE_SAAS_BETA_AR.md",
        "sales/DIAGNOSTIC_QUESTIONS_AR.md",
        "sales/OBJECTION_BANK_AR.md",
        "docs/ops/COMMERCIAL_OPERATING_SYSTEM.md",
        "docs/ops/CLIENT_ONBOARDING_RUNBOOK.md",
        "docs/ops/COMMERCIAL_KPI_TREE.md",
        "scripts/commercial_bootstrap.py",
    ]
    for path in required:
        assert Path(path).exists(), path
