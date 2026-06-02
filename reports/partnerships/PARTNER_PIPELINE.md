# خط أنابيب الشركاء — Partner Pipeline

> قالب يُجمَّع من [data/partners/partners.jsonl](../../data/partners/partners.jsonl) وفق
> [schemas/partner.schema.json](../../schemas/partner.schema.json). كحالة: {{as_of}}.
> الشريك يملك علاقة العميل؛ Dealix يشغّل Revenue OS. كل صرف بموافقة المؤسس.

## النماذج
referral_fee · revenue_share · implementation_margin (نطاقات إرشادية، يضبطها المؤسس).

## الشركاء
| partner_id | name | type | fit_score | deal_split_model | status | owner |
|---|---|---|---|---|---|---|
| {{partner_id}} | {{name}} | {{type}} | {{fit}} | {{split}} | {{status}} | {{owner}} |

## دورة الحياة
identify → qualify (fit_score) → agree → enable → co-deliver → track.
المرجع: `auto_client_acquisition/partnership_os/`.

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
