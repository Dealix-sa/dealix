import type { QuizToolDef } from "./types";

export const businessOsScore: QuizToolDef = {
  slug: "business-os-score",
  kind: "quiz",
  titleAr: "Business OS Score",
  titleEn: "Business OS Score",
  introAr:
    "خمسة أسئلة سريعة تقيس مدى وضوح تشغيل أعمالك: الفرص، المتابعة، العروض، الإثبات، والقرار التنفيذي القادم.",
  introEn:
    "Five quick questions measuring how clearly your business runs: opportunities, follow-up, offers, proof, and the next executive decision.",
  questions: [
    {
      id: "opportunities",
      promptAr: "هل تعرف بدقة أين تتعطل فرصك الحالية؟",
      promptEn: "Do you know exactly where your current opportunities stall?",
      gapAr: "لا توجد صورة واضحة لمكان تعطل الفرص.",
      gapEn: "No clear picture of where opportunities stall.",
      options: [
        { labelAr: "نعم، لكل فرصة حالة واضحة", labelEn: "Yes, every opportunity has a clear stage", weight: 1 },
        { labelAr: "جزئياً", labelEn: "Partially", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "followup",
      promptAr: "هل المتابعة موثّقة ولها مالك ومسؤول؟",
      promptEn: "Is follow-up documented with a clear owner?",
      gapAr: "المتابعة غير موثّقة أو بلا مالك واضح.",
      gapEn: "Follow-up is undocumented or has no clear owner.",
      options: [
        { labelAr: "نعم دائماً", labelEn: "Yes, always", weight: 1 },
        { labelAr: "أحياناً", labelEn: "Sometimes", weight: 0.5 },
        { labelAr: "نادراً", labelEn: "Rarely", weight: 0 },
      ],
    },
    {
      id: "offers",
      promptAr: "هل عروضك واضحة وجاهزة للإرسال بسرعة؟",
      promptEn: "Are your offers clear and ready to send quickly?",
      gapAr: "العروض تأخذ وقتاً طويلاً أو غير موحّدة.",
      gapEn: "Offers take too long or are inconsistent.",
      options: [
        { labelAr: "نعم، قالب جاهز", labelEn: "Yes, a ready template", weight: 1 },
        { labelAr: "نبنيها كل مرة", labelEn: "We rebuild each time", weight: 0.5 },
        { labelAr: "غير منظمة", labelEn: "Unstructured", weight: 0 },
      ],
    },
    {
      id: "proof",
      promptAr: "هل لديك سجل إثبات يربط كل قرار بدليله؟",
      promptEn: "Do you have a proof register linking each decision to its evidence?",
      gapAr: "لا يوجد سجل إثبات قابل للتدقيق.",
      gapEn: "No auditable proof register.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "جزئياً", labelEn: "Partially", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "decision",
      promptAr: "هل تعرف ما القرار التنفيذي القادم لكل ملف مهم؟",
      promptEn: "Do you know the next executive decision for each key file?",
      gapAr: "القرار التنفيذي القادم غير واضح.",
      gapEn: "The next executive decision is unclear.",
      options: [
        { labelAr: "نعم، لوحة قرارات واضحة", labelEn: "Yes, a clear decision board", weight: 1 },
        { labelAr: "في رأسي فقط", labelEn: "Only in my head", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
  ],
  recommended: {
    low: {
      osAr: "Command Sprint (نبدأ من الأساس)",
      osEn: "Command Sprint (start from the foundation)",
      nextStep: { labelAr: "ابدأ Command Sprint", labelEn: "Start Command Sprint", route: "command-sprint" },
    },
    med: {
      osAr: "تشخيص 7 أيام لسد الفجوات",
      osEn: "7-day Diagnostic to close the gaps",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
    high: {
      osAr: "تشخيص لتأكيد القيمة قبل التوسّع",
      osEn: "Diagnostic to confirm value before scaling",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
  },
  disclaimer: "default",
};
