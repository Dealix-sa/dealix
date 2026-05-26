import sys
import os
import json
import argparse
from datetime import datetime, timezone

DECISIONS_FILE = os.path.join("data", "ledgers", "hermes_decisions.json")

def create_memo(topic, decision, rational, impact):
    print("==========================================")
    print(" COMPILING SOVEREIGN FOUNDER DECISION MEMO ")
    print("==========================================")
    
    os.makedirs(os.path.dirname(DECISIONS_FILE), exist_ok=True)
    if os.path.exists(DECISIONS_FILE):
        with open(DECISIONS_FILE, "r", encoding="utf-8") as f:
            try:
                decisions = json.load(f)
            except Exception:
                decisions = []
    else:
        decisions = []
        
    dec_id = f"DEC-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
    new_dec = {
        "id": dec_id,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "topic": topic,
        "decision": decision,
        "rational": rational,
        "impact": impact
    }
    
    decisions.append(new_dec)
    with open(DECISIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(decisions, f, indent=2, ensure_ascii=False)
        
    # Write MD report
    reports_dir = os.path.join("reports", "founder")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, f"decision_memo_{dec_id.lower()}.md")
    
    content = f"""# 🛡️ وثيقة قرار المؤسس السيادي (Sovereign Founder Decision Memo)
**القرار المعرّف:** {dec_id}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**الموضوع:** {topic}

---

## 1. القرار المتخذ (The Decision):
{decision}

## 2. مبررات القرار والمنطق التشغيلي (The Rational):
{rational}

## 3. الأثر المتوقع على الأرباح والنمو (The Expected Impact):
{impact}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Sovereign Decision {dec_id} logged.")
    print(f"Memo drafted at: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="B2B Pilot Pricing Policy")
    parser.add_argument("--decision", default="Standardize diagnostic fee at 5,000 SAR prepaid.")
    parser.add_argument("--rational", default="Aligns client commitment and funds immediate delivery sprints.")
    parser.add_argument("--impact", default="Creates healthy working capital margins.")
    
    args = parser.parse_args()
    create_memo(args.topic, args.decision, args.rational, args.impact)
