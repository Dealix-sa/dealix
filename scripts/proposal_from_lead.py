import sys
import json
import os
import subprocess
from datetime import datetime, timezone
from dealix_local_ai import generate_text

PROSPECTS_FILE = os.path.join("data", "ledgers", "prospects.json")
REPORTS_DIR = os.path.join("reports")

def proposal_from_lead(company: str):
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
            "sector": "Technology",
            "offer": "ai-trust"
        }
        
    offer_type = lead.get("offer", "ai-trust")
    print(f"Generating Proposal for {company} regarding {offer_type}...")
    
    # Fallback Proposal Templates
    proposal_text = ""
    
    if offer_type == "delivery-accuracy":
        proposal_text = f"""# 📦 عرض سعر تنفيذي: Delivery Accuracy Sprint
**مقدم لشركة:** {company}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**مقدم من:** شركة ديلكس لتنظيم وحوكمة تقنيات الأعمال

---

## 1. المقدمة والأهداف
يواجه قطاع الخدمات اللوجستية والتجارة الإلكترونية في المملكة تحديات متسارعة، خاصة مع تطبيق إلزام الهيئة العامة للنقل (TGA) للتحقق من العنوان الوطني للشحنات بحلول يناير 2026.
يهدف هذا العرض إلى تقديم **Delivery Accuracy Sprint** لتنظيم ومعالجة أسباب فشل التوصيل وتحسين جودة بيانات العناوين.

## 2. نطاق العمل (Scope of Work)
1. **Address Readiness Audit:** مراجعة جودة بيانات العناوين وتحديد الثغرات.
2. **Failed Delivery Reason Map:** رسم خريطة بأسباب فشل التوصيل المتكررة.
3. **Customer Correction Flow:** تصميم مسار آلي لتصحيح العناوين بواسطة العميل مباشرة.
4. **Delivery Accuracy Report:** تقرير تنفيذي شامل يوضح معدلات النجاح والتحسين المالي.

## 3. مدة التنفيذ والجدول الزمني
* **المدة الإجمالية:** 10 أيام عمل من تاريخ توقيع الاتفاقية ودفع الدفعة الأولى.

## 4. الميزانية والاستثمار (B2B Investment)
* **القيمة الإجمالية للمشروع:** 5,000 ريال سعودي.
* **شروط الدفع:** 100% مقدماً للبدء المباشر.

## 5. الخطوة التالية (Call to Action)
للبدء الفوري وتجهيز بوابة العمل، يرجى الموافقة على هذا المقترح للبدء في مسار الإعداد والتحصيل.
"""
    else:
        proposal_text = f"""# 🏢 عرض سعر تنفيذي: AI Trust Diagnostic
**مقدم لشركة:** {company}
**التاريخ:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
**مقدم من:** شركة ديلكس لتنظيم وحوكمة تقنيات الأعمال

---

## 1. المقدمة والأهداف
مع زيادة استخدام أدوات الذكاء الاصطناعي في الأعمال (كتابة المحتوى، الدعم، والمبيعات)، تظهر مخاطر مرتبطة بتسريب البيانات وحماية الخصوصية (PDPL) وسلامة الادعاءات الخارجية.
يهدف هذا التشخيص لمساعدتكم على حصر الاستخدامات وتحديد المخاطر وبناء مصفوفة موافقات تشغيلية واضحة.

## 2. نطاق العمل (Scope of Work)
1. **AI Usage Inventory:** حصر شامل لجميع أدوات ونماذج الذكاء الاصطناعي المستخدمة داخل الشركة.
2. **Agent & Tool Risk Map:** تحديد المخاطر المرتبطة بكل أداة وصلاحيات الوصول.
3. **Data Sensitivity Review:** مراجعة البيانات الحساسة ومستوى توافقها مع نظام حماية البيانات الشخصية الشخصية السعودي (PDPL).
4. **Human Approval Matrix:** بناء مصفوفة الصلاحيات والموافقات البشرية قبل خروج أي مخرج خارجي للعميل.

## 3. مدة التنفيذ والجدول الزمني
* **المدة الإجمالية:** 5 أيام عمل من تاريخ البدء وتأكيد الدفع.

## 4. الميزانية والاستثمار (B2B Investment)
* **القيمة الإجمالية للتشخيص:** 5,000 ريال سعودي.
* **شروط الدفع:** 100% مقدماً للبدء المباشر.

## 5. الخطوة التالية (Call to Action)
للبدء الفوري وتجهيز بوابة العمل، يرجى الموافقة على هذا المقترح للبدء في مسار الإعداد والتحصيل.
"""

    try:
        prompt = f"Write a professional Arabic proposal for {company} regarding {offer_type}. Keep it formal B2B, no overpromises."
        ai_generated = generate_text(prompt, model="qwen2.5-coder:7b")
        if ai_generated and len(ai_generated.strip()) > 100:
            proposal_text = ai_generated
    except Exception:
        pass

    os.makedirs(REPORTS_DIR, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    filename = f"proposal_{company.replace(' ', '_').lower()}_{today}.md"
    filepath = os.path.join(REPORTS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(proposal_text)
        
    print(f"Proposal generated at {filepath}")
    
    cmd = [sys.executable, os.path.join("scripts", "mark_lead.py"), company, "proposal_sent", f"Proposal sent: reports/{filename}"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to update lead status to proposal_sent.", file=sys.stderr)
        
    print(f"\nNext Action: Review {filepath}, send to client, then run:")
    print(f"powershell -File scripts/start_paid_delivery.ps1 -Client \"{company}\" -Offer \"{offer_type}\" -Amount \"5000\"")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py -3 scripts/proposal_from_lead.py \"Company Name\"")
        sys.exit(1)
        
    company = sys.argv[1]
    proposal_from_lead(company)
