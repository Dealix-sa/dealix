import type { CtaRoute } from "@/lib/wave3/scoring";

export type AnswerSection = { heading: string; body: string };

export type Answer = {
  slug: string;
  questionAr: string;
  questionEn: string;
  descAr: string;
  descEn: string;
  sections: { ar: AnswerSection[]; en: AnswerSection[] };
  routeTo: CtaRoute;
};

export const ANSWERS: Answer[] = [
  {
    slug: "what-is-ai-business-operating-system",
    questionAr: "ما هو نظام تشغيل الأعمال بالذكاء الاصطناعي؟",
    questionEn: "What is an AI Business Operating System?",
    descAr: "تعريف بسيط لنظام تشغيل الأعمال بالذكاء الاصطناعي ولماذا يختلف عن الأدوات العامة.",
    descEn: "A simple definition of an AI Business Operating System and why it differs from generic tools.",
    sections: {
      ar: [
        { heading: "التعريف", body: "نظام تشغيل أعمال بالذكاء الاصطناعي يوضّح الفرص والمتابعة والعروض والإثبات والقرار التنفيذي القادم — تحت حوكمة وبموافقة بشرية." },
        { heading: "الفرق", body: "ليس أداة واحدة، بل طبقات تشغيل: Revenue, Proof, Governance, Delivery, Market Intelligence. دييلكس يبدأ من Command Sprint." },
      ],
      en: [
        { heading: "Definition", body: "An AI Business Operating System clarifies opportunities, follow-up, offers, proof, and the next executive decision — under governance, with human approval." },
        { heading: "The difference", body: "Not one tool but operating layers: Revenue, Proof, Governance, Delivery, Market Intelligence. Dealix starts with the Command Sprint." },
      ],
    },
    routeTo: "business-os-score",
  },
  {
    slug: "crm-vs-business-os",
    questionAr: "ما الفرق بين CRM ونظام تشغيل الأعمال؟",
    questionEn: "CRM vs Business OS — what's the difference?",
    descAr: "لماذا دييلكس ليس CRM ولا بديلاً عنه.",
    descEn: "Why Dealix is not a CRM and not a replacement for one.",
    sections: {
      ar: [
        { heading: "CRM يسجّل", body: "الـ CRM مكان لتخزين بيانات العملاء والفرص." },
        { heading: "Business OS يثبت ويقرّر", body: "دييلكس يحوّل ما بداخل أدواتك إلى صورة قرار: أين تتعطل الفرص، ما الدليل، ما الخطوة التالية." },
      ],
      en: [
        { heading: "A CRM records", body: "A CRM stores customer and opportunity data." },
        { heading: "A Business OS proves and decides", body: "Dealix turns what's inside your tools into a decision picture: where opportunities stall, what proof exists, what's next." },
      ],
    },
    routeTo: "business-os-score",
  },
  {
    slug: "what-is-command-sprint",
    questionAr: "ما هو Command Sprint؟",
    questionEn: "What is a Command Sprint?",
    descAr: "تجربة 7 أيام ثابتة النطاق تنتج Proof Pack.",
    descEn: "A 7-day fixed-scope engagement that produces a Proof Pack.",
    sections: {
      ar: [
        { heading: "النطاق", body: "7 أيام ثابتة النطاق: Revenue Map, Proof Register, Approval Register, Next Action Board, Executive Command Brief." },
        { heading: "الوعد", body: "وضوح وصورة قابلة للمراجعة — لا وعد بنتيجة مالية." },
      ],
      en: [
        { heading: "Scope", body: "A 7-day fixed scope: Revenue Map, Proof Register, Approval Register, Next Action Board, Executive Command Brief." },
        { heading: "The promise", body: "Clarity and a review-ready picture — not a financial-result promise." },
      ],
    },
    routeTo: "command-sprint",
  },
  {
    slug: "what-is-proof-register",
    questionAr: "ما هو سجل الإثبات (Proof Register)؟",
    questionEn: "What is a Proof Register?",
    descAr: "سجل يربط كل قرار بدليله القابل للتدقيق.",
    descEn: "A register linking each decision to its auditable evidence.",
    sections: {
      ar: [
        { heading: "الفكرة", body: "كل صف يربط فرصة أو قراراً بمصدره ودليله: مكتمل، بانتظار مدخلات، أو محظور." },
        { heading: "لماذا يهم", body: "يمنع التوسّع قبل الإثبات ويعطي الإدارة صورة موثوقة." },
      ],
      en: [
        { heading: "The idea", body: "Each row links an opportunity or decision to its source and evidence: complete, pending inputs, or blocked." },
        { heading: "Why it matters", body: "It prevents scaling before proof and gives leadership a trustworthy picture." },
      ],
    },
    routeTo: "diagnostic",
  },
  {
    slug: "what-is-approval-first-ai",
    questionAr: "ما معنى الذكاء الاصطناعي بالموافقة أولاً؟",
    questionEn: "What is approval-first AI?",
    descAr: "كل إجراء خارجي يتطلب موافقة بشرية موثّقة.",
    descEn: "Every external action requires documented human approval.",
    sections: {
      ar: [
        { heading: "المبدأ", body: "دييلكس يجهّز مسودات قابلة للمراجعة، ولا يرسل أي شيء خارجي تلقائياً." },
        { heading: "الأثر", body: "أمان وامتثال: لا إرسال تلقائي، لا واتساب بارد، لا scraping." },
      ],
      en: [
        { heading: "The principle", body: "Dealix prepares review-ready drafts and never sends anything external automatically." },
        { heading: "The effect", body: "Safety and compliance: no auto-send, no cold WhatsApp, no scraping." },
      ],
    },
    routeTo: "diagnostic",
  },
  {
    slug: "revenue-leakage",
    questionAr: "ما هو تسرّب الإيراد (Revenue Leakage)؟",
    questionEn: "What is revenue leakage?",
    descAr: "القيمة المعرّضة للخطر بسبب الفرص التي تمر بلا متابعة موثّقة.",
    descEn: "Value at risk from opportunities passing without documented follow-up.",
    sections: {
      ar: [
        { heading: "أين يحدث", body: "بين وصول الفرصة وأول رد، وبين الرد والخطوة التالية." },
        { heading: "كيف تقيسه", body: "ابدأ بحاسبة استرشادية ثم رتّب فرصك في Command Sprint." },
      ],
      en: [
        { heading: "Where it happens", body: "Between a lead's arrival and first reply, and between the reply and the next step." },
        { heading: "How to measure", body: "Start with an indicative calculator, then organize your opportunities in a Command Sprint." },
      ],
    },
    routeTo: "business-os-score",
  },
  {
    slug: "proof-gap",
    questionAr: "ما هي فجوة الإثبات (Proof Gap)؟",
    questionEn: "What is a proof gap?",
    descAr: "عدم القدرة على إثبات ما حدث بعد وصول الفرصة.",
    descEn: "The inability to prove what happened after a lead arrived.",
    sections: {
      ar: [
        { heading: "العلامات", body: "لا سجل دليل، لا مالك واضح، لا موافقة موثّقة قبل الإرسال." },
        { heading: "الحل", body: "Proof OS عبر Command Sprint يبني سجل إثبات قابل للتدقيق." },
      ],
      en: [
        { heading: "Signs", body: "No evidence log, no clear owner, no documented approval before sending." },
        { heading: "The fix", body: "Proof OS via a Command Sprint builds an auditable proof register." },
      ],
    },
    routeTo: "business-os-score",
  },
  {
    slug: "whatsapp-sales-followup",
    questionAr: "كيف ننظّم متابعة المبيعات عبر واتساب بأمان؟",
    questionEn: "How to organize WhatsApp sales follow-up safely?",
    descAr: "متابعة منظمة بموافقة بشرية — بلا واتساب بارد أو إرسال تلقائي.",
    descEn: "Organized follow-up with human approval — no cold WhatsApp, no auto-send.",
    sections: {
      ar: [
        { heading: "القاعدة", body: "دييلكس يجهّز مسودات الرد، وأنت ترسلها يدوياً بعد المراجعة عبر قناة وافق عليها العميل." },
        { heading: "ما لا نفعله", body: "لا رسائل واتساب باردة، ولا إرسال تلقائي، ولا قوائم مشتراة." },
      ],
      en: [
        { heading: "The rule", body: "Dealix prepares reply drafts; you send them manually after review through a channel the customer opted into." },
        { heading: "What we don't do", body: "No cold WhatsApp, no auto-send, no purchased lists." },
      ],
    },
    routeTo: "diagnostic",
  },
  {
    slug: "client-memory",
    questionAr: "ما هي ذاكرة العميل (Client Memory)؟",
    questionEn: "What is client memory?",
    descAr: "صورة موحّدة لكل ما يخص العميل تساعد على القرار التالي.",
    descEn: "A unified picture of everything about a client to support the next decision.",
    sections: {
      ar: [
        { heading: "الفكرة", body: "بدل تشتت المعلومات، صورة واحدة: المصدر، التاريخ، الدليل، الخطوة التالية." },
        { heading: "الأثر", body: "قرارات أسرع وأوضح بموافقة بشرية." },
      ],
      en: [
        { heading: "The idea", body: "Instead of scattered information, one picture: source, history, evidence, next step." },
        { heading: "The effect", body: "Faster, clearer decisions with human approval." },
      ],
    },
    routeTo: "diagnostic",
  },
  {
    slug: "delivery-visibility",
    questionAr: "ما هي وضوح التسليم (Delivery Visibility)؟",
    questionEn: "What is delivery visibility?",
    descAr: "معرفة ما تم تسليمه فعلاً مقابل ما لا يزال قيد العمل.",
    descEn: "Knowing what was actually delivered vs what's still in progress.",
    sections: {
      ar: [
        { heading: "الفكرة", body: "سجل تسليم يومي خلال 7 أيام يوضّح ما تم فعلاً — بلا وعود بما لم يُسلَّم." },
        { heading: "الأثر", body: "ثقة العميل وصورة تنفيذية واضحة." },
      ],
      en: [
        { heading: "The idea", body: "A daily 7-day delivery log shows what was actually delivered — no promises for what isn't done." },
        { heading: "The effect", body: "Client trust and a clear executive picture." },
      ],
    },
    routeTo: "command-sprint",
  },
];

export function answerSlugs(): string[] {
  return ANSWERS.map((a) => a.slug);
}

export function getAnswer(slug: string): Answer | undefined {
  return ANSWERS.find((a) => a.slug === slug);
}
