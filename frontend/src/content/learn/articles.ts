export type LearnSection = { heading: string; body: string };

export type LearnArticle = {
  slug: string;
  titleAr: string;
  titleEn: string;
  descriptionAr: string;
  descriptionEn: string;
  readTimeMinAr?: string;
  readTimeMinEn?: string;
  sections: { ar: LearnSection[]; en: LearnSection[] };
};

export const LEARN_ARTICLES: LearnArticle[] = [
  {
    slug: "post-lead-revenue-ops",
    titleAr: "ما هو Post-Lead Revenue Ops؟",
    titleEn: "What is Post-Lead Revenue Ops?",
    descriptionAr: "تشغيل ما يحدث بعد وصول الـ lead — مالك، دليل، موافقة، خطوة تالية.",
    descriptionEn: "Operating what happens after the lead — owner, proof, approval, next step.",
    readTimeMinAr: "4 دقائق",
    readTimeMinEn: "4 min read",
    sections: {
      ar: [
        { heading: "التعريف", body: "Post-Lead Revenue Ops هو تشغيل ما يحدث بعد وصول الـ lead: من يملك المتابعة؟ ما الدليل؟ ما الموافقة؟ Dealix لا يستبدل CRM — يثبت قرار إيراد موثّق." },
        { heading: "متى تحتاجه", body: "الإعلانات تجيب leads لكن الإدارة تسأل ماذا حدث؟ لا owner واضح؟ follow-up غير موثّق؟ وكالة تحتاج Proof Pack لعميلها؟" },
        { heading: "خطوات SOAEN", body: "Source — Owner خلال 15 دقيقة — Approval قبل الإرسال — Evidence لكل رد — Next Action بتاريخ واحد." },
        { heading: "الفرق عن CRM", body: "CRM يسجّل. Revenue Ops يُثبِت. الفرق: evidence trail قابل للتدقيق بدون مسافة بين اللمسة والقرار." },
      ],
      en: [
        { heading: "Definition", body: "Post-Lead Revenue Ops runs what happens after a lead arrives: who owns follow-up, what proof exists, what approval is required. Dealix does not replace your CRM — it documents revenue decisions." },
        { heading: "When you need it", body: "Ads bring leads but leadership asks what happened next. No clear owner. Undocumented follow-up. An agency needs a Proof Pack for their client." },
        { heading: "SOAEN steps", body: "Source — Owner within 15 minutes — Approval before external send — Evidence per reply — One next action with a date." },
        { heading: "Difference from CRM", body: "CRM records. Revenue Ops proves. The difference: an auditable evidence trail without a gap between the touch and the decision." },
      ],
    },
  },
  {
    slug: "what-is-proof-pack",
    titleAr: "ما هو Proof Pack؟",
    titleEn: "What is a Proof Pack?",
    descriptionAr: "حزمة إثبات منظمة للوكالة أو العميل — أقسام وحالة واضحة.",
    descriptionEn: "A structured proof bundle for agency or client — clear sections and status.",
    readTimeMinAr: "3 دقائق",
    readTimeMinEn: "3 min read",
    sections: {
      ar: [
        { heading: "التعريف", body: "Proof Pack ليس تقريراً عاماً — هو أقسام (مصادر، أصحاب، أدلة، قرارات) كل قسم له حالة: مكتمل، بانتظار مدخلات، أو محظور." },
        { heading: "لماذا للوكالات", body: "العميل يريد إثباتاً أسبوعياً بعد الحملة. Dealix يعطيك مسودة حوكَمة + عينة عامة قبل الشراء." },
        { heading: "مستويات الأدلة", body: "L0–L5: من فرضية إلى إثبات قابل للتدقيق. L0=فرضية، L1=مؤشر، L2=منطقي، L3=موثّق، L4=مُثبَت، L5=مُتحقَّق خارجياً. لا upsell قبل L4." },
        { heading: "ما يحتوي عليه Proof Pack", body: "1) مصادر الـ leads وجودتها — 2) ملاك القرارات وسرعة الاستجابة — 3) سجل الأدلة لكل محادثة — 4) قرارات الإيراد المُثبَتة وتوصيات التوسع." },
      ],
      en: [
        { heading: "Definition", body: "A Proof Pack is not a generic PDF — it is sections (sources, owners, evidence, decisions) each with status: complete, pending inputs, or blocked." },
        { heading: "Why agencies", body: "Clients want weekly proof after campaigns. Dealix gives governed drafts plus a public sample before purchase." },
        { heading: "Evidence levels", body: "L0–L5: from hypothesis to auditable proof. L0=hypothesis, L1=indicator, L2=logical, L3=documented, L4=proven, L5=externally verified. No upsell before L4." },
        { heading: "What a Proof Pack contains", body: "1) Lead sources and quality — 2) Decision owners and response speed — 3) Evidence log per conversation — 4) Proven revenue decisions and expansion recommendations." },
      ],
    },
  },
  {
    slug: "crm-vs-revenue-ops",
    titleAr: "CRM مقابل Revenue Ops — أين الفجوة؟",
    titleEn: "CRM vs Revenue Ops — where is the gap?",
    descriptionAr: "CRM يسجّل؛ Revenue Ops يثبت القرار بعد الـ lead.",
    descriptionEn: "CRM records; Revenue Ops proves the decision after the lead.",
    readTimeMinAr: "5 دقائق",
    readTimeMinEn: "5 min read",
    sections: {
      ar: [
        { heading: "CRM يفعل", body: "جهات اتصال، مراحل، مهام، تقارير خط أنابيب. أدوات ممتازة للتسجيل والتتبع." },
        { heading: "ما لا يفعله CRM", body: "لا يفرض موافقة قبل واتساب. لا يربط كل لمسة بحدث دليل. لا يحدّ العروض على السطح. لا يُنتج Proof Pack للعميل." },
        { heading: "دور Dealix", body: "طبقة حوكمة + أدلة + 3 عروض سطح — فوق CRM الحالي بدون استبداله. Dealix يُضيف: Evidence Trail، Approval Center، Proof Pack." },
        { heading: "متى تحتاج كليهما", body: "CRM للتسجيل + Dealix للإثبات. الشركة التي تريد الامتثال لـ PDPL وZATCA تحتاج كليهما معاً." },
      ],
      en: [
        { heading: "CRM does", body: "Contacts, stages, tasks, pipeline reports. Excellent tools for recording and tracking." },
        { heading: "What CRM does not", body: "No approval gate before WhatsApp. No evidence event per touch. No surface-offer boundary. No Proof Pack for the client." },
        { heading: "Dealix role", body: "Governance + evidence + three surface offers — on top of your CRM, not replacing it. Dealix adds: Evidence Trail, Approval Center, Proof Pack." },
        { heading: "When you need both", body: "CRM for recording + Dealix for proving. A company that wants PDPL and ZATCA compliance needs both together." },
      ],
    },
  },
  {
    slug: "no-cold-whatsapp-policy",
    titleAr: "لماذا لا واتساب بارد في Dealix؟",
    titleEn: "Why no cold WhatsApp in Dealix?",
    descriptionAr: "سياسة PDPL + ثقة السوق السعودي — مسودات وموافقة فقط.",
    descriptionEn: "PDPL + Saudi market trust — drafts and approval only.",
    readTimeMinAr: "4 دقائق",
    readTimeMinEn: "4 min read",
    sections: {
      ar: [
        { heading: "السياسة", body: "لا إرسال واتساب بارد آلي. لا LinkedIn DM آلي. كل إرسال خارجي يمر بموافقة بشرية. هذا مبدأ #2 من المبادئ الـ 11 غير القابلة للتفاوض." },
        { heading: "لماذا PDPL يمنعه", body: "PDPL (نظام حماية البيانات الشخصية) يشترط موافقة صريحة قبل التواصل التجاري. Cold WhatsApp يُعرّضك لغرامات تصل لـ 5 مليون ر.س." },
        { heading: "البديل", body: "قوائم warm معتمدة، مسودات من آلة اليوم، 10 لمسات يدوية مسجّلة في Evidence. Dealix يُنتج المسودة، أنت تراجع وترسل يدوياً." },
        { heading: "النتيجة", body: "ثقة أعلى، مخاطر امتثال أقل، Proof حقيقي لا أرقام مخترعة. السوق السعودي يشتري بالثقة والعلاقات — لا بالـ spam." },
      ],
      en: [
        { heading: "Policy", body: "No automated cold WhatsApp. No automated LinkedIn DMs. Every external send requires human approval. This is principle #2 of the 11 non-negotiables." },
        { heading: "Why PDPL prohibits it", body: "PDPL (Personal Data Protection Law) requires explicit consent before commercial communication. Cold WhatsApp exposes you to fines up to 5M SAR." },
        { heading: "Alternative", body: "Approved warm lists, daily draft machine, 10 manual touches logged as Evidence events. Dealix generates the draft, you review and send manually." },
        { heading: "Outcome", body: "Higher trust, lower compliance risk, real proof not invented metrics. Saudi market buys on trust and relationships — not spam." },
      ],
    },
  },
  {
    slug: "10-lead-audit",
    titleAr: "10-Lead Audit — متى تطلبه؟",
    titleEn: "10-Lead Audit — when to request it?",
    descriptionAr: "مراجعة 10 leads مع توصية حوكمة — عرض سطح للوكالات.",
    descriptionEn: "Review 10 leads with governance recommendation — surface offer for agencies.",
    readTimeMinAr: "3 دقائق",
    readTimeMinEn: "3 min read",
    sections: {
      ar: [
        { heading: "المدخلات", body: "قائمة leads حقيقية (تصدير CRM أو جدول) — بدون scraping. ملاحظة: نعمل فقط مع leads موجودة، لا نجلب leads جديدة." },
        { heading: "المخرجات", body: "مالك لكل lead، فجوات أدلة، مسودة Proof، خطوة تالية واحدة. السعر: 499 ر.س. الوقت: 48 ساعة." },
        { heading: "الخطوة التالية", body: "Agency Proof Pack (1,500 ر.س) أو Governed Diagnostic 7 أيام (من 4,999 ر.س) حسب الجاهزية والحجم." },
        { heading: "لمن هو مناسب", body: "وكالات تسويق تريد إثبات قيمة لعميلها. فرق مبيعات B2B تريد تنظيف pipeline. مؤسسون يريدون فهم سبب ضعف التحويل." },
      ],
      en: [
        { heading: "Inputs", body: "A real lead list (CRM export or sheet) — no scraping. Note: we work with existing leads only, we do not generate new leads." },
        { heading: "Outputs", body: "Owner per lead, evidence gaps, Proof draft, one next action. Price: 499 SAR. Time: 48 hours." },
        { heading: "Next step", body: "Agency Proof Pack (1,500 SAR) or 7-Day Governed Diagnostic (from 4,999 SAR) based on readiness and scale." },
        { heading: "Who is it for", body: "Marketing agencies proving value to clients. B2B sales teams wanting to clean their pipeline. Founders wanting to understand why conversion is low." },
      ],
    },
  },
  {
    slug: "audit-lead-follow-up",
    titleAr: "متابعة الـ lead بعد التدقيق",
    titleEn: "Lead follow-up after audit",
    descriptionAr: "من التشخيص إلى الاجتماع — بدون تسريب.",
    descriptionEn: "From diagnostic to meeting — without leakage.",
    readTimeMinAr: "3 دقائق",
    readTimeMinEn: "3 min read",
    sections: {
      ar: [
        { heading: "خلال 24 ساعة", body: "تأكيد المالك، مسودة رسالة واحدة، موافقة، إرسال يدوي، سجل Evidence." },
        { heading: "خلال 7 أيام", body: "إما اجتماع أو Proof Pack عينة أو closed_lost مع سبب." },
        { heading: "حوكمة", body: "لا أكثر من 3 عروض على السطح في أي محادثة. هذا يحمي العلاقة ويحافظ على الثقة." },
      ],
      en: [
        { heading: "Within 24 hours", body: "Confirm owner, one draft message, approval, manual send, Evidence log." },
        { heading: "Within 7 days", body: "Meeting booked, sample Proof Pack, or closed_lost with reason." },
        { heading: "Governance", body: "No more than three surface offers in any conversation. This protects the relationship and maintains trust." },
      ],
    },
  },
  {
    slug: "pdpl-guide-saudi-b2b-2026",
    titleAr: "دليل PDPL للشركات السعودية B2B — 2026",
    titleEn: "PDPL Guide for Saudi B2B Companies — 2026",
    descriptionAr: "كل ما تحتاج معرفته عن نظام حماية البيانات الشخصية وكيف يؤثر على عمليات B2B في السعودية.",
    descriptionEn: "Everything you need to know about PDPL and how it affects B2B operations in Saudi Arabia.",
    readTimeMinAr: "8 دقائق",
    readTimeMinEn: "8 min read",
    sections: {
      ar: [
        { heading: "ما هو PDPL؟", body: "نظام حماية البيانات الشخصية هو التشريع السعودي الشامل لحماية البيانات، دخل حيز التنفيذ في 2024. يُلزم كل شركة تعالج بيانات أشخاص في السعودية — سواء كانت سعودية أو أجنبية." },
        { heading: "ما يُلزمك PDPL بفعله", body: "1) الحصول على موافقة صريحة قبل معالجة البيانات. 2) توثيق غرض معالجة البيانات. 3) منح صاحب البيانات حق الوصول والتصحيح والحذف. 4) الإخطار بأي خرق خلال 72 ساعة. 5) تعيين مسؤول حماية بيانات (DPO) إذا كانت الشركة كبيرة." },
        { heading: "الغرامات", body: "مخالفات PDPL يمكن أن تصل غراماتها لـ 5 مليون ريال سعودي. للمخالفات الجسيمة يُضاف حبس لسنة. التوعية والامتثال الوقائي أرخص بكثير من الغرامة." },
        { heading: "ما يعنيه للـ B2B", body: "لا شراء قوائم leads. لا cold WhatsApp آلي. كل تواصل تجاري يحتاج موافقة مسبقة أو علاقة تجارية قائمة. سجلات CRM تحتاج consent timestamp." },
        { heading: "كيف يساعد Dealix", body: "Approval Center يُوثّق موافقة قبل كل إرسال خارجي. Audit Trail كامل لكل عملية بيانات. لا automated cold outreach — هذا مبدأ غير قابل للتفاوض. PDPL Compliance رُكِّز في النظام من البداية." },
        { heading: "خطوات الامتثال الفورية", body: "1) افحص قاعدة بيانات CRM: هل لكل جهة اتصال consent مُوثَّق؟ 2) راجع عمليات التواصل: هل هناك cold outreach آلي؟ 3) أضف consent checkbox لكل نموذج جمع بيانات. 4) وثّق سياسة حذف البيانات. 5) عيّن DPO إذا كانت الشركة تُعالج بيانات واسعة النطاق." },
      ],
      en: [
        { heading: "What is PDPL?", body: "The Personal Data Protection Law is Saudi Arabia's comprehensive data protection legislation, effective since 2024. It applies to every company processing data of people in Saudi Arabia — whether Saudi or foreign." },
        { heading: "What PDPL requires", body: "1) Obtain explicit consent before processing data. 2) Document the purpose of data processing. 3) Grant data subjects rights to access, correct, and delete. 4) Notify of any breach within 72 hours. 5) Appoint a Data Protection Officer (DPO) for large-scale processing." },
        { heading: "Penalties", body: "PDPL violations can reach 5 million SAR in fines. Serious violations add up to 1 year imprisonment. Compliance is far cheaper than the fine." },
        { heading: "What it means for B2B", body: "No buying lead lists. No automated cold WhatsApp. All commercial communication requires prior consent or an existing business relationship. CRM records need consent timestamps." },
        { heading: "How Dealix helps", body: "Approval Center documents consent before every external send. Full Audit Trail for every data operation. No automated cold outreach — this is a non-negotiable principle. PDPL compliance was built into the system from day one." },
        { heading: "Immediate compliance steps", body: "1) Audit CRM database: does every contact have documented consent? 2) Review communication processes: is there any automated cold outreach? 3) Add consent checkbox to every data collection form. 4) Document data deletion policy. 5) Appoint DPO if company processes large-scale data." },
      ],
    },
  },
  {
    slug: "zatca-wave-24-guide",
    titleAr: "دليل ZATCA Wave 24 — الموعد النهائي يونيو 2026",
    titleEn: "ZATCA Wave 24 Guide — June 2026 Deadline",
    descriptionAr: "كل شركة تجاوزت 375,000 ر.س إيراداً ملزمة بالفوترة الإلكترونية المتكاملة. إليك ما يجب فعله الآن.",
    descriptionEn: "Every company exceeding 375,000 SAR revenue must comply with Phase 2 e-invoicing. Here's what to do now.",
    readTimeMinAr: "7 دقائق",
    readTimeMinEn: "7 min read",
    sections: {
      ar: [
        { heading: "ما هي ZATCA Wave 24؟", body: "هيئة الزكاة والضريبة والجمارك تُلزم الشركات بتطبيق الفوترة الإلكترونية المتكاملة (Phase 2) على مراحل. Wave 24 تشمل الشركات التي تجاوزت 375,000 ر.س إيراداً في 2022. الموعد النهائي: 30 يونيو 2026." },
        { heading: "ما الفرق بين Phase 1 وPhase 2؟", body: "Phase 1 (ديسمبر 2021): توليد وحفظ الفواتير رقمياً. Phase 2: ربط النظام مباشرة بـ ZATCA وإرسال كل فاتورة في الوقت الفعلي. Phase 2 أكثر تعقيداً وتحتاج API integration." },
        { heading: "الغرامات", body: "عدم الامتثال يعني: غرامات مالية، وقف التسجيل الضريبي، صعوبة في المناقصات الحكومية. الامتثال المبكر أوفر وأأمن." },
        { heading: "خطوات الامتثال", body: "1) تحديد إذا كانت الشركة ضمن Wave 24. 2) اختيار نظام فوترة ZATCA-compliant. 3) ربط النظام بـ ZATCA API. 4) اختبار الربط قبل الموعد النهائي بشهرين. 5) تدريب الفريق على العمليات الجديدة." },
        { heading: "كيف يساعد Dealix", body: "ZATCA Readiness diagnostic مدمج في نظام التشخيص. Proof Pack يتضمن تقييم جاهزية ZATCA. مساعدة في اختيار المورد المناسب وخطة التطبيق. التركيز: نُجهّزك للامتثال ونُحسّن إيراداتك في نفس الوقت." },
        { heading: "هل شركتي ضمن Wave 24؟", body: "إذا تجاوز إيراد شركتك 375,000 ر.س في عام 2022 وكانت مسجلة في الفترة المحددة، فأنت ضمن Wave 24. ابدأ بـ Risk Score في Dealix لتعرف وضعك بالتفصيل." },
      ],
      en: [
        { heading: "What is ZATCA Wave 24?", body: "The Zakat, Tax and Customs Authority mandates integrated e-invoicing (Phase 2) in waves. Wave 24 covers companies that exceeded 375,000 SAR in 2022 revenue. Deadline: June 30, 2026." },
        { heading: "What's the difference between Phase 1 and Phase 2?", body: "Phase 1 (December 2021): digital invoice generation and storage. Phase 2: direct integration with ZATCA system, sending every invoice in real-time. Phase 2 requires API integration and is more complex." },
        { heading: "Penalties", body: "Non-compliance means: financial fines, tax registration suspension, difficulty in government tenders. Early compliance is cheaper and safer." },
        { heading: "Compliance steps", body: "1) Determine if your company is in Wave 24. 2) Choose a ZATCA-compliant invoicing system. 3) Connect to ZATCA API. 4) Test integration 2 months before deadline. 5) Train team on new processes." },
        { heading: "How Dealix helps", body: "ZATCA Readiness diagnostic built into the diagnostic system. Proof Pack includes ZATCA readiness assessment. Help selecting the right vendor and implementation plan. Focus: we get you compliant while improving your revenue ops simultaneously." },
        { heading: "Is my company in Wave 24?", body: "If your company's revenue exceeded 375,000 SAR in 2022 and was registered in the specified period, you're in Wave 24. Start with Dealix's Risk Score to understand your position in detail." },
      ],
    },
  },
  {
    slug: "ai-governance-saudi-b2b",
    titleAr: "حوكمة AI في B2B السعودي — لماذا الآن؟",
    titleEn: "AI Governance in Saudi B2B — Why Now?",
    descriptionAr: "استخدام AI بدون حوكمة = مخاطر امتثال وقرارات غير موثّقة. كيف تبني AI مسؤولاً في عمليات B2B؟",
    descriptionEn: "Using AI without governance = compliance risks and undocumented decisions. How to build responsible AI in B2B operations.",
    readTimeMinAr: "6 دقائق",
    readTimeMinEn: "6 min read",
    sections: {
      ar: [
        { heading: "المشكلة", body: "كثير من الشركات تستخدم AI (ChatGPT، Copilot، وغيرها) في العمليات اليومية دون توثيق: من أجاز هذا القرار؟ ما المصدر؟ هل هو صحيح؟ هذا يُعرّضك لمخاطر PDPL وقرارات غير قابلة للتدقيق." },
        { heading: "ما هي حوكمة AI؟", body: "حوكمة AI هي: 1) سياسات واضحة لاستخدام AI. 2) موافقة بشرية قبل تنفيذ أي قرار AI حرج. 3) سجل Audit Trail لكل قرار AI. 4) حدود واضحة لما يملكه AI وما يملكه الإنسان." },
        { heading: "Approval-First Architecture", body: "مبدأ Dealix: كل قرار AI حرج يمر بـ Approval Center قبل التنفيذ. AI يُقترح، الإنسان يُقرّر. لا إرسال تلقائي. لا تنفيذ بدون مراجعة. هذا يحميك قانونياً ويبني ثقة العميل." },
        { heading: "Company Brain — الذاكرة المؤسسية", body: "Company Brain في Dealix يجمع معرفة شركتك في مكان واحد مع مصادر واضحة. كل إجابة مرتبطة بمصدر. لا إجابة بدون مصدر. هذا يمنع الهلوسة ويُبني ذاكرة مؤسسية قابلة للتدقيق." },
        { heading: "خطوات البناء المسؤول", body: "1) وثّق كل use case لـ AI في شركتك. 2) حدّد من يراجع قرارات AI. 3) أضف Audit Trail لكل قرار AI. 4) لا ترسل خارجياً بدون مراجعة بشرية. 5) راجع PDPL compliance لكل AI processing." },
        { heading: "السوق السعودي خصيصاً", body: "السوق السعودي يشتري بالثقة والعلاقات. AI محكوم يبني ثقة. AI غير محكوم يدمر علاقات عمل استغرق بناؤها سنوات. الاستثمار في الحوكمة ليس عبئاً — هو ميزة تنافسية." },
      ],
      en: [
        { heading: "The Problem", body: "Many companies use AI (ChatGPT, Copilot, etc.) in daily operations without documenting: who approved this decision? What's the source? Is it correct? This exposes you to PDPL risks and non-auditable decisions." },
        { heading: "What is AI Governance?", body: "AI Governance means: 1) Clear policies for AI usage. 2) Human approval before executing any critical AI decision. 3) Audit Trail for every AI decision. 4) Clear boundaries for what AI owns vs. what humans own." },
        { heading: "Approval-First Architecture", body: "Dealix principle: every critical AI decision goes through Approval Center before execution. AI proposes, humans decide. No automated sending. No execution without review. This protects you legally and builds client trust." },
        { heading: "Company Brain — Institutional Memory", body: "Company Brain in Dealix gathers your company's knowledge in one place with clear sources. Every answer is linked to a source. No answer without a source. This prevents hallucination and builds auditable institutional memory." },
        { heading: "Responsible Building Steps", body: "1) Document every AI use case in your company. 2) Define who reviews AI decisions. 3) Add Audit Trail for every AI decision. 4) Don't send externally without human review. 5) Review PDPL compliance for every AI processing activity." },
        { heading: "Saudi Market Specifically", body: "Saudi market buys on trust and relationships. Governed AI builds trust. Ungoverned AI destroys business relationships that took years to build. Investing in governance is not a burden — it's a competitive advantage." },
      ],
    },
  },
  {
    slug: "revenue-leakage-detection",
    titleAr: "تسرّب الإيراد — كيف تكشفه وتوقفه؟",
    titleEn: "Revenue Leakage — How to Detect and Stop It",
    descriptionAr: "معظم الشركات تخسر 10-20% من إيراداتها في تسريبات غير مرئية. كيف تكتشفها وتُصلحها؟",
    descriptionEn: "Most companies lose 10-20% of revenue in invisible leakages. How to detect and fix them.",
    readTimeMinAr: "6 دقائق",
    readTimeMinEn: "6 min read",
    sections: {
      ar: [
        { heading: "ما هو تسرّب الإيراد؟", body: "تسرّب الإيراد هو الفجوة بين الإيراد المحتمل والإيراد الفعلي. يُسبّبه: leads لم تُتابَع، صفقات تأخّرت بلا سبب، خصومات غير مُوثَّقة، عملاء لم يُجدَّد عقدهم، وأخطاء في الفواتير." },
        { heading: "المؤشرات الرئيسية", body: "1) معدل تحويل leads أقل من 20%: يشير لمشكلة follow-up. 2) متوسط زمن إغلاق صفقة أطول من المعيار الصناعي: يشير لعوائق غير محددة. 3) خصومات متكررة بدون توثيق: تسريب مالي مباشر. 4) عملاء لم يجدّدوا بدون تواصل: تسريب retention." },
        { heading: "أنواع التسريبات الشائعة في السعودية", body: "لوجستيات: تأخّر فواتير بسبب عدم الامتثال لـ ZATCA. خدمات B2B: leads من LinkedIn لا تُتابَع خلال 24 ساعة. عقارات: عروض أسعار غير موثّقة تُفقَد. مقاولات: تعديلات scope بدون أوامر تغيير رسمية." },
        { heading: "كيف يكشف Dealix التسريبات", body: "Diagnostic 7 أيام يحلّل: 1) كل مرحلة في pipeline ومعدل التحويل. 2) زمن الاستجابة لكل lead. 3) الصفقات المُغلَقة الخاسرة وأسبابها. 4) الفواتير غير المُحصَّلة. يُنتج: خريطة تسريبات ذات أولويات + الإجراءات الـ 3 الأعلى أثراً." },
        { heading: "خطوات الإصلاح", body: "1) حدّد أكبر نقطة تسريب (عادة follow-up أو الفواتير). 2) عيّن مالكاً واضحاً لكل leads. 3) أضف SLA 24 ساعة لأول رد. 4) وثّق سبب كل صفقة خاسرة. 5) ابنِ Proof Pack لقياس التحسّن." },
        { heading: "كم يُكلّف عدم الإصلاح؟", body: "شركة بإيراد 2M ر.س/سنة مع تسريب 15% = 300,000 ر.س سنوياً مفقودة. تشخيص Dealix يبدأ من 499 ر.س. العائد المحتمل على الاستثمار يتجاوز 100x في أول شهر." },
      ],
      en: [
        { heading: "What is revenue leakage?", body: "Revenue leakage is the gap between potential revenue and actual revenue. Caused by: un-followed leads, delayed deals without reason, undocumented discounts, unrenewed client contracts, and invoicing errors." },
        { heading: "Key indicators", body: "1) Lead conversion rate below 20%: indicates follow-up problem. 2) Average deal close time longer than industry benchmark: indicates unidentified blockers. 3) Repeated discounts without documentation: direct financial leakage. 4) Clients who didn't renew without contact: retention leakage." },
        { heading: "Common leakage types in Saudi Arabia", body: "Logistics: delayed invoices due to ZATCA non-compliance. B2B services: LinkedIn leads not followed up within 24 hours. Real estate: undocumented price quotes lost. Construction: scope changes without formal change orders." },
        { heading: "How Dealix detects leakages", body: "7-day Diagnostic analyzes: 1) Every pipeline stage and conversion rate. 2) Response time per lead. 3) Lost deals and their reasons. 4) Uncollected invoices. Produces: prioritized leakage map + top 3 highest-impact actions." },
        { heading: "Fix steps", body: "1) Identify the biggest leakage point (usually follow-up or invoicing). 2) Assign a clear owner for all leads. 3) Add 24-hour SLA for first response. 4) Document reason for every lost deal. 5) Build Proof Pack to measure improvement." },
        { heading: "What does not fixing cost?", body: "A company with 2M SAR/year revenue and 15% leakage = 300,000 SAR lost annually. Dealix diagnostic starts from 499 SAR. Potential ROI exceeds 100x in the first month." },
      ],
    },
  },
  {
    slug: "zatca-penalties-guide",
    titleAr: "غرامات ZATCA: ماذا يحدث إذا فاتك موعد يونيو 2026؟",
    titleEn: "ZATCA Penalties: What Happens If You Miss the June 2026 Deadline?",
    descriptionAr: "الغرامات التصاعدية وإيقاف الترخيص — دليل عملي لكل شركة سعودية B2B معرّضة للمخاطر.",
    descriptionEn: "Escalating fines and license suspension — a practical guide for every at-risk Saudi B2B company.",
    readTimeMinAr: "5 دقائق",
    readTimeMinEn: "5 min read",
    sections: {
      ar: [
        { heading: "من يتأثر بـ Wave 24؟", body: "كل شركة إيراداتها السنوية تتجاوز 375,000 ريال سعودي ملزمة بالامتثال لـ ZATCA Phase 2 قبل 30 يونيو 2026. هذا يشمل الغالبية العظمى من شركات B2B السعودية في القطاعات: العقارات، اللوجستيات، الاستشارات، التقنية، والمقاولات." },
        { heading: "هيكل الغرامات التصاعدي", body: "المخالفة الأولى: تحذير رسمي. التأخير البسيط: حتى 5,000 ريال. الامتثال الجزئي: 5,000 إلى 50,000 ريال. رفض الامتثال: حتى 100,000 ريال. المخالفات المتكررة: إيقاف الترخيص التجاري. الغرامات تتراكم يومياً حتى اكتمال الامتثال." },
        { heading: "ماذا تعني هذه الأرقام فعلياً؟", body: "شركة إيراداتها 3 ملايين ريال ومعدل تأخير 60 يوماً قد تواجه غرامات تتجاوز 200,000 ريال — وهو رقم أكبر بكثير من تكلفة التجهيز الكاملة. التجهيز المبكر أرخص دائماً من الغرامة." },
        { heading: "الأخطاء الأكثر شيوعاً", body: "الاعتقاد بأن Phase 1 كافية: خطأ — Phase 2 تتطلب Clearance مباشر مع ZATCA. الاعتماد على المحاسب فقط: الامتثال يحتاج تكاملاً تقنياً مع نظام ERP. التأجيل حتى اليوم الأخير: عملية التسجيل والاختبار وحدها تأخذ 3 إلى 8 أسابيع." },
        { heading: "الجدول الزمني الواقعي", body: "التسجيل في بوابة ZATCA: أسبوع. الحصول على شهادة رقمية: أسبوعان. تكييف نظام ERP: 2 إلى 6 أسابيع. اختبار Sandbox: أسبوعان. الإطلاق الإنتاجي: أسبوع. المجموع: 7 إلى 12 أسبوعاً. بدأ بيونيو، بقي أقل من 5 أسابيع." },
        { heading: "خطوتك الأولى اليوم", body: "لا تبدأ بالتقنية — ابدأ بتشخيص واضح: هل نظامك متوافق؟ ما الفجوات؟ من المسؤول؟ Sprint 7 أيام من Dealix يعطيك خريطة ZATCA readiness كاملة وخطة عمل واضحة لفريقك التقني — 499 ريال فقط." },
      ],
      en: [
        { heading: "Who's affected by Wave 24?", body: "Every company with annual revenue exceeding 375,000 SAR must comply with ZATCA Phase 2 by June 30, 2026. This covers the vast majority of Saudi B2B companies in: real estate, logistics, consulting, technology, and construction." },
        { heading: "The escalating fine structure", body: "First violation: official warning. Minor delay: up to SAR 5,000. Partial compliance: SAR 5,000 to 50,000. Refusing compliance: up to SAR 100,000. Repeated violations: commercial license suspension. Fines accumulate daily until full compliance." },
        { heading: "What these numbers mean in practice", body: "A company with 3M SAR revenue and a 60-day delay could face fines exceeding 200,000 SAR — far more than the total cost of getting compliant. Early preparation is always cheaper than fines." },
        { heading: "Most common mistakes", body: "Believing Phase 1 is enough: wrong — Phase 2 requires direct Clearance with ZATCA. Relying on the accountant alone: compliance requires technical ERP integration. Waiting until the last day: registration, testing alone take 3 to 8 weeks." },
        { heading: "Realistic timeline", body: "ZATCA portal registration: 1 week. Digital certificate: 2 weeks. ERP adaptation: 2–6 weeks. Sandbox testing: 2 weeks. Production launch: 1 week. Total: 7–12 weeks. Starting in June leaves less than 5 weeks." },
        { heading: "Your first step today", body: "Don't start with technology — start with a clear diagnosis: is your system compatible? What are the gaps? Who's responsible? Dealix's 7-day Sprint gives you a complete ZATCA readiness map and clear action plan for your tech team — only SAR 499." },
      ],
    },
  },
  {
    slug: "zatca-einvoicing-phase2-setup",
    titleAr: "الفاتورة الإلكترونية Phase 2: كيف تنجز الربط مع ZATCA خطوة بخطوة",
    titleEn: "E-Invoicing Phase 2: How to Complete Your ZATCA Integration Step by Step",
    descriptionAr: "من التسجيل إلى الإطلاق الإنتاجي — دليل تقني مبسّط لأصحاب الأعمال والفرق التقنية.",
    descriptionEn: "From registration to production launch — a simplified technical guide for business owners and tech teams.",
    readTimeMinAr: "7 دقائق",
    readTimeMinEn: "7 min read",
    sections: {
      ar: [
        { heading: "الفرق بين Phase 1 و Phase 2", body: "Phase 1 (2022): إنشاء فاتورة XML وحفظها محلياً. Phase 2 (Clearance Model): كل فاتورة B2B يجب أن تُرسل لـ ZATCA وتحصل على ختم الموافقة قبل إرسالها للعميل. Reporting Model للـ B2C: ترسل خلال 24 ساعة. الفرق الجوهري: من نظام محلي إلى نظام متصل بـ ZATCA في الوقت الحقيقي." },
        { heading: "متطلبات ZATCA التقنية", body: "1) شهادة رقمية CSID (Cryptographic Stamp ID) من ZATCA. 2) فواتير بصيغة UBL 2.1 XML مع hash وQR Code. 3) توقيع رقمي لكل فاتورة. 4) API Integration مع ZATCA Fatoora portal. 5) اختبار ناجح في بيئة Simulation قبل الإنتاج." },
        { heading: "خطوات التسجيل والتجهيز", body: "الخطوة 1: تسجيل في بوابة Fatoora وإنشاء حساب. الخطوة 2: طلب شهادة CSID وتفعيلها (1-2 أسبوع). الخطوة 3: تكييف نظام ERP أو برنامج المحاسبة لإنتاج UBL 2.1 XML. الخطوة 4: اختبار الاتصال في Simulation Environment. الخطوة 5: الحصول على Production Certificate والإطلاق." },
        { heading: "اختيار نظام ERP المناسب", body: "الأنظمة المتوافقة مع ZATCA Wave 24: SAP Business One، Oracle NetSuite، Microsoft Dynamics 365، Odoo، Zoho Books (بتحديثات محلية)، وبعض الأنظمة المحلية السعودية. إذا كنت تستخدم برنامج محاسبة قديم، قد تحتاج ترقية أو middleware." },
        { heading: "الأخطاء التقنية الشائعة", body: "توليد QR Code بصيغة خاطئة (TLV encoding). Hash SHA-256 غير صحيح للفاتورة. Certificate غير مفعّل في بيئة الإنتاج. Timeout في API calls بدون retry logic. عدم تخزين UUID لكل فاتورة للرجوع إليها لاحقاً." },
        { heading: "كيف يساعدك Dealix؟", body: "Dealix لا يستبدل فريقك التقني — لكنه يعطيهم خارطة طريق واضحة: ما المطلوب بالضبط؟ أي فجوات في نظامك الحالي؟ ما الأولوية؟ Sprint 7 أيام يُنتج ZATCA readiness map كاملة مع قائمة تحقق تقنية — بدليل موثَّق وليس تقدير عام." },
      ],
      en: [
        { heading: "The difference between Phase 1 and Phase 2", body: "Phase 1 (2022): create XML invoice and store locally. Phase 2 (Clearance Model): every B2B invoice must be sent to ZATCA and receive an approval stamp before sending to the client. Reporting Model for B2C: sent within 24 hours. Core difference: from a local system to a real-time ZATCA-connected system." },
        { heading: "ZATCA technical requirements", body: "1) Digital certificate CSID (Cryptographic Stamp ID) from ZATCA. 2) Invoices in UBL 2.1 XML format with hash and QR Code. 3) Digital signature for every invoice. 4) API Integration with ZATCA Fatoora portal. 5) Successful test in Simulation environment before production." },
        { heading: "Registration and setup steps", body: "Step 1: Register on Fatoora portal and create account. Step 2: Request CSID certificate and activate it (1–2 weeks). Step 3: Adapt ERP or accounting software to produce UBL 2.1 XML. Step 4: Test connectivity in Simulation Environment. Step 5: Obtain Production Certificate and launch." },
        { heading: "Choosing the right ERP system", body: "ZATCA Wave 24 compatible systems: SAP Business One, Oracle NetSuite, Microsoft Dynamics 365, Odoo, Zoho Books (with local updates), and some local Saudi systems. If you're using legacy accounting software, you may need an upgrade or middleware." },
        { heading: "Common technical mistakes", body: "Wrong QR Code format (TLV encoding). Incorrect SHA-256 hash for the invoice. Certificate not activated in production environment. API call timeouts without retry logic. Not storing UUID for each invoice for future reference." },
        { heading: "How Dealix helps", body: "Dealix doesn't replace your tech team — it gives them a clear roadmap: what's needed exactly? Which gaps exist in your current system? What's the priority? A 7-day Sprint produces a complete ZATCA readiness map with a technical checklist — with documented evidence, not general estimates." },
      ],
    },
  },
  {
    slug: "saudi-b2b-compliance-checklist-2026",
    titleAr: "قائمة الامتثال الشاملة لشركات B2B السعودية في 2026",
    titleEn: "Complete Compliance Checklist for Saudi B2B Companies in 2026",
    descriptionAr: "ZATCA + PDPL + AI Governance + Revenue Ops — كل ما تحتاجه في قائمة واحدة قابلة للتنفيذ.",
    descriptionEn: "ZATCA + PDPL + AI Governance + Revenue Ops — everything you need in one actionable checklist.",
    readTimeMinAr: "6 دقائق",
    readTimeMinEn: "6 min read",
    sections: {
      ar: [
        { heading: "لماذا 2026 عام امتثال حاسم؟", body: "ثلاثة متطلبات تشريعية تتزامن في 2026: ZATCA Wave 24 (يونيو 2026)، PDPL بنظامه التنفيذي الكامل، ولوائح AI Governance الإقليمية الجديدة. الشركات التي تتجاهل هذا التزامن تخاطر بغرامات متعددة في وقت واحد." },
        { heading: "قائمة ZATCA (9 بنود)", body: "✓ تحديد إذا كنت ضمن نطاق Wave 24 (إيراد > 375K ريال). ✓ تسجيل في بوابة Fatoora. ✓ شهادة CSID رقمية. ✓ تكييف ERP لـ UBL 2.1 XML. ✓ اختبار Sandbox ناجح. ✓ QR Code معتمد على كل فاتورة. ✓ Clearance workflow جاهز للإنتاج. ✓ فريق يعرف العملية كاملاً. ✓ خطة Rollback في حالة خلل تقني." },
        { heading: "قائمة PDPL (7 بنود)", body: "✓ تحديد كل بيانات شخصية تعالجها. ✓ سياسة خصوصية محدّثة وموثّقة. ✓ عملية موافقة واضحة قبل جمع البيانات. ✓ نظام لتلبية طلبات الحذف خلال 30 يوماً. ✓ لا إرسال بيانات لطرف ثالث بدون موافقة. ✓ Audit log لكل معالجة بيانات. ✓ Soft deletes — لا حذف مادي للسجلات." },
        { heading: "قائمة AI Governance (6 بنود)", body: "✓ توثيق كل أداة AI مستخدمة في الشركة. ✓ تحديد من يوافق على مخرجات AI قبل الإجراء. ✓ لا قرار حرج بمخرج AI بدون مراجعة بشرية. ✓ Audit trail لكل إجراء مبني على AI. ✓ سياسة واضحة: أي بيانات يُدخَل في AI؟. ✓ مراجعة دورية لدقة النماذج." },
        { heading: "قائمة Revenue Ops (5 بنود)", body: "✓ كل lead له owner واضح خلال 15 دقيقة. ✓ Approval قبل أي إرسال تجاري. ✓ توثيق سبب كل صفقة خاسرة. ✓ متابعة مستحقات كل 30 يوماً. ✓ Proof Pack لكل قرار إيراد يُشارَك مع الإدارة." },
        { heading: "كيف تبدأ؟", body: "القائمة تبدو طويلة — لكن أولويتها واضحة: ZATCA أولاً (الموعد حرج)، ثم PDPL، ثم AI Governance. Dealix Sprint 7 أيام يُقيّم وضعك في كل محور ويعطيك قائمة أولويات محددة — لا توصيات عامة، بل أدلة موثّقة بمستوى L0-L5." },
      ],
      en: [
        { heading: "Why is 2026 a critical compliance year?", body: "Three regulatory requirements converge in 2026: ZATCA Wave 24 (June 2026), PDPL with its full executive regulations, and new regional AI Governance rules. Companies ignoring this convergence risk multiple simultaneous fines." },
        { heading: "ZATCA checklist (9 items)", body: "✓ Determine if you're in Wave 24 scope (revenue > 375K SAR). ✓ Register on Fatoora portal. ✓ Digital CSID certificate. ✓ Adapt ERP for UBL 2.1 XML. ✓ Successful Sandbox test. ✓ ZATCA-compliant QR Code on every invoice. ✓ Clearance workflow ready for production. ✓ Team trained on the full process. ✓ Rollback plan for technical failures." },
        { heading: "PDPL checklist (7 items)", body: "✓ Identify all personal data you process. ✓ Updated and documented privacy policy. ✓ Clear consent process before data collection. ✓ System to fulfill deletion requests within 30 days. ✓ No data sent to third parties without consent. ✓ Audit log for every data processing action. ✓ Soft deletes — no physical record deletion." },
        { heading: "AI Governance checklist (6 items)", body: "✓ Document every AI tool used in the company. ✓ Define who approves AI outputs before action. ✓ No critical decision from AI output without human review. ✓ Audit trail for every AI-based action. ✓ Clear policy: what data goes into AI?. ✓ Periodic review of model accuracy." },
        { heading: "Revenue Ops checklist (5 items)", body: "✓ Every lead has a clear owner within 15 minutes. ✓ Approval before any commercial send. ✓ Document reason for every lost deal. ✓ Follow up on receivables every 30 days. ✓ Proof Pack for every revenue decision shared with management." },
        { heading: "How to start?", body: "The list looks long — but the priority is clear: ZATCA first (critical deadline), then PDPL, then AI Governance. Dealix's 7-day Sprint assesses your position in each area and gives you a specific priority list — not general recommendations, but documented evidence at L0-L5 levels." },
      ],
    },
  },
];

export function getArticle(slug: string): LearnArticle | undefined {
  return LEARN_ARTICLES.find((a) => a.slug === slug);
}

export function allSlugs(): string[] {
  return LEARN_ARTICLES.map((a) => a.slug);
}
