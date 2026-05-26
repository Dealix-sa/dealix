import os
import json
from datetime import datetime, timezone

REPORTS_DIR = os.path.join("reports", "hermes")
OPPORTUNITIES_FILE = os.path.join("data", "ledgers", "hermes_opportunities.json")

def scan_radar():
    print("==========================================")
    print(" SCANNING HERMES OPPORTUNITY RADAR ")
    print("==========================================")
    
    # Pre-populate some options
    opportunities = [
        {
            "id": "OP-01",
            "sector": "Logistics",
            "pain": "TGA National Address Compliance Jan 2026",
            "fit_offer": "Delivery Accuracy Sprint",
            "status": "Targeting",
            "value_potential": "High"
        },
        {
            "id": "OP-02",
            "sector": "Marketing Agency",
            "pain": "PII data leakage via public LLMs",
            "fit_offer": "AI Trust Diagnostic",
            "status": "Contacted",
            "value_potential": "Medium"
        }
    ]
    
    os.makedirs(os.path.dirname(OPPORTUNITIES_FILE), exist_ok=True)
    with open(OPPORTUNITIES_FILE, "w", encoding="utf-8") as f:
        json.dump(opportunities, f, indent=2, ensure_ascii=False)
        
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"opportunity-radar-{datetime.now(timezone.utc).strftime('%Y%m%d')}.md")
    
    content = f"""# 📡 Hermes Opportunity Radar — {today}

## High Value Target Sectors

### 1. Logistics & Last-Mile Delivery
* **Wedge:** Mandatory National Address validation (TGA Jan 2026).
* **Fit:** *Delivery Accuracy Sprint* (5,000 to 25,000 SAR).
* **Action:** Direct outbound to Operations Directors.

### 2. B2B Professional Agencies & Consultants
* **Wedge:** Human-in-the-loop policies to prevent PII leakage under PDPL limits.
* **Fit:** *AI Trust Diagnostic* (5,000 SAR Starter).
"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[PASS] Opportunity radar generated at: {filepath}")

if __name__ == "__main__":
    scan_radar()
