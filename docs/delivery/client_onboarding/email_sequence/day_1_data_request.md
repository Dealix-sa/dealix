# Day 1 — Data sources request (bilingual)

> Draft template — never auto-sent. Founder approves.

**Merge fields:** `{{customer_name}}`, `{{sprint_id}}`, `{{secure_upload_url}}`,
`{{dpa_url}}`, `{{founder_name}}`.

---

## Subject
- AR: اليوم 1 · المصادر التي نحتاجها من شركتكم
- EN: Day 1 — Data sources we need from your team

---

## Body — Arabic

أهلًا {{customer_name}}،

لنبدأ Sprint `{{sprint_id}}` نحتاج المصادر التالية. ارفعها على الرابط
الآمن: [{{secure_upload_url}}]({{secure_upload_url}}) — التشفير
end-to-end، الوصول محدود بفريق Dealix فقط.

**القائمة الأساسية (مطلوب):**

| المصدر | التنسيق المقبول | لماذا نحتاجه |
|--------|-------------------|---------------|
| قائمة العملاء أو الـ leads | CSV / Excel / HubSpot export | لحساب DQ score + ICP match |
| عينة من رسائل outreach السابقة | نص أو CSV (10-20 سجل) | لفهم الأسلوب + تجنب التكرار |
| تعريف ICP الحالي | فقرة واحدة أو 5 سمات | لمقارنة ما تقصده بما نشاهده فعليًا |
| سياسة الـ privacy/PDPL لديكم | PDF أو رابط | لتوافق DPA معنا |

**اختياري (يزيد الدقة):**
- تحليلات CRM (sales velocity، conversion rate)
- prior proof points (case studies إن وجدت)
- نموذج رسالة WhatsApp/Email آخر مرة استخدمتموها

**ضمانات معالجة البيانات:**
- التخزين في Postgres مشفر at-rest، region: KSA (Riyadh) عبر Railway.
- الاحتفاظ: 90 يومًا من تاريخ Sprint ثم حذف تلقائي ما لم نوقع
  managed-ops retainer.
- DPA: راجع [{{dpa_url}}]({{dpa_url}}). نعمل بالـ "lawful basis: legitimate
  interest" مع opt-out متاح.

عند جاهزية الرفع، يبدأ تشغيل الـ DQ pipeline تلقائيًا. تتوقع report
في غضون 24 ساعة.

شكرًا،
{{founder_name}}

---

## Body — English

Hello {{customer_name}},

To start Sprint `{{sprint_id}}` we need the following. Upload to the
secure link: [{{secure_upload_url}}]({{secure_upload_url}}) — end-to-end
encrypted, accessible only by the Dealix team.

**Required:**

| Source | Accepted format | Why we need it |
|--------|------------------|----------------|
| Customer / lead list | CSV / Excel / HubSpot export | DQ score + ICP match |
| Sample of past outreach | Text or CSV (10-20 rows) | Voice alignment + duplicate avoidance |
| Current ICP definition | One paragraph or 5 traits | Compare intent vs reality |
| Privacy/PDPL policy | PDF or URL | DPA alignment |

**Optional (improves precision):**
- CRM analytics (sales velocity, conversion rate)
- Prior proof points (case studies if any)
- Last WhatsApp/Email template used

**Data-handling guarantees:**
- Postgres encrypted-at-rest, region: KSA (Riyadh) via Railway.
- Retention: 90 days from Sprint end then auto-delete unless a
  managed-ops retainer is signed.
- DPA: see [{{dpa_url}}]({{dpa_url}}). Legal basis: legitimate interest,
  with opt-out available.

Once uploaded, the DQ pipeline starts automatically. Expect the report
within 24 hours.

Thanks,
{{founder_name}}

---

## Internal review checklist

- [ ] `secure_upload_url` issued with TTL ≤ 7 days
- [ ] `dpa_url` matches the customer's signed DPA version
- [ ] Retention default confirmed (90d) — adjust if customer requested
      shorter window in kickoff
- [ ] Founder approval before send
