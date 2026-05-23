"""Read and update `stage/stage_exit_checklist.csv` based on the evidence report.

The updater never *creates* artefacts — it only reflects state. A row goes
from `pending` to `done` only when a matching ScanResult passed; it goes from
`done` back to `pending` only via explicit human edit.
"""

from __future__ import annotations

import csv
import dataclasses
from pathlib import Path

from execution_engine.evidence_scanner import EvidenceReport


CHECKLIST_HEADER = ("stage", "check", "status", "evidence", "updated_at")


@dataclasses.dataclass
class ChecklistRow:
    stage: str
    check: str
    status: str  # 'pending' | 'done'
    evidence: str
    updated_at: str

    def to_dict(self) -> dict[str, str]:
        return dataclasses.asdict(self)


def load_checklist(path: Path) -> list[ChecklistRow]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [ChecklistRow(**row) for row in csv.DictReader(f)]


def _write_checklist(path: Path, rows: list[ChecklistRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(CHECKLIST_HEADER))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_dict())


def update_checklist(
    path: Path,
    report: EvidenceReport,
) -> list[ChecklistRow]:
    """Sync the checklist file against the evidence report.

    Adds missing rows for the report's stage. Updates status to `done` when
    the corresponding check passed. Returns the new row list.
    """
    rows = load_checklist(path)
    by_key = {(r.stage, r.check): r for r in rows}

    for result in report.results:
        key = (report.stage, result.name)
        existing = by_key.get(key)
        if existing is None:
            rows.append(
                ChecklistRow(
                    stage=report.stage,
                    check=result.name,
                    status="done" if result.passed else "pending",
                    evidence=result.detail,
                    updated_at=report.generated_at,
                )
            )
        else:
            if result.passed and existing.status != "done":
                existing.status = "done"
                existing.evidence = result.detail
                existing.updated_at = report.generated_at
            elif not result.passed and existing.status == "done":
                # do not silently regress; leave done rows alone
                pass

    _write_checklist(path, rows)
    return rows
