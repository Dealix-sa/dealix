# Dealix — 30 / 60 / 90 Day Roadmap

**Owner of the plan:** Founder. **Operator:** Dealix PM agent + sub-agents.
**Strategy source:** [`FULL_OPS_STRATEGY.md`](FULL_OPS_STRATEGY.md) — derived from founder roadmap (Appendix §14).
**Non-negotiables:** Every milestone that touches money, contracts, external sends, or sensitive data carries an explicit **`APPROVAL-GATED`** marker — these execute only after a recorded founder approval per the 11 non-negotiables in `AGENTS.md`.

**Decision rules (apply at every horizon):**
- If a milestone hasn't been done **manually 5 times**, it stays in draft/founder-assisted mode — do not automate.
- If a milestone would emit an external commitment (message, contract, claim, payment), it must route through `approval_center`.
- If revenue at day 60 is below 25K SAR cumulative, halt new offer-building and double down on sales motion (warm-list re-engagement, content cadence, price tests).

---

## Horizon 0: First 48 hours

| # | Milestone | Owner | Success metric | Approval gate? | Dependencies |
|---|-----------|-------|----------------|----------------|--------------|
| 0.1 | Revenue Sprint landing copy drafted (AR primary + EN mirror) — outcome, deliverables, price (2,500 SAR Starter), 7-day timeline | dealix-content (drafts) | Draft reviewable in repo or markdown | Founder approves before publish | New strategy installed |
| 0.2 | Minimal CRM record set defined (accounts, contacts, conversations, opportunities, proposals, payments — schema-only sketch) | dealix-engineer (design only) | Schema doc in `docs/strategy/` or `docs/architecture/` | None (design doc) | Strategy installed |
| 0.3 | Signal Sample template (5 leads + 5 pain reasons + 5 outreach drafts + mini memo) — markdown template only | dealix-content | Template renders for 1 example sector | None (template) | 0.2 schema sketch |
| 0.4 | Proposal template for Sprint Starter / Growth / Premium (single bilingual template, variable-driven) | dealix-content | Template handles all 3 tiers | None (template) | Strategy installed |
| 0.5 | Delivery report template (Sprint output structure: list + score rationale + outreach pack + 14-day plan) | dealix-content | Template renders for stub data | None (template) | 0.3 |
| 0.6 | Approval queue UX confirmed (route every external send through `approval_center` — confirm pathway, no new code) | dealix-engineer (audit, not build) | One-page audit note: every external channel inventoried | None (audit) | None |
| 0.7 | Sensitive file audit: client data / lead lists / pricing experiments / DM queues moved to private repo or `.gitignore` | Founder + dealix-engineer | Audit checklist completed; no PII in public repo | **APPROVAL-GATED** (founder confirms move) | None |
| 0.8 | Outreach drafts prepared (50 messages across 3 ICP sectors) — drafts only, no send | dealix-sales | 50 drafts in approval queue | **APPROVAL-GATED** (per send) | 0.1 + 0.7 |
| 0.9 | 5 Signal Samples prepared (one per priority account) | dealix-delivery | 5 sample packs ready | **APPROVAL-GATED** before send | 0.3 |
| 0.10 | Payment workaround documented (invoice + manual receipt path) while Moyasar live mode pending founder cutover | Founder | Documented path in `docs/ops/` or `docs/strategy/` | **APPROVAL-GATED** (no auto-charge) | None |

---

## Horizon 1: First 7 days

| # | Milestone | Owner | Success metric | Approval gate? | Dependencies |
|---|-----------|-------|----------------|----------------|--------------|
| 1.1 | First paid customer (Sprint Starter or Growth) | Founder (sales) | 1 invoice paid; payment recorded in ledger | **APPROVAL-GATED** (founder closes) | 0.1, 0.4, 0.10 |
| 1.2 | First delivery (Sprint deliverable handed off with Proof Pack) | dealix-delivery + Founder QA | Proof Pack score ≥ 70; client confirms receipt | **APPROVAL-GATED** (QA + handoff) | 1.1, 0.5 |
| 1.3 | First testimonial captured (written or recorded) | Founder | 1 customer quote, on file, with consent for use | **APPROVAL-GATED** (consent recorded) | 1.2 |
| 1.4 | First internal case study drafted (no PII, lessons-learned, what worked) | dealix-content | Internal doc in `docs/strategy/case_studies/` or similar | None (internal) | 1.2 |
| 1.5 | Founder-only dashboard live (daily brief: revenue, customers, delivery, risk, learning) | dealix-engineer | Dashboard renders for founder; one-page view | None (founder-only) | 0.2 |

---

## Horizon 2: First 30 days

| # | Milestone | Owner | Success metric | Approval gate? | Dependencies |
|---|-----------|-------|----------------|----------------|--------------|
| 2.1 | **5 paid sprints delivered** (avg ~3,500 SAR each → ~17,500 SAR proof) | Founder + delivery | Cumulative sprint revenue ≥ 15K SAR | **APPROVAL-GATED** per close | 1.x complete |
| 2.2 | **2 retainers signed** (5,000 SAR/mo each → 10K MRR floor) | Founder | 2 signed SOWs in repo; first invoices issued | **APPROVAL-GATED** per SOW | 2.1 (≥1 sprint success required before each retainer pitch) |
| 2.3 | 3 ICP sectors tested (agencies / ERP-CRM-billing / contracting-B2B-services) — at least 1 sprint completed in each | dealix-sales + dealix-delivery | 3 sector logs with response rate, close rate, friction | None (analysis) | 2.1 |
| 2.4 | 1 sector report published (chose the highest-signal sector from 2.3) | dealix-content | Public report draft; founder reviews; published | **APPROVAL-GATED** (publish) | 2.3 |
| 2.5 | 1 public case study (with customer consent) | dealix-content | Case study published; consent letter on file | **APPROVAL-GATED** (consent + publish) | 1.3, 2.1 |
| 2.6 | 1 partner channel activated (agency referral or white-label intro) | Founder | 1 partner agreement; first referred lead | **APPROVAL-GATED** (partner SOW) | 2.1 |

**Day-30 honesty check:** if 2.1 (5 sprints) < 4 paid sprints, halt new feature work; founder + PM run a sales-motion review.

---

## Horizon 3: First 60 days

| # | Milestone | Owner | Success metric | Approval gate? | Dependencies |
|---|-----------|-------|----------------|----------------|--------------|
| 3.1 | Sprint runbook automated to founder-assisted level (founder time per sprint ≤ 4h) | dealix-engineer + dealix-delivery | Time-tracking: 3 consecutive sprints ≤ 4h founder time | None (internal) | 2.1 (5 sprints completed manually first) |
| 3.2 | Outreach + follow-up engine drafted-and-approved at scale (200 drafts/week through approval queue) | dealix-sales | 200 drafts/week reviewed; founder approval rate logged | **APPROVAL-GATED** (per batch) | 2.3 |
| 3.3 | Trust OS hardened — no-overclaim register active, suppression list enforced, evidence-pack assembly automated for Sprint deliverables | dealix-engineer | All Sprint outputs auto-attach Evidence Pack; suppression list blocks dupes | None (internal) | 1.2 |
| 3.4 | Cumulative revenue check: ≥ 25K SAR or escalate per decision rules | Founder + PM | Revenue ledger sums | None (review) | All above |
| 3.5 | 3rd retainer signed (target: enter day 60 with 3 retainers ≈ 15K MRR floor) | Founder | 3 active retainers | **APPROVAL-GATED** per SOW | 2.2 |

**Day-60 escalation rule:** if cumulative revenue < 25K SAR, founder + PM hold a "halt + redirect" meeting; new build work pauses, sales motion accelerates.

---

## Horizon 4: First 90 days

| # | Milestone | Owner | Success metric | Approval gate? | Dependencies |
|---|-----------|-------|----------------|----------------|--------------|
| 4.1 | **20 paid sprints cumulative** (target) | Founder + delivery | Cumulative count ≥ 16 (= 80% of target acceptable; below 16 = escalate) | **APPROVAL-GATED** per close | 2.1, 3.x |
| 4.2 | **5 retainers active** | Founder | 5 active retainers in good standing | **APPROVAL-GATED** per SOW | 2.2, 3.5 |
| 4.3 | **25K–50K SAR MRR** | Founder + finance | Monthly recurring revenue in stated range | **APPROVAL-GATED** per renewal | 4.2 |
| 4.4 | First Managed Pilot closed (12K SAR base, only if a Sprint Premium customer requests it) | Founder | 1 Managed Pilot SOW signed | **APPROVAL-GATED** (SOW) | Sprint Premium history |
| 4.5 | Dealix OS direction decision: build vs defer based on actual demand signals | Founder | Written decision in repo (build / defer / kill) | **APPROVAL-GATED** (strategic decision) | 4.1–4.3 |
| 4.6 | Official compliance/trust pack published (PDPL-aware language, no-overclaim language, approval matrix, evidence-pack examples) | dealix-content + dealix-engineer | Trust pack in `docs/strategy/` or `docs/trust/`; reviewed externally if possible | **APPROVAL-GATED** (publish) | 3.3 |
| 4.7 | Investor/Scale OS minimum: data room with metrics + roadmap + financial model + hiring plan stub | Founder | Data room folder accessible to founder; populated | **APPROVAL-GATED** (external access) | 4.1–4.4 |

**Day-90 promotion rule:** Wave 16 / Enterprise expansion unlocks only if:
- ≥ 1 paid invoice in Moyasar live (cutover happened), and
- ≥ 1 Proof Pack delivered (score ≥ 70), and
- ≥ 1 case-safe summary published, and
- 0 doctrine violations in audit trail.

---

## Cross-cutting commitments (every horizon)

| Commitment | What it means |
|------------|---------------|
| **Approval-first** | No external send / contract / payment without recorded founder approval. Routes through `approval_center`. |
| **No-overclaim** | "PDPL-aware" not "PDPL compliant". "ZATCA Phase 2" only with verified integration. "Founder-assisted" not "managed" for anything not run manually 5×. |
| **Evidence Pack per delivery** | Every paid delivery generates an Evidence Pack with score ≥ 70 before handoff. |
| **No PII in logs / public repo** | Sensitive client data / lead lists / pricing experiments stay private. |
| **Doctrine guards passing** | `tests/test_no_*` (no scraping, no cold WhatsApp, no LinkedIn automation, no overclaim, no unsourced answers, etc.) must pass before any merge. |

---

## Appendix — direct line to founder's words

Roadmap milestones above are derived from the founder's appendix §14 ("Roadmap"). For verbatim founder language and the surrounding context, see [`FULL_OPS_STRATEGY_APPENDIX.ar.md`](FULL_OPS_STRATEGY_APPENDIX.ar.md).
