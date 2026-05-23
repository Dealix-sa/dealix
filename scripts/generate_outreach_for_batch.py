#!/usr/bin/env python3
"""generate_outreach_for_batch.py — Render per-lead drafts from a batch CSV.

Reads the batch CSV + the outreach message library and writes one markdown
file per language under `acquisition/outreach_messages/_rendered/<batch>/`.
Drafts only — no send, no Gmail API, nothing networked.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_DIR = REPO_ROOT / "acquisition" / "outreach_messages"


def load_library() -> dict[str, str]:
    """Parse the message library into {message_id: body}."""
    library: dict[str, str] = {}
    for md in LIBRARY_DIR.glob("*.md"):
        text = md.read_text(encoding="utf-8")
        for match in re.finditer(
            r"^## (?P<mid>[a-z0-9_]+)[^\n]*\n+```\n(?P<body>.*?)```",
            text,
            re.DOTALL | re.MULTILINE,
        ):
            library[match.group("mid")] = match.group("body").strip()
    return library


def render(body: str, row: dict[str, str]) -> str:
    company = row.get("company", "{company}")
    return (
        body.replace("{company}", company)
        .replace("{الشركة}", company)
        .replace("{first_name_or_team}", "team")
        .replace("{الفريق_أو_الاسم_الأول}", "الفريق")
    )


def render_batch(batch_path: Path) -> int:
    library = load_library()
    if not library:
        print("no outreach library found", file=sys.stderr)
        return 1
    with batch_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    out_dir = LIBRARY_DIR / "_rendered" / batch_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    rendered_count = 0
    for row in rows:
        base_id = row.get("suggested_message_id") or ""
        if not base_id:
            continue
        for suffix in ("_en", "_ar", "_followup_en", "_followup_ar"):
            mid = base_id if base_id.endswith(suffix) else base_id.replace("_en", suffix)
            if mid not in library:
                continue
            body = render(library[mid], row)
            slug = re.sub(r"[^a-z0-9]+", "-", row.get("company", "x").lower()).strip("-")
            target = out_dir / f"{slug}__{mid}.md"
            target.write_text(
                f"# {row.get('company')} — {mid}\n\n"
                f"Status: DRAFT — requires founder approval before send.\n\n"
                f"```\n{body}\n```\n",
                encoding="utf-8",
            )
            rendered_count += 1
    print(f"rendered {rendered_count} draft files under {out_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to batch CSV.")
    args = parser.parse_args()
    return render_batch(Path(args.file))


if __name__ == "__main__":
    sys.exit(main())
