# مراجعة قابلية التسليم — Deliverability Review

> قالب يُجمَّع من [data/outreach/email_accounts.jsonl](../../data/outreach/email_accounts.jsonl)
> وفق [schemas/email_account.schema.json](../../schemas/email_account.schema.json).
> كحالة: {{as_of}} — Asia/Riyadh.

## قائمة التحقق قبل أي إرسال
- [ ] SPF · [ ] DKIM · [ ] DMARC · [ ] دومين تتبع مخصص
- [ ] رابط إلغاء اشتراك (List-Unsubscribe بنقرة) · [ ] reply-to صحيح
- [ ] عنوان بريدي/هوية مرسل متوافقة · [ ] قائمة كبت فعّالة
- [ ] معالجة ارتداد · [ ] مراقبة معدل spam

## الحدود الصحية
| المؤشر | الحد | الحالة |
|---|---|---|
| bounce rate | < 3% | {{bounce}} |
| spam complaint rate | < 0.1–0.3% | {{spam}} |
| unsubscribe rate | مُراقب | {{unsub}} |
| positive reply rate | في تحسّن | {{pos}} |
| provider warnings | لا شيء | {{warn}} |

## الحسابات
| account_id | domain | spf | dkim | dmarc | warmup_stage | daily_cap | health |
|---|---|---|---|---|---|---|---|
| {{account}} | {{domain}} | ✓/✗ | ✓/✗ | ✓/✗ | {{stage}} | {{cap}} | {{health}} |

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
