// from __future__ import annotations
"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Check, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PricingFeature {
  ar: string;
  en: string;
}

interface PricingTier {
  id: string;
  mostPopular: boolean;
  approvalFirstBadge: boolean;
  label: { ar: string; en: string };
  subtitle: { ar: string; en: string };
  price: { ar: string; en: string };
  period: { ar: string; en: string };
  type: "one-time" | "monthly" | "range";
  features: PricingFeature[];
  cta: { ar: string; en: string };
  href: string;
}

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------

const TIERS: PricingTier[] = [
  {
    id: "free_diagnostic",
    mostPopular: false,
    approvalFirstBadge: false,
    label: { ar: "التشخيص المجاني", en: "Free Diagnostic" },
    subtitle: {
      ar: "مكالمة 30 دقيقة — بدون التزام",
      en: "30-min call — no commitment",
    },
    price: { ar: "0", en: "0" },
    period: { ar: "ر.س", en: "SAR" },
    type: "one-time",
    features: [
      { ar: "مكالمة استراتيجية 30 دقيقة", en: "30-minute strategy call" },
      { ar: "تقييم المخاطر الأولي", en: "Initial risk assessment" },
      { ar: "نتائج موثّقة ثنائية اللغة", en: "Bilingual documented findings" },
      { ar: "توصية بالمسار المناسب", en: "Path recommendation" },
      { ar: "بدون التزام", en: "No commitment required" },
    ],
    cta: { ar: "ابدأ مجاناً", en: "Start Free" },
    href: "/risk-score",
  },
  {
    id: "revenue_sprint",
    mostPopular: false,
    approvalFirstBadge: true,
    label: { ar: "Revenue Sprint", en: "Revenue Sprint" },
    subtitle: {
      ar: "DQ score + تسجيل الحساب + مسودة الدليل + Proof Pack",
      en: "DQ score, account scoring, draft pack, proof pack",
    },
    price: { ar: "499", en: "499" },
    period: { ar: "ر.س / 7 أيام", en: "SAR / 7 days" },
    type: "one-time",
    features: [
      { ar: "DQ Score (1-100) لبياناتك", en: "DQ Score (1-100) for your data" },
      { ar: "تسجيل وتصنيف الحسابات", en: "Account scoring and classification" },
      { ar: "مسودة Proof Pack (3 leads)", en: "Proof Pack draft (3 leads)" },
      { ar: "Proof Pack كامل محكوم", en: "Full governed Proof Pack" },
      { ar: "تحليل ZATCA/PDPL", en: "ZATCA/PDPL analysis" },
    ],
    cta: { ar: "ابدأ Sprint", en: "Start Sprint" },
    href: "/dealix-diagnostic",
  },
  {
    id: "data_pack",
    mostPopular: false,
    approvalFirstBadge: true,
    label: { ar: "Data Pack — حزمة البيانات", en: "Data Pack" },
    subtitle: {
      ar: "30 يوماً من خط بيانات + 3 أشهر لوحات تحكم",
      en: "30-day data pipeline + 3 months of dashboards",
    },
    price: { ar: "1,500", en: "1,500" },
    period: { ar: "ر.س", en: "SAR" },
    type: "one-time",
    features: [
      { ar: "خط بيانات نشط لمدة 30 يوماً", en: "Active data pipeline for 30 days" },
      { ar: "لوحات تحكم لمدة 3 أشهر", en: "Dashboards for 3 months" },
      { ar: "Source Passport لكل مصدر بيانات", en: "Source Passport for every data source" },
      { ar: "تقارير PDPL محكومة", en: "PDPL-governed reports" },
      { ar: "دعم التكامل مع أنظمتك", en: "Integration support for your systems" },
    ],
    cta: { ar: "احصل على Data Pack", en: "Get Data Pack" },
    href: "/dealix-diagnostic",
  },
  {
    id: "managed_ops",
    mostPopular: true,
    approvalFirstBadge: true,
    label: { ar: "Managed Ops — العمليات المُدارة", en: "Managed Ops" },
    subtitle: {
      ar: "نقاط صحة شهرية + مراقبة ZATCA/PDPL + تقارير أسبوعية",
      en: "Monthly health scores, ZATCA/PDPL monitoring, weekly reports",
    },
    price: { ar: "2,999 – 4,999", en: "2,999 – 4,999" },
    period: { ar: "ر.س / شهر", en: "SAR / month" },
    type: "range",
    features: [
      { ar: "نقاط صحة العميل شهرياً", en: "Monthly client health scores" },
      { ar: "مراقبة ZATCA و PDPL", en: "ZATCA & PDPL monitoring" },
      { ar: "تقارير أسبوعية مُحكمة", en: "Governed weekly reports" },
      { ar: "Proof Pack شهري", en: "Monthly Proof Pack" },
      { ar: "دعم ذو أولوية", en: "Priority support" },
    ],
    cta: { ar: "ابدأ Managed Ops", en: "Start Managed Ops" },
    href: "/dealix-diagnostic",
  },
  {
    id: "custom_ai",
    mostPopular: false,
    approvalFirstBadge: true,
    label: { ar: "Custom AI — ذكاء اصطناعي مخصص", en: "Custom AI" },
    subtitle: {
      ar: "نموذج AI مخصص + تكاملات مخصصة + عمليات مخصصة",
      en: "Bespoke AI model, custom integrations, dedicated ops",
    },
    price: { ar: "5,000 – 25,000", en: "5,000 – 25,000" },
    period: { ar: "ر.س", en: "SAR" },
    type: "range",
    features: [
      { ar: "نموذج AI مدرّب على بياناتك", en: "AI model trained on your data" },
      { ar: "تكاملات مخصصة مع أنظمتك", en: "Custom integrations with your systems" },
      { ar: "فريق عمليات مخصص", en: "Dedicated operations team" },
      { ar: "Proof Pack مُخصّص ومحكوم", en: "Bespoke governed Proof Pack" },
      { ar: "SLA مضمون", en: "Guaranteed SLA" },
    ],
    cta: { ar: "احجز استشارة", en: "Book Consultation" },
    href: "/dealix-diagnostic",
  },
];

// ---------------------------------------------------------------------------
// Href builder helper
// ---------------------------------------------------------------------------

function buildHref(locale: string, path: string): string {
  return `/${locale}${path}`;
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

interface PricingCardsProps {
  className?: string;
}

export function PricingCards({ className = "" }: PricingCardsProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const t = {
    header: isAr ? "خطط الأسعار" : "Pricing Plans",
    subtitle: isAr
      ? "ابدأ بالتشخيص المجاني — انتقل إلى Sprint عند الاستعداد. لا ارتباط سنوي."
      : "Start with the free diagnostic — move to Sprint when ready. No annual lock-in.",
    approvalFirstNote: isAr
      ? "جميع الخطط المدفوعة تعمل بمبدأ الموافقة أولاً — لا إرسال تلقائي دون موافقة بشرية."
      : "All paid tiers operate under APPROVAL_FIRST — no automated sends without human approval.",
  };

  return (
    <section
      className={`space-y-8 ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Header */}
      <div className={`space-y-2 ${isAr ? "text-right" : "text-left"}`}>
        <h2 className="text-2xl font-bold text-[var(--dealix-navy)]">{t.header}</h2>
        <p className="text-sm text-muted-foreground max-w-2xl">{t.subtitle}</p>
      </div>

      {/* Approval-first notice */}
      <div className="flex items-start gap-2 rounded-xl border border-[var(--dealix-navy)]/20 bg-[var(--dealix-navy)]/5 px-4 py-3 text-sm text-[var(--dealix-navy)]">
        <Shield className="w-4 h-4 flex-shrink-0 mt-0.5" aria-hidden="true" />
        <span>{t.approvalFirstNote}</span>
      </div>

      {/* Cards grid */}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {TIERS.map((tier) => (
          <PricingCardInner key={tier.id} tier={tier} isAr={isAr} locale={locale} />
        ))}
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Inner card — receives locale via prop to avoid conditional hook calls
// ---------------------------------------------------------------------------

interface PricingCardInnerProps {
  tier: PricingTier;
  isAr: boolean;
  locale: string;
}

function PricingCardInner({ tier, isAr, locale }: PricingCardInnerProps) {
  const t = {
    mostPopular: isAr ? "الأكثر طلباً" : "Most Popular",
    approvalFirst: isAr ? "الموافقة أولاً" : "APPROVAL_FIRST",
    free: isAr ? "مجاني" : "Free",
  };

  const priceDisplay =
    tier.price.ar === "0"
      ? t.free
      : isAr
      ? tier.price.ar
      : tier.price.en;

  return (
    <div
      className={`relative flex flex-col rounded-2xl border p-6 gap-5 transition-shadow hover:shadow-md ${
        tier.mostPopular
          ? "border-[var(--dealix-gold)] shadow-md shadow-[var(--dealix-gold)]/20 bg-[var(--dealix-gold)]/5"
          : "border-border bg-card"
      }`}
    >
      {/* Most popular badge */}
      {tier.mostPopular && (
        <div className={`absolute -top-3 ${isAr ? "left-4" : "right-4"}`}>
          <span className="bg-[var(--dealix-gold)] text-[var(--dealix-navy)] text-xs font-bold px-3 py-1 rounded-full">
            {t.mostPopular}
          </span>
        </div>
      )}

      {/* Header */}
      <div className={`space-y-1 ${isAr ? "text-right" : "text-left"}`}>
        <div className="flex items-start justify-between gap-2 flex-wrap">
          <h3 className="text-base font-bold text-[var(--dealix-navy)]">
            {isAr ? tier.label.ar : tier.label.en}
          </h3>
          {tier.approvalFirstBadge && (
            <Badge
              variant="outline"
              className="flex items-center gap-1 text-xs border-[var(--dealix-navy)]/30 text-[var(--dealix-navy)] bg-[var(--dealix-navy)]/5 flex-shrink-0"
            >
              <Shield className="w-3 h-3" />
              {t.approvalFirst}
            </Badge>
          )}
        </div>
        <p className="text-xs text-muted-foreground">
          {isAr ? tier.subtitle.ar : tier.subtitle.en}
        </p>
      </div>

      {/* Price */}
      <div className={isAr ? "text-right" : "text-left"}>
        <div className="flex items-end gap-1 flex-wrap">
          <span
            className={`text-3xl font-black tabular-nums ${
              tier.mostPopular ? "text-[var(--dealix-gold)]" : "text-[var(--dealix-navy)]"
            }`}
          >
            {priceDisplay}
          </span>
          {tier.price.ar !== "0" && (
            <span className="text-sm text-muted-foreground pb-1">
              {isAr ? tier.period.ar : tier.period.en}
            </span>
          )}
        </div>
      </div>

      {/* Feature list */}
      <ul className="space-y-2 flex-1">
        {tier.features.map((feature, idx) => (
          <li
            key={idx}
            className={`flex items-start gap-2 text-sm ${isAr ? "flex-row-reverse text-right" : ""}`}
          >
            <Check
              className="w-4 h-4 text-[var(--dealix-success)] flex-shrink-0 mt-0.5"
              aria-hidden="true"
            />
            <span>{isAr ? feature.ar : feature.en}</span>
          </li>
        ))}
      </ul>

      {/* CTA */}
      <Button
        asChild
        className={
          tier.mostPopular
            ? "w-full bg-[var(--dealix-gold)] hover:bg-[var(--dealix-gold-hover)] text-[var(--dealix-navy)] font-bold"
            : "w-full bg-[var(--dealix-navy)] hover:bg-[var(--dealix-navy-hover)] text-white font-semibold"
        }
      >
        <Link href={buildHref(locale, tier.href)}>
          {isAr ? tier.cta.ar : tier.cta.en}
        </Link>
      </Button>
    </div>
  );
}
