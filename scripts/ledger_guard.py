import os
import sys

def guard_ledgers():
    print("==========================================")
    print(" RUNNING LEDGER GUARD - INTEGRITY MATRIX ")
    print("==========================================")
    
    ledgers_dir = os.path.join("docs", "ops")
    ledgers = [
        "EXECUTION_LEDGER.md",
        "REVENUE_LEDGER.md",
        "PROOF_LEDGER.md",
        "RISK_LEDGER.md",
        "DECISION_LEDGER.md"
    ]
    
    all_ok = True
    for l in ledgers:
        path = os.path.join(ledgers_dir, l)
        if not os.path.exists(path):
            print(f"  - {l}: [FAIL] File missing!")
            all_ok = False
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        if len(lines) < 2:
            print(f"  - {l}: [FAIL] Empty or corrupted markdown structure!")
            all_ok = False
            continue
            
        # Check if first and second lines start with '|'
        if not lines[0].strip().startswith("|") or not lines[1].strip().startswith("|"):
            print(f"  - {l}: [FAIL] Markdown table header structure invalid!")
            all_ok = False
            continue
            
        print(f"  - {l}: [PASS] Integrity check completed.")
        
    if all_ok:
        print("\nLEDGER_GUARD=PASS")
    else:
        print("\nLEDGER_GUARD=FAIL")
        sys.exit(1)

if __name__ == "__main__":
    guard_ledgers()
