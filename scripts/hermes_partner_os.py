import sys
import os
import json
from datetime import datetime, timezone

PARTNERS_FILE = os.path.join("data", "ledgers", "hermes_partners.json")
REPORTS_DIR = os.path.join("reports", "partners")

def add_partner(name, company, p_type, sector, trust, audience, offer_fit, potential_value, next_step):
    print("==========================================")
    print(" ADDING NEW SOVEREIGN CHANNEL PARTNER ")
    print("==========================================")
    
    os.makedirs(os.path.dirname(PARTNERS_FILE), exist_ok=True)
    if os.path.exists(PARTNERS_FILE):
        with open(PARTNERS_FILE, "r", encoding="utf-8") as f:
            try:
                partners = json.load(f)
            except Exception:
                partners = []
    else:
        partners = []
        
    new_partner = {
        "name": name,
        "company": company,
        "type": p_type,
        "sector": sector,
        "trust": trust,
        "audience": audience,
        "offer_fit": offer_fit,
        "potential_value": potential_value,
        "next": next_step
    }
    
    partners.append(new_partner)
    with open(PARTNERS_FILE, "w", encoding="utf-8") as f:
        json.dump(partners, f, indent=2, ensure_ascii=False)
        
    print(f"Partner '{name}' ({company}) successfully registered in B2B database.")

def build_report():
    print("==========================================")
    print(" COMPILING HERMES PARTNERS REPORT ")
    print("==========================================")
    
    if not os.path.exists(PARTNERS_FILE):
        print(f"Error: {PARTNERS_FILE} not found.")
        return
        
    with open(PARTNERS_FILE, "r", encoding="utf-8") as f:
        partners = json.load(f)
        
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filepath = os.path.join(REPORTS_DIR, f"partner-report-{datetime.now(timezone.utc).strftime('%Y%m%d')}.md")
    
    content = f"""# 🤝 تقرير الشركاء والموزعين المعتمدين (Hermes Partners Report) — {today}

## شبكة التوزيع الحالية
إجمالي الشركاء المسجلين: {len(partners)}

### تفاصيل الشركاء النشطين
"""
    for p in partners:
        content += f"* **{p.get('name')}** ({p.get('company')}) — Type: `{p.get('type')}` | Offer Fit: `{p.get('offer_fit')}` | Potential: `{p.get('potential_value')}` | Next Action: {p.get('next')}\n"
        
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[PASS] Partners report compiled successfully at: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        build_report()
    elif len(sys.argv) >= 10:
        add_partner(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10] if len(sys.argv) > 10 else "")
    else:
        # Fallback interactive parse
        # Sample add command wrapper
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["add", "report"])
        parser.add_argument("--name", default="Agency One")
        parser.add_argument("--company", default="Riyadh Ads")
        parser.add_argument("--type", default="agency")
        parser.add_argument("--sector", default="Marketing")
        parser.add_argument("--trust", default="new")
        parser.add_argument("--audience", default="SMB brands")
        parser.add_argument("--offer-fit", default="AI Trust Diagnostic")
        parser.add_argument("--potential-value", default="high")
        parser.add_argument("--next", default="send partner intro")
        
        args = parser.parse_args()
        if args.action == "add":
            add_partner(args.name, args.company, args.type, args.sector, args.trust, args.audience, args.offer_fit, args.potential_value, args.next)
        else:
            build_report()
