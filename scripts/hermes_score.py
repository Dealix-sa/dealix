import sys
import json

def calculate_score(input_json_str: str):
    print("==========================================")
    print(" CALCULATING OPPORTUNITY CORE SCORE - HERMES ")
    print("==========================================")
    
    try:
        data = json.loads(input_json_str)
        rev = float(data.get("verified_revenue_potential", 50))
        speed = float(data.get("speed_to_cash", 50))
        
        # Simple weighted scoring
        score = (rev * 0.6) + (speed * 0.4)
        
        print(f"Metrics Evaluated:")
        print(f"  - Revenue Potential (60% weight): {rev}")
        print(f"  - Speed to Cash     (40% weight): {speed}")
        print(f"\nWeighted Hermes Score: {score}/100")
        
        if score >= 75:
            print("\n[VERDICT] Priority Tier 1: Engage outreach immediately.")
        else:
            print("\n[VERDICT] Priority Tier 2: Nurture phase candidate.")
            
    except Exception as e:
        print(f"Error parsing metrics input: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/hermes_score.py \"{\\\"verified_revenue_potential\\\":80,\\\"speed_to_cash\\\":80}\"")
        sys.exit(1)
    calculate_score(sys.argv[1])
