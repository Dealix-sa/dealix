<!-- Layer: ops | Owner: Founder | Date: 2026-05-17 -->

# Founder Launch Action List — قائمة مهام الإطلاق للمؤسس

The daily operating engine (`content_os`) auto-drafts everything and runs the
daily loop. The code cannot do the steps below — only the founder can. The
engine stays safe (nothing sent, nothing charged) until these are done.

محرّك التشغيل اليومي (`content_os`) يصيغ كل شيء تلقائياً ويشغّل الحلقة اليومية.
الخطوات التالية لا يقدر الكود يسوّيها — المؤسس فقط. المحرّك يبقى آمناً (لا إرسال،
لا خصم) حتى تُنجَز هذه الخطوات.

---

## English

1. **Connect n8n.** Create an n8n instance and build one workflow per
   channel (LinkedIn, X) holding *your own* OAuth connections. Point its
   inbound webhook at the `social_post_approved` event. Set `N8N_WEBHOOK_URL`.
   Dealix never holds LinkedIn/X credentials — publishing is founder-owned.
2. **Keep the live gate OFF until verified.** Leave
   `SOCIAL_PUBLISH_ALLOW_LIVE=false` until n8n is connected and tested with a
   dummy post. Flip it to `true` only as a deliberate, audited decision.
3. **Provide consented contacts only.** Targeting runs on inbound /
   consented / founder-supplied lists. Never upload scraped or purchased
   data — it breaks PDPL and the doctrine.
4. **Schedule the daily engine.** Point an external scheduler (Railway
   scheduler / GitHub Actions / n8n cron) at
   `python scripts/dealix_daily_engine.py` or `POST /api/v1/automation/daily-engine/run`.
   It is idempotent per day.
5. **Work the queue every morning.** Open the digest, review the approval
   queue, click approve / edit / reject. Nothing is sent without your click.
6. **Wire the public form.** Connect the public intake form to
   `POST /api/v1/public/demo-request` — it auto-qualifies, routes to an offer
   rung, and drafts a proposal into the queue for your approval.

---

## العربية

1. **اربط n8n.** أنشئ n8n وابنِ workflow لكل قناة (LinkedIn، X) يحمل اتصالات
   OAuth *الخاصة بك*. وجّه الـ webhook لحدث `social_post_approved`، واضبط
   `N8N_WEBHOOK_URL`. Dealix لا يحمل بيانات اعتماد LinkedIn/X إطلاقاً — النشر
   مملوك للمؤسس.
2. **أبقِ بوابة النشر مغلقة حتى التحقق.** اترك
   `SOCIAL_PUBLISH_ALLOW_LIVE=false` حتى توصل n8n وتختبرها ببوست تجريبي. لا
   تحوّلها إلى `true` إلا كقرار متعمّد ومُوثّق.
3. **استخدم قوائم بموافقة فقط.** الاستهداف يعمل على قوائم واردة / بموافقة /
   مزوّدة منك. لا ترفع بيانات مكشوطة أو مشتراة — تخالف PDPL والدستور.
4. **جدوِل المحرّك اليومي.** وجّه مجدوِلاً خارجياً (Railway / GitHub Actions /
   n8n) إلى `python scripts/dealix_daily_engine.py` أو
   `POST /api/v1/automation/daily-engine/run`. المحرّك idempotent لكل يوم.
5. **اشتغل على الطابور كل صباح.** افتح الموجز، راجع طابور الموافقات، اضغط
   موافقة / تعديل / رفض. لا يُرسَل شيء بدون ضغطتك.
6. **اربط النموذج العام.** اربط نموذج الاستقبال العام بـ
   `POST /api/v1/public/demo-request` — يؤهّل تلقائياً، يوجّه إلى درجة عرض،
   ويصيغ عرضاً في الطابور لموافقتك.

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
