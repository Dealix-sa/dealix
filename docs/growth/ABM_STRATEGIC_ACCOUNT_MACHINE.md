# ABM Strategic Account Machine | آلة الحسابات الاستراتيجية

## Purpose | الغرض
Run high-touch, multi-thread, multi-channel campaigns against A-bucket accounts.
ABM is the most expensive distribution channel by founder time — and the highest
expected value.

Every touch is drafted, queued, and founder-approved. No autopilot.

## Inputs | المدخلات
- A-bucket accounts from Account Scoring Model
- Full account dossier: company profile, buying committee, recent triggers,
  competitive presence, proof matches
- Founder weekly ABM capacity (typically 5-10 accounts active)

## Outputs | المخرجات
- Per-account ABM plan: 3-6 touchpoints across 2-3 channels, 4-8 weeks
- `abm.touchpoints`: id, account_id, buyer_id, channel, type, draft_id, state
- Weekly ABM review board for founder

## Touchpoint types | أنواع نقاط التواصل
- Personalized LinkedIn DM to multiple buying-committee members
- Custom-cut email to economic buyer
- Tailored sample / mini-proof artifact
- Partner-led warm intro
- In-person or video meeting
- Custom one-pager pinned to a real, named pain
- Founder-authored short note (handwritten tone)

## Account plan structure | بنية خطة الحساب
1. Why this account, why now (1 paragraph, evidence-cited)
2. Buying committee map (3-5 named roles, public sources only)
3. Top 3 pains, top 3 proofs that match
4. 4-8 week touchpoint sequence
5. Success criterion: meeting booked OR proposal drafted
6. Exit criterion: hard no OR 12 weeks elapsed without movement

## Multi-thread rules | قواعد التواصل المتعدد
- Touch 2+ committee members in parallel
- Differentiate message per role (CRO ≠ COO ≠ Founder)
- Never imply private info from one buyer to another
- Buying-committee mapping uses public sources only

## Data source | مصدر البيانات
`abm.plans`, `abm.touchpoints`, `intelligence.accounts`, `personas.profiles`,
`proof.artifacts`, `partners.network`.

## Approval class | فئة الموافقة
- A1: plan drafting, dossier compilation, internal review
- A2: every touchpoint approved before send
- A3: ABM into regulated/government accounts; any plan that names competitors

## Trust gate | بوابة الثقة
- Buying committee map uses public sources only
- No cross-pollination of private buyer info between touchpoints
- No price/contract commitments in any touchpoint
- Per-touchpoint policy snapshot + audit row
- Trust risk re-checked at every touch

## Owner | المالك
Founder owns each account plan and approves every touch.

## Worker name
`growth.abm_machine`

## KPI | المؤشرات
- Active ABM accounts (target: 5-10 at any time)
- Meeting-booked rate (target: >= 30% within 8 weeks)
- Proposal-drafted rate (target: >= 50% of meetings)
- Paid-conversion rate

## Failure mode | حالات الفشل
- Touchpoints uncoordinated — buyer sees overlap
- Same proof artifact reused across committee members
- Founder capacity overrun → plan stalls mid-sequence

## Recovery path | مسار الاسترداد
- Cross-touchpoint deduper at plan time
- Proof artifact rotation enforced per account
- Capacity cap: no new ABM account opened while > 10 active
