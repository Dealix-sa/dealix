#!/usr/bin/env python3
"""Dealix Free LLM Provider Registry freshness guard.

Offline, dependency-free check that the curated provider registry
(`data/ai/free_llm_provider_registry.json`, adopted from
cheahjs/free-llm-api-resources) has been reviewed recently. Free tiers,
rate limits, and model availability drift fast; the `improve` skill's cheap
executor selects from this registry, so a stale registry risks dispatching work
to a dead or changed free tier.

Prints status only — never a secret, never an external call. Exit code:
    0  registry fresh (or within grace)
    1  registry stale / malformed  (usable as a CI or pre-execute gate)

Override the max age with DEALIX_PROVIDER_REGISTRY_MAX_AGE_DAYS (default 45).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "data" / "ai" / "free_llm_provider_registry.json"
DEFAULT_MAX_AGE_DAYS = 45


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Registry not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def max_age_days() -> int:
    raw = os.environ.get("DEALIX_PROVIDER_REGISTRY_MAX_AGE_DAYS")
    if not raw:
        return DEFAULT_MAX_AGE_DAYS
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_MAX_AGE_DAYS
    return value if value > 0 else DEFAULT_MAX_AGE_DAYS


def evaluate(
    registry: dict[str, Any],
    *,
    today: _dt.date | None = None,
    max_age: int | None = None,
) -> dict[str, Any]:
    """Pure evaluation — returns a status dict. No I/O, testable."""
    today = today or _dt.date.today()
    max_age = max_age if max_age is not None else max_age_days()

    reviewed_raw = registry.get("last_reviewed")
    problems: list[str] = []

    reviewed: _dt.date | None = None
    if not reviewed_raw:
        problems.append("registry missing 'last_reviewed'")
    else:
        try:
            reviewed = _dt.date.fromisoformat(str(reviewed_raw))
        except ValueError:
            problems.append(f"'last_reviewed' not ISO date: {reviewed_raw!r}")

    if not registry.get("providers"):
        problems.append("registry has no providers")
    if not registry.get("upstream_readme_sha_observed"):
        problems.append("registry missing 'upstream_readme_sha_observed' drift anchor")

    age_days: int | None = None
    stale = False
    if reviewed is not None:
        age_days = (today - reviewed).days
        if age_days < 0:
            problems.append(f"'last_reviewed' is in the future: {reviewed_raw}")
        elif age_days > max_age:
            stale = True

    ok = not problems and not stale
    return {
        "ok": ok,
        "stale": stale,
        "age_days": age_days,
        "max_age_days": max_age,
        "last_reviewed": reviewed_raw,
        "providers": len(registry.get("providers", [])),
        "problems": problems,
    }


def render(status: dict[str, Any]) -> str:
    lines = ["# Dealix Provider Registry Freshness"]
    lines.append(f"- last_reviewed: {status['last_reviewed']}")
    lines.append(f"- age_days: {status['age_days']} (max {status['max_age_days']})")
    lines.append(f"- providers: {status['providers']}")
    if status["problems"]:
        lines.append("- problems:")
        lines.extend(f"    - {p}" for p in status["problems"])
    if status["stale"]:
        lines.append(
            "- STALE: re-review against "
            "https://github.com/cheahjs/free-llm-api-resources, then bump "
            "'last_reviewed' and 'upstream_readme_sha_observed'."
        )
    lines.append(f"\nRESULT: {'FRESH' if status['ok'] else 'ATTENTION'}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    status = evaluate(load_registry())
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(render(status))
    raise SystemExit(0 if status["ok"] else 1)


if __name__ == "__main__":
    main()
