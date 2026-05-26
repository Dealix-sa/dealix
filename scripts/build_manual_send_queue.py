import sys
import json
import os
from datetime import datetime, timezone
from dealix_local_ai import generate_text
from verify_quality_scorer import score_quality
from verify_governance_check import check_governance

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
QUEUE_DIR = os.path.join("local_ai", "queue")

def build_send_queue():
    if not os.path.exists(PROSPECTS_FILE):
        print(f"Error: {PROSPECTS_FILE} not found.")
        sys.exit(1)
        
    with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
        prospects = json.load(f)
        
    ready_to_send = [p for p in prospects if p.get("status") == "ready_to_send" or p.get("status") == "not_contacted"]
    
    if not ready_to_send:
        print("No leads ready for outreach.")
        sys.exit(0)
        
    os.makedirs(QUEUE_DIR, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    queue_file = os.path.join(QUEUE_DIR, f"manual-send-queue-{today}.md")
    
    with open(queue_file, "w", encoding="utf-8") as out:
        out.write(f"# Manual Send Queue - {today}\n\n")
        
        for p in ready_to_send:
            company = p.get("company", "Unknown")
            print(f"Processing draft for {company}...")
            
            prompt = f"""
Write a B2B LinkedIn/Email outreach message to the CEO/Founder of {company}.
The offer is an "AI Trust Diagnostic" or "Delivery Accuracy Sprint" (choose the most relevant based on the company if known, else AI Trust).
The goal is to book a 15-minute discovery call.
Be professional, concise, and end with a clear question (CTA).
DO NOT use absolute claims. Write in Arabic.
"""
            draft = generate_text(prompt, model="qwen3:4b")
            
            is_quality = score_quality(draft)
            is_governed = check_governance(draft)
            
            if is_quality and is_governed:
                out.write(f"## Lead: {company}\n")
                out.write(f"**Target:** {p.get('target', 'CEO/Founder')}\n")
                out.write(f"**Status:** {p.get('status')}\n\n")
                out.write("### Message Draft\n")
                out.write(f"{draft}\n\n")
                out.write("---\n")
                
                # Auto-update status to 'draft_ready' or something similar so we don't draft again?
                # The user requested 'ready_to_send' -> 'outreach_sent' manually.
            else:
                out.write(f"## Lead: {company} [DRAFT REJECTED BY SCORER/GOVERNANCE]\n")
                out.write("---\n")
                
    print(f"Queue generated at {queue_file}")

if __name__ == "__main__":
    build_send_queue()
