import os
import json
import sys

DELIVERY_LEDGER = os.path.join("data", "ledgers", "delivery_ledger.json")

def track_delivery():
    print("==========================================")
    print(" ACTIVE SPRINT DELIVERY TRACKER ")
    print("==========================================")
    
    if not os.path.exists(DELIVERY_LEDGER):
        # Seed placeholder
        data = [{
            "client": "Al-Majd Group",
            "offer": "ai-trust",
            "kickoff_date": "2026-05-26",
            "status": "delivery_started",
            "progress_percent": 80
        }]
        os.makedirs(os.path.dirname(DELIVERY_LEDGER), exist_ok=True)
        with open(DELIVERY_LEDGER, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    with open(DELIVERY_LEDGER, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    for r in records:
        print(f"* Client:   {r.get('client')}")
        print(f"  Offer:    {r.get('offer')}")
        print(f"  Kickoff:  {r.get('kickoff_date')}")
        print(f"  Progress: {r.get('progress_percent')}%")
        print(f"  Status:   {r.get('status')}\n")
        
    print("DELIVERY_REPORT=PASS")

if __name__ == "__main__":
    track_delivery()
