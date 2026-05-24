# Market Domination Intelligence | ذكاء السيطرة على السوق

## Purpose | الغرض
The Market Domination Intelligence layer is Dealix's central brain for understanding
where Saudi B2B revenue is moving, which sectors are heating up, which accounts are
buying, and where Dealix can win — without ever sending an unapproved message, making
a guaranteed revenue claim, or committing pricing.

It is a *signal-to-draft* system, not a *signal-to-send* system.

## Non-negotiables | المبادئ غير القابلة للتفاوض
- No external sending. Every intelligence-driven action ends in a draft inside the
  Dealix queue; the founder approves before anything leaves.
- No proof publishing without approval. Even auto-generated case-study candidates
  are A2/A3-gated.
- No guaranteed revenue claims. Intelligence describes pipelines, win-likelihoods,
  and weighted forecasts only.
- No pricing/contract/payment commitments produced by intelligence outputs.
- All external-impact actions emit a policy snapshot + audit row.

## Inputs | المدخلات
- Public web signals (company sites, press releases, hiring pages, gov tenders)
- LinkedIn surface signals (titles, posts, hiring, funding markers)
- News + market wires (Saudi business press, sector publications)
- Dealix internal CRM + reply ledger (closed-loop feedback)
- Partner / referral network notes
- Founder-curated watchlists

## Outputs | المخرجات
- A ranked **Account Domination Map** updated daily
- **Sector Heat Index** (sector_id, heat_score 0-100, trend arrow, evidence_refs)
- **Trigger event queue** (new hires, raises, expansions, tenders, leadership moves)
- **Competitive moves log** (who else is selling into the same account)
- **Draft suggestions** for Outbound, ABM, Content, and Partner machines

## Core models | النماذج الأساسية
1. **Saudi Relevance Score** — KSA HQ, KSA branch, KSA buyer presence, KSA spend signal
2. **B2B Fit Score** — sells to businesses, not consumers, high-ticket >= SAR 30k
3. **Buyer Clarity Score** — named decision maker identifiable in public surfaces
4. **Pain Urgency Score** — triggers in last 90 days
5. **Outreach Fit Score** — channel availability (LinkedIn, form, email)
6. **Proof Fit Score** — Dealix has a relevant proof artifact (sample/case study)
7. **Partner Potential Score** — could be a channel multiplier vs direct sale
8. **Trust Risk Score** — regulated/sensitive/political risk

Final priority = weighted blend → A / B / C / Reject

## Decision rules | قواعد القرار
- A-priority accounts → enter ABM Strategic Account Machine
- B-priority accounts → enter Outbound Draft Machine
- C-priority accounts → enter Nurture Machine
- Reject → never re-surface for 90 days, with reason logged

## Approval classes | فئات الموافقة
- A1 (auto): scoring updates, sector re-ranking, internal dashboards
- A2 (founder): publishing any new "intelligence report" externally, contacting
  any new account, attaching a proof artifact to a draft
- A3 (escalation): anything touching regulated sectors, government, or a competitor
  named directly in outbound copy

## Trust gate | بوابة الثقة
Every output passes:
- Source citation present (at least one URL or document ref)
- No guaranteed-revenue language
- No price/contract/payment language
- Policy snapshot ID + audit row written
- PII minimization check

## Owner | المالك
Founder is final approver. Intelligence Worker is the autonomous engine.

## Worker name
`intelligence.market_domination`

## KPI | المؤشرات
- Coverage: # KSA B2B accounts profiled
- Freshness: median age of last signal per A-account
- Conversion: % A-accounts that reach proposal stage
- Trust: 0 unapproved external messages, 0 unauthorized proof publications

## Failure modes | حالات الفشل
- Stale signals (> 30 days) silently feeding outbound — auto-quarantined
- Source URL 404 — score frozen until re-verified
- Sector heat spike from a single noisy source — requires 2+ independent sources

## Recovery path | مسار الاسترداد
- Quarantine the affected account, rollback its score to previous snapshot
- Notify founder in daily digest
- Mark the source as low-confidence for 14 days
