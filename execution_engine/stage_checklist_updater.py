from pathlib import Path
import csv

from execution_engine.evidence_scanner import scan_stage_1_evidence


HEADERS = ["criterion", "status", "evidence", "next_action"]


def update_stage_checklist(private_ops_root: str) -> Path:
    root = Path(private_ops_root)
    checklist_path = root / "stage/stage_exit_checklist.csv"

    if not checklist_path.exists():
        raise FileNotFoundError(f"Missing checklist: {checklist_path}")

    evidence = scan_stage_1_evidence(private_ops_root)

    rows = []
    with checklist_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            criterion = row.get("criterion", "")
            if criterion in evidence:
                row["status"] = "Done" if evidence[criterion] else "Pending"
            rows.append(row)

    with checklist_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    return checklist_path
