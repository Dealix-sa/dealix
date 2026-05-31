import type { Metadata } from "next";
import Link from "next/link";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "خدمات Dealix — سلم العروض الخمسة" : "Dealix Services — Five-Tier Offer Ladder",
    description: isAr
      ? "من التشخيص المجاني إلى مشاريع AI المخصصة — كل مستوى يبني على الإثبات قبل التوسع."
      : "From free diagnostic to custom AI projects — every tier builds on proof before expansion.",
    alternates: { canonical: `https://dealix.me/${locale}/services` },
  };
}

const TIERS_AR = [
  {
    id: "free",
    icon: "🔍",
    label: "تشخيص مجاني",
    price: "مجاني",
    period: "",
    badge: "",
    highlight: false,
    desc: "نقطة البداية لكل شركة — اعرف وضعك قبل أي التزام.",
    deliverables: [
      "Risk Score تشغيلي (1-100)",
      "تحليل جاهزية ZATCA/PDPL",
      "تحديد 3 فجوات رئيسية",
      "توصية المسار التالي",
    ],
    timeline: "5 دقائق",
    suitable: "كل شركة تريد تقييم وضعها",
    cta: "احسب Risk Score",
    href: "/risk-score",
  },
  {
    id: "sprint",
    icon: "⚡",
    label: "10-Lead Audit Sprint",
    price: "499",
    period: "ر.س",
    badge: "",
    highlight: false,
    desc: "مراجعة عميقة لـ 10 leads حقيقية من قائمتك — ليس lead generation.",
    deliverables: [
      "مالك واضح لكل lead",
      "فجوات أدلة CRM",
      "مسودة Proof لأفضل 3 leads",
      "خطوة تالية واحدة لكل lead",
      "ملاحظة governance",
    ],
    timeline: "48 ساعة",
    suitable: "وكالات تسويق، فرق مبيعات B2B",
    cta: "ابدأ Sprint 499 ر.س",
    href: "/dealix-diagnostic",
  },
  {
    id: "proof",
    icon: "📦",
    label: "Agency Proof Pack",
    price: "1,500",
    period: "ر.س",
    badge: "",
    highlight: false,
    desc: "حزمة إثبات كاملة لتقديمها للعميل — 4 أقسام، مستويات L0-L5.",
    deliverables: [
      "4 أقسام: مصادر، ملاك، أدلة، قرارات",
      "مستويات أدلة L0-L5 موثّقة",
      "PDF ثنائي اللغة (AR + EN)",
      "جدول حالة الأقسام",
      "توصية Sprint / Retainer",
    ],
    timeline: "7 أيام",
    suitable: "وكالات تريد إثبات قيمة العمل للعملاء",
    cta: "اطلب Agency Proof Pack",
    href: "/dealix-diagnostic",
  },
  {
    id: "managed",
    icon: "🏢",
    label: "Managed Ops Retainer",
    price: "2,999 – 4,999",
    period: "ر.س/شهر",
    badge: "الأكثر طلباً",
    highlight: true,
    desc: "تشغيل مُدار شهرياً — OKR، proof، أولوية دعم. يبدأ فقط بعد Proof Pack.",
    deliverables: [
      "OKR أسبوعي محكوم",
      "Proof Pack شهري مُحدَّث",
      "مراجعة CRM + evidence",
      "دعم أولوية (48 ساعة SLA)",
      "Approval Center لكل قرار حرج",
      "Company Brain snapshot شهري",
    ],
    timeline: "يبدأ بعد Proof Pack",
    suitable: "شركات أثبتت قيمة من التشخيص",
    cta: "احجز استشارة",
    href: "/dealix-diagnostic",
  },
  {
    id: "custom",
    icon: "🤖",
    label: "Custom AI Project",
    price: "5,000 – 25,000",
    period: "ر.س",
    badge: "",
    highlight: false,
    desc: "تطوير AI مخصص لعملياتك — Scope محدد، نتائج موثّقة، Approval Center لكل خطوة.",
    deliverables: [
      "Scope document محدد ومُوقَّع",
      "تطوير مخصص مع audit trail",
      "Approval Center لكل خطوة",
      "Proof Pack ختامي",
      "توثيق PDPL كامل",
      "Hand-off مع training",
    ],
    timeline: "4-12 أسبوع",
    suitable: "شركات على Managed Ops تريد توسع",
    cta: "ناقش مشروعك",
    href: "/dealix-diagnostic",
  },
];

const TIERS_EN = [
  {
    id: "free",
    icon: "🔍",
    label: "Free Diagnostic",
    price: "Free",
    period: "",
    badge: "",
    highlight: false,
    desc: "The starting point for every company — know your position before any commitment.",
    deliverables: [
      "Operational Risk Score (1-100)",
      "ZATCA/PDPL readiness analysis",
      "3 main gap identification",
      "Next path recommendation",
    ],
    timeline: "5 minutes",
    suitable: "Every company that wants to assess their position",
    cta: "Calculate Risk Score",
    href: "/risk-score",
  },
  {
    id: "sprint",
    icon: "⚡",
    label: "10-Lead Audit Sprint",
    price: "499",
    period: "SAR",
    badge: "",
    highlight: false,
    desc: "Deep review of 10 real leads from your list — not lead generation.",
    deliverables: [
      "Clear owner per lead",
      "CRM evidence gaps",
      "Proof draft for top 3 leads",
      "One next action per lead",
      "Governance note",
    ],
    timeline: "48 hours",
    suitable: "Marketing agencies, B2B sales teams",
    cta: "Start Sprint 499 SAR",
    href: "/dealix-diagnostic",
  },
  {
    id: "proof",
    icon: "📦",
    label: "Agency Proof Pack",
    price: "1,500",
    period: "SAR",
    badge: "",
    highlight: false,
    desc: "Full proof bundle to present to your client — 4 sections, L0-L5 evidence levels.",
    deliverables: [
      "4 sections: sources, owners, evidence, decisions",
      "L0-L5 evidence levels documented",
      "Bilingual PDF (AR + EN)",
      "Section status table",
      "Sprint / Retainer recommendation",
    ],
    timeline: "7 days",
    suitable: "Agencies that want to prove value to clients",
    cta: "Request Agency Proof Pack",
    href: "/dealix-diagnostic",
  },
  {
    id: "managed",
    icon: "🏢",
    label: "Managed Ops Retainer",
    price: "2,999 – 4,999",
    period: "SAR/mo",
    badge: "Most Popular",
    highlight: true,
    desc: "Monthly managed ops — OKR, proof, priority support. Starts only after Proof Pack.",
    deliverables: [
      "Governed weekly OKR",
      "Monthly updated Proof Pack",
      "CRM + evidence review",
      "Priority support (48h SLA)",
      "Approval Center for critical decisions",
      "Monthly Company Brain snapshot",
    ],
    timeline: "Starts after Proof Pack",
    suitable: "Companies that have proven value from diagnostic",
    cta: "Book Consultation",
    href: "/dealix-diagnostic",
  },
  {
    id: "custom",
    icon: "🤖",
    label: "Custom AI Project",
    price: "5,000 – 25,000",
    period: "SAR",
    badge: "",
    highlight: false,
    desc: "Custom AI development for your operations — defined scope, documented outcomes, Approval Center at every step.",
    deliverables: [
      "Defined and signed Scope document",
      "Custom development with audit trail",
      "Approval Center at every step",
      "Final Proof Pack",
      "Full PDPL documentation",
      "Hand-off with training",
    ],
    timeline: "4-12 weeks",
    suitable: "Companies on Managed Ops who want to expand",
    cta: "Discuss Your Project",
    href: "/dealix-diagnostic",
  },
];

const COMPARISON_ROWS_AR = [
  { feature: "Risk Score فوري", free: true, sprint: true, proof: true, managed: true, custom: true },
  { feature: "مراجعة leads حقيقية", free: false, sprint: true, proof: true, managed: true, custom: true },
  { feature: "PDF Proof ثنائي اللغة", free: false, sprint: false, proof: true, managed: true, custom: true },
  { feature: "OKR أسبوعي", free: false, sprint: false, proof: false, managed: true, custom: true },
  { feature: "Approval Center", free: false, sprint: false, proof: false, managed: true, custom: true },
  { feature: "تطوير مخصص", free: false, sprint: false, proof: false, managed: false, custom: true },
  { feature: "PDPL/ZATCA موثّق", free: "جزئي", sprint: "جزئي", proof: true, managed: true, custom: true },
];

const COMPARISON_ROWS_EN = [
  { feature: "Instant Risk Score", free: true, sprint: true, proof: true, managed: true, custom: true },
  { feature: "Real lead review", free: false, sprint: true, proof: true, managed: true, custom: true },
  { feature: "Bilingual Proof PDF", free: false, sprint: false, proof: true, managed: true, custom: true },
  { feature: "Weekly OKR", free: false, sprint: false, proof: false, managed: true, custom: true },
  { feature: "Approval Center", free: false, sprint: false, proof: false, managed: true, custom: true },
  { feature: "Custom development", free: false, sprint: false, proof: false, managed: false, custom: true },
  { feature: "PDPL/ZATCA documented", free: "partial", sprint: "partial", proof: true, managed: true, custom: true },
];

function CheckCell({ v }: { v: boolean | string }) {
  if (v === true) return <span className="text-emerald-500 font-bold text-lg">✓</span>;
  if (v === false) return <span className="text-muted-foreground/40">—</span>;
  return <span className="text-amber-500 text-xs font-medium">{v}</span>;
}

export default async function ServicesHubPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const tiers = isAr ? TIERS_AR : TIERS_EN;
  const rows = isAr ? COMPARISON_ROWS_AR : COMPARISON_ROWS_EN;

  return (
    <PublicGtmShell>
      <div className={`mx-auto max-w-5xl px-6 py-12 space-y-16 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>

        {/* Header */}
        <header>
          <p className="text-sm font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wide">
            {isAr ? "سلم العروض" : "Offer Ladder"}
          </p>
          <h1 className="mt-2 text-4xl font-bold leading-tight">
            {isAr ? "خمسة مستويات — ابدأ من حيث أنت جاهز" : "Five Tiers — Start Where You're Ready"}
          </h1>
          <p className="mt-4 max-w-2xl text-muted-foreground leading-relaxed">
            {isAr
              ? "كل مستوى يبني على الإثبات من المستوى السابق. لا توسع بدون Proof Pack مُسلَّم. هذا مبدأ غير قابل للتفاوض."
              : "Every tier builds on proof from the previous tier. No expansion without a delivered Proof Pack. This is non-negotiable."}
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link href={`${base}/risk-score`} className="inline-flex items-center gap-2 rounded-lg border border-emerald-500/40 bg-emerald-50/50 dark:bg-emerald-950/20 px-4 py-2 text-sm font-medium text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100/50 dark:hover:bg-emerald-900/30 transition-colors">
              🔍 {isAr ? "ابدأ بـ Risk Score مجاني" : "Start with Free Risk Score"}
            </Link>
            <Link href={`${base}/proof-pack`} className="inline-flex items-center gap-2 rounded-lg border border-border/60 bg-card/60 px-4 py-2 text-sm font-medium hover:bg-muted/30 transition-colors">
              📦 {isAr ? "شاهد عيّنة Proof Pack" : "View Sample Proof Pack"}
            </Link>
          </div>
        </header>

        {/* Tier Cards */}
        <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          {tiers.map((tier) => (
            <div
              key={tier.id}
              className={`relative flex flex-col rounded-2xl border p-6 transition-shadow hover:shadow-md ${
                tier.highlight
                  ? "border-amber-500/50 bg-gradient-to-b from-amber-50/30 to-card dark:from-amber-950/20 shadow-sm"
                  : "border-border/60 bg-card/50"
              }`}
            >
              {tier.badge && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-amber-500 text-white text-xs font-bold px-3 py-0.5 whitespace-nowrap">
                  {tier.badge}
                </div>
              )}
              <div className="flex items-start gap-2 mb-4">
                <span className="text-2xl">{tier.icon}</span>
                <div>
                  <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">{tier.label}</p>
                  <div className="flex items-baseline gap-1 mt-0.5">
                    <span className="text-2xl font-bold">{tier.price}</span>
                    {tier.period && <span className="text-sm text-muted-foreground">{tier.period}</span>}
                  </div>
                </div>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed mb-4">{tier.desc}</p>
              <div className="flex-1">
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                  {isAr ? "المخرجات" : "Deliverables"}
                </p>
                <ul className="space-y-1">
                  {tier.deliverables.map((d) => (
                    <li key={d} className="flex items-start gap-1.5 text-xs">
                      <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                      <span>{d}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="mt-4 pt-4 border-t border-border/40 space-y-2">
                <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <span>⏱</span>
                  <span>{tier.timeline}</span>
                </div>
                <div className="flex items-start gap-1.5 text-xs text-muted-foreground">
                  <span>👥</span>
                  <span>{tier.suitable}</span>
                </div>
                <Link
                  href={`${base}${tier.href}`}
                  className={`mt-2 flex w-full items-center justify-center rounded-lg px-4 py-2.5 text-sm font-semibold transition-colors ${
                    tier.highlight
                      ? "bg-amber-500 text-white hover:bg-amber-600"
                      : "bg-primary text-primary-foreground hover:bg-primary/90"
                  }`}
                >
                  {tier.cta}
                </Link>
              </div>
            </div>
          ))}
        </section>

        {/* Comparison Table */}
        <section>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "مقارنة المستويات" : "Tier Comparison"}
          </h2>
          <div className="overflow-x-auto rounded-xl border border-border/60">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border/60 bg-muted/30">
                  <th className="py-3 px-4 text-start font-semibold">
                    {isAr ? "الميزة" : "Feature"}
                  </th>
                  {tiers.map((t) => (
                    <th key={t.id} className={`py-3 px-3 text-center font-semibold text-xs ${t.highlight ? "text-amber-600 dark:text-amber-400" : ""}`}>
                      {t.icon} {t.label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-muted/20 transition-colors">
                    <td className="py-3 px-4 font-medium">{row.feature}</td>
                    <td className="py-3 px-3 text-center"><CheckCell v={row.free} /></td>
                    <td className="py-3 px-3 text-center"><CheckCell v={row.sprint} /></td>
                    <td className="py-3 px-3 text-center"><CheckCell v={row.proof} /></td>
                    <td className="py-3 px-3 text-center"><CheckCell v={row.managed} /></td>
                    <td className="py-3 px-3 text-center"><CheckCell v={row.custom} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Which tier am I? */}
        <section className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8">
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "أي مستوى يناسبني؟" : "Which tier is right for me?"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {(isAr ? [
              { cond: "أريد معرفة وضعي الحالي فقط", ans: "ابدأ بـ Risk Score مجاني", tier: "free", href: "/risk-score" },
              { cond: "عندي leads ولا أعرف لماذا لا تتحوّل", ans: "10-Lead Audit Sprint — 499 ر.س", tier: "sprint", href: "/dealix-diagnostic" },
              { cond: "وكالة تريد تقديم دليل لعميلها", ans: "Agency Proof Pack — 1,500 ر.س", tier: "proof", href: "/dealix-diagnostic" },
              { cond: "أثبتت قيمة التشخيص وأريد نتائج مستمرة", ans: "Managed Ops Retainer من 2,999 ر.س/شهر", tier: "managed", href: "/dealix-diagnostic" },
            ] : [
              { cond: "I want to understand my current position", ans: "Start with Free Risk Score", tier: "free", href: "/risk-score" },
              { cond: "I have leads but don't know why they don't convert", ans: "10-Lead Audit Sprint — 499 SAR", tier: "sprint", href: "/dealix-diagnostic" },
              { cond: "Agency that wants to prove value to a client", ans: "Agency Proof Pack — 1,500 SAR", tier: "proof", href: "/dealix-diagnostic" },
              { cond: "I've proven diagnostic value and want ongoing results", ans: "Managed Ops Retainer from 2,999 SAR/mo", tier: "managed", href: "/dealix-diagnostic" },
            ]).map((item) => (
              <Link
                key={item.tier}
                href={`${base}${item.href}`}
                className="block rounded-xl border border-white/10 bg-white/5 p-4 hover:bg-white/10 transition-colors"
              >
                <p className="text-white/60 text-xs mb-1">{isAr ? "إذا كنت:" : "If you:"}</p>
                <p className="text-white font-medium text-sm">{item.cond}</p>
                <p className="mt-2 text-amber-300 text-xs font-semibold">→ {item.ans}</p>
              </Link>
            ))}
          </div>
          <p className="mt-6 text-white/50 text-xs">
            {isAr
              ? "* لا upsell بدون Proof Pack مُسلَّم · الأسعار بالريال السعودي · موافقة بشرية على كل خطوة حرجة"
              : "* No upsell without delivered Proof Pack · All prices in SAR · Human approval at every critical step"}
          </p>
        </section>

      </div>
    </PublicGtmShell>
  );
}
