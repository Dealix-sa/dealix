import sys
import os
import subprocess

def create_proof(client: str):
    print("==========================================")
    print(f" BUILDING B2B PROOF PACK FOR: {client.upper()} ")
    print("==========================================")
    
    client = client.replace('"', '').replace("'", "").strip()
    
    # Just invoke our generate_proof_pack.py
    cmd = [sys.executable, os.path.join("scripts", "generate_proof_pack.py"), client]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\nproof-pack generated and registered.")
    except Exception as e:
        print(f"Error running generate_proof_pack: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/proof_from_lead.py \"Client Name\"")
        sys.exit(1)
    create_proof(sys.argv[1])
