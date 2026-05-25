# Dealix — Sample AI Use Policy — سياسة استخدام الذكاء الاصطناعي (نموذج)

> Bilingual sample. Customer must tailor sections marked `{{ ... }}` and have legal counsel review. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### 1. الغرض
تحدّد هذه السياسة كيف تستخدم `{{ شركة العميل }}` أدوات الذكاء الاصطناعي عبر منصّة Dealix، وما هو المسموح، وما هو الممنوع، ومن يملك القرار.

### 2. النطاق
تنطبق هذه السياسة على كل وكيل AI مسجَّل في Agent Registry، وكل أداة مدرَجة في Tool Permission Matrix، وكل مخرج يُولَّد داخل المستأجِر.

### 3. المبادئ
1. **لا إيراد بدون دليل** — كل إيراد منسوب إلى الـ AI يجب أن يرتبط بـ Evidence Pack.
2. **سيادة المالك** — الإجراءات الحساسة تتطلّب موافقة صريحة من المالك المُسمّى.
3. **لا إرسال خارجي بدون إذن** — لا ترسل أي رسالة لطرف خارجي دون موافقة لكل رسالة.
4. **طبقة تدقيق دائمة** — كل تشغيل وكيل مُسجَّل بـ context_hash في AI Run Ledger.

### 4. الاستخدامات المسموحة
- توليد مسودّات داخلية يراجعها بشر قبل الإرسال.
- تصنيف وفرز الواردات.
- تلخيص مستندات داخلية للموظفين المخوّلين.
- تشغيل خدمات S1–S7 وفق نطاقها المُعلن.

### 5. الاستخدامات الممنوعة
- scraping للمواقع بما يخالف شروطها.
- أتمتة WhatsApp أو LinkedIn الباردة.
- استخراج بيانات شخصية من مصادر غير مرخّصة.
- اتخاذ قرارات قانونية أو طبية أو مالية نهائية دون مراجعة بشرية.
- نسخ نصوص محمية بحقوق طبع ونشرها بصفة المصدر.

### 6. أدوار وملكية
- **المالك** (`{{ owner_role }}`): يوافق على الإجراءات الحساسة.
- **DPO**: يراجع الالتزام بـ PDPL ويُدير DSAR.
- **مسؤول الحوكمة**: يراجع Agent Registry وTool Permission Matrix شهريًا.
- **المُستخدِم**: مسؤول عن مراجعة مخرجات الـ AI قبل الاستخدام.

### 7. البيانات
- لا تُدخَل بيانات شخصية حسّاسة في موجِّهات (prompts) عامّة.
- المصادر مُعلَنة في Source Passport.
- الاحتفاظ يخضع لـ [DATA_BOUNDARIES_SAMPLE.md](DATA_BOUNDARIES_SAMPLE.md).

### 8. الموافقات
- **Tier 0**: تلخيص داخلي — مسموح بدون موافقة.
- **Tier 1**: مسودّة موجَّهة لطرف خارجي — تتطلّب موافقة بشرية واحدة.
- **Tier 2**: إرسال خارجي — تتطلّب موافقة المالك المُسمّى ولكل رسالة.
- **Tier 3**: تعديل بيانات إنتاجية — تتطلّب موافقتين مستقلّتين.

### 9. الحوادث
أي سلوك وكيل خارج النطاق يُبلَّغ خلال 24 ساعة عبر [INCIDENT_RESPONSE_SAMPLE.md](INCIDENT_RESPONSE_SAMPLE.md).

### 10. المراجعة
تُراجَع هذه السياسة كل 6 أشهر أو عند أي تغيير جوهري في AI Run Ledger.

---

## English

### 1. Purpose
This policy defines how `{{ Customer Company }}` uses AI tools through the Dealix platform: what is allowed, what is prohibited, and who owns each decision.

### 2. Scope
Applies to every AI agent registered in the Agent Registry, every tool listed in the Tool Permission Matrix, and every output generated inside the tenant.

### 3. Principles
1. **No revenue without evidence** — every revenue claim attributed to AI must link to an Evidence Pack.
2. **Owner sovereignty** — sensitive actions require explicit approval from the named owner.
3. **No external sends without consent** — no message leaves the tenant to a third party without per-message approval.
4. **Persistent audit layer** — every agent run is logged with a context_hash in the AI Run Ledger.

### 4. Allowed Uses
- Internal draft generation reviewed by humans before sending.
- Classification and triage of inbound items.
- Summarization of internal documents for authorized employees.
- Operating S1–S7 services within their declared scope.

### 5. Prohibited Uses
- Scraping sites in violation of their terms.
- Cold WhatsApp or LinkedIn automation.
- Extraction of personal data from unlicensed sources.
- Final legal, medical, or financial decisions without human review.
- Copying copyrighted text and publishing it as source.

### 6. Roles and Ownership
- **Owner** (`{{ owner_role }}`): approves sensitive actions.
- **DPO**: reviews PDPL compliance and manages DSAR.
- **Governance lead**: monthly review of Agent Registry and Tool Permission Matrix.
- **User**: responsible for reviewing AI outputs before use.

### 7. Data
- No sensitive personal data placed in general-purpose prompts.
- Sources declared in the Source Passport.
- Retention governed by [DATA_BOUNDARIES_SAMPLE.md](DATA_BOUNDARIES_SAMPLE.md).

### 8. Approval Tiers
- **Tier 0**: internal summarization — no approval needed.
- **Tier 1**: external-facing draft — one human approval.
- **Tier 2**: external send — named owner approval, per message.
- **Tier 3**: production data mutation — two independent approvals.

### 9. Incidents
Any agent behavior outside scope is reported within 24 hours via [INCIDENT_RESPONSE_SAMPLE.md](INCIDENT_RESPONSE_SAMPLE.md).

### 10. Review
This policy is reviewed every 6 months or after any material change in the AI Run Ledger.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
