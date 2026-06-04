# Failure Response Playbook — دليل الاستجابة للأعطال

> When something fails, follow the first/second/third action for that case. No fix may introduce automated external sending of any kind.
>
> عند حدوث عطل، اتبع الإجراء الأول/الثاني/الثالث لتلك الحالة. لا يجوز لأي إصلاح أن يُدخل إرسالًا خارجيًا آليًا من أي نوع.

---

## EN — Response table

| Failure | First action | Second action | Third action |
|---|---|---|---|
| Website build failed | Run `scripts/site_launch_static_check.py`, read the error | Fix the failing page/asset locally | Re-run check; deploy only when green |
| Safety audit failed | Stop all outreach immediately | Open `safety_audit.json`, find the violating drafts | Fix the draft template; re-run `commercial_safety_audit.py` until zero |
| Drafts < 400 | Re-run `commercial_generate_400_drafts.py` | Check `daily_metrics.json` for the cause (lead pool, filters) | Top up the lead pool; never lower the safety flags to inflate count |
| Workflow failed | Open the GitHub Actions run log | Confirm `permissions: contents: read`, no secrets, artifacts only | Fix the failing step; re-run; never add secrets |
| API health failed | Run `scripts/api_commercial_static_check.py` | Check the live `/health` separately from the static scan | Restart/redeploy the API; confirm no send endpoints exist |
| Spam / complaint signal | Pause outreach to that segment | Review which approved messages went out and why | Tighten copy + targeting; document the change |
| LinkedIn restriction | Stop all LinkedIn activity | Confirm no automation was used (manual-only is the rule) | Operate within the LinkedIn User Agreement; appeal if wrongly flagged |
| WhatsApp compliance issue | Stop any WhatsApp outreach | Confirm no cold/bulk/automated sending occurred | Use only opted-in, manual, business-policy-compliant contact |
| Lead quality weak | Review source tracking in CRM | Tighten vertical and qualification criteria | Re-load a cleaner lead set; re-run drafts |
| No replies | Review the top-50 copy and targeting | A/B two manual message variants on a small set | Shift effort to the vertical with evidenced response |
| High rejection rate | Pause and read rejected drafts | Identify the common failure (tone, relevance, claim) | Revise the template; re-generate; re-review |
| Founder overwhelmed | Cut the daily review to top 20, not 50 | Batch outreach to two focused windows | Defer non-critical content; protect the safety + review steps first |

### Hard rule under pressure
No failure justifies enabling auto-send, storing forbidden PII, or sending from GitHub Actions. If a "fix" requires any of these, the answer is NO-GO.

---

## AR — جدول الاستجابة

| العطل | الإجراء الأول | الإجراء الثاني | الإجراء الثالث |
|---|---|---|---|
| فشل بناء الموقع | شغّل `scripts/site_launch_static_check.py` واقرأ الخطأ | أصلح الصفحة/الأصل المعطوب محليًا | أعد الفحص؛ انشر فقط عند الأخضر |
| فشل تدقيق الأمان | أوقف كل التواصل فورًا | افتح `safety_audit.json` وجد المسودات المخالفة | أصلح قالب المسودة؛ أعد `commercial_safety_audit.py` حتى صفر |
| المسودات < 400 | أعد تشغيل `commercial_generate_400_drafts.py` | افحص `daily_metrics.json` للسبب (مجمع العملاء، المرشحات) | عزّز مجمع العملاء؛ لا تخفّض أعلام الأمان لتضخيم العدد |
| فشل سير العمل | افتح سجل تشغيل GitHub Actions | تأكد من `permissions: contents: read`، بدون أسرار، مخرجات فقط | أصلح الخطوة المعطوبة؛ أعد التشغيل؛ لا تضف أسرارًا |
| فشل صحة الواجهة البرمجية | شغّل `scripts/api_commercial_static_check.py` | افحص `/health` الحي منفصلًا عن الفحص الثابت | أعد تشغيل/نشر الواجهة؛ تأكد من عدم وجود نقاط إرسال |
| إشارة إزعاج / شكوى | أوقف التواصل لتلك الشريحة | راجع أي رسائل معتمدة خرجت ولماذا | شدّد النص والاستهداف؛ وثّق التغيير |
| تقييد لينكدإن | أوقف كل نشاط لينكدإن | تأكد من عدم استخدام أي أتمتة (القاعدة يدوي فقط) | اعمل ضمن اتفاقية مستخدم لينكدإن؛ اعترض إن وُسمت خطأً |
| مشكلة امتثال واتساب | أوقف أي تواصل واتساب | تأكد من عدم حدوث إرسال بارد/بالجملة/آلي | استخدم فقط تواصلًا بموافقة مسبقة، يدويًا، متوافقًا مع سياسة الأعمال |
| ضعف جودة العملاء | راجع تتبع المصدر في CRM | شدّد معايير القطاع والتأهيل | أعد تحميل مجموعة عملاء أنظف؛ أعد المسودات |
| لا ردود | راجع نص واستهداف أعلى 50 | اختبر نسختين يدويتين على مجموعة صغيرة | حوّل الجهد للقطاع ذي الاستجابة المُثبتة |
| ارتفاع معدل الرفض | أوقف واقرأ المسودات المرفوضة | حدد الفشل الشائع (النبرة، الصلة، الادعاء) | نقّح القالب؛ أعد التوليد؛ أعد المراجعة |
| إرهاق المؤسس | قلّص المراجعة اليومية لأعلى 20 لا 50 | جمّع التواصل في نافذتين مركّزتين | أجّل المحتوى غير الحرج؛ احمِ خطوتي الأمان والمراجعة أولًا |

### قاعدة صارمة تحت الضغط
لا عطل يبرر تفعيل الإرسال التلقائي، أو تخزين PII ممنوع، أو الإرسال من GitHub Actions. إذا تطلّب أي "إصلاح" أيًا من هذا، فالجواب توقّف.

---

Related: [Go / No-Go Matrix](02_GO_NO_GO_MATRIX.md) · [Daily Command Center](05_DAILY_COMMAND_CENTER.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
