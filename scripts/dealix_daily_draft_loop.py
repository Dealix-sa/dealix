#!/usr/bin/env python3
"""Dealix daily draft loop — the "company starts now" heartbeat.

Runs the commercial orchestrator over the curated Saudi B2B target frame,
produces COMPANY-LEVEL bilingual first-touch drafts, queues every one of them
for founder approval, and writes a founder brief (Markdown + JSON).

Degraded-but-real: needs ZERO secrets. With no API keys, no database, and no
network it still produces real drafts to `data/founder_briefs/` and a durable
approval queue under `var/`. Secrets only ever flip "draft → live send".

Usage:
    python scripts/dealix_daily_draft_loop.py                # write brief + queue
    python scripts/dealix_daily_draft_loop.py --print        # also echo to stdout
    python scripts/dealix_daily_draft_loop.py --no-enqueue   # render only, no queue
    python scripts/dealix_daily_draft_loop.py --limit 10     # first N prospects

Doctrine: nothing is sent. Every draft is company-level, approval_required, and
carries `consent_status=required_before_contact`.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.commercial_orchestrator import (  # noqa: E402
    draft_queue,
    load_prospects,
    run_acquisition_to_drafts,
)

_DISCLAIMER = (
    "النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed."
)


def _build_markdown(date: str, result, queue_stats: dict) -> str:
    lines: list[str] = []
    lines.append(f"# Dealix · موجز الدرافتات اليومي · {date}")
    lines.append("")
    s = result.summary()
    lines.append(
        f"**درافتات جاهزة لموافقتك:** {s['generated']}  ·  **مُتجاوَزة:** {s['skipped']}  "
        f"·  **إجمالي الطابور المعلّق:** {queue_stats.get('pending', 0)}"
    )
    lines.append("")
    lines.append(
        "> كل درافت أدناه على **مستوى الشركة**، بانتظار **موافقتك** قبل أي تواصل. "
        "لا يُرسَل شيء تلقائياً. اعتمِد أو ارفض عبر `/api/v1/founder/approvals` أو لوحة الموافقات."
    )
    lines.append("")
    if s["by_sector"]:
        by_sector = ", ".join(f"{k}: {v}" for k, v in sorted(s["by_sector"].items()))
        lines.append(f"**حسب القطاع:** {by_sector}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## الدرافتات / Drafts")
    lines.append("")
    for i, d in enumerate(result.drafts, 1):
        lines.append(
            f"### {i}. {d.get('company_name')} "
            f"· {d.get('sector')} · {d.get('city')} "
            f"· ICP {d.get('icp_score')} ({d.get('icp_band')})"
        )
        lines.append(f"- **id:** `{d.get('id', 'n/a')}`  ·  **status:** {d.get('status', 'pending')}")
        lines.append(f"- **offer:** {d.get('offer')}  ·  **consent:** {d.get('consent_status')}")
        lines.append(f"- **subject (EN):** {d.get('subject_en')}")
        lines.append(f"- **subject (AR):** {d.get('subject_ar')}")
        if d.get("source_url"):
            lines.append(f"- **source:** {d.get('source_type')} — {d.get('source_url')}")
        lines.append("")
        lines.append("<details><summary>عرض نص المسوّدة / Show draft body</summary>")
        lines.append("")
        lines.append(d.get("body_md", "").strip())
        lines.append("")
        lines.append("</details>")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"_{_DISCLAIMER}_")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix daily draft loop")
    ap.add_argument("--print", dest="echo", action="store_true",
                    help="echo the brief to stdout")
    ap.add_argument("--out-dir", default="data/founder_briefs",
                    help="output directory for the founder brief")
    ap.add_argument("--min-band", default="warm",
                    help="minimum ICP band that earns a draft (cold|cool|warm|hot)")
    ap.add_argument("--limit", type=int, default=0,
                    help="only process the first N prospects (0 = all)")
    ap.add_argument("--no-enqueue", dest="enqueue", action="store_false",
                    help="render drafts without writing to the approval queue")
    args = ap.parse_args(argv)

    prospects = load_prospects()
    if args.limit > 0:
        prospects = prospects[: args.limit]

    if not prospects:
        print("[daily-loop] no prospects found at data/leads/saudi_b2b_prospects.csv",
              file=sys.stderr)
        return 1

    result = run_acquisition_to_drafts(
        prospects, min_band=args.min_band, enqueue_drafts=args.enqueue
    )
    queue_stats = draft_queue.stats()
    date = datetime.now(UTC).strftime("%Y-%m-%d")

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = _REPO_ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    md = _build_markdown(date, result, queue_stats)
    md_path = out_dir / f"daily_drafts_{date}.md"
    json_path = out_dir / f"daily_drafts_{date}.json"
    payload = {
        "date": date,
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": result.summary(),
        "queue_stats": queue_stats,
        "drafts": result.drafts,
        "doctrine": {
            "no_live_send": True,
            "approval_required": True,
            "company_level_only": True,
            "disclaimer": _DISCLAIMER,
        },
    }
    md_path.write_text(md, encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[daily-loop] {result.generated} drafts generated, "
          f"{queue_stats.get('pending', 0)} pending approval")
    print(f"[daily-loop] brief: {md_path}")
    print(f"[daily-loop] json:  {json_path}")
    if args.echo:
        print("\n" + "=" * 72 + "\n")
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
