#!/usr/bin/env python3
"""Inventory every api/routers/*.py against api/main.py imports.

Outputs a markdown table to docs/reference/UNMOUNTED_ROUTERS.md:
  - file: router path
  - mounted: yes/no (imported in api/main.py)
  - last_modified: ISO date from git log
  - prefix: detected APIRouter prefix
  - tag: detected APIRouter tag
  - recommendation: keep | review | deprecate

Mounted routers are detected via two signals in api/main.py:
  1. `import api.routers.<name>` style imports
  2. `from api.routers import <name>` style imports

Domain aggregators (api/routers/domains/*) are followed transitively —
a router included via a domain aggregator counts as mounted.

Read-only diagnostic. No code changes.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROUTERS_DIR = REPO / "api" / "routers"
MAIN_PY = REPO / "api" / "main.py"
DOMAINS_DIR = REPO / "api" / "routers" / "domains"
OUT_FILE = REPO / "docs" / "reference" / "UNMOUNTED_ROUTERS.md"


def _read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _mounted_in_main() -> set[str]:
    """Names that appear imported/aliased in api/main.py."""
    text = _read_text(MAIN_PY)
    names: set[str] = set()
    # `from api.routers import foo` or `from api.routers import (a, b, c)`
    for m in re.finditer(
        r"from api\.routers import \(([^)]+)\)", text, re.DOTALL
    ):
        for piece in m.group(1).split(","):
            piece = piece.strip().split(" as ")[0].strip()
            if piece:
                names.add(piece)
    for m in re.finditer(
        r"from api\.routers import (\w+)(?:\s+as\s+\w+)?", text
    ):
        names.add(m.group(1))
    # `from api.routers import foo as bar`
    for m in re.finditer(
        r"from api\.routers\.(\w+) import", text
    ):
        names.add(m.group(1))
    # Defensive helper pattern:  _import_optional_router("name", "api.routers.name")
    for m in re.finditer(
        r'api\.routers\.(\w+)["\']',
        text,
    ):
        names.add(m.group(1))
    return names


def _mounted_via_domains() -> set[str]:
    """Names re-exported by api/routers/domains/* OR imported lazily by
    revenue_ops_autopilot (which appends to AUTOPILOT_ROUTERS at runtime)."""
    names: set[str] = set()
    paths: list[Path] = []
    if DOMAINS_DIR.is_dir():
        paths.extend(DOMAINS_DIR.glob("*/__init__.py"))
    # revenue_ops_autopilot.py builds AUTOPILOT_ROUTERS via lazy imports
    rop = ROUTERS_DIR / "revenue_ops_autopilot.py"
    if rop.is_file():
        paths.append(rop)
    for path in paths:
        text = _read_text(path)
        for m in re.finditer(r"from api\.routers\.(\w+) import", text):
            names.add(m.group(1))
        for m in re.finditer(
            r"from api\.routers import \(([^)]+)\)", text, re.DOTALL
        ):
            for piece in m.group(1).split(","):
                piece = piece.strip().split(" as ")[0].strip()
                if piece:
                    names.add(piece)
        for m in re.finditer(r"from api\.routers import (\w+)", text):
            names.add(m.group(1))
    return names


def _git_last_modified(path: Path) -> str:
    rel = path.relative_to(REPO)
    try:
        out = subprocess.check_output(  # noqa: S603,S607
            ["git", "log", "-1", "--format=%cs", "--", str(rel)],
            cwd=REPO,
            text=True,
        ).strip()
        return out or "unknown"
    except Exception:
        return "unknown"


def _detect_prefix_tag(path: Path) -> tuple[str, str]:
    text = _read_text(path)
    prefix = ""
    tag = ""
    pm = re.search(r'APIRouter\([^)]*prefix\s*=\s*"([^"]+)"', text, re.DOTALL)
    if pm:
        prefix = pm.group(1)
    tm = re.search(r'tags\s*=\s*\[\s*"([^"]+)"', text)
    if tm:
        tag = tm.group(1)
    return prefix, tag


def _recommendation(stem: str, mounted: bool, prefix: str) -> str:
    if mounted:
        return "keep"
    # Versioned legacy: v3, v10, v11, v12 prefixes
    if re.search(r"_v(3|10|11|12|13)\b", stem) or re.search(r"v(3|10|11|12)_", stem):
        return "deprecate"
    if stem in ("public", "sandbox", "agents"):
        return "review"
    return "review"


def main() -> int:
    if not ROUTERS_DIR.is_dir():
        print(f"FATAL: {ROUTERS_DIR} not found")
        return 1

    mounted = _mounted_in_main() | _mounted_via_domains()

    rows: list[tuple[str, str, str, str, str, str]] = []
    for path in sorted(ROUTERS_DIR.glob("*.py")):
        stem = path.stem
        if stem == "__init__":
            continue
        is_mounted = stem in mounted
        prefix, tag = _detect_prefix_tag(path)
        last = _git_last_modified(path)
        rec = _recommendation(stem, is_mounted, prefix)
        rows.append(
            (
                stem,
                "✅ yes" if is_mounted else "⚠️  no",
                last,
                prefix,
                tag,
                rec,
            )
        )

    total = len(rows)
    mounted_n = sum(1 for r in rows if r[1].startswith("✅"))
    unmounted_n = total - mounted_n

    by_rec = {"keep": 0, "review": 0, "deprecate": 0}
    for r in rows:
        by_rec[r[5]] += 1

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Unmounted Routers Inventory")
    lines.append("")
    lines.append(
        f"> Auto-generated by `scripts/inventory_unmounted_routers.py`. "
        f"Total: **{total}** · Mounted: **{mounted_n}** · "
        f"Unmounted: **{unmounted_n}**."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **keep** (already mounted): {by_rec['keep']}")
    lines.append(f"- **review** (unmounted, decide): {by_rec['review']}")
    lines.append(f"- **deprecate** (legacy v3/v10/v11/v12): {by_rec['deprecate']}")
    lines.append("")
    lines.append("## Decision rules")
    lines.append("")
    lines.append("- **keep** → router is wired; no action.")
    lines.append("- **review** → orphan but no obvious legacy marker. Decide: (a) wire into `api/main.py` or domain aggregator, (b) move to `archive/`, or (c) document why intentionally unmounted (admin-only, internal-only).")
    lines.append("- **deprecate** → versioned legacy. Schedule removal in a follow-up PR.")
    lines.append("")
    lines.append("## Full table")
    lines.append("")
    lines.append("| Router | Mounted | Last modified | Prefix | Tag | Recommendation |")
    lines.append("|--------|---------|---------------|--------|-----|----------------|")
    for stem, mflag, last, prefix, tag, rec in rows:
        lines.append(
            f"| `{stem}` | {mflag} | {last} | `{prefix or '—'}` | {tag or '—'} | **{rec}** |"
        )
    lines.append("")

    OUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"OK: wrote {OUT_FILE.relative_to(REPO)} · {total} routers "
        f"({mounted_n} mounted, {unmounted_n} unmounted)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
