"use client";

import Link from "next/link";
import { useLocale } from "next-intl";

/* ─── Team Data ─────────────────────────────────────────────────── */

type TeamMember = {
  name: string;
  titleAr: string;
  titleEn: string;
  bioAr: string;
  bioEn: string;
  linkedinSlug?: string;
  initials: string;
  color: string;
};

const TEAM: TeamMember[] = [
  {
    name: "بسام",
    titleAr: "المؤسس والرئيس التنفيذي",
    titleEn: "Founder & CEO",
    bioAr:
      "متخصص في تشغيل الإيرادات للشركات السعودية. بنى Dealix لحل مشكلة واحدة: مساعدة الشركات السعودية على تحويل البيانات إلى إيرادات متكررة.",
    bioEn:
      "Revenue operations specialist for Saudi companies. Built Dealix to solve one problem: helping Saudi businesses convert data into recurring revenue.",
    initials: "ب",
    color: "bg-[#C9974B]/20 text-[#C9974B]",
  },
];

type Value = {
  icon: string;
  titleAr: string;
  titleEn: string;
  descAr: string;
  descEn: string;
};

const VALUES: Value[] = [
  {
    icon: "🏛",
    titleAr: "الحوكمة أولاً",
    titleEn: "Governance First",
    descAr: "لا شيء يُرسل بدون موافقة المؤسس. APPROVAL_FIRST ليس سياسة — هو هوية.",
    descEn: "Nothing is sent without founder approval. APPROVAL_FIRST is not a policy — it's our identity.",
  },
  {
    icon: "🎯",
    titleAr: "الإثبات قبل الوعد",
    titleEn: "Proof Before Promise",
    descAr: "كل ادعاء مدعوم بـ Proof Pack. لا نبيع بالأرقام المضمونة — نبيع بالنتائج الموثقة.",
    descEn: "Every claim is backed by a Proof Pack. We don't sell with guaranteed numbers — we sell with documented results.",
  },
  {
    icon: "🇸🇦",
    titleAr: "محلي حقيقي",
    titleEn: "Authentically Local",
    descAr:
      "PDPL، ZATCA، العربية أولاً. لسنا أداة غربية تُعرَّب — نحن منتج سعودي بنيناه من الداخل.",
    descEn:
      "PDPL, ZATCA, Arabic-first. We're not a Western tool being Arabized — we're a Saudi product built from the inside.",
  },
  {
    icon: "🔁",
    titleAr: "الإيراد المتكرر فقط",
    titleEn: "Recurring Revenue Only",
    descAr: "لا مشاريع لمرة واحدة. كل عميل نبدأ معه نريد بناء علاقة شهرية طويلة الأمد.",
    descEn: "No one-off projects. Every client we start with, we aim to build a long-term monthly relationship.",
  },
  {
    icon: "📊",
    titleAr: "البيانات ليست ملكنا",
    titleEn: "Your Data Is Yours",
    descAr: "بيانات العميل تعود له 100٪. نعالجها، لا نحتجزها. PDPL متجذر في كل سطر كود.",
    descEn: "Client data belongs 100% to the client. We process it, not hold it. PDPL baked into every line of code.",
  },
  {
    icon: "⚡",
    titleAr: "7 أيام أو لا شيء",
    titleEn: "7 Days or Nothing",
    descAr: "Sprint 7 أيام يُثبت القيمة أو لا تدفع. السرعة تبني الثقة أكثر من أي عرض.",
    descEn: "7-day Sprint proves value or you don't pay. Speed builds more trust than any proposal.",
  },
];

type Milestone = {
  dateAr: string;
  dateEn: string;
  titleAr: string;
  titleEn: string;
};

const MILESTONES: Milestone[] = [
  {
    dateAr: "أكتوبر 2024",
    dateEn: "October 2024",
    titleAr: "تأسيس Dealix — الفكرة والبنية الأولى",
    titleEn: "Dealix founded — concept and initial architecture",
  },
  {
    dateAr: "يناير 2025",
    dateEn: "January 2025",
    titleAr: "إطلاق Sprint الأول — أول عميل مدفوع",
    titleEn: "First Sprint launched — first paid client",
  },
  {
    dateAr: "مارس 2025",
    dateEn: "March 2025",
    titleAr: "منظومة Proof Pack — توثيق النتائج بشكل منهجي",
    titleEn: "Proof Pack system — systematic results documentation",
  },
  {
    dateAr: "يونيو 2025",
    dateEn: "June 2025",
    titleAr: "Managed Ops — أول عملاء بعقود شهرية",
    titleEn: "Managed Ops — first monthly retainer clients",
  },
  {
    dateAr: "ديسمبر 2025",
    dateEn: "December 2025",
    titleAr: "PDPL/ZATCA Native — امتثال كامل مضمّن في المنتج",
    titleEn: "PDPL/ZATCA Native — full compliance baked into the product",
  },
  {
    dateAr: "2026",
    dateEn: "2026",
    titleAr: "Custom AI — حلول AI مخصصة للشركات السعودية الكبيرة",
    titleEn: "Custom AI — tailored AI solutions for large Saudi enterprises",
  },
];

/* ─── Component ─────────────────────────────────────────────────── */

export function TeamPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <div className="space-y-16" dir={isAr ? "rtl" : "ltr"}>

      {/* ── Hero ── */}
      <header className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2">
          {isAr ? "عن Dealix" : "About Dealix"}
        </p>
        <h1 className="text-4xl font-bold leading-tight">
          {isAr
            ? "منصة تشغيل الإيرادات الأولى في السعودية المبنية على الحوكمة"
            : "Saudi Arabia's First Governance-First Revenue Operations Platform"}
        </h1>
        <p className="mt-5 text-muted-foreground text-lg leading-relaxed max-w-3xl">
          {isAr
            ? "بنينا Dealix لأننا رأينا شركات سعودية رائعة تخسر عملاء ليس بسبب ضعف المنتج — بل بسبب ضعف تشغيل الإيرادات. الأدوات الموجودة إما معقدة جداً، أو غير ملائمة للسياق السعودي (PDPL، ZATCA، العربية)."
            : "We built Dealix because we saw great Saudi companies losing clients not because of weak products — but because of weak revenue operations. Existing tools are either too complex or not built for the Saudi context (PDPL, ZATCA, Arabic)."}
        </p>
      </header>

      {/* ── Mission ── */}
      <div className="rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] text-white p-8 md:p-10">
        <p className="text-xs font-semibold uppercase tracking-widest text-white/50 mb-3">
          {isAr ? "رسالتنا" : "Our Mission"}
        </p>
        <blockquote className="text-2xl md:text-3xl font-semibold leading-snug">
          {isAr
            ? '"تمكين كل شركة B2B سعودية من تحويل بياناتها إلى إيرادات متكررة — بشفافية تامة وامتثال كامل."'
            : '"Empower every Saudi B2B company to convert their data into recurring revenue — with full transparency and complete compliance."'}
        </blockquote>
      </div>

      {/* ── Values ── */}
      <section>
        <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-6">
          {isAr ? "قيمنا الجوهرية" : "Core Values"}
        </p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {VALUES.map((v) => (
            <div
              key={v.titleEn}
              className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-2 hover:border-border hover:shadow-sm transition-all"
            >
              <span className="text-2xl">{v.icon}</span>
              <h3 className="font-semibold text-sm">{isAr ? v.titleAr : v.titleEn}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {isAr ? v.descAr : v.descEn}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Team ── */}
      <section>
        <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-6">
          {isAr ? "الفريق" : "The Team"}
        </p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {TEAM.map((member) => (
            <div
              key={member.name}
              className="rounded-xl border border-border/60 bg-card/50 p-6 flex flex-col gap-4"
            >
              <div className="flex items-center gap-4">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold flex-shrink-0 ${member.color}`}
                >
                  {member.initials}
                </div>
                <div>
                  <p className="font-semibold text-sm">{member.name}</p>
                  <p className="text-xs text-muted-foreground">
                    {isAr ? member.titleAr : member.titleEn}
                  </p>
                </div>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {isAr ? member.bioAr : member.bioEn}
              </p>
            </div>
          ))}

          {/* Hiring card */}
          <div className="rounded-xl border border-dashed border-border/60 bg-card/20 p-6 flex flex-col gap-3 justify-center items-center text-center">
            <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center text-xl">
              +
            </div>
            <p className="font-semibold text-sm">
              {isAr ? "نحن نبحث عنك" : "We're Looking for You"}
            </p>
            <p className="text-xs text-muted-foreground">
              {isAr
                ? "Customer Success، Sales، Engineering — الرياض أو عن بُعد"
                : "Customer Success, Sales, Engineering — Riyadh or Remote"}
            </p>
            <Link
              href={`${base}/dealix-diagnostic`}
              className="text-xs text-[#C9974B] hover:underline font-medium"
            >
              {isAr ? "تواصل معنا" : "Get in Touch"}
            </Link>
          </div>
        </div>
      </section>

      {/* ── Milestones ── */}
      <section>
        <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-6">
          {isAr ? "رحلتنا" : "Our Journey"}
        </p>
        <div className="relative">
          <div className="absolute top-0 bottom-0 start-5 w-px bg-border/60" aria-hidden />
          <ol className="space-y-6 ps-12">
            {MILESTONES.map((m, i) => (
              <li key={i} className="relative">
                <div className="absolute -start-7 w-4 h-4 rounded-full border-2 border-[#C9974B] bg-background top-1" />
                <p className="text-xs text-muted-foreground mb-0.5">
                  {isAr ? m.dateAr : m.dateEn}
                </p>
                <p className="text-sm font-medium">{isAr ? m.titleAr : m.titleEn}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* ── CTA ── */}
      <div className="rounded-xl border border-border/60 bg-card/50 p-6 flex flex-wrap gap-4 items-center justify-between">
        <div>
          <p className="font-semibold">
            {isAr ? "مستعد لتجربة Dealix؟" : "Ready to try Dealix?"}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            {isAr
              ? "ابدأ بتشخيص مجاني — 30 دقيقة تُظهر أين تتسرب إيراداتك."
              : "Start with a free diagnostic — 30 minutes shows where your revenue leaks."}
          </p>
        </div>
        <Link
          href={`${base}/dealix-diagnostic`}
          className="inline-flex items-center rounded-lg bg-[#C9974B] text-[#0A1628] px-5 py-2.5 text-sm font-semibold hover:bg-[#b8863a] transition-colors"
        >
          {isAr ? "تشخيص مجاني" : "Free Diagnostic"}
        </Link>
      </div>
    </div>
  );
}
