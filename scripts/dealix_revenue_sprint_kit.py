"""Revenue Sprint Kit CLI command.

Usage:
    python scripts/dealix_revenue_sprint_kit.py
    python scripts/dealix_revenue_sprint_kit.py --private-ops ./private_ops

The command prints the list of operating files in the private kit and then
invokes the private verifier. It performs no external actions.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

KIT_FILES = [
    "offers/revenue_sprint/founder_dm_pack.md",
    "offers/revenue_sprint/sample_pack_template.md",
    "offers/revenue_sprint/proposal_fast_template.md",
    "offers/revenue_sprint/payment_followup_templates.md",
    "offers/revenue_sprint/client_intake.md",
    "offers/revenue_sprint/delivery_report_template.md",
    "offers/revenue_sprint/qa_checklist.md",
    "offers/revenue_sprint/handoff_template.md",
    "offers/revenue_sprint/feedback_request.md",
    "offers/revenue_sprint/retainer_ask.md",
]


def ensure_private_ops(path_str: str) -> Path:
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"private ops directory not found: {path}")
    if not path.is_dir():
        raise SystemExit(f"private ops path is not a directory: {path}")
    return path


def kit(private_ops: str) -> int:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Revenue Sprint Kit")
    print("=" * 40)
    print("Use these files:")
    missing: list[str] = []
    for relative in KIT_FILES:
        file_path = private_ops_path / relative
        marker = "  " if file_path.exists() else "! "
        print(f"{marker}- {file_path}")
        if not file_path.exists():
            missing.append(relative)

    verifier = private_ops_path / "verify_revenue_sprint_kit.py"
    if verifier.exists():
        print(f"\nRunning private verifier: {verifier}")
        result = subprocess.run(
            [sys.executable, str(verifier)],
            check=False,
        )
        if result.returncode != 0:
            print("FAIL: private verifier reported errors.")
            return result.returncode
    else:
        print(f"\nNote: private verifier not found at {verifier}")

    if missing:
        print("\nFAIL: some kit files are missing:")
        for relative in missing:
            print("-", relative)
        return 1

    print("\nPASS: kit command completed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Revenue Sprint Kit command.")
    parser.add_argument(
        "--private-ops",
        default=str(REPO_ROOT / "private_ops"),
        help="Path to the private operations directory (default: ./private_ops).",
    )
    args = parser.parse_args()
    return kit(args.private_ops)


if __name__ == "__main__":
    raise SystemExit(main())
