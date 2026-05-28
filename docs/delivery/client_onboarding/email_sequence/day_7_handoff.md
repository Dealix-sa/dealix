# Day 7 — Sprint handoff (bilingual)

> Draft template — never auto-sent. Founder approves.

**Merge fields:** `{{customer_name}}`, `{{sprint_id}}`, `{{proof_pack_final_url}}`,
`{{nps_link}}`, `{{managed_ops_url}}`, `{{founder_name}}`.

---

## Subject
- AR: اليوم 7 · Proof Pack نهائي + الخطوات التالية
- EN: Day 7 — Final Proof Pack + next steps

---

## Body — Arabic

أهلًا {{customer_name}}،

اكتمل Sprint `{{sprint_id}}`. هذه الـ deliverables النهائية:

**1. Proof Pack نهائي (ثنائي اللغة، 14 قسم)**
[{{proof_pack_final_url}}]({{proof_pack_final_url}})

تحتوي على:
- Executive Summary (AR + EN)
- Methodology + قيود البيانات
- DQ Score + توصيات
- Top-20 prospects نهائي مع evidence لكل صف
- 10 outreach drafts معتمدة (أرشيف 5)
- Gap analysis + ROI estimate (محدد is_estimate=True)
- 30/60/90 roadmap
- Doctrine compliance attestation
- Glossary بالعربية والإنجليزية

**2. أصول قابلة للنقل لفريقك**
- HubSpot import file (لو الـ retainer غير مفعّل، الـ records تُحذف
  بعد 90 يومًا)
- Email templates approved (markdown مع merge fields)
- WhatsApp scripts approved (لا تستخدمها للـ cold)
- Founder briefing summary (1 صفحة)

**3. الخطوات التالية (اختيارية)**
- **خيار A — Managed Revenue Ops** (٢٩٩٩ ر.س/شهر): استمرار من حيث
  انتهى Sprint، تشغيل دائم للأسطول، proof events جديدة شهريًا. تفاصيل:
  [{{managed_ops_url}}]({{managed_ops_url}})
- **خيار B — Custom AI engagement** (٥-٢٥ ألف ر.س): مشروع محدد على
  Workflow معين.
- **خيار C — End of engagement**: نحذف بياناتكم بعد ٩٠ يومًا تلقائيًا.

**4. NPS — تقييم تجربتك (٢ دقيقة)**
رأيك يحسّن Dealix للعميل التالي. الـ feedback يدخل proof ledger
بصراحة (مجهول الهوية إن أردت).
[{{nps_link}}]({{nps_link}})

**شكر صريح:**
كنت أول من فتح لنا فرصة العمل في sector {{customer_name}} بهذا
العمق. كل proof event سجّلناه معك يخدم رواد الأعمال السعوديين القادمين.

شكرًا،
{{founder_name}}

---

## Body — English

Hello {{customer_name}},

Sprint `{{sprint_id}}` is complete. Final deliverables:

**1. Final Proof Pack (bilingual, 14 sections)**
[{{proof_pack_final_url}}]({{proof_pack_final_url}})

Contains:
- Executive Summary (AR + EN)
- Methodology + data limitations
- Final DQ Score + recommendations
- Final Top-20 prospects with evidence per row
- 10 approved outreach drafts (5 archived)
- Gap analysis + ROI estimate (is_estimate=True flag)
- 30/60/90 roadmap
- Doctrine compliance attestation
- Arabic + English glossary

**2. Portable assets for your team**
- HubSpot import file (if no retainer activated, records auto-delete
  in 90 days)
- Approved email templates (markdown with merge fields)
- Approved WhatsApp scripts (do not use for cold outreach)
- Founder briefing summary (1 page)

**3. Next steps (optional)**
- **Option A — Managed Revenue Ops** (2,999 SAR/mo): continue where
  the Sprint left off, ongoing fleet operation, new proof events
  monthly. Details: [{{managed_ops_url}}]({{managed_ops_url}})
- **Option B — Custom AI engagement** (5-25K SAR): targeted workflow
  project.
- **Option C — End of engagement**: we auto-delete your data after
  90 days.

**4. NPS — rate your experience (2 min)**
Your feedback improves Dealix for the next customer. Feedback enters
the proof ledger transparently (anonymously if you prefer).
[{{nps_link}}]({{nps_link}})

**Direct thanks:**
You were the first to open the door for us in
{{customer_name}}'s sector at this depth. Every proof event we
captured with you serves the next Saudi entrepreneur.

Thanks,
{{founder_name}}

---

## Internal review checklist

- [ ] Proof Pack final == signed-off Proof Pack v2 (no late edits)
- [ ] Portable assets bundled in single zip
- [ ] HubSpot import file validated
- [ ] managed_ops_url leads to the correct plan page
- [ ] NPS link generates a fresh response token
- [ ] Doctrine compliance attestation signed by founder
- [ ] Founder approval before send
