import argparse
import csv
from pathlib import Path
from datetime import date


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    pipeline = read_csv(root / "pipeline/pipeline_tracker.csv")
    send_queue = read_csv(root / "outreach/outreach_send_queue.csv")
    followups = read_csv(root / "outreach/followup_queue.csv")
    replies = read_csv(root / "outreach/reply_log.csv")
    samples = read_csv(root / "delivery/sample_quality_log.csv")
    proposals = read_csv(root / "sales/proposal_tracker.csv")
    ready_to_send = [r for r in send_queue if r.get("status") == "Ready"]
    pending_approval = [r for r in send_queue if r.get("approval_status") != "Approved"]
    planned_followups = [r for r in followups if r.get("status") == "Planned"]
    positive_replies = [
        r for r in replies
        if (r.get("reply_type") or "").lower() in {"positive", "interested", "yes"}
    ]
    content = f"""# Daily Acquisition Report
## Date
{date.today().isoformat()}
## Funnel
- Pipeline leads: {len(pipeline)}
- Ready to send: {len(ready_to_send)}
- Pending approval: {len(pending_approval)}
- Planned followups: {len(planned_followups)}
- Replies logged: {len(replies)}
- Positive replies: {len(positive_replies)}
- Sample tasks: {len(samples)}
- Proposals: {len(proposals)}
## Top Action
"""
    if len(pipeline) < 25:
        content += "Add more qualified leads.\n"
    elif len(ready_to_send) > 0:
        content += "Approve/send outbound batch.\n"
    elif len(planned_followups) > 0:
        content += "Send planned followups.\n"
    elif len(positive_replies) > 0 and len(samples) < 3:
        content += "Prepare sample packs for positive replies.\n"
    elif len(proposals) < 1:
        content += "Convert best positive reply/sample into proposal.\n"
    else:
        content += "Pursue payment / PO / written approval.\n"
    content += "\n## CEO Rule\nDo the top action before adding new systems.\n"
    out = root / "founder/daily_acquisition_report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print("PASS: daily acquisition report generated.")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
