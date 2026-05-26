import sys
import os
from datetime import datetime, timezone

REPORTS_DIR = os.path.join("reports", "partners")

def generate_partner_pack(partner_name: str, offer_fit: str):
    print("==========================================")
    print(f" COMPILING HERMES PARTNER PACK FOR {partner_name.upper()} ")
    print("==========================================")
    
    partner_name = partner_name.replace('"', '').replace("'", "").strip()
    offer_fit = offer_fit.replace('"', '').replace("'", "").strip()
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"partner_pack_{partner_name.replace(' ', '_').lower()}.md")
    
    content = f"""# 🤝 حزمة تدريب وتأهيل الشركاء (Hermes Partner Pack)
**الطرف الشريك:** {partner_name}
**الخدمة المعروضة:** {offer_fit}
**التاريخ:** {today}

---

## 1. برنامج التمكين للشركاء (Commission & Value Share)
نقدم لشركائنا المعتمدين برنامج شراكة مجزٍ ومستدام:
* **عمولة تشجيعية (Referral):** 10% من قيمة التشخيص الأولي لأي عميل يتم تحويله وإغلاقه بنجاح.
* **إدارة الحسابات المشتركة:** نحن نقوم بالتسليم الفني للتشخيص وتصنيف الأدوات، بينما تظل العلاقة التشغيلية كاملة تحت تصرفكم.

## 2. العروض التسويقية المجهزة (Whitelabel Assets)
* **Outreach templates:** نصوص التواصل الأولي الموثقة التي أثبتت فعاليتها.
* **Proof Pack Template:** نموذج استعراض عائد الاستثمار الفني والتنظيمي.
* **PDPL compliance guide:** دليل أمان البيانات لتسهيل ردود فعل الشركاء القانونيين.
"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Partner Pack successfully generated at: {filepath}")

if __name__ == "__main__":
    p_name = sys.argv[1] if len(sys.argv) > 1 else "Marketing Agency Partner"
    o_fit = sys.argv[2] if len(sys.argv) > 2 else "AI Trust Diagnostic"
    generate_partner_pack(p_name, o_fit)
