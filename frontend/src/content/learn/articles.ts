export type LearnSection = { heading: string; body: string };

export type LearnArticle = {
  slug: string;
  titleAr: string;
  titleEn: string;
  descriptionAr: string;
  descriptionEn: string;
  sections: { ar: LearnSection[]; en: LearnSection[] };
};

export const LEARN_ARTICLES: LearnArticle[] = [
  {
    slug: "post-lead-revenue-ops",
    titleAr: "ما هو Post-Lead Revenue Ops؟",
    titleEn: "What is Post-Lead Revenue Ops?",
    descriptionAr: "تشغيل ما يحدث بعد وصول الـ lead — مالك، دليل، موافقة، خطوة تالية.",
    descriptionEn: "Operating what happens after the lead — owner, proof, approval, next step.",
    sections: {
      ar: [
        {
          heading: "التعريف",
          body: "Post-Lead Revenue Ops هو تشغيل ما يحدث بعد وصول الـ lead: من يملك المتابعة؟ ما الدليل؟ ما الموافقة؟ Dealix لا يستبدل CRM — يثبت قرار إيراد موثّق.",
        },
        {
          heading: "متى تحتاجه",
          body: "الإعلانات تجيب leads لكن الإدارة تسأل ماذا حدث؟ لا owner واضح؟ follow-up غير موثّق؟ وكالة تحتاج Proof Pack لعميلها؟",
        },
        {
          heading: "خطوات SOAEN",
          body: "Source — Owner خلال 15 دقيقة — Approval قبل الإرسال — Evidence لكل رد — Next Action بتاريخ واحد.",
        },
      ],
      en: [
        {
          heading: "Definition",
          body: "Post-Lead Revenue Ops runs what happens after a lead arrives: who owns follow-up, what proof exists, what approval is required. Dealix does not replace your CRM — it documents revenue decisions.",
        },
        {
          heading: "When you need it",
          body: "Ads bring leads but leadership asks what happened next. No clear owner. Undocumented follow-up. An agency needs a Proof Pack for their client.",
        },
        {
          heading: "SOAEN steps",
          body: "Source — Owner within 15 minutes — Approval before external send — Evidence per reply — One next action with a date.",
        },
      ],
    },
  },
  {
    slug: "what-is-proof-pack",
    titleAr: "ما هو Proof Pack؟",
    titleEn: "What is a Proof Pack?",
    descriptionAr: "حزمة إثبات منظمة للوكالة أو العميل — أقسام وحالة واضحة.",
    descriptionEn: "A structured proof bundle for agency or client — clear sections and status.",
    sections: {
      ar: [
        {
          heading: "التعريف",
          body: "Proof Pack ليس تقريراً عاماً — هو أقسام (مصادر، أصحاب، أدلة، قرارات) كل قسم له حالة: مكتمل، بانتظار مدخلات، أو محظور.",
        },
        {
          heading: "لماذا للوكالات",
          body: "العميل يريد إثباتاً أسبوعياً بعد الحملة. Dealix يعطيك مسودة حوكَمة + عينة عامة قبل الشراء.",
        },
        {
          heading: "مستويات الأدلة",
          body: "L0–L5: من فرضية إلى إثبات قابل للتدقيق. لا upsell قبل L4.",
        },
      ],
      en: [
        {
          heading: "Definition",
          body: "A Proof Pack is not a generic PDF — it is sections (sources, owners, evidence, decisions) each with status: complete, pending inputs, or blocked.",
        },
        {
          heading: "Why agencies",
          body: "Clients want weekly proof after campaigns. Dealix gives governed drafts plus a public sample before purchase.",
        },
        {
          heading: "Evidence levels",
          body: "L0–L5: from hypothesis to auditable proof. No upsell before L4.",
        },
      ],
    },
  },
  {
    slug: "crm-vs-revenue-ops",
    titleAr: "CRM مقابل Revenue Ops — أين الفجوة؟",
    titleEn: "CRM vs Revenue Ops — where is the gap?",
    descriptionAr: "CRM يسجّل؛ Revenue Ops يثبت القرار بعد الـ lead.",
    descriptionEn: "CRM records; Revenue Ops proves the decision after the lead.",
    sections: {
      ar: [
        {
          heading: "CRM يفعل",
          body: "جهات اتصال، مراحل، مهام، تقارير خط أنابيب.",
        },
        {
          heading: "ما لا يفعل",
          body: "لا يفرض موافقة قبل واتساب. لا يربط كل لمسة بحدث دليل. لا يحدّ العروض على السطح.",
        },
        {
          heading: "دور Dealix",
          body: "طبقة حوكمة + أدلة + 3 عروض سطح — فوق CRM الحالي بدون استبداله.",
        },
      ],
      en: [
        {
          heading: "CRM does",
          body: "Contacts, stages, tasks, pipeline reports.",
        },
        {
          heading: "What it does not",
          body: "No approval gate before WhatsApp. No evidence event per touch. No surface-offer boundary.",
        },
        {
          heading: "Dealix role",
          body: "Governance + evidence + three surface offers — on top of your CRM, not replacing it.",
        },
      ],
    },
  },
  {
    slug: "no-cold-whatsapp-policy",
    titleAr: "لماذا لا واتساب بارد في Dealix؟",
    titleEn: "Why no cold WhatsApp in Dealix?",
    descriptionAr: "سياسة PDPL + ثقة السوق السعودي — مسودات وموافقة فقط.",
    descriptionEn: "PDPL + Saudi market trust — drafts and approval only.",
    sections: {
      ar: [
        {
          heading: "السياسة",
          body: "لا إرسال واتساب بارد آلي. لا LinkedIn DM آلي. كل إرسال خارجي يمر بموافقة بشرية.",
        },
        {
          heading: "البديل",
          body: "قوائم warm معتمدة، مسودات من آلة اليوم، 10 لمسات يدوية مسجّلة في Evidence.",
        },
        {
          heading: "النتيجة",
          body: "ثقة أعلى، مخاطر امتثال أقل، Proof حقيقي لا أرقام مخترعة.",
        },
      ],
      en: [
        {
          heading: "Policy",
          body: "No automated cold WhatsApp. No automated LinkedIn DMs. Every external send requires human approval.",
        },
        {
          heading: "Alternative",
          body: "Approved warm lists, daily draft machine, 10 manual touches logged as Evidence events.",
        },
        {
          heading: "Outcome",
          body: "Higher trust, lower compliance risk, real proof not invented metrics.",
        },
      ],
    },
  },
  {
    slug: "10-lead-audit",
    titleAr: "10-Lead Audit — متى تطلبه؟",
    titleEn: "10-Lead Audit — when to request it?",
    descriptionAr: "مراجعة 10 leads مع توصية حوكمة — عرض سطح للوكالات.",
    descriptionEn: "Review 10 leads with governance recommendation — surface offer for agencies.",
    sections: {
      ar: [
        {
          heading: "المدخلات",
          body: "قائمة leads حقيقية (تصدير CRM أو جدول) — بدون scraping.",
        },
        {
          heading: "المخرجات",
          body: "مالك لكل lead، فجوات أدلة، مسودة Proof، خطوة تالية واحدة.",
        },
        {
          heading: "الخطوة التالية",
          body: "Agency Proof Pack أو Governed Diagnostic حسب الجاهزية.",
        },
      ],
      en: [
        {
          heading: "Inputs",
          body: "A real lead list (CRM export or sheet) — no scraping.",
        },
        {
          heading: "Outputs",
          body: "Owner per lead, evidence gaps, Proof draft, one next action.",
        },
        {
          heading: "Next step",
          body: "Agency Proof Pack or Governed Diagnostic based on readiness.",
        },
      ],
    },
  },
  {
    slug: "audit-lead-follow-up",
    titleAr: "متابعة الـ lead بعد التدقيق",
    titleEn: "Lead follow-up after audit",
    descriptionAr: "من التشخيص إلى الاجتماع — بدون تسريب.",
    descriptionEn: "From diagnostic to meeting — without leakage.",
    sections: {
      ar: [
        {
          heading: "خلال 24 ساعة",
          body: "تأكيد المالك، مسودة رسالة واحدة، موافقة، إرسال يدوي، سجل Evidence.",
        },
        {
          heading: "خلال 7 أيام",
          body: "إما اجتماع أو Proof Pack عينة أو closed_lost مع سبب.",
        },
        {
          heading: "حوكمة",
          body: "لا أكثر من 3 عروض على السطح في أي محادثة.",
        },
      ],
      en: [
        {
          heading: "Within 24 hours",
          body: "Confirm owner, one draft message, approval, manual send, Evidence log.",
        },
        {
          heading: "Within 7 days",
          body: "Meeting booked, sample Proof Pack, or closed_lost with reason.",
        },
        {
          heading: "Governance",
          body: "No more than three surface offers in any conversation.",
        },
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
