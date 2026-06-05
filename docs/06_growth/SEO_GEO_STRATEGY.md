# SEO + GEO Strategy — البحث ومحركات الإجابة

> Arabic-first SEO + GEO (Generative Engine Optimization for AI answer engines). We build
> **structure and clarity** so machines and people understand Dealix — never ranking tricks.
> **We never promise rankings.** Coordinate structure with `seo-geo-agent`. Status: `DOCS_ONLY`.

## المبدأ (Principle)

GEO and SEO win on the same thing: a clear, evidence-backed answer to a real Arabic business
question, structured so both Google and AI answer engines can quote it safely. No cloaking, no
keyword stuffing, no doorway pages, no link schemes.

## خريطة المحتوى (Content map)

| Cluster | Core query intent | Lands on | Primary CTA |
|---------|-------------------|----------|-------------|
| Category education | "ما هو AI Business Operating System؟" | Learn / category page | Get Business OS Score |
| Sector pages | "AI للعقار / خدمات B2B / العيادات" | `verticals.html`, sector diagnostics | Book Diagnostic |
| Pain-led | "تنظيم العملاء المحتملين / متابعة العروض" | Learn articles | Book Diagnostic |
| Governance/PDPL | "PDPL B2B السعودية" | `landing/blog/saudi-pdpl-b2b-2026.html`, Trust | Book Diagnostic |
| FAQ | "كم تكلفة / كيف تعمل Dealix" | FAQ page | Get Business OS Score |
| Proof patterns | anonymized outcome patterns | Proof Pack | Book Diagnostic |

## الميتاداتا (Metadata plan)

- Unique, Arabic-first `<title>` (≤60 chars) + `description` (≤155) per page; English mirror where bilingual.
- `<link rel="canonical">` on every page (the lead-score tool already does this — apply repo-wide).
- Open Graph + Twitter card per page; `og:locale` = `ar_SA`, alternate `en`.
- One H1 per page; descriptive H2/H3 matching real questions.

## البيانات المنظّمة JSON-LD (Structured data)

Implement, validated, never falsified:

- `Organization` (Dealix) — sitewide.
- `WebSite` + `SearchAction`.
- `FAQPage` — on FAQ + sector pages (real Q&A only).
- `Article` — on Learn/blog (author = founder, datePublished).
- `Service` — for Command Sprint and ladder rungs (price in SAR where public).
- `BreadcrumbList` — sector and Learn hierarchies.
- `Product`/`Review` — **only** when backed by approved Proof Packs; never fabricate aggregateRating.

## hreflang + sitemap

- `hreflang` pairs: `ar-SA` ↔ `en` with `x-default` → Arabic.
- `sitemap.xml` segmented (pages, learn, sector, tools); submit; keep lastmod accurate.
- `robots.txt`: allow indexable surfaces; disallow checkout/dashboard/internal.

## صفحات القطاعات وFAQ (Sector + FAQ pages)

- One sector page per ICP vertical (B2B services first, real estate, clinics next), each with:
  sector-specific pain, anonymized pattern (hypothesis-framed if no Proof Pack yet), FAQ block,
  one Diagnostic CTA.
- FAQ answers are quotable, ≤3 sentences, evidence-backed or hypothesis-framed.

## GEO (AI answer engines)

- Write definitional, extractable paragraphs ("Dealix is a Saudi-first AI Business Operating
  System that turns scattered WhatsApp/Excel/meetings into one governed operating rhythm").
- Keep claims attributable and dated so engines cite safely.
- Maintain a consistent entity description across all pages (no contradictory positioning).

## ما لا نفعله (What we never do)

- Never promise or imply guaranteed rankings or traffic.
- No fake reviews, fake FAQ, fake schema, scraped content, or auto-generated thin pages.

## خطة 30 يوم (30-day plan)

1. Audit canonical + metadata coverage; fill gaps on top 20 pages.
2. Add `Organization`, `WebSite`, `FAQPage`, `Article` JSON-LD to templates.
3. Build/repair `sitemap.xml` + `hreflang` ar/en + `x-default`.
4. Publish the B2B-services sector page + FAQ (one Diagnostic CTA), coordinated with `seo-geo-agent`.
5. Write one clean category-definition page optimized for GEO extraction.
