import type { LeakageToolDef } from "./types";

export const revenueLeakage: LeakageToolDef = {
  slug: "revenue-leakage",
  kind: "leakage",
  titleAr: "Revenue Leakage Calculator",
  titleEn: "Revenue Leakage Calculator",
  introAr:
    "تقدير تعليمي للقيمة المعرّضة للخطر بسبب الفرص التي تمر بلا متابعة موثّقة. الأرقام استرشادية وليست ضماناً.",
  introEn:
    "An educational estimate of value at risk from opportunities that pass without documented follow-up. Numbers are indicative, not a guarantee.",
  recommended: {
    low: {
      osAr: "Revenue OS عبر Command Sprint",
      osEn: "Revenue OS via Command Sprint",
      nextStep: { labelAr: "ابدأ Command Sprint", labelEn: "Start Command Sprint", route: "command-sprint" },
    },
    med: {
      osAr: "تشخيص 7 أيام لرسم خريطة الإيراد",
      osEn: "7-day Diagnostic to map revenue",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
    high: {
      osAr: "تشخيص لتأكيد القيمة قبل التوسّع",
      osEn: "Diagnostic to confirm value before scaling",
      nextStep: { labelAr: "احجز تشخيصاً", labelEn: "Book Diagnostic", route: "diagnostic" },
    },
  },
  disclaimer: "educational",
};
