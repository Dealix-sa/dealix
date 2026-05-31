# Dealix Growth OS — Founder Control Center
# مركز تحكم المؤسس — ديليكس Growth OS

**Version:** 1.0 | **Date:** 2026-05-31
**Implemented in:** `founder_dashboard.py`

---

## Overview / نظرة عامة

The Founder Control Center gives you 6 real-time dashboard screens and a daily brief. All data comes from the memory/ JSONL files. No external API calls in the dashboard layer.

Run your daily brief:
```bash
python -c "
from growth_os.founder_dashboard import FounderDashboard
d = FounderDashboard()
print(d.generate_daily_brief())
"
```

---

## Screen 1: Growth Production / إنتاج النمو

**Method:** `get_growth_production(date)`

**What you see:**
| Metric | Description |
|--------|-------------|
| new_leads_discovered | New companies added to raw_leads.jsonl today |
| company_briefs_completed | Briefs fully researched and scored |
| drafts_created | Channel assets generated |
| drafts_ready_auto_send | Passed QA >= 90, queued for send |
| drafts_pending_founder_review | Awaiting your approval in founder_review/ |
| jobs_queued | Total jobs in execution queue |

**Healthy daily numbers (at scale):**
- 10-20 new leads discovered
- 8-15 briefs completed
- 6-12 drafts created
- 3-6 ready to auto-send
- 2-4 pending your review (review daily, do not let sit > 24h)

---

## Screen 2: Channel Execution / تنفيذ القنوات

**Method:** `get_channel_execution(date)`

**What you see:**
- By-channel breakdown: sent / queued / paused / rejected
- Count of jobs pending your approval
- List of pending jobs (up to 10)

**Action trigger:** If pending_founder_approval > 0, review in `outputs/founder_review/`

**To approve a draft:**
1. Read the draft file in `outputs/founder_review/`
2. Edit if needed
3. Set `approved_by: "founder"` and `approved_at: "ISO8601 timestamp"`
4. Move file to `outputs/execution_queue/`
5. Update job status in `memory/channel_jobs.jsonl` to "queued"

---

## Screen 3: Health and Risk / الصحة والمخاطر

**Method:** `get_health_risk(date)`

**Risk Levels:**
| Level | Color | Meaning |
|-------|-------|---------|
| green | GREEN | All clear — continue |
| yellow | YELLOW | Monitor — review warnings |
| red | RED | STOP — investigate immediately |

**When red:**
1. Check `memory/warnings.jsonl` for active warnings
2. Check email provider (Postmaster Tools) for bounce/spam rate
3. Check WhatsApp Business Manager for block rate
4. Fix the root cause
5. Manually resume channel after fix

**Warning types and actions:**

| Warning | Cause | Action |
|---------|-------|--------|
| email bounce > 5% | Bad email list | Clean list, suppress bounced |
| email spam > 0.3% | Content or reputation | Review subject lines, check SPF |
| whatsapp block > 2% | Unwanted messages | Review opt-in list, pause |
| stuck jobs > 48h | Founder not reviewing | Clear founder_review queue |

---

## Screen 4: Sales Pipeline / خط المبيعات

**Method:** `get_sales_pipeline(date)`

**Pipeline Stages:**

```
new → outreach_sent → replied → nurturing → 
discovery_call_scheduled → discovery_call_completed → 
proposal_sent → proposal_reviewed → 
closed_won | closed_not_interested | closed_no_response
```

**What you see:**
- Total open opportunities + weighted pipeline value (SAR)
- Opportunities needing action (with next_action)
- Recent positive replies count

**Priority focus (review daily):**
1. discovery_call_requested → book the call within 24h
2. pricing_shared → follow up within 48h
3. founder_escalation_required → you must respond, not the system

**Pipeline health benchmarks:**
- Reply rate >= 2% (of sends)
- Positive reply rate >= 0.5%
- Call booking from positive: >= 20%
- Proposal from discovery call: >= 30%
- Close from proposal: >= 10%

---

## Screen 5: Segment Performance / أداء الشرائح

**Method:** `get_segment_performance(date)`

**What you see:**
- All segments (sector × country) ranked by positive reply rate
- Best segment (double down here)
- Worst segment (pause or pivot)

**Decision rules:**
- positive_reply_rate >= 2% → double outreach volume in this segment
- positive_reply_rate < 0.5% after 20+ sends → pause segment, test new angle
- reply_rate >= 5% → excellent — this is a high-priority segment

**Weekly action based on segment performance:**
1. Identify top 2 segments
2. Increase leads per week in those segments
3. Identify bottom segment with > 20 sends and < 0.5% positive rate
4. Pause outreach, propose new experiment (new angle, different offer, different channel)

---

## Screen 6: Founder Actions Today / إجراءات المؤسس اليوم

**Method:** `get_founder_actions_today(date)`

**Priority levels:**
| Priority | Label | Examples |
|----------|-------|---------|
| 1 | CRITICAL | Channel paused by anti-ban, active warning |
| 2 | HIGH | Drafts awaiting approval, interested replies |
| 3 | HIGH | Hot opportunities needing follow-up |
| 4 | MEDIUM | Learning review, experiment decisions |
| 5 | LOW | Weekly review (Sunday only) |

**Maximum 5 action items per day.** If more than 5 are generated, only the top 5 by priority are shown.

**Daily rhythm (30 minutes total):**
```
07:00 — Read daily brief from outputs/daily/YYYY-MM-DD.md
07:10 — Review and approve pending drafts in outputs/founder_review/
07:20 — Respond to interested/pricing replies from memory/replies.jsonl
07:25 — Resolve any active warnings
07:30 — Back to client work
```

---

## Weekly Review (Every Sunday)

**Method:** `learning_engine.generate_weekly_review()`

7 questions to answer before the new week:
1. What was the best performing segment this week?
2. What is the overall reply rate vs. 2% target?
3. Which channel produced the best positive replies?
4. Were there any doctrine violations in the audit trail?
5. What experiments should we start next week?
6. Which segments should we pause or double down on?
7. Are we on track for the 90-day revenue target?

**90-Day Revenue Check:**
- Day 30 target: First paid sprint or data pack
- Day 60 check: Revenue >= 25K SAR? If not → stop building, focus on sales
- Day 90 target: 8-15K SAR MRR + 30-40K SAR one-time

---

## Kill Switch (Emergency Stop)

To halt ALL outreach immediately:
```bash
export GROWTH_OS_KILL_SWITCH=true
```

To resume:
```bash
export GROWTH_OS_KILL_SWITCH=false
```

The kill switch is checked before every execution. Nothing sends while it is active.

---

## Dry Run Mode (Testing)

To run all pipeline steps without sending anything:
```bash
export DRY_RUN=true
```

Use dry run to:
- Test new segments
- Validate acceptance tests
- Review quality scores before launch

---

## Important File Locations

| File | Purpose |
|------|---------|
| `outputs/founder_review/` | Drafts awaiting your approval |
| `outputs/daily/YYYY-MM-DD.md` | Daily brief |
| `memory/warnings.jsonl` | Active channel warnings |
| `memory/learning_log.jsonl` | Daily learning analysis |
| `memory/opportunities.jsonl` | Sales pipeline |
| `memory/replies.jsonl` | All inbound replies |
| `memory/suppression.jsonl` | Suppressed contacts |

---

## Non-Negotiables Reminder

The system enforces these automatically, but the founder should know them:
1. No cold WhatsApp — always opt-in first
2. No LinkedIn automation — you send manually
3. No scraping — blocked at architecture level
4. No guaranteed ROI claims — ever
5. Every paid project needs a Proof Pack (score >= 70)

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
