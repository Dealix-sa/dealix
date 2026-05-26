import os
import sys
import zipfile
from datetime import datetime, timezone

def create_snapshot():
    backup_dir = os.path.join("data", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    zip_filename = f"dealix_snapshot_{timestamp}.zip"
    zip_filepath = os.path.join(backup_dir, zip_filename)
    
    # Files to backup
    ops_dir = os.path.join("docs", "ops")
    ledgers_dir = os.path.join("data", "ledgers")
    
    print("==========================================")
    print(" CREATING DEALIX RUNTIME SNAPSHOT ")
    print("==========================================")
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Backup docs/ops/
        if os.path.exists(ops_dir):
            for root, _, files in os.walk(ops_dir):
                for file in files:
                    if file.endswith(".md") or file.endswith(".csv"):
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, start=os.getcwd())
                        zipf.write(filepath, arcname)
                        print(f"  + Added: {arcname}")
                        
        # Backup data/ledgers/
        if os.path.exists(ledgers_dir):
            for root, _, files in os.walk(ledgers_dir):
                for file in files:
                    if file.endswith(".json"):
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, start=os.getcwd())
                        zipf.write(filepath, arcname)
                        print(f"  + Added: {arcname}")
                        
    print(f"\n[green]Success:[/green] Zipped runtime snapshot created at: {zip_filepath}")

if __name__ == "__main__":
    create_snapshot()
