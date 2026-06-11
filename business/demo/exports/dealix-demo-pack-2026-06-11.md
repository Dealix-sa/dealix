# Dealix Demo Pack — 2026-06-11 (AR+EN)

_Demo material. No customer data. Founder-reviewed before any external share._

## سيناريو العرض (عربي)

# سيناريو العرض التوضيحي — Dealix (عربي)

مدة: 20 دقيقة. مستمع: مسؤول تجاري / مالك شركة B2B سعودية.

## (1) دقيقتان — الافتتاحية

"Dealix يبني نظام تشغيل تجاري حقيقي فوق أدواتك الموجودة. مش CRM جديد، مش وكالة. نظام يومي يقلب تشتيت المبيعات والواتساب والسمعة إلى قرارات قابلة للقياس."

## (2) 3 دقائق — لوحة Command Center

افتح `/command-center`:
- Top accounts بتقديرات.
- Drafts الواتساب الجاهزة للمراجعة.
- المتابعات المستحقة اليوم.
- إثباتات الأسبوع.

ركّز: "كل شيء معد بشري قبل ما يطلع منك."

## (3) 4 دقائق — Revenue Machine

افتح `/revenue-machine`:
- العروض الـ 17 (17 OS modules).
- خط القمع: Diagnostic 499 → Data Pack 1,500 → Managed 2,999-4,999 → Custom 5,000-25,000.
- شفافية الأسعار.

## (4) 4 دقائق — Persuasion Room + Daily Draft

افتح `/persuasion-room` و `/daily-draft`:
- زوايا الإقناع المعتمدة.
- مسوّدات الواتساب التي ينتجها النظام يومياً.
- زر مراجعة + موافقة + رفض.

## (5) 3 دقائق — Proof Vault

افتح `/proof-vault`:
- إثباتات بدليل، ليست شهادات وهمية.
- تقارير أسبوعية للعميل.

## (6) 2 دقيقة — الحوكمة

افتح `/enterprise-readiness`:
- سياسة الذكاء الاصطناعي.
- المراجعة البشرية.
- حدود البيانات.
- شجاعة الإفصاح: ما لسنا متوافقين معه نقول.

## (7) دقيقتان — الإغلاق

"ابدأ بـ Diagnostic Sprint بـ 499 ريال. أسبوع واحد. تطلع منه بسجل احتكاكات مكتوب + أول تقرير إثبات. لو حبيتنا، ندخل في Managed Ops. لو ما حبيتنا، عندك الـ artifact مجاناً."

CTA: `/book`.


## Demo Script (English)

# Dealix Demo Script (English)

Length: 20 minutes. Audience: B2B commercial owner / founder.

## (1) 2 min — Opening

"Dealix builds a real business operating system on top of the tools you already use. Not a new CRM, not an agency. A daily system that converts scattered sales, WhatsApp, and reputation into measurable decisions."

## (2) 3 min — Command Center dashboard

Open `/command-center`:
- Top scored accounts.
- WhatsApp drafts pending review.
- Follow-ups due today.
- This week's proof items.

Key line: "Everything is human-reviewed before it leaves your name."

## (3) 4 min — Revenue Machine

Open `/revenue-machine`:
- 17 productized OS offerings.
- Funnel ladder: Diagnostic 499 → Data Pack 1,500 → Managed 2,999-4,999 → Custom 5,000-25,000 SAR.
- Transparent pricing.

## (4) 4 min — Persuasion Room + Daily Draft

Open `/persuasion-room` and `/daily-draft`:
- Approved persuasion angles.
- WhatsApp drafts produced daily by the engine.
- Review + approve + reject controls.

## (5) 3 min — Proof Vault

Open `/proof-vault`:
- Evidence-based proof, not fake testimonials.
- Weekly customer reports.

## (6) 2 min — Governance

Open `/enterprise-readiness`:
- AI policy.
- Human review.
- Data boundaries.
- Plain disclosure of what we are NOT compliant with.

## (7) 2 min — Close

"Start with the Diagnostic Sprint at 499 SAR. One week. You walk out with a written friction log + first proof report. If you like us, Managed Ops next. If you don't, the artifact is yours for free."

CTA: `/book`.


## Founder Demo Flow

# Founder Demo Flow — Internal Reference

Step-by-step the founder follows during a live demo.

## Before the call
1. Open `/command-center` in tab 1.
2. Open `/revenue-machine` in tab 2.
3. Open `/daily-draft` in tab 3.
4. Open `/proof-vault` in tab 4.
5. Open `/enterprise-readiness` in tab 5.
6. Have `LIVE_WORKFLOW_REVIEW_SCRIPT.md` open on second screen.

## During the call
- Speak the Arabic script if the buyer is Arabic-first, English otherwise.
- After every section, ask: "هل هذا قريب من تحديكم اليوم؟" / "Does this match a real friction you're hitting?"
- If yes, drill into the specific friction; pivot to the workflow review offer.
- If no, pivot to a different OS module.

## After the call
- Score the lead in `business/_data/scored_leads.json` via `scripts/score_leads.py`.
- Generate a follow-up using `scripts/generate_followup_queue.py`.
- Generate a tailored proposal using `scripts/generate_proposal.py`.
- Schedule the workflow review.

## Anti-patterns
- Do not promise outcomes. Promise the diagnostic sprint produces a written artifact.
- Do not improvise pricing. Read from `/pricing`.
- Do not skip the governance pillar even if the buyer doesn't ask — it's the differentiator.


## Live Workflow Review

# Live Workflow Review Script

Used during the 7-day diagnostic sprint, day 2-3 workshop.

## Setup
- 90-min slot.
- Founder + customer's commercial owner + 1 operator who actually does the work.
- Screen share their CRM, WhatsApp, and review console live.

## Sequence

### Block 1 (15 min) — Lead arrival
- Where do leads land?
- Who sees them first?
- How long until first response?
- Tag every friction visible on screen.

### Block 2 (15 min) — Qualification
- Who qualifies? What rule?
- Show 5 most recent qualified leads. Trace each to outcome.

### Block 3 (20 min) — Outreach
- WhatsApp tone, follow-up cadence, missed-follow-up rate.
- Pull last 10 conversations. Find the one that should have closed.

### Block 4 (15 min) — Proposal → close
- Time from proposal sent → decision.
- Decision rate.
- Common objections heard.

### Block 5 (15 min) — Post-close
- Onboarding. Time to first value. Retention signals.

### Block 6 (10 min) — Friction log
- Founder reads back the captured frictions ranked by revenue impact.
- Customer agrees on top 3 to address in the data pack.

## Output
- `business/_data/friction_logs/<account-id>-<date>.json`
- Ranked top 3 frictions become the Data Pack scope.


## Demo Q&A — Objections

# Demo Q&A — Common Objections + Responses

## "We already have a CRM."
Good. Dealix sits on top. We don't replace it. We connect, govern, and produce proof on top of HubSpot / Salesforce / Zoho / Bitrix / Pipedrive.

## "We tried an agency, didn't work."
Agencies run campaigns; Dealix builds a system that outlives the contract. Start with a 499 SAR diagnostic sprint — no commitment.

## "ChatGPT can do this."
ChatGPT generates text. Dealix runs a daily operator pack, queues drafts for human review, logs every approval, produces customer-facing proof reports, and protects you from auto-sending something embarrassing.

## "We don't have budget."
The Diagnostic Sprint is 499 SAR. If after the friction log you don't see 5x ROI in the data pack scope, walk away with the artifact for free.

## "How do I know this works?"
You don't yet. That's why we built the diagnostic sprint as a low-risk first step. You'll know after 7 days.

## "What about our data?"
Stays in your systems. Read `business/enterprise/DATA_BOUNDARY_STATEMENT.md`. Dealix processes copies inside the SOW scope only.

## "Do you guarantee ROI?"
No. Anyone who does is lying. We commit to delivering the artifacts in the SOW.

## "Can we start with one OS module?"
Yes. Pick Revenue OS, Review OS, or Command Center. We'll scope a 30-day pilot.

## "Are you GDPR / PDPL compliant?"
We follow PDPL principles. We hold operational scaffolds; formal attestation is a roadmap item. See `business/enterprise/AI_GOVERNANCE_STATEMENT.md`.

## "Why Arabic-first?"
Because the buyers we serve work in Arabic. Drafts in both AR and EN; founder reviews both.


## Demo Close

# Demo Close

Closing sequence after the 20-min walkthrough.

## Step 1 — Confirm
"Before we wrap, did you see at least one part of your workflow you'd want to fix in the next 30 days?"

If yes → Step 2. If no → respectful close, send the FAQ, ask permission to follow up in 60 days.

## Step 2 — Offer
"I'd like to propose the Diagnostic Sprint. It's 7 days, 499 SAR. By day 7 you have a written friction log, a tailored data pack proposal, and the first proof report. If you don't see 5x value in the data pack scope, the artifact is yours and we part friends."

## Step 3 — Book
Open `/book` and book the kickoff slot live. Don't say "I'll send a link" — book it now.

## Step 4 — Confirm SOW expectations
"Right after the call I'll send a one-page SOW. It lists what we'll cover, what's out of scope, and what you need to bring (CRM access, 1 commercial owner, 1 operator). Reply with 'approved' and we start."

## Step 5 — Set the workflow review
- Day 2 or 3.
- 90 min.
- Customer's commercial owner + operator.
- Tell them what to bring (recent leads, recent WhatsApp threads, last quarter's review console).

## Anti-patterns
- Don't discount the sprint. 499 is the price.
- Don't promise outcomes. Promise the artifact.
- Don't end the call without a calendar event booked.

