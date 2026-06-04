"""Daily Draft Factory — generate 400+ review-only founder drafts.

AI generates and ranks drafts only. Founder reviews and approves.
Nothing is sent. Outputs are written to outputs/commercial_launch/<DATE>/.

Usage:
    python scripts/commercial_generate_400_drafts.py --target 400
    python scripts/commercial_generate_400_drafts.py --target 400 --leads data/commercial_seed_leads.example.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date as date_cls
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import (
    OUTPUT_ROOT,
    SEED_LEADS,
    generate_drafts,
    load_all_configs,
    load_seed_leads,
    strip_internal,
)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(strip_internal(row), ensure_ascii=False) + "\n")


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def build_outputs(target: int, leads_path: Path | None, run_date: str, out_dir: Path) -> dict:
    cfg = load_all_configs()
    leads = load_seed_leads(leads_path) if leads_path else load_seed_leads()
    result = generate_drafts(target=target, leads=leads, run_date=run_date, cfg=cfg)
    drafts = result.drafts
    out_dir.mkdir(parents=True, exist_ok=True)

    by_status = Counter(d["status"] for d in drafts)
    by_channel = Counter(d["channel"] for d in drafts)
    by_vertical = Counter(d["vertical"] for d in drafts)
    by_language = Counter(d["language"] for d in drafts)

    reviewable = [
        d
        for d in drafts
        if d["status"] in ("founder_review", "needs_research", "ready_for_manual_copy")
    ]
    rejected = [d for d in drafts if d["status"].startswith("rejected_")]
    needs_research = [d for d in drafts if d["status"] == "needs_research"]
    ranked = sorted(reviewable, key=lambda d: d["priority_score"], reverse=True)
    top50 = ranked[:50]

    # ── draft_queue.jsonl
    _write_jsonl(out_dir / "draft_queue.jsonl", drafts)
    _write_jsonl(out_dir / "rejected_drafts.jsonl", rejected)
    _write_jsonl(out_dir / "needs_research.jsonl", needs_research)

    # ── founder_review.csv
    fields = [
        "draft_id",
        "company_name",
        "vertical",
        "channel",
        "language",
        "buyer_title",
        "offer_stage",
        "priority_score",
        "quality_score",
        "compliance_score",
        "fit_score",
        "risk_level",
        "status",
        "send_allowed",
        "external_send_blocked",
        "requires_founder_approval",
        "no_auto_send",
    ]
    with (out_dir / "founder_review.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for d in ranked:
            w.writerow({k: d.get(k) for k in fields})

    # ── approved_manual_sends.example.csv (empty template — founder fills after approval)
    with (out_dir / "approved_manual_sends.example.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "draft_id",
                "company_name",
                "channel",
                "approved_by_founder",
                "approved_at",
                "manual_action_taken",
                "reply_status",
                "notes",
            ]
        )
        w.writerow(
            [
                "# Fill ONLY after founder approval. AI never sends. Manual action only.",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )

    # ── reports JSON
    quality_report = {
        "schema_version": "1.0",
        "run_date": run_date,
        "pass_threshold": cfg["quality"]["pass_threshold"],
        "rejected_quality": by_status.get("rejected_quality", 0),
        "avg_quality_score": round(
            sum(d["quality_score"] for d in drafts) / max(1, len(drafts)), 1
        ),
        "below_threshold_reasons": Counter(
            r
            for d in drafts
            if d["status"] == "rejected_quality"
            for r in (d["rejection_reason"].split("; ") if d["rejection_reason"] else [])
        ),
    }
    quality_report["below_threshold_reasons"] = dict(quality_report["below_threshold_reasons"])
    (out_dir / "quality_report.json").write_text(
        json.dumps(quality_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    compliance_report = {
        "schema_version": "1.0",
        "run_date": run_date,
        "pass_threshold": cfg["compliance"]["pass_threshold"],
        "rejected_compliance": by_status.get("rejected_compliance", 0),
        "avg_compliance_score": round(
            sum(d["compliance_score"] for d in drafts) / max(1, len(drafts)), 1
        ),
        "risk_levels": dict(Counter(d["risk_level"] for d in drafts)),
    }
    (out_dir / "compliance_report.json").write_text(
        json.dumps(compliance_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    daily_metrics = {
        "schema_version": "1.0",
        "run_date": run_date,
        "drafts_generated": len(drafts),
        "target": target,
        "target_met": len(drafts) >= target,
        "founder_review_count": by_status.get("founder_review", 0),
        "needs_research": by_status.get("needs_research", 0),
        "rejected_quality": by_status.get("rejected_quality", 0),
        "rejected_compliance": by_status.get("rejected_compliance", 0),
        "approved_manual": 0,
        "channel_distribution": dict(by_channel),
        "vertical_distribution": dict(by_vertical),
        "language_distribution": dict(by_language),
        "top_vertical": by_vertical.most_common(1)[0][0] if by_vertical else None,
        "top_channel": by_channel.most_common(1)[0][0] if by_channel else None,
        "used_real_leads": result.used_real_leads,
        "warnings_count": len(result.warnings),
        "safety_flags_invariant": {
            "send_allowed": False,
            "external_send_blocked": True,
            "requires_founder_approval": True,
            "no_auto_send": True,
        },
    }
    (out_dir / "daily_metrics.json").write_text(
        json.dumps(daily_metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    batch_manifest = {
        "schema_version": "1.0",
        "batch_id": f"BATCH-{run_date}",
        "run_date": run_date,
        "total_drafts": len(drafts),
        "files": [
            "draft_queue.jsonl",
            "founder_review.csv",
            "founder_review.md",
            "top_50_priority.md",
            "rejected_drafts.jsonl",
            "needs_research.jsonl",
            "compliance_report.json",
            "quality_report.json",
            "daily_metrics.json",
            "next_actions.md",
            "approved_manual_sends.example.csv",
        ],
        "doctrine": "AI drafts only. Founder approves. No external sending.",
    }
    (out_dir / "batch_manifest.json").write_text(
        json.dumps(batch_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ── founder_review.md
    top_value = sorted(reviewable, key=lambda d: d["priority_score"], reverse=True)[:10]
    top_risk = sorted(
        drafts, key=lambda d: (d["risk_level"] == "high", -d["priority_score"]), reverse=True
    )[:10]
    fr = []
    fr.append("# Founder Review — Daily Draft Queue")
    fr.append(
        f"\n**Run date:** {run_date}  \n**Doctrine:** AI drafts only. Founder approves. "
        "No external sending.\n"
    )
    fr.append("## Executive Summary\n")
    fr.append(
        f"- Total Drafts Generated: **{len(drafts)}** (target {target}, "
        f"met: {daily_metrics['target_met']})"
    )
    fr.append(f"- Accepted into Founder Review: **{by_status.get('founder_review', 0)}**")
    fr.append(f"- Needs Research: **{by_status.get('needs_research', 0)}**")
    fr.append(f"- Rejected (Quality): **{by_status.get('rejected_quality', 0)}**")
    fr.append(f"- Rejected (Compliance): **{by_status.get('rejected_compliance', 0)}**")
    fr.append(f"- Used real seed leads: **{result.used_real_leads}**\n")
    fr.append("## Channel Distribution\n")
    fr.append(_md_table(["Channel", "Count"], [[k, v] for k, v in by_channel.items()]))
    fr.append("\n## Vertical Distribution\n")
    fr.append(_md_table(["Vertical", "Count"], [[k, v] for k, v in by_vertical.items()]))
    fr.append("\n## Language Distribution\n")
    fr.append(_md_table(["Language", "Count"], [[k, v] for k, v in by_language.items()]))
    fr.append("\n## Top 50 Priority Drafts\n")
    fr.append(
        _md_table(
            ["Rank", "Company", "Vertical", "Channel", "Lang", "Priority", "Risk", "Status"],
            [
                [
                    i + 1,
                    d["company_name"],
                    d["vertical"],
                    d["channel"],
                    d["language"],
                    d["priority_score"],
                    d["risk_level"],
                    d["status"],
                ]
                for i, d in enumerate(top50)
            ],
        )
    )
    fr.append("\n## Top 10 Highest-Value Opportunities\n")
    fr.append(
        _md_table(
            ["Company", "Vertical", "Offer", "Priority"],
            [
                [d["company_name"], d["vertical"], d["offer_name"], d["priority_score"]]
                for d in top_value
            ],
        )
    )
    fr.append("\n## Top 10 Risk Items\n")
    fr.append(
        _md_table(
            ["Company", "Vertical", "Risk", "Reason"],
            [
                [
                    d["company_name"],
                    d["vertical"],
                    d["risk_level"],
                    d["rejection_reason"] or "review",
                ]
                for d in top_risk
            ],
        )
    )
    fr.append("\n## Manual Actions for Founder\n")
    fr.append("1. Review the Top 50 above; approve only what fits.")
    fr.append("2. Copy approved drafts manually into the chosen channel. AI never sends.")
    fr.append("3. Research any `needs_research` drafts before contacting anyone.")
    fr.append("\n## Today's Recommended Focus\n")
    fr.append(
        f"- Best sector: **{daily_metrics['top_vertical']}**; "
        f"best channel: **{daily_metrics['top_channel']}**."
    )
    fr.append("\n## Go/No-Go by Channel\n")
    fr.append(
        "- Email: GO for manual copy after external readiness (SPF/DKIM/DMARC). NO bulk send."
    )
    fr.append("- LinkedIn: GO for manual note only. NO automation.")
    fr.append("- WhatsApp: NO cold outreach. Opt-in inbound replies only.")
    fr.append("- Website forms: GO for manual copy. NO auto-submit.")
    fr.append("\n## Warnings\n")
    for wmsg in result.warnings or ["None."]:
        fr.append(f"- {wmsg}")
    fr.append("\n## Next Steps\n")
    fr.append("- See `next_actions.md` and `top_50_priority.md`.")
    (out_dir / "founder_review.md").write_text("\n".join(fr), encoding="utf-8")

    # ── top_50_priority.md
    tp = ["# Top 50 Priority Drafts", f"\n**Run date:** {run_date}\n"]
    for i, d in enumerate(top50):
        tp.append(f"\n## {i + 1}. {d['company_name']}")
        tp.append(f"- Rank: {i + 1}")
        tp.append(f"- Vertical: {d['vertical']}")
        tp.append(f"- Buyer Title: {d['buyer_title']}")
        tp.append(f"- Channel: {d['channel']}")
        tp.append(f"- Language: {d['language']}")
        tp.append(f"- Pain Angle: {d['pain_angle']}")
        tp.append(f"- Offer: {d['offer_name']} ({d['offer_stage']})")
        tp.append(f"- Priority Score: {d['priority_score']}")
        tp.append(f"- Risk Level: {d['risk_level']}")
        tp.append(
            f"- Why This Lead Matters: trigger = {d['trigger_event']}; " f"fit = {d['fit_score']}"
        )
        tp.append(
            "- Manual Action: founder reviews, then copies manually if approved. AI never sends."
        )
        tp.append(
            f"- Draft Preview:\n\n> Subject: {d['subject']}\n>\n> "
            + d["body"].replace("\n", "\n> ")
        )
    (out_dir / "top_50_priority.md").write_text("\n".join(tp), encoding="utf-8")

    # ── next_actions.md
    na = ["# Next Actions — Founder", f"\n**Run date:** {run_date}\n"]
    na.append("## What to review first\n- Top 10 highest-value + all `high` risk items.")
    na.append("## What to send manually\n- Only founder-approved drafts. Copy by hand.")
    na.append("## What to hold\n- Anything you are unsure about; hold beats a bad first touch.")
    na.append("## What needs research\n- All `needs_research` drafts (placeholder companies).")
    na.append(
        "## What not to touch\n- WhatsApp cold outreach, LinkedIn automation, bulk email — forbidden."
    )
    best_sectors = [k for k, _ in by_vertical.most_common(3)]
    na.append("## Best 3 sectors today\n- " + ", ".join(best_sectors))
    na.append(
        "## Best 10 companies today\n"
        + "\n".join(
            f"- {d['company_name']} ({d['vertical']}, priority {d['priority_score']})"
            for d in top_value
        )
    )
    na.append(
        "## Suggested founder message of the day\n"
        "- Pick the single highest-fit reviewed draft and personalize one sentence before sending manually."
    )
    na.append(
        "## Tomorrow improvement loop\n"
        "- Log replies, refine angles per objection, rotate the next sector focus."
    )
    (out_dir / "next_actions.md").write_text("\n".join(na), encoding="utf-8")

    return {
        "out_dir": str(out_dir),
        "total": len(drafts),
        "target": target,
        "target_met": len(drafts) >= target,
        "by_status": dict(by_status),
        "warnings": result.warnings,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate 400+ review-only founder drafts.")
    ap.add_argument("--target", type=int, default=400)
    ap.add_argument("--date", default=date_cls.today().isoformat())
    ap.add_argument("--leads", default=None, help="Path to seed leads JSONL (optional).")
    ap.add_argument("--out", default=None, help="Override output directory.")
    args = ap.parse_args(argv)

    leads_path = Path(args.leads) if args.leads else (SEED_LEADS if SEED_LEADS.exists() else None)
    out_dir = Path(args.out) if args.out else (OUTPUT_ROOT / args.date)
    summary = build_outputs(args.target, leads_path, args.date, out_dir)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["target_met"]:
        print(f"ERROR: generated {summary['total']} < target {summary['target']}")
        return 1
    # Hard invariant: nothing is sendable
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
