# Dealix Proposal Factory — مصنع العروض

`dealix/distribution/proposals.py` · CLI: `scripts/generate_proposal_draft.py` ·
Make: `make proposal-drafts`

> التسعير والنطاق والمدة **تُسحب من كتالوج العروض الرسمي** `os/03_OFFERS.yml` عبر
> `dealix/distribution/offers.py`. لا أرقام مخترعة هنا.

## المنطق
- يولّد عرضًا لكل prospect حالته `qualified` أو `proposal` (dedupe لكل prospect).
- `offer_ref` يأتي من القطاع (`sectors.yaml`) → ثم تفاصيل العرض من الكتالوج.
- يبدأ `draft_pending_approval` — لا التزام تعاقدي ولا دفع بدون موافقة.

## بنية العرض
يطابق `schemas/proposal.schema.json`:
```
id, prospect_id, company, sector, offer_ref, problem, scope[],
timeline_days, price_range_sar, evidence_level,
assumptions[], risks[], status, created_at
```

## سلّم العروض (من الكتالوج الرسمي)
يتبع `natural_next_offer` في `os/03_OFFERS.yml`، مثال:
```
ai_workflow_audit → agentic_workflow_pilot → … → ai_ops_retainer → department_expansion
```
أداة مساعدة:
```python
from dealix.distribution.offers import upsell_ladder, price_range_sar, get_offer
upsell_ladder("ai_workflow_audit")
price_range_sar(get_offer("ai_workflow_audit"))
```

## الموافقة
```python
from dealix.distribution.proposals import approve_proposal
approve_proposal(proposal_id)   # شرط لإنشاء مسودة تسليم الدفع
```

> ملاحظة: المخاطر تتضمن صراحةً «لا أرقام أو وعود مضمونة — القيمة تُثبت بالـ Proof».
