#!/usr/bin/env python3
"""Generate the Campaign Command Room report.

Reads:
  - $PRIVATE_OPS/campaigns/campaign_registry.csv
  - $PRIVATE_OPS/campaigns/campaign_assets.csv
  - $PRIVATE_OPS/campaigns/campaign_queue.csv
  - $PRIVATE_OPS/campaigns/campaign_results.csv

Writes:
  - $PRIVATE_OPS/campaigns/campaign_command_report.md
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    BOOTSTRAP_ROOT,
    ReportContext,
    load_with_fallback,
    now_iso,
    private_ops_root,
    safe_int,
    write_markdown,
)


def main() -> int:
    priv = private_ops_root()
    files = {
        "registry": (
            priv / "campaigns" / "campaign_registry.csv",
            BOOTSTRAP_ROOT / "campaigns" / "campaign_registry.csv",
        ),
        "assets": (
            priv / "campaigns" / "campaign_assets.csv",
            BOOTSTRAP_ROOT / "campaigns" / "campaign_assets.csv",
        ),
        "queue": (
            priv / "campaigns" / "campaign_queue.csv",
            BOOTSTRAP_ROOT / "campaigns" / "campaign_queue.csv",
        ),
        "results": (
            priv / "campaigns" / "campaign_results.csv",
            BOOTSTRAP_ROOT / "campaigns" / "campaign_results.csv",
        ),
    }

    loaded: dict[str, list[dict[str, str]]] = {}
    fallbacks: list[Path] = []
    for key, (primary, bootstrap) in files.items():
        _, rows, source = load_with_fallback(primary, bootstrap)
        loaded[key] = rows
        if source == "fallback":
            fallbacks.append(bootstrap)

    ctx = ReportContext(
        name="Campaign Command Room",
        runtime_paths_checked=[p for p, _ in files.values()],
        fallback_paths_used=fallbacks,
        started_at=now_iso(),
    )

    registry = loaded["registry"]
    assets = loaded["assets"]
    queue = loaded["queue"]
    results = loaded["results"]

    lines = ctx.header()

    status_counts: dict[str, int] = defaultdict(int)
    for r in registry:
        status_counts[(r.get("status") or "draft").strip() or "draft"] += 1
    lines += [
        "## Campaigns by status",
        "",
    ]
    for s in ("draft", "pending_approval", "live", "paused", "complete", "killed"):
        lines.append(f"- **{s}**: {status_counts.get(s, 0)}")

    lines += [
        "",
        "## Queue health",
        "",
    ]
    queue_status: dict[str, int] = defaultdict(int)
    for q in queue:
        queue_status[(q.get("send_status") or "queued").strip() or "queued"] += 1
    for s in ("queued", "approved", "sent", "held", "rejected"):
        lines.append(f"- **{s}**: {queue_status.get(s, 0)}")

    lines += [
        "",
        "## Assets by approval status",
        "",
    ]
    asset_approval: dict[str, int] = defaultdict(int)
    asset_proof: dict[str, int] = defaultdict(int)
    for a in assets:
        asset_approval[(a.get("approval_status") or "pending").strip() or "pending"] += 1
        asset_proof[(a.get("proof_status") or "n_a").strip() or "n_a"] += 1
    lines.append("Approval:")
    for k, v in sorted(asset_approval.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("Proof status:")
    for k, v in sorted(asset_proof.items()):
        lines.append(f"- {k}: {v}")

    lines += [
        "",
        "## Results aggregate (since file inception)",
        "",
    ]
    totals = defaultdict(int)
    by_channel: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in results:
        for col in (
            "impressions",
            "clicks",
            "replies",
            "positive_replies",
            "samples",
            "proposals",
            "payments",
        ):
            v = safe_int(row.get(col))
            totals[col] += v
            by_channel[row.get("channel", "unknown")][col] += v

    if not results:
        lines.append("_No results captured yet. Populate `campaign_results.csv` weekly._")
    else:
        for col in (
            "impressions",
            "clicks",
            "replies",
            "positive_replies",
            "samples",
            "proposals",
            "payments",
        ):
            lines.append(f"- **{col}**: {totals[col]}")

        lines += [
            "",
            "### By channel",
            "",
            "| Channel | Replies | Positive | Samples | Proposals | Payments |",
            "| ------- | ------- | -------- | ------- | --------- | -------- |",
        ]
        for ch, vals in sorted(by_channel.items()):
            lines.append(
                f"| {ch} | {vals['replies']} | {vals['positive_replies']} "
                f"| {vals['samples']} | {vals['proposals']} | {vals['payments']} |"
            )

    lines += [
        "",
        "## Doctrine reminders",
        "",
        "- Nothing exits the queue without an explicit approval row.",
        "- Reported numbers are observed signals, not guaranteed outcomes.",
        "- Scale / Fix / Kill decisions belong in the weekly growth review.",
    ]

    out = priv / "campaigns" / "campaign_command_report.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
