import sys
import os
import json
import argparse
from datetime import datetime, timezone

SIGNALS_FILE = os.path.join("data", "ledgers", "hermes_signals.json")

def capture_signal(source, sector, text, why, offer, first_action):
    print("==========================================")
    print(" CAPTURING MARKET INTEL SIGNAL ")
    print("==========================================")
    
    os.makedirs(os.path.dirname(SIGNALS_FILE), exist_ok=True)
    
    if os.path.exists(SIGNALS_FILE):
        with open(SIGNALS_FILE, "r", encoding="utf-8") as f:
            try:
                signals = json.load(f)
            except Exception:
                signals = []
    else:
        signals = []
        
    signal_id = f"SIG-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
    new_signal = {
        "id": signal_id,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source": source,
        "sector": sector,
        "text": text,
        "why": why,
        "offer": offer,
        "first_action": first_action
    }
    
    signals.append(new_signal)
    with open(SIGNALS_FILE, "w", encoding="utf-8") as f:
        json.dump(signals, f, indent=2, ensure_ascii=False)
        
    print(f"Signal {signal_id} captured successfully.")
    print(f"  + Sector: {sector}")
    print(f"  + Pain:   {text}")
    print(f"  + Action: {first_action}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture Hermes Market Intel Signal")
    parser.add_argument("--source", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--why", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--first-action", required=True)
    
    args = parser.parse_args()
    capture_signal(args.source, args.sector, args.text, args.why, args.offer, args.first_action)
