import sys
import os
from datetime import datetime, timezone

def generate_retainer(client: str, offer_type: str):
    print("==========================================")
    print(f" COMPILING RETAINER OFFER: {client.upper()} ({offer_type.upper()}) ")
    print("==========================================")
    
    client = client.replace('"', '').replace("'", "").strip()
    offer_type = offer_type.replace('"', '').replace("'", "").strip()
    
    reports_dir = os.path.join("reports", "retainers")
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, f"retainer_offer_{client.replace(' ', '_').lower()}.md")
    
    content = f"""# 🏆 مقترح التعاقد والاستبقاء الشهري (B2B Retainer Proposal)
**مقدم لشركة:** {client}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**الخدمة السابقة:** {offer_type}

---

## 1. نموذج التعاقد المستمر (Monthly Retainer Model)
بعد نجاح تسليم التشخيص التشغيلي وإثبات القيمة، نوصي بالانتقال لباقة الاستبقاء لضمان استدامة الضوابط:

* **باقة الحماية الأساسية (Light - 5,000 ريال شهرياً):** مراجعة شهرية لمخرجات الذكاء الاصطناعي وتحديث مصفوفات الصلاحيات.
* **باقة التشغيل الكامل (Standard - 10,000 ريال شهرياً):** مراجعة نصف شهرية، تحديث مستمر لخريطة المخاطر، وتقرير شهري تنفيذي للإدارة.
* **باقة التميز التنفيذي (Executive - 20,000 ريال شهرياً):** دعم كامل على مدار الساعة، مراجعة فورية للمسودات، وتدريب مستمر للفريق.

---

**الخطوة التالية:** يرجى الموافقة وتحديد مستوى الباقة المفضلة للبدء في صياغة العقد السنوي المعتمد.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Retainer Offer generated successfully at: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: py -3 scripts/retainer_offer.py \"Client Name\" \"Offer Type\"")
        sys.exit(1)
    generate_retainer(sys.argv[1], sys.argv[2])
