#!/usr/bin/env python3
"""Generate a curated knowledge pack from the indexed sources."""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "business" / "_data" / "knowledge_index.json"
OUT_DIR = ROOT / "business" / "knowledge" / "exports"


def main() -> int:
    if not IDX.exists():
        print("ERROR: knowledge index missing.")
        return 1
    data = json.loads(IDX.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()
    lines = [f"# Dealix Knowledge Pack — {date}", "", f"Indexed files: **{len(data['entries'])}**", ""]
    categories: dict[str, list[dict]] = {}
    for e in data["entries"]:
        top = e["path"].split("/", 2)[1] if "/" in e["path"] else "root"
        categories.setdefault(top, []).append(e)
    for cat, items in sorted(categories.items()):
        lines.append(f"## {cat} ({len(items)})")
        lines.append("")
        for e in items:
            lines.append(f"- `{e['path']}` — {e['title']}")
        lines.append("")
    out = OUT_DIR / f"knowledge-pack-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
