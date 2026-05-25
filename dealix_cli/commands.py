import subprocess
import sys
from pathlib import Path


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"FAIL: private ops path does not exist: {path}")
    if not path.is_dir():
        raise SystemExit(f"FAIL: private ops path is not a directory: {path}")
    return path


def run_command(cmd):
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def finance(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        "scripts/generate_finance_review.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: finance command completed.")
    print(f"Review: {private_ops_path / 'finance/monthly_finance_review.md'}")
