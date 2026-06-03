#!/usr/bin/env python3
"""Run the GTM draft quality gate over a JSONL drafts file.

    python3 scripts/gtm_quality_gate.py \
        --input data/gtm/outreach/drafts.sample.jsonl \
        --suppression data/gtm/suppression/suppression.sample.jsonl \
        --report reports/gtm/DRAFT_QUALITY_REPORT.md

Exit code is 0 by default (audit mode). Pass ``--require-all-pass`` to fail
(exit 1) if any draft is blocked — use that on a *production* drafts file
before queueing for approval. The committed sample intentionally contains
failing drafts, so CI runs this in audit mode and relies on pytest for the
correctness contract.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auto_client_acquisition.gtm_os.draft_quality_gate import (
    GateResult,
    summarize_gate_results,
    validate_outreach_draft,
)


def _load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _load_suppression(path: Path | None) -> set[str]:
    if path is None:
        return set()
    return {r.get("recipient_ref", "") for r in _load_jsonl(path) if r.get("recipient_ref")}


def _render_report(results: list[GateResult], summary: dict) -> str:
    lines = [
        "# GTM Draft Quality Report — تقرير جودة المسودات",
        "",
        f"_Generated: {datetime.now(UTC).isoformat()}_",
        "",
        f"- Total drafts / إجمالي المسودات: **{summary['total']}**",
        f"- Approval-ready / جاهزة للموافقة: **{summary['passed']}**",
        f"- Blocked / محجوبة: **{summary['failed']}**",
        "",
        "## Per-draft results — النتائج",
        "",
        "| draft_id | verdict | governance | issues |",
        "| --- | --- | --- | --- |",
    ]
    for r in results:
        codes = ", ".join(r.codes) if r.codes else "—"
        lines.append(f"| `{r.draft_id}` | {r.verdict} | {r.governance_decision} | {codes} |")
    if summary["top_failure_reasons"]:
        lines += ["", "## Top failure reasons — أكثر أسباب الحجب", ""]
        for code, count in summary["top_failure_reasons"].items():
            lines.append(f"- `{code}`: {count}")
    lines += [
        "",
        "> Drafts that pass are marked `approval_required` — ready for founder review, never auto-sent.",
        "> المسودات الناجحة تُعلَّم `approval_required` — جاهزة لمراجعة المؤسس، لا تُرسَل تلقائيًا.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run the GTM draft quality gate.")
    ap.add_argument("--input", default="data/gtm/outreach/drafts.sample.jsonl")
    ap.add_argument("--suppression", default="data/gtm/suppression/suppression.sample.jsonl")
    ap.add_argument("--report", default=None, help="Optional path to write a markdown report.")
    ap.add_argument("--require-all-pass", action="store_true",
                    help="Exit non-zero if any draft is blocked (use on production drafts).")
    args = ap.parse_args(argv)

    repo = Path(__file__).resolve().parents[1]
    drafts = _load_jsonl(repo / args.input)
    suppression = _load_suppression(repo / args.suppression if args.suppression else None)

    results = [validate_outreach_draft(d, suppression_refs=suppression) for d in drafts]
    summary = summarize_gate_results(results)

    report = _render_report(results, summary)
    if args.report:
        out = repo / args.report
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report + "\n", encoding="utf-8")
        print(f"report -> {args.report}")
    print(
        f"GTM quality gate: total={summary['total']} "
        f"approval_ready={summary['passed']} blocked={summary['failed']}"
    )
    for r in results:
        mark = "PASS" if r.passed else "BLOCK"
        print(f"  [{mark}] {r.draft_id}: {', '.join(r.codes) or 'ok'}")

    if args.require_all_pass and summary["failed"]:
        print("FAIL: --require-all-pass set and some drafts are blocked.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
