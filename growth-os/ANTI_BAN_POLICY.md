# Dealix Growth OS — Anti-Ban Policy
# سياسة منع الحظر — ديليكس Growth OS

**Version:** 1.0 | **Date:** 2026-05-31
**Implemented in:** `anti_ban_guardian.py` + `config/anti-ban.yml`

---

## Policy Summary / ملخص السياسة

Dealix's anti-ban policy protects sender reputation, respects platform terms of service, and ensures all outreach is welcome, relevant, and compliant. This policy is enforced in code — not just documented.

---

## Email Policy

**Compliance frameworks:** CAN-SPAM, Saudi PDPL

### Sending Limits
- Daily maximum: 500 emails
- Hourly maximum: 50 emails
- Same domain: max 2 per day
- Same company: max 2 touchpoints in 14 days

### Warm-Up Schedule (New Domain)
| Days | Daily Max |
|------|-----------|
| 1-3  | 20 |
| 4-7  | 50 |
| 8-10 | 100 |
| 11-14 | 250 |
| 15+  | 500 |

### Automatic Pause Triggers
- Bounce rate > 5% → PAUSE immediately
- Bounce rate > 3% → Reduce quota by 50%
- Spam rate > 0.3% → PAUSE immediately
- 10 consecutive hard bounces → PAUSE

### Required Elements
- Physical address in every commercial email (CAN-SPAM)
- One-click unsubscribe in every email
- No deceptive subject lines
- Sender identity clearly stated

### Monitoring Tools
- Google Postmaster Tools: Check daily
- MXToolbox: Verify SPF/DKIM/DMARC weekly
- Email provider bounce/spam webhooks: Real-time

---

## WhatsApp Policy

**Compliance framework:** WhatsApp Business Policy

### Non-Negotiable Rules
- Opt-in REQUIRED before any message — HARD BLOCK without it
- Approved Meta template REQUIRED for outbound first contact
- 24-hour window enforced for free-form replies after inbound

### Stop Keywords (Immediate Suppression)
`stop`, `unsubscribe`, `توقف`, `إيقاف`, `لا`, `أوقف`, `إلغاء`, `cancel`

Processing time: 0-15 minutes (immediate)

### Sending Limits
- Daily maximum: 100 messages
- Hourly maximum: 20 messages
- Warm-up: 10/day first week, 30/day second week, 100/day after

### Automatic Pause Triggers
- Block rate > 2% → PAUSE immediately
- Quality rating = Red → PAUSE
- Quality rating = Yellow for 3+ days → REVIEW

---

## LinkedIn Policy

**Compliance framework:** LinkedIn User Agreement and Professional Community Policies

### Non-Negotiable Rules
- ALL LinkedIn actions are ASSISTED_MANUAL — system never touches LinkedIn
- No automation of any kind — ToS violation
- No scraping — blocked at architecture level, non-negotiable
- Founder manually executes every action

### Guidance Limits (Not Enforced by System — LinkedIn Enforces These)
- Connection requests: 25 per week (LinkedIn limit)
- Messages: 20 per day
- Profile views: 50 per day

### What System Does
- Prepares draft message and context package
- Writes to `outputs/founder_review/`
- Founder reads, personalizes, and sends manually

### What System Never Does
- Access linkedin.com
- Send any message
- Connect with anyone
- View any profile
- Extract any data

---

## Instagram Policy

**Compliance framework:** Meta Platform Messaging Policy

### Non-Negotiable Rules
- INBOUND ONLY — no outbound DM
- 24-hour window strictly enforced
- Human handoff for pricing, contracts, security topics

### Allowed Actions
- Reply to DMs that users send to Dealix account
- Reply to comments on Dealix posts
- Max 50 DM replies/day, 30 comment replies/day

### Not Allowed
- Sending DMs to users who have not messaged first
- Automated bulk replies
- Sending messages outside 24-hour window without new inbound trigger

---

## Messenger Policy

**Compliance framework:** Meta Platform Messaging Policy

### Non-Negotiable Rules
- INBOUND ONLY — no outbound DM
- 24-hour window strictly enforced
- Human handoff for sensitive topics

### 24-Hour Window Rule
After user sends a message, the system can auto-reply for up to 24 hours.
After 24 hours, only founder can re-engage manually.

---

## X (Twitter) Policy

**Compliance framework:** X Platform Rules

### Allowed
- Posts: 10/day (thought leadership content)
- Replies: 30/day (to relevant public posts)
- DMs: Only in response to direct relevant request

### Not Allowed
- Bulk DM
- Unsolicited mass messaging
- Follow/unfollow automation

---

## Telegram Policy

**Compliance framework:** Telegram Terms of Service

### Non-Negotiable Rules
- Opt-in via /start command — user initiates
- No random DMs
- Group posting: Admin invite only

### Stop Command
User sends `/stop` or "stop"/"توقف" → immediate suppression

---

## Website Forms Policy

- Maximum 1 submission per domain per day
- Minimum 60 minutes between any two submissions
- Human review required before every submission
- No CAPTCHA bypass tools
- No duplicate submissions

---

## Global Rules (All Channels)

- Same company: max 2 touchpoints in any 14-day period
- Same contact: max 2 touchpoints in any 14-day period
- Global warning: 3 violations → pause ALL channels for 48 hours
- After suppression: 90-day cooldown before review

---

## Resume Process After Pause

1. Founder receives notification in daily brief
2. Founder investigates root cause (check Postmaster Tools, webhook logs)
3. Founder fixes underlying issue
4. Founder manually resumes channel in dashboard
5. Guardian logs resume with `resolved_at` timestamp
6. Quota restored at 50% for first 24 hours after resume

---

## Compliance References

| Rule | Framework | Where Configured |
|------|-----------|------------------|
| No cold WhatsApp | WhatsApp Business Policy | config/anti-ban.yml |
| No LinkedIn automation | LinkedIn User Agreement | config/anti-ban.yml |
| No scraping | Dealix Non-Negotiable #1 | Architecture |
| Unsubscribe honored | CAN-SPAM, PDPL | reply_classifier.py |
| Data minimization | PDPL, GDPR | memory/ schema |
| Legitimate interest | PDPL | compliance.yml |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
