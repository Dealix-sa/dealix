# PDPL Breach Response Runbook — 72-Hour Window
# دليل الاستجابة لخرق البيانات وفق PDPL — نافذة 72 ساعة

**Status:** ACTIVE (effective Day 14 of the 180-day Build-Out Plan)
**Owner:** DPO (Data Protection Officer — see `dealix/registers/dpo_appointment.yaml`)
**Last reviewed:** 2026-05-24
**Drill cadence:** Monthly Day 60–180 (compressed), quarterly post-Series A
**Binding authority:** PDPL Art. 25 (breach notification), Constitution Art. V (S3 sensitivity), Master spec `dealix/masters/incident_rollback_runbook.md`

---

## 1. What constitutes a PDPL breach?

A **personal data breach** is any incident that leads to:
- **Unauthorized access** to personal data (intentional or accidental)
- **Unauthorized disclosure** to a third party
- **Loss of availability** (data permanently inaccessible)
- **Loss of integrity** (data corrupted, tampered)
- **Loss of confidentiality** (data leaked)

**Examples relevant to Dealix:**
- LLM provider returns customer PII in completion text to another tenant
- Postgres backup leaked publicly
- Audit log corrupted (S3 data history lost)
- Cross-border transfer to non-PDPL-aligned country
- Sub-processor (HubSpot, Calendly, Moyasar) breach affecting Dealix data
- Prompt injection extracts another tenant's account data
- BOPLA redaction failure exposes NID/IBAN in logs

**NOT a breach (but still tracked):**
- Internal access by authorized staff per ROPA
- Successful pen-test finding (not exploited)
- Provider planned downtime under SLA

---

## 2. The 72-Hour Clock

PDPL Art. 25 requires SDAIA notification within **72 hours** of becoming aware of a breach likely to result in risk to data subjects.

**The clock starts at "awareness"** — not at "containment." Discovering at 23:00 KSA means SDAIA must be notified by 23:00 KSA three days later.

```
T+0:00   Awareness — incident detected and confirmed
T+0:30   Triage complete — severity + scope + affected subjects known
T+2:00   Containment plan executed — bleeding stopped
T+24:00  Root cause identified — technical post-mortem drafted
T+48:00  Data subject impact assessment + notification draft
T+72:00  SDAIA notification submitted (or "not notifying" justification documented)
T+7d     Customer/data subject notifications sent (if high risk)
T+14d    Full post-incident review + remediation plan
T+30d    Remediation complete + follow-up to SDAIA if applicable
```

---

## 3. Detection sources

Breach is detected via one of:

| Source | Channel | Owner | Response time SLA |
|---|---|---|---|
| Sentry alert (PII pattern in logs) | Sentry → PagerDuty → SMS | On-call | < 15 min ack |
| Audit log anomaly (privilege escalation) | nightly cron + alert | DPO | < 1 hr ack |
| Customer report (DSAR cites missing data) | `dsar@dealix.me` | DPO | < 4 hr ack |
| Sub-processor notification (HubSpot/Calendly/PSP) | Email + phone | DPO | < 1 hr ack |
| Security researcher disclosure | `security@dealix.me` (per SECURITY.md) | Founder + DPO | < 4 hr ack |
| Internal staff observation | Slack / WhatsApp founder-personal | Founder | < 1 hr ack |
| SDAIA contact | Official letter / portal | Founder + DPO + Legal | < 30 min ack |

---

## 4. Step-by-step response

### Phase 1 — DETECT (T+0:00 to T+0:30)

**Actions:**
1. **Acknowledge alert** — on-call confirms receipt within 15 min
2. **Open incident channel** — Slack `#incident-YYYYMMDD-NNN` (use template)
3. **Assign Incident Commander** — DPO if available, founder if not, escalates to board if both unavailable
4. **Page on-call** — primary DPO; secondary founder; tertiary CTO co-founder (post-Day-60)
5. **Start the 72h timer** — recorded in `dealix/registers/incident_drills.yaml` (new entry)

**Decisions:**
- Is this a real incident or a false positive? (Verify with 2 independent signals before declaring breach)
- Is customer data involved? (S2 or S3?)
- Is cross-border data involved?

**Outputs:**
- Incident ID
- Detection timestamp (UTC + KSA)
- Initial severity tag (P0/P1/P2/P3)

### Phase 2 — TRIAGE (T+0:30 to T+2:00)

**Actions:**
1. **Scope assessment:**
   - Which data categories? (cross-reference ROPA Activity IDs)
   - How many data subjects affected?
   - Time window of exposure?
   - Geographic scope (KSA only, or cross-border)?
2. **Severity classification:**
   - **P0 (critical):** > 1,000 subjects OR S3 data OR cross-border leak
   - **P1 (high):** 100–1,000 subjects OR sub-processor breach
   - **P2 (medium):** 10–100 subjects OR single-tenant impact
   - **P3 (low):** <10 subjects, contained, no S3
3. **Notify stakeholders:**
   - P0/P1 → founder + DPO + board chair immediate
   - P2 → founder + DPO within 4h
   - P3 → DPO daily digest
4. **Preserve evidence:**
   - Snapshot audit log
   - Capture system state (logs, metrics, configs)
   - Postgres backup at incident timestamp
   - Photo/screenshot any human-facing surfaces

**Outputs:**
- Severity classification
- Affected data subject list (or count + categories if list infeasible immediately)
- Evidence package stored read-only

### Phase 3 — CONTAIN (T+0:30 to T+4:00)

**Stop the bleeding. Containment ≠ remediation.**

**Actions:**
1. **Disable the vector:**
   - Compromised credentials → rotate immediately
   - Vulnerable endpoint → take offline (return 503)
   - Bad LLM output → disable affected agent via feature flag
   - Sub-processor breach → cut off data flow + invoke fallback
2. **Block lateral movement:**
   - Revoke session tokens
   - Force re-authentication
   - Audit access logs for related compromise
3. **Preserve forensics:**
   - Do NOT delete logs
   - Do NOT modify affected records
   - All actions logged with operator + timestamp + justification

**Decisions:**
- Can we contain without customer impact? If yes, proceed.
- If contain requires customer downtime > 1h, escalate to founder for go/no-go.

**Outputs:**
- Containment actions log
- Service status update (if customer-visible)

### Phase 4 — ASSESS IMPACT (T+2:00 to T+24:00)

**Actions:**
1. **Risk to data subjects:**
   - Identity theft? (NID/Iqama leaked?)
   - Financial loss? (IBAN/payment data?)
   - Reputation harm? (sensitive communications?)
   - Discrimination risk? (health/political/religious data?)
2. **Likelihood vs severity matrix:**
   - High likelihood + high severity → data subject notification required
   - Low likelihood OR contained quickly → may not require subject notification (DPO judgment, documented)
3. **Cross-border assessment:**
   - Was data transferred outside KSA during incident?
   - Does any sub-processor's incident response satisfy our obligation?
4. **DPIA review:**
   - If activity had a DPIA, did it predict this risk?
   - Update DPIA based on actual incident

**Outputs:**
- Impact assessment document
- Subject notification decision (yes / no / partial)

### Phase 5 — NOTIFY (T+48:00 to T+72:00)

**SDAIA notification:**
- Channel: SDAIA portal (when filed under SDAIA registration) OR official letter
- Content:
  - Nature of breach
  - Categories of data and subjects affected
  - Approximate number of subjects
  - Likely consequences
  - Measures taken or proposed
  - DPO contact info
- Submit within 72 hours of awareness
- If beyond 72h, justify the delay in writing

**Data subject notification** (if required):
- Channel: email + WhatsApp + portal banner (multi-channel for high risk)
- Plain language Arabic + English
- What happened, what data, what subjects can do, who to contact
- Submit "without undue delay" — target T+7 days

**Customer notification** (if customer's data is involved):
- Channel: email + phone call from founder
- Include: incident summary, scope of their tenant's data, our actions, contractual obligations under DPA, next steps
- Submit within 24 hours of confirmed customer impact (contractual SLA — tighter than PDPL)

### Phase 6 — REMEDIATE (T+24:00 to T+30 days)

**Actions:**
1. **Root cause analysis:**
   - Technical: what enabled the breach?
   - Process: which control failed?
   - People: who needed to know what?
2. **Fix the root cause:**
   - Code change + tests + deployment
   - Process change + runbook update
   - Training + drill
3. **Verify the fix:**
   - Reproduce the breach in test environment
   - Confirm patch prevents it
   - Add CI gate to prevent regression
4. **Update controls:**
   - Add new audit log entry types
   - Tighten policy rules in `dealix/trust/policy.py`
   - Update guardrails if applicable

**Outputs:**
- Root cause document
- Fix PR(s) merged
- New test cases
- Updated runbook (this document)

### Phase 7 — REVIEW (T+14 days)

**Post-incident review meeting:**
- Attendees: founder, DPO, CTO, on-call, anyone involved
- Blameless format
- Outcome: PIR document + action items + owners + due dates
- Stored in `docs/25_compliance_trust/incident_reviews/YYYYMMDD-NNN.md`

**Update:**
- `no_overclaim.yaml` if a claimed control failed
- `dealix/registers/incident_drills.yaml` with full timeline
- `compliance_saudi.yaml` if a PDPL/NCA control needs adjustment
- Training material if human error contributed

---

## 5. Communication templates

### SDAIA notification (skeleton)

```
إلى: الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA)
الموضوع: إشعار خرق بيانات شخصية وفق نظام حماية البيانات الشخصية

تاريخ الاكتشاف: [UTC + KSA]
رقم الحادثة: [INCIDENT-ID]
المسؤول عن البيانات: Dealix
مسؤول حماية البيانات: [DPO_NAME] · [DPO_EMAIL] · [DPO_PHONE]

1. طبيعة الخرق: [وصف موجز]
2. فئات البيانات المتأثرة: [من ROPA]
3. عدد أصحاب البيانات المتأثرين تقريباً: [N]
4. النتائج المحتملة: [التقييم]
5. الإجراءات المتخذة: [الاحتواء + الإصلاح]
6. الإجراءات المقترحة: [الخطوات التالية]
```

### Data subject notification (skeleton)

```
الموضوع: إشعار مهم بشأن بياناتك في Dealix

عزيزي/عزيزتي [الاسم]،

نكتب إليك لإعلامك بأنه في [تاريخ]، اكتشفنا حادثة أمنية أثرت على بعض بياناتك المخزنة لدينا.

ما الذي حدث: [الوصف بلغة بسيطة]
ما هي بياناتك المتأثرة: [القائمة]
ما الذي قمنا به: [الإجراءات]
ما الذي يمكنك فعله: [الإرشادات]
كيف تتواصل معنا: dsar@dealix.me · [DPO_PHONE]
```

### Customer notification (skeleton)

English + Arabic — see `docs/25_compliance_trust/templates/CUSTOMER_BREACH_NOTIFICATION.md` (to be created with DPO appointment).

---

## 6. Drills (monthly Day 60–180)

**Schedule:** Last Sunday of month at 14:00 KSA
**Duration:** 90 min
**Attendees:** DPO, founder, CTO (post-Day-60), on-call

**Drill scenarios (rotated):**
1. Compromised LLM provider returns another tenant's data
2. Audit log corruption discovered during nightly check
3. Sub-processor (HubSpot) notifies us of their breach
4. Prompt injection extracts NID from another tenant
5. Cross-border transfer to non-PDPL country (config error)
6. Mass exfiltration via DSAR abuse

**Drill outputs:**
- Time-to-acknowledge
- Time-to-contain
- Time-to-notify (simulated SDAIA + subjects)
- Gap list (training needs, runbook updates)
- Logged in `dealix/registers/incident_drills.yaml`

---

## 7. Hard rules

- **Never destroy evidence.** Even buggy logs are evidence.
- **Never miss the 72h SDAIA window** without documented justification reviewed by board chair.
- **Never notify externally without DPO + founder sign-off** (except for sub-processor breaches where contractual notification is binding).
- **Never apologize without legal review** beyond a templated empathy line — anything more can create unintended liability.
- **The DPO has veto authority** over external communications during a breach (per Constitution Art. V).
- **Every breach is followed by a no_overclaim.yaml audit** — did we claim a control that failed?

---

## 8. Related documents

- `dealix/masters/incident_rollback_runbook.md` — operational incident response (non-PDPL)
- `dealix/masters/constitution.md` — Constitution Art. V (S3 sensitivity)
- `dealix/registers/dpo_appointment.yaml` — DPO details + escalation
- `dealix/registers/compliance_saudi.yaml` — PDPL/NCA/ZATCA control matrix
- `dealix/registers/ropa.yaml` — Record of Processing Activities
- `dealix/registers/no_overclaim.yaml` — claims that may need adjustment post-incident
- `docs/SECURITY_RUNBOOK.md` — security-incident-specific procedures
- `docs/ON_CALL.md` — on-call rotation and escalation
