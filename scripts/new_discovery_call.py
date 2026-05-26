import sys
import subprocess
import os
from datetime import datetime, timezone

def new_discovery_call(company: str):
    # Sanitize quotes
    company = company.replace('"', '').replace("'", "").strip()
    
    print(f"Booking discovery call for {company}...")
    
    # 1. Update status
    cmd = [sys.executable, os.path.join("scripts", "mark_lead.py"), company, "call_booked", "Prepare for discovery meeting"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to mark lead {company} as call_booked.", file=sys.stderr)
        sys.exit(1)
        
    # 2. Generate a custom discovery template in reports/
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    safe_name = company.replace(' ', '_').lower()
    filename = f"discovery_brief_{safe_name}.md"
    filepath = os.path.join(reports_dir, filename)
    
    template_content = f"""# 📞 Discovery Session Guide — {company}
Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
Owner: Sami Assiri (Founder, Dealix)
Prospect Company: {company}

---

## 🎯 Meeting Objectives
1. Understand their current AI usage / Address validation bottlenecks.
2. Identify critical governance / delivery accuracy risks.
3. Validate BANT criteria.
4. Agree on next step (AI Trust Diagnostic / Delivery Accuracy Sprint).

## 📋 BANT Qualification Framework

### 💰 Budget (الميزانية)
* *Target investment range:* 5,000 SAR to 25,000 SAR.
* *Question:* "بناءً على النطاق، تكلفة التشخيص تبدأ من 5,000 ريال. هل هذا المخصص متوافق مع خططكم الحالية؟"

### 👑 Authority (الصلاحية)
* *Decision Maker:* Founder / CEO / Operations Director.
* *Question:* "من يشارك في اتخاذ القرار النهائي للموافقة على البدء بالتشخيص والعمل؟"

### 🎯 Need (الاحتياج)
* *For AI Trust:* Risks of PII leakage, lack of approval matrix, claims safety issues.
* *For Delivery Accuracy:* Address verification failures, TGA 2026 compliance.
* *Question:* "إيش أكبر تحدي يواجه الفريق حالياً بخصوص ضوابط البيانات أو تسليم الشحنات؟"

### ⏱️ Timeline (الجدول الزمني)
* *Diagnostic delivery:* 5 to 14 days.
* *Question:* "لو كل شي مناسب، متى تحبون نبدأ ونستلم المخرجات؟"

---

## 📝 Post-Call Action Plan
1. Send customized B2B proposal:
   `py -3 scripts/proposal_from_lead.py "{company}"`
2. Schedule a 10-minute proposal review.
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template_content)
        
    print(f"\nSuccess: Generated Custom Discovery Agenda template at: {filepath}")
    print(f"Next Action: Review {filepath} before joining the meeting.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/new_discovery_call.py \"Company Name\"")
        sys.exit(1)
        
    company = sys.argv[1]
    new_discovery_call(company)
