#!/usr/bin/env python3
"""
Dealix GCC Draft Factory — Daily Pipeline Orchestrator
Runs the full 24-hour production cycle: scan -> classify -> research -> brief -> draft -> gate -> report
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MEMORY_DIR = BASE_DIR / "memory"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def ensure_dirs() -> None:
    """Create all required output and memory directories if they do not exist."""
    for d in [
        MEMORY_DIR,
        OUTPUTS_DIR / "daily",
        OUTPUTS_DIR / "review_queue",
        OUTPUTS_DIR / "approved",
        OUTPUTS_DIR / "rejected",
        REPORTS_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)


def load_jsonl(path: Path) -> list[dict]:
    """Load all records from a JSONL file."""
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, record: dict) -> None:
    """Append a single record to a JSONL file."""
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_pipeline() -> dict:
    """Execute the full daily pipeline and return a statistics dictionary."""
    ensure_dirs()
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    # Add file log handler after dirs are created
    file_handler = logging.FileHandler(OUTPUTS_DIR / "daily" / f"pipeline_{datetime.now(timezone.utc).strftime('%Y%m%d')}.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(file_handler)

    log.info("=== Dealix GCC Draft Factory — Pipeline Start [%s] ===", date_str)

    stats: dict = {
        "run_id": run_id,
        "date": date_str,
        "raw_leads": 0,
        "qualified_companies": 0,
        "company_briefs": 0,
        "arabic_drafts": 0,
        "english_drafts": 0,
        "followup_drafts": 0,
        "rejected_drafts": 0,
        "founder_ready": 0,
    }

    # Phase 1: Load qualified companies from memory
    companies = load_jsonl(MEMORY_DIR / "companies.jsonl")
    stats["qualified_companies"] = len(companies)
    log.info("Phase 1: Loaded %d qualified companies", len(companies))

    # Phase 2: Load drafts waiting in queue
    draft_queue = load_jsonl(MEMORY_DIR / "draft_queue.jsonl")
    pending = [d for d in draft_queue if d.get("status") == "pending_quality_gate"]
    log.info("Phase 2: %d drafts pending quality gate", len(pending))

    # Phase 3: Run quality + compliance gate on pending drafts
    sys.path.insert(0, str(Path(__file__).parent))
    from quality_gate import run_quality_gate
    from compliance_checker import run_compliance_check

    approved: list[dict] = []
    rejected: list[dict] = []
    for draft in pending:
        qr = run_quality_gate(draft)
        cr = run_compliance_check(draft)
        draft["quality_score"] = qr["score"]
        draft["compliance_score"] = cr["score"]
        draft["quality_flags"] = qr.get("flags", [])
        draft["compliance_flags"] = cr.get("flags", [])

        if qr["score"] >= 70 and cr["score"] >= 70:
            draft["status"] = "founder_review"
            approved.append(draft)
        else:
            draft["status"] = "rejected"
            draft["reject_reason"] = qr.get("reason") or cr.get("reason")
            rejected.append(draft)

    stats["founder_ready"] = len(approved)
    stats["rejected_drafts"] = len(rejected)
    log.info("Phase 3: %d approved for review, %d rejected", len(approved), len(rejected))

    # Write approved to review queue
    review_path = OUTPUTS_DIR / "review_queue" / f"queue_{date_str}.jsonl"
    for draft in sorted(approved, key=lambda d: d.get("quality_score", 0), reverse=True):
        append_jsonl(review_path, draft)

    # Write rejected for analysis
    rejected_path = OUTPUTS_DIR / "rejected" / f"rejected_{date_str}.jsonl"
    for draft in rejected:
        append_jsonl(rejected_path, draft)

    # Phase 4: Generate founder report
    from founder_review_report import generate_report
    report = generate_report(date_str, stats, approved, rejected)
    report_path = REPORTS_DIR / f"founder_report_{date_str}.md"
    report_path.write_text(report, encoding="utf-8")
    log.info("Phase 4: Founder report written to %s", report_path)

    # Log run stats
    append_jsonl(MEMORY_DIR / "learning_log.jsonl", {
        "type": "pipeline_run",
        "run_id": run_id,
        "date": date_str,
        "stats": stats,
    })

    log.info("=== Pipeline Complete: %d founder-ready drafts ===", stats["founder_ready"])
    return stats


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2, ensure_ascii=False))
