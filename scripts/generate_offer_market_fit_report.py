#!/usr/bin/env python3
"""Generate the offer-market fit report from offer_market_fit_tests.csv."""

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
    write_markdown,
)

DECISIONS = ("scale", "fix", "kill", "hold")


def main() -> int:
    priv = private_ops_root()
    primary = priv / "market_attack" / "offer_market_fit_tests.csv"
    bootstrap = BOOTSTRAP_ROOT / "market_attack" / "offer_market_fit_tests.csv"

    _, rows, source = load_with_fallback(primary, bootstrap)
    ctx = ReportContext(
        name="Offer-Market Fit Report",
        runtime_paths_checked=[primary],
        fallback_paths_used=[] if source == "runtime" else [bootstrap],
        started_at=now_iso(),
    )

    by_decision: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_sector: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        d = (r.get("decision") or "hold").strip() or "hold"
        by_decision[d].append(r)
        by_sector[r.get("sector", "unknown")].append(r)

    lines = ctx.header()
    lines += [
        "## Tests by decision",
        "",
    ]
    for d in DECISIONS:
        n = len(by_decision.get(d, []))
        lines.append(f"- **{d}**: {n}")

    for d in DECISIONS:
        tests = by_decision.get(d, [])
        if not tests:
            continue
        lines += [
            "",
            f"### {d.title()}",
            "",
            "| Test | Sector | Offer | Channel | Hypothesis | Result | Next Action |",
            "| ---- | ------ | ----- | ------- | ---------- | ------ | ----------- |",
        ]
        for t in tests:
            lines.append(
                f"| {t.get('test_id','')} | {t.get('sector','')} "
                f"| {t.get('offer','')} | {t.get('channel','')} "
                f"| {t.get('hypothesis','')} | {t.get('result','pending')} "
                f"| {t.get('next_action','')} |"
            )

    lines += [
        "",
        "## Per-sector signal summary",
        "",
        "| Sector | Tests | Scale | Fix | Kill | Hold |",
        "| ------ | ----- | ----- | --- | ---- | ---- |",
    ]
    for sector, items in sorted(by_sector.items()):
        counts = defaultdict(int)
        for it in items:
            counts[(it.get("decision") or "hold").strip() or "hold"] += 1
        lines.append(
            f"| {sector} | {len(items)} | {counts['scale']} "
            f"| {counts['fix']} | {counts['kill']} | {counts['hold']} |"
        )

    lines += [
        "",
        "## Doctrine reminders",
        "",
        "- Signals are directional. No guaranteed revenue claim is allowed.",
        "- Scale requires positive_reply_rate ≥ 30% AND at least one proposal sent.",
        "- Kill requires sample_size ≥ 30 with positive_reply_rate < 10%.",
        "- Every decision must be reflected in `MARKET_LEARNING_MEMORY.md`.",
    ]

    out = priv / "market_attack" / "offer_market_fit_report.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
