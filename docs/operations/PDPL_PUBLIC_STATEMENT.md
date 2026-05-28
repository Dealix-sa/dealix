# Dealix · PDPL Compliance Public Statement

> Public-facing. Bilingual. Auto-linked from any customer-facing surface
> that touches personal data. Reviewed quarterly by founder + Saudi
> legal counsel.
>
> **Effective:** 2026-06-01 · **Next review:** 2026-09-01

---

## Arabic — العربية

### 1. التزامنا

Dealix يعمل تحت نظام حماية البيانات الشخصية السعودي (PDPL) — لا
استثناءات، لا "compliance by hand-wave". هذا المستند هو الـ public
statement الذي نلتزم به علنًا.

### 2. الـ Lawful Basis لأي معالجة

- **B2B outreach:** Legitimate Interest (الأكثر استخدامًا).
- **Customer data ingest:** Contractual Necessity (بعد DPA موقعة).
- **Marketing على inquirers existing:** Consent صريح (دائمًا opt-in،
  دائمًا withdrawable).
- **Internal analytics:** Legitimate Interest + anonymization
  layer.

كل lead عنده Source Passport يسجل الـ basis ومتى/كيف تم الـ
capture.

### 3. حقوق الـ Data Subject

نوفّر الـ ٨ حقوق المنصوص عليها في PDPL:
- **حق الوصول** — `POST /api/v1/pdpl/dsar/access`
- **حق التصحيح** — `POST /api/v1/pdpl/dsar/rectify`
- **حق المحو** — `POST /api/v1/pdpl/dsar/erase`
- **حق النقل** — `POST /api/v1/pdpl/dsar/port`
- **حق الاعتراض** — email `privacy@dealix.me`
- **حق سحب الموافقة** — opt-out link في كل رسالة
- **حق الإبلاغ** — SDAIA portal أو مباشرة لنا
- **حق التعويض** — وفق المادة ٣٧ من PDPL

الـ SLA للرد: ١٤ يوم من تاريخ الطلب (PDPL article 36).

### 4. تخزين البيانات

- **الموقع:** Riyadh / Saudi Arabia (Railway KSA region).
- **التشفير:** at-rest (Postgres TLS) + in-transit (HTTPS only).
- **النسخ الاحتياطي:** يومي، مشفر، يُحتفظ به ٣٠ يوم.
- **الاحتفاظ:** ٩٠ يوم من إنهاء العلاقة → auto-delete (إلا
  retention agreement موقعة).

### 5. مشاركة البيانات مع طرف ثالث

نشارك فقط مع:
- **Moyasar** (المدفوعات) — DPA موقعة
- **Anthropic Claude / OpenAI** (LLM، لو طلبتم) — DPA منهم
- **HubSpot** (CRM، اختياري) — DPA موقعة
- **Calendly** (الحجوزات، اختياري) — DPA موقعة
- **Railway** (الاستضافة) — DPA موقعة + region locked to KSA

كل تشارك موثّق في `dealix/registers/compliance_saudi.yaml#sub_processors`.

### 6. الـ DPO

Dealix يلتزم بتعيين DPO رسمي قبل أول customer يعالج > ٥٠٠٠ data
subject سعودي (per PDPL article 27).

حاليًا: founder = acting DPO. Contact: `privacy@dealix.me`.

### 7. الـ Breach Response

في حال خرق بيانات:
- إشعار SDAIA خلال ٧٢ ساعة (PDPL article 28).
- إشعار الـ data subjects المتأثرين خلال ٧٢ ساعة لو الخرق
  high-risk.
- Public post-mortem خلال ٧ أيام.

Runbook: `docs/operations/BREACH_RESPONSE.md` (internal).

### 8. الـ Cross-border Transfer

البيانات تبقى في KSA افتراضيًا. أي transfer خارج KSA يحتاج:
- Explicit consent من العميل
- DPA موقعة مع receiving party
- SDAIA notification لو > ١٠٠ data subject

---

## English

### 1. Our commitment

Dealix operates under Saudi Personal Data Protection Law (PDPL) —
no exceptions, no "compliance by hand-wave". This document is the
public statement we hold ourselves to.

### 2. Lawful basis for processing

- **B2B outreach:** Legitimate Interest (most used).
- **Customer data ingest:** Contractual Necessity (after DPA
  signed).
- **Marketing to existing inquirers:** Explicit Consent (always
  opt-in, always withdrawable).
- **Internal analytics:** Legitimate Interest + anonymization
  layer.

Every lead has a Source Passport recording the basis + capture
when/how.

### 3. Data subject rights

We provide the 8 rights granted by PDPL:
- **Right to access** — `POST /api/v1/pdpl/dsar/access`
- **Right to rectify** — `POST /api/v1/pdpl/dsar/rectify`
- **Right to erase** — `POST /api/v1/pdpl/dsar/erase`
- **Right to port** — `POST /api/v1/pdpl/dsar/port`
- **Right to object** — email `privacy@dealix.me`
- **Right to withdraw consent** — opt-out link in every message
- **Right to complain** — SDAIA portal or directly to us
- **Right to compensation** — per PDPL article 37

SLA for response: 14 days from request date (PDPL article 36).

### 4. Data storage

- **Location:** Riyadh / Saudi Arabia (Railway KSA region).
- **Encryption:** at-rest (Postgres TLS) + in-transit (HTTPS only).
- **Backup:** daily, encrypted, retained 30 days.
- **Retention:** 90 days from engagement end → auto-delete (unless
  signed retention agreement).

### 5. Third-party sharing

We share only with:
- **Moyasar** (payments) — DPA signed
- **Anthropic Claude / OpenAI** (LLM if you opt in) — their DPA
- **HubSpot** (CRM, optional) — DPA signed
- **Calendly** (booking, optional) — DPA signed
- **Railway** (hosting) — DPA signed + region locked to KSA

Every share documented in
`dealix/registers/compliance_saudi.yaml#sub_processors`.

### 6. DPO

Dealix commits to appointing a formal DPO before the first customer
processing > 5,000 Saudi data subjects (per PDPL article 27).

Currently: founder = acting DPO. Contact: `privacy@dealix.me`.

### 7. Breach response

In case of breach:
- SDAIA notification within 72 hours (PDPL article 28).
- Affected data subjects notified within 72 hours if breach is
  high-risk.
- Public post-mortem within 7 days.

Runbook: `docs/operations/BREACH_RESPONSE.md` (internal).

### 8. Cross-border transfer

Data stays in KSA by default. Any transfer outside KSA requires:
- Explicit customer consent
- DPA signed with receiving party
- SDAIA notification if > 100 data subjects

---

## Contact

- **Privacy questions:** `privacy@dealix.me`
- **Breach reports:** `security@dealix.me` (encrypted PGP available
  on request)
- **SDAIA complaints:** if unsatisfied, the data subject may
  complain directly to SDAIA at sdaia.gov.sa

---

## Audit chain

This document hashes to the latest commit. Version history at
`git log -- docs/operations/PDPL_PUBLIC_STATEMENT.md`. Material
changes notified to existing customers 30 days before effect.
