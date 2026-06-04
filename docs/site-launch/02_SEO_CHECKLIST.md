# SEO Checklist — Dealix Public Website — قائمة تحقّق السيو

Per-page metadata, structured data, and link integrity for the Dealix website. Every entry must be verified before publish. No metadata may contain an unproven claim, a guarantee, or a value figure without the estimated-value disclosure.

## 1. Per-page metadata — وسوم كل صفحة

Each route ships a unique `title` (50–60 chars) and `description` (140–160 chars). Titles are bilingual where the page is bilingual.

| Route | Title (EN) | Description (EN) |
|---|---|---|
| `/` , `/en` | Dealix — AI Revenue & Operations OS for Saudi & GCC B2B | Governed AI that drafts, ranks, and recommends revenue and operations work. The founder reviews and approves. The system never sends externally. |
| `/commercial` | Dealix Commercial — Engagements & Offer Ladder | How Dealix engagements work: workflow audit, pilot, department OS, and retainer. Approval-first, human-in-the-loop. |
| `/services` | Dealix Services — Audit, Pilot, Department OS | Service scope across the offer ladder. Concrete deliverables, no blind automation, founder-reviewed output. |
| `/pricing` | Dealix Pricing — Offer Ladder in SAR | Audit, pilot, department OS, retainer, and enterprise tiers in SAR. Scope per tier, no hidden automation. |
| `/trust` | Dealix Trust — Approval-First, Human-in-the-Loop | How Dealix governs AI: drafts only, founder approval, PDPL-aware handling, no external sending by the system. |
| `/launch` | Dealix Launch Status — What Is Live | What is live and what is review-only. Transparent launch posture for Saudi and GCC B2B teams. |
| `/contact` | Contact Dealix — Request Audit or Diagnostic | Request an AI workflow audit or book a paid diagnostic. Intake routes to founder review. |
| `/status` | Dealix Status — System & Service Health | Current status of Dealix services and the public site. |
| `/verticals` | Dealix Verticals — Five Saudi B2B Sectors | Workflow patterns for FM, contracting, real estate ops, legal services, and consulting. |
| `/verticals/facilities-management` | Dealix for Facilities Management | AI workflow patterns for facilities management revenue and operations in Saudi and GCC. |
| `/verticals/contracting-project-controls` | Dealix for Contracting & Project Controls | AI workflow patterns for contracting and project controls. Founder-reviewed, no blind automation. |
| `/verticals/real-estate-property-ops` | Dealix for Real Estate & Property Ops | AI workflow patterns for real estate and property operations teams. |
| `/verticals/legal-professional-services` | Dealix for Legal & Professional Services | AI workflow patterns for legal and professional services firms. Approval-first handling. |
| `/verticals/consulting-training-b2b` | Dealix for Consulting & B2B Training | AI workflow patterns for consulting and B2B training providers. |
| `/case-method` | Dealix Case Method — Case-Safe Outcomes | How Dealix documents outcomes without overclaiming. Estimated value is not Verified value. |
| `/media` | Dealix Media & Social Planning | Media posture and social calendar planning. Manual posting, no automated sending. |
| `/faq` | Dealix FAQ — How Engagements Work | Common questions, including the governing rule: the system never sends externally. |

AR titles/descriptions mirror the EN entries in the copy deck (`03_COPY_DECK_AR_EN.md`), one-to-one, equal length.

## 2. OpenGraph — أوبن غراف

- [ ] `og:title`, `og:description`, `og:type` (`website`), `og:url` (canonical), `og:image` per page.
- [ ] `og:locale` = `ar_SA` for `/` and verticals; `og:locale:alternate` = `en_US`. Reverse for `/en`.
- [ ] OG image: 1200×630, no unproven claim baked into the image text.

## 3. Twitter / X card — بطاقة تويتر

- [ ] `twitter:card` = `summary_large_image`.
- [ ] `twitter:title`, `twitter:description`, `twitter:image` mirror OG values.

## 4. sitemap.xml — خريطة الموقع

- [ ] All 18 public routes present in `apps/web/app/sitemap.ts`.
- [ ] `alternates.languages` set for AR (`ar-SA`) and EN (`en-US`) on each bilingual route.
- [ ] Internal ops surfaces excluded.
- [ ] `lastModified`, `changeFrequency`, `priority` set sensibly (home highest).

## 5. robots.txt — روبوتس

- [ ] `apps/web/app/robots.ts` allows all public routes, disallows `/api/`, `/_next/`, `/healthz`, and internal ops surfaces.
- [ ] AI training crawlers (GPTBot, CCBot, anthropic-ai) handled per current policy.
- [ ] `sitemap` and `host` point to the live domain.

## 6. Canonical — الرابط الأساسي

- [ ] Every page declares a self-referential canonical URL.
- [ ] AR/EN counterparts use `hreflang` (`ar-SA`, `en-US`, `x-default`) in `alternates.languages`.

## 7. JSON-LD structured data — البيانات المنظمة

- [ ] **Organization** on home: name "Dealix", URL, logo, `sameAs` profiles, `areaServed` Saudi Arabia and GCC.
- [ ] **WebSite** on home, with `inLanguage` `ar-SA` and `en-US`.
- [ ] **Service** on `/services` and each vertical page: service name, provider (Organization), `areaServed`, no price guarantee — list offer tiers as `OfferCatalog` with SAR ranges.
- [ ] **FAQPage** on `/faq`: each Q/A mirrors visible copy; no guaranteed-outcome answers.
- [ ] **BreadcrumbList** on nested routes (`/verticals/*`): home → verticals → sector.

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Dealix AI Workflow Audit",
  "provider": { "@type": "Organization", "name": "Dealix" },
  "areaServed": ["SA", "GCC"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Dealix Offer Ladder",
    "itemListElement": [
      { "@type": "Offer", "name": "Audit", "priceCurrency": "SAR", "price": "499-2500" },
      { "@type": "Offer", "name": "Pilot", "priceCurrency": "SAR", "price": "5000-25000" }
    ]
  }
}
```

## 8. Multilingual AR/EN — تعدد اللغات

- [ ] `<html lang>` correct per locale (`ar` with `dir="rtl"` on AR, `en` on EN).
- [ ] hreflang pairs reciprocal and validated.
- [ ] AR and EN content reach parity before a route is indexed as Ready.

## 9. Internal links & integrity — الروابط الداخلية والسلامة

- [ ] Every CTA links to a real route in the page map.
- [ ] No broken internal links; no dangling anchors.
- [ ] Cross-links between verticals index and each sector page resolve.
- [ ] No external link implies Dealix sends messages on a customer's behalf.

## 10. Claim safety — سلامة الادعاءات

- [ ] No "guaranteed ROI", "100%", "replace your team", "automate everything", "no human needed", or fake urgency in any tag or visible copy.
- [ ] Any value figure carries: "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Related — روابط

- `docs/site-launch/01_PAGE_MAP.md`
- `docs/05_governance_os/CLAIM_SAFETY.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
