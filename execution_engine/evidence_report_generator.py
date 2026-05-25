from __future__ import annotations

"""Render evidence checks as a human-readable Markdown report."""

from datetime import datetime
from pathlib import Path

from .evidence_checker import EvidenceCheck

REPORT_RELPATH = "stage/evidence_report.md"


def generate_evidence_report(
    private_ops_path: Path, checks: list[EvidenceCheck]
) -> Path:
    """Write `stage/evidence_report.md` summarising the current state."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / REPORT_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)

    total = len(checks)
    passing = sum(1 for c in checks if c.status == "pass")
    failing = total - passing
    blockers = [c for c in checks if c.status != "pass"]

    lines: list[str] = []
    lines.append("# Stage Evidence Report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total criteria: {total}")
    lines.append(f"- Passing: {passing}")
    lines.append(f"- Blockers: {failing}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    lines.append("| Criterion | Status | Evidence | Next Action |")
    lines.append("|---|---|---|---|")
    for chk in checks:
        next_action = chk.next_action or "-"
        evidence = chk.evidence_path or "-"
        lines.append(
            f"| {chk.criterion} | {chk.status} | {evidence} | {next_action} |"
        )
    lines.append("")

    if blockers:
        lines.append("## Blockers")
        lines.append("")
        for chk in blockers:
            lines.append(f"- {chk.criterion}: {chk.next_action or 'see evidence'}")
        lines.append("")

    target.write_text("\n".join(lines), encoding="utf-8")
    return target
