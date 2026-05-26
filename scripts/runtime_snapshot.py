#!/usr/bin/env python3
import os
import shutil
import datetime

def main():
    print("[Dealix Runtime Backup] Initiating Snapshot...")
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/ledgers"))
    dest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../data/backups/snapshot_{timestamp}"))
    
    if not os.path.exists(source_dir):
        print("No ledgers found to backup.")
        return
        
    os.makedirs(dest_dir, exist_ok=True)
    for f in os.listdir(source_dir):
        if f.endswith(".json"):
            shutil.copy2(os.path.join(source_dir, f), dest_dir)
            
    print(f"[Success] Snapshot created at {dest_dir}")

if __name__ == "__main__":
    main()
