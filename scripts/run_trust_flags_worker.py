#!/usr/bin/env python3
"""Roll up open trust flags and refresh worker state."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from api.internal import runtime_reader  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args(argv)
    root = Path(args.private_ops).expanduser().resolve()
    os.environ["DEALIX_PRIVATE_OPS"] = str(root)

    flags = runtime_reader.trust_flags()
    notes = (
        f"flags={flags['count']} suppression={flags['suppression_count']} "
        f"a3_attempts={flags['a3_attempts']}"
    )
    status = "ok" if flags["count"] == 0 else "warning"

    subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "update_worker_state.py"),
            "--worker", "trust_flags",
            "--status", status,
            "--notes", notes,
            "--private-ops", str(root),
        ],
        check=False,
    )
    print(notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
