#!/usr/bin/env python3
"""Generate a bilingual client status report."""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.workspace_store import find, load

OUT_DIR = Path(__file__).resolve().parent.parent / "business" / "proof" / "exports"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    args = parser.parse_args()

    data = load()
    w = find(data["workspaces"], args.client_id)
    if not w:
        print("ERROR: workspace not found.", file=sys.stderr)
        return 1
    out_dir = OUT_DIR / w["clientId"]
    out_dir.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()

    def render(lang: str) -> str:
        if lang == "ar":
            return (
                f"# تقرير حالة — {w['clientName']} ({date})\n\n"
                f"- الباقة: {w['offer']}\n"
                f"- الحالة: {w['status']}\n"
                f"- المراجعة القادمة: {w.get('nextReview','—')}\n\n"
                "## التسليمات\n"
                + "\n".join(f"- {d['title']} — {d['status']}" for d in w["deliverables"])
                + "\n\n## الموافقات\n"
                + "\n".join(f"- {a['item']} — {a['status']}" for a in w["approvals"])
                + "\n\n## الإثباتات\n"
                + "\n".join(f"- {p['title']} (دليل: {p['evidence']}, {p['date']})" for p in w["proofItems"])
                + "\n"
            )
        return (
            f"# Status report — {w['clientName']} ({date})\n\n"
            f"- Offer: {w['offer']}\n"
            f"- Status: {w['status']}\n"
            f"- Next review: {w.get('nextReview','—')}\n\n"
            "## Deliverables\n"
            + "\n".join(f"- {d['title']} — {d['status']}" for d in w["deliverables"])
            + "\n\n## Approvals\n"
            + "\n".join(f"- {a['item']} — {a['status']}" for a in w["approvals"])
            + "\n\n## Proof\n"
            + "\n".join(f"- {p['title']} (evidence: {p['evidence']}, {p['date']})" for p in w["proofItems"])
            + "\n"
        )

    written: list[Path] = []
    if args.lang in ("ar", "both"):
        p = out_dir / f"status-{date}-ar.md"
        p.write_text(render("ar"), encoding="utf-8")
        written.append(p)
    if args.lang in ("en", "both"):
        p = out_dir / f"status-{date}-en.md"
        p.write_text(render("en"), encoding="utf-8")
        written.append(p)

    for p in written:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
