# Dealix Founder System Overview — How Everything Works Together

**Status:** All systems operational and ready for execution
**Start Date:** Tomorrow, 8:00 AM
**Goal:** 3 pilots by Day 30; 12 customers by Day 90

---

## QUICK START (Read This First)

### What is this system?

You have a complete founder execution system that automates:
- **Lead research** (Google Places API finds 50+ leads/day)
- **Lead qualification** (BANT scoring ranks them by close probability)
- **Sales approvals** (AI drafts objection responses; you approve/send)
- **Pilot delivery** (14-day sprint with daily checklists)
- **Proof tracking** (logs customer wins automatically)
- **Dashboard** (shows daily metrics + pending approvals)

### Your job (15-30 min/day):

1. **Morning (45 min):**
   - Check overnight funnel
   - Send 1 personal WhatsApp
   - Approve AI-drafted items
   - Check calendar

2. **As scheduled (30-60 min each):**
   - Run diagnostic calls

3. **Evening (15 min):**
   - Update tracking spreadsheet
   - Prepare tomorrow's outreach

### How to start:

**Tomorrow at 8:00 AM:**
```bash
bash scripts/dealix_founder_daily_complete.sh
```

This generates all your dashboards, qualified leads, and approval queue. Then follow the morning ritual in FOUNDER_DAILY_EXECUTION_PLAYBOOK.md.

---

## SYSTEM ARCHITECTURE

### Layer 1: Lead Research (Automated Daily)

**What it does:**
- Queries Google Places API for Saudi B2B companies
- Searches 5 high-priority sectors: Real Estate, Distribution, SaaS, Agencies, Restaurants
- Generates 50+ raw leads with phone, website, rating, address
- Scores by establishment signals (ratings, review count, business age)

**Output:**
- `company/runtime/places/{date}/real_leads.csv` — raw leads from Google
- `company/runtime/places/{date}/REAL_LEADS_REPORT.md` — markdown report of top 30

**Run manually:**
```bash
python company/leads/real_leads_engine.py
```

**Dependencies:**
- `GOOGLE_MAPS_API_KEY` environment variable (set in .env)

---

### Layer 2: Lead Qualification (Automated Daily)

**What it does:**
- Reads raw leads from real_leads_engine
- Scores for "warm intro potential" (0-100 scale)
- Requires: phone + name + sector weight ≥ 50 points
- Deduplicates against existing targets
- Generates daily report for founder review

**Scoring (max 100):**
- Base: 20 points
- Has phone: +25 (critical for WhatsApp)
- Has website: +10 (signals establishment)
- 100+ reviews: +15 (accessible decision maker)
- 4.5+ rating: +10 (trustworthy)
- Sector weight: varies by strategic priority

**Output:**
- `company/runtime/qualified_leads_{date}.json` — scored candidates
- `company/runtime/daily_qualified_leads_{date}.md` — founder-readable report

**Run manually:**
```bash
python company/sales/lead_qualification_engine.py
```

**Founder action:**
- Review `daily_qualified_leads_{date}.md`
- Identify which prospects you have warm intros for
- Copy promising ones to `/warm-intro-targets.csv`

---

### Layer 3: Sales Qualification Agent (Automated Daily)

**What it does:**
- Generates BANT qualification assessments (Budget, Authority, Need, Timeline)
- Drafts objection responses (5 types, Khaliji Arabic + English)
- Creates follow-up reminders (day 3, 7, 14 of pilot)
- Saves all to approval queue for founder review

**BANT Scoring (max 20 points):**
- Budget (5): Has discretionary budget?
- Authority (5): Can sign contracts?
- Need (5): Real pain? Major impact?
- Timeline (5): Will decide soon?

**Objection Handling (pre-written responses):**
1. "Too expensive" → Focus on ROI (each lost deal = 10K+ SAR)
2. "No time now" → Shows why (40h/week freed up)
3. "Using competitor tool" → Differentiation angle
4. "Need boss approval" → Founder meeting offer
5. "Let me think" → Video demo + 24h response SLA

**Output:**
- `company/runtime/approval_queue.json` — items awaiting approval

**Run manually:**
```bash
python company/sales/sales_qualification_agent.py
```

**Founder action:**
- Review `/decisions.html` each morning
- Approve, edit, or reject each item
- Approved items are sent automatically (no further action needed)

---

### Layer 4: Dashboard & Reporting (Automated Daily)

**Founder Dashboard (`founder_dashboard.html`):**
- Real-time metrics: warm intros, contacted, diagnostics, pilots signed
- Conversion rates: WhatsApp → diagnostic → pilot
- Pipeline value (in SAR)
- Status breakdown (ready, sent, completed, signed)

**Approvals Queue (`/decisions.html`):**
- Pending AI-drafted items (objections, follow-ups, diagnostics)
- Approve/reject interface
- Status tracking

**Lead Report (`daily_qualified_leads_{date}.md`):**
- Top 20 qualified prospects
- Sector, phone, recommended offer
- Direct WhatsApp links

---

### Layer 5: Pilot Delivery Orchestrator (On Demand)

**What it does:**
- When pilot is signed: Creates `/pilots/{pilot_id}/` directory
- Generates 14-day delivery schedule (5 phases)
- Daily checklist for founder (tasks + estimated hours)
- Proof pack template (case study structure)
- Event logging (tracks prospects added, follow-ups sent, deals advanced)

**14-Day Schedule:**
- **Days 1-3:** Onboarding & setup (3h founder time)
- **Days 4-7:** Daily support & monitoring (2h)
- **Days 8-11:** Proof accumulation (3h)
- **Days 12-14:** Final push & proof pack (4h)
- **Total:** ~12-15 hours founder time per pilot

**Outputs:**
- `/pilots/{pilot_id}/metadata.json` — pilot tracking record
- `/pilots/{pilot_id}/day1_checklist.json` — today's tasks
- `/pilots/{pilot_id}/contract.json` — pilot terms
- `/pilots/{pilot_id}/proof_pack_template.json` — case study structure
- `/pilots/{pilot_id}/proof_events.jsonl` — all customer wins logged

**Run when pilot is signed:**
```bash
python company/delivery/pilot_delivery_orchestrator.py
```

---

### Master Orchestrator (Daily, Automated)

**`scripts/dealix_founder_daily_complete.sh`**

Runs all 4 layers in sequence:
1. **Phase 1:** Lead research (Google Places)
2. **Phase 2:** Lead qualification (BANT scoring)
3. **Phase 3:** Sales agent (objections + follow-ups)
4. **Phase 4:** Dashboards (founder UI + reports)

**Output:**
- All dashboards ready
- Summary printed to console
- Log file: `company/runtime/daily_ritual_{date}.log`

**How to run:**
```bash
# Manual (anytime)
bash scripts/dealix_founder_daily_complete.sh

# Automated (daily at 8 AM)
# Add to crontab: 0 8 * * 1-5 cd /home/user/dealix && bash scripts/dealix_founder_daily_complete.sh
```

---

## YOUR DAILY WORKFLOW

### Morning (8:00-8:45 AM)

**Step 1: Run daily ritual (automated)**
```bash
bash scripts/dealix_founder_daily_complete.sh
```
All dashboards and approvals ready. Takes 30 seconds.

**Step 2: Check funnel (5 min)**
- Open `company/runtime/founder_dashboard.html` in browser
- Look for overnight diagnostics, replies, payment confirmations
- Reply to any demo requests (30-min SLA)

**Step 3: Send 1 warm WhatsApp (20 min)**
- Open `company/runtime/warm_intro_targets.csv`
- Pick prospect from "Ready" status who hasn't been contacted yet
- Draft personal message (Khaliji Arabic, no template)
- Mark "Sent"; note timestamp

**Step 4: Approve AI drafts (10 min)**
- Open `/decisions.html`
- Review 3-5 pending items:
  - Objection responses
  - Follow-up messages
  - Diagnostic summaries
- Approve or edit; send approved items
- Reject if needed (log as learnings)

**Step 5: Check calendar (5 min)**
- Any demos scheduled for today?
- If yes: review prospect company; prepare 1-pager
- If no: move on

### Demo Call (30 min, as scheduled)

Follow the demo script from FOUNDER_DAILY_EXECUTION_PLAYBOOK.md:
1. Opening (2 min): establish rapport
2. Discovery (8 min): listen more than talk
3. Pitch (5 min): show outcome, not features
4. Close (7 min): ask directly; handle objections
5. Post-call (5 min): update tracking immediately

### Evening (5:00-5:15 PM)

**Step 1: Update tracking (10 min)**
- Open `warm_intro_targets.csv`
- Update today's activities:
  - WhatsApps sent: ✅ or ❌
  - Demos completed: count
  - Outcomes: Yes, No, Maybe
  - Status: Sent, Completed Diagnostic, Pilot Signed, etc.

**Step 2: Prep tomorrow (5 min)**
- Identify tomorrow's warm WhatsApp prospect
- Draft message (don't send yet)
- Set phone reminder: 8:15 AM

---

## SUCCESS METRICS

### Daily
- [ ] 1 warm WhatsApp sent
- [ ] Approval queue reviewed (5 min)

### Weekly
- [ ] 5 WhatsApps sent
- [ ] 2-3 diagnostics completed
- [ ] 1 pilot signed (by week 2)

### Monthly (30 days)
- [ ] 20 warm intros contacted
- [ ] 8-10 diagnostics completed
- [ ] 3 pilots signed
- [ ] 1 pilot delivered
- [ ] 0-1 pilot renewed (proof of model)

### Quarter (90 days)
- [ ] 60 warm intros contacted
- [ ] 20+ diagnostics completed
- [ ] 12 pilots signed
- [ ] 6+ pilots delivered
- [ ] 5+ pilots renewed (MRR = 20K SAR+)

---

## CRITICAL FILES

| File | Purpose | Update Frequency | Owner |
|------|---------|------------------|-------|
| `/warm-intro-targets.csv` | Your prospect pipeline | Daily (evening) | Founder |
| `/founder_dashboard.html` | Real-time metrics | Generated daily (8 AM) | System |
| `/decisions.html` | AI-drafted approvals | Generated daily (8 AM) | System |
| `/daily_qualified_leads_{date}.md` | Top leads for manual review | Generated daily (8 AM) | System |
| `/pilots/{id}/metadata.json` | Pilot tracking | Auto-updated during sprint | System |
| `/pilots/{id}/proof_events.jsonl` | Proof events (append-only) | As events occur | System |
| `daily_ritual_{date}.log` | System execution log | Generated daily (8 AM) | System |

---

## TROUBLESHOOTING

### "I'm not seeing qualified leads in /decisions.html"

**Diagnosis:** Google Places API either not running or not returning results.

**Fix:**
1. Check GOOGLE_MAPS_API_KEY is set: `echo $GOOGLE_MAPS_API_KEY`
2. Manually run lead research: `python company/leads/real_leads_engine.py`
3. Check output: `ls -la company/runtime/places/$(date +%Y-%m-%d)/`

### "Demo conversion is low (< 30%)"

**Diagnosis:** Demo script or targeting needs adjustment.

**Fix:**
1. Review last 3 diagnostic call recordings
2. Compare against demo script (FOUNDER_DAILY_EXECUTION_PLAYBOOK.md)
3. Adjust one element: opening, pain probe, pitch, or close
4. Test 3 more prospects before further changes

### "Founder hours exceeding 40/week"

**Diagnosis:** Either too many demos scheduled or delivery work is expanding.

**Fix:**
1. Limit demos to 2 per day (3 pilots in parallel is max)
2. Stick to 14-day sprint timeline (no extensions)
3. Delegate unapproved work to next month

### "Pilot customer says 'need more time to decide' at Day 14"

**Diagnosis:** Proof pack not compelling enough; customer still evaluating.

**Fix:**
1. Offer 1 week extension (no charge) to see "more results"
2. During extension: show additional proof events (deals advanced, follow-ups automated)
3. Final decision point: Day 21

---

## ENVIRONMENT VARIABLES

Set in `.env` (gitignored):

```bash
# Google Places API
GOOGLE_MAPS_API_KEY=your_api_key_here

# Moyasar (payment processing)
MOYASAR_API_KEY=your_api_key_here
MOYASAR_API_SECRET=your_secret_here

# WhatsApp API (future: automated sending)
WHATSAPP_API_KEY=your_api_key_here
WHATSAPP_BUSINESS_ACCOUNT_ID=your_account_id_here

# Email (future: founder summaries)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=sami.assiri11@gmail.com
SMTP_PASSWORD=your_app_password_here
```

---

## NEXT IMMEDIATE ACTIONS

**Tomorrow at 8:00 AM:**

1. Run the system: `bash scripts/dealix_founder_daily_complete.sh`
2. Open three browser tabs:
   - `company/runtime/founder_dashboard.html`
   - `company/runtime/decisions.html`
   - `company/runtime/daily_qualified_leads_*.md`
3. Send your first warm WhatsApp (8:15 AM)
4. Approve 3 AI items (8:40 AM)
5. Log the time spent

**Friday (Day 5):**
- Review this week: 5 WhatsApps sent? 2 diagnostics booked?
- Adjust for next week based on results

**Day 30:**
- Target: 3 pilots signed, 1 delivered, clear proof of model

---

## FINAL WORDS

This system exists to automate everything EXCEPT the thing that matters most:

**You calling people and asking them directly: "ودك تجرب?"**

The dashboards, dashboards, lead scoring, objection handlers, approval queues — all support this single action.

When you're tired, when it feels hard, when you want to wait for "perfect conditions":

Remember: 1 WhatsApp per day × 5 days/week × 4 weeks = 20 WhatsApps = 1-2 pilot offers = revenue.

The market is waiting.

---

**Document Version:** 1.0
**Last Updated:** 2026-06-17
**Next Review:** 2026-06-24 (Day 7)

---

## Quick Reference Commands

```bash
# Generate all dashboards (run daily at 8 AM)
bash scripts/dealix_founder_daily_complete.sh

# Manual lead research (if not running automatically)
python company/leads/real_leads_engine.py

# Manual lead qualification (if not running automatically)
python company/sales/lead_qualification_engine.py

# Generate sales approvals (if not running automatically)
python company/sales/sales_qualification_agent.py

# Initialize a new pilot (when pilot is signed)
python company/delivery/pilot_delivery_orchestrator.py

# Check system health
tail -20 company/runtime/daily_ritual_$(date +%Y-%m-%d).log
```

