<!-- Wave 6 | Owner: Founder | Arabic-first -->

# Command Sprint — Standard Terms / الشروط القياسية

**Purpose / الغرض:** الشروط القياسية لعرض Command Sprint من الدرجة الأولى في سُلّم Wave 6.

> مرجع السُّلّم الكامل والتسعير المعتمد: `docs/OFFER_LADDER_AND_PRICING.md`.
> تسعير Wave 6 التأسيسي أدناه خاص بأول 3 عملاء.

---

## Offer summary / ملخص العرض
| Item | Value |
|------|-------|
| Duration / المدة | **7 days / 7 أيام** |
| Founding price / السعر التأسيسي | **499–1,500 SAR** (أول 3 عملاء) |
| Payment / الدفع | يدوي الآن — دليل دفع يُسجّل في `data/revenue/payments.jsonl` |

## Deliverables / المخرجات
1. Revenue Map / خريطة الإيراد
2. Proof Register / سجل الإثبات
3. Approval Register / سجل الموافقات
4. Next Action Board / لوحة الإجراءات
5. Executive Command Brief / موجز تنفيذي
6. Proof Pack — انظر القالب: `docs/delivery/PROOF_PACK_TEMPLATE.md`
7. Upsell Recommendation / توصية التوسعة

## Data & approval rules / قواعد البيانات والموافقة
- no customer data for model training / لا بيانات عميل لتدريب نماذج.
- every external action requires founder approval / كل إجراء خارجي بموافقة المؤسس.
- no public case study without written approval / لا حالة نجاح علنية بدون إذن كتابي.

## What is NOT included / ما هو غير مشمول
- لا أتمتة إرسال خارجي (واتساب/بريد/LinkedIn).
- لا scraping أو شراء بيانات.
- لا ضمان إيراد — نلتزم بـ KPIs ومخرجات، لا بأرقام إيراد مضمونة.

## Next step / الخطوة التالية
- إرسال `sales/PROPOSAL_TEMPLATE.md` بعد موافقة المؤسس → تسجيل في `data/revenue/offers.jsonl`.
- عند `payment_status = paid` → `python scripts/create_customer_workspace.py --name <slug>`.
