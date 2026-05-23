# Sample Factory | مصنع العينات

## Purpose | الغرض
When a buyer says "show me", the Sample Factory produces a tailored, time-boxed,
risk-free sample of Dealix's work specifically for that buyer's context. The
sample is a draft → founder approves → buyer receives.

A sample is *evidence in their hands*, not a commitment.

## Inputs | المدخلات
- Reply Router intent: "wants sample"
- Account dossier (sector, ICP, persona, pain pattern, named buyer)
- Matched proof artifact templates
- Buyer-specific public signals (their website, their public goals)

## Outputs | المخرجات
- `samples.artifacts`: sample_id, account_id, buyer_id, type, content_pointer,
  state, created_at, approved_at, delivered_at, feedback_state
- A buyer-ready file (PDF / deck / short video / live mini-walkthrough)
- A short cover note framing the sample

## Sample types | أنواع العينات
- **Audit snapshot** — quick read of buyer's current outbound or revenue posture
- **Mini lead list** — 10 pre-scored target accounts in their sector
- **Cold draft pack** — 3 personalized cold drafts for their top targets
- **Process diagnosis** — short diagram + commentary on their current funnel
- **Proof excerpt** — anonymized slice of a comparable Dealix engagement

## Time-box | الإطار الزمني
- Drafted within 24-48 hours of buyer's request
- Approved within 24 hours by founder
- Delivered within 72 hours of original request
- Feedback expected within 7 days; otherwise auto-follow-up draft

## Personalization gate | بوابة التخصيص
- Sample references buyer-specific public signals (3+ citations)
- Sample includes 1 explicit "what this would look like for you" paragraph
- No price, no contract, no payment terms
- No guaranteed-outcome language

## Data source | مصدر البيانات
`samples.artifacts`, `intelligence.accounts`, `personas.profiles`,
`proof.artifacts` (templates).

## Approval class | فئة الموافقة
- A1: drafting sample content from templates
- A2: founder approval before sample is sent
- A3: samples to regulated/government buyers; samples that reference any
  competitor by name

## Trust gate | بوابة الثقة
- Sample never contains another client's PII
- Public signals cited with source URLs
- No revenue guarantees
- Watermarked "sample — not a proposal"
- Policy snapshot + audit row per sample

## Owner | المالك
Founder approves every sample before delivery.

## Worker name
`revenue.sample_factory`

## KPI | المؤشرات
- Median time: request → delivery (target ≤ 72h)
- Sample → proposal-requested rate (target ≥ 40%)
- Sample → meeting-booked rate
- Founder edit-distance on drafts (should fall over time)

## Failure mode | حالات الفشل
- Sample uses outdated signals about buyer
- Sample template accidentally exposes another client's data
- Founder approval delayed → 72h SLA missed

## Recovery path | مسار الاسترداد
- Signal freshness check at draft time; stale > 14 days blocks the draft
- Cross-client PII scanner before sample finalization
- SLA breach surfaces on founder dashboard; auto-extend with explanation note
