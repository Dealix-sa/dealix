# Client Data Handling Policy

> **Status:** Hard policy. PDPL-aligned.
> **Companion:** `docs/privacy/PRIVACY_GUARD_OS_AR.md` (repo) + `docs/wave8/DPA_CHECKLIST_AR_EN.md` (repo).

## The principle

> No client data is stored, processed, or shared without an explicit consent record.

## The 4 categories of data

### A. Public data (no consent needed)

- LinkedIn profile (public view).
- Company website.
- Google Maps listing.
- Public reviews.
- Public social posts.

### B. Permissioned data (consent record required)

- WhatsApp threads.
- Email threads.
- CRM data.
- Internal documents.
- Recordings (if any).

### C. Sensitive data (special handling)

- Patient data (HIPAA-style handling required).
- Legal data (privileged; no AI processing).
- Financial data (PCI handling required).
- Children's data (never).
- Biometric data (never, by default).

### D. Secret data (never)

- API keys.
- Passwords.
- Tokens.
- Private keys.
- Any value that should not be in a prompt or a report.

## The consent record

```json
{
  "consent_id": "consent_001",
  "account_id": "agency_x_riyadh",
  "data_categories": ["B: WhatsApp", "B: CRM"],
  "granted_by": "Sara",
  "granted_at_iso": "2024-12-01T10:00:00Z",
  "scope": "audit and pilot delivery",
  "expires_iso": "2024-12-31T23:59:59Z",
  "revocable": true,
  "source": "signed_consent_form",
  "dpo_reviewed": true
}
```

## The 5 hard rules

1. **No category B data without a consent record.** No exceptions.
2. **No category C data without a DPA.** Even with consent, the DPA defines the handling.
3. **No category D data in Dealix ever.** If a secret appears in a draft, the preflight rejects.
4. **No data export without the client's permission.** Even at the end of the engagement.
5. **No data sharing with a third party without the client's explicit permission.** No "we share with our subprocessors" hidden in T&C.

## The 5 storage rules

1. **Encryption at rest.** All Dealix-managed storage is encrypted.
2. **Encryption in transit.** TLS only.
3. **Access control.** Role-based; principle of least privilege.
4. **Audit log.** Every read and write is logged.
5. **Retention policy.** Data is deleted at the end of the engagement + the retention period.

## The 5 deletion rules

1. **On consent revocation.** Within 24 hours.
2. **On engagement end.** Within 30 days (or per DPA).
3. **On legal request.** Within 7 days.
4. **On DSR (Data Subject Request).** Within 30 days (PDPL).
5. **On data breach.** Per the security runbook.

## The 5 things the bundle's scripts do

1. **Read consent records** to verify the data is permissioned.
2. **Never store data** outside the founder's environment.
3. **Never log PII** in the preflight output.
4. **Never include PII** in the bundle's example JSONs.
5. **Never make a network call** to send data anywhere.

## The 5 things the bundle's scripts do NOT do

1. **No real WhatsApp data** in the examples.
2. **No real phone numbers** in the examples.
3. **No real email addresses** in the examples (the founder's signature is generic).
4. **No real client logos** in the examples.
5. **No real CRM data** in the examples.

## The DSR (Data Subject Request) flow

1. **Receive the request** (email or in-person).
2. **Verify the identity** of the requester.
3. **Log the request** in the DSR template (`docs/wave8/DSR_REQUEST_TEMPLATE.md` in the repo).
4. **Process within 30 days** (PDPL default).
5. **Notify the requester** of completion.

## The breach flow

If a breach is suspected:

1. **Stop processing** the affected data.
2. **Notify the founder** within 1 hour.
3. **Follow `docs/SECURITY_RUNBOOK.md`** (in the repo).
4. **Notify the client** within 24 hours.
5. **Notify the regulator** within the PDPL-defined window.

## When to update

- When a new data category is added.
- When a new tool is added (and its data handling is reviewed).
- When a DSR is processed.
- When a breach occurs.
- When PDPL guidance changes.
