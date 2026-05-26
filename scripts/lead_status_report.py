import os
import json
from datetime import datetime, timezone

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
REPORTS_DIR = os.path.join("reports")

def generate_report():
    print("==========================================")
    print(" GENERATING LEAD STATUS REPORT ")
    print("==========================================")
    
    if not os.path.exists(PROSPECTS_FILE):
        print(f"Error: {PROSPECTS_FILE} not found.")
        return
        
    with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
        prospects = json.load(f)
        
    status_counts = {}
    for p in prospects:
        stat = p.get("status", "unknown")
        status_counts[stat] = status_counts.get(stat, 0) + 1
        
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_text = f"""# 📈 Dealix B2B Lead Status Report — {today}
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC

## Pipeline Snapshot
Total active prospects in database: {len(prospects)}

### Leads by Stage
"""
    for stat, count in status_counts.items():
        report_text += f"- **{stat}**: {count} leads\n"
        
    report_text += "\n## Lead Registry Details\n"
    for p in prospects:
        comp = p.get("company", p.get("company_name", p.get("name", "Unknown")))
        sect = p.get("sector", "Technology")
        stat = p.get("status", "unknown")
        touch = p.get("last_touch", "TBD")
        report_text += f"* **{comp}** ({sect}) — Stage: `{stat}` | Last touch: {touch}\n"
        
    os.makedirs(REPORTS_DIR, exist_ok=True)
    file_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    filepath = os.path.join(REPORTS_DIR, f"lead-status-{file_date}.md")
    
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(report_text)
        
    print(f"[PASS] Lead status report generated at: {filepath}")

if __name__ == "__main__":
    generate_report()
