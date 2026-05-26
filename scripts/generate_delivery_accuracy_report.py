import sys
import os
from datetime import datetime, timezone

def generate_report(client: str):
    print("==========================================")
    print(f" GENERATING DELIVERY ACCURACY REPORT FOR {client.upper()} ")
    print("==========================================")
    
    client = client.replace('"', '').replace("'", "").strip()
    
    reports_dir = os.path.join("reports", "delivery")
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, f"delivery_accuracy_report_{client.replace(' ', '_').lower()}.md")
    
    content = f"""# 📦 تقرير تحسين دقة التوصيل والعناوين (Delivery Accuracy Report)
**العميل:** {client}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**المعد:** سامي عسيري (ديلكس)

---

## 1. أسباب فشل التوصيل الحالية (Delivery Defect Analysis)
* أخطاء العنوان الوطني الصالح للطرود.
* تجاهل العملاء لمكالمات المندوبين.
* عدم دقة إدخال تفاصيل الشحن.

## 2. توافق لوائح هيئة النقل 2026 (TGA National Address Compliance)
* **نسبة الجاهزية الحالية:** 40% (تحتاج تصحيح).
* **الفجوة الحرجة:** رفض الشحنات التي لا تحتوي على عناوين موثقة ابتداءً من يناير 2026.

## 3. مسار التصحيح المقترح (Customer Correction Flow)
* إرسال تنبيه واتساب آلي بتوقيع معتمد يحوي رابط تصحيح الخرائط فور استلام الشحنة الناقصة.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Report generated successfully at: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/generate_delivery_accuracy_report.py \"Client Name\"")
        sys.exit(1)
    generate_report(sys.argv[1])
