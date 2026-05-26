import sys
import os
from datetime import datetime, timezone

REPORTS_DIR = os.path.join("reports")

def generate_payment_request(client: str, amount: str, offer: str):
    print("==========================================")
    print(" GENERATING PAYMENT REQUEST DRAFT ")
    print("==========================================")
    
    # Sanitize quotes
    client = client.replace('"', '').replace("'", "").strip()
    amount = amount.replace('"', '').replace("'", "").strip()
    offer = offer.replace('"', '').replace("'", "").strip()
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"payment_request_{client.replace(' ', '_').lower()}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md")
    
    content = f"""# 💳 طلب دفعة مالية معتمد (Payment Request)
**العميل:** {client}
**الخدمة:** {offer}
**قيمة الاستثمار:** {amount} ريال سعودي
**التاريخ:** {today}

---

يسعدنا البدء بتشخيص أعمالكم وتنظيم حوكمة البيانات والذكاء الاصطناعي.
الرجاء تحويل دفعة الاستثمار البالغة **{amount} ريال** لإطلاق خطة العمل المباشرة Intake وتجهيز بوابة المخرجات.

لأي استفسارات قانونية، نرفق لكم ملخص الامتثال لنظام PDPL في الملحق الفني.
"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"PAYMENT_REQUEST=PASS")
    print(f"Draft saved to: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: py -3 scripts/payment_request.py \"Client Name\" \"Amount\" \"Offer Name\"")
        sys.exit(1)
    client = sys.argv[1]
    amount = sys.argv[2]
    offer = sys.argv[3]
    generate_payment_request(client, amount, offer)
