import type { QuizToolDef } from "./types";

export const proofGapAudit: QuizToolDef = {
  slug: "proof-gap-audit",
  kind: "quiz",
  titleAr: "Proof Gap Audit",
  titleEn: "Proof Gap Audit",
  introAr:
    "قِس قدرتك على إثبات ما يحدث بعد وصول الفرصة: المصدر، المالك، الدليل، والموافقة قبل أي إرسال خارجي.",
  introEn:
    "Measure your ability to prove what happens after a lead arrives: source, owner, evidence, and approval before any external send.",
  questions: [
    {
      id: "source",
      promptAr: "هل تعرف مصدر كل فرصة وجودته؟",
      promptEn: "Do you know each opportunity's source and its quality?",
      gapAr: "مصادر الفرص غير موثّقة أو غير مصنّفة.",
      gapEn: "Lead sources are undocumented or unclassified.",
      options: [
        { labelAr: "نعم لكل فرصة", labelEn: "Yes for every opportunity", weight: 1 },
        { labelAr: "للبعض", labelEn: "For some", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "evidence",
      promptAr: "هل يوجد سجل دليل لكل محادثة أو قرار؟",
      promptEn: "Is there an evidence log for each conversation or decision?",
      gapAr: "لا يوجد سجل دليل لكل لمسة.",
      gapEn: "No evidence log per touch.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "جزئياً", labelEn: "Partially", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "approval",
      promptAr: "هل كل إرسال خارجي يمرّ بموافقة بشرية موثّقة؟",
      promptEn: "Does every external send pass documented human approval?",
      gapAr: "الإرسال الخارجي بلا سجل موافقة.",
      gapEn: "External sends lack an approval record.",
      options: [
        { labelAr: "نعم دائماً", labelEn: "Yes, always", weight: 1 },
        { labelAr: "أحياناً", labelEn: "Sometimes", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "shareable",
      promptAr: "هل تستطيع تسليم حزمة إثبات منظمة لعميل أو إدارة خلال يوم؟",
      promptEn: "Can you hand a structured proof bundle to a client or leadership within a day?",
      gapAr: "لا يمكن تجميع Proof Pack بسرعة.",
      gapEn: "A Proof Pack cannot be assembled quickly.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "بصعوبة", labelEn: "With difficulty", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
    {
      id: "levels",
      promptAr: "هل تميّز بين الفرضية والدليل المُثبَت قبل التوسّع؟",
      promptEn: "Do you distinguish a hypothesis from proven evidence before scaling?",
      gapAr: "لا تمييز واضح بين الفرضية والإثبات.",
      gapEn: "No clear line between hypothesis and proof.",
      options: [
        { labelAr: "نعم", labelEn: "Yes", weight: 1 },
        { labelAr: "نوعاً ما", labelEn: "Somewhat", weight: 0.5 },
        { labelAr: "لا", labelEn: "No", weight: 0 },
      ],
    },
  ],
  recommended: {
    low: {
      osAr: "Proof OS عبر Command Sprint",
      osEn: "Proof OS via Command Sprint",
      nextStep: { labelAr: "ابدأ Command Sprint", labelEn: "Start Command Sprint", route: "command-sprint" },
    },
    med: {
      osAr: "تشخيص 7 أيام لبناء سجل الإثبات",
      osEn: "7-day Diagnostic to build the proof register",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
    high: {
      osAr: "تشخيص لتثبيت الإثبات قبل التوسّع",
      osEn: "Diagnostic to lock proof before scaling",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
  },
  disclaimer: "default",
};
