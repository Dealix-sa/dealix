#!/usr/bin/env python3
"""Dealix module-status verifier (Wave 7).

Hard rule: a module that is not yet live must never be presented to a
customer as if it were live. The source of truth is
data/launch/module_status.json. Each module declares a status:

  live     — shipped and operable today (founder can deliver it manually)
  planned  — on the roadmap, NOT to be sold as available
  internal — internal tooling, not customer-facing

Customer-visible landing pages may reference a `planned` module only if
they also carry a roadmap/soon marker near it. This verifier flags any
`planned` module name that appears on the public surface without such a
marker.

Exit 0 = PASS, 1 = FAIL. Pure stdlib.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"
REGISTRY = ROOT / "data" / "launch" / "module_status.json"

ROADMAP_MARKERS = [
    "roadmap",
    "coming soon",
    "soon",
    "planned",
    "قريبًا",
    "قريبا",
    "خارطة",
    "لاحقًا",
    "لاحقا",
]

FAILURES: list[str] = []
WARNINGS: list[str] = []


def load_registry() -> dict:
    if not REGISTRY.is_file():
        FAILURES.append(f"missing module status registry: {REGISTRY.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        FAILURES.append(f"module_status.json is not valid JSON: {exc}")
        return {}


def check_planned_not_sold_as_live(registry: dict) -> None:
    modules = registry.get("modules", [])
    planned = [m for m in modules if m.get("status") == "planned"]
    if not LANDING.is_dir():
        return
    pages = list(LANDING.glob("*.html"))
    for mod in planned:
        name = mod.get("name", "")
        labels = mod.get("public_labels", [name])
        for page in pages:
            html = page.read_text(encoding="utf-8")
            low = html.lower()
            for label in labels:
                if not label:
                    continue
                for m in re.finditer(re.escape(label.lower()), low):
                    window = low[max(0, m.start() - 120) : m.start() + 120]
                    if not any(marker in window for marker in ROADMAP_MARKERS):
                        FAILURES.append(
                            f"{page.name}: planned module {name!r} (label {label!r}) "
                            f"appears without a roadmap/soon marker — reads as live"
                        )
                        break


def check_live_modules_are_deliverable(registry: dict) -> None:
    """A live module should declare how it is delivered today."""
    for mod in registry.get("modules", []):
        if mod.get("status") == "live" and not mod.get("delivery"):
            WARNINGS.append(
                f"live module {mod.get('name')!r} has no 'delivery' field "
                "(how is it delivered today?)"
            )


def main() -> int:
    print("== Dealix module-status verifier ==")
    registry = load_registry()
    if registry:
        check_planned_not_sold_as_live(registry)
        check_live_modules_are_deliverable(registry)

    for w in WARNINGS:
        print(f"  WARN: {w}")
    for f in FAILURES:
        print(f"  FAIL: {f}")

    if FAILURES:
        print(f"\nRESULT: FAIL ({len(FAILURES)} blocker(s), {len(WARNINGS)} warning(s))")
        return 1
    print(f"\nRESULT: PASS ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
