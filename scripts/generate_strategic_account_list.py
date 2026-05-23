#!/usr/bin/env python3
"""Generate the Strategic Account List markdown report."""

from __future__ import annotations

import sys
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


def main() -> int:
    priv = private_ops_root()
    primary = priv / "market_attack" / "strategic_accounts.csv"
    bootstrap = BOOTSTRAP_ROOT / "market_attack" / "strategic_accounts.csv"

    _, rows, source = load_with_fallback(primary, bootstrap)
    ctx = ReportContext(
        name="Strategic Account Attack Plan",
        runtime_paths_checked=[primary],
        fallback_paths_used=[] if source == "runtime" else [bootstrap],
        started_at=now_iso(),
    )

    by_tier: dict[str, list[dict[str, str]]] = {
        "T0": [],
        "T1": [],
        "T2": [],
        "T3": [],
    }
    violations: list[str] = []
    for r in rows:
        prio = (r.get("priority") or "").strip() or "T3"
        by_tier.setdefault(prio, []).append(r)
        if prio in ("T0", "T1") and not (r.get("relationship_path") or "").strip():
            violations.append(
                f"{r.get('account_id','?')} {r.get('company','')} "
                "is T0/T1 but has no relationship_path."
            )

    lines = ctx.header()

    active = len(by_tier.get("T0", [])) + len(by_tier.get("T1", []))
    lines += [
        f"_Active T0+T1 accounts: {active} (ceiling 25)._",
        "",
    ]
    if active > 25:
        lines.append(
            "> **Warning:** Active T0+T1 exceeds the 25 ceiling. Demote, "
            "close, or park accounts before adding new ones."
        )
        lines.append("")

    for tier in ("T0", "T1", "T2", "T3"):
        accounts = by_tier.get(tier, [])
        lines.append(f"## Tier {tier}")
        lines.append("")
        if not accounts:
            lines.append(f"_No accounts at {tier}._")
            lines.append("")
            continue
        lines.append(
            "| Account | Sector | Buyer | Why Strategic | Path | Next Action | Status |"
        )
        lines.append(
            "| ------- | ------ | ----- | ------------- | ---- | ----------- | ------ |"
        )
        for r in accounts:
            lines.append(
                f"| {r.get('account_id','')} {r.get('company','')} "
                f"| {r.get('sector','')} | {r.get('buyer_title','')} "
                f"| {r.get('why_strategic','')} | {r.get('relationship_path','')} "
                f"| {r.get('next_action','')} | {r.get('status','')} |"
            )
        lines.append("")

    lines.append("## Out-of-bounds rows")
    lines.append("")
    if not violations:
        lines.append("_None._")
    else:
        for v in violations:
            lines.append(f"- {v}")

    lines += [
        "",
        "## Notes",
        "",
        "- This list is intentionally small. Strategic ≠ Big List.",
        "- T0/T1 must have a `relationship_path`. Without one, the account is demoted to T2.",
        "- Touchpoints log to `outreach/conversation_log.csv`.",
    ]

    out = priv / "market_attack" / "strategic_account_list.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
