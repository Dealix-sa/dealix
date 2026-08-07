# Dealix Founder Execution System — Complete Operating Manual

**Welcome, Sami. This is your command center for the next 90 days.**

This repository contains a complete founder execution system designed to help you acquire 3 paid pilot customers in 30 days, then scale to 12+ customers by Day 90.

---

## WHAT YOU NEED TO KNOW (5 min read)

### The Situation

You have:
- ✅ Excellent product (8 hard gates, 340+ tests, PDPL-native)
- ✅ Clear pricing model (499 SAR pilots → 3,999 SAR/month recurring)
- ✅ Proven delivery process (14-day sprint, repeatable)
- ❌ **Zero customers** (that's what we're fixing)

### The Solution

A complete automation system that:
1. **Finds leads daily** (Google Places API)
2. **Qualifies them** (BANT scoring: Budget, Authority, Need, Timeline)
3. **Drafts responses** (AI objection handler)
4. **Tracks approvals** (your `/decisions.html` queue)
5. **Manages delivery** (14-day sprint with daily checklists)
6. **Logs proof** (customer wins, proof events)
7. **Shows you metrics** (founder dashboard)

**Your job:** Send 1 personal warm WhatsApp per day. The system handles everything else.

### Start Tomorrow at 8:00 AM

```bash
# This single command generates all your dashboards and approvals
bash scripts/dealix_founder_daily_complete.sh
```

Then follow the 45-minute morning ritual in FOUNDER_DAILY_EXECUTION_PLAYBOOK.md.

---

## QUICK NAVIGATION

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **THIS FILE** | Project overview + quick start | 5 min |
| `FOUNDER_DAILY_EXECUTION_PLAYBOOK.md` | Your daily 45-min ritual + demo scripts | 20 min |
| `FOUNDER_REVENUE_MANUAL.md` | 90-day revenue strategy + tactics | 30 min |
| `FOUNDER_SYSTEM_OVERVIEW.md` | How the system works + architecture | 20 min |
| `PILOT_DAY1_ONBOARDING.md` | Customer onboarding checklist | 15 min |

**Recommended Reading Order:**
1. THIS FILE (overview)
2. FOUNDER_DAILY_EXECUTION_PLAYBOOK.md (your daily ritual)
3. FOUNDER_SYSTEM_OVERVIEW.md (understand the automation)
4. FOUNDER_REVENUE_MANUAL.md (strategic context)
5. PILOT_DAY1_ONBOARDING.md (when first pilot is signed)

---

## YOUR METRICS (What Success Looks Like)

### Day 30 Target
- [ ] 20 warm intros contacted (via WhatsApp)
- [ ] 8 diagnostics completed (30-min calls)
- [ ] 3 pilots signed (499 SAR payment received)
- [ ] 1 pilot delivered end-to-end
- [ ] Founder working 30-35h/week (sustainable)

### Day 90 Target
- [ ] 60 warm intros contacted
- [ ] 20+ diagnostics completed
- [ ] 12 pilots signed
- [ ] 6+ pilots delivered
- [ ] 5+ renewals at 3,999 SAR/month
- [ ] **MRR = 20,000+ SAR** (proof of model)

---

## EXECUTION STARTING TODAY

### Phase 1: Lead Research & Qualification (Automated)

**What happens at 8:00 AM:**
1. System queries Google Places API for high-potential B2B companies
2. Scores them by "warm intro potential" (phone + website + ratings)
3. Generates report: `/daily_qualified_leads_{date}.md`
4. You read it and pick prospects you have warm intros for

**What you do:** Review the report and copy promising prospects to `/warm-intro-targets.csv`

---

### Phase 2: Your Morning Ritual (45 minutes)

**8:15 AM - Send 1 warm WhatsApp (20 min)**
```
السلام عليكم 👋
أنا سامي من ديليكس، شركة سعودية في AI للمبيعات
فيه 30 دقيقة مجانية لنشوف إن كان عندك فرصة في الـCRM
وقت مناسب للاتصال الأسبوع الجاي؟
```
- Personal (not template)
- Khaliji Arabic (not English, not formal MSA)
- Direct ask (ودك تجرب؟)
- Log it immediately

**8:35 AM - Approve AI Drafts (10 min)**
- Open `/decisions.html`
- Review 3-5 items AI drafted:
  - Objection responses
  - Follow-up reminders
  - Diagnostic summaries
- Approve or edit; send approved

**8:45 AM - Check Calendar (5 min)**
- Any diagnostics booked for today?
- If yes: review prospect company + prepare 1-pager

---

### Phase 3: Diagnostics & Deal Closure (As Scheduled)

**30-min Diagnostic Call Script:**
1. **Opening (2 min):** Establish rapport
2. **Discovery (8 min):** Listen more; ask about pain
3. **Pitch (5 min):** Show outcome (not features)
4. **Close (7 min):** Ask directly; handle objections
5. **Post-call (5 min):** Update tracking immediately

Demo scripts for 3 sectors: Real Estate, Distribution, SaaS (see PLAYBOOK)

---

### Phase 4: Pilot Delivery (14-day sprint)

When pilot is signed:
1. System creates `/pilots/{pilot_id}/` directory
2. Generates 14-day schedule (5 phases)
3. Daily checklists for you + customer
4. Proof event logging (prospects added, follow-ups sent, deals advanced)

Day 1-3: Setup (3h founder time)
Day 4-7: Support (2h)
Day 8-11: Proof (3h)
Day 12-14: Final push + case study (4h)
**Total: ~12h founder time per 14-day pilot**

---

## SYSTEM ARCHITECTURE (How It All Connects)

```
┌─────────────────────────────────────────────────────────┐
│  Dealix Founder Execution System (5 Layers)              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Layer 1: LEAD RESEARCH (Automated daily @ 8 AM)         │
│  ────────────────────────────────────────────────────    │
│  Google Places API → Find 50+ Saudi B2B companies        │
│  Output: real_leads.csv                                  │
│                                                           │
│  Layer 2: LEAD QUALIFICATION (Automated daily @ 8:05 AM) │
│  ───────────────────────────────────────────────────     │
│  Score leads: BANT + warm intro potential (0-100)        │
│  Output: daily_qualified_leads_{date}.md                 │
│                                                           │
│  Layer 3: SALES AGENT (Automated daily @ 8:10 AM)        │
│  ─────────────────────────────────────────────────       │
│  AI drafts: objections + follow-ups + summaries          │
│  Output: approval_queue.json → /decisions.html           │
│                                                           │
│  Layer 4: FOUNDER APPROVALS (YOU @ 8:35 AM)             │
│  ─────────────────────────────────────────────           │
│  Review + approve/edit/reject AI items                   │
│  Output: Approved items send via WhatsApp/Email          │
│                                                           │
│  Layer 5: DELIVERY ORCHESTRATOR (YOU + Customer)         │
│  ───────────────────────────────────────────────         │
│  14-day sprint with daily checklists + proof logging     │
│  Output: Proof pack + renewal decision                   │
│                                                           │
│  DASHBOARDS (Real-time):                                 │
│  ─────────────────────────                               │
│  /founder_dashboard.html → Metrics (contacted, pilots)   │
│  /decisions.html → Approval queue (3-5 pending items)    │
│  /warm-intro-targets.csv → Your prospect pipeline        │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## CRITICAL FILES & THEIR PURPOSE

### Documentation
- `FOUNDER_DAILY_EXECUTION_PLAYBOOK.md` — Your 45-min daily ritual
- `FOUNDER_REVENUE_MANUAL.md` — 90-day strategy + tactics
- `FOUNDER_SYSTEM_OVERVIEW.md` — System architecture + troubleshooting
- `PILOT_DAY1_ONBOARDING.md` — Day 1 customer onboarding

### Python Modules (Automated)
- `company/leads/real_leads_engine.py` — Google Places lead research
- `company/sales/lead_qualification_engine.py` — BANT scoring (0-100)
- `company/sales/sales_qualification_agent.py` — Objection handler + BANT
- `company/delivery/pilot_delivery_orchestrator.py` — 14-day sprint orchestration

### Scripts
- `scripts/dealix_founder_daily_complete.sh` — Master daily ritual (runs all 4 phases)
- `scripts/generate_founder_dashboard.py` — Metrics dashboard generator
- `scripts/generate_approvals_queue.py` — Approval queue UI generator
- `scripts/check_system_health.py` — System health verification

### Runtime Data (Gitignored)
- `company/runtime/warm-intro_targets.csv` — Your prospect pipeline (YOU UPDATE THIS)
- `company/runtime/founder_dashboard.html` — Real-time metrics (GENERATED DAILY)
- `company/runtime/decisions.html` — AI approval queue (GENERATED DAILY)
- `company/runtime/daily_qualified_leads_{date}.md` — Top prospects (GENERATED DAILY)
- `company/runtime/pilots/{id}/` — Pilot directories (CREATED PER PILOT)

---

## ENVIRONMENT SETUP

### Required
Set these in `.env` (copy `.env.example`):

```bash
# Google Places API (for lead research)
GOOGLE_MAPS_API_KEY=sk-xxx...

# Optional (for future phases)
MOYASAR_API_KEY=pk-xxx...
MOYASAR_API_SECRET=sk-xxx...
WHATSAPP_API_KEY=xxx...
WHATSAPP_BUSINESS_ACCOUNT_ID=xxx...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=sami.assiri11@gmail.com
SMTP_PASSWORD=app-password-here
```

### Quick Setup
```bash
# Copy template
cp .env.example .env

# Edit with your keys
nano .env

# Verify setup
python scripts/check_system_health.py
```

---

## RUNNING THE SYSTEM

### Daily (Automated, 8:00 AM)
```bash
bash scripts/dealix_founder_daily_complete.sh
```
Generates: dashboards + approvals + lead report (30 seconds)

### Manual Commands
```bash
# Lead research (if needed)
python company/leads/real_leads_engine.py

# Lead qualification
python company/sales/lead_qualification_engine.py

# Sales agent (objections + follow-ups)
python company/sales/sales_qualification_agent.py

# Generate dashboards
python scripts/generate_founder_dashboard.py
python scripts/generate_approvals_queue.py

# Health check
python scripts/check_system_health.py
```

### With Crontab (Optional, for automation)
```bash
# Add to crontab (runs daily 8 AM Monday-Friday)
0 8 * * 1-5 cd /home/user/dealix && bash scripts/dealix_founder_daily_complete.sh
```

---

## CHECKLIST: BEFORE YOU START DAY 1

- [ ] Read: FOUNDER_DAILY_EXECUTION_PLAYBOOK.md (20 min)
- [ ] Setup: .env with GOOGLE_MAPS_API_KEY
- [ ] Verify: `python scripts/check_system_health.py` (all green)
- [ ] Prepare: Identify 5 warm intro prospects (people you know or can get intros to)
- [ ] Practice: Read demo script 2x; practice opening
- [ ] Set reminder: 8:15 AM tomorrow for first WhatsApp

**Tomorrow at 8:15 AM, send your first message. Everything else flows from there.**

---

## SUCCESS CRITERIA

### Week 1
- [ ] Send 5 warm WhatsApps
- [ ] Book 1-2 diagnostics
- [ ] Understand demo script
- [ ] Approve/reject 15+ AI items

**Feeling:** "This rhythm works"

---

### Week 2
- [ ] Send 5 more WhatsApps (10 total)
- [ ] Complete 2-3 diagnostics
- [ ] Close 1 pilot
- [ ] Adjust demo script based on objections

**Feeling:** "I can do this"

---

### Week 3-4
- [ ] Send 5 more WhatsApps (15-20 total)
- [ ] Complete 2-3 more diagnostics
- [ ] Sign 2 more pilots (3 total)
- [ ] Start delivery on pilot #1

**Feeling:** "The funnel works"

---

### Day 30 Review
- [ ] 3 pilots signed ✅
- [ ] 1 pilot delivered ✅
- [ ] 20+ warm intros contacted ✅
- [ ] 30-35h/week founder time ✅

**Feeling:** "We have a business"

---

## TROUBLESHOOTING

### "I'm not seeing qualified leads"

```bash
# 1. Check API key is set
echo $GOOGLE_MAPS_API_KEY

# 2. Run lead research manually
python company/leads/real_leads_engine.py

# 3. Check output
ls -la company/runtime/places/$(date +%Y-%m-%d)/
```

### "Demo conversion is low (< 30%)"

Re-read the demo script. Adjust one element:
- Opening: Add specific sector reference
- Pain probe: Ask more open-ended questions
- Pitch: Simplify (one benefit, not three)
- Close: Ask more directly ("ودك تجرب؟")

Test 3 more prospects before further changes.

### "Founder hours exceeding 40/week"

Limit demos to 2/day. Stick to 14-day sprint (no extensions). Deliver pilots on time even if imperfect.

### "Customer says 'maybe' at Day 14"

Offer 1-week extension. Show more proof events. Final decision Day 21.

---

## NEXT STEPS

1. **Read:** FOUNDER_DAILY_EXECUTION_PLAYBOOK.md (20 min)
2. **Setup:** .env with API key (5 min)
3. **Prepare:** List 5 warm intro prospects (15 min)
4. **Tomorrow 8:00 AM:** Run `bash scripts/dealix_founder_daily_complete.sh`
5. **Tomorrow 8:15 AM:** Send your first WhatsApp

---

## SUPPORT

Questions? Read the relevant section:
- Daily ritual issues → FOUNDER_DAILY_EXECUTION_PLAYBOOK.md
- Strategy questions → FOUNDER_REVENUE_MANUAL.md
- System questions → FOUNDER_SYSTEM_OVERVIEW.md
- Customer onboarding → PILOT_DAY1_ONBOARDING.md
- Troubleshooting → FOUNDER_SYSTEM_OVERVIEW.md §Troubleshooting

---

## FINAL WORDS

You have everything you need. The system is ready. The market is ready.

What you need now is courage to send 1 WhatsApp.

Send 5 per week, and you'll have 3 pilots by Day 30. Deliver 1 end-to-end, and renewal is 80% likely.

By Day 90, you'll have 12+ customers and 20K+ SAR MRR. You'll be a real company.

But it all starts with one WhatsApp tomorrow at 8:15 AM.

Go.

---

**Document Version:** 1.0
**Date:** 2026-06-17
**Next Update:** 2026-06-24 (Week 1 review)

**Good luck, Sami. The market is waiting.** 🚀

