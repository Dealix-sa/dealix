import subprocess
import sys
from pathlib import Path


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: list) -> None:
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def productization(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        "scripts/generate_productization_review.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: productization command completed.")
    print(f"Review: {private_ops_path / 'productization/productization_review.md'}")
