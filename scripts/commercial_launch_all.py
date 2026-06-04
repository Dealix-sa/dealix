#!/usr/bin/env python3
"""Launch everything — single orchestrator for the Commercial Launch OS.

Runs the full daily launch pipeline in-process and writes a consolidated
LAUNCH_SNAPSHOT to today's output folder:

  1. Generate 400+ founder-review drafts (approval-gated)
  2. Hard safety assertion + safety audit (no external send)
  3. Launch readiness verification
  4. 30-day media/social content calendar (plan only)
  5. Metrics snapshot
  6. Seed-lead validation

The system NEVER sends anything externally. AI drafts and ranks; the founder
reviews and approves.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json

import commercial_launch_lib as lib
import commercial_launch_readiness as readiness
import commercial_safety_audit as safety
import commercial_seed_leads_validate as seed
import media_social_calendar_generate as media


def run_all(target: int = 400, date: str | None = None) -> dict:
    config = lib.load_all_config()

    # 1. Generate + 2. hard safety guarantee
    drafts = lib.generate_drafts(target=target, config=config)
    lib.assert_safety(drafts)
    out = lib.write_outputs(drafts, config, date=date)
    summary = lib.summarize(drafts)

    # 3. Safety audit (scans code + the batch we just wrote)
    audit = safety.run_audit()

    # 4. Readiness
    ready = readiness.check()

    # 5. Media/social calendar (plan only, no auto-publish)
    calendar = media.build_calendar()
    media_dir = out / "media_social"
    media_dir.mkdir(parents=True, exist_ok=True)
    (media_dir / "content_calendar.json").write_text(
        json.dumps({"days": len(calendar), "auto_publish": False, "calendar": calendar}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 6. Seed validation
    seeds = seed.validate()

    snapshot = {
        "generated_at": _dt.datetime.now(_dt.UTC).isoformat(),
        "golden_rule": config["launch"]["golden_rule"],
        "target": target,
        "drafts": summary,
        "safety_audit": {"verdict": audit["verdict"], "drafts_checked": audit["drafts_checked"]},
        "readiness": {"verdict": ready["verdict"]},
        "media_calendar_days": len(calendar),
        "seed_validation": {"verdict": seeds["verdict"], "rows": seeds["rows"]},
        "safety_flags": lib.SAFETY_FLAGS,
        "external_sends_performed": 0,
        "output_dir": str(out),
    }

    (out / "LAUNCH_SNAPSHOT.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "LAUNCH_SNAPSHOT.md").write_text(_render_md(snapshot), encoding="utf-8")
    return snapshot


def _render_md(s: dict) -> str:
    d = s["drafts"]
    lines = [
        "# Dealix — Launch Snapshot",
        "",
        f"_Generated: {s['generated_at']}_",
        "",
        f"> {s['golden_rule']}",
        "",
        "## Pipeline result",
        f"- Drafts generated: **{d['drafts_generated']}** (target {s['target']})",
        f"- Into founder review: **{d['founder_review_count']}**",
        f"- Rejected (quality): {d['rejected_quality']} · Rejected (compliance): {d['rejected_compliance']} · Needs research: {d['needs_research']}",
        f"- Safety audit: **{s['safety_audit']['verdict']}** ({s['safety_audit']['drafts_checked']} drafts checked)",
        f"- Readiness: **{s['readiness']['verdict']}**",
        f"- Media calendar: **{s['media_calendar_days']} days** (plan only, no auto-publish)",
        f"- Seed validation: **{s['seed_validation']['verdict']}** ({s['seed_validation']['rows']} rows)",
        f"- External sends performed: **{s['external_sends_performed']}** (by design — the system never sends)",
        "",
        "## What the founder does next",
        "1. Open `top_50_priority.md` and approve the top 20–50 manually.",
        "2. Send approved drafts manually (email/LinkedIn) — never via this system.",
        "3. Update CRM stages and suppression list.",
        "4. Adapt and publish one social calendar item manually.",
        "",
        "## Channel Go/No-Go",
        "- Cold email: **NO-GO** until SPF/DKIM/DMARC + manual founder send.",
        "- Follow-up: **NO-GO** until a prior legitimate touch exists.",
        "- LinkedIn: **MANUAL-ONLY** (no automation).",
        "- Website form: **NO AUTO-SUBMIT**.",
        "- Paid ads: **NO-GO** until tracking + legal/privacy review.",
        "",
        "See `docs/commercial-launch/01_MASTER_LAUNCH_PLAN_A_TO_Z.md` for the full plan.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch everything (no external send)")
    parser.add_argument("--target", type=int, default=400)
    parser.add_argument("--date", type=str, default=None)
    args = parser.parse_args(argv)

    snapshot = run_all(target=args.target, date=args.date)

    print("🚀 Dealix launch pipeline complete (no external sends).")
    print(f"   Drafts: {snapshot['drafts']['drafts_generated']} | Review: {snapshot['drafts']['founder_review_count']}")
    print(f"   Safety: {snapshot['safety_audit']['verdict']} | Readiness: {snapshot['readiness']['verdict']}")
    print(f"   Media calendar: {snapshot['media_calendar_days']} days | Seeds: {snapshot['seed_validation']['verdict']}")
    print(f"   Snapshot: {snapshot['output_dir']}/LAUNCH_SNAPSHOT.md")

    failures = []
    if snapshot["safety_audit"]["verdict"] != "PASS":
        failures.append("safety_audit")
    if snapshot["readiness"]["verdict"] != "READY":
        failures.append("readiness")
    if snapshot["seed_validation"]["verdict"] != "PASS":
        failures.append("seed_validation")
    if snapshot["drafts"]["drafts_generated"] < args.target:
        failures.append("draft_target")
    if failures:
        print(f"❌ Launch gate failures: {failures}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
