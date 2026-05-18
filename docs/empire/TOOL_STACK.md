# Tool Stack — مكدّس الأدوات

**الغرض:** أخف stack ممكن الآن. لا تشتري stack كبيراً قبل أول paid proof.

> القاعدة: ابدأ بالأخف. لا تقفز إلى مستوى قبل أن يثبت المستوى الذي قبله.

## مستويات التشغيل

| المستوى | متى | الأدوات |
|---------|-----|---------|
| **L1 — الآن** | قبل أول Proof Pack | Google Form · Sheet/Airtable · Apps Script · WhatsApp warm يدوي · email يدوي · فاتورة يدوية · Sample Proof Pack · Daily Scorecard |
| **L2 — بعد أول Proof Pack** | بعد إثبات واحد | Dealix API مربوط بالـ form · بطاقات تُولَّد آلياً · مسودة Proof Pack generator · dashboard · partner sheet |
| **L3 — بعد 3 pilots** | بعد تكرار | WhatsApp Cloud API (inbound) · opt-in registry · portal أساسي · Proof Pack generator · partner dashboard |
| **L4 — بعد 10 pilots** | عند طلب حقيقي | CRM · billing automation · CS automation · revenue analytics · benchmark engine |

## الأدوات حسب الفئة

| الفئة | ابدأ بـ | لاحقاً |
|-------|---------|--------|
| CRM / Pipeline | Sheet / Airtable / Notion | HubSpot · Pipedrive · Attio |
| Automation | Apps Script | n8n · Make · Temporal / Celery |
| Analytics | Plausible · GA4 | PostHog · Metabase |
| Observability | Sentry | OpenTelemetry · Prometheus/Grafana |
| Knowledge / RAG | Postgres + pgvector | Qdrant · LlamaIndex |
| Sales Enablement | One-pager · Sample Proof Pack | deck · procurement pack |
| Content | Canva · Google Docs | Typefully/Buffer · Beehiiv/ConvertKit |
| Billing | فاتورة Moyasar يدوية + تحويل بنكي + PDF | Stripe (إن احتجت عالمي) |
| Support | inbox بسيط | Crisp · Intercom · Zendesk |

## حدود الحوكمة (غير قابلة للتفاوض)

> أي automation خارجي = **approval-first**.

- لا **live charge** ولا auto-billing — فاتورة يدوية بعد اتفاق نطاق.
- لا **scraping** ولا mass DMs ولا cold WhatsApp.
- لا **PII خام** في اللوقز (هاتف، إيميل، secrets، PII غير مُقنّعة).
- n8n/Make للتدفقات الداخلية فقط — لا أفعال خارجية عالية المخاطر بلا موافقة.
- **No source = no answer** لأي إجابة داخلية أو Proof Pack.

تفاصيل: [TRUST_LAYER.md](TRUST_LAYER.md).

## ما يُقاس

risk score completions · sample Proof Pack downloads · diagnostic CTA clicks · booking conversion · مسار source → lead → demo.

## روابط ذات صلة

- [TRUST_LAYER.md](TRUST_LAYER.md) — حدود الثقة
- [DAILY_SCORECARD.md](DAILY_SCORECARD.md) — لوحة القياس اليومية
- [PRODUCTIZATION_PATH.md](PRODUCTIZATION_PATH.md) — متى تبني module
