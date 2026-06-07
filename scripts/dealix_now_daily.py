#!/usr/bin/env python3
"""Dealix Now — daily founder brief generator.

Builds today's deterministic Now pack and writes:
  - data/founder_briefs/{YYYY-MM-DD}.json   (full pack)
  - data/founder_briefs/{YYYY-MM-DD}.md     (Arabic Founder Daily Brief)
  - apps/web/public/now-pack.json           (refreshed live pack, is_sample=False)

Prints a short Arabic summary to stdout. NEVER sends anything: every draft is
approval-first and Dealix never auto-sends.

Usage:
    python scripts/dealix_now_daily.py [--date YYYY-MM-DD] [--out-dir PATH]

Fully offline: no LLM, no network, no API keys.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from dealix.now import build_now_pack, render_daily_brief_markdown  # noqa: E402

log = logging.getLogger("dealix_now_daily")

_DEFAULT_OUT_DIR = _REPO_ROOT / "data" / "founder_briefs"
_WEB_PACK = _REPO_ROOT / "apps" / "web" / "public" / "now-pack.json"


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def _summary_ar(pack: dict, json_path: Path, md_path: Path) -> str:
    m = pack["metrics"]
    priorities = pack.get("priorities", [])
    top = priorities[0]["what_ar"] if priorities else "—"
    lines = [
        f"Dealix Now — البريف اليومي ({pack['date']})",
        f"  leads: {m['leads_total']}  |  high: {m['priority_high']}  medium: {m['priority_medium']}  "
        f"nurture: {m['nurture']}  disqualified: {m['disqualified']}",
        f"  drafts جاهزة للمراجعة: {m['drafts_ready']}  |  متوسط الملاءمة: {m['avg_fit_score']}/100",
        f"  قيمة خط الأنابيب (typical): {m['pipeline_value_sar']['typical']:,} SAR",
        f"  أولوية اليوم #1: {top}",
        f"  ملف JSON: {json_path}",
        f"  ملف Markdown: {md_path}",
        "  ملاحظة: كل draft بانتظار موافقتك — Dealix لا يرسل تلقائيًا.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the Dealix Now daily founder brief.")
    parser.add_argument(
        "--date", default=None, help="Brief date (YYYY-MM-DD). Default: today (Asia/Riyadh)."
    )
    parser.add_argument(
        "--out-dir",
        default=str(_DEFAULT_OUT_DIR),
        help="Output directory for the dated brief files.",
    )
    args = parser.parse_args(argv)

    pack = build_now_pack(today=args.date)
    markdown = render_daily_brief_markdown(pack)

    date = pack["date"]
    out_dir = Path(args.out_dir)
    json_path = out_dir / f"{date}.json"
    md_path = out_dir / f"{date}.md"

    _write_json(json_path, pack)
    _write_text(md_path, markdown)
    # Refresh the live web pack (real run keeps is_sample=False).
    _write_json(_WEB_PACK, pack)

    print(_summary_ar(pack, json_path, md_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
