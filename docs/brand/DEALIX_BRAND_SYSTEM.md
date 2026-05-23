# DEALIX Brand System

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**
> Positioning: **Saudi B2B Revenue Operating System**

This document is the single source of truth for how the Dealix brand is built,
expressed, and governed. It is written for engineers, designers, founders, and
operators who ship customer-facing surfaces. Where another brand document
exists (visual identity, color, typography, voice), this file points to it and
sets the rules that bind them together.

The brand is not a logo. It is the system that makes every Dealix surface look,
sound, and behave as if one operator wrote it on one careful day.

---

## 1. What Dealix is

Dealix is the Saudi B2B Revenue Operating System. It is the layer that sits
between fragmented tools, scattered conversations, and real revenue. It helps
Saudi B2B teams move from noise to closed deals — with evidence, with
approvals, and without the inflated claims that the local market has learned
to distrust.

The brand exists to carry three signals at the same time:

1. **Sober competence.** This is enterprise software, not a growth-hack toy.
2. **Saudi context.** Right-to-left, bilingual, locally grounded.
3. **Operator-first.** Built by someone who has closed a deal, not by a
   marketing department.

If a surface — landing page, deck, email, dashboard, invoice — does not carry
those three signals, it is off-brand.

---

## 2. The five pillars

The brand is anchored on five pillars. They appear, in different weights, in
every public-facing artifact.

| Pillar | What it means | Where it shows up |
| --- | --- | --- |
| Built on Trust | Approval gates, evidence ledger, no auto-send | Product, contracts, deck |
| Driven by Growth | Pipeline, retention, expansion — measured | Dashboards, reports |
| Closing Deals | The verb that defines the company | Sales narrative, CTAs |
| Focused on Results | Outcomes over activity | Case studies, reviews |
| Global Mindset, Local Impact | World-class craft, Saudi-first execution | Voice, partnerships |

The pillars are not slogans. They are the filter we use when deciding whether
a feature, page, or sentence ships.

---

## 3. Voice in one paragraph

Dealix sounds like a senior operator who has nothing to prove and no time to
waste. Confident, specific, bilingual when it must be, never breathless. We
prefer nouns and verbs over adjectives. We never write "guaranteed revenue",
"guaranteed sales", or "guaranteed meetings". We do not promise outcomes we
cannot defend with evidence. We do not publish customer names, logos, or
quotes without written approval recorded in the proof ledger.

Full voice guidance lives in `DEALIX_BRAND_VOICE.md`.

---

## 4. Visual identity in one paragraph

The logo is a **D** monogram with an embedded growth arrow and three revenue
bars, finished with a teal swoosh. The palette is Deep Navy (`#0B1220`),
Slate (`#0F1726`), Emerald Teal (`#00D1A1`), Soft Silver (`#B2BBC6`), and
White (`#FFFFFF`). The type stack is Inter for Latin script and IBM Plex Sans
Arabic for Arabic script. The aesthetic is dark-surface enterprise: navy
fields, teal accents used sparingly, generous white space, and no
decoration that does not carry information.

Detail lives in `DEALIX_VISUAL_IDENTITY.md`, `DEALIX_COLOR_SYSTEM.md`, and
`DEALIX_TYPOGRAPHY.md`.

---

## 5. Surfaces the brand must cover

The brand system is responsible for every surface a customer, prospect,
partner, or regulator can encounter. The current list:

- Product UI (web app, founder shell, customer rooms)
- Marketing site and OG cards
- Sales deck, proposal, pricing one-pager
- Sector reports and benchmark briefs
- Email templates and signatures
- LinkedIn company page and founder profiles
- Social posts (LinkedIn, X)
- Contracts and DPA cover pages
- Internal operator dashboards (still on-brand; customer may see them)

Every surface is treated as a contract: it must carry the wordmark, hold the
palette, respect the typography, and follow the tone rules. A surface that
breaks any of those is not "creative" — it is broken.

---

## 6. Non-negotiables (the guardrails)

These are the rules that override any creative or commercial argument. They
exist because the brand has to survive a skeptical Saudi enterprise buyer who
has been disappointed by martech promises before.

### 6.1 No guaranteed revenue, sales, or meetings claims

We do not write — in any language, on any surface — sentences of the form
"guaranteed revenue", "guaranteed sales", "guaranteed meetings", or any
near-paraphrase. We do not use "promise" or "promised" attached to a revenue,
sales, or meeting outcome. We can describe what the system does, what
customers have reported (with approval), and what we target. We do not
guarantee the result.

### 6.2 No proof publication without approval

No customer name, logo, quote, screenshot, metric, or case study is published
on any external surface without a written approval recorded in the proof
ledger. "Verbal yes in a call" is not approval. The approval has a record, a
timestamp, and an owner. If we cannot show the approval, the asset stays in
draft.

### 6.3 No external sending automation; all execution is trust-gated

The product never sends a message, email, or document to an external party
without a human approval recorded in the approval queue. Marketing reflects
that: we do not advertise "AI sends emails for you", "auto-outreach", or
"hands-off outbound". We advertise drafted-then-approved execution, because
that is what the product actually does.

If a draft, a screenshot, or a deck slide implies otherwise, it is off-brand
and must be revised before it leaves the building.

---

## 7. Governance — who decides what

| Decision | Owner | Reviewer |
| --- | --- | --- |
| New logo lockup or wordmark variant | Founder | Brand director |
| Palette change (any) | Founder | Brand director, design lead |
| New surface added to the system | Brand director | Founder |
| Public claim language (case studies, headlines) | Brand director | Founder, legal |
| Customer proof publication | Brand director | Customer (written), founder |
| Voice changes (EN or AR) | Brand director | Bilingual reviewer |
| Token changes in `brand-tokens.json` | Design lead | Brand director |

The brand director is the steward. The founder is the final signer. Legal
reviews any claim that could be read as a guarantee.

---

## 8. How the brand is wired in code

The brand is not only a PDF. It is wired into the codebase:

- `docs/brand/brand-tokens.json` — canonical tokens (colors, type, spacing,
  pillars, tagline, positioning).
- `apps/web/lib/brand-tokens.ts` — typed token surface for the web app.
- `apps/web/styles/brand.css` — CSS custom properties that mirror the tokens.
- `apps/web/components/brand/*` — React components (logo, cards, badges,
  CTAs) that consume the tokens and cannot be styled off-brand without an
  explicit override.

Two verifiers keep the system honest:

- `scripts/verify_brand_system.py` — checks files and color tokens.
- `scripts/verify_brand_growth_operating_layer.py` — composite verifier that
  bundles brand, growth, marketing, product distribution, and positioning.

Any pull request that changes a brand surface should leave both verifiers
green.

---

## 9. Workflow — adding or changing a surface

1. Read this document and the relevant sibling (visual identity, color, type,
   voice).
2. Draft the surface in the lowest-fidelity form that proves the idea.
3. Run it past the brand director. If it touches a claim, run it past the
   founder and legal.
4. Check the non-negotiables (section 6). If any are violated, revise.
5. Wire it into the component library if it is a repeatable surface.
6. Add a verifier hook if the surface is load-bearing.
7. Ship.

---

## 10. The brand in one sentence

Dealix is the calm, evidence-bearing operating system Saudi B2B teams trust
because everything it says about itself is something it can show.

---

## 11. Bilingual note — العربية

نظام علامة دِيليكس مبني على الثقة، النمو، إغلاق الصفقات، التركيز على
النتائج، والعقلية العالمية بأثر محلي. لا نَعِد بإيرادات أو مبيعات أو اجتماعات
مضمونة. لا ننشر اسم عميل أو شعاره أو اقتباساً منه دون موافقة مكتوبة. ولا نرسل
أي رسالة خارجية تلقائياً — كل تنفيذ يمر بموافقة بشرية. هذه القواعد ليست قابلة
للتفاوض، وهي ما يجعل العلامة قابلة للدفاع أمام مشترٍ سعودي محنّك.

---

## 12. Pointers

- Visual identity: `DEALIX_VISUAL_IDENTITY.md`
- Logo usage: `DEALIX_LOGO_USAGE.md`
- Color: `DEALIX_COLOR_SYSTEM.md`
- Typography: `DEALIX_TYPOGRAPHY.md`
- Voice: `DEALIX_BRAND_VOICE.md`
- Asset export: `DEALIX_MARKETING_ASSET_GUIDE.md`
- Accessibility: `DEALIX_ACCESSIBILITY_GUIDE.md`
- Social kit: `DEALIX_SOCIAL_MEDIA_KIT.md`
- Proposal template: `DEALIX_PROPOSAL_TEMPLATE_GUIDE.md`
- Sales deck: `DEALIX_SALES_DECK_GUIDE.md`
- Sector report: `DEALIX_REPORT_TEMPLATE_GUIDE.md`
- Email signature: `DEALIX_EMAIL_SIGNATURE_GUIDE.md`
- LinkedIn: `DEALIX_LINKEDIN_PROFILE_GUIDE.md`
