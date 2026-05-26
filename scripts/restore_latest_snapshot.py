#!/usr/bin/env python3
import os
import shutil

def main():
    print("[Dealix Runtime Restore] Restoring from Latest Snapshot...")
    backups_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/backups"))
    dest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/ledgers"))
    
    if not os.path.exists(backups_dir):
        print("No backups found.")
        return
        
    snapshots = sorted([d for d in os.listdir(backups_dir) if d.startswith("snapshot_")], reverse=True)
    if not snapshots:
        print("No snapshots available.")
        return
        
    latest = snapshots[0]
    source_dir = os.path.join(backups_dir, latest)
    
    os.makedirs(dest_dir, exist_ok=True)
    for f in os.listdir(source_dir):
        shutil.copy2(os.path.join(source_dir, f), dest_dir)
        
    print(f"[Success] Restored from {latest}")

if __name__ == "__main__":
    main()
