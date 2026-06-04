# Final Launch Control Tower — برج التحكم النهائي للإطلاق

> Review-only launch system. Nothing sends externally. Every outreach draft is blocked from auto-send and requires manual founder approval before any human action.
>
> نظام إطلاق للمراجعة فقط. لا يُرسل أي شيء خارجيًا. كل مسودة تواصل محظورة من الإرسال التلقائي وتتطلب موافقة يدوية من المؤسس قبل أي إجراء بشري.

---

## EN — What this is

The Final Launch Control Tower is the single coordination layer for the Dealix commercial launch across five Saudi B2B verticals: Logistics & Last-Mile, Contracting & Construction, Private Clinics & Healthcare, Professional Services, and Industrial & Manufacturing.

It connects a **draft factory** (400+ review-only outreach drafts per day), a **founder review queue**, a **media & social OS**, a **CRM / Lead Ops layer**, and a set of **verification scripts** that prove readiness without sending anything externally.

### What is ready (automated, internal only)
- Generation of 400+/day outreach drafts — every draft carries `send_allowed=false`, `external_send_blocked=true`, `no_auto_send=true`, `requires_founder_approval=true`.
- Safety audit over every draft and output.
- Founder review report and top-50 priority list.
- Media & social 30-day calendar generation (planning only).
- Static checks for website, API source, and CRM schema.
- Daily GitHub Actions run that produces artifacts only (no secrets, read-only).

### What is still manual (by design)
- All outreach happens **after** the founder approves a draft, sent manually by the founder.
- Discovery calls, diagnostic delivery, proposals, retainer conversations.
- All social posting — drafted by the OS, posted by a human.
- Any decision to spend on paid ads.

### What is forbidden to automate (never)
- Automated email / SMTP sending.
- WhatsApp cold outreach or outbound automation.
- LinkedIn automation (connect, message, scrape) — forbidden by the LinkedIn User Agreement.
- Website contact-form auto-submit.
- Bulk sending of any kind.
- Sending from GitHub Actions.
- Scraping or collecting sensitive personal data before a signed agreement.

---

## AR — ما هذا

برج التحكم النهائي للإطلاق هو طبقة التنسيق الواحدة لإطلاق ديالكس التجاري عبر خمسة قطاعات سعودية بين الشركات: اللوجستيات والميل الأخير، المقاولات والإنشاءات، العيادات الخاصة والرعاية الصحية، الخدمات المهنية، والصناعة والتصنيع.

يربط البرج بين **مصنع المسودات** (أكثر من 400 مسودة تواصل للمراجعة يوميًا)، و**طابور مراجعة المؤسس**، و**نظام الإعلام والتواصل الاجتماعي**، و**طبقة إدارة العملاء المحتملين (CRM)**، ومجموعة من **سكربتات التحقق** التي تُثبت الجاهزية دون إرسال أي شيء خارجيًا.

### ما هو جاهز (آلي، داخلي فقط)
- توليد أكثر من 400 مسودة تواصل يوميًا — كل مسودة تحمل `send_allowed=false` و`external_send_blocked=true` و`no_auto_send=true` و`requires_founder_approval=true`.
- تدقيق أمان على كل مسودة ومخرج.
- تقرير مراجعة المؤسس وقائمة أولوية أعلى 50.
- توليد تقويم الإعلام والتواصل لمدة 30 يومًا (تخطيط فقط).
- فحوصات ثابتة للموقع ومصدر الواجهة البرمجية ومخطط CRM.
- تشغيل يومي عبر GitHub Actions ينتج مخرجات فقط (بدون أسرار، قراءة فقط).

### ما يزال يدويًا (بالتصميم)
- كل تواصل يحدث **بعد** موافقة المؤسس على المسودة، ويُرسله المؤسس يدويًا.
- مكالمات الاستكشاف، تسليم التشخيص، العروض، محادثات العقود الشهرية.
- كل النشر الاجتماعي — تُكتب بواسطة النظام وينشرها إنسان.
- أي قرار بالإنفاق على الإعلانات المدفوعة.

### ما يُمنع أتمتته (أبدًا)
- الإرسال الآلي للبريد الإلكتروني / SMTP.
- تواصل واتساب البارد أو الأتمتة الصادرة.
- أتمتة لينكدإن (الإضافة، الرسائل، الكشط) — ممنوعة بموجب اتفاقية مستخدم لينكدإن.
- الإرسال التلقائي لنموذج الاتصال بالموقع.
- الإرسال بالجملة بأي شكل.
- الإرسال من GitHub Actions.
- كشط أو جمع بيانات شخصية حساسة قبل اتفاق موقّع.

---

## Links — الروابط

| Item / العنصر | Path / المسار |
|---|---|
| Master verifier | `scripts/final_launch_control_verify.py` |
| Draft factory (400+/day) | `scripts/commercial_generate_400_drafts.py` |
| Safety audit | `scripts/commercial_safety_audit.py` |
| Launch readiness | `scripts/commercial_launch_readiness.py` |
| Media/social calendar generator | `scripts/media_social_calendar_generate.py` |
| Media/social verifier | `scripts/media_social_verify.py` |
| Site static check | `scripts/site_launch_static_check.py` |
| API source static check | `scripts/api_commercial_static_check.py` |
| CRM schema verifier | `scripts/commercial_crm_schema_verify.py` |
| Secret + risk scan | `scripts/final_secret_and_risk_scan.py` |
| Daily workflow | `.github/workflows/final-launch-control.yml` |
| Draft queue output | `outputs/commercial_launch/latest/draft_queue.jsonl` |
| Founder review | `outputs/commercial_launch/latest/founder_review.md` |
| Top 50 priority | `outputs/commercial_launch/latest/top_50_priority.md` |
| Safety audit output | `outputs/commercial_launch/latest/safety_audit.json` |
| Daily metrics | `outputs/commercial_launch/latest/daily_metrics.json` |
| Media/social outputs | `outputs/media_social/` |
| Control tower outputs | `outputs/final_launch_control/` |
| CRM schema | `config/crm_pipeline_schema.json` |
| Media/social calendar config | `config/media_social_calendar.json` |

### Companion docs / المستندات المصاحبة
- [Launch Scorecard](01_LAUNCH_SCORECARD.md)
- [Go / No-Go Matrix](02_GO_NO_GO_MATRIX.md)
- [Evidence Pack](03_EVIDENCE_PACK.md)
- [30-Day War Room](04_30_DAY_WAR_ROOM.md)
- [Daily Command Center](05_DAILY_COMMAND_CENTER.md)
- [Failure Response Playbook](06_FAILURE_RESPONSE_PLAYBOOK.md)
- [Founder Execution Checklist](07_FOUNDER_EXECUTION_CHECKLIST.md)
- [Lead Ops Final QA](../commercial-launch/23_LEAD_OPS_FINAL_QA.md)
- [Media & Social OS](../media-social-os/00_MEDIA_SOCIAL_OS.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
