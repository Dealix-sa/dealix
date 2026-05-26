import os
import sys
import zipfile
import glob

def restore_latest():
    backup_dir = os.path.join("data", "backups")
    if not os.path.exists(backup_dir):
        print(f"Error: Backup directory {backup_dir} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    zip_files = glob.glob(os.path.join(backup_dir, "dealix_snapshot_*.zip"))
    if not zip_files:
        print("Error: No dealix snapshots found to restore.", file=sys.stderr)
        sys.exit(1)
        
    # Find latest file
    latest_zip = max(zip_files, key=os.path.getmtime)
    print("==========================================")
    print(f" RESTORING LATEST SNAPSHOT: {os.path.basename(latest_zip)} ")
    print("==========================================")
    
    with zipfile.ZipFile(latest_zip, 'r') as zipf:
        zipf.extractall()
        for member in zipf.namelist():
            print(f"  - Extracted/Restored: {member}")
            
    print("\n[green]Success:[/green] Latest snapshot successfully restored to active state.")

if __name__ == "__main__":
    restore_latest()
