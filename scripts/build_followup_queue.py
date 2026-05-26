import sys
import json
import os
from datetime import datetime, timezone
from dealix_local_ai import generate_text
from verify_quality_scorer import score_quality
from verify_governance_check import check_governance

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
QUEUE_DIR = os.path.join("local_ai", "followups")

def build_followup_queue():
    if not os.path.exists(PROSPECTS_FILE):
        print(f"Error: {PROSPECTS_FILE} not found.")
        sys.exit(1)
        
    with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
        prospects = json.load(f)
        
    followups_needed = [p for p in prospects if p.get("status") == "outreach_sent"]
    
    if not followups_needed:
        print("No leads need follow-up currently.")
        sys.exit(0)
        
    os.makedirs(QUEUE_DIR, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    queue_file = os.path.join(QUEUE_DIR, f"follow-up-queue-{today}.md")
    
    with open(queue_file, "w", encoding="utf-8") as out:
        out.write(f"# Follow-up Queue - {today}\n\n")
        
        for p in followups_needed:
            company = p.get("company", "Unknown")
            print(f"Processing follow-up draft for {company}...")
            
            prompt = f"""
Write a polite, professional, and short follow-up message to the CEO/Founder of {company}.
We previously offered an AI Trust Diagnostic.
The goal is to gently bump the conversation and ask if they have 5 minutes this week.
DO NOT be pushy. Write in Arabic.
"""
            draft = generate_text(prompt, model="qwen3:4b")
            
            is_quality = score_quality(draft)
            is_governed = check_governance(draft)
            
            if is_quality and is_governed:
                out.write(f"## Lead: {company}\n")
                out.write(f"**Target:** {p.get('target', 'CEO/Founder')}\n")
                out.write(f"**Status:** {p.get('status')}\n\n")
                out.write("### Follow-up Draft\n")
                out.write(f"{draft}\n\n")
                out.write("---\n")
            else:
                out.write(f"## Lead: {company} [FOLLOW-UP DRAFT REJECTED]\n")
                out.write("---\n")
                
    print(f"Follow-up Queue generated at {queue_file}")

if __name__ == "__main__":
    build_followup_queue()
