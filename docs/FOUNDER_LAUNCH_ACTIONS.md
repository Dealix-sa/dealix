# Founder Launch Actions — قائمة إجراءات المؤسس قبل الإطلاق

> **Audience / الجمهور:** Sami (founder) only. **Last updated:** 2026-05-18.
>
> **EN —** This is the human/account/legal residue of launch. Everything that *can* be
> built or configured in code already has been. The items below cannot be done by an
> engineer or an automated system — they need Sami's identity, his accounts, his
> credentials, or his legal authority. Each item is concrete enough to finish without
> asking further questions.
>
> **AR —** هذه هي البقايا البشرية والقانونية والحسابات المطلوبة للإطلاق. كل ما *يمكن*
> بناؤه أو ضبطه برمجيًا تم إنجازه فعلًا. البنود التالية لا يستطيع مهندس ولا نظام آلي
> تنفيذها — تحتاج هوية سامي، أو حساباته، أو بيانات اعتماده، أو صلاحيته القانونية. كل
> بند مكتوب بدقة كافية لإنجازه دون أسئلة إضافية.

**Doctrine / المبدأ:** Dealix never sends an external message without prior human
approval. Dealix never performs scraping, cold WhatsApp, LinkedIn automation, or bulk
outreach. Social credentials below are for publishing Dealix's *own* posts only.
ديلكس لا يرسل أي رسالة خارجية دون موافقة بشرية مسبقة، ولا يقوم بأي جمع آلي للبيانات أو
تواصل بارد أو أتمتة لينكدإن أو إرسال جماعي. بيانات الحسابات الاجتماعية أدناه لنشر محتوى
ديلكس نفسه فقط.

---

## How to read this list — كيف تقرأ هذه القائمة

Each item gives: (a) what to do, (b) why it matters for launch, (c) where exactly to
do it, (d) what to hand back to the repo or engineer, (e) rough time, (f) priority.
كل بند يوضح: (أ) ما العمل، (ب) لماذا يهم للإطلاق، (ج) أين بالضبط، (د) ما تسلّمه للمستودع
أو المهندس، (هـ) الوقت التقديري، (و) الأولوية.

| Priority | Meaning — المعنى |
|---|---|
| **P0** | Launch blocker. Dealix cannot take a paying customer until this is done. مانع إطلاق — لا يمكن قبول عميل يدفع قبل إنجازه. |
| **P1** | Needed in the launch week; degrades operations if missing. مطلوب خلال أسبوع الإطلاق. |
| **P2** | Needed soon after launch; not a hard gate. مطلوب بعد الإطلاق بقليل. |

---

## P0 — 1. Moyasar payment account — حساب مدفوعات ميسر

**This is THE launch blocker. هذا هو مانع الإطلاق الأول.**

**EN — What to do:** Complete Moyasar business KYC / verification, then provide the
**live** secret key and the **webhook** secret.

- Submit KYC documents: Saudi commercial registration (CR / السجل التجاري), national
  address (Wasel), founder national ID (both sides), authorised-signatory letter on
  company letterhead, corporate Saudi bank IBAN + bank confirmation letter, VAT
  certificate, and a short business description (what Dealix sells, average ticket,
  expected monthly volume, refund-policy URL).
- After approval, copy the **live** secret key `sk_live_...` from the dashboard.
- Register the production webhook and set its secret.

**Test mode vs live mode — وضع الاختبار مقابل الوضع الحي:** Moyasar issues two key
families. `sk_test_...` only moves play money — no real card is charged and no money
reaches the bank. `sk_live_...` moves real money and only works **after** KYC is
approved. The code currently runs in test mode; switching the env var to a live key
is the moment Dealix can actually charge a customer. التجربة لا تحرّك مالًا حقيقيًا؛
الوضع الحي يعمل فقط بعد اعتماد KYC، وتبديل المتغير إلى مفتاح حي هو لحظة قدرة ديلكس على
تحصيل المال فعليًا.

**Why it blocks launch — لماذا يمنع الإطلاق:** Without a live key, every checkout is
play money. Dealix literally cannot collect a single riyal. كل عملية دفع تكون أموالًا
تجريبية، ولا يمكن تحصيل ريال واحد.

**Where — أين:** https://dashboard.moyasar.com → Settings → Verification (KYC), then
Settings → API Keys (live key), then Webhooks → Add Webhook.

- Webhook URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
- Webhook events: `payment_paid`, `payment_failed`, `payment_refunded`,
  `payment_authorized`, `payment_captured`.

**Hand back — ما تسلّمه:** three values, into 1Password (`Dealix Production` vault)
and to the engineer for Railway env vars:

- `MOYASAR_SECRET_KEY` = `sk_live_...`
- `MOYASAR_WEBHOOK_SECRET` = the exact secret you set in the Moyasar webhook screen
  (generate with `python -c "import secrets; print(secrets.token_hex(32))"` and paste
  the **same value** in both Railway and the Moyasar dashboard — any mismatch causes
  401s and a SEV-1 page).
- `MOYASAR_MODE` = `production`

**Time — الوقت:** ~30 min to assemble and submit documents; **1–3 business days**
for Moyasar approval (the long pole). أيام عمل ١–٣ للاعتماد.

**Detailed steps:** [`docs/ops/MOYASAR_KYC_CHECKLIST.md`](ops/MOYASAR_KYC_CHECKLIST.md)
· cutover: [`docs/MOYASAR_LIVE_CUTOVER.md`](MOYASAR_LIVE_CUTOVER.md)

---

## P0 — 2. Sentry error monitoring — مراقبة الأخطاء (Sentry)

**EN — What to do:** Create a Sentry account and a `dealix-backend` project, copy the
`SENTRY_DSN`, and have it set as an environment variable on the production host
(Railway). The code already supports Sentry and silently no-ops until the DSN is set —
so without it, a production error during the first paid checkout would be invisible.

**Why it matters — لماذا يهم:** On launch day a silent backend error during a real
payment would be invisible without Sentry. This is a P0 because the first paying
customer must not hit an undiagnosable failure. أول عميل يدفع يجب ألا يصطدم بعطل لا
يمكن تشخيصه.

**Where — أين:** https://sentry.io → create org `dealix` → create project
`dealix-backend` (platform: Python / FastAPI) → Settings → Client Keys (DSN).

**Hand back — ما تسلّمه:** the DSN string, to the engineer / Railway:

- `SENTRY_DSN` = `https://<key>@<org>.ingest.sentry.io/<project>`

(The engineer sets `SENTRY_ENVIRONMENT`, sample rates, and PII scrubbing — those are
code/config, not founder-only.)

**Time — الوقت:** ~10 min.

**Detailed steps:** [`docs/ops/SENTRY_SETUP.md`](ops/SENTRY_SETUP.md)

---

## P1 — 3. Uptime monitoring — مراقبة التشغيل (UptimeRobot)

**EN — What to do:** Create an UptimeRobot account and add two HTTP(S) monitors, then
set yourself as the alert contact.

- Monitor 1: `https://api.dealix.me/health` — expect HTTP 200.
- Monitor 2: `https://dealix.me` — expect HTTP 200.
- Alert contact: your email (and WhatsApp if you connect that integration).

**Why it matters — لماذا يهم:** If the API or landing page goes down, you need to know
before a customer tells you. إذا توقّفت الواجهة، يجب أن تعرف قبل أن يخبرك العميل.

**Where — أين:** https://uptimerobot.com → Dashboard → Add New Monitor (×2) →
My Settings → Alert Contacts.

**Hand back — ما تسلّمه:** nothing into code. Optionally copy the Main API Key
(`My Settings → API Settings`) for the engineer if you want the public status page
auto-provisioned via `scripts/infra/setup_uptimerobot.sh` — record it as
`UPTIMEROBOT_API_KEY`.

**Time — الوقت:** ~10 min.

**Detailed steps:** [`docs/ops/UPTIMEROBOT_SETUP.md`](ops/UPTIMEROBOT_SETUP.md)

---

## P1 — 4. Resend email + sending domain — بريد Resend ونطاق الإرسال

**EN — What to do:** Create a Resend account, verify the `dealix.me` sending domain by
adding the SPF/DKIM DNS records Resend gives you, then get the API key.

- In Resend, add domain `dealix.me`. Resend shows a set of DNS records (SPF TXT, DKIM
  CNAME/TXT, optionally DMARC). Add those records at the DNS provider for `dealix.me`.
- Wait for Resend to mark the domain **Verified**.
- Create an API key.

**Why it matters — لماذا يهم:** Without a verified domain and key, the **daily founder
digest** email cannot send — you lose your daily revenue/operations summary. The
domain verification also keeps Dealix mail out of spam. بدون نطاق موثّق ومفتاح، لا
يُرسل ملخّص المؤسس اليومي.

**Where — أين:** https://resend.com → Domains → Add Domain → (add DNS records at your
domain provider) → API Keys → Create API Key.

**Hand back — ما تسلّمه:** add as a **GitHub Actions repository secret** (not a code
file) so the scheduled digest workflow can send:

- `RESEND_API_KEY` = `re_...`

GitHub → repo → Settings → Secrets and variables → Actions → New repository secret.

**Time — الوقت:** ~15 min of work; DNS propagation up to a few hours before
verification completes. انتشار DNS قد يستغرق ساعات.

---

## P1 — 5. GitHub Actions secrets for the Daily Revenue Machine — أسرار التشغيل المجدول

**EN — What to do:** Add two repository secrets so the Daily Revenue Machine cron
workflow can call the production API on schedule.

- `DEALIX_API_BASE` = `https://api.dealix.me`
- `DEALIX_API_KEY` = the production API key (from 1Password `Dealix Production`
  vault — if it does not exist yet, ask the engineer to mint one and you store it).

**Why it matters — لماذا يهم:** The scheduled workflow stays inert without these
secrets — no daily lead prep, no revenue snapshot, no founder digest data. The cron
runs but exits early. تبقى المهمة المجدولة خاملة بدون هذه الأسرار.

**Where — أين:** GitHub → repo → Settings → Secrets and variables → Actions →
New repository secret (×2).

**Hand back — ما تسلّمه:** nothing further — adding the secrets *is* the deliverable.
Tell the engineer once both are set so they can trigger one manual run to confirm.

**Time — الوقت:** ~5 min.

---

## P1 — 6. Deploy the Next.js console — نشر لوحة التحكم

**EN — What to do:** Deploy the `frontend/` Next.js console to a host (Vercel
recommended) and point a subdomain such as `app.dealix.me` at it.

- Import the repo into Vercel, set the project root to `frontend/`.
- Set the environment variable `NEXT_PUBLIC_API_URL` = `https://api.dealix.me`.
- In Vercel → Domains, add `app.dealix.me` and add the CNAME record Vercel shows you
  at your DNS provider.

**Why it matters — لماذا يهم:** The console builds clean but is not deployed — there is
no place for a customer or for you to log in and see results. The first paying
customer expects a working console. لا يوجد مكان لتسجيل الدخول ورؤية النتائج.

**Where — أين:** https://vercel.com → Add New Project → import repo → set root +
env var → Domains.

**Hand back — ما تسلّمه:** confirm to the engineer the live URL (`https://app.dealix.me`)
and that `NEXT_PUBLIC_API_URL` is set on Vercel. If the API needs CORS for the new
origin, the engineer adds it — flag it to them.

**Time — الوقت:** ~30 min including DNS.

---

## P1 — 7. Legal documents — الوثائق القانونية

**EN — What to do:** Publish the privacy policy, terms of use, and a company Data
Processing Agreement (DPA), and confirm PDPL procedures are documented and tested.

- Review and publish the privacy policy and terms (drafts exist in
  [`docs/PRIVACY_POLICY_v2.md`](PRIVACY_POLICY_v2.md) and
  [`docs/TERMS_OF_SERVICE_v2.md`](TERMS_OF_SERVICE_v2.md)) at `dealix.me/privacy` and
  `dealix.me/terms`.
- Approve the company DPA ([`docs/DPA_DEALIX_FULL.md`](DPA_DEALIX_FULL.md)) for use
  with customers.
- Confirm the PDPL data-subject procedures — export, delete, suppression — are
  documented and have been tested at least once
  ([`docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`](PDPL_DATA_SUBJECT_REQUEST_SOP.md),
  [`docs/PRIVACY_PDPL_READINESS.md`](PRIVACY_PDPL_READINESS.md)).

**Why it matters — لماذا يهم:** A paying B2B customer in Saudi Arabia will ask for
these before signing. Publishing them is a legal-authority decision only the founder
can make. عميل B2B سعودي سيطلبها قبل التوقيع، ونشرها قرار بصلاحية المؤسس وحده.

**Where — أين:** the landing site repo (`landing/`) for the public pages; the founder
signs/approves the DPA and the PDPL sign-off.

**Hand back — ما تسلّمه:** the live URLs (`/privacy`, `/terms`) and a one-line
sign-off in [`docs/PRIVACY_PDPL_READINESS.md`](PRIVACY_PDPL_READINESS.md) stating the
export/delete/suppression drill was run and passed, with the date.

**Time — الوقت:** ~1–2 hours of founder review (assuming legal counsel already
reviewed the drafts).

---

## P2 — 8. LinkedIn / X (Twitter) publishing credentials — بيانات نشر المحتوى

**EN — What to do:** Create developer API credentials for the founder's **own**
LinkedIn and X accounts so Dealix's social scheduler can publish Dealix's own posts.

- LinkedIn: create an app at the LinkedIn Developer portal, request the posting
  scopes, and authorise it for the company page.
- X: create a project/app in the X Developer portal and generate the API
  key/secret and access token.

**This is for publishing Dealix's own announcements only — never cold outreach,
never automation against other people's accounts.** هذا لنشر إعلانات ديلكس فقط — لا
تواصل بارد، ولا أتمتة ضد حسابات الآخرين.

**Why it matters — لماذا يهم:** The social scheduler stays queued — drafts accumulate
and nothing publishes — until these credentials exist. It is P2 because launch does
not depend on it; revenue does not. جدولة المحتوى تبقى في قائمة الانتظار حتى توجد هذه
البيانات.

**Where — أين:** https://developer.linkedin.com and https://developer.x.com.

**Hand back — ما تسلّمه:** store in 1Password and give the engineer:

- `LINKEDIN_ACCESS_TOKEN` (and `LINKEDIN_ORG_ID`)
- `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`

**Time — الوقت:** ~30–45 min (X developer access can take a day to approve).

---

## P2 — 9. Domain & DNS housekeeping — ضبط النطاق و DNS

**EN — What to do:** Confirm all three hostnames resolve and have valid TLS:

- `dealix.me` — landing site, valid HTTPS certificate.
- `api.dealix.me` — backend API, valid HTTPS certificate.
- `app.dealix.me` — the console subdomain from item 6, valid HTTPS certificate.

**Why it matters — لماذا يهم:** A broken or expired certificate shows a browser
security warning and instantly destroys trust with a Saudi business buyer. شهادة
معطوبة تُظهر تحذير أمان وتُفقد ثقة المشتري فورًا.

**Where — أين:** your DNS provider's dashboard for `dealix.me`; verify in a browser
and with an SSL checker (e.g. https://www.ssllabs.com/ssltest/).

**Hand back — ما تسلّمه:** confirm to the engineer that all three resolve with valid
TLS, and note any certificate that auto-renews vs needs manual renewal.

**Time — الوقت:** ~15 min.

---

## P2 — 10. First outreach approvals — اعتماد أول دفعة تواصل

**EN — What to do:** Personally review and approve the first batch of message drafts
sitting in the approval queue before anything goes out.

- Open the approval queue, read each draft in full.
- Edit or reject anything off-tone; approve only what you would send yourself.
- Nothing leaves Dealix to an external recipient without your explicit approval —
  this is doctrine, not a setting.

**Why it matters — لماذا يهم:** Dealix never sends an external message without prior
human approval. The very first batch sets the tone of every customer relationship,
and only the founder can sign off on it. أول دفعة تحدّد نبرة كل علاقة عميل، والمؤسس
وحده يعتمدها.

**Where — أين:** the Dealix console approval queue (`app.dealix.me`, available after
item 6) — see [`docs/sales-kit/OUTREACH_DRAFTS_QUEUED.md`](sales-kit/OUTREACH_DRAFTS_QUEUED.md).

**Hand back — ما تسلّمه:** nothing into code — approving (or rejecting) each draft in
the queue *is* the action.

**Time — الوقت:** ~20–30 min for the first batch.

---

## Definition of done — تعريف الإنجاز

**EN —** When **both P0 items (Moyasar live + webhook keys, and Sentry DSN)** are
checked and live in Railway, Dealix can take its first paying customer.

**AR —** عند إنجاز بَندَي P0 (مفاتيح ميسر الحية + الويبهوك، وSentry DSN) وتفعيلهما على
Railway، يصبح بإمكان ديلكس قبول أول عميل يدفع.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
