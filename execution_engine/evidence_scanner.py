"""Scan a private-ops directory for evidence that the current stage's exit
criteria are met.

The scanner is read-only — it does not modify the private repo. Output is a
deterministic `EvidenceReport` that callers can render to markdown.
"""

from __future__ import annotations

import csv
import dataclasses
import datetime as dt
from pathlib import Path
from typing import Iterable


STAGES = (
    "setup",
    "pipeline",
    "outreach",
    "samples",
    "proposal",
    "payment_attempt",
    "delivery",
    "learning",
)


@dataclasses.dataclass(frozen=True)
class ScanResult:
    """Outcome of one evidence check."""

    name: str
    passed: bool
    detail: str


@dataclasses.dataclass(frozen=True)
class EvidenceReport:
    """All evidence checks for the current stage."""

    stage: str
    generated_at: str
    results: tuple[ScanResult, ...]

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    def to_markdown(self) -> str:
        lines = [
            f"# Evidence Report — stage `{self.stage}`",
            "",
            f"_Generated: {self.generated_at}_",
            "",
            "| Check | Status | Detail |",
            "|---|---|---|",
        ]
        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            lines.append(f"| {r.name} | {status} | {r.detail} |")
        lines.append("")
        lines.append(f"**Overall:** {'PASS' if self.passed else 'FAIL'}")
        lines.append("")
        return "\n".join(lines)


def _read_current_stage(private_ops: Path) -> str:
    path = private_ops / "stage" / "current_stage.md"
    if not path.exists():
        return "setup"
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("stage:"):
            value = line.split(":", 1)[1].strip().lower()
            if value in STAGES:
                return value
    return "setup"


def _csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _check_pipeline(private_ops: Path) -> ScanResult:
    rows = _csv_rows(private_ops / "pipeline" / "pipeline_tracker.csv")
    if len(rows) < 25:
        return ScanResult(
            "pipeline.>=25_leads",
            False,
            f"found {len(rows)}, need 25",
        )
    missing_next = [r for r in rows if not r.get("next_action") and r.get("stage") != "lost"]
    if missing_next:
        return ScanResult(
            "pipeline.next_action_set",
            False,
            f"{len(missing_next)} rows missing next_action",
        )
    return ScanResult("pipeline.>=25_leads", True, f"{len(rows)} leads")


def _count_actions(rows: Iterable[dict[str, str]], action_type: str) -> int:
    return sum(1 for r in rows if r.get("action_type") == action_type)


def _check_outreach(private_ops: Path) -> ScanResult:
    rows = _csv_rows(private_ops / "revenue" / "revenue_action_log.csv")
    sent = _count_actions(rows, "dm_sent")
    if sent < 25:
        return ScanResult(
            "outreach.>=25_dms",
            False,
            f"found {sent}, need 25",
        )
    return ScanResult("outreach.>=25_dms", True, f"{sent} DMs logged")


def _check_samples(private_ops: Path) -> ScanResult:
    sample_dir = private_ops / "offers" / "revenue_sprint"
    if not sample_dir.exists():
        return ScanResult("samples.>=3_packs", False, "offers/revenue_sprint missing")
    samples = [
        p
        for p in list(sample_dir.glob("sample_pack_*.md"))
        + list(sample_dir.glob("sample_pack_*.pdf"))
        if p.stem != "sample_pack_template"
    ]
    if len(samples) < 3:
        return ScanResult(
            "samples.>=3_packs",
            False,
            f"found {len(samples)}, need 3",
        )
    return ScanResult("samples.>=3_packs", True, f"{len(samples)} sample packs")


def _check_proposal(private_ops: Path) -> ScanResult:
    rows = _csv_rows(private_ops / "revenue" / "revenue_action_log.csv")
    proposals = [r for r in rows if r.get("action_type") == "proposal_sent"]
    if not proposals:
        return ScanResult("proposal.>=1_sent", False, "no proposal_sent in revenue log")
    missing_followup = [p for p in proposals if not p.get("next_followup")]
    if missing_followup:
        return ScanResult(
            "proposal.followup_set",
            False,
            f"{len(missing_followup)} proposals missing next_followup",
        )
    return ScanResult("proposal.>=1_sent", True, f"{len(proposals)} proposals logged")


def _check_payment_attempt(private_ops: Path) -> ScanResult:
    rows = _csv_rows(private_ops / "revenue" / "revenue_action_log.csv")
    types = {"payment_link_sent", "po_received", "written_approval"}
    attempts = [r for r in rows if r.get("action_type") in types]
    if not attempts:
        return ScanResult(
            "payment.>=1_attempt",
            False,
            "no payment_link_sent / po_received / written_approval",
        )
    return ScanResult("payment.>=1_attempt", True, f"{len(attempts)} attempts logged")


def _check_delivery(private_ops: Path) -> ScanResult:
    delivery_dir = private_ops / "delivery"
    if not delivery_dir.exists():
        return ScanResult("delivery.>=1_report", False, "delivery/ missing")
    reports = list(delivery_dir.glob("**/delivery_report*.md"))
    if not reports:
        return ScanResult("delivery.>=1_report", False, "no delivery_report*.md found")
    return ScanResult("delivery.>=1_report", True, f"{len(reports)} report(s)")


def _check_learning(private_ops: Path) -> ScanResult:
    reviews_dir = private_ops / "weekly_reviews"
    if not reviews_dir.exists():
        return ScanResult("learning.weekly_review", False, "weekly_reviews/ missing")
    today = dt.date.today()
    iso_year, iso_week, _ = today.isocalendar()
    target = reviews_dir / f"{iso_year}-W{iso_week:02d}.md"
    if not target.exists():
        return ScanResult(
            "learning.weekly_review",
            False,
            f"missing {target.name}",
        )
    if target.stat().st_size < 100:
        return ScanResult(
            "learning.weekly_review",
            False,
            f"{target.name} too short",
        )
    return ScanResult("learning.weekly_review", True, target.name)


_CHECKS_BY_STAGE = {
    "setup": (),  # setup is verified by audit_dealix_implementation.py itself
    "pipeline": (_check_pipeline,),
    "outreach": (_check_pipeline, _check_outreach),
    "samples": (_check_pipeline, _check_outreach, _check_samples),
    "proposal": (_check_pipeline, _check_outreach, _check_samples, _check_proposal),
    "payment_attempt": (
        _check_pipeline,
        _check_outreach,
        _check_samples,
        _check_proposal,
        _check_payment_attempt,
    ),
    "delivery": (
        _check_pipeline,
        _check_outreach,
        _check_samples,
        _check_proposal,
        _check_payment_attempt,
        _check_delivery,
    ),
    "learning": (
        _check_pipeline,
        _check_outreach,
        _check_samples,
        _check_proposal,
        _check_payment_attempt,
        _check_delivery,
        _check_learning,
    ),
}


def scan_evidence(private_ops: Path, stage: str | None = None) -> EvidenceReport:
    """Run the evidence checks for the given stage (or the current stage)."""
    if stage is None:
        stage = _read_current_stage(private_ops)
    if stage not in _CHECKS_BY_STAGE:
        raise ValueError(f"unknown stage: {stage}")
    results = tuple(check(private_ops) for check in _CHECKS_BY_STAGE[stage])
    return EvidenceReport(
        stage=stage,
        generated_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        results=results,
    )
