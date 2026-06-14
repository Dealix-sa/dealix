"""Verify the Executive Control Plane files exist and are non-trivial."""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/control_plane/EXECUTIVE_CONTROL_PLANE.md",
    "control_plane/priority_router.py",
    "scripts/generate_ceo_action_queue.py",
    "docs/ops/OPERATING_CONTRACTS.md",
    "DEALIX_SYSTEM_MAP.md",
]


def main() -> None:
    failures: list[str] = []
    for file in REQUIRED:
        p = REPO_ROOT / file
        if not p.exists():
            failures.append(f"Missing: {file}")
        elif p.stat().st_size < 150:
            failures.append(f"Too short: {file}")
    if failures:
        print("Executive control plane verification failed:")
        for f in failures:
            print("-", f)
        raise SystemExit(1)
    print("PASS: Executive control plane is ready.")


if __name__ == "__main__":
    main()
