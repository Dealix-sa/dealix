"""Roll up decisions, outcomes, and learnings into a long-term memory report.

Reads:
    founder/decision_log.csv (date, decision, owner, outcome)
    graph/learnings.csv      (date, topic, learning, source, tag)
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _private_ops_runtime import (  # noqa: E402
    ledger_path,
    parse_args,
    read_csv,
    today_iso,
    write_or_print,
)


def main() -> int:
    args = parse_args("generate_company_memory_report")
    po = args.private_ops

    _, decisions = read_csv(ledger_path(po, "founder", "decision_log.csv"))
    _, learnings = read_csv(ledger_path(po, "graph", "learnings.csv"))

    if args.strict and not (decisions or learnings):
        print("[strict] both ledgers empty", file=sys.stderr)
        return 1

    by_outcome = Counter((d.get("outcome") or "unknown").lower() for d in decisions)
    by_tag = Counter((l.get("tag") or "untagged").lower() for l in learnings)

    lines = [f"# Company Memory — {today_iso()}\n",
             "Source: private_ops decision_log + learnings (read-only).\n",
             f"## Decisions ({len(decisions)} total)\n"]
    if by_outcome:
        for k, v in by_outcome.most_common():
            lines.append(f"- {k}: {v}")
        lines.append("")
        lines.append("### Last 10 decisions\n")
        for d in list(reversed(decisions))[:10]:
            lines.append(
                f"- {d.get('date', '?')} — **{d.get('decision', '?')}** "
                f"(owner: {d.get('owner', '?')}, outcome: {d.get('outcome', 'pending')})"
            )
    else:
        lines.append("- (no decisions logged)")

    lines.append(f"\n## Learnings ({len(learnings)} total)\n")
    if by_tag:
        for k, v in by_tag.most_common(10):
            lines.append(f"- #{k}: {v}")
        lines.append("")
        lines.append("### Last 15 learnings\n")
        for l in list(reversed(learnings))[:15]:
            lines.append(
                f"- {l.get('date', '?')} — *{l.get('topic', '?')}* — "
                f"{l.get('learning', '')} (src: {l.get('source', '?')})"
            )
    else:
        lines.append("- (no learnings recorded)")

    write_or_print("\n".join(lines), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
