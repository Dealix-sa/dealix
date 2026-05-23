from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str]) -> None:
    print(f"\n== Running: {' '.join(command)} ==")
    result = subprocess.run(command)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def ensure_private_ops(path: str) -> Path:
    private_ops = Path(path).resolve()
    if not private_ops.exists():
        raise SystemExit(f"Private ops path does not exist: {private_ops}")

    required = [
        "pipeline/pipeline_tracker.csv",
        "revenue/mrr_tracker.csv",
        "trust/approval_log.csv",
        "founder",
        "learning",
    ]

    missing = [item for item in required if not (private_ops / item).exists()]
    if missing:
        print("Private ops is missing required files/folders:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)

    return private_ops


def daily(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    run_command([
        sys.executable,
        "scripts/generate_ops_from_private.py",
        "--private-ops",
        str(private_ops_path),
    ])

    run_command([
        sys.executable,
        "scripts/export_dashboard_data.py",
        "--private-ops",
        str(private_ops_path),
    ])

    print("\nPASS: Daily command completed.")
    print(f"Updated: {private_ops_path / 'founder/daily_brief.md'}")
    print(f"Updated: {private_ops_path / 'founder/decision_queue.md'}")
    print(f"Updated: {private_ops_path / 'learning/weekly_intelligence_review.md'}")
    print("Generated local dashboard data: dashboard_data/company_metrics.json")


def weekly(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    run_command([
        sys.executable,
        "scripts/generate_ops_from_private.py",
        "--private-ops",
        str(private_ops_path),
    ])

    run_command([
        sys.executable,
        "scripts/export_dashboard_data.py",
        "--private-ops",
        str(private_ops_path),
    ])

    if (private_ops_path / "verify_private_ops_deep.py").exists():
        run_command([
            sys.executable,
            str(private_ops_path / "verify_private_ops_deep.py"),
        ])

    print("\nPASS: Weekly command completed.")
    print("Next required CEO action:")
    print("- Open founder/weekly_ceo_review.md")
    print("- Write one learning decision")
    print("- Update one playbook, checklist, message, pricing rule, or trust rule")


def dashboard(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    run_command([
        sys.executable,
        "scripts/export_dashboard_data.py",
        "--private-ops",
        str(private_ops_path),
    ])

    print("\nPASS: Dashboard data generated.")
    print("Open locally:")
    print("python -m http.server 8080")
    print("http://localhost:8080/internal_dashboard/ceo_dashboard_v2.html")


def verify(private_ops: str | None = None) -> None:
    checks = [
        ["python", "scripts/verify_master_tree.py"],
        ["python", "scripts/verify_document_quality.py"],
        ["python", "scripts/verify_company_os_deep.py"],
        ["python", "scripts/verify_dashboard_v2.py"],
        ["python", "scripts/verify_ops_runtime.py"],
    ]

    optional_checks = [
        ["python", "scripts/verify_public_safety.py"],
        ["python", "scripts/verify_private_boundary.py"],
        ["python", "scripts/verify_weekly_playbook_rule.py"],
    ]

    for command in checks:
        if Path(command[1]).exists():
            run_command([sys.executable, command[1]])

    for command in optional_checks:
        if Path(command[1]).exists():
            run_command([sys.executable, command[1]])

    if private_ops:
        private_ops_path = ensure_private_ops(private_ops)
        for script in [
            "verify_private_ops_integrity.py",
            "verify_private_ops_deep.py",
            "verify_decision_queue.py",
        ]:
            script_path = private_ops_path / script
            if script_path.exists():
                run_command([sys.executable, str(script_path)])

    run_command([
        sys.executable,
        "-m",
        "compileall",
        "control_plane",
        "operating_intelligence",
        "ops_runtime",
        "dealix",
        "scripts",
        "dealix_cli",
    ])

    print("\nPASS: Dealix CLI verify completed.")
