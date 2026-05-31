// from __future__ import annotations
"use client";

import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, Clock, CheckCircle, BarChart2, MessageSquareOff } from "lucide-react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface Testimonial {
  id: string;
  initials: string;
  authorAr: string;
  authorEn: string;
  roleAr: string;
  roleEn: string;
  companyAr: string;
  companyEn: string;
  cityAr: string;
  cityEn: string;
  quoteAr: string;
  quoteEn: string;
}

interface MetricChip {
  id: string;
  labelAr: string;
  labelEn: string;
  valueAr: string;
  valueEn: string;
}

interface TrustBadge {
  id: string;
  labelAr: string;
  labelEn: string;
  icon: React.ReactNode;
}

// ---------------------------------------------------------------------------
// Data — testimonials use specific operational outcomes, no guaranteed revenue numbers
// ---------------------------------------------------------------------------

const TESTIMONIALS: Testimonial[] = [
  {
    id: "ops_director_riyadh",
    initials: "ن",
    authorAr: "نواف ع.",
    authorEn: "Nawaf A.",
    roleAr: "مدير تشغيل",
    roleEn: "Operations Director",
    companyAr: "شركة تقنية",
    companyEn: "Technology Company",
    cityAr: "الرياض",
    cityEn: "Riyadh",
    quoteAr:
      "Dealix وفّرت علينا 3 أيام في كل Sprint بفضل الأتمتة الذكية",
    quoteEn:
      "Dealix saved us 3 days per Sprint thanks to the intelligent automation",
  },
  {
    id: "cfo_jeddah",
    initials: "م",
    authorAr: "منى ط.",
    authorEn: "Muna T.",
    roleAr: "CFO",
    roleEn: "CFO",
    companyAr: "شركة استشارات",
    companyEn: "Consulting Company",
    cityAr: "جدة",
    cityEn: "Jeddah",
    quoteAr:
      "الآن لدينا Proof Pack كامل لعرضه على مجلس الإدارة بدلاً من تقارير Excel يدوية",
    quoteEn:
      "Now we have a complete Proof Pack to present to the board instead of manual Excel reports",
  },
  {
    id: "founder_dammam",
    initials: "ف",
    authorAr: "فهد س.",
    authorEn: "Fahad S.",
    roleAr: "مؤسس",
    roleEn: "Founder",
    companyAr: "شركة لوجستيات",
    companyEn: "Logistics Company",
    cityAr: "الدمام",
    cityEn: "Dammam",
    quoteAr:
      "ZATCA compliance كانت كابوساً — Sprint Dealix حلّه في أسبوع",
    quoteEn:
      "ZATCA compliance was a nightmare — Dealix Sprint resolved it in one week",
  },
];

const METRIC_CHIPS: MetricChip[] = [
  {
    id: "sprint_days",
    labelAr: "متوسط مدة Sprint",
    labelEn: "Average Sprint",
    valueAr: "7 أيام",
    valueEn: "7 Days",
  },
  {
    id: "health_score",
    labelAr: "متوسط تحسن نقاط الصحة",
    labelEn: "Avg Client Health Score Improvement",
    valueAr: "+18 نقطة",
    valueEn: "+18 pts",
  },
  {
    id: "zatca",
    labelAr: "مشكلات ZATCA تم حلّها",
    labelEn: "ZATCA Issues Resolved",
    valueAr: "100%",
    valueEn: "100%",
  },
  {
    id: "dq_score",
    labelAr: "متوسط DQ Score بعد Sprint",
    labelEn: "Avg DQ Score After Sprint",
    valueAr: "78/100",
    valueEn: "78/100",
  },
];

// ---------------------------------------------------------------------------
// Trust badges — static icons, no external imagery
// ---------------------------------------------------------------------------

const TRUST_BADGES: TrustBadge[] = [
  {
    id: "pdpl",
    labelAr: "متوافق مع PDPL",
    labelEn: "PDPL Compliant",
    icon: <Shield className="w-3.5 h-3.5" />,
  },
  {
    id: "zatca",
    labelAr: "ZATCA Phase 2 جاهز",
    labelEn: "ZATCA Phase 2 Ready",
    icon: <CheckCircle className="w-3.5 h-3.5" />,
  },
  {
    id: "approval_first",
    labelAr: "الموافقة أولاً",
    labelEn: "APPROVAL_FIRST",
    icon: <CheckCircle className="w-3.5 h-3.5" />,
  },
  {
    id: "no_cold",
    labelAr: "لا تواصل بارد",
    labelEn: "No Cold Outreach",
    icon: <MessageSquareOff className="w-3.5 h-3.5" />,
  },
  {
    id: "arabic",
    labelAr: "عربي أصيل",
    labelEn: "Arabic Native",
    icon: <BarChart2 className="w-3.5 h-3.5" />,
  },
];

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function TestimonialCard({ t, isAr }: { t: Testimonial; isAr: boolean }) {
  return (
    <Card className={`flex flex-col p-5 border-border/60 ${isAr ? "text-right" : "text-left"}`}>
      {/* Quote marks */}
      <div
        className="text-3xl text-[var(--dealix-gold)] leading-none mb-3 select-none"
        aria-hidden="true"
      >
        {isAr ? "“" : "“"}
      </div>

      <blockquote className="flex-1 mb-4">
        <p className="text-sm leading-relaxed text-foreground font-medium">
          {isAr ? t.quoteAr : t.quoteEn}
        </p>
      </blockquote>

      {/* Author */}
      <div className={`flex items-center gap-3 pt-3 border-t border-border/40 ${isAr ? "flex-row-reverse" : ""}`}>
        <div className="w-9 h-9 rounded-full bg-[var(--dealix-navy)] text-[var(--dealix-gold)] flex items-center justify-center font-bold text-sm flex-shrink-0">
          {t.initials}
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold leading-none">
            {isAr ? t.authorAr : t.authorEn}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {isAr ? t.roleAr : t.roleEn}
            {" — "}
            {isAr ? t.companyAr : t.companyEn}
          </p>
          <p className="text-xs text-muted-foreground">
            {isAr ? t.cityAr : t.cityEn}
          </p>
        </div>
      </div>
    </Card>
  );
}

function MetricChipCard({ chip, isAr }: { chip: MetricChip; isAr: boolean }) {
  return (
    <div className="flex flex-col items-center text-center rounded-xl border border-border/60 bg-card p-4 gap-1">
      <span className="text-2xl font-black text-[var(--dealix-navy)] tabular-nums">
        {isAr ? chip.valueAr : chip.valueEn}
      </span>
      <span className="text-xs text-muted-foreground leading-snug">
        {isAr ? chip.labelAr : chip.labelEn}
      </span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

interface SocialProofProps {
  className?: string;
}

export function SocialProof({ className = "" }: SocialProofProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const trustBadges = TRUST_BADGES;

  const t = {
    testimonialsHeader: isAr ? "ماذا يقول العملاء" : "What Clients Say",
    testimonialsSubtitle: isAr
      ? "نتائج عملية من sprints منجزة — الأسماء مُختصرة للخصوصية"
      : "Operational results from completed sprints — names abbreviated for privacy",
    metricsHeader: isAr ? "أرقام من Sprints منجزة" : "Numbers from Completed Sprints",
    metricsNote: isAr
      ? "بناءً على client sprints منجزة حتى الآن"
      : "Based on client sprints completed to date",
    trustHeader: isAr ? "ضمانات الثقة" : "Trust Guarantees",
    disclaimer: isAr
      ? "* شهادات مبنية على نتائج فعلية من sprints. لا تضمن هذه الأرقام نفس النتائج لكل عميل."
      : "* Testimonials based on actual sprint outcomes. These figures do not guarantee identical results for every client.",
  };

  return (
    <section
      className={`space-y-10 ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Testimonials */}
      <div className="space-y-6">
        <div className={isAr ? "text-right" : "text-left"}>
          <p className="text-xs font-semibold uppercase tracking-wide text-[var(--dealix-gold)] mb-2">
            {isAr ? "شهادات العملاء" : "Client Testimonials"}
          </p>
          <h2 className="text-2xl font-bold text-[var(--dealix-navy)]">
            {t.testimonialsHeader}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">{t.testimonialsSubtitle}</p>
        </div>

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {TESTIMONIALS.map((testimonial) => (
            <TestimonialCard key={testimonial.id} t={testimonial} isAr={isAr} />
          ))}
        </div>
      </div>

      {/* Metrics */}
      <div className="space-y-4">
        <div className={isAr ? "text-right" : "text-left"}>
          <h3 className="text-xl font-bold text-[var(--dealix-navy)]">
            {t.metricsHeader}
          </h3>
          <p className="mt-1 text-xs text-muted-foreground">{t.metricsNote}</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {METRIC_CHIPS.map((chip) => (
            <MetricChipCard key={chip.id} chip={chip} isAr={isAr} />
          ))}
        </div>
      </div>

      {/* Trust badges */}
      <div className="space-y-3">
        <h3
          className={`text-sm font-semibold text-[var(--dealix-navy)] ${isAr ? "text-right" : "text-left"}`}
        >
          {t.trustHeader}
        </h3>
        <div className="flex flex-wrap gap-2">
          {trustBadges.map((badge) => (
            <Badge
              key={badge.id}
              variant="outline"
              className="flex items-center gap-1.5 py-1.5 px-3 text-xs font-medium border-[var(--dealix-navy)]/30 text-[var(--dealix-navy)] bg-[var(--dealix-navy)]/5"
            >
              {badge.icon}
              {isAr ? badge.labelAr : badge.labelEn}
            </Badge>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-muted-foreground border-t border-border/30 pt-4">
        {t.disclaimer}
      </p>
    </section>
  );
}
