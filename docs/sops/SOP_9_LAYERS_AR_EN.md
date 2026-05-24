# Dealix — SOPs للايرات التسع
# Dealix — SOPs for the 9 Layers

> **Owner:** dealix-pm
> **Branch:** `claude/vibrant-lovelace-KwZio`
> **Bilingual:** Arabic + English. Each SOP is one page max.

---

## SOP-01 — DATA OS

**هدف / Goal:** ضمان أن كل lead يدخل النظام عبر مصدر مشروع، مع DQ score ≥ 70.
**Goal:** ensure every lead enters via a lawful source with DQ score ≥ 70.

**خطوات / Steps:**
1. AR: استلم البيانات من warm list, inbound form, partner referral, Calendly, demo signup.
   EN: receive data from warm list, inbound form, partner referral, Calendly, demo signup.
2. AR: أنشئ Source Passport (`auto_client_acquisition.data_os.source_passport`).
   EN: create Source Passport.
3. AR: شغّل `validate_account_row` + `compute_dq`.
   EN: run `validate_account_row` + `compute_dq`.
4. AR: إذا DQ < 70، أعد بطلب توضيح من المرسل قبل المعالجة.
   EN: if DQ < 70, request clarification before processing.
5. AR: سجّل Source Passport في الـ ledger.
   EN: register Source Passport in the ledger.

**SLA:** 5 minutes from intake to DQ score.

**Forbidden:** scraping, cold-purchased lists, LinkedIn auto-pulls.

---

## SOP-02 — GOVERNANCE OS

**هدف / Goal:** كل قرار خارجي يمر عبر بوابة الحوكمة قبل التنفيذ.
**Goal:** every external decision passes the governance gate first.

**خطوات / Steps:**
1. AR: استدع `policy_check_draft` لكل نص خارجي.
   EN: call `policy_check_draft` for every external text.
2. AR: استدع `audit_claim_safety` للتأكد من غياب ادعاءات بدون مصدر.
   EN: call `audit_claim_safety` to ensure no unsourced claims.
3. AR: استدع `approval_for_external_channel` للحصول على مستوى الموافقة المطلوب.
   EN: call `approval_for_external_channel` for required approval level.
4. AR: سجّل `governance_decision` على كل output.
   EN: log `governance_decision` on every output.
5. AR: إذا حدثت violation، افتح friction event severity=high.
   EN: if violation occurs, open friction event severity=high.

**SLA:** < 100ms per check.

**Forbidden:** override gate, bypass approval_center, send without governance_decision attached.

---

## SOP-03 — PROOF OS

**هدف / Goal:** كل engagement مدفوع ينتج Proof Pack بدرجة ≥ 70.
**Goal:** every paid engagement yields a Proof Pack with score ≥ 70.

**خطوات / Steps:**
1. AR: ابدأ بـ `build_empty_proof_pack_v2`.
   EN: start with `build_empty_proof_pack_v2`.
2. AR: املأ 14 قسماً (executive_summary, problem, inputs, ..., capital_assets_created).
   EN: fill all 14 sections.
3. AR: تأكد من ربط كل value claim بـ source_ref.
   EN: ensure every value claim has a source_ref.
4. AR: شغّل `proof_pack_completeness_score` + `proof_pack_score_with_governance_penalty`.
   EN: run both score functions.
5. AR: المؤسس يوافق قبل النشر للعميل.
   EN: founder approves before publishing.

**SLA:** 48 hours after sprint completion.

**Required disclaimer:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## SOP-04 — VALUE OS

**هدف / Goal:** سجّل القيمة المالية بثلاثة tiers: estimated → verified → client_confirmed.
**Goal:** record financial value in three tiers.

**خطوات / Steps:**
1. AR: استخدم `value_os.add_event` مع tier="estimated" عند انتهاء sprint.
   EN: use `value_os.add_event` with tier="estimated" at sprint end.
2. AR: حدّث إلى tier="verified" عندما توفر بيانات قابلة للقياس (مع source_ref).
   EN: upgrade to verified once measurable data exists (with source_ref).
3. AR: حدّث إلى tier="client_confirmed" بعد توقيع العميل (مع رابطين مصدر).
   EN: upgrade to client_confirmed after sign-off (two source_refs).
4. AR: لا تخلط estimated مع verified في تقارير العميل.
   EN: never blend estimated and verified in customer-facing reports.

**SLA:** estimated ≤ 24h after sprint; verified ≤ 30d; client_confirmed ≤ 60d.

---

## SOP-05 — CAPITAL OS

**هدف / Goal:** كل engagement مدفوع ينتج ≥ 1 capital asset.
**Goal:** every paid engagement yields ≥ 1 capital asset.

**خطوات / Steps:**
1. AR: تأكد من Moyasar invoice مدفوع (status=paid).
   EN: confirm Moyasar invoice paid.
2. AR: تأكد من proof_pack_score ≥ 70.
   EN: confirm proof_pack_score ≥ 70.
3. AR: اختر نوع الأصل من CapitalAssetType (scoring_rule, draft_template, governance_rule, proof_example, sector_insight, productization_signal).
   EN: select asset type from CapitalAssetType.
4. AR: استدع `capital_os.add_asset` مع invoice_ref و proof_pack_ref.
   EN: call `capital_os.add_asset` with invoice_ref and proof_pack_ref.
5. AR: المؤسس يوافق على التسجيل (founder approval).
   EN: founder approves registration.

**SLA:** 48 hours after payment confirmation.

---

## SOP-06 — ADOPTION OS

**هدف / Goal:** كل عميل يصل إلى adoption_band ≥ B قبل عرض retainer.
**Goal:** every customer reaches adoption_band ≥ B before retainer offer.

**خطوات / Steps:**
1. AR: قِس 8 أبعاد (executive_sponsor, workflow_owner, data_readiness, ...).
   EN: measure 8 dimensions.
2. AR: شغّل `adoption_score` + `adoption_band`.
   EN: run `adoption_score` + `adoption_band`.
3. AR: إذا band < B، فعّل enablement kit (`ENABLEMENT_KIT_ITEMS`).
   EN: if band < B, trigger enablement kit.
4. AR: تابع NPS أسبوعياً + سجّل friction events.
   EN: track NPS weekly + log friction events.

**SLA:** adoption review at day 7, 14, 30, 60, 90.

---

## SOP-07 — CLIENT OS

**هدف / Goal:** كل عميل له workspace معزول مع health score مرئي.
**Goal:** every customer has an isolated workspace with visible health score.

**خطوات / Steps:**
1. AR: أنشئ tenant عبر `admin_tenants.create_tenant`.
   EN: create tenant via `admin_tenants.create_tenant`.
2. AR: طبّق tenant theming من قاعدة بيانات tenant_theme.
   EN: apply tenant theming from tenant_theme DB.
3. AR: عيّن agent transparency cards لكل agent يخدم العميل.
   EN: assign agent transparency cards for each serving agent.
4. AR: ولّد monthly value + governance reports آلياً.
   EN: auto-generate monthly value + governance reports.

**SLA:** tenant ready in 24h after first payment.

---

## SOP-08 — SALES OS

**هدف / Goal:** كل proposal يُولَّد ضمن 24h من إكمال qualification.
**Goal:** every proposal is generated within 24h of qualification completion.

**خطوات / Steps:**
1. AR: شغّل `qualify` على إجابات discovery call.
   EN: run `qualify` on discovery answers.
2. AR: شغّل `icp_score` + `client_risk_score`.
   EN: run `icp_score` + `client_risk_score`.
3. AR: استدع `build_proposal_skeleton` للحصول على هيكل العرض.
   EN: call `build_proposal_skeleton` for proposal skeleton.
4. AR: ادفعه إلى approval_center، لا ترسل مباشرة.
   EN: route to approval_center, never send directly.

**SLA:** ≤ 24h qualification → draft proposal in approval queue.

**Forbidden:** automated send, automated follow-up over WhatsApp/LinkedIn.

---

## SOP-09 — REVENUE INTELLIGENCE OS

**هدف / Goal:** تقرير executive أسبوعي + scorecard CEO شهري.
**Goal:** weekly executive pack + monthly CEO scorecard.

**خطوات / Steps:**
1. AR: شغّل `scripts/dealix_weekly_executive_pack.py` كل أحد.
   EN: run `scripts/dealix_weekly_executive_pack.py` every Sunday.
2. AR: شغّل `dealix_status.py` يومياً.
   EN: run `dealix_status.py` daily.
3. AR: شغّل `monthly_loop` يوم 1 من كل شهر.
   EN: run `monthly_loop` on day 1 of each month.
4. AR: راقب unit economics + capability factory metrics.
   EN: monitor unit economics + capability factory metrics.

**SLA:** weekly pack delivered Sunday 6pm AST.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
