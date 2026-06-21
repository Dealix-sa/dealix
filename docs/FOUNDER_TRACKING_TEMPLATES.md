# Founder Tracking Templates

**Purpose:** Ready-to-use CSV/JSON templates for daily founder execution and metrics tracking.

---

## 1. WARM INTRO TARGETS TRACKING

**File:** `company/runtime/warm_intro_targets.csv`

**Format:**
```csv
rank,name,company,sector,phone,email,status,whatsapp_sent_date,whatsapp_response,diagnostic_scheduled,diagnostic_date,diagnostic_outcome,pilot_signed,pilot_date,pilot_id,notes
1,محمد الأحمد,العقارات السعودية,Real Estate,+966501234567,m.alahmed@example.com,Contacted,2026-06-17,Pending,False,,,,False,,,"Founded 2015, 50+ brokers"
2,فهد المحيسن,توزيع الرياض,Distribution,+966502345678,fahad@distribution.com,Not Contacted,,,False,,,,False,,,"Warehousing, 100+ employees"
3,سارة العتيبي,تقنيات ذكية,SaaS,+966503456789,sarah@smarttech.com,Not Contacted,,,False,,,,False,,,"AI consulting, growing fast"
4,عبدالعزيز النقيان,مقاولات النقيان,Real Estate,+966504567890,az.naqqayan@example.com,Contacted,2026-06-17,No Response,False,,,,False,,,"Large real estate firm"
5,لطيفة الدعيج,وكالات التأمين,Insurance,+966505678901,latifa@insurance.com,Not Contacted,,,False,,,,False,,,"Insurance brokers"
```

**Columns Explained:**
- **rank:** Priority order (1-50)
- **name:** Arabic name (use Arabic)
- **company:** Company name (Arabic)
- **sector:** Real Estate / Distribution / SaaS / Consulting / Insurance / Other
- **phone:** +966XXXXXXXXX format
- **email:** Work email
- **status:** Not Contacted / Contacted / Scheduled / Completed / Closed / No
- **whatsapp_sent_date:** YYYY-MM-DD when message sent
- **whatsapp_response:** Pending / Yes / No / Maybe / Not Responded
- **diagnostic_scheduled:** True/False
- **diagnostic_date:** YYYY-MM-DD HH:MM
- **diagnostic_outcome:** Closed / No / Maybe / Not Yet
- **pilot_signed:** True/False
- **pilot_date:** YYYY-MM-DD when pilot payment received
- **pilot_id:** UUID if signed (e.g., pilot_20260617_001)
- **notes:** Any context (founded year, size, pain points, objection)

**Daily Update Instructions:**
1. After sending WhatsApp at 8:15 AM: Mark `whatsapp_sent_date`, set `status="Contacted"`
2. When response arrives: Update `whatsapp_response`
3. When diagnostic booked: Set `diagnostic_scheduled=True`, add date
4. After diagnostic: Update `diagnostic_outcome`
5. If closed: Set `pilot_signed=True`, add `pilot_date`, generate `pilot_id`

**Excel/Google Sheets Tracking:**
- Sort by `status` to see all "Contacted" prospects together
- Filter by `sector` to focus on one market
- Use conditional formatting:
  - Green: Closed pilots
  - Blue: Diagnostics scheduled
  - Yellow: WhatsApp sent, awaiting response
  - Gray: Not yet contacted

---

## 2. DAILY RITUAL LOG

**File:** `company/runtime/daily_ritual_{YYYY-MM-DD}.log`

**Format (JSON Lines):**
```json
{"timestamp":"2026-06-17T08:00:00+03:00","phase":"automation","status":"completed","duration_sec":32,"leads_found":47,"leads_qualified":13}
{"timestamp":"2026-06-17T08:15:30+03:00","phase":"whatsapp","status":"sent","recipient":"محمد الأحمد","phone":"+966501234567","company":"العقارات السعودية"}
{"timestamp":"2026-06-17T08:35:00+03:00","phase":"approvals","status":"started","items_in_queue":5}
{"timestamp":"2026-06-17T08:38:45+03:00","phase":"approvals","status":"approved","item_type":"objection_response","item_index":1,"action":"approved"}
{"timestamp":"2026-06-17T08:41:30+03:00","phase":"approvals","status":"approved","item_type":"followup_reminder","item_index":2,"action":"approved"}
{"timestamp":"2026-06-17T08:43:15+03:00","phase":"approvals","status":"rejected","item_type":"diagnostic_summary","item_index":3,"action":"rejected"}
{"timestamp":"2026-06-17T08:45:00+03:00","phase":"calendar","status":"checked","diagnostics_today":0}
{"timestamp":"2026-06-17T17:00:00+03:00","phase":"tracking","status":"updated","whatsapps_sent":1,"approvals_processed":3,"metrics_logged":true}
```

**Log Entry Fields:**
- **timestamp:** ISO 8601 datetime (includes timezone)
- **phase:** automation / whatsapp / approvals / calendar / tracking / diagnostic / pilot
- **status:** completed / started / approved / rejected / sent / received / closed / error
- **Additional fields:** Phase-specific data

**How to Use:**
1. Scripts auto-generate this file at `company/runtime/daily_ritual_{date}.log`
2. Check end-of-day: `tail -20 company/runtime/daily_ritual_*.log`
3. Weekly analysis: Aggregate logs to measure consistency
4. Troubleshooting: Find errors by searching for `"status":"error"`

---

## 3. DIAGNOSTIC CALL TRACKER

**File:** `company/runtime/diagnostics_{YYYY-MM}.json`

**Format:**
```json
{
  "date_month": "2026-06",
  "diagnostics": [
    {
      "id": "diag_20260617_001",
      "date": "2026-06-17T10:30:00+03:00",
      "prospect_name": "محمد الأحمد",
      "prospect_company": "العقارات السعودية",
      "sector": "Real Estate",
      "phone": "+966501234567",
      "duration_minutes": 32,
      "opening_success": true,
      "discovery_quality": 8,
      "pain_points": [
        "Lost 50 deals last quarter due to poor follow-up",
        "CRM is outdated, team uses WhatsApp only",
        "No visibility into pipeline"
      ],
      "current_solution": "Manual WhatsApp + Excel",
      "pitch_effectiveness": 7,
      "close_attempt": true,
      "close_outcome": "Maybe",
      "objection_raised": "Need boss approval",
      "objection_response_used": "Founder meeting offer",
      "next_steps": "Send 24h video demo",
      "close_probability": 0.6,
      "followup_date": "2026-06-21",
      "follow_up_method": "WhatsApp",
      "notes": "Strong pain, good fit, needs internal approval"
    },
    {
      "id": "diag_20260620_001",
      "date": "2026-06-20T14:15:00+03:00",
      "prospect_name": "فهد المحيسن",
      "prospect_company": "توزيع الرياض",
      "sector": "Distribution",
      "phone": "+966502345678",
      "duration_minutes": 28,
      "opening_success": true,
      "discovery_quality": 9,
      "pain_points": [
        "Sales reps not following up (40% fall-through rate)",
        "Can't track deals in real-time",
        "Lost 200K SAR in Q1 due to poor pipeline"
      ],
      "current_solution": "Salesforce (but not using it well)",
      "pitch_effectiveness": 8,
      "close_attempt": true,
      "close_outcome": "Closed",
      "objection_raised": null,
      "objection_response_used": null,
      "next_steps": "Send contract, schedule pilot onboarding",
      "close_probability": 1.0,
      "pilot_signed": true,
      "pilot_date": "2026-06-20",
      "pilot_id": "pilot_20260620_001",
      "notes": "Immediate yes, strong urgency, high value"
    }
  ],
  "summary": {
    "total_diagnostics": 2,
    "closed": 1,
    "no": 0,
    "maybe": 1,
    "close_rate": 0.5,
    "average_discovery_quality": 8.5,
    "average_pitch_effectiveness": 7.5,
    "most_common_pain": "Poor follow-up / pipeline visibility",
    "most_common_objection": "Need approval",
    "next_month_forecast_pilots": 4,
    "next_month_forecast_revenue": "1,996 SAR (4 × 499)"
  }
}
```

**How to Use:**
1. Script generates this after each diagnostic
2. Review weekly: Open file, check summary section
3. Identify patterns: Which sectors convert best? Which pain points? Which objections?
4. Adjust pitch: If close_rate < 50%, review transcripts and adjust
5. Forecast: Use average rates to predict Month 2

**Monthly Analysis:**
- Average discovery quality (0-10): Is your listening strong?
- Average pitch effectiveness (0-10): Is your message clear?
- Close rate: What % of diagnostics → pilots?
- Pain point frequency: What are top 3 pains across all prospects?

---

## 4. APPROVAL QUEUE TRACKING

**File:** `company/runtime/approval_queue_history_{YYYY-MM-DD}.json`

**Format:**
```json
{
  "date": "2026-06-17",
  "timestamp": "2026-06-17T08:00:00+03:00",
  "total_items": 5,
  "items": [
    {
      "id": "item_001",
      "type": "objection_response",
      "lead_name": "محمد الأحمد",
      "lead_phone": "+966501234567",
      "lead_company": "العقارات السعودية",
      "objection": "Too expensive",
      "draft_ar": "حسناً، بفهمك اللي تقول\nلكن تخيل إنك تخسر عقد واحد بـ 100K ريال\nالحل اللي نقدمه يساعدك تحفظ العقد...",
      "draft_en": "I understand what you're saying...",
      "founder_action": "approved",
      "action_timestamp": "2026-06-17T08:37:00+03:00",
      "action_time_minutes": 2,
      "edit_notes": null
    },
    {
      "id": "item_002",
      "type": "followup_reminder",
      "lead_name": "فهد المحيسن",
      "lead_phone": "+966502345678",
      "lead_company": "توزيع الرياض",
      "followup_day": 3,
      "draft_ar": "السلام عليكم يا فهد 👋\nأتمنى كل شي تمام بعد اليومين\nشمعة نشتغل بـ 30 دقيقة مجانية يوم الأربعاء؟",
      "draft_en": "Hi Fahad, hope all is well...",
      "founder_action": "approved",
      "action_timestamp": "2026-06-17T08:40:00+03:00",
      "action_time_minutes": 1,
      "scheduled_send": "2026-06-20T08:00:00+03:00"
    },
    {
      "id": "item_003",
      "type": "diagnostic_summary",
      "lead_name": "سارة العتيبي",
      "lead_phone": "+966503456789",
      "lead_company": "تقنيات ذكية",
      "summary": "Prospect interested in AI for sales, but needs founder approval from CTO",
      "founder_action": "rejected",
      "action_timestamp": "2026-06-17T08:42:00+03:00",
      "action_time_minutes": 1,
      "rejection_reason": "Not her decision, skip for now"
    },
    {
      "id": "item_004",
      "type": "objection_response",
      "lead_name": "عبدالعزيز النقيان",
      "lead_phone": "+966504567890",
      "lead_company": "مقاولات النقيان",
      "objection": "Need boss approval",
      "draft_ar": "ما فيه مشكلة 👍\nبنقدر نعمل meeting مع الـ boss الأسبوع الجاي؟\nبنوديهم الحل بـ 30 دقيقة فقط وبدون أي التزام",
      "draft_en": "No problem at all...",
      "founder_action": "edited",
      "action_timestamp": "2026-06-17T08:43:30+03:00",
      "action_time_minutes": 2,
      "edit_from": "ما فيه مشكلة 👍\nبنقدر نعمل meeting مع الـ boss الأسبوع الجاي؟",
      "edit_to": "تمام تمام 👍\nخلاص، إن شاء الله نعمل meeting مع الـ boss الأسبوع الجاي\nأنا سامي، بأكون سعيد نشرح الحل ليهم\nوقت مناسب الثلاثاء أو الأربعاء؟",
      "founder_action_after_edit": "sent"
    },
    {
      "id": "item_005",
      "type": "followup_reminder",
      "lead_name": "لطيفة الدعيج",
      "lead_phone": "+966505678901",
      "lead_company": "وكالات التأمين",
      "followup_day": 7,
      "draft_ar": "السلام عليكم يا لطيفة 👋\nبعد أسبوع من الدايركت اللي قلنا فيها...",
      "draft_en": "Hi Latifa, following up...",
      "founder_action": "pending",
      "action_timestamp": null,
      "action_time_minutes": null
    }
  ],
  "summary": {
    "total_items": 5,
    "approved": 2,
    "edited_and_sent": 1,
    "rejected": 1,
    "pending": 1,
    "total_approval_time_minutes": 6,
    "average_time_per_item_minutes": 1.2
  }
}
```

**How to Use:**
1. Review daily at 8:35 AM: Open /decisions.html
2. For each item: Approve, edit, or reject
3. Log automatically tracks your action + timestamps
4. Weekly analysis:
   - Do you reject > 10%? (Maybe agent is poor quality)
   - Do edits take >2 min each? (Maybe improve agent prompts)
   - Are certain lead types rejected more? (Maybe adjust scoring)

---

## 5. PILOT DELIVERY TRACKER

**File:** `company/runtime/pilots/{pilot_id}/delivery_log.json`

**Format:**
```json
{
  "pilot_id": "pilot_20260620_001",
  "customer_name": "فهد المحيسن",
  "customer_company": "توزيع الرياض",
  "customer_phone": "+966502345678",
  "customer_email": "fahad@distribution.com",
  "sector": "Distribution",
  "pilot_start_date": "2026-06-21",
  "pilot_end_date": "2026-07-04",
  "contract_amount": "499 SAR",
  "renewable_amount": "3,999 SAR/month",
  "founder_hours_budget": 12,
  "founder_hours_actual": 0,
  "phases": {
    "onboarding": {
      "phase": 1,
      "days": "1-3",
      "hours_budget": 3,
      "hours_actual": 0,
      "status": "planned",
      "checklist": [
        {
          "task": "Day 1 onboarding call (1h)",
          "completed": false,
          "date": null,
          "notes": "Scheduled: 2026-06-21 at 3 PM"
        },
        {
          "task": "Database setup and initial config (1h)",
          "completed": false,
          "date": null,
          "notes": "Wait for Day 1 call"
        },
        {
          "task": "First batch of 5 prospects imported (1h)",
          "completed": false,
          "date": null,
          "notes": "Customer to provide contact list"
        }
      ]
    },
    "support": {
      "phase": 2,
      "days": "4-7",
      "hours_budget": 2,
      "hours_actual": 0,
      "status": "upcoming",
      "checklist": [
        {
          "task": "Daily standup with customer (10 min × 4)",
          "completed": false,
          "date": null
        },
        {
          "task": "Help customer add prospects (30 min × 2)",
          "completed": false,
          "date": null
        },
        {
          "task": "Review draft messages + approve (20 min × 2)",
          "completed": false,
          "date": null
        }
      ]
    },
    "proof": {
      "phase": 3,
      "days": "8-11",
      "hours_budget": 3,
      "hours_actual": 0,
      "status": "upcoming",
      "checklist": [
        {
          "task": "Track proof events (prospects added, follow-ups, deals advanced)",
          "completed": false,
          "date": null,
          "target_metrics": "5+ prospects, 3+ follow-ups, 1+ deal advanced"
        },
        {
          "task": "Daily follow-ups with customer (15 min × 4)",
          "completed": false,
          "date": null
        },
        {
          "task": "Accumulate proof pack assets",
          "completed": false,
          "date": null
        }
      ]
    },
    "final_push": {
      "phase": 4,
      "days": "12-14",
      "hours_budget": 4,
      "hours_actual": 0,
      "status": "upcoming",
      "checklist": [
        {
          "task": "Final customer demo call (1h)",
          "completed": false,
          "date": null
        },
        {
          "task": "Assemble case study (1h)",
          "completed": false,
          "date": null,
          "content": [
            "Customer intro",
            "Pain statement",
            "Implementation results",
            "Metrics",
            "ROI calculation",
            "Quote"
          ]
        },
        {
          "task": "Prepare renewal proposal (1h)",
          "completed": false,
          "date": null,
          "content": "3,999 SAR/month for ongoing management"
        },
        {
          "task": "Renewal conversation (1h)",
          "completed": false,
          "date": null
        }
      ]
    }
  },
  "proof_events": [
    {
      "date": "2026-06-21",
      "event_type": "prospects_added",
      "count": 5,
      "notes": "First batch imported by customer"
    }
  ],
  "renewal_decision": {
    "status": "pending",
    "decision_date": null,
    "decision": null,
    "renewal_amount": null,
    "renewal_start_date": null,
    "notes": null
  },
  "notes": "Strong prospect, large team, high urgency"
}
```

**How to Track:**
1. Create this file on Day 1 of pilot (after onboarding call)
2. Update `phases.X.checklist[].completed` as you complete each task
3. Log `hours_actual` at end of each phase
4. Record `proof_events` daily (prospects added, deals advanced)
5. At Day 14: Make renewal decision
6. Calculate ROI for case study

---

## 6. MONTHLY REVENUE SUMMARY

**File:** `company/runtime/monthly_revenue_{YYYY-MM}.json`

**Format:**
```json
{
  "month": "2026-06",
  "revenue_summary": {
    "one_time_pilots": {
      "pilots_signed": 1,
      "pilot_price_sar": 499,
      "total_one_time": 499
    },
    "monthly_recurring": {
      "renewals": 0,
      "renewal_price_sar": 3999,
      "total_mrr": 0
    },
    "total_revenue": 499,
    "total_mrr": 0
  },
  "activity_metrics": {
    "whatsapps_sent": 20,
    "diagnostics_completed": 8,
    "conversion_rate_contacted_to_diagnostic": 0.4,
    "conversion_rate_diagnostic_to_pilot": 0.375,
    "overall_conversion_rate": 0.15,
    "cost_per_pilot_sar": 0,
    "acquisition_time_days_average": 8
  },
  "founder_metrics": {
    "hours_worked": 32,
    "hours_per_week": 8,
    "revenue_per_hour": 15.59,
    "sustainable": true
  },
  "pilots_active": [
    "pilot_20260620_001"
  ],
  "pilots_delivered": [],
  "pilots_renewed": [],
  "month_over_month_growth": {
    "revenue_growth": "N/A (first month)",
    "pilot_growth": "N/A (first month)",
    "mrr_growth": "N/A (first month)"
  },
  "forecast_next_month": {
    "projected_diagnostics": 12,
    "projected_pilots": 4,
    "projected_revenue": 1996,
    "projected_renewals": 0,
    "projected_mrr": 0,
    "projected_total": 1996
  }
}
```

**How to Use:**
1. Review on last day of month
2. Calculate all metrics automatically from other files
3. Compare to target (Day 30: 1,500 SAR minimum)
4. Identify bottlenecks (If conversion rate < 10%, focus on pitch)
5. Use forecast for Month 2 planning

---

## 7. QUICK DAILY METRICS

**Create this as simple text file:**

**File:** `company/runtime/daily_metrics_{YYYY-MM-DD}.txt`

**Format:**
```
DEALIX DAILY METRICS — 2026-06-17
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TODAY'S ACTIVITY:
  WhatsApps sent: 1
  Approvals processed: 3
  Diagnostics completed: 0
  Pilots signed: 0
  Revenue today: 0 SAR

WEEK TO DATE (Mon-Fri):
  WhatsApps sent: 1/5 ✅
  Diagnostics: 0/1-2
  Pilots: 0/1
  Revenue: 0/1,500 SAR

MONTH TO DATE (Days 1-17):
  WhatsApps sent: 17/20
  Diagnostics: 7/8 ✅
  Pilots: 1/3
  Revenue: 499/1,500 SAR (33%)

PIPELINE:
  Not contacted: 13
  Awaiting response: 4
  Scheduled for diagnostic: 2
  In delivery: 1

NEXT 3 DAYS:
  [ ] Diagnostic with فهد (Jun 18)
  [ ] Follow-up call with سارة (Jun 19)
  [ ] Pilot #2 close attempt (Jun 20)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Founder hours this week: 8/35
Status: On pace ✅
Next focus: Close Pilot #2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## SUMMARY: WHICH FILE TO USE WHEN

| File | Purpose | When to Check | Update Frequency |
|------|---------|---------------|------------------|
| warm_intro_targets.csv | Prospect pipeline | Daily, after WhatsApp | Daily |
| daily_ritual_*.log | Execution tracking | End of day / troubleshooting | Auto-generated |
| diagnostics_*.json | Call quality analysis | Weekly review | After each call |
| approval_queue_history_*.json | AI quality tracking | Weekly review | Auto-generated |
| pilots/{id}/delivery_log.json | Pilot progress | Daily for active pilots | Daily |
| monthly_revenue_*.json | Revenue analysis | Month-end | Auto-generated |
| daily_metrics_*.txt | Quick status check | Every morning | Daily |

---

**Print the Daily Ritual Checklist and Daily Metrics Template. Use them every single day.**

**Good luck.** 🚀

