/**
 * Legal content — Privacy Policy + Terms of Service in AR + EN.
 *
 * Source of truth: docs/sales-kit/dealix_privacy_policy_ar.md and
 * docs/sales-kit/dealix_terms_of_service_ar.md. Any change here must be
 * mirrored in those markdown files for legal review; the markdown files
 * remain the canonical artifact for procurement/DPA exchanges.
 *
 * Schema deliberately mirrors LearnArticle so the same renderer pattern
 * (heading + body sections) is reused across the site.
 */

export type LegalSection = { heading: string; body: string };

export type LegalDocument = {
  slug: "privacy" | "terms";
  effectiveDate: string; // ISO date
  titleAr: string;
  titleEn: string;
  tldrAr: string[];
  tldrEn: string[];
  sections: { ar: LegalSection[]; en: LegalSection[] };
};

export const PRIVACY_POLICY: LegalDocument = {
  slug: "privacy",
  effectiveDate: "2026-04-23",
  titleAr: "سياسة الخصوصية",
  titleEn: "Privacy Policy",
  tldrAr: [
    "من نحن: Dealix — Post-Lead Revenue OS سعودي للوكالات والشركات.",
    "ماذا نجمع: بيانات تشغيل المنصة + بيانات العملاء التي تدخلها.",
    "لماذا: تقديم الخدمة، تحسينها، والامتثال للأنظمة.",
    "مع من نشارك: Subprocessors محددون فقط (STC Cloud, Moyasar, PostHog, Sentry).",
    "حقوقك: الوصول، التصحيح، الحذف، النقل، الاعتراض — مُعرّفة أدناه.",
    "الاحتفاظ: تشغيلي 30 يوماً بعد الإلغاء، ثم حذف نهائي.",
    "التواصل: privacy@dealix.sa (مسؤول حماية البيانات).",
  ],
  tldrEn: [
    "Who we are: Dealix — Saudi Post-Lead Revenue OS for agencies and B2B teams.",
    "What we collect: platform-operation data + customer data you input.",
    "Why: deliver the service, improve it, and comply with regulations.",
    "Who we share with: a fixed list of subprocessors (STC Cloud, Moyasar, PostHog, Sentry).",
    "Your rights: access, rectify, delete, port, object — defined below.",
    "Retention: 30 days operational after cancellation, then permanent deletion.",
    "Contact: privacy@dealix.sa (Data Protection Officer).",
  ],
  sections: {
    ar: [
      {
        heading: "1. الأطراف",
        body: "المتحكم (Controller): شركة Dealix للتقنية. مسؤول حماية البيانات (DPO): privacy@dealix.sa. السلطة المختصة: الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA).",
      },
      {
        heading: "2. البيانات التي نجمعها",
        body: "بيانات الحساب (الاسم، البريد، رقم الهاتف، اسم الشركة)، بيانات الدفع (عبر Moyasar فقط — لا نخزن أرقام بطاقات)، بيانات الاستخدام التلقائية (IP، نوع الجهاز، الصفحات المزارة، مدة الجلسة)، وبيانات عملائك (Leads) التي تدخلها أنت بصلاحية تعاقدية معهم.",
      },
      {
        heading: "3. كيف نستخدم البيانات",
        body: "تقديم خدمات Risk Score، Proof Pack، Diagnostic، Managed Ops، والوفاء بالعقود. تحسين المنتج بطرق محكومة (تجميعية، بدون PII في السجلات). الامتثال للوائح (PDPL، نظام مكافحة غسل الأموال، نظام الإثبات الإلكتروني SAR).",
      },
      {
        heading: "4. مع من نشارك البيانات (Subprocessors)",
        body: "STC Cloud (استضافة في المملكة العربية السعودية)، Moyasar (معالجة المدفوعات فقط)، PostHog (تحليلات استخدام مجهولة)، Sentry (تتبع الأخطاء بدون PII). نشر أي subprocessor جديد يحصل عبر إشعار مسبق 30 يوماً عبر البريد الإلكتروني.",
      },
      {
        heading: "5. حقوقك (PDPL مادة 12-15 + GDPR)",
        body: "حق الوصول (DSAR access)، حق التصحيح، حق الحذف، حق نقل البيانات، حق الاعتراض على المعالجة. لممارسة أي حق: قدّم طلب DSAR عبر /legal/dsar وسنرد خلال 5 أيام عمل (الحد الأقصى النظامي 30 يوماً). حق تقديم شكوى للسلطة المختصة (SDAIA).",
      },
      {
        heading: "6. مدة الاحتفاظ",
        body: "بيانات الحساب: طوال فترة الاشتراك + 30 يوماً بعد الإلغاء. بيانات الفواتير: 5 سنوات (نظام الإثبات الإلكتروني SAR). بيانات السجلات الأمنية: 90 يوماً. بعد انقضاء المدة: حذف نهائي مع شهادة حذف مرفوعة في سجل التدقيق.",
      },
      {
        heading: "7. أمان البيانات",
        body: "تشفير TLS 1.3 في النقل، AES-256 في التخزين، فصل بيانات المستأجرين (multi-tenant isolation)، تدوير المفاتيح كل 90 يوماً، اختراق سنوي مستقل (penetration test)، استضافة في حدود المملكة العربية السعودية (data residency).",
      },
      {
        heading: "8. حوادث البيانات",
        body: "نتبع خطة الاستجابة للحوادث الموثقة. في حال أي اختراق بيانات شخصية: إشعار SDAIA خلال 72 ساعة، إشعار المتأثرين خلال 72 ساعة، نشر تقرير ما بعد الحادث (post-incident review) خلال 14 يوماً.",
      },
      {
        heading: "9. ملفات تعريف الارتباط (Cookies)",
        body: "ضرورية (الجلسة، CSRF): لا تحتاج موافقة. اختيارية (التحليلات): نطلب موافقتك صراحة قبل الاستخدام. لا نستخدم Cookies إعلانية تتبعية من أطراف ثالثة.",
      },
      {
        heading: "10. الأطفال",
        body: "خدمة Dealix موجهة للشركات (B2B) فقط. لا نجمع عمداً بيانات من قاصرين دون 18 عاماً. إذا اكتشفنا ذلك، نحذف البيانات فوراً.",
      },
      {
        heading: "11. النقل الدولي للبيانات",
        body: "بيانات Dealix الأساسية مستضافة داخل المملكة العربية السعودية. أي نقل لبيانات شخصية خارج المملكة (مثل إرسال إشعارات بريدية عبر مزود دولي) يتم فقط بأساس قانوني صريح ومع ضمانات تعاقدية كافية (Standard Contractual Clauses).",
      },
    ],
    en: [
      {
        heading: "1. Parties",
        body: "Controller: Dealix Technologies. Data Protection Officer: privacy@dealix.sa. Supervisory authority: Saudi Data & AI Authority (SDAIA).",
      },
      {
        heading: "2. Data we collect",
        body: "Account data (name, email, phone, company name); payment data (via Moyasar only — no card numbers stored); automatic usage data (IP, device type, pages visited, session duration); and your customer leads, which you input under your own contractual basis with those customers.",
      },
      {
        heading: "3. How we use the data",
        body: "To deliver Risk Score, Proof Pack, Diagnostic and Managed Ops services and fulfil our contracts; to improve the product through governed means (aggregate, no PII in logs); to comply with regulations (PDPL, AML, Saudi e-invoicing).",
      },
      {
        heading: "4. Subprocessors",
        body: "STC Cloud (hosting in Saudi Arabia), Moyasar (payment processing only), PostHog (anonymous usage analytics), Sentry (error tracking with no PII). Any new subprocessor is announced 30 days in advance by email.",
      },
      {
        heading: "5. Your rights (PDPL Art. 12–15 + GDPR)",
        body: "Right to access (DSAR access), right to rectify, right to delete, right to data portability, right to object to processing. To exercise any right, file a DSAR via /legal/dsar — we reply within 5 business days (statutory maximum 30 days). You may also lodge a complaint with SDAIA.",
      },
      {
        heading: "6. Retention",
        body: "Account data: throughout the subscription + 30 days after cancellation. Invoice data: 5 years (Saudi e-invoicing law). Security logs: 90 days. After expiry, final deletion is recorded in the audit ledger with a deletion certificate.",
      },
      {
        heading: "7. Security",
        body: "TLS 1.3 in transit, AES-256 at rest, multi-tenant isolation, key rotation every 90 days, annual independent penetration test, data residency inside Saudi Arabia.",
      },
      {
        heading: "8. Data incidents",
        body: "We follow a documented incident response plan. In a personal-data breach: SDAIA notification within 72 hours, affected-party notification within 72 hours, and a post-incident review published within 14 days.",
      },
      {
        heading: "9. Cookies",
        body: "Necessary cookies (session, CSRF) do not require consent. Optional analytics cookies require explicit consent before use. We do not use third-party advertising trackers.",
      },
      {
        heading: "10. Children",
        body: "Dealix is B2B-only. We do not knowingly collect data from anyone under 18. Any such data discovered is deleted immediately.",
      },
      {
        heading: "11. International transfers",
        body: "Core Dealix data is hosted inside Saudi Arabia. Any cross-border personal-data transfer (e.g. transactional email via an international provider) happens only on an explicit legal basis with adequate contractual safeguards (Standard Contractual Clauses).",
      },
    ],
  },
};

export const TERMS_OF_SERVICE: LegalDocument = {
  slug: "terms",
  effectiveDate: "2026-04-23",
  titleAr: "شروط الخدمة",
  titleEn: "Terms of Service",
  tldrAr: [
    "Dealix يقدم Post-Lead Revenue Ops: Risk Score (مجاني)، Diagnostic (499 ر.س)، Proof Pack (1,500 ر.س)، Managed Ops (من 2,999 ر.س شهرياً).",
    "أنت كعميل: تضمن أن لك صلاحية قانونية لإدخال بيانات عملائك (leads).",
    "نحن: لا نضمن نتائج مبيعات. نضمن تنفيذ الخدمة وفق نطاقها الموثق.",
    "الدفع: عبر Moyasar (SAR). الاسترداد خلال 7 أيام من Diagnostic إذا لم تُسلَّم العينة.",
    "الإلغاء: في أي وقت بإشعار 30 يوماً قبل تجديد الاشتراك الشهري.",
    "القانون المختص: نظام المملكة العربية السعودية. الاختصاص: المحاكم الرياضية.",
  ],
  tldrEn: [
    "Dealix delivers Post-Lead Revenue Ops: Risk Score (free), Diagnostic (SAR 499), Proof Pack (SAR 1,500), Managed Ops (from SAR 2,999/month).",
    "You: warrant that you have legal authority to input your customer leads.",
    "We: do not guarantee sales outcomes. We do guarantee scope-of-work execution.",
    "Payment: via Moyasar in SAR. 7-day refund window on Diagnostic if no sample delivered.",
    "Cancellation: anytime with 30 days notice before monthly renewal.",
    "Governing law: Kingdom of Saudi Arabia. Jurisdiction: Riyadh courts.",
  ],
  sections: {
    ar: [
      {
        heading: "1. التعريف والقبول",
        body: "بإنشاء حساب أو استخدام أي خدمة من Dealix، توافق على هذه الشروط. إن لم توافق، لا تستخدم الخدمة.",
      },
      {
        heading: "2. الخدمات",
        body: "Risk Score: فحص ذاتي مجاني لإشارات الحوكمة. Diagnostic (499 ر.س): تشخيص 7 أيام لـ 10 leads مع Proof Pack عينة. Proof Pack (1,500 ر.س): تقرير كامل لـ 20-50 lead. Managed Ops (2,999-4,999 ر.س شهرياً): تشغيل Post-Lead Revenue Ops مستمر مع SLA موثق. Custom AI Setup (5,000-25,000 ر.س + 1,000 ر.س شهرياً): إعداد مخصص.",
      },
      {
        heading: "3. التزامات العميل",
        body: "أنت تضمن أن لديك صلاحية قانونية لإدخال بيانات leads (موافقة العميل، أساس قانوني PDPL مادة 5/13). أنت تتحمل مسؤولية دقة البيانات. أنت تلتزم بعدم استخدام Dealix لإرسال بارد أو spam أو scraping.",
      },
      {
        heading: "4. التزاماتنا",
        body: "تنفيذ الخدمة وفق نطاق العمل (Statement of Work) الموثق. توافر 99.5% (Managed Ops). استجابة DSAR خلال 5 أيام عمل. لا نضمن نتائج مبيعات أو تحويلات أو إيرادات — هذا خارج عن سيطرتنا ويعتمد على السوق وفريقك. لا نضمن نتائج مضمونة (هذا أحد non-negotiables Dealix).",
      },
      {
        heading: "5. الدفع",
        body: "كل المبالغ بالريال السعودي عبر Moyasar. تجدد الاشتراكات الشهرية تلقائياً. يمكنك الإلغاء في أي وقت قبل 30 يوماً من التجديد. سياسة استرداد محددة: 7 أيام لـ Diagnostic إذا لم تُسلَّم العينة. لا استرداد للأشهر المنقضية من Managed Ops.",
      },
      {
        heading: "6. الملكية الفكرية",
        body: "Dealix يملك المنصة، الكود، الواجهات، والـ trademarks. أنت تملك بياناتك ومخرجات Proof Pack الخاصة بك. ترخيص محدود لاستخدام المنصة طوال فترة الاشتراك.",
      },
      {
        heading: "7. تحديد المسؤولية",
        body: "مسؤولية Dealix الإجمالية في أي 12 شهراً محدودة بمبلغ ما دفعته خلال نفس الفترة. لا نتحمل أي خسائر غير مباشرة (فقدان أرباح، خسائر سمعة). هذا التحديد لا يطبّق على: الاحتيال المتعمد، الإهمال الجسيم، أو خرق التزامات أمن البيانات الأساسية.",
      },
      {
        heading: "8. الإنهاء",
        body: "أنت تستطيع الإلغاء في أي وقت بإشعار 30 يوماً. نحن نستطيع الإلغاء عند خرقك للشروط (بإشعار 14 يوماً للتصحيح إن أمكن). عند الإنهاء: تصدير بياناتك خلال 30 يوماً، ثم حذف نهائي مع شهادة.",
      },
      {
        heading: "9. القانون المختص",
        body: "نظام المملكة العربية السعودية. أي نزاع يحل أولاً بالتفاوض الودي خلال 30 يوماً، ثم بالتحكيم في الرياض وفق نظام التحكيم السعودي، ثم بالمحاكم المختصة في الرياض.",
      },
      {
        heading: "10. التحديثات",
        body: "نحتفظ بحق تعديل هذه الشروط بإشعار 30 يوماً عبر البريد الإلكتروني. الاستمرار في الاستخدام بعد التعديل يعد قبولاً.",
      },
    ],
    en: [
      {
        heading: "1. Definitions and acceptance",
        body: "By creating an account or using any Dealix service, you agree to these terms. If you do not agree, do not use the service.",
      },
      {
        heading: "2. Services",
        body: "Risk Score: free self-scan of governance signals. Diagnostic (SAR 499): 7-day diagnostic of 10 leads with a sample Proof Pack. Proof Pack (SAR 1,500): full report for 20–50 leads. Managed Ops (SAR 2,999–4,999/month): continuous Post-Lead Revenue Ops with documented SLA. Custom AI Setup (SAR 5,000–25,000 + SAR 1,000/month): bespoke setup.",
      },
      {
        heading: "3. Customer obligations",
        body: "You warrant you have legal authority to input lead data (customer consent or another lawful basis under PDPL Art. 5/13). You are responsible for data accuracy. You commit not to use Dealix for cold outreach, spam, or scraping.",
      },
      {
        heading: "4. Our obligations",
        body: "Deliver services per the documented Statement of Work. 99.5% availability for Managed Ops. DSAR response within 5 business days. We do NOT guarantee sales outcomes, conversions, or revenue — those depend on your market and team. Guaranteed-outcome language is one of Dealix's non-negotiables.",
      },
      {
        heading: "5. Payment",
        body: "All amounts in SAR via Moyasar. Monthly subscriptions auto-renew. You may cancel anytime with 30 days notice before renewal. Refund policy: 7 days on Diagnostic if no sample was delivered. No refunds on elapsed Managed Ops months.",
      },
      {
        heading: "6. Intellectual property",
        body: "Dealix owns the platform, code, interfaces, and trademarks. You own your data and your Proof Pack outputs. Limited license to use the platform during the subscription.",
      },
      {
        heading: "7. Limitation of liability",
        body: "Dealix's total liability in any 12-month period is capped at fees paid during that period. We are not liable for indirect losses (lost profits, reputation damage). This cap does not apply to intentional fraud, gross negligence, or core data-security breaches.",
      },
      {
        heading: "8. Termination",
        body: "You may cancel anytime with 30 days notice. We may terminate on your breach (with 14 days notice to cure when possible). On termination: data export available for 30 days, then permanent deletion with a certificate.",
      },
      {
        heading: "9. Governing law",
        body: "Laws of the Kingdom of Saudi Arabia. Disputes are resolved first by good-faith negotiation within 30 days, then by arbitration in Riyadh under the Saudi arbitration law, then by the competent courts in Riyadh.",
      },
      {
        heading: "10. Updates",
        body: "We may amend these terms with 30 days notice by email. Continued use after the change is acceptance.",
      },
    ],
  },
};
