import sys
import os
import json
import argparse
from datetime import datetime, timezone

OUTCOMES_FILE = os.path.join("data", "ledgers", "hermes_outcomes.json")

def log_outcome(action_type, target, expected, actual, won, revenue, learning):
    print("==========================================")
    print(" LOGGING OUTCOME ACTION & LEARNING MEMO ")
    print("==========================================")
    
    os.makedirs(os.path.dirname(OUTCOMES_FILE), exist_ok=True)
    if os.path.exists(OUTCOMES_FILE):
        with open(OUTCOMES_FILE, "r", encoding="utf-8") as f:
            try:
                outcomes = json.load(f)
            except Exception:
                outcomes = []
    else:
        outcomes = []
        
    out_id = f"OUT-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
    new_out = {
        "id": out_id,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "action_type": action_type,
        "target": target,
        "expected": expected,
        "actual": actual,
        "won": won,
        "revenue": float(revenue),
        "learning": learning
    }
    
    outcomes.append(new_out)
    with open(OUTCOMES_FILE, "w", encoding="utf-8") as f:
        json.dump(outcomes, f, indent=2, ensure_ascii=False)
        
    print(f"Action Outcome {out_id} logged successfully.")
    print(f"  + Target:   {target}")
    print(f"  + Learning: {learning}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-type", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--actual", required=True)
    parser.add_argument("--won", required=True)
    parser.add_argument("--revenue", required=True)
    parser.add_argument("--learning", required=True)
    
    args = parser.parse_args()
    log_outcome(args.action_type, args.target, args.expected, args.actual, args.won, args.revenue, args.learning)
