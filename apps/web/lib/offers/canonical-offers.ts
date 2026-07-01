// Canonical Dealix offer ladder — the single source of truth for every
// pricing/offer surface (web pages, PREMIUM_OFFERS derivations, exports).
// Mirrors docs/DEALIX_BUSINESS_MODEL.md and CLAUDE.md "Business Model Summary".
// Do not fork this ladder into page-local arrays — import from here.

export type OfferId =
  | "free_diagnostic"
  | "micro_sprint"
  | "data_pack"
  | "managed_ops"
  | "transformation_sprint"
  | "custom_enterprise";

export type OfferBilling = "free" | "one_time" | "monthly";

export interface CanonicalOffer {
  tier: 1 | 2 | 3 | 4 | 5 | 6;
  id: OfferId;
  name: string;
  nameAr: string;
  price: string;
  priceEn: string;
  billing: OfferBilling;
  duration: string;
  badge: string;
  badgeColor: string;
  highlight: boolean;
  description: string;
  outputs: string[];
  bestFor: string[];
  cta: string;
  ctaHref: string;
  ctaStyle: string;
  waMessage: string;
}

export const CANONICAL_OFFERS: CanonicalOffer[] = [
  {
    tier: 1,
    id: "free_diagnostic",
    name: "Free Diagnostic",
    nameAr: "التشخيص المجاني",
    price: "مجاني",
    priceEn: "Free",
    billing: "free",
    duration: "30 دقيقة",
    badge: "نقطة البداية",
    badgeColor: "border-slate-400/40 text-slate-300",
    highlight: false,
    description:
      "محادثة سريعة نحدد فيها أين تضيع الفرص في شركتك وما أول خطوة منطقية.",
    outputs: [
      "تحديد 3 نقاط تسرب رئيسية",
      "توصية بأول نظام مناسب",
      "وضوح هل Diagnostic Sprint مناسب أم لا",
    ],
    bestFor: ["first-touch", "warm-lead", "inbound"],
    cta: "احجز محادثة مجانية",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-white/20 hover:bg-white/10",
    waMessage: "السلام عليكم، أريد حجز التشخيص المجاني (30 دقيقة) من Dealix.",
  },
  {
    tier: 2,
    id: "micro_sprint",
    name: "Micro Sprint",
    nameAr: "سبرنت سريع",
    price: "499 ريال",
    priceEn: "SAR 499",
    billing: "one_time",
    duration: "1–2 يوم",
    badge: "إثبات الكفاءة",
    badgeColor: "border-blue-400/40 text-blue-300",
    highlight: false,
    description:
      "نثبت قدرتنا بحل واحد سريع وملموس. مخرج حقيقي في يومين بسعر منخفض.",
    outputs: [
      "حل تشغيلي واحد مُنجز",
      "توثيق الحل وطريقة الاستخدام",
      "تقرير مبدئي بفرص إضافية",
    ],
    bestFor: ["quick-proof", "small-budget", "first-paid-step"],
    cta: "ابدأ Micro Sprint",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-blue-400/40 text-blue-200 hover:bg-blue-400/10",
    waMessage: "السلام عليكم، أريد البدء بـ Micro Sprint (499 ريال) من Dealix.",
  },
  {
    tier: 3,
    id: "data_pack",
    name: "Data Intelligence Pack",
    nameAr: "حزمة بيانات",
    price: "1,500 ريال",
    priceEn: "SAR 1,500",
    billing: "one_time",
    duration: "2–3 أيام",
    badge: "أصل بيانات",
    badgeColor: "border-purple-400/40 text-purple-300",
    highlight: false,
    description: "نبني لك قاعدة بيانات عملاء مؤهلة، مصنفة، وجاهزة للتواصل.",
    outputs: [
      "قاعدة بيانات عملاء محتملين (100+ سجل)",
      "تصنيف حسب القطاع والأولوية",
      "تقرير جودة البيانات",
      "خريطة التواصل الأولى",
    ],
    bestFor: ["outbound-prep", "sales-team", "new-market"],
    cta: "احصل على حزمة البيانات",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-purple-400/40 text-purple-200 hover:bg-purple-400/10",
    waMessage: "السلام عليكم، أريد طلب حزمة البيانات (1,500 ريال) من Dealix.",
  },
  {
    tier: 4,
    id: "managed_ops",
    name: "Managed AI Operations",
    nameAr: "تشغيل AI شهري",
    price: "2,999–4,999 ريال/شهر",
    priceEn: "SAR 2,999–4,999/mo",
    billing: "monthly",
    duration: "شهري مستمر",
    badge: "علاقة مستمرة",
    badgeColor: "border-amber-400/40 text-amber-300",
    highlight: false,
    description:
      "نشغّل نظام AI يومياً ونسلمك تقرير أسبوعي بالنتائج والتوصيات.",
    outputs: [
      "تقرير أسبوعي بالأداء والتوصيات",
      "تحديثات مستمرة على النظام",
      "دعم واتساب مباشر",
      "مراجعة شهرية مع المؤسس",
    ],
    bestFor: ["existing-client", "ongoing-partner", "no-internal-team"],
    cta: "ابدأ الإدارة الشهرية",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-amber-400/40 text-amber-200 hover:bg-amber-400/10",
    waMessage:
      "السلام عليكم، أريد الاستفسار عن التشغيل الشهري Managed AI Operations من Dealix.",
  },
  {
    tier: 5,
    id: "transformation_sprint",
    name: "Transformation Diagnostic Sprint",
    nameAr: "تشخيص تحولي مدفوع",
    price: "7,500–25,000 ريال",
    priceEn: "SAR 7,500–25,000",
    billing: "one_time",
    duration: "3–7 أيام",
    badge: "نقطة الدخول الرئيسية",
    badgeColor: "border-cyan-300/60 text-cyan-200",
    highlight: true,
    description:
      "نكتشف أين يتسرب إيرادك ونبني لك خارطة الحل قبل أي التزام كبير.",
    outputs: [
      "Workflow Map — خريطة العمليات الحالية",
      "Leakage Map — أين يتسرب الإيراد وكم يكلف",
      "KPI Model — الأرقام التي يجب متابعتها",
      "First System Recommendation — أول نظام يستحق البناء",
      "Implementation Quote — السعر والجدول الزمني",
      "14-Day Pilot Plan — كيف تبدأ خلال أسبوعين",
    ],
    bestFor: ["founder-led", "b2b_services", "primary-entry"],
    cta: "ابدأ التشخيص الآن",
    ctaHref: "/ar/diagnostic-sprint",
    ctaStyle: "bg-cyan-400 text-[#06111f] hover:bg-cyan-300 font-black",
    waMessage:
      "السلام عليكم، أريد البدء بالتشخيص التحولي المدفوع (Transformation Diagnostic Sprint) من Dealix.",
  },
  {
    tier: 6,
    id: "custom_enterprise",
    name: "Custom Enterprise System",
    nameAr: "نظام مؤسسي مخصص",
    price: "25,000–100,000+ ريال",
    priceEn: "SAR 25,000–100,000+",
    billing: "one_time",
    duration: "4–12 أسبوع",
    badge: "للمؤسسات",
    badgeColor: "border-rose-400/40 text-rose-300",
    highlight: false,
    description:
      "نظام AI مبني خصيصاً لعمليات شركتك، مدمج مع فريقك وأدواتك الحالية.",
    outputs: [
      "تحليل العمليات الكامل",
      "تصميم النظام المخصص",
      "بناء وتكامل كامل",
      "تدريب الفريق",
      "دعم 90 يوم بعد الإطلاق",
      "توثيق كامل وتسليم الملكية",
    ],
    bestFor: ["50+ employees", "group", "regulated"],
    cta: "ناقش مشروعك",
    ctaHref: "/ar/intake",
    ctaStyle: "border border-rose-400/40 text-rose-200 hover:bg-rose-400/10",
    waMessage:
      "السلام عليكم، أريد مناقشة نظام مؤسسي مخصص (Custom Enterprise System) مع Dealix.",
  },
];

export const PRIMARY_OFFER: CanonicalOffer = CANONICAL_OFFERS.find(
  (o) => o.tier === 5,
)!;

// Rules-endorsed auxiliary framings (.claude/rules/dealix-commercial-os.md):
// a beta-priced entry into rung 5 and the retainer extension of rung 4.
export const BETA_SPRINT = {
  nameAr: "سبرينت غرفة قيادة الإيراد — 7 أيام",
  name: "7-Day Revenue Command Room Sprint (beta)",
  price: "5,000–12,000 ريال",
  priceEn: "SAR 5,000–12,000",
  tierRef: 5 as const,
};

export const RETAINER_PATH = {
  nameAr: "مسار التشغيل الشهري الموسع",
  name: "Extended retainer path",
  price: "3,000–15,000 ريال/شهر",
  priceEn: "SAR 3,000–15,000/mo",
  tierRef: 4 as const,
};
