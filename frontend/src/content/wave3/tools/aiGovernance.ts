import type { QuizToolDef } from "./types";

export const aiGovernance: QuizToolDef = {
  slug: "ai-governance",
  kind: "quiz",
  titleAr: "AI Governance Checklist",
  titleEn: "AI Governance Checklist",
  introAr:
    "قائمة فحص سريعة لجاهزية حوكمة الذكاء الاصطناعي: الموافقة البشرية، الخصوصية، والوضوح في ما لا يفعله النظام.",
  introEn:
    "A quick checklist for AI governance readiness: human approval, privacy, and clarity on what the system does NOT do.",
  questions: [
    {
      id: "approval",
      promptAr: "هل كل إجراء خارجي يتطلب موافقة بشرية صريحة؟",
      promptEn: "Does every external action require explicit human approval?",
      gapAr: "بعض الإجراءات الخارجية تتم بلا موافقة موثّقة.",
      gapEn: "Some external actions happen without documented approval.",
      options: [
        { labelAr: "نعم دائماً", labelEn: "Yes, always", weight: 1 },
        { labelAr: "أحياناً", labelEn: "Sometimes", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "privacy",
      promptAr: "هل بيانات العملاء محمية ولا تُستخدم لتدريب النماذج؟",
      promptEn: "Is customer data protected and never used to train models?",
      gapAr: "لا توجد سياسة واضحة لحماية بيانات العملاء.",
      gapEn: "No clear policy protecting customer data.",
      options: [
        { labelAr: "نعم، سياسة موثّقة", labelEn: "Yes, a documented policy", weight: 1 },
        { labelAr: "غير متأكد", labelEn: "Unsure", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "audit",
      promptAr: "هل تحتفظ بسجل تدقيق لما فعله الذكاء الاصطناعي؟",
      promptEn: "Do you keep an audit log of what the AI did?",
      gapAr: "لا يوجد سجل تدقيق لأفعال النظام.",
      gapEn: "No audit log of system actions.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "جزئياً", labelEn: "Partially", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "claims",
      promptAr: "هل لديك قائمة بالادعاءات الممنوعة (مثل وعود مضمونة)؟",
      promptEn: "Do you maintain a register of forbidden claims (e.g. guaranteed promises)?",
      gapAr: "لا يوجد سجل للادعاءات الممنوعة.",
      gapEn: "No register of forbidden claims.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "غير رسمي", labelEn: "Informal", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "boundaries",
      promptAr: "هل حدود النظام واضحة (ما لا يفعله) لفريقك وعملائك؟",
      promptEn: "Are the system's boundaries (what it does NOT do) clear to your team and clients?",
      gapAr: "حدود النظام غير موثّقة بوضوح.",
      gapEn: "System boundaries are not clearly documented.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "نوعاً ما", labelEn: "Somewhat", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
  ],
  recommended: {
    low: {
      osAr: "Governance OS عبر Command Sprint",
      osEn: "Governance OS via Command Sprint",
      nextStep: { labelAr: "ابدأ Command Sprint", labelEn: "Start Command Sprint", route: "command-sprint" },
    },
    med: {
      osAr: "تشخيص 7 أيام لسد فجوات الحوكمة",
      osEn: "7-day Diagnostic to close governance gaps",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
    high: {
      osAr: "تشخيص لتوثيق الحوكمة قبل التوسّع",
      osEn: "Diagnostic to document governance before scaling",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
  },
  disclaimer: "default",
};
