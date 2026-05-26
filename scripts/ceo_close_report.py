import os
import json
from datetime import datetime, timezone

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
REPORTS_DIR = os.path.join("reports")

def generate_report():
    print("==========================================")
    print(" GENERATING CEO CLOSE WON REPORT ")
    print("==========================================")
    
    if not os.path.exists(PROSPECTS_FILE):
        print(f"Error: {PROSPECTS_FILE} not found.")
        return
        
    with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
        prospects = json.load(f)
        
    closed_won = [p for p in prospects if p.get("status", "").lower() in ["paid", "delivery_started", "proof_pack_created", "complete"]]
    total_rev = len(closed_won) * 5000 # Each pilot is 5000 SAR
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_text = f"""# 🏆 Dealix CEO Close Won Report — {today}
Owner: Sami Assiri (Founder)

## Key Revenue Metrics
* **Closed Won Pilots:** {len(closed_won)}
* **Estimated Pipeline Revenue:** {total_rev} SAR
* **Conversion Rate (Outbound to Won):** {round(len(closed_won)/len(prospects)*100, 2) if len(prospects) > 0 else 0}%

## Closed Won Customers
"""
    for p in closed_won:
        comp = p.get("company", p.get("company_name", p.get("name", "Unknown")))
        sect = p.get("sector", "Technology")
        offer = p.get("offer", "ai-trust")
        report_text += f"- **{comp}** ({sect}) — Offer: `{offer}` | Diagnostic Value: 5,000 SAR (Won)\n"
        
    os.makedirs(REPORTS_DIR, exist_ok=True)
    file_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    filepath = os.path.join(REPORTS_DIR, f"ceo-close-report-{file_date}.md")
    
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(report_text)
        
    print(f"[PASS] CEO close report generated at: {filepath}")

if __name__ == "__main__":
    generate_report()
