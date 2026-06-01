# GCC Omni-Channel Growth OS — نظام النمو متعدد القنوات للخليج

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [../06_APPROVAL_GATES.yml](../06_APPROVAL_GATES.yml) | [CHANNEL_ROUTER.yml](CHANNEL_ROUTER.yml) | [ANTI_BAN_GUARDIAN.yml](ANTI_BAN_GUARDIAN.yml) | [../sales/DEAL_QUALIFICATION_SCORECARD.md](../sales/DEAL_QUALIFICATION_SCORECARD.md)

---

## 1. Mission — المهمة

Generate 300+ qualified outreach drafts per day across GCC sectors in Arabic and English. Every draft waits in queue. The founder reviews and approves each send. No message leaves without explicit approval.

توليد أكثر من 300 مسودة تواصل مؤهَّلة يومياً عبر قطاعات الخليج باللغتين العربية والإنجليزية. كل مسودة تنتظر في قائمة الانتظار. يراجع المؤسس ويوافق على كل رسالة قبل الإرسال. لا تغادر أي رسالة بدون موافقة صريحة.

**What this OS does not do / ما لا يفعله هذا النظام:**

- Does not send cold WhatsApp blasts — لا يُرسل رسائل واتساب جماعية غير مرغوب فيها
- Does not scrape LinkedIn — لا يستخرج بيانات لينكدإن
- Does not automate DMs on any platform — لا يُرسل رسائل مباشرة تلقائية على أي منصة
- Does not guarantee reply rates, bookings, or revenue — لا يضمن معدلات رد أو حجوزات أو إيرادات

---

## 2. Channel Hierarchy — تسلسل القنوات

| Priority — الأولوية | Channel — القناة | Mode — الأسلوب | Notes — ملاحظات |
|---|---|---|---|
| Primary | Website / Inbound | Passive attract | SEO, content, referral traffic — موقع وتحسين محركات |
| Primary | Referral network | Active request | From delivered clients and partners — إحالات من عملاء |
| Secondary | Warm email | Semi-automated draft, manual send | Opt-in lists only — قوائم موافقة فقط |
| Secondary | LinkedIn manual | Human-operated, no automation | 20 connections/day max — يدوي فقط |
| Secondary | Webinar / events | Calendar-based cadence | Industry events, online sessions — فعاليات |
| BLOCKED | Cold WhatsApp blast | — | Zero tolerance — ممنوع تماماً |
| BLOCKED | Cold LinkedIn auto-DM | — | Zero tolerance — ممنوع تماماً |
| BLOCKED | Mass unsolicited email | — | Zero tolerance — ممنوع تماماً |

---

## 3. Sector → Channel Map — خريطة القطاع إلى القناة

### Facilities Management (FM) — إدارة المرافق

- **Best channels:** Referral (FM directors know each other), warm email to ops leads, FM sector events
- **Also useful:** LinkedIn manual (search Operations Director, FM Director), Dealix webinar on SLA automation
- **Avoid:** Cold WhatsApp, cold LinkedIn DM, mass email blasts

### Contracting / PMO — المقاولات وإدارة المشاريع

- **Best channels:** Referral from existing clients, warm email to PMO Directors, engineering associations
- **Also useful:** LinkedIn manual (Project Director, VP Engineering), industry events (CIOB, Saudi contractors events)
- **Avoid:** Cold WhatsApp, auto-DM, mass unsolicited email

### Industrial / Manufacturing — الصناعة والتصنيع

- **Best channels:** Industry events (ADIPEC, Saudi Manufacturing), referral, warm email
- **Also useful:** LinkedIn manual (Plant Manager, Maintenance Manager)
- **Avoid:** Cold WhatsApp, LinkedIn automation

### B2B Professional Services — الخدمات المهنية

- **Best channels:** Referral (professional networks are tight), warm email, LinkedIn manual
- **Also useful:** Webinar on specific use case (proposal automation, client reporting)
- **Avoid:** Cold WhatsApp, LinkedIn auto-DM

### Legal Firms — المكاتب القانونية

- **Best channels:** Referral only (trust-driven sector), formal email through bar association contacts
- **Also useful:** Legal tech events, LinkedIn manual
- **Avoid:** Cold WhatsApp (damages trust), cold LinkedIn DM, any bulk outreach

### Real Estate / Property — العقارات والإدارة العقارية

- **Best channels:** Referral, warm email, property management events
- **Also useful:** LinkedIn manual (Property Director, FM lead in real estate firms)
- **Avoid:** Cold WhatsApp

### International Companies (GCC presence) — شركات دولية في الخليج

- **Best channels:** LinkedIn manual (executive level), warm email, executive referral
- **Also useful:** Webinar, expat-accessible events
- **Avoid:** Cold WhatsApp, LinkedIn automation (account ban risk)

---

## 4. Daily Growth Rhythm — الإيقاع اليومي للنمو

### 07:30 — Morning Pipeline Review (15 min) | مراجعة الصباح

- Review [DAILY_GROWTH_REPORT.md](DAILY_GROWTH_REPORT.md) generated overnight
- Check reply classifications from previous sends
- Confirm active deals needing follow-up today (reference [../sales/FOLLOW_UP_SEQUENCES.md](../sales/FOLLOW_UP_SEQUENCES.md))

### 08:00 — Draft Queue Generation (automated) | توليد قائمة المسودات

- System generates up to 300 drafts per day against active prospect list
- Each draft uses [PERSUASION_DOSSIER_SCHEMA.json](PERSUASION_DOSSIER_SCHEMA.json) data
- Drafts written in Arabic if language_preference = arabic or bilingual; English if English
- Drafts logged in [DRAFT_QUEUE_SCHEMA.json](DRAFT_QUEUE_SCHEMA.json) with status = `draft`

### 09:00–10:00 — Founder Review and Approve Window | نافذة مراجعة المؤسس

- Founder opens draft queue
- Reviews each message: accuracy, tone, timing, channel fit
- Approves → status = `approved` | Rejects with reason → status = `rejected`
- No message is sent without status = `approved`

### 10:00–12:00 — Send Execution | تنفيذ الإرسال

- Approved emails go out in batches (max 200/day, see [ANTI_BAN_GUARDIAN.yml](ANTI_BAN_GUARDIAN.yml))
- LinkedIn manual outreach done by founder or designated team member — no automation
- WhatsApp: opt-in contacts only, approved template, one-by-one
- All sends logged: sent_at, channel, draft_id

### 17:00 — Evening Tracking (10 min) | تتبع المساء

- Update reply statuses in CRM
- Flag any bounces or unsubscribes
- Any channel metric above threshold → pause + escalate (see ANTI_BAN_GUARDIAN)
- Generate input for next day's draft queue: which prospects advance, which park

---

## 5. Quality Gates — بوابات الجودة

| Metric — المقياس | Threshold — الحد | Action if Exceeded — الإجراء عند التجاوز |
|---|---|---|
| Email bounce rate | < 3% | Pause email, review list, notify founder |
| Email spam rate | < 0.1% | Immediate pause, audit all templates |
| LinkedIn connections/day | ≤ 20 (manual) | Hard stop if automated |
| LinkedIn auto-DM | Zero tolerance | Block feature, log violation |
| WhatsApp opt-in status | Required before send | Reject if not confirmed |
| WhatsApp broadcast list | Zero tolerance | Block feature entirely |
| First email approval | 100% founder-reviewed | No bypass |

---

## 6. Metrics Dashboard — لوحة المقاييس

Reviewed every Monday. Reported in [DAILY_GROWTH_REPORT.md](DAILY_GROWTH_REPORT.md) daily, summarized weekly.

| Metric — المقياس | Target — الهدف | Review Cadence — دورية المراجعة |
|---|---|---|
| New prospects added to pipeline | ≥ 50/week | Weekly |
| Drafts generated | ≥ 300/day | Daily |
| Drafts approved and sent | Varies by founder capacity | Daily |
| Reply rate (all channels) | ≥ 8% | Weekly |
| Discovery calls booked | ≥ 3/week | Weekly |
| Proposals created | ≥ 1/week | Weekly |
| Referral introductions received | ≥ 2/week | Weekly |
| Deals advanced in pipeline | Track by stage | Weekly |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
