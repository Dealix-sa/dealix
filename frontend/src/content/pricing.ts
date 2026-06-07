/**
 * Canonical Dealix pricing ladder for the public website.
 *
 * SINGLE SOURCE OF TRUTH for the frontend. Mirrors the backend registry
 * `auto_client_acquisition/service_catalog/registry.py` (OFFERINGS) — the same
 * IDs are accepted by `POST /api/v1/checkout`. If you change a price here,
 * change it in registry.py too (and vice-versa). The `usePlanPrices` hook can
 * additionally reconcile prices at runtime from `GET /api/v1/pricing/plans`.
 *
 * Doctrine: KPI lines are commitments ("we work for free until…"), never
 * guarantees. No invented numbers.
 */

export type PricePeriod = "free" | "one_time" | "monthly" | "custom";

/** What the primary CTA on a tier does. */
export type TierCtaKind = "checkout" | "diagnostic" | "custom" | "contact";

export interface PricingTier {
  /** Canonical registry id — passed to /api/v1/checkout as `plan`. */
  id: string;
  slug: string;
  nameAr: string;
  nameEn: string;
  /** SAR. 0 means free or custom (see `period`). */
  priceSar: number;
  period: PricePeriod;
  taglineAr: string;
  taglineEn: string;
  deliverablesAr: string[];
  deliverablesEn: string[];
  /** Commitment language (never a guarantee). */
  kpiAr: string;
  kpiEn: string;
  ctaKind: TierCtaKind;
  featured?: boolean;
}

export const PRICING_TIERS: PricingTier[] = [
  {
    id: "free_mini_diagnostic",
    slug: "free-diagnostic",
    nameAr: "التشخيص المجاني المختصر",
    nameEn: "Free Mini Diagnostic",
    priceSar: 0,
    period: "free",
    taglineAr: "ابدأ هنا — تحليل مطابقة القطاع و٣ فرص مرتّبة خلال ٢٤ ساعة.",
    taglineEn: "Start here — sector-fit analysis and 3 ranked opportunities within 24h.",
    deliverablesAr: [
      "تحليل مطابقة القطاع (صفحة واحدة)",
      "٣ فرص مرتّبة بالأولوية",
      "مسودة رسالة عربية واحدة",
      "توصية بأفضل قناة + خطوة تالية",
    ],
    deliverablesEn: [
      "1-page sector-fit analysis",
      "3 ranked opportunities",
      "1 Arabic message draft",
      "Best-channel recommendation + next step",
    ],
    kpiAr: "نسلّم خلال ٢٤ ساعة من تعبئة النموذج.",
    kpiEn: "Delivered within 24 hours of form submission.",
    ctaKind: "diagnostic",
  },
  {
    id: "revenue_proof_sprint_499",
    slug: "revenue-proof-sprint",
    nameAr: "سبرنت إثبات الإيرادات",
    nameEn: "Revenue Proof Sprint",
    priceSar: 499,
    period: "one_time",
    taglineAr: "٧ مخرجات في ٧ أيام — ينتهي بـ Proof Pack موقّع.",
    taglineEn: "7 deliverables in 7 days — ends with a signed Proof Pack.",
    deliverablesAr: [
      "أفضل ١٠ فرص مرتّبة",
      "Decision Passport لأعلى ٣",
      "حزمة مسودّات عربية (٥ رسائل)",
      "خطة متابعة ٧ أيام",
      "Proof Pack + توصية العرض التالي",
    ],
    deliverablesEn: [
      "Top 10 ranked opportunities",
      "Decision Passports for top 3",
      "Arabic draft pack (5 messages)",
      "7-day follow-up plan",
      "Proof Pack + next-offer recommendation",
    ],
    kpiAr: "إذا لم نصل إلى ≥١٠ فرص، نشتغل بدون مقابل حتى نوصل.",
    kpiEn: "If we don't surface ≥10 opportunities, we work for free until we do.",
    ctaKind: "checkout",
    featured: true,
  },
  {
    id: "data_to_revenue_pack_1500",
    slug: "data-to-revenue-pack",
    nameAr: "حزمة من البيانات إلى الإيراد",
    nameEn: "Data-to-Revenue Pack",
    priceSar: 1500,
    period: "one_time",
    taglineAr: "نظّف بياناتك وحوّلها إلى ٢٠ فرصة معتمدة خلال ١٤ يوماً.",
    taglineEn: "Clean your data into 20 approved opportunities in 14 days.",
    deliverablesAr: [
      "لوحة Leads نظيفة (بلا تكرار)",
      "تقرير تحقّق المصدر + تقرير المخاطر",
      "أفضل ٢٠ فرصة مُقيّمة",
      "١٠ مسودّات عربية + خطة متابعة",
    ],
    deliverablesEn: [
      "Clean, deduplicated lead board",
      "Source-validation + risk report",
      "Top 20 scored opportunities",
      "10 Arabic drafts + follow-up plan",
    ],
    kpiAr: "تنظيف ٤٠٠+ سطر في ١٤ يوماً. إن لم نصل لـ٢٠ فرصة، نواصل حتى نوصل.",
    kpiEn: "Clean 400+ rows in 14 days. If we don't surface 20 opportunities, we work until we do.",
    ctaKind: "checkout",
  },
  {
    id: "growth_ops_monthly_2999",
    slug: "growth-ops-monthly",
    nameAr: "عمليات النمو الشهرية",
    nameEn: "Growth Ops Monthly",
    priceSar: 2999,
    period: "monthly",
    taglineAr: "تشغيل إيراد محكوم شهرياً — تدقيق أسبوعي وProof Pack شهري.",
    taglineEn: "Monthly governed revenue ops — weekly audits, monthly Proof Pack.",
    deliverablesAr: [
      "٤ تدقيقات أسبوعية للأنبوب",
      "طابور موافقات يومي",
      "≥٢٠ مسودة رسالة شهرياً",
      "Proof Pack + ملخّص تنفيذي شهري",
    ],
    deliverablesEn: [
      "4 weekly pipeline audits",
      "Daily approval queue",
      "≥20 message drafts / month",
      "Monthly Proof Pack + executive summary",
    ],
    kpiAr: "نلتزم بزيادة معدّل الردود +٢٠٪ خلال ٤ أشهر، وإلا نشتغل بدون مقابل حتى يتحقق.",
    kpiEn: "We commit to +20% reply-rate lift in 4 months, or work for free until reached.",
    ctaKind: "checkout",
  },
  {
    id: "executive_command_center_7500",
    slug: "executive-command-center",
    nameAr: "غرفة قيادة الإدارة",
    nameEn: "Executive Command Center",
    priceSar: 7500,
    period: "monthly",
    taglineAr: "لوحة قيادة الإيراد الكاملة + موجز يومي للمؤسس.",
    taglineEn: "Full revenue command center + daily founder brief.",
    deliverablesAr: [
      "موجز يومي للمؤسس",
      "رادار الإيراد المباشر + لوحة الإشارات",
      "Pack مجلس إدارة شهري",
      "سجل الأدلة + طابور الموافقات اليومي",
    ],
    deliverablesEn: [
      "Daily founder brief",
      "Live revenue radar + signals board",
      "Monthly board pack",
      "Proof ledger + daily approval queue",
    ],
    kpiAr: "نوفّر للإدارة ٤٠٪+ من وقت اتخاذ القرار خلال ٤ أشهر، وإلا شهر مجاني.",
    kpiEn: "Save the executive 40%+ of decision time in 4 months, or 1 free month.",
    ctaKind: "checkout",
  },
  {
    id: "agency_partner_os",
    slug: "custom-ai-build",
    nameAr: "بناء ذكاء اصطناعي مخصّص",
    nameEn: "Custom AI Build",
    priceSar: 0,
    period: "custom",
    taglineAr: "عندك شيء محدّد تبي نبنيه؟ قل لنا النطاق ونرجع لك بخطة وتقدير.",
    taglineEn: "Have something specific in mind? Tell us the scope — we return a plan and estimate.",
    deliverablesAr: [
      "وكيل/أتمتة مخصّصة لحالتك",
      "تكامل مع أنظمتك الحالية",
      "حوكمة وموافقات حسب نطاقك",
      "تدريب وتسليم موثّق",
    ],
    deliverablesEn: [
      "Bespoke agent/automation for your case",
      "Integration with your existing systems",
      "Governance & approvals scoped to you",
      "Training & documented handover",
    ],
    kpiAr: "نطاق وتقدير مبدئي خلال يوم عمل — بلا أرقام مخترَعة، بلا التزام قبل الموافقة.",
    kpiEn: "Scope and initial estimate within one business day — no invented numbers, no commitment before approval.",
    ctaKind: "custom",
  },
];

/** Optional monthly add-on (sold alongside Growth Ops / ECC, not a standalone rung). */
export const SUPPORT_ADDON: PricingTier = {
  id: "support_os_addon_1500",
  slug: "support-os-addon",
  nameAr: "إضافة دعم العملاء (Support OS)",
  nameEn: "Support OS Add-on",
  priceSar: 1500,
  period: "monthly",
  taglineAr: "تصنيف التذاكر ومسودّات ردود وتنبيهات SLA — يُضاف لأي باقة شهرية.",
  taglineEn: "Ticket classification, reply drafts, SLA alerts — add to any monthly plan.",
  deliverablesAr: [
    "تصنيف التذاكر (١٢ فئة)",
    "مسودّات ردود (بلا إرسال تلقائي)",
    "قائمة تصعيد أسبوعية + خريطة الأسباب",
  ],
  deliverablesEn: [
    "Ticket classification (12 categories)",
    "Reply drafts (no auto-send)",
    "Weekly escalation list + root-cause map",
  ],
  kpiAr: "نقلّل وقت الردّ الأول إلى ≤٣٠ دقيقة في ساعات العمل، وإلا شهران مجاناً.",
  kpiEn: "Reduce first-response time to ≤30 min in business hours, or 2 free months.",
  ctaKind: "checkout",
};

const AR_DIGITS = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];

function toArabicDigits(value: string): string {
  return value.replace(/\d/g, (d) => AR_DIGITS[Number(d)]);
}

/** Render a tier's price for display (bilingual, Arabic-Indic digits in AR). */
export function formatTierPrice(tier: PricingTier, isAr: boolean): string {
  if (tier.period === "free") return isAr ? "مجاناً" : "Free";
  if (tier.period === "custom") return isAr ? "حسب النطاق" : "Custom";
  const amount = tier.priceSar.toLocaleString("en-US");
  const amountStr = isAr ? toArabicDigits(amount) : amount;
  const currency = isAr ? "ر.س" : "SAR";
  const suffix =
    tier.period === "monthly" ? (isAr ? " / شهر" : " / mo") : "";
  return isAr ? `${amountStr} ${currency}${suffix}` : `${amountStr} ${currency}${suffix}`;
}

export function getTier(id: string): PricingTier | undefined {
  return [...PRICING_TIERS, SUPPORT_ADDON].find((t) => t.id === id);
}
