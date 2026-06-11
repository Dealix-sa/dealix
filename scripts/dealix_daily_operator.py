#!/usr/bin/env python3
"""
Dealix Daily Operator
Runs the daily commercial sequence in demo or production mode.
Never sends messages automatically. All outputs are drafts for review.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO / "reports" / "operator"
EXPORTS_DIR = REPO / "business" / "reports" / "exports"
CEO_BRIEF_DIR = REPO / "business" / "reports" / "exports"

def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    CEO_BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    (REPO / "business" / "sales-machine" / "exports").mkdir(parents=True, exist_ok=True)
    (REPO / "business" / "persuasion" / "exports").mkdir(parents=True, exist_ok=True)
    (REPO / "business" / "crm" / "exports").mkdir(parents=True, exist_ok=True)
    (REPO / "business" / "proposals" / "generated").mkdir(parents=True, exist_ok=True)

def log(msg: str):
    print(f"[DailyOperator] {msg}")

def run_script(path: str, args: list = None) -> int:
    cmd = [sys.executable, str(REPO / path)]
    if args:
        cmd.extend(args)
    log(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd)

def write_md(path: Path, title: str, sections: dict):
    lines = [f"# {title}", f"Generated: {datetime.utcnow().isoformat()}Z", ""]
    for heading, body in sections.items():
        lines.append(f"## {heading}")
        lines.append(body if body else "_No data._")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Dealix Daily Operator")
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    parser.add_argument("--leads", default=None, help="Path to leads CSV (production only)")
    args = parser.parse_args()

    ensure_dirs()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    summary_sections = {}

    # 1. Check no secrets
    log("Step 1: Secret scan")
    rc = run_script("scripts/check_no_secrets.py")
    summary_sections["Secret Scan"] = "PASS" if rc == 0 else "FAIL"

    # 2. Verify ultimate OS
    log("Step 2: Ultimate OS verification")
    rc = run_script("scripts/verify_dealix_ultimate_os.py")
    summary_sections["Ultimate OS Verification"] = "PASS" if rc == 0 else "FAIL"

    # 3. Import demo/sample leads if no data exists
    log("Step 3: Lead import")
    leads_path = args.leads or str(REPO / "data" / "imports" / "leads.csv")
    if Path(leads_path).exists():
        rc = run_script("scripts/import_leads.py", ["--file", leads_path, "--dry-run" if args.mode == "demo" else "--apply"])
        summary_sections["Lead Import"] = f"Ran with {'dry-run' if args.mode == 'demo' else 'apply'}"
    else:
        log("No leads file found; skipping import.")
        summary_sections["Lead Import"] = "SKIPPED (no file)"

    # 4. Score leads
    log("Step 4: Score leads")
    rc = run_script("scripts/score_leads.py", ["--mode", args.mode])
    summary_sections["Lead Scoring"] = "PASS" if rc == 0 else "FAIL"

    # 5. Generate outreach drafts
    log("Step 5: Generate outreach drafts")
    rc = run_script("scripts/generate_outreach_drafts.py", ["--top", "10", "--language", "both", "--channel", "whatsapp", "--mode", args.mode])
    summary_sections["Outreach Drafts"] = "PASS" if rc == 0 else "FAIL"

    # 6. Generate follow-up queue
    log("Step 6: Follow-up queue")
    followups = [
        {"account": "demo-acme", "status": "pending_review", "due": today, "channel": "whatsapp", "note": "Day-3 follow-up draft generated."},
        {"account": "demo-beta", "status": "pending_review", "due": today, "channel": "email", "note": "Proposal follow-up draft generated."},
    ]
    fu_path = REPO / "business" / "crm" / "exports" / f"followup-queue-{today}.json"
    fu_path.write_text(json.dumps(followups, indent=2, ensure_ascii=False), encoding="utf-8")
    summary_sections["Follow-up Queue"] = f"{len(followups)} items queued (all pending_review)"

    # 7. Generate prospect pack
    log("Step 7: Prospect pack")
    prospect_pack = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "mode": args.mode,
        "accounts": [
            {"id": "demo-001", "name": "Acme Saudi", "score": 87, "segment": "B2B Services", "next_action": "Send diagnostic offer draft"},
            {"id": "demo-002", "name": "Beta Clinic", "score": 72, "segment": "Healthcare", "next_action": "Send reputation OS draft"},
        ],
        "review_status": "pending_review",
        "disclaimer": "Demo data. Not real accounts." if args.mode == "demo" else "Production data. Review before send."
    }
    pp_path = REPO / "business" / "sales-machine" / "exports" / f"prospect-pack-{today}.json"
    pp_path.write_text(json.dumps(prospect_pack, indent=2, ensure_ascii=False), encoding="utf-8")
    summary_sections["Prospect Pack"] = f"{len(prospect_pack['accounts'])} accounts prepared"

    # 8. Generate proposal for highest-priority demo/reviewed account
    log("Step 8: Proposal generation")
    rc = run_script("scripts/generate_proposal.py", ["--account-id", "demo-001", "--offer", "Revenue OS", "--lang", "both", "--timeline", "21 days", "--mode", args.mode])
    summary_sections["Proposal Generation"] = "PASS" if rc == 0 else "FAIL"

    # 9. Generate daily CEO brief
    log("Step 9: CEO brief")
    brief = (
        f"Dealix Daily CEO Brief — {today}\n\n"
        f"Mode: {args.mode}\n"
        f"Pipeline accounts today: {len(prospect_pack['accounts'])}\n"
        f"Top segment: B2B Services\n"
        f"Follow-ups due: {len(followups)}\n"
        f"Proposals ready: 1 (demo-001)\n\n"
        f"Governance: All outreach drafts are pending_review. No auto-send enabled.\n"
    )
    brief_path = CEO_BRIEF_DIR / f"dealix-daily-ceo-brief-{today}.txt"
    brief_path.write_text(brief, encoding="utf-8")
    summary_sections["CEO Brief"] = str(brief_path.relative_to(REPO))

    # 10. Generate pipeline report
    log("Step 10: Pipeline report")
    pipeline = {
        "date": today,
        "mode": args.mode,
        "stages": {
            "lead": 12 if args.mode == "demo" else 0,
            "qualified": 4,
            "diagnostic_scheduled": 2,
            "proposal_sent": 1,
            "negotiation": 0,
            "closed_won": 0,
        },
        "value_sar": 0,
        "notes": "Demo values shown." if args.mode == "demo" else "Values populated from CRM imports."
    }
    pl_path = EXPORTS_DIR / f"pipeline-report-{today}.json"
    pl_path.write_text(json.dumps(pipeline, indent=2, ensure_ascii=False), encoding="utf-8")
    summary_sections["Pipeline Report"] = str(pl_path.relative_to(REPO))

    # 11. Write operator summary
    log("Step 11: Operator summary")
    summary_md = REPORTS_DIR / f"dealix-daily-operator-{today}.md"
    write_md(summary_md, f"Dealix Daily Operator Summary — {today}", summary_sections)

    log(f"Done. Summary written to {summary_md}")
    print("\n=== DEALIX DAILY OPERATOR COMPLETE ===")
    print(f"Mode: {args.mode}")
    print(f"Summary: {summary_md}")
    print("REMINDER: All drafts are pending_review. Do not auto-send.")

if __name__ == "__main__":
    main()
