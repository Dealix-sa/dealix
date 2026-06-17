/**
 * Dealix service catalog — typed, bilingual, for the public web.
 *
 * SOURCE OF TRUTH: `auto_client_acquisition/service_catalog/registry.py`
 * (the 7 canonical offerings). This file MIRRORS that registry for the
 * Next.js surface (which cannot import Python). Keep prices/deliverables in
 * sync with registry.py — pricing changes are 1-line edits there first.
 *
 * Doctrine: every customer-facing surface is approval-first and carries the
 * bilingual value disclaimer. No guaranteed outcomes, no auto-send, no
 * scraping. KPI language is a commitment, never a guarantee.
 */

export type Accent = "slate" | "cyan" | "emerald" | "violet" | "gold" | "amber";

export interface Offering {
  id: string;
  /** Short tier label, e.g. "Rung 0" */
  rung: string;
  nameEn: string;
  nameAr: string;
  /** Display price, already formatted (SAR). */
  priceEn: string;
  priceAr: string;
  /** Billing unit / cadence. */
  unitEn: string;
  unitAr: string;
  durationEn: string;
  durationAr: string;
  taglineEn: string;
  taglineAr: string;
  deliverablesEn: string[];
  deliverablesAr: string[];
  /** KPI commitment (commitment language, never "guarantee"). */
  kpiEn: string;
  kpiAr: string;
  accent: Accent;
  /** Whether this is the recommended starting point. */
  featured?: boolean;
}

/**
 * The self-serve productized ladder (ascending). Mirrors registry.py OFFERINGS.
 * Non-chargeable entries (Free Diagnostic, Agency Partner custom) are sales
 * offerings only — they are NOT in the chargeable Moyasar `PLANS` map.
 */
export const SERVICE_LADDER: Offering[] = [
  {
    id: "free_mini_diagnostic",
    rung: "Rung 0",
    nameEn: "Free Mini Diagnostic",
    nameAr: "التشخيص المجاني المختصر",
    priceEn: "Free",
    priceAr: "مجاناً",
    unitEn: "no payment",
    unitAr: "بدون دفع",
    durationEn: "24 hours",
    durationAr: "٢٤ ساعة",
    taglineEn: "See where your revenue leaks — before you pay anything.",
    taglineAr: "شوف أين تتسرّب إيراداتك — قبل أن تدفع أي شيء.",
    deliverablesEn: [
      "1-page sector-fit analysis",
      "3 ranked opportunities",
      "1 Arabic message draft",
      "Best-channel recommendation",
      "1 risk to avoid + next-step decision passport",
    ],
    deliverablesAr: [
      "تحليل ملاءمة قطاعك في صفحة واحدة",
      "٣ فرص مرتّبة بالأولوية",
      "مسودة رسالة عربية واحدة",
      "توصية بأفضل قناة تواصل",
      "خطر يجب تجنّبه + جواز قرار للخطوة التالية",
    ],
    kpiEn: "Delivered within 24 hours of form submission.",
    kpiAr: "نسلّم خلال ٢٤ ساعة من تعبئة النموذج.",
    accent: "slate",
  },
  {
    id: "revenue_proof_sprint_499",
    rung: "Rung 1",
    nameEn: "Revenue Proof Sprint",
    nameAr: "سبرنت إثبات الإيرادات",
    priceEn: "499 SAR",
    priceAr: "٤٩٩ ريال",
    unitEn: "one-time",
    unitAr: "مرة واحدة",
    durationEn: "7 days",
    durationAr: "٧ أيام",
    taglineEn: "Prove the value in one week. No long contract.",
    taglineAr: "نثبت القيمة في أسبوع. بدون عقد طويل.",
    deliverablesEn: [
      "Company Brain v1 + Top 10 ranked opportunities",
      "Decision Passports for the top 3",
      "Arabic Draft Pack (5 messages)",
      "7-day follow-up plan + risk/objection map",
      "Executive Pack + Proof Pack + next-best-offer",
    ],
    deliverablesAr: [
      "Company Brain v1 + أفضل ١٠ فرص مرتّبة",
      "جوازات قرار لأفضل ٣",
      "حزمة مسودات عربية (٥ رسائل)",
      "خطة متابعة ٧ أيام + خريطة مخاطر واعتراضات",
      "حزمة تنفيذية + Proof Pack + العرض التالي",
    ],
    kpiEn: "7 deliverables in 7 days. If we don't surface ≥10 opportunities, we work for free until we do.",
    kpiAr: "٧ مخرجات في ٧ أيام. إذا لم نصل لـ١٠ فرص، نشتغل بدون مقابل حتى نوصل.",
    accent: "cyan",
    featured: true,
  },
  {
    id: "data_to_revenue_pack_1500",
    rung: "Rung 2",
    nameEn: "Data-to-Revenue Pack",
    nameAr: "حزمة من البيانات إلى الإيراد",
    priceEn: "1,500 SAR",
    priceAr: "١٥٠٠ ريال",
    unitEn: "one-time",
    unitAr: "مرة واحدة",
    durationEn: "14 days",
    durationAr: "١٤ يوم",
    taglineEn: "Turn a messy lead list into a clean, scored pipeline.",
    taglineAr: "نحوّل قائمة leads فوضوية إلى pipeline نظيف ومُقيّم.",
    deliverablesEn: [
      "Clean, deduplicated Lead Board + duplicate report",
      "Source validation + risk report",
      "Top 20 scored opportunities",
      "10 Arabic drafts + follow-up plan",
      "Decision Passports for the top 5",
    ],
    deliverablesAr: [
      "Lead Board نظيف بلا تكرار + تقرير المكرّر",
      "التحقق من المصادر + تقرير المخاطر",
      "أفضل ٢٠ فرصة مُقيّمة",
      "١٠ مسودات عربية + خطة متابعة",
      "جوازات قرار لأفضل ٥",
    ],
    kpiEn: "Clean 400+ rows in 14 days. If we don't surface 20 approved opportunities, we work until we do.",
    kpiAr: "تنظيف ٤٠٠+ سطر في ١٤ يوم. إذا لم نصل لـ٢٠ فرصة معتمدة، نواصل حتى نوصل.",
    accent: "cyan",
  },
  {
    id: "growth_ops_monthly_2999",
    rung: "Rung 3",
    nameEn: "Growth Ops — Monthly",
    nameAr: "عمليات النمو الشهرية",
    priceEn: "2,999 SAR",
    priceAr: "٢٩٩٩ ريال",
    unitEn: "per month",
    unitAr: "شهرياً",
    durationEn: "4-month minimum",
    durationAr: "٤ أشهر كحد أدنى",
    taglineEn: "A weekly revenue-ops layer — without hiring a team.",
    taglineAr: "طبقة تشغيل إيرادات أسبوعية — بدون توظيف فريق.",
    deliverablesEn: [
      "4 weekly pipeline audits + weekly lead board",
      "Daily approval queue",
      "Draft pack (≥20 messages/month)",
      "Support insights + ongoing proof events",
      "Monthly Proof Pack + executive summary",
    ],
    deliverablesAr: [
      "٤ مراجعات pipeline أسبوعية + Lead Board أسبوعي",
      "قائمة موافقات يومية",
      "حزمة مسودات (٢٠+ رسالة/شهر)",
      "رؤى الدعم + أحداث إثبات مستمرة",
      "Proof Pack شهري + ملخّص تنفيذي",
    ],
    kpiEn: "Commit to +20% reply-rate lift in 4 months. If not reached, we work for free until reached.",
    kpiAr: "نلتزم بزيادة معدل الردود +٢٠٪ خلال ٤ أشهر. إن لم يتحقق، نشتغل بدون مقابل حتى يتحقق.",
    accent: "emerald",
    featured: true,
  },
  {
    id: "support_os_addon_1500",
    rung: "Add-on",
    nameEn: "Support OS Add-on",
    nameAr: "إضافة دعم العملاء",
    priceEn: "1,500 SAR",
    priceAr: "١٥٠٠ ريال",
    unitEn: "per month",
    unitAr: "شهرياً",
    durationEn: "monthly",
    durationAr: "شهري",
    taglineEn: "Classify, draft, and triage support — approval-first.",
    taglineAr: "تصنيف ومسودات وفرز الدعم — بموافقة أولاً.",
    deliverablesEn: [
      "Ticket classification (12 categories)",
      "Suggested replies (draft-only)",
      "Weekly escalation list + root-cause map",
      "Customer health-score updates",
      "SLA-breach alerts + support proof events",
    ],
    deliverablesAr: [
      "تصنيف التذاكر (١٢ فئة)",
      "ردود مقترحة (مسودة فقط)",
      "قائمة تصعيد أسبوعية + خريطة جذور",
      "تحديث Customer Health Score",
      "تنبيهات خرق SLA + أحداث إثبات",
    ],
    kpiEn: "Reduce first-response time to ≤30 min in business hours. If unmet, 2 free months.",
    kpiAr: "نقلّل وقت الرد الأول إلى ≤٣٠ دقيقة في ساعات العمل. إن لم يتحقق، شهران مجاناً.",
    accent: "amber",
  },
  {
    id: "executive_command_center_7500",
    rung: "Rung 4",
    nameEn: "Executive Command Center",
    nameAr: "غرفة قيادة الإدارة",
    priceEn: "7,500 SAR",
    priceAr: "٧٥٠٠ ريال",
    unitEn: "per month",
    unitAr: "شهرياً",
    durationEn: "4-month engagement",
    durationAr: "ارتباط ٤ أشهر",
    taglineEn: "The founder's single screen for revenue, decisions, and risk.",
    taglineAr: "شاشة المؤسس الواحدة للإيراد والقرارات والمخاطر.",
    deliverablesEn: [
      "Daily founder brief (WhatsApp) + weekly pipeline audit",
      "Monthly board pack + live revenue radar",
      "Sales pipeline, growth signals & support health",
      "Proof ledger + daily approval queue",
      "Weekly risk register + next-7-days plan",
    ],
    deliverablesAr: [
      "ملخّص مؤسس يومي (واتساب) + مراجعة pipeline أسبوعية",
      "حزمة مجلس شهرية + رادار إيراد حي",
      "Pipeline المبيعات وإشارات النمو وصحة الدعم",
      "سجلّ الإثبات + قائمة موافقات يومية",
      "سجلّ مخاطر أسبوعي + خطة الأيام السبعة القادمة",
    ],
    kpiEn: "Save the executive 40%+ of decision time in 4 months. If unmet, 1 free month.",
    kpiAr: "نوفّر للإدارة ٤٠٪+ من وقت القرار خلال ٤ أشهر. إن لم يتحقق، شهر مجاني.",
    accent: "violet",
  },
  {
    id: "agency_partner_os",
    rung: "Channel",
    nameEn: "Agency Partner OS",
    nameAr: "نظام الشريك الوكالة",
    priceEn: "Custom",
    priceAr: "مخصّص",
    unitEn: "partnership",
    unitAr: "شراكة",
    durationEn: "ongoing",
    durationAr: "مستمر",
    taglineEn: "Run Dealix for your own clients, co-branded.",
    taglineAr: "شغّل Dealix لعملائك تحت علامتك المشتركة.",
    deliverablesEn: [
      "Partner intake + co-branded diagnostic",
      "Client proof sprint + proof pack per client",
      "Renewal / upsell pack",
      "Partner revenue tracking",
      "30% first-year commission tracking",
    ],
    deliverablesAr: [
      "Partner Intake + تشخيص مشترك العلامة",
      "Proof Sprint + Proof Pack لكل عميل",
      "حزمة تجديد / upsell",
      "تتبّع إيرادات الشريك",
      "تتبّع عمولة ٣٠٪ للسنة الأولى",
    ],
    kpiEn: "30% commission for the first paid year per referred customer. Never publish proof without signed consent.",
    kpiAr: "عمولة ٣٠٪ للسنة المدفوعة الأولى لكل عميل محوّل. ولا ننشر إثباتاً بدون موافقة موقّعة.",
    accent: "gold",
  },
];

/**
 * The flagship founder-led custom engagement. A premium layer ABOVE the
 * self-serve ladder (the "Custom AI Service Setup" rung), not a replacement.
 * Pricing band is the private-launch price; reconcile in
 * docs/30_pricing/SPRINT_PRICING.md before any public pricing page hard-codes it.
 */
export const COMMAND_SPRINT = {
  id: "command_sprint",
  nameEn: "Dealix Command Sprint",
  nameAr: "Dealix Command Sprint",
  priceEn: "7,500 – 15,000 SAR",
  priceAr: "٧٥٠٠ – ١٥٠٠٠ ريال",
  unitEn: "one-time · 10 working days",
  unitAr: "مرة واحدة · ١٠ أيام عمل",
  taglineEn:
    "A founder-led, done-with-you build: turn scattered follow-up, offers, and revenue decisions into one approval-first AI operating workflow — in 10 working days.",
  taglineAr:
    "بناء بقيادة المؤسس معك: نحوّل فوضى المتابعة والعروض والقرار التجاري إلى نظام تشغيل إيرادات واحد بأسلوب الموافقة أولاً — خلال ١٠ أيام عمل.",
  deliverablesEn: [
    "Business intake + current workflow map",
    "Lead & follow-up audit (where opportunities leak)",
    "Offer / proposal audit",
    "WhatsApp / email response map (manual, approval-first — no cold automation)",
    "Executive dashboard prototype (revenue-leakage view)",
    "Approval-first AI workflow (drafts → human approves → execute)",
    "Dry-run AI assistant (no live external action without approval)",
    "Bilingual, evidence-backed Proof Pack",
    "CEO brief + retainer proposal (path to Monthly RevOps / ECC)",
  ],
  deliverablesAr: [
    "Business intake + خريطة سير العمل الحالي",
    "تدقيق leads والمتابعة (أين تتسرّب الفرص)",
    "تدقيق العروض / المقترحات",
    "خريطة ردود واتساب/الإيميل (يدوي، موافقة أولاً — بلا أتمتة باردة)",
    "نموذج لوحة تنفيذية (عرض تسرّب الإيراد)",
    "تدفّق AI بموافقة أولاً (مسودات ← موافقة بشرية ← تنفيذ)",
    "مساعد AI بوضع تجريبي (لا فعل خارجي حي بدون موافقة)",
    "Proof Pack ثنائي اللغة قائم على الأدلة",
    "ملخّص للمدير التنفيذي + عرض retainer (مسار إلى RevOps الشهري / ECC)",
  ],
} as const;

/** Governance points shown on every services surface (doctrine, not marketing). */
export const GOVERNANCE_EN: string[] = [
  "AI drafts → you review → you send. No auto-send in any service.",
  "No scraping of external data. No cold WhatsApp / LinkedIn automation.",
  "No ROI claims without a documented baseline.",
  "No external send and no live payment without explicit approval.",
];

export const GOVERNANCE_AR: string[] = [
  "AI يكتب ← أنت تراجع ← أنت ترسل. لا إرسال آلي في أي خدمة.",
  "لا scraping لبيانات خارجية. لا أتمتة واتساب/لينكدإن باردة.",
  "لا ادعاءات ROI بدون baseline موثّق.",
  "لا إرسال خارجي ولا دفع حي بدون موافقة صريحة.",
];

/** Mandatory bilingual value disclaimer — must end every customer-facing surface. */
export const VALUE_DISCLAIMER =
  "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.";

export const SECTORS = [
  "Consulting",
  "Training & Education",
  "Marketing Agency",
  "Real Estate Services",
  "Technology / SaaS",
  "Professional Services",
  "Logistics & Supply",
  "Healthcare Services",
  "Other",
];
