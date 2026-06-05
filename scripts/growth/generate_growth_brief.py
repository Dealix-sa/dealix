#!/usr/bin/env python3
"""Daily Growth Brief — aggregates the Dealix Self-Growth OS state.

Offline, deterministic. Reads the data/growth/* assets and prints a single
founder-facing brief: what assets exist, what needs approval, and the next
founder actions. No external calls, no sends.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DG = ROOT / "data" / "growth"
OUT = ROOT / "reports" / "growth"


def _jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    experiments = _jsonl(DG / "experiments.jsonl")
    ideas = _jsonl(DG / "content_ideas.jsonl")
    free_tools = []
    if (DG / "free_tools.json").exists():
        free_tools = json.loads((DG / "free_tools.json").read_text(encoding="utf-8")).get(
            "tools", []
        )
    sequences = []
    if (DG / "nurture_sequences.json").exists():
        sequences = json.loads((DG / "nurture_sequences.json").read_text(encoding="utf-8")).get(
            "sequences", []
        )
    partners = []
    if (DG / "partner_targets.csv").exists():
        partners = list(
            csv.DictReader((DG / "partner_targets.csv").read_text(encoding="utf-8").splitlines())
        )

    pending_content = [i for i in ideas if i.get("status") == "needs-approval"]

    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Daily Growth Brief — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        "",
        "## Asset inventory",
        "",
        f"- Free tools (lead magnets): **{len(free_tools)}**",
        f"- Content ideas in pool: **{len(ideas)}** ({len(pending_content)} need founder approval)",
        f"- Growth experiments: **{len(experiments)}**",
        f"- Nurture sequences: **{len(sequences)}**",
        f"- Partner categories: **{len(partners)}**",
        "",
        "## Growth loop check (each should route to: lead → Sprint → Proof → MRR → partner)",
        "",
        "1. Free tools attract.",
        "2. Sector pages explain.",
        "3. Content builds trust.",
        "4. Diagnostics qualify.",
        "5. Command Sprint sells.",
        "6. Delivery proves.",
        "7. Proof Pack markets.",
        "8. Managed OS repeats revenue.",
        "9. Partners expand distribution.",
        "10. Academy lowers resistance.",
        "",
        "## Needs founder approval",
        "",
    ]
    if pending_content:
        for i in pending_content:
            lines.append(f"- [ ] Content `{i.get('id')}`: {i.get('topic_ar')}")
    else:
        lines.append("- (none)")
    lines += [
        "",
        "## Next founder actions",
        "",
        "1. Approve any pending case-safe content above.",
        "2. Pick 1 sector page to ship full copy this week.",
        "3. Launch / refine 1 free tool.",
        "4. Run up to 10 experiments this week (see EXPERIMENT_BACKLOG.md).",
        "5. Send 5 warm partner outreach drafts (founder-approved).",
        "",
        "> Guardrails: no spam, no cold WhatsApp, no fake proof, no fake scarcity,",
        "> no guaranteed revenue, one CTA per asset, founder approval before any external send.",
        "",
    ]
    (OUT / "GROWTH_BRIEF.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        "DEALIX_GROWTH_BRIEF=PASS "
        f"(tools={len(free_tools)} ideas={len(ideas)} experiments={len(experiments)} "
        f"sequences={len(sequences)} partners={len(partners)} pending_approval={len(pending_content)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
