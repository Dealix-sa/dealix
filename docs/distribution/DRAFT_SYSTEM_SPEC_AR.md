# Dealix Draft System — مواصفة مصنع المسودات

`dealix/distribution/drafts.py` · CLI: `scripts/generate_distribution_drafts.py` ·
Make: `make distribution-drafts`

## ماذا يفعل
- يقرأ prospects (مصدرها المؤسس: referral / inbound / network / event — لا scraping).
- يحمّل قالب القطاع من `data/templates/distribution/{sector}_ar.md` (أو `_default_ar.md`).
- يملأ `{company}` و`{pain}`، ثم **يفحص الحوكمة وعبارات الادعاء الممنوعة قبل الكتابة**.
- يكتب draft واحد لكل prospect في `data/drafts/drafts.jsonl`.
- **idempotent:** لا يكرّر مسودة لنفس prospect طالما لها draft مفتوح.

## بنية الـ draft
يطابق `schemas/draft.schema.json`:
```
id, prospect_id, company, sector, channel, language="ar",
body, evidence_level=0, policy="draft_only_no_auto_send",
status="draft_pending_approval", created_at
```

## الحالات
```
draft_pending_approval → approved → copied_manual_send
                       ↘ rejected
```
الانتقالات صريحة وبشرية فقط:
```python
from dealix.distribution import drafts
drafts.approve_draft(draft_id)
drafts.reject_draft(draft_id, "off-ICP")
drafts.mark_copied(draft_id)   # نسخ يدوي للإرسال — ليس إرسالًا تلقائيًا
```

## القيود (تُفرض في الكود)
- يستدعي `assert_distribution_safe()` (نفس non-negotiables المطبّقة بالاختبارات).
- يرفض أي عبارة في `BANNED_CLAIM_PHRASES` (نضمن/مضمون/إرسال جماعي…).
- المخرجات مسودات فقط — لا إرسال.
