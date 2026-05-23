from pathlib import Path
import csv


def read_csv_rows(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_pipeline_stage(private_ops_root: str, stage: str) -> int:
    rows = read_csv_rows(Path(private_ops_root) / "pipeline/pipeline_tracker.csv")
    return sum(1 for r in rows if (r.get("stage") or "").strip().lower() == stage.lower())


def count_pipeline_rows(private_ops_root: str) -> int:
    rows = read_csv_rows(Path(private_ops_root) / "pipeline/pipeline_tracker.csv")
    return len(rows)


def count_revenue_actions(private_ops_root: str, action_type: str | None = None) -> int:
    rows = read_csv_rows(Path(private_ops_root) / "revenue/revenue_action_log.csv")
    if action_type is None:
        return len(rows)
    return sum(1 for r in rows if (r.get("type") or "").strip().lower() == action_type.lower())


def directory_has_files(private_ops_root: str, relative_path: str) -> bool:
    path = Path(private_ops_root) / relative_path
    return path.exists() and path.is_dir() and any(p.is_file() for p in path.iterdir())


def file_has_content(private_ops_root: str, relative_path: str) -> bool:
    path = Path(private_ops_root) / relative_path
    return path.exists() and path.is_file() and path.stat().st_size > 0


def scan_stage_1_evidence(private_ops_root: str) -> dict:
    leads = count_pipeline_rows(private_ops_root)
    contacted = count_pipeline_stage(private_ops_root, "Contacted")
    proposal_sent = count_pipeline_stage(private_ops_root, "Proposal Sent")
    paid = count_pipeline_stage(private_ops_root, "Paid")

    return {
        "25 leads": leads >= 25,
        "25 DMs sent": contacted >= 25 or count_revenue_actions(private_ops_root, "Outbound") >= 25,
        "3 samples prepared": directory_has_files(private_ops_root, "delivery/samples"),
        "1 proposal sent": proposal_sent >= 1 or count_revenue_actions(private_ops_root, "Proposal") >= 1,
        "payment or PO pursued": paid >= 1 or count_revenue_actions(private_ops_root, "Payment Follow-Up") >= 1,
        "weekly learning completed": file_has_content(private_ops_root, "learning/weekly_intelligence_review.md"),
        "one system update committed": False,
    }
