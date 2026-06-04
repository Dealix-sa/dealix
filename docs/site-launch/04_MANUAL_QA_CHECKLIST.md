# Manual QA Checklist — Dealix Public Website — قائمة الفحص اليدوي

The human review the founder runs before publishing the website. Every box is a manual check. Do not publish with any open P0 box unless explicitly risk-accepted and recorded.

## 1. Content & claims — المحتوى والادعاءات

- [ ] Hero EN and AR match the approved copy deck exactly.
- [ ] No forbidden claim anywhere: "guaranteed ROI", "100%", "replace your team", "automate everything", "no human needed", fake urgency / countdowns.
- [ ] No page describes scraping, cold WhatsApp, LinkedIn automation, or bulk outreach as a service.
- [ ] Every page with a value figure shows: "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
- [ ] The governing rule appears on home, `/trust`, and `/faq`.
- [ ] Offer ladder prices in SAR match the copy deck (Audit 499–2,500; Pilot 5,000–25,000; Department OS 25,000–150,000; Retainer 3,000–25,000/mo; Enterprise 150,000+).

## 2. Bilingual parity — التكافؤ اللغوي

- [ ] Each AR section has a matching EN section of equal structure and length.
- [ ] AR renders right-to-left; numerals and SAR figures display correctly.
- [ ] No untranslated placeholder or lorem text on either locale.
- [ ] Language switch between `/` and `/en` lands on the equivalent page.

## 3. Routes & navigation — المسارات والتنقل

- [ ] All 18 routes load without error (200), AR and EN where applicable.
- [ ] Three CTAs (Request AI Workflow Audit, Book Diagnostic, Start Pilot) all route to founder-reviewed intake.
- [ ] No CTA triggers any external send. Form submit creates a review item only.
- [ ] Verticals index links to all five sector pages; each sector links back.
- [ ] No broken internal links; no dangling anchors.

## 4. SEO surface — سطح السيو

- [ ] `/robots.txt` and `/sitemap.xml` reachable and correct.
- [ ] Each page has unique title and description.
- [ ] OpenGraph and Twitter card render correctly in a link preview.
- [ ] Canonical and hreflang pairs validated (`ar-SA`, `en-US`, `x-default`).
- [ ] JSON-LD (Organization, WebSite, Service, FAQPage, BreadcrumbList) validates with no errors and no overclaim.

## 5. Forms & intake — النماذج والاستقبال

- [ ] Contact form validates required fields in AR and EN.
- [ ] Submission produces a founder review item; no auto-reply that implies the system sent on the customer's behalf.
- [ ] No unnecessary personal data captured or logged.
- [ ] Confirmation message sets a human follow-up expectation, not an automated one.

## 6. Visual & responsive — العرض والاستجابة

- [ ] Renders on mobile, tablet, desktop without overflow or clipped AR text.
- [ ] Images have alt text in the page language.
- [ ] No emoji in headings or body copy.
- [ ] Contrast and font sizes readable for both scripts.

## 7. Performance & integrity — الأداء والسلامة

- [ ] Pages load within an acceptable time on a typical mobile connection.
- [ ] No console errors on any public route.
- [ ] `/status` reachable and accurate.
- [ ] 404 page exists and offers a route back to home.

## 8. Final gate — البوابة النهائية

- [ ] Founder has personally read every published page in AR and EN.
- [ ] Cross-checked against `docs/launch-control/02_GO_NO_GO_MATRIX.md`.
- [ ] Publish decision recorded with date and owner.

## Related — روابط

- `docs/site-launch/02_SEO_CHECKLIST.md`
- `docs/launch-control/02_GO_NO_GO_MATRIX.md`
- `docs/ops/COMMERCIAL_GO_LIVE_GATE.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
