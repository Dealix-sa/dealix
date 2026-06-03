# Dealix Revenue Execution OS — طبقة التصريف (Distribution)

طبقة تشغيلية فوق Revenue OS تحوّل Dealix إلى **مكينة تصريف منتجات يومية**: قابلة
للقياس، آمنة، ومبنية على **موافقات وأدلة** — بدون أن تتحول إلى spam bot أو agent خطير.

> القاعدة الأم: **كل المخرجات مسودات. لا إرسال خارجي تلقائي. الموافقة والإرسال يدويان.**
> `operating_mode = draft_only_no_auto_send`

## التدفق اليومي

```
prospects → drafts → quality gate → queue → follow-ups
         → proposals → proof packs → payment handoff → renewals
         → metrics → win/loss → founder summary
```

أمر واحد يشغّل السلسلة كاملة:

```bash
make distribution-day      # python scripts/distribution_day.py
# يطبع: DEALIX_DISTRIBUTION_DAY=PASS|FAIL ويكتب reports/distribution/DISTRIBUTION_DAY.md
```

## الوثائق

| الوثيقة | الموضوع |
| --- | --- |
| [PRODUCT_DISTRIBUTION_OS_AR.md](PRODUCT_DISTRIBUTION_OS_AR.md) | النظرة الكاملة + المعمارية + الأوامر |
| [CHANNEL_POLICY_AR.md](CHANNEL_POLICY_AR.md) | سياسة القنوات (ما هو مسموح/ممنوع لكل قناة) |
| [SECTOR_PRIORITIZATION_AR.md](SECTOR_PRIORITIZATION_AR.md) | تحديد أولوية القطاعات + بوابة الدخول |
| [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) | مواصفة مصنع المسودات |
| [DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md) | دليل الموافقة والإرسال اليدوي |
| [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) | سياسة بوابة الجودة |
| [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) | محرك المتابعة |
| [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) | مصنع العروض (من كتالوج العروض الرسمي) |
| [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md) | مصنع أطقم الإثبات + مستويات الأدلة |
| [PAYMENT_HANDOFF_AR.md](PAYMENT_HANDOFF_AR.md) | تسليم الدفع (لا رابط دفع تلقائي) |
| [RENEWAL_ENGINE_AR.md](RENEWAL_ENGINE_AR.md) | محرك التجديد والـ upsell |
| [WIN_LOSS_LEARNING_AR.md](WIN_LOSS_LEARNING_AR.md) | تعلّم الربح/الخسارة |
| [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) | لوحة مؤشرات القمع |

## الكود

- المنطق المُختبَر: `dealix/distribution/` (package)
- أوامر CLI رفيعة: `scripts/*.py` (تُستدعى عبر Makefile)
- المخططات: `schemas/*.schema.json`
- بيانات الإعداد/الأمثلة: `data/distribution/` (مُتعقّبة) — السجلات الزمنية `data/<type>/*.jsonl` (متجاهَلة)
- الاختبارات: `tests/test_distribution_os.py`

## الحوكمة (غير قابل للتجاوز)

يعيد استخدام نفس non-negotiables المطبّقة في كل المستودع
(`auto_client_acquisition/safe_send_gateway`) ومستويات الأدلة L0–L5
(`auto_client_acquisition/proof_engine/evidence`):

- لا cold WhatsApp · لا أتمتة LinkedIn · لا scraping · لا تواصل جماعي
- لا وعود مضمونة · لا إثبات مزيّف · لا إرسال خارجي بدون موافقة
- لا upsell قبل Proof · أي استخدام عام للأدلة يتطلب L4 + موافقة صريحة
