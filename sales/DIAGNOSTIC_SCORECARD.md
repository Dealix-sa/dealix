<!-- Wave 6 | Owner: Founder | Arabic-first -->

# Diagnostic Scorecard — بطاقة تقييم التشخيص

**Rule / القاعدة:** قدّم عرض Command Sprint **فقط إذا المجموع ≥ 70**.

> النتيجة تُسجّل في `data/revenue/diagnostics.jsonl` (الحقول: `score`, `top_blockers`,
> `os_fit`, `sprint_fit_score`, `outcome`, `no_fit_reason`).

---

## Scoring (100 points) / التسجيل

| المحور / Axis | النقاط | الدرجة |
|---------------|--------|--------|
| ألم واضح / clear pain | 25 |  |
| صاحب قرار موجود / decision-maker present | 20 |  |
| عنده عروض/فرص/تسليم / has offers-pipeline-delivery | 20 |  |
| يقدر يدفع Sprint / can pay for sprint | 15 |  |
| عنده بيانات أولية / has initial data | 10 |  |
| يقبل human-approved AI | 10 |  |
| **Total** | **100** |  |

## Decision / القرار
- **≥ 70** → Command Sprint offer (`sales/COMMAND_SPRINT_TERMS.md`).
- **50–69** → Nurture (متابعة + نموذج Proof Pack).
- **< 50** → Not fit (وضّح `no_fit_reason`).
- خارج النطاق → Partner path.

## Outcome record / سجل النتيجة
```
company:          
date:             
score:            (0-100)
top_blockers:     [b1, b2, b3]
os_fit:           
sprint_fit_score: 
outcome:          not_fit | nurture | command_sprint_offer | partner_path
no_fit_reason:    (if not_fit)
```

> لا ادعاءات مضمونة · لا أرقام مخترعة · كل معوّق مبني على ما قاله العميل.
