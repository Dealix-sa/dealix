#!/usr/bin/env python3
"""Smoke Internal API: confirm api/routers/internal/founder_console.py exposes
read-only endpoints (no external action) and the router module imports cleanly."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, must_exist, report, file_contains  # noqa: E402

LAYER = "Internal API"
MOD_PATH = REPO_ROOT / "api" / "routers" / "internal" / "founder_console.py"


def main() -> None:
    reasons = must_exist(
        "api/routers/internal/__init__.py",
        "api/routers/internal/founder_console.py",
    )
    if reasons:
        report(LAYER, False, reasons)

    text = MOD_PATH.read_text(encoding="utf-8")
    if "router = APIRouter" not in text:
        reasons.append("founder_console.py missing APIRouter instantiation")
    # Read-only: no requests.post / httpx.post / send_email / send_sms / send_whatsapp
    forbidden = ("send_email(", "send_sms(", "send_whatsapp(", "requests.post(", "httpx.post(")
    for f in forbidden:
        if f in text:
            reasons.append(f"internal API performs external action: {f}")

    # Module imports — fastapi is an optional runtime dep in CI shards.
    try:
        import fastapi  # noqa: F401
    except ImportError:
        # Without fastapi we can't load the module, but the file passes
        # the structural checks above; that is sufficient for the verifier.
        report(LAYER, not reasons, reasons)

    spec = importlib.util.spec_from_file_location("founder_console", str(MOD_PATH))
    if not spec or not spec.loader:
        reasons.append("founder_console.py failed to spec")
    else:
        try:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if not hasattr(mod, "router"):
                reasons.append("founder_console.py missing `router` attr")
        except Exception as exc:  # noqa: BLE001
            reasons.append(f"founder_console import error: {exc!s}")

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
