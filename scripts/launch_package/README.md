# Launch Package — Approval-First Prospecting Helpers

سكربتات خفيفة بدون اعتماديات خارجية (Python stdlib فقط)، مأخوذة من حزمة الإطلاق
الخارجية ومواءمة لاصطلاحات الريبو ودستور Dealix. **لا ترسل أي رسالة، ولا تعمل
scraping، ولا تتصل بأي خدمة خارجية.** كل المخرجات قوائم مراجعة محلية يعتمدها
المؤسس يدويًا قبل أي تواصل.

> هذه السكربتات مسار سريع/مبسّط للمؤسس. **المسار الرسمي المحكوم داخل التطبيق
> يبقى** `POST /api/v1/leads` (intake + ICP + BANT + decision passport) و
> `/[locale]/ops/war-room` للتشغيل اليومي. راجع `docs/external/LAUNCH_PACKAGE_RECONCILIATION_AR.md`.

## التشغيل

```bash
# 1) قائمة تواصل قابلة للمراجعة (approval-first) من البذرة
python3 scripts/launch_package/dealix_daily_prospect_drafts.py

# 2) تقييم الحسابات (0-100) + الإجراء التالي اليدوي
python3 scripts/launch_package/dealix_lead_scoring.py

# 3) تقرير قيادة يومي (JSON) من الملف المُقيَّم
python3 scripts/launch_package/dealix_daily_command_center.py
```

- المدخل الافتراضي: `scripts/launch_package/sample_data/icp_seed_accounts_saudi.csv`
  (أمثلة فقط — استبدلها ببياناتك عبر `--input`).
- المخرجات تُكتب في `reports/launch_package/` (ليست ضمن git؛ تُولَّد عند التشغيل).
- بياناتك الحقيقية ضعها تحت `data/prospects/` (مُستثناة في `.gitignore`).

## الملفات

| الملف | الوظيفة |
| --- | --- |
| `dealix_daily_prospect_drafts.py` | يولّد قائمة تواصل بحالة `needs_founder_review` (لا إرسال) |
| `dealix_lead_scoring.py` | يقيّم CSV مزوّد من المؤسس (لا scraping) |
| `dealix_daily_command_center.py` | تقرير يومي JSON من الملف المُقيَّم |
| `sample_data/icp_seed_accounts_saudi.csv` | بذرة أمثلة (9 أعمدة) |
| `ICP_SEED_SCHEMA_AR.md` | مخطط الأعمدة وقواعد البيانات |

## قواعد الحوكمة (مفروضة في المخرجات)

- `no automated outbound` — لا إرسال آلي.
- `human approval before sending` — موافقة بشرية قبل أي إرسال.
- `use public/consented context only` — مصادر عامة/إذن فقط.

السياسة الكاملة: [`docs/compliance/OUTBOUND_AND_DATA_POLICY_AR.md`](../../docs/compliance/OUTBOUND_AND_DATA_POLICY_AR.md).
