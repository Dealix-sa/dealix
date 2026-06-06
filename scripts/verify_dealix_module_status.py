#!/usr/bin/env python3
"""Verify the Module Status Map is present and honest.

Dependency-free (stdlib only). Part of the Dealix launch gates.

PASS criteria:
  1. docs/00_platform_truth/MODULE_STATUS_MAP.md exists.
  2. Every module row uses a status from the controlled vocabulary.
  3. No module marked PLANNED / ROADMAP is simultaneously claimed LIVE.
  4. The map declares at least one PRODUCTION_READY module and is honest
     about DEMO_FALLBACK / PLANNED ones (no future module shown as LIVE).

The map is a simple Markdown table. Status is read from the column whose
header contains "status".

Exit 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs/00_platform_truth/MODULE_STATUS_MAP.md"

ALLOWED = {
    "LIVE",
    "PRODUCTION_READY",
    "DEMO_FALLBACK",
    "BETA",
    "PLANNED",
    "ROADMAP",
    "DEPRECATED",
}
# Statuses that mean "not shippable as a live customer promise".
NON_LIVE = {"PLANNED", "ROADMAP", "DEMO_FALLBACK", "DEPRECATED"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"PASS: {msg}")


def parse_table(text: str):
    """Parse every Markdown table; collect data rows + the status column index.

    Handles multiple tables: any row whose cells match a header (contains a
    'status' cell) re-establishes the column layout and is not treated as data.
    """
    rows = []
    status_idx = None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # separator row like |---|---|
        if all(set(c) <= set("-: ") for c in cells if c):
            continue
        lowered = [c.lower() for c in cells]
        if any(c == "status" for c in lowered):
            # (re)header row — record where the status column is, skip as data
            status_idx = lowered.index("status")
            continue
        rows.append(cells)
    return None, status_idx, rows


def main() -> int:
    print("== Dealix Module Status Verifier ==")
    failures = 0

    if not MAP.is_file():
        fail(f"Module Status Map missing ({MAP.relative_to(ROOT)})")
        print("\nRESULT: FAIL (1 issue)")
        return 1
    ok(f"Module Status Map present ({MAP.relative_to(ROOT)})")

    text = MAP.read_text(encoding="utf-8", errors="ignore")
    header, status_idx, rows = parse_table(text)

    if status_idx is None:
        fail("no 'status' column found in any table")
        print("\nRESULT: FAIL (1 issue)")
        return 1

    statuses = []
    for cells in rows:
        if status_idx >= len(cells):
            continue
        raw = cells[status_idx].upper().replace("`", "").strip()
        if not raw or raw == "STATUS":
            continue
        # Normalize tokens like "PRODUCTION READY" -> "PRODUCTION_READY"
        token = raw.split()[0] if raw else ""
        token = token.replace("PRODUCTION_READY", "PRODUCTION_READY")
        if "PRODUCTION" in raw and "READY" in raw:
            token = "PRODUCTION_READY"
        elif "DEMO" in raw:
            token = "DEMO_FALLBACK"
        name = cells[0] if cells else "(unnamed)"
        if token not in ALLOWED:
            fail(f"module '{name}' has invalid status '{raw}' (allowed: {sorted(ALLOWED)})")
            failures += 1
            continue
        statuses.append((name, token))

    if not statuses:
        fail("no module rows parsed from the status table")
        failures += 1
    else:
        ok(f"parsed {len(statuses)} module rows, all using controlled vocabulary")

    # Honesty check: a row whose description calls the module future/planned/
    # roadmap must NOT carry a LIVE / PRODUCTION_READY status.
    FUTURE_WORDS = ("future", "planned", "roadmap", "coming soon", "مستقبل", "قادم")
    for cells in rows:
        if status_idx >= len(cells):
            continue
        raw = cells[status_idx].upper().replace("`", "")
        if "PRODUCTION" in raw and "READY" in raw:
            token = "PRODUCTION_READY"
        else:
            token = (raw.split() or [""])[0]
        if token in {"LIVE", "PRODUCTION_READY"}:
            desc = " ".join(c.lower() for i, c in enumerate(cells) if i != status_idx)
            if any(w in desc for w in FUTURE_WORDS):
                fail(f"row '{cells[0]}' is {token} but described as future/planned: {desc[:70]}")
                failures += 1

    live_like = [n for n, t in statuses if t in {"LIVE", "PRODUCTION_READY"}]
    if live_like:
        ok(f"{len(live_like)} module(s) PRODUCTION_READY/LIVE: {', '.join(live_like[:6])}")
    else:
        fail("no PRODUCTION_READY or LIVE module declared")
        failures += 1

    demo = [n for n, t in statuses if t == "DEMO_FALLBACK"]
    if demo:
        ok(f"honest DEMO_FALLBACK disclosure for: {', '.join(demo)}")

    print()
    if failures:
        print(f"RESULT: FAIL ({failures} issue(s))")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
