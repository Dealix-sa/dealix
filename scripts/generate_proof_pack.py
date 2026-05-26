import sys
import os
import json
import subprocess
from datetime import datetime, timezone
from dealix_local_ai import generate_text

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
REPORTS_DIR = os.path.join("reports", "board")

def generate_proof_pack(company: str):
    # Sanitize quotes
    company = company.replace('"', '').replace("'", "").strip()
    
    if not os.path.exists(PROSPECTS_FILE):
        print(f"Error: {PROSPECTS_FILE} not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(PROSPECTS_FILE, "r", encoding="utf-8") as f:
        prospects = json.load(f)
        
    lead = next((p for p in prospects if p.get("company", "").lower() == company.lower() or p.get("name", "").lower() == company.lower() or p.get("company_name", "").lower() == company.lower()), None)
    
    if not lead:
        lead = {
            "company": company,
            "offer": "ai-trust"
        }

    offer_type = lead.get("offer", "ai-trust")
    print(f"Generating Proof Pack for {company} ({offer_type})...")
    
    # Pre-formatted elegant fallback template
    proof_text = f"""# 🏆 حزمة الإثبات وعرض الاستبقاء (Proof Pack & Retainer Offer)
**العميل:** {company}
**الخدمة المنجزة:** {offer_type}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**شريك النجاح:** سامي عسيري (مؤسس ديلكس)

---

## 1. إثبات القيمة (Proof of Value)
خلال فترة العمل السابقة، نجحنا في تسليم المخرجات التالية بجودة عالية:
* **AI Usage Inventory:** حصر كامل لجميع أدوات ونماذج الذكاء الاصطناعي المستخدمة.
* **Risk Map:** خريطة دقيقة تحدد ثغرات الأمن والخصوصية ومخاطر تسريب البيانات الحساسة.
* **Human Approval Matrix:** مصفوفة صلاحيات تضمن موافقة الموظف البشري قبل خروج أي محتوى أو رد خارجي.
* **Governance Roadmap:** خطة عمل واضحة للـ 30 يوماً القادمة متوافقة مع NIST AI RMF ونظام PDPL السعودي.

## 2. العوائد المحققة (Value Realized)
* **تقليل مخاطر تسريب البيانات الحساسة بنسبة 100%.**
* **تنظيم تدفق الموافقات البشرية وتقليل وقت المراجعة التشغيلية.**
* **بناء الثقة القانونية مع الشركاء والعملاء.**

## 3. مقترح باقة الاستبقاء الشهري (AI Governance Retainer)
للحفاظ على هذا المستوى من الحماية والنمو المنضبط، نقدم خيارات الاستبقاء التالية:
* **Light (4,000 ريال/شهرياً):** مراجعة شهرية لمخرجات الذكاء الاصطناعي الحساسة وتحديث مصفوفة الصلاحيات.
* **Standard (10,000 ريال/شهرياً):** مراجعة نصف شهرية، تحديث مستمر لخريطة المخاطر، وتقرير شهري تنفيذي للإدارة.
* **Executive (20,000 ريال/شهرياً):** دعم كامل على مدار الساعة، مراجعة فورية للمسودات، وتدريب مستمر للفريق.

---

**الخطوة التالية:** مراجعة التقرير وتحديد مستوى باقة الاستبقاء المطلوبة لتوقيع العقد السنوي.
"""

    try:
        prompt = f"Write a professional Arabic Proof Pack and Retainer Offer for {company} regarding {offer_type}. Summarize risk mitigations."
        ai_generated = generate_text(prompt, model="qwen2.5-coder:7b")
        if ai_generated and len(ai_generated.strip()) > 100:
            proof_text = ai_generated
    except Exception:
        pass

    os.makedirs(REPORTS_DIR, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    filename = f"proof_pack_{company.replace(' ', '_').lower()}_{today}.md"
    filepath = os.path.join(REPORTS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(proof_text)
        
    print(f"Proof Pack and Retainer Offer generated at {filepath}")
    
    cmd = [sys.executable, "dealix.py", "proof-pack", "--client", company, "--service", offer_type]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Failed to run dealix CLI proof-pack logging.", file=sys.stderr)
        
    print(f"\nNext Action: Present the Proof Pack to the client and wait for Retainer decision.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/generate_proof_pack.py \"Company Name\"")
        sys.exit(1)
        
    company = sys.argv[1]
    generate_proof_pack(company)
