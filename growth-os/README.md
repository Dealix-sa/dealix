# Dealix Growth OS
# نظام النمو — ديليكس

**Governed AI Operations for Saudi B2B — Growth Intelligence System**

---

## What This Is

Dealix Growth OS is the complete outreach and pipeline intelligence system for Dealix. It handles the full lifecycle from lead discovery to proposal delivery, with built-in governance, compliance, and learning.

**Key principle:** Every output is governed. Every send is auditable. Every claim is labeled as estimated or verified.

---

## Quick Start

### Run Verification Gates
```bash
python growth-os/verification_gates.py
```

### Run Acceptance Tests
```bash
python -m pytest growth-os/acceptance_tests.py -v
```

### Generate Daily Brief
```python
from growth_os.founder_dashboard import FounderDashboard
d = FounderDashboard()
print(d.generate_daily_brief())
```

### Check Channel Safety
```python
from growth_os.anti_ban_guardian import AntiBanGuardian
g = AntiBanGuardian()
print(g.check_channel("email", {"batch": ["test@example.com"]}))
print(g.check_linkedin())  # Always: assisted_manual
```

### Score a Draft
```python
from growth_os.quality_gate import DraftQualityGate
gate = DraftQualityGate()
result = gate.score_draft({
    "text": "Your draft text here. To unsubscribe reply STOP.",
    "subject": "Quick question about your operations",
    "channel": "email",
    "language": "en",
    "company_name": "Test Company",
})
print(result)
```

### Classify a Reply
```python
from growth_os.reply_classifier import ReplyClassifier
c = ReplyClassifier()
result = c.classify("Yes, I'm interested! When can we talk?", "en")
print(result)  # {'classification': 'interested', ...}
next_action = c.get_next_action(result)
print(next_action)  # {'action': 'book_discovery_call', 'urgency': 'high', ...}
```

---

## Directory Structure

```
growth-os/
  README.md                     ← This file
  FINAL_OPERATING_MODEL.md      ← Full architecture documentation
  VERIFICATION_PLAYBOOK.md      ← All 10 gates explained
  ANTI_BAN_POLICY.md            ← Channel-by-channel compliance rules
  FOUNDER_CONTROL_CENTER.md     ← 6 dashboards + daily rhythm

  verification_gates.py         ← 10 gate classes + run_all_gates()
  anti_ban_guardian.py          ← Channel health monitoring
  reply_classifier.py           ← Inbound reply classification
  quality_gate.py               ← Draft quality scoring
  founder_dashboard.py          ← 6 dashboard screens + daily brief
  learning_engine.py            ← Daily analysis + weekly review
  acceptance_tests.py           ← 7 acceptance tests

  config/
    anti-ban.yml                ← Per-channel rate limits and thresholds
    scoring.yml                 ← Quality weights and funnel benchmarks
    countries.yml               ← Target countries with language and sector data
    sectors.yml                 ← 12 sectors with pains, buyers, channels
    offers.yml                  ← 5 offer rungs + enterprise
    channel-router.yml          ← Routing rules by sector/country/language
    execution-modes.yml         ← auto_send, founder_approval, assisted_manual, inbound_only
    compliance.yml              ← PDPL, GDPR, CAN-SPAM, platform policies
    buyer-personas.yml          ← 8 buyer personas with objection handling
    persuasion.yml              ← PAIN→SOLUTION→PROOF→CTA per sector
    experiments.yml             ← A/B experiment templates
    quotas.yml                  ← Daily/weekly/monthly quotas per channel

  memory/
    raw_leads.jsonl             ← Discovered companies (company-level only)
    companies.jsonl             ← Company profiles
    contacts.jsonl              ← Contact info (business only, no PII)
    company_briefs.jsonl        ← Researched company briefs with scores
    channel_assets.jsonl        ← Generated outreach drafts
    channel_jobs.jsonl          ← Execution queue
    execution_logs.jsonl        ← Full audit trail
    replies.jsonl               ← All inbound replies (classified)
    opportunities.jsonl         ← Sales pipeline
    suppression.jsonl           ← Suppressed contacts/domains
    opt_ins.jsonl               ← Confirmed opt-ins for WhatsApp/Telegram
    warnings.jsonl              ← Active channel health warnings
    learning_log.jsonl          ← Daily learning analysis

  agents/                       ← Agent specification docs (16 agents)
  channels/                     ← Per-channel config (12 channels)
  prompts/                      ← LLM prompt templates (15 prompts)
  outputs/                      ← Execution outputs
    daily/                      ← Daily briefs
    channel_packs/              ← Channel-ready asset packs
    execution_queue/            ← Queued for send
    founder_review/             ← Awaiting founder approval
    sent/                       ← Successfully sent
    paused/                     ← Paused by anti-ban
    rejected/                   ← Rejected by quality/compliance
    reports/                    ← Analytics reports
```

---

## 11 Non-Negotiables

These are enforced in code, not just policy:
1. No scraping
2. No cold WhatsApp automation (opt-in required)
3. No LinkedIn automation (always assisted_manual)
4. No fake or unsourced claims
5. No guaranteed sales outcomes
6. No PII in logs
7. No sourceless knowledge answers
8. No external action without approval
9. No agent without identity
10. No project without Proof Pack (score >= 70)
11. No project without Capital Asset

---

## Governance Requirement

Every output object produced by Dealix Growth OS carries a `governance_decision` field:
```json
{"governance_decision": "descriptive string of what was decided and why"}
```

Every customer-facing output ends with:
"Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| DRY_RUN | No sends when true | false |
| GROWTH_OS_KILL_SWITCH | Halt all execution when true | false |
| SENDING_DOMAIN | Email sending domain | Required for email |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
