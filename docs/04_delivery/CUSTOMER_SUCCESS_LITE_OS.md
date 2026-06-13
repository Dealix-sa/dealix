<!-- Wave 6 | Owner: Founder | Arabic-first -->

# Customer Success Lite OS — نظام نجاح العميل المبسّط

**Purpose / الغرض:** بعد أول عميل، فكّر في **retention**، لا فقط البيع التالي.

> Data: `data/customers/customer_health.jsonl` · Brief: `reports/customers/customer_health_brief.md`

---

## Track per customer / تتبّع لكل عميل
- customer / العميل
- current offer / العرض الحالي
- value delivered / القيمة المسلّمة
- proof level / مستوى الإثبات
- open blockers / معوّقات مفتوحة
- next action / الإجراء التالي
- renewal risk / خطر التجديد
- expansion opportunity / فرصة التوسعة
- referral opportunity / فرصة الإحالة

---

## Customer Health Score (100 points) / درجة صحة العميل

| المحور / Axis | النقاط |
|---------------|--------|
| Proof Pack reviewed | 20 |
| Next action agreed | 20 |
| Customer sees value | 20 |
| Follow-up scheduled | 15 |
| Upsell fit | 15 |
| Referral potential | 10 |

### Bands / النطاقات
- **80–100** → Healthy → اطرح Upsell/Referral.
- **55–79** → Watch → ثبّت القيمة وحدد follow-up.
- **< 55** → At risk → عالج المعوّقات فورًا.

## Record schema / مخطط السجل
```
customer:               
current_offer:          
value_delivered:        
proof_level:            
health_score:           (0-100)
open_blockers:          
next_action:            
renewal_risk:           low | medium | high
expansion_opportunity:  
referral_opportunity:   
date:                   
```

> لا أسماء عملاء علنية بدون إذن · لا ضمان نتائج · القيمة مبنية على إثبات حقيقي.
