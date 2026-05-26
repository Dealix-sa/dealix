import sys
import os
from datetime import datetime, timezone

def generate_report(client: str):
    print("==========================================")
    print(f" GENERATING AI TRUST REPORT FOR {client.upper()} ")
    print("==========================================")
    
    client = client.replace('"', '').replace("'", "").strip()
    
    reports_dir = os.path.join("reports", "delivery")
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, f"ai_trust_report_{client.replace(' ', '_').lower()}.md")
    
    content = f"""# 🛡️ تقرير تشخيص أمان الذكاء الاصطناعي (AI Trust Diagnostic)
**العميل:** {client}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**المعد:** سامي عسيري (ديلكس للحوكمة)

---

## 1. حصر الأدوات والأنظمة (AI Usage Inventory)
* **ChatGPT & Claude:** تستخدم في المبيعات وكتابة المقترحات.
* **Ollama (المحلي):** مستخدم في التحليلات والحوكمة الداخلية.

## 2. خريطة المخاطر الحالية (Risk Mapping)
* **تسريب البيانات (PII/PDPL):** خطر متوسط بسبب مدخلات العملاء الحساسة بدون فلترة.
* **أمان الادعاءات الخارجية:** خطر عالٍ بسبب استخدام صيغ مطلقة مثل "نضمن 100%".

## 3. مصفوفة الصلاحيات المقترحة (Human Approval Matrix)
* **المسودة الأولية:** ذكاء اصطناعي.
* **المراجعة والاعتماد:** بشري (الموظف المسؤول).
* **إطلاق الإرسال:** بشري مع تسجيل رمز الموافقات المعتمد.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Report generated successfully at: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/generate_ai_trust_report.py \"Client Name\"")
        sys.exit(1)
    generate_report(sys.argv[1])
