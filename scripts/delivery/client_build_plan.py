#!/usr/bin/env python3
"""Client build plan — generate a sprint plan skeleton from the blueprint.

Usage:
    python scripts/delivery/client_build_plan.py --client-slug acme --sprints 3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"


def build_plan(slug: str, sprints: int = 3) -> Path:
    """Write a sprint plan skeleton into 03_delivery/sprint_plan.md."""
    ws = CLIENTS_DIR / slug
    if not ws.exists():
        raise FileNotFoundError(f"client workspace not found: {ws}")

    delivery_dir = ws / "03_delivery"
    delivery_dir.mkdir(parents=True, exist_ok=True)
    plan = delivery_dir / "sprint_plan.md"

    lines = [
        "# Sprint Plan",
        "",
        "Doctrine: Map -> Design -> Build -> Operate -> Scale.",
        "",
        "## Engagement overview",
        "",
        f"- **Total sprints planned:** {sprints}",
        "- **Sprint length:** 2 weeks",
        "- **Sprint cadence:** kickoff Monday, demo Friday",
        "",
    ]

    for i in range(sprints + 1):
        title = "Setup & diagnosis closure" if i == 0 else f"Sprint {i} — [goal]"
        lines.append(f"### Sprint {i} — {title}")
        lines.append("- [ ] ")
        lines.append("- **Demo:** ")
        lines.append("- **Acceptance check:** ")
        lines.append("")

    lines.extend(
        [
            "## Sprint exit gate",
            "",
            "- [ ] Demo delivered to sponsor",
            "- [ ] Acceptance criteria progress documented",
            "- [ ] Risks updated",
            "- [ ] Next sprint backlog confirmed",
            "",
        ]
    )

    plan.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a client sprint plan skeleton.")
    parser.add_argument("--client-slug", required=True)
    parser.add_argument("--sprints", type=int, default=3)
    args = parser.parse_args()

    try:
        path = build_plan(args.client_slug, args.sprints)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"sprint plan written: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())