#!/usr/bin/env python3
"""Build a deterministic local knowledge index from sources."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "business" / "_data" / "knowledge_sources.json"
OUT = ROOT / "business" / "_data" / "knowledge_index.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if not SRC.exists():
        print("ERROR: knowledge_sources.json missing.")
        return 1
    cfg = json.loads(SRC.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for src in cfg.get("sources", []):
        base = ROOT / src
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            text = p.read_text(encoding="utf-8")
            first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
            title = first_line.lstrip("# ").strip() or p.stem
            entries.append({
                "path": str(p.relative_to(ROOT)),
                "title": title,
                "preview": text[:500],
                "chars": len(text),
            })
    OUT.write_text(
        json.dumps({
            "version": 1,
            "builtAt": _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds"),
            "demo": bool(args.demo),
            "entries": entries,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"indexed {len(entries)} files → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
