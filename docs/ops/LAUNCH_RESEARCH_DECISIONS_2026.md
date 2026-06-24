# Dealix Launch Research Decisions — 2026

## Executive decision

Dealix should launch as a Saudi B2B AI Operating Systems company, not as a generic AI chatbot, CRM clone, or marketing agency.

The go-to-market standard is:

1. conversion-focused public website
2. draft-first commercial workflow
3. high-velocity but compliant targeting
4. backend readiness gates
5. proof packs for every pilot
6. no uncontrolled external sending

## Sources translated into operating decisions

### Email deliverability

Google requires all senders to Gmail accounts to use SPF or DKIM, and bulk senders must use SPF, DKIM, and DMARC. Google also says senders should keep spam rates below 0.3%, support visible unsubscribe for marketing messages, and increase sending volume gradually.

Dealix decision:

- No cold blast mode.
- Start with manual founder-led sends.
- Require SPF/DKIM/DMARC before any live email automation.
- Require unsubscribe wording in commercial templates.
- Track domain reputation before scaling.
- Use controlled daily volume, not bursts.

### WhatsApp

WhatsApp Business Platform requires opt-in before template messages and requires approved templates. WhatsApp policy also says businesses may only contact people when they have the number and opt-in permission, and must respect opt-out requests.

Dealix decision:

- WhatsApp is draft-only by default.
- No cold automated WhatsApp.
- Future live WhatsApp requires opt-in, approved template, quality monitoring, and suppression list.

### AI safety

OWASP identifies prompt injection, insecure output handling, sensitive information disclosure, excessive agency, and overreliance as key LLM application risks.

Dealix decision:

- Keep human approval for external actions.
- Treat AI output as recommendation, not authority.
- Validate generated drafts before use.
- Use least-privilege tools.
- Block fake ROI, fake testimonials, and misleading claims.

### B2B website conversion

A B2B visitor must understand quickly:

- who Dealix is for
- what pain it solves
- what first offer they can buy
- why it is safe
- what happens next

Dealix decision:

- Homepage hero focuses on Saudi B2B AI Operating Systems.
- Offer cards show product, pain, timeline, and suggested price range.
- CTA is a review/diagnostic, not a vague “contact us”.
- Proof language is operational, not fabricated case studies.

## Launch standards

### Website

- Clear headline above the fold.
- One primary CTA: book operating review.
- Product cards with pain/outcome/timeline/price range.
- Safety section: no uncontrolled send.
- Process section: Map → Design → Build → Operate → Scale.
- Sector wedge list.
- Structured data for SEO.

### Backend

- App boots with safe env.
- Outbound flags default false.
- Commercial scripts run without external APIs.
- No secrets in repo.
- No destructive DB migrations.
- Health and readiness endpoints must remain stable.

### Targeting

The safe daily targeting loop:

| Step | Volume | Rule |
|---|---:|---|
| Research companies | 100 | public source only |
| Verify | 40 | source_url required |
| Draft messages | 25 | no fake claims |
| Manual sends | 10–15 | founder approval |
| Calls | 3 | high-fit only |
| Proposals | 1 | scoped offer only |

## Non-negotiables

- No spam language.
- No fake urgency.
- No scraped private data.
- No bought lists.
- No live WhatsApp without opt-in.
- No guaranteed revenue claim.
- No unreviewed AI external action.
