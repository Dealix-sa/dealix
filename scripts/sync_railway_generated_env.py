#!/usr/bin/env python3
"""Sync generated Railway env files (no secret values printed)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_ENV = ROOT / ".env.railway.generated"
FE_ENV = ROOT / ".env.railway.frontend.generated"


def _key_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def _write(
    path: Path,
    data: dict[str, str],
    *,
    remove_keys: frozenset[str] = frozenset(),
) -> None:
    lines: list[str] = []
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                lines.append(raw.rstrip())
                continue
            key = line.partition("=")[0].strip()
            if key in remove_keys:
                continue
            if key in data:
                lines.append(f"{key}={data[key]}")
                del data[key]
            else:
                lines.append(raw.rstrip())
    else:
        lines = [f"# {path.name}"]
    for key, val in data.items():
        lines.append(f"{key}={val}")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    api = _parse(API_ENV)
    fe = _parse(FE_ENV)
    if not api and not fe:
        print("RAILWAY_ENV_SYNC=SKIP (no .env.railway.*.generated)")
        return 0

    admin_values = set(_key_list(api.get("ADMIN_API_KEYS", "")))
    admin_values.update(
        value
        for value in (
            fe.get("DEALIX_ADMIN_API_KEY"),
            api.get("DEALIX_ADMIN_API_KEY"),
        )
        if value
    )
    service_values = set(_key_list(api.get("API_KEYS", "")))
    if api.get("DEALIX_API_KEY"):
        service_values.add(api["DEALIX_API_KEY"])
    admin = (
        fe.get("DEALIX_ADMIN_API_KEY")
        or api.get("DEALIX_ADMIN_API_KEY")
        or next(iter(_key_list(api.get("ADMIN_API_KEYS", ""))), "")
    )
    service = (
        next(iter(_key_list(api.get("API_KEYS", ""))), "")
        or api.get("DEALIX_API_KEY")
    )
    changes: list[str] = []
    api_remove_keys: set[str] = set()
    public_admin_key = "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"
    if public_admin_key in fe:
        del fe[public_admin_key]
        changes.append(f"FE:REMOVE_{public_admin_key}")
    invalid_service = bool(service_values & admin_values)
    if invalid_service:
        for key in ("API_KEYS", "DEALIX_API_KEY"):
            if key in api:
                del api[key]
                api_remove_keys.add(key)
                changes.append(f"API:REMOVE_{key}")
        service = ""
    if admin:
        if not fe.get("DEALIX_ADMIN_API_KEY"):
            fe["DEALIX_ADMIN_API_KEY"] = admin
            changes.append("FE:DEALIX_ADMIN_API_KEY")
        if not api.get("DEALIX_ADMIN_API_KEY"):
            api["DEALIX_ADMIN_API_KEY"] = admin
            changes.append("API:DEALIX_ADMIN_API_KEY")
    if service:
        if not api.get("API_KEYS"):
            api["API_KEYS"] = service
            changes.append("API:API_KEYS")
        if api.get("DEALIX_API_KEY") != service:
            api["DEALIX_API_KEY"] = service
            changes.append("API:DEALIX_API_KEY")
        if fe.get("DEALIX_API_KEY") != service:
            fe["DEALIX_API_KEY"] = service
            changes.append("FE:DEALIX_API_KEY")

    for key, val in (
        ("NEXT_PUBLIC_API_URL", "https://api.dealix.me"),
        ("NEXT_PUBLIC_SITE_URL", "https://dealix.me"),
        ("NEXT_PUBLIC_USE_DEALIX_OPS_PROXY", "1"),
    ):
        if not fe.get(key):
            fe[key] = val
            changes.append(f"FE:{key}")

    if not changes:
        print("RAILWAY_ENV_SYNC=OK (already aligned)")
        return 0

    print("RAILWAY_ENV_SYNC=UPDATED")
    for c in changes:
        print(f"  {c}")
    if args.dry_run:
        print("  (dry-run — no files written)")
        return 0

    if fe:
        _write(FE_ENV, fe, remove_keys=frozenset({public_admin_key}))
    if api:
        _write(API_ENV, api, remove_keys=frozenset(api_remove_keys))
    print(f"  wrote: {API_ENV.name}, {FE_ENV.name}")
    if invalid_service:
        print(
            "RAILWAY_ENV_SYNC=INCOMPLETE "
            "(service credential matched an admin credential)"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
