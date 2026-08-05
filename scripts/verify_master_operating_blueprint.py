from pathlib import Path
import subprocess
import sys

required_files = [
    "DEALIX_MASTER_OPERATING_BLUEPRINT.md",
    "DEALIX_INTEGRATION_MAP.md",
    "DEALIX_FINAL_REPO_TREE.md",
    "docs/ops/MASTER_COMMAND_SYSTEM.md",
    "docs/ops/GITHUB_GOVERNANCE_SYSTEM.md",
]

required_verifiers = [
    "scripts/verify_company_data_architecture.py",
    "scripts/verify_execution_assurance_system.py",
    "scripts/verify_revenue_operations_playbook.py",
    "scripts/verify_delivery_client_success_os.py",
    "scripts/verify_finance_pricing_os.py",
    "scripts/verify_trust_ai_risk_os.py",
    "scripts/verify_brand_proof_content_os.py",
    "scripts/verify_people_partner_os.py",
    "scripts/verify_productization_engineering_os.py",
    "scripts/verify_board_level_os.py",
]

failures = []

for file in required_files:
    p = Path(file)
    if not p.exists():
        failures.append(f"Missing: {file}")
    elif p.stat().st_size < 200:
        failures.append(f"Too short: {file}")

for script in required_verifiers:
    p = Path(script)
    if not p.exists():
        failures.append(f"Missing verifier: {script}")

if failures:
    print("Master operating blueprint verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

for script in required_verifiers:
    print(f"Running {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        failures.append(f"Verifier failed: {script}")

compile_result = subprocess.run([
    sys.executable,
    "-m",
    "compileall",
    "scripts",
    "ops_runtime",
    "dealix_cli",
    "control_plane",
    "execution_engine",
])
if compile_result.returncode != 0:
    failures.append("Compile failed")

if failures:
    print("Master operating blueprint verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: Master operating blueprint is ready.")
