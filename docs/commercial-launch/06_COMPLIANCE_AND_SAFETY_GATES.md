# Compliance & Safety Gates

Three independent layers protect the brand, the domain, and the channels.
Sources: `config/commercial_quality_gates.json`, `dealix/commercial_launch/`.

---

## 1. Quality gate (0–100, reject below 70)

Every draft gets a `quality_score`. A draft is **rejected** if it:

- scores below **70**
- does not name a **clear pain**
- has no single **CTA**
- has no **opt-out**
- is **too generic**
- contains **exaggeration**
- contains **more than one offer**
- has **literal / poor Arabic**
- reads as **generic AI-agency English**
- is **not tied to its vertical**

Weights are configurable in `commercial_quality_gates.json → quality_gate.weights`.

---

## 2. Compliance gate (0–100, reject below 70)

Every draft gets a `compliance_score`. A draft is **rejected** if it:

- has **no opt-out**
- contains **fake familiarity** ("as discussed", "كما اتفقنا", …)
- promises **guaranteed ROI**
- **claims access** to the prospect's data
- mentions **personal data without justification**
- is a **legal/regulated** vertical **without privacy-first language**
- is **WhatsApp without opt-in**
- is a **LinkedIn automated action**
- implies **any external send**

---

## 3. Safety audit (hard fail)

```bash
python scripts/commercial_safety_audit.py
```

The audit **fails (non-zero exit)** if it finds, in any commercial-launch
source file or generated draft:

- a mail client (smtp client, send mail, sendgrid, mailgun)
- `.send_message(` style calls
- twilio / WhatsApp send calls
- LinkedIn automation (auto-connect / auto-message)
- selenium / playwright used for outreach
- `requests.post` to an external send endpoint
- `send_allowed = true`
- `external_send_blocked = false`
- any draft missing a required field or with `send_allowed` not `False`

### Context-aware, not blunt

The audit distinguishes **active external sending** from ordinary integrations.
Generic `requests` usage for internal tests is **not** flagged — only
`requests.post` to send/mail/messages/outreach endpoints is. Lines that
legitimately reference a forbidden word (e.g. policy text, the audit's own
denylist) carry a `# safety-audit-allow` marker and are skipped.

---

## Risk levels

| Level | When |
|-------|------|
| `high` | WhatsApp, or regulated vertical with low compliance score |
| `medium` | Regulated vertical, or `research_required` |
| `low` | Default |

---

## What "blocked" means on every draft

```json
{ "send_allowed": false, "external_send_blocked": true, "requires_founder_approval": true }
```

These three are invariant. The safety audit and the test suite
(`tests/test_commercial_no_external_send.py`) fail the build if any draft
deviates.
