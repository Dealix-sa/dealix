import os
import json

def safe_init():
    print("==========================================")
    print(" INITIALIZING HERMES LEDGERS SAFELY ")
    print("==========================================")
    
    ledgers_dir = os.path.join("data", "ledgers")
    os.makedirs(ledgers_dir, exist_ok=True)
    
    hermes_files = {
        "hermes_signals.json": [],
        "hermes_opportunities.json": [],
        "hermes_outcomes.json": [],
        "hermes_assets.json": [],
        "hermes_decisions.json": [],
        "hermes_relationships.json": [],
        "hermes_deal_rooms.json": [],
        "hermes_partners.json": [],
        "hermes_productization.json": []
    }
    
    for filename, default_data in hermes_files.items():
        filepath = os.path.join(ledgers_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
            print(f"  + Created ledger: {filename}")
        else:
            print(f"  - Verified existing: {filename}")
            
    print("\nState: HERMES_CORE_V1_ACTIVE")

if __name__ == "__main__":
    safe_init()
