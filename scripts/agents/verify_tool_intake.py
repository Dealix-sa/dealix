#!/usr/bin/env python3
"""Dependency-free verifier for the Dealix monthly tool radar.

This validator performs deterministic schema, date, source, license, decision,
and safety checks. It does not access the network or install any tool.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ALLOWED_DECISIONS = {
    "adopt_now",
    "pilot",
    "pattern_only",
    "connector_only",
    "hold",
    "reject_core",
}
ALLOWED_PRIORITIES = {"P0", "P1", "P2", "P3"}
NON_OPEN_LICENSES = {
    "proprietary_api",
    "proprietary_service",
    "Elastic-2.0",
    "Sustainable Use License / fair-code",
    "AGPL-3.0 with enterprise modules",
    "unverified",
}
REQUIRED_ITEM_FIELDS = {
    "id",
    "name",
    "category",
    "july_signal",
    "release_date",
    "source",
    "license",
    "license_source",
    "decision",
    "priority",
    "dealix_surfaces",
    "integration",
    "gates",
}


def _parse_date(value: str, field: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be ISO-8601 YYYY-MM-DD: {value!r}") from exc


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    window = payload.get("research_window", {})
    try:
        start = _parse_date(window.get("start"), "research_window.start")
        end = _parse_date(window.get("end"), "research_window.end")
        if start > end:
            errors.append("research window start is after end")
    except ValueError as exc:
        errors.append(str(exc))
        start = end = date.min

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        return errors + ["items must be a non-empty list"]

    ids: Counter[str] = Counter()
    for index, item in enumerate(items):
        label = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_ITEM_FIELDS - item.keys())
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
            continue

        item_id = item["id"]
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
        else:
            ids[item_id] += 1

        if item["decision"] not in ALLOWED_DECISIONS:
            errors.append(f"{label}.decision is invalid: {item['decision']!r}")
        if item["priority"] not in ALLOWED_PRIORITIES:
            errors.append(f"{label}.priority is invalid: {item['priority']!r}")

        if item["release_date"] is None:
            if item.get("date_precision") != "github_created_filter_2026-07-01_to_2026-07-21":
                errors.append(f"{label} with no exact release_date needs the GitHub in-window date basis")
        else:
            try:
                released = _parse_date(item["release_date"], f"{label}.release_date")
                if not start <= released <= end:
                    errors.append(f"{label}.release_date is outside the research window")
            except ValueError as exc:
                errors.append(str(exc))

        source = item["source"]
        if not isinstance(source, str) or not source.startswith("https://"):
            errors.append(f"{label}.source must be an HTTPS primary-source URL")

        if not isinstance(item["dealix_surfaces"], list) or not item["dealix_surfaces"]:
            errors.append(f"{label}.dealix_surfaces must be a non-empty list")
        if not isinstance(item["gates"], list) or not item["gates"]:
            errors.append(f"{label}.gates must be a non-empty list")

        license_name = item["license"]
        license_source = item["license_source"]
        if license_name == "unverified":
            if item["decision"] != "hold":
                errors.append(f"{label} with unverified license must be held")
        elif not isinstance(license_source, str) or not license_source.startswith("https://"):
            errors.append(f"{label}.license_source must be HTTPS unless license is unverified")

        if license_name in NON_OPEN_LICENSES and item["decision"] == "adopt_now":
            errors.append(f"{label} non-open/mixed license cannot be adopt_now")

        risky_text = " ".join(str(x).lower() for x in [item["category"], item["integration"], *item["gates"]])
        if any(token in risky_text for token in ("external", "send", "browser", "production db", "payment")):
            if not any(
                guard in risky_text
                for guard in (
                    "approval",
                    "no external",
                    "no outreach",
                    "read-only",
                    "isolated",
                    "never",
                    "manual",
                    "token vault",
                    "data classification",
                    "reject wholesale",
                )
            ):
                errors.append(f"{label} mentions a sensitive surface without an explicit safety guard")

    duplicates = sorted(item_id for item_id, count in ids.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate ids: {', '.join(duplicates)}")
    return errors


def summary(payload: dict[str, Any]) -> dict[str, Any]:
    items = payload["items"]
    return {
        "items": len(items),
        "by_decision": dict(sorted(Counter(item["decision"] for item in items).items())),
        "by_priority": dict(sorted(Counter(item["priority"] for item in items).items())),
        "licenses": dict(sorted(Counter(item["license"] for item in items).items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "registry",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("dealix_july_2026_tool_radar.json"),
    )
    args = parser.parse_args()
    payload = json.loads(args.registry.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(json.dumps(summary(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
