# AI Search & GEO Strategy — Dealix Self-Growth OS

استراتيجية الظهور في البحث التقليدي **و** في إجابات الذكاء الاصطناعي
(Answer Engines / GEO / AIO). الجيل الجديد من البحث يتجه إلى **إجابات**،
لا روابط فقط — لذلك Dealix يكتب محتوى **structured وواضح** تفهمه محركات
البحث وAI answers.

---

## 1. Technical SEO (صحيح من البداية)

أساسيات Google Search Central التي نبنيها لكل صفحة قطاعية ومنتجية:

- `<title>` + meta description موجّهة للقطاع.
- canonical URL.
- hreflang **ar/en** متبادل بين النسختين (صفحات متعددة اللغات).
- structured data (Service / FAQPage) صحيحة وقابلة للتحقق.
- إدراج الصفحة في `sitemap.xml`.
- `robots.txt` يسمح بالزحف.
- Search Console للمراقبة.

> مولّد بنية الصفحات القطاعية يضمّن هذه القائمة في كل brief:
> `python3 scripts/growth/generate_sector_pages.py`
> → [`reports/growth/sector_pages/`](../../reports/growth/sector_pages/).

الصفحات القطاعية ليست صفحات شكلية — تُبنى تقنيًا صحيحة لتجلب بحثًا مستهدفًا.

---

## 2. GEO / AIO — الظهور داخل إجابات AI

اكتب محتوى بصيغة **سؤال/جواب** واضحة تستطيع نماذج الإجابة اقتباسها:

- ما هو نظام تشغيل الأعمال (Business OS)؟
- ما الفرق بين CRM وBusiness OS؟
- ما هو Command Sprint؟
- ما هو Proof OS / Proof Register؟
- ما معنى Revenue Leakage؟
- ما معنى Approval-first AI؟
- كيف تعرف أن شركتك تضيع فرصًا؟

ظهور العلامة داخل إجابات AI يتأثر **باتساق الرسالة عبر القنوات والمحتوى**؛
التشتت بين الفرق والقنوات يضعف الظهور. لذلك:

- رسالة واحدة متسقة: *Saudi AI Business Operating System, Approval-first*.
- نفس التعريفات في كل صفحة وبوست ووثيقة.
- مصطلحات ثابتة: Command Sprint, Proof Register, Business OS Score.

---

## 3. كلمات/مواضيع مستهدفة

Saudi AI Business OS · Revenue OS Saudi · Proof Pack للشركات ·
AI Governance للشركات · business operating rhythm · واتساب والمبيعات B2B.

> **لا نخترع أحجام بحث.** قوائم الكلمات تُستخدم كمواضيع للمحتوى؛ أي
> ترتيب أولوية حسب حجم البحث يحتاج مصدر بيانات حقيقي (Search Console /
> Bing Webmaster / مزوّد معتمد) أو مراجعة بشرية.

---

## 4. Benchmark Reports (سلطة)

تقارير دورية مثل: *Saudi B2B Follow-up Leakage Report* · *Proof Gap Report*
· *AI Business OS Readiness Report* · *WhatsApp-to-Revenue Operations Report*.

وسم إلزامي على أي تقرير:

> *Based on observed public signals and founder-led diagnostics.
> Not a statistical national survey.*

لا أرقام مُختلقة؛ البيانات الأولية من diagnostics ومراجعات عامة فقط، موسومة بوضوح.

---

## 5. الربط بالبنية الحالية

يوجد في الريبو مدقق SEO تقني ([`scripts/seo_audit.py`](../../scripts/seo_audit.py))
وتقرير ([`docs/SEO_AUDIT_REPORT.json`](../SEO_AUDIT_REPORT.json)) وتقويم GEO
([`docs/GEO_CONTENT_CALENDAR.md`](../GEO_CONTENT_CALENDAR.md)). استخدمها بدل
بناء أدوات موازية؛ هذا الملف يضيف الطبقة الاستراتيجية وربط الصفحات القطاعية.
