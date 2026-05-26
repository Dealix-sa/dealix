import sys
import os
import json
from datetime import datetime, timezone

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
DELIVERY_LEDGER = os.path.join("data", "ledgers", "delivery_ledger.json")

def load_delivery():
    if not os.path.exists(DELIVERY_LEDGER):
        return []
    with open(DELIVERY_LEDGER, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_delivery(data):
    os.makedirs(os.path.dirname(DELIVERY_LEDGER), exist_ok=True)
    with open(DELIVERY_LEDGER, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def kickoff_intake(client: str, offer: str):
    print("==========================================")
    print(" KICKING OFF NEW CLIENT INTAKE FLOW ")
    print("==========================================")
    
    client = client.replace('"', '').replace("'", "").strip()
    offer = offer.replace('"', '').replace("'", "").strip()
    
    # Register in delivery_ledger.json
    deliv_records = load_delivery()
    exists = next((d for d in deliv_records if d.get("client", "").lower() == client.lower()), None)
    
    if not exists:
        deliv_records.append({
            "client": client,
            "offer": offer,
            "kickoff_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "status": "intake_pending",
            "progress_percent": 10
        })
        save_delivery(deliv_records)
        
    # Generate intake file
    reports_dir = os.path.join("reports", "delivery")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, f"client_intake_{client.replace(' ', '_').lower()}.md")
    
    content = f"""# 📝 استمارة إعداد العميل (Client Intake Form) — {client}
**الخدمة:** {offer}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

---

## 1. أسئلة البدء الأساسية:
* **الأهداف الحالية:** ما هو الهدف الأساسي من وراء هذا التشغيل؟
* **الصلاحيات والأدوات:** ما هي أدوات الذكاء الاصطناعي النشطة حالياً في الفريق؟
* **قنوات التواصل:** أين يتم استخدام مخرجات الذكاء الاصطناعي مع الجمهور الخارجي؟

## 2. الخطوة التشغيلية القادمة:
1. مراجعة هذه الاستمارة مع الموظف التقني المسؤول.
2. إطلاق خريطة الحوكمة والمخاطر.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Intake form generated at: {filepath}")
    print("STATE: INTAKE_ACTIVE")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: py -3 scripts/new_client_intake.py \"Client Name\" \"Offer Name\"")
        sys.exit(1)
    client = sys.argv[1]
    offer = sys.argv[2]
    kickoff_intake(client, offer)
