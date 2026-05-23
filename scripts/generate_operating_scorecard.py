#!/usr/bin/env python3
"""Generate the Dealix Operating Scorecard markdown.

Reads the private-ops runtime CSV files, computes simple scores per
domain, picks the top bottleneck, and writes
``<private_ops>/founder/operating_scorecard.md``.

This script never sends anything externally. It only reads private CSVs
and writes a markdown report into the private-ops tree.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import os
from pathlib import Path
from typing import Any


def _root(args) -> Path:
    return Path(args.private_ops or os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))


def _read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except Exception:
        return []


def _score(count: int, *, scale: int) -> int:
    return min(100, int(round((count / scale) * 100))) if scale > 0 else 0


def _fmt_pct(n: int) -> str:
    return f"{n}/100"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--private-ops", default=None)
    args = p.parse_args()
    root = _root(args)

    leads = _read(root / "intelligence/lead_intelligence_base.csv")
    convo = _read(root / "outreach/conversation_log.csv")
    proposals = _read(root / "sales/proposal_queue.csv")
    cash = _read(root / "finance/cash_collected.csv")
    incidents = _read(root / "trust/incidents.csv")
    flags = _read(root / "trust/trust_flags.csv")
    workers = _read(root / "runtime/worker_state.csv")
    candidates = _read(root / "product/productization_candidates.csv")
    security = _read(root / "security/security_status.csv")
    evals = _read(root / "evals/eval_status.csv")

    revenue = _score(len(cash), scale=10)
    trust = max(0, 100 - 10 * sum(1 for r in incidents if r.get("status") == "open"))
    runtime = _score(sum(1 for w in workers if w.get("status") == "ok"), scale=6)
    leverage = _score(len(proposals), scale=5)
    productization = _score(len(candidates), scale=3)
    ai_gov = 100 if (Path("registries/agent_registry.yaml").exists()
                     and Path("policies/dealix_control_policy.yaml").exists()
                     and Path("evals/gates/dealix_agent_eval_gate.yaml").exists()) else 30
    sec = _score(sum(1 for r in security if r.get("status") == "ok"), scale=5)
    data_platform = 100 if (root / "intelligence/lead_intelligence_base.csv").exists() else 0

    sections: list[tuple[str, int]] = [
        ("Revenue Score", revenue),
        ("Trust Score", trust),
        ("Runtime Score", runtime),
        ("Founder Leverage Score", leverage),
        ("Productization Score", productization),
        ("AI Governance Score", ai_gov),
        ("Security Score", sec),
        ("Data Platform Score", data_platform),
    ]

    bottleneck = min(sections, key=lambda kv: kv[1])
    next_action = _next_action(bottleneck[0])

    lines = [
        "# Dealix — Operating Scorecard",
        "",
        f"Generated: {_dt.datetime.now(_dt.UTC).isoformat(timespec='seconds')}",
        f"Private runtime: `{root}`",
        "",
        "| Domain | Score |",
        "| --- | --- |",
    ]
    for name, val in sections:
        lines.append(f"| {name} | {_fmt_pct(val)} |")
    lines += [
        "",
        f"**Top Bottleneck:** {bottleneck[0]} ({_fmt_pct(bottleneck[1])})",
        f"**Next Best Action:** {next_action}",
        "",
        "## Inputs",
        f"- leads={len(leads)} replies={sum(1 for r in convo if r.get('direction') == 'inbound')}"
        f" proposals={len(proposals)} cash_rows={len(cash)}",
        f"- incidents_open={sum(1 for r in incidents if r.get('status') == 'open')}"
        f" flags={len(flags)} workers={len(workers)}",
        f"- productization_candidates={len(candidates)} security_rows={len(security)}"
        f" eval_rows={len(evals)}",
        "",
        "> This scorecard is a private founder artefact. It is NOT a public proof.",
    ]

    out = root / "founder/operating_scorecard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {out}")
    return 0


def _next_action(domain: str) -> str:
    mapping = {
        "Revenue Score": "Move one warm conversation to proposal this week.",
        "Trust Score": "Resolve the oldest open incident before adding new work.",
        "Runtime Score": "Run `make bootstrap-runtime` + restart the API.",
        "Founder Leverage Score": "Convert one drafted action to an approval entry.",
        "Productization Score": "Capture the most-repeated delivery pattern as a candidate.",
        "AI Governance Score": "Run `make policy-check agent-registry eval-gate`.",
        "Security Score": "Set `DEALIX_INTERNAL_TOKEN` and verify the auth gate.",
        "Data Platform Score": "Run `make bootstrap-runtime PRIVATE_OPS=...`.",
    }
    return mapping.get(domain, "Pick the lowest-score domain and improve one row.")


if __name__ == "__main__":
    raise SystemExit(main())
