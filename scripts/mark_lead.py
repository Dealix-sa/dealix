import sys
import json
import os
import re
from datetime import datetime, timezone

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
REVENUE_LEDGER = os.path.join("docs", "ops", "REVENUE_LEDGER.md")

# Force UTF-8 encoding on standard streams
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def load_prospects():
    if not os.path.exists(PROSPECTS_FILE):
        return []
    with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_prospects(prospects):
    os.makedirs(os.path.dirname(PROSPECTS_FILE), exist_ok=True)
    with open(PROSPECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prospects, f, indent=2, ensure_ascii=False)

def parse_markdown_table(filepath):
    if not os.path.exists(filepath):
        return [], []
    
    rows = []
    headers = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        line_str = line.strip()
        if not line_str.startswith("|"):
            continue
        parts = [p.strip() for p in line_str.split("|")][1:-1]
        if not headers:
            headers = parts
        elif len(parts) > 0 and all(c == '-' or c == ':' for c in parts[0]):
            continue
        else:
            rows.append(parts)
    return headers, rows

def save_markdown_table(filepath, headers, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        separators = []
        for h in headers:
            if h == "Value":
                separators.append("---:")
            else:
                separators.append("---")
        f.write("| " + " | ".join(separators) + " |\n")
        for row in rows:
            while len(row) < len(headers):
                row.append("")
            f.write("| " + " | ".join(row[:len(headers)]) + " |\n")

def mark_lead(company_name: str, status: str, notes: str = ""):
    # Sanitize quotes
    company_name = company_name.replace('"', '').replace("'", "").strip()
    status = status.replace('"', '').replace("'", "").strip()
    notes = notes.replace('"', '').replace("'", "").strip()
    
    # 1. Update prospects.json
    prospects = load_prospects()
    found_json = False
    target_prospect = None
    
    for p in prospects:
        name_check = p.get("company", p.get("company_name", p.get("name", "")))
        if name_check.lower() == company_name.lower():
            p["status"] = status
            p["last_updated"] = datetime.now(timezone.utc).isoformat()
            if notes:
                p["notes"] = p.get("notes", "") + f" | [{datetime.now(timezone.utc).date()}] {notes}"
            found_json = True
            target_prospect = p
            break
            
    if not found_json:
        target_prospect = {
            "company": company_name,
            "company_name": company_name,
            "sector": "Technology",
            "problem": notes or "BANT Lead",
            "status": status,
            "outreach_sent_at": datetime.now(timezone.utc).isoformat(),
            "replied": False,
            "proposal_sent": False,
            "offer": "ai-trust",
            "last_touch": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "next_step": notes or "Follow up",
            "notes": notes,
            "message_variant": "AI_TRUST_V1"
        }
        prospects.append(target_prospect)
        save_prospects(prospects)
        print(f"Created new lead in prospects.json: {company_name}")
    else:
        save_prospects(prospects)
        
    # 2. Update REVENUE_LEDGER.md
    headers, rows = parse_markdown_table(REVENUE_LEDGER)
    if not headers:
        headers = ["ID", "Date", "Client", "Offer", "Stage", "Value", "Next Step", "Close Date", "Status"]
        
    found_md = False
    for row in rows:
        if len(row) > 2 and company_name.lower() in row[2].lower():
            row[4] = status
            if notes:
                row[6] = notes
            if status == "paid" or status == "complete" or status == "delivery_started":
                row[8] = "Won"
                row[7] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            elif status == "lost":
                row[8] = "Lost"
            found_md = True
            break
            
    if not found_md:
        lead_id = f"LD-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
        date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        offer_val = target_prospect.get("offer", "ai-trust")
        stage_val = status
        val_str = "5,000 SAR" if "trust" in offer_val or "accuracy" in offer_val else "TBD"
        next_step_val = notes if notes else "Follow up"
        close_date_val = datetime.now(timezone.utc).strftime('%Y-%m-%d') if status in ["paid", "complete", "delivery_started"] else "TBD"
        status_val = "Won" if status in ["paid", "complete", "delivery_started"] else "Active"
        
        new_row = [lead_id, date_str, f"{company_name} (Technology)", offer_val, stage_val, val_str, next_step_val, close_date_val, status_val]
        rows.append(new_row)
        print(f"Appended new lead in REVENUE_LEDGER.md: {company_name}")
        
    save_markdown_table(REVENUE_LEDGER, headers, rows)
    print(f"SUCCESS: Marked '{company_name}' as {status} inside prospects.json and REVENUE_LEDGER.md.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: py -3 scripts/mark_lead.py \"Company Name\" status \"optional notes\"")
        sys.exit(1)
        
    company = sys.argv[1]
    status = sys.argv[2]
    notes = sys.argv[3] if len(sys.argv) > 3 else ""
    
    mark_lead(company, status, notes)
