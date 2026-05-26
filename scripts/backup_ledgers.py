import os
import shutil
from datetime import datetime, timezone

def backup():
    print("==========================================")
    print(" BACKING UP ACTIVE LEDGERS ")
    print("==========================================")
    
    backup_dir = os.path.join("data", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    ops_dir = os.path.join("docs", "ops")
    ledgers = [
        "EXECUTION_LEDGER.md",
        "REVENUE_LEDGER.md",
        "PROOF_LEDGER.md",
        "RISK_LEDGER.md",
        "DECISION_LEDGER.md"
    ]
    
    for l in ledgers:
        src = os.path.join(ops_dir, l)
        if os.path.exists(src):
            dest = os.path.join(backup_dir, f"{l}.bak")
            shutil.copy2(src, dest)
            print(f"  + Backed up: {l} -> backups/{l}.bak")
            
    print("\nBACKUP_LEDGERS=PASS")

if __name__ == "__main__":
    backup()
