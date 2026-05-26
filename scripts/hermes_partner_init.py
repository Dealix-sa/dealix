import os
import json

PARTNERS_FILE = os.path.join("data", "ledgers", "hermes_partners.json")

def init_partners():
    print("==========================================")
    print(" INITIALIZING HERMES PARTNERS SCHEMA ")
    print("==========================================")
    
    os.makedirs(os.path.dirname(PARTNERS_FILE), exist_ok=True)
    
    # Pre-populate sample partner
    partners = [
        {
            "name": "Creative Agency partner",
            "company": "Mena Marketing",
            "type": "agency",
            "sector": "Marketing",
            "trust": "established",
            "audience": "SMB brands",
            "offer_fit": "AI Trust Diagnostic",
            "potential_value": "high",
            "next": "send partner intro pack"
        }
    ]
    
    with open(PARTNERS_FILE, "w", encoding="utf-8") as f:
        json.dump(partners, f, indent=2, ensure_ascii=False)
        
    print(f"Partners schema initialized successfully.")

if __name__ == "__main__":
    init_partners()
