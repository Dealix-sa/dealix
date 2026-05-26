import sys
import os
import json
import argparse
from datetime import datetime, timezone

PROD_FILE = os.path.join("data", "ledgers", "hermes_productization.json")

def check_gate(name, offer, paid_runs, proof_packs, retainers, repeat_uses, delivery_burden, demand_score):
    print("==========================================")
    print(" SOVEREIGN PRODUCTIZATION GATE EVALUATION ")
    print("==========================================")
    
    paid_runs = int(paid_runs)
    proof_packs = int(proof_packs)
    retainers = int(retainers)
    repeat_uses = int(repeat_uses)
    delivery_burden = int(delivery_burden)
    demand_score = int(demand_score)
    
    os.makedirs(os.path.dirname(PROD_FILE), exist_ok=True)
    if os.path.exists(OP_FILE := PROD_FILE):
        with open(OP_FILE, "r", encoding="utf-8") as f:
            try:
                prod_data = json.load(f)
            except Exception:
                prod_data = []
    else:
        prod_data = []
        
    gate_id = f"PRD-{datetime.now(timezone.utc).strftime('%m%d%H%M')}"
    
    # Logic checklist for SaaS transition
    # Rules: No SaaS before: 3 paid runs, 2 proof packs, 1 retainer
    is_saas_ready = paid_runs >= 3 and proof_packs >= 2 and retainers >= 1
    
    decision = "SELL_MORE_CONSULTING"
    rational = "Need to compile more active case studies and secure paid retainers to build the baseline truth."
    
    if is_saas_ready:
        if delivery_burden > 50:
            decision = "UNIFY_DELIVERY_WORKFLOW"
            rational = "Delivery burden is high (>50m per run). Build custom templates and generators before writing SaaS code."
        else:
            decision = "BUILD_SAAS_MVP"
            rational = "Sufficient validation secured. Low delivery burden enables rapid SaaS automation loop."
            
    new_gate = {
        "id": gate_id,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "offer": offer,
        "decision": decision,
        "rational": rational
    }
    prod_data.append(new_gate)
    with open(PROD_FILE, "w", encoding="utf-8") as f:
        json.dump(prod_data, f, indent=2, ensure_ascii=False)
        
    # Write MD report
    reports_dir = os.path.join("reports", "productization")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, f"productization-gate-{gate_id.lower()}.md")
    
    content = f"""# ⚙️ بوابة تعليب وتسويق المنتج (Sovereign Productization Gate) — {gate_id}
**الخدمة الخاضعة للتدقيق:** {offer}
**تاريخ التحليل:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

---

## 1. المدخلات والقياسات الحالية (Operating Metrics):
* **عدد دورات التشغيل المدفوعة:** {paid_runs} (المطلوب للمنتج: 3+)
* **عدد حزم الإثبات المسلمة:** {proof_packs} (المطلوب للمنتج: 2+)
* **عدد عقود الاستبقاء النشطة:** {retainers} (المطلوب للمنتج: 1+)
* **العبء التشغيلي لكل دورة فنية:** {delivery_burden} دقيقة

## 2. القرار النهائي المعتمد (The Sovereign Decision):
**القرار الحالي:** `{decision}`

## 3. مبررات القرار وخطة العمل (The Rational Roadmap):
{rational}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Productization Gate {gate_id} evaluated: {decision}.")
    print(f"Memo drafted at: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="AI Trust Diagnostic")
    parser.add_argument("--offer", default="AI Trust Diagnostic")
    parser.add_argument("--paid-runs", default="0")
    parser.add_argument("--proof-packs", default="0")
    parser.add_argument("--retainers", default="0")
    parser.add_argument("--repeat-uses", default="0")
    parser.add_argument("--delivery-burden", default="60")
    parser.add_argument("--demand-score", default="70")
    
    args = parser.parse_args()
    check_gate(args.name, args.offer, args.paid_runs, args.proof_packs, args.retainers, args.repeat_uses, args.delivery_burden, args.demand_score)
