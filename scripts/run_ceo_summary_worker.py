#!/usr/bin/env python3
"""Compose the CEO summary report and update worker_state.

Reads private ops, runs the operating scorecard generator, and writes
`worker_state` for the `ceo_summary` worker. Never sends anything.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args(argv)
    root = Path(args.private_ops).expanduser().resolve()
    env = {**os.environ, "DEALIX_PRIVATE_OPS": str(root)}

    status = "ok"
    notes = ""
    try:
        subprocess.run(
            [
                sys.executable,
                str(REPO / "scripts" / "generate_operating_scorecard.py"),
                "--private-ops",
                str(root),
            ],
            check=True,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        status = "failed"
        notes = f"scorecard exit={exc.returncode}"

    subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "update_worker_state.py"),
            "--worker",
            "ceo_summary",
            "--status",
            status,
            "--notes",
            notes,
            "--private-ops",
            str(root),
        ],
        check=False,
        env=env,
    )
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
