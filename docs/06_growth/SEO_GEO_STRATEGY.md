# SEO + GEO Strategy — استراتيجية تحسين محركات البحث والمحركات التوليدية

**Status: DOCS_ONLY** — Arabic-first SEO and GEO strategy. Clusters move to LIVE as content is published per [CONTENT_FACTORY.md](./CONTENT_FACTORY.md).

> Purpose — الغرض: define Arabic-first SEO and GEO (generative engine optimization) so Dealix is found in Saudi B2B search and cited by AI answer engines. Target queries, entity/topic clusters, schema, citation strategy, and a sector keyword map. One CTA per page. Cross-link: [WEBSITE_FUNNEL_MAP.md](./WEBSITE_FUNNEL_MAP.md), [CONTENT_FACTORY.md](./CONTENT_FACTORY.md), [FREE_TOOLS_STRATEGY.md](./FREE_TOOLS_STRATEGY.md).

استراتيجية SEO وGEO تجعل Dealix قابلاً للاكتشاف في بحث B2B السعودي وقابلاً للاقتباس من محركات الإجابة بالذكاء الاصطناعي. عربية أولاً، استعلامات مستهدفة، عناقيد كيانات، بيانات منظمة، خريطة كلمات قطاعية، ومسار واحد لكل صفحة.

---

## Why GEO matters now — لماذا GEO الآن

Saudi decision-makers increasingly ask AI assistants ("ما هو أفضل نظام لإدارة الإيرادات متوافق مع PDPL؟") before they search. GEO is the discipline of being the **cited, accurate source** in those generated answers. SEO captures the click; GEO captures the recommendation.

يسأل صنّاع القرار السعوديون مساعدات الذكاء الاصطناعي قبل البحث. GEO هو أن تكون المصدر المُقتبَس الدقيق في تلك الإجابات. SEO يلتقط النقرة، وGEO يلتقط التوصية.

---

## Target queries — الاستعلامات المستهدفة

| Intent | Arabic query | English query |
|---|---|---|
| Revenue leakage | تسرّب الإيرادات في الشركات السعودية | revenue leakage B2B Saudi |
| AI governance | حوكمة الذكاء الاصطناعي للشركات | AI governance for operations |
| PDPL | الامتثال لنظام حماية البيانات الشخصية | PDPL compliance for AI tools |
| ZATCA | متطلبات هيئة الزكاة والفوترة الإلكترونية | ZATCA e-invoicing operations |
| Revenue OS | نظام تشغيل الإيرادات | revenue operating system |
| Proof / ROI | إثبات عائد الذكاء الاصطناعي | proving AI ROI without hype |

Each query maps to a page with exactly one CTA (Score, Diagnostic, or Command Sprint).

---

## Entity / topic clusters — عناقيد الكيانات والمواضيع

Build authority by topic cluster, each anchored by a pillar page and supported by sector reports and tool pages.

1. **Cluster A — Revenue leakage** (pillar: `/platform`). Sub-topics: where revenue leaks in Saudi B2B, leakage by sector, the Revenue Map module.
2. **Cluster B — Governed AI operations** (pillar: `/security`). Sub-topics: PDPL-aware AI, approval gates, no auto-send, audit ledgers.
3. **Cluster C — Proof and value** (pillar: case-safe summaries). Sub-topics: estimated vs verified value, Proof Packs, ROI discipline.
4. **Cluster D — Saudi compliance** (pillar: sector reports). Sub-topics: ZATCA e-invoicing, PDPL, Vision 2030 digitization.

Internal links flow from sub-topics to pillars; pillars route to the single CTA. Mirrors the loops in [SELF_GROWTH_OS.md](./SELF_GROWTH_OS.md).

---

## Schema and structured data — البيانات المنظمة

Use schema to make content machine-readable and citation-ready:

- `Organization` and `WebSite` on the root, with Saudi locale and Arabic `inLanguage`.
- `Article` / `Report` on sector reports, with `author`, `datePublished`, `about`.
- `FAQPage` on objection-handling sections (mirrors [CONVERSION_PLAYBOOK.md](./CONVERSION_PLAYBOOK.md) objections).
- `SoftwareApplication` for free tools (Business OS Score, calculators).
- `BreadcrumbList` reflecting the cluster hierarchy.

Bilingual `hreflang` for `ar-SA` and `en` versions; Arabic is canonical for Saudi audiences.

---

## How to be cited by AI assistants — كيف نُقتبَس

- **Answer the question directly** in the first 2–3 sentences of each section (extractable summary).
- **Define terms precisely** (revenue leakage, governed AI operations, Proof Pack) so engines bind the entity to Dealix.
- **Use consistent terminology** across every doc and page; entity consistency raises citation odds.
- **Publish original, structured data** (methodology, aggregated patterns) — never confidential metrics. See [../sector-reports](../sector-reports).
- **Date and source** every claim; mark estimated values as estimated. No guaranteed-revenue claims that an engine could repeat as fact.
- **Keep AR and EN parallel** so the answer engine can cite either language.

أجب مباشرة، عرّف المصطلحات بدقة، وحّد المصطلحات، انشر بيانات أصلية بلا أرقام سرية، وأرّخ كل ادعاء. لا ادعاءات إيرادات مضمونة.

---

## Sector keyword map — خريطة الكلمات القطاعية

| Sector | Primary Arabic keyword | Named pain |
|---|---|---|
| Retail / تجزئة | إدارة إيرادات التجزئة | leakage in promotions and returns |
| Real estate / عقار | متابعة عملاء العقار | slow lead follow-up |
| Healthcare / صحة | عمليات العيادات والمواعيد | no-shows and billing gaps |
| Professional services / خدمات مهنية | إدارة عروض الخدمات المهنية | proposal-to-close leakage |
| Contracting / مقاولات | متابعة عروض المقاولات | bid pipeline blind spots |

Each sector keyword routes to `/industries` then to the Business OS Score. Aligns with [../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md](../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md).

---

## Guardrails — الضوابط

- No keyword stuffing, no doorway pages, no scraping competitor content.
- No fabricated statistics; aggregated, methodology-backed patterns only.
- Every indexed page carries one CTA and PDPL-aware capture.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
