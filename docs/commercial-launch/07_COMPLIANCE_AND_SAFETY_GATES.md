# Compliance & Safety Gates — بوابات الامتثال والأمان

> AI recommends and drafts. Deterministic workflows verify. Founder approves.
> Nothing is sent automatically.

Three deterministic gates run on every draft. They are enforced in code:
`scripts/commercial_quality_gate.py`, `scripts/commercial_compliance_gate.py`,
and `scripts/commercial_safety_audit.py`, configured by
`config/commercial_quality_gates.json` and `config/commercial_compliance_gates.json`.

---

## 1. Quality Gate — بوابة الجودة

A draft is **rejected** (`rejected_quality`) if:

- quality score < 70
- it does not mention a specific sector or pain
- it does not contain exactly one CTA
- it lacks an opt-out where one is required
- a sensitive sector draft omits human-approval / control language
- it sells more than one offer in the same message
- it uses generic AI-agency language
- Arabic reads as a literal translation; English is too long or too generic
- it does not fit the company or sector / gives no clear value
- it overpromises, or the subject is misleading
- the body exceeds the channel length limit

### Length limits / الحدود

| Channel | Max words |
|---------|-----------|
| Email | ~180 |
| LinkedIn | ~100 |
| Website form | ~120 |
| WhatsApp (manual opt-in reply) | ~80 |

---

## 2. Compliance Gate — بوابة الامتثال

A draft is **rejected** (`rejected_compliance`) if it:

- has no opt-out (where required)
- uses fake familiarity ("as discussed" without a real conversation)
- promises guaranteed ROI or any unprovable result
- uses fake urgency / artificial deadline / pressure or threat
- makes unproven claims (no case study)
- references personal data without necessity
- implies Dealix accessed/extracted private data
- requests sensitive data in the first message
- (legal/healthcare/finance) lacks privacy-first language
- is WhatsApp without opt-in
- implies LinkedIn automation
- implies website form auto-submit
- contains more than one CTA or more than one offer
- is too generic

### Banned phrases / العبارات الممنوعة

`guaranteed`, `100%`, `replace your team`, `replace your employees`,
`replace your lawyer`, `automate everything`, `no human needed`, `as discussed`,
`we found your data`, `from our database`, `we accessed your data`,
`we extracted your data`.

Each draft is assigned: `compliance_score`, `quality_score`, `risk_level`,
`rejection_reason`, `founder_review_notes`.

---

## 3. Safety Gate — بوابة الأمان (no external send)

`scripts/commercial_safety_audit.py` scans this OS's executable surface and the
generated drafts. It is **tiered**:

- **Enablement patterns** (e.g. `send_allowed: true`, `external_send_blocked: false`,
  `no_auto_send: false`) are a hard failure **anywhere**.
- **Code send-signatures** (SMTP libraries, mail-API SDKs, `auto_send`, `bulk_send`,
  browser-automation drivers, outbound `requests.post(...send...)`) are a hard
  failure in executable files. The same terms appearing inside policy prose
  (this doc, the channel policy) are recorded as warnings, not failures, because
  documents legitimately name what is prohibited.
- The bare word `requests` is **not** blocked — only outbound sending is.

It also verifies every generated draft has:
`send_allowed = false`, `external_send_blocked = true`,
`requires_founder_approval = true`, `no_auto_send = true`, and a non-forbidden status.

Output: `outputs/commercial_launch/YYYY-MM-DD/safety_audit.json` with
`pass`, `blocked_terms_found`, `files_scanned`, `violations`, `warnings`,
`recommended_fix`.

---

## Draft statuses / حالات المسودة

**Allowed:** `founder_review`, `needs_research`, `rejected_quality`,
`rejected_compliance`, `ready_for_manual_copy`, `archived`.

**Forbidden (never produced):** `sent`, `auto_sent`, `queued_for_send`,
`smtp_ready`, `whatsapp_ready`, `linkedin_auto_ready`.
