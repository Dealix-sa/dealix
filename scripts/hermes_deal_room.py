import sys
import os
import json
import argparse
from datetime import datetime, timezone

DEALS_FILE = os.path.join("data", "ledgers", "hermes_deal_rooms.json")

def create_deal_room(client, pain, offer, target_price, floor_price, strategic_value):
    print("==========================================")
    print(f" INITIALIZING SOVEREIGN B2B DEAL ROOM ")
    print("==========================================")
    
    os.makedirs(os.path.dirname(DEALS_FILE), exist_ok=True)
    if os.path.exists(DEALS_FILE):
        with open(DEALS_FILE, "r", encoding="utf-8") as f:
            try:
                deals = json.load(f)
            except Exception:
                deals = []
    else:
        deals = []
        
    deal_id = f"DR-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
    new_deal = {
        "id": deal_id,
        "client": client,
        "pain": pain,
        "offer": offer,
        "target_price": target_price,
        "floor_price": floor_price,
        "strategic_value": strategic_value,
        "status": "Negotiation"
    }
    
    deals.append(new_deal)
    with open(DEALS_FILE, "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
        
    print(f"B2B Deal Room {deal_id} for '{client}' initialized successfully.")
    print(f"  - Target Price: {target_price} SAR")
    print(f"  - Floor Price:  {floor_price} SAR")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True)
    parser.add_argument("--pain", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--target-price", required=True)
    parser.add_argument("--floor-price", required=True)
    parser.add_argument("--strategic-value", required=True)
    
    args = parser.parse_args()
    create_deal_room(args.client, args.pain, args.offer, args.target_price, args.floor_price, args.strategic_value)
