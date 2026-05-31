# Dealix Growth OS — Verification Playbook
# دليل التحقق — ديليكس Growth OS

**Version:** 1.0 | **Date:** 2026-05-31

Run all gates: `python growth-os/verification_gates.py`
Run tests: `python -m pytest growth-os/acceptance_tests.py -v`

---

## Gate Overview

| Gate | Name | Status Required | Blocks |
|------|------|-----------------|--------|
| 1 | Infrastructure Ready | pass | All execution |
| 2 | Data Quality Ready | pass | Asset generation |
| 3 | Company Understanding Ready | pass | Asset generation |
| 4 | Draft Quality Ready | pass | Execution |
| 5 | Channel Safety Ready | pass | All execution |
| 6 | Execution Health Ready | pass | Execution queue |
| 7 | Deliverability Ready | pass | Email sends |
| 8 | Reply Quality Ready | pass | Reply processing |
| 9 | Pipeline Conversion Ready | warning | Scaling decisions |
| 10 | Learning Loop Ready | pass | Optimization |

---

## Gate 1: Infrastructure Ready

**Class:** `Gate1InfrastructureReady`

**What is checked:**
- suppression.jsonl exists and is readable
- opt_ins.jsonl exists
- execution_logs.jsonl exists
- All 8 output directories exist (daily, channel_packs, execution_queue, founder_review, sent, paused, rejected, reports)
- All 9 required config files exist
- GROWTH_OS_KILL_SWITCH status
- DRY_RUN mode status
- SENDING_DOMAIN env var set
- SPF/DKIM/DMARC (manual check flag)
- Memory files count >= 5

**Target:** All files exist + no kill switch active

**How to fix failures:**
1. Missing files: Create them from templates in memory/ and config/
2. SENDING_DOMAIN missing: Set in Railway env vars or .env file
3. SPF/DKIM/DMARC: Use MXToolbox to verify, fix DNS records

---

## Gate 2: Data Quality Ready

**Class:** `Gate2DataQualityReady`

**What is checked:**
- Duplicate rate by domain: < 3%
- Missing sector rate: < 10%
- Missing country rate: < 5%
- Sensitive sector flagging: 100% (all sensitive sectors defined in config)
- Invalid contacts rate (no email, no linkedin, no phone): < 10%
- Suppression respected: No suppressed contacts in active queue

**Target:** All rates within thresholds

**How to fix failures:**
1. High duplicate rate: Deduplicate companies.jsonl by domain
2. Missing sector/country: Run sector-classifier and language-detector agents
3. Invalid contacts: Add email or LinkedIn URL for each contact
4. Suppression: Re-run suppression check before every send

---

## Gate 3: Company Understanding Ready

**Class:** `Gate3CompanyUnderstandingReady`

**Scoring thresholds:**
- understanding_score: >= 80
- offer_fit_score: >= 75
- buyer_confidence_score: >= 60
- pain_clarity_score: >= 75
- language_confidence_score: >= 90

**Target:** >= 80% of company briefs meet all thresholds

**How to fix failures:**
1. Re-run company-researcher agent with more context
2. Improve sector-specific prompts for low-confidence sectors
3. Manual founder review for low language_confidence companies
4. Do not proceed to asset generation for briefs below threshold

---

## Gate 4: Draft Quality Ready

**Class:** `Gate4DraftQualityReady`

**What is checked:**
- Average quality score >= 75
- Reject rate < 20%
- Compliance pass rate >= 95%
- All 8 scoring criteria applied

**Scoring breakdown (100 points total):**
- company_personalization: 20
- clear_pain: 20
- single_offer: 15
- simple_cta: 10
- channel_language: 10
- no_exaggeration: 10
- compliance_optout: 10
- brevity_clarity: 5

**Decision thresholds:**
- >= 90: ready (auto_send eligible)
- 82-89: founder_review
- 70-81: rewrite
- < 70: reject

**How to fix failures:**
1. High reject rate: Review email_draft.md prompt — strengthen personalization
2. Low average score: Add more sector-specific pain data to briefs
3. Missing compliance_optout: Add opt-out instruction to all templates

---

## Gate 5: Channel Safety Ready

**Class:** `Gate5ChannelSafetyReady`

**What is checked:**
- LinkedIn mode = assisted_manual (hard fail if not)
- WhatsApp opt-in required = true (hard fail if not)
- LinkedIn block_scraping = true (hard fail if not)
- Website forms rate limit configured
- Instagram unsolicited DM blocked

**Target:** All checks pass — no exceptions

**How to fix failures:**
1. LinkedIn not assisted_manual: Update config/anti-ban.yml — NON-NEGOTIABLE
2. WhatsApp opt-in not required: Update config/anti-ban.yml — NON-NEGOTIABLE
3. Scraping not blocked: Never unblock this — non-negotiable

---

## Gate 6: Execution Health Ready

**Class:** `Gate6ExecutionHealthReady`

**What is checked:**
- Execution logs schema: all required fields present
- Channel jobs schema: all required fields present
- Governance decision field: present in all jobs
- Stuck jobs: none pending > 48 hours

**Required log fields:** log_id, job_id, company_id, channel, event_type, event_at, governance_decision

**Required job fields:** job_id, asset_id, company_id, channel, execution_mode, status, governance_decision

**How to fix failures:**
1. Missing governance_decision: Update execution agent to always include it
2. Stuck jobs: Review and action or cancel pending_founder_approval jobs
3. Missing fields: Update job creation code to include all required fields

---

## Gate 7: Deliverability Ready

**Class:** `Gate7DeliverabilityReady`

**Thresholds:**
- bounce_rate: < 2%
- spam_rate: < 0.1%
- unsubscribe_rate: < 1%
- reply_rate: > 3%

**Input:** Provide metrics dict to check() for full evaluation
```python
gate = Gate7DeliverabilityReady()
result = gate.check(metrics={
    "bounce_rate": 0.015,
    "spam_rate": 0.0005,
    "unsubscribe_rate": 0.008,
    "reply_rate": 0.04,
})
```

**How to fix failures:**
1. High bounce rate: Clean email list, check for typos, suppress bounced addresses
2. High spam rate: Review subject lines, check sending reputation, use postmaster tools
3. Low reply rate: Test new angles, review quality gate minimum, check segment fit

---

## Gate 8: Reply Quality Ready

**Class:** `Gate8ReplyQualityReady`

**What is checked:**
- Reply schema: all required fields present
- Unsubscribe handling: all routed to add_to_suppression_immediately
- Bounce handling: all marked as mark_invalid_email
- Classification coverage: >= 95% of replies classified

**How to fix failures:**
1. Unsubscribe not routed to suppression: Fix reply_classifier.py get_next_action()
2. Low classification coverage: Review reply_classifier patterns for edge cases
3. Missing schema fields: Update reply processing to include all required fields

---

## Gate 9: Pipeline Conversion Ready

**Class:** `Gate9PipelineConversionReady`

**Funnel benchmarks:**
- reply_rate: >= 2%
- positive_reply_rate: >= 0.5%
- call_booking_from_positive: >= 20%
- proposal_from_discovery: >= 30%
- close_from_proposal: >= 10%

**Note:** Requires 20+ sends for meaningful comparison

**How to interpret:**
- Below benchmark after 50 sends → stop and revise strategy
- Below benchmark after 20 sends → monitor, not yet actionable
- At or above benchmark → scale up volume in this segment

---

## Gate 10: Learning Loop Ready

**Class:** `Gate10LearningLoopReady`

**What is checked:**
- Learning log has entries
- Last entry is within 2 days (current)
- All entries have recommendations
- Experiments config loaded with >= 5 ideas

**How to fix failures:**
1. No learning logs: Run `from learning_engine import LearningEngine; LearningEngine().analyze_daily()`
2. Stale logs (> 7 days): Set up nightly cron for learning_engine.analyze_daily()
3. No recommendations: Fix _generate_recommendations() in learning_engine.py

---

## Running All Gates

```bash
# Full verification
python growth-os/verification_gates.py

# Acceptance tests
python -m pytest growth-os/acceptance_tests.py -v

# Quick gate check in Python
from growth_os.verification_gates import run_all_gates
summary = run_all_gates()
print(summary['summary'])
```

---

## Pre-Launch Checklist

Before first live send:
- [ ] Gate 1 status: pass
- [ ] Gate 2 status: pass (or warning with < 5 companies)
- [ ] Gate 5 status: MUST be pass (no exceptions)
- [ ] SENDING_DOMAIN configured in env
- [ ] SPF/DKIM/DMARC verified via MXToolbox
- [ ] Suppression list initialized
- [ ] DRY_RUN=false confirmed
- [ ] GROWTH_OS_KILL_SWITCH=false confirmed
- [ ] Moyasar: founder has toggled to live mode (or test mode for testing)
- [ ] First canary batch: max 5 emails, monitor for 24h before scaling

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
