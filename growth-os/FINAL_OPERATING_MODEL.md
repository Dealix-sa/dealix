# Dealix Growth OS — Final Operating Model
# نموذج التشغيل النهائي — ديليكس Growth OS

**Version:** 1.0 | **Date:** 2026-05-31 | **Branch:** claude/dealix-growth-os-verification-6rJki

---

## Strategic Frame / الإطار الاستراتيجي

Dealix sells **Governed AI Operations for Saudi B2B** — operating capability with auditable proof. Not AI tools. Not spam. Governed outputs with a paper trail.

**The 5-Rung Commercial Ladder:**

| Rung | Offer | Price (SAR) | Duration |
|------|-------|-------------|----------|
| 0 | Free AI Ops Diagnostic | 0 | 48 hours |
| 1 | 7-Day Revenue Intelligence Sprint | 499 | 7 days |
| 2 | Data-to-Revenue Pack | 1,500 | 14 days |
| 3 | Managed Revenue Ops | 2,999-4,999/mo | Ongoing |
| 4 | Custom AI Service Setup | 5,000-25,000 | 4-12 weeks |
| Enterprise | AI Governance Review | 25,000-50,000 | 8-16 weeks |

**90-Day Target:** 8-15K SAR MRR + 30-40K SAR one-time = 40-55K SAR cumulative

---

## Full Architecture / الهيكل الكامل

```
DATA SOURCES
    ↓
[Market Scanner Agent]
    ↓ raw_leads.jsonl
[Company Researcher Agent]
    ↓ company_briefs.jsonl
[Sector Classifier] + [Language Detector] + [Buyer Mapper]
    ↓
[Offer Router Agent] → recommended_offer
    ↓
[Channel Router Agent] → channel + execution_mode
    ↓
[Asset Generator Agent] → channel_assets.jsonl
    ↓
[Quality Gate] ─── score < 70 → REJECT
    ↓ score >= 70
[Compliance Gate] ─── violation → HARD BLOCK
    ↓ pass
[Execution Agent]
    ├── auto_send (QA >= 90, email only, non-sensitive)
    │       ↓ sent/
    ├── founder_approval (sensitive, large, low QA)
    │       ↓ founder_review/ → founder approves → sent/
    ├── assisted_manual (LinkedIn always)
    │       ↓ package to founder_review/ → founder executes manually
    └── inbound_only (Instagram, Messenger, Telegram)
            ↓ reply to inbound within 24h

MONITORING
    ↓
[Anti-Ban Guardian] → warnings.jsonl → pause channels if threshold breached
    ↓
[Reply Classifier] → replies.jsonl → next_action → opportunities.jsonl
    ↓
[Proposal Seed Agent] → seed package → founder builds proposal → client signs
    ↓
[Learning Agent] → learning_log.jsonl → weekly_review → experiment updates
    ↓
[Founder Chief of Staff] → daily_brief → outputs/daily/YYYY-MM-DD.md
```

---

## 11 Non-Negotiables (Enforced in Code)

1. **No scraping** — architecture blocks it, LinkedIn channel is assisted_manual only
2. **No cold WhatsApp automation** — opt-in required, hard-blocked without it
3. **No LinkedIn automation** — always assisted_manual, never touched by system
4. **No fake claims** — quality gate rejects drafts with guaranteed outcome language
5. **No guaranteed sales outcomes** — forbidden phrases list in quality_gate.py
6. **No PII in logs** — company-level data only, no personal emails/names in memory files
7. **No sourceless knowledge answers** — all estimates labeled as estimates
8. **No external action without approval** — execution_modes.yml, kill switch
9. **No agent without identity** — every agent has explicit identity declaration
10. **No project without Proof Pack** — proposal-seed-agent.md enforces this
11. **No project without Capital Asset** — proposal seed includes capital_asset_plan

---

## Data Flow Details

### Stage 1: Market Intelligence (Market Scanner)
- Sources: Public registries, industry directories, event lists, news
- Output: raw_leads.jsonl (company-level only, no PII)
- Quota: 20 new leads per run
- Suppression: Checked before writing any lead

### Stage 2: Company Research (Company Researcher)
- Input: raw_leads.jsonl entry
- Process: LLM call with public data → structured brief
- Thresholds: All 5 scores must meet minimums before proceeding
- Output: company_briefs.jsonl

### Stage 3: Routing (Offer Router + Channel Router)
- Offer: Waterfall logic based on sector + size + pain
- Channel: Routing rules from channel-router.yml
- Mode: auto_send | founder_approval | assisted_manual | inbound_only
- Anti-ban: Check before assigning any channel

### Stage 4: Asset Generation (Asset Generator)
- Templates: prompts/ directory — one per channel
- Framework: PAIN → SOLUTION → PROOF → CTA
- Word limits: email 150, WhatsApp 80, LinkedIn 200
- Output: channel_assets.jsonl

### Stage 5: Quality + Compliance Gates
- Quality: 8 criteria, 100 points total
- Compliance: Hard blocks + warnings per channel
- Decision: ready | founder_review | rewrite | reject
- Nothing proceeds below 70 points

### Stage 6: Execution
- Dry run: DRY_RUN=true → no sends
- Kill switch: GROWTH_OS_KILL_SWITCH=true → halt all
- Auto-send: email only, QA >= 90, non-sensitive
- Founder review: All sensitive, large company, non-email, QA 82-89
- Assisted manual: LinkedIn (always)
- Inbound only: Instagram, Messenger, Telegram

### Stage 7: Reply Management
- Classifier: 9 categories, AR + EN patterns
- SLA: unsubscribe = 0-15 min, interested = 2-4 hours
- Suppression: Immediate on unsubscribe or bounce
- Opportunities: Updated based on classification

### Stage 8: Learning Loop
- Daily: learning_engine.analyze_daily() at 23:00
- Weekly: learning_engine.generate_weekly_review() every Sunday
- Experiments: Propose and track A/B tests via experiments.yml
- Learning log: Appended daily to memory/learning_log.jsonl

---

## Governance Architecture

Every execution produces:
```json
{
  "governance_decision": "descriptive string of what decision was made and why",
  "proof_pack_planned": true,
  "capital_asset_planned": true,
  "pii_collected": false,
  "non_negotiables_checked": true
}
```

Every paid engagement produces:
- Proof Pack with score >= 70
- At least 1 Capital Asset
- Bilingual disclaimer on all customer-facing outputs

Every customer-facing markdown ends with:
"Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

---

## Decision Rules

| Condition | Action |
|-----------|--------|
| Revenue >= 40K SAR + 3 retainers by Day 90 | Propose Wave 3 (Enterprise Trust OS) |
| Revenue < 25K SAR by Day 60 | Stop building — double down on sales |
| Founder time > 5h/sprint after Customer 5 | Halt new sprint sales, push automation |
| Any non-negotiable violation | Refuse and explain safe alternative |

---

## File Structure Reference

```
growth-os/
  config/         — All YAML configuration
  memory/         — All JSONL data stores
  agents/         — Agent specification docs
  channels/       — Per-channel configuration
  prompts/        — LLM prompt templates
  outputs/        — Execution outputs
  *.py            — Python implementation modules
  *.md            — Documentation
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
