"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const SECTORS_AR = [
  "B2B / خدمات",
  "استشارات هندسية",
  "تقنية / SaaS",
  "رعاية صحية",
  "لوجستيات",
  "تدريب",
  "عقارات",
  "تجزئة / تجارة إلكترونية",
  "مواد غذائية",
  "أخرى",
] as const;

const SECTORS_EN = [
  "B2B / Services",
  "Engineering Consulting",
  "Technology / SaaS",
  "Healthcare",
  "Logistics",
  "Training",
  "Real Estate",
  "Retail / E-Commerce",
  "Food & Beverage",
  "Other",
] as const;

const PAIN_POINTS_AR = [
  "إيراد ضائع / فرص غير مُغلقة",
  "CRM غير منظم أو غير مُستخدم",
  "AI بدون حوكمة أو مسؤولية",
  "إيصالات ZATCA غير مُؤتمتة",
  "فجوة في امتثال PDPL",
  "تقارير يدوية تستهلك وقتاً",
] as const;

const PAIN_POINTS_EN = [
  "Revenue leakage / unclosed opportunities",
  "CRM disorganised or unused",
  "AI tools without governance",
  "ZATCA invoices not automated",
  "PDPL compliance gap",
  "Manual reporting consuming time",
] as const;

const STEPS_AR = [
  { icon: "①", title: "أخبرنا عن شركتك", desc: "الاسم، القطاع، التحدي الرئيسي" },
  { icon: "②", title: "نحلّل في ٧ دقائق", desc: "مسارات الإيراد + جودة البيانات + جاهزية AI" },
  { icon: "③", title: "تحصل على Proof Pack", desc: "٣ قرارات محكومة + تقرير بالعربية والإنجليزية" },
  { icon: "④", title: "قرار مدروس", desc: "Sprint 499 ر.س أو Retainer شهري" },
] as const;

const STEPS_EN = [
  { icon: "①", title: "Tell us about your company", desc: "Name, sector, main challenge" },
  { icon: "②", title: "We analyse in 7 minutes", desc: "Revenue flows + data quality + AI readiness" },
  { icon: "③", title: "You get a Proof Pack", desc: "3 governed decisions + bilingual report" },
  { icon: "④", title: "An informed decision", desc: "499 SAR Sprint or monthly Retainer" },
] as const;

const ZATCA_DEADLINE = "30 يونيو 2026 — ZATCA Wave 24";
const ZATCA_DEADLINE_EN = "June 30, 2026 — ZATCA Wave 24";

export function DealixDiagnosticLanding() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [companyName, setCompanyName] = useState("");
  const [sector, setSector] = useState("");
  const [painPoint, setPainPoint] = useState("");
  const [sectorMatch, setSectorMatch] = useState<string | null>(null);
  const nameInputRef = useRef<HTMLInputElement>(null);

  // Instant sector match preview when typing a company name
  useEffect(() => {
    if (companyName.length < 2) {
      setSectorMatch(null);
      return;
    }
    const lower = companyName.toLowerCase();
    if (lower.includes("clinic") || lower.includes("طب") || lower.includes("مستشف") || lower.includes("عياد")) {
      setSectorMatch(isAr ? "رعاية صحية — PDPL + ZATCA عاجل" : "Healthcare — PDPL + ZATCA urgent");
    } else if (lower.includes("tech") || lower.includes("تقن") || lower.includes("saas")) {
      setSectorMatch(isAr ? "تقنية — CRM gap شائع" : "Technology — CRM gap common");
    } else if (lower.includes("logistic") || lower.includes("شحن") || lower.includes("نقل")) {
      setSectorMatch(isAr ? "لوجستيات — invoice automation" : "Logistics — invoice automation");
    } else if (lower.includes("مطعم") || lower.includes("food") || lower.includes("بيت")) {
      setSectorMatch(isAr ? "مواد غذائية — ZATCA Wave 24 عاجل" : "F&B — ZATCA Wave 24 urgent");
    } else if (lower.includes("استشار") || lower.includes("consult")) {
      setSectorMatch(isAr ? "استشارات — revenue leakage شائع" : "Consulting — revenue leakage common");
    } else {
      setSectorMatch(null);
    }
  }, [companyName, isAr]);

  const sectors = isAr ? SECTORS_AR : SECTORS_EN;
  const painPoints = isAr ? PAIN_POINTS_AR : PAIN_POINTS_EN;
  const steps = isAr ? STEPS_AR : STEPS_EN;

  const formReady = companyName.trim().length >= 2 && sector && painPoint;

  const diagnosticHref = formReady
    ? `/${locale}/risk-score?company=${encodeURIComponent(companyName)}&sector=${encodeURIComponent(sector)}&pain=${encodeURIComponent(painPoint)}`
    : `/${locale}/risk-score`;

  return (
    <div className="space-y-10 max-w-3xl" dir={isAr ? "rtl" : "ltr"}>
      {/* Hero */}
      <header className={isAr ? "text-right" : "text-left"}>
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <Badge variant="destructive" className="text-xs font-medium animate-pulse">
            {isAr ? ZATCA_DEADLINE : ZATCA_DEADLINE_EN}
          </Badge>
          <Badge variant="outline" className="text-xs">
            {isAr ? "PDPL مُفعَّل ٤٨ مخالفة ٢٠٢٥-٢٠٢٦" : "PDPL — 48 violations 2025-2026"}
          </Badge>
        </div>
        <h1 className="text-3xl font-bold tracking-tight leading-snug">
          {isAr
            ? "تشخيص ٧ أيام — أين يضيع إيرادك؟"
            : "7-Day Diagnostic — Where Is Your Revenue Leaking?"}
        </h1>
        <p className="mt-3 text-muted-foreground leading-relaxed max-w-2xl">
          {isAr
            ? "نحلّل مسارات إيرادك، جودة CRM، وجاهزية AI — ثم نعطيك ٣ قرارات قابلة للتنفيذ فوراً مع Proof Pack بالعربية والإنجليزية."
            : "We analyse your revenue flows, CRM quality, and AI readiness — then give you 3 immediately actionable decisions with a bilingual Proof Pack."}
        </p>
      </header>

      {/* 4-Step Process */}
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {steps.map((step) => (
          <Card key={step.icon} className="p-4 text-center border-border/60">
            <p className="text-2xl font-bold text-primary">{step.icon}</p>
            <p className="mt-1 text-sm font-semibold">{step.title}</p>
            <p className="mt-1 text-xs text-muted-foreground leading-tight">{step.desc}</p>
          </Card>
        ))}
      </div>

      {/* Interactive Form */}
      <Card className="p-6 border-primary/20 bg-card/60">
        <h2 className="text-lg font-semibold mb-4">
          {isAr ? "ابدأ تشخيصك المجاني" : "Start Your Free Diagnostic"}
        </h2>
        <div className="space-y-4">
          {/* Company Name */}
          <div>
            <label className="text-sm font-medium text-foreground/80 block mb-1">
              {isAr ? "اسم الشركة" : "Company Name"}
            </label>
            <div className="relative">
              <input
                ref={nameInputRef}
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder={isAr ? "مثال: شركة النور للتقنية" : "e.g. Al-Nour Technology"}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                dir={isAr ? "rtl" : "ltr"}
              />
              {sectorMatch && (
                <p className="mt-1 text-xs text-primary/80 font-medium">
                  {isAr ? "✓ تطابق: " : "✓ Match: "}{sectorMatch}
                </p>
              )}
            </div>
          </div>

          {/* Sector */}
          <div>
            <label className="text-sm font-medium text-foreground/80 block mb-1">
              {isAr ? "القطاع" : "Sector"}
            </label>
            <select
              value={sector}
              onChange={(e) => setSector(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              dir={isAr ? "rtl" : "ltr"}
            >
              <option value="">{isAr ? "اختر القطاع..." : "Choose sector..."}</option>
              {sectors.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* Pain Point */}
          <div>
            <label className="text-sm font-medium text-foreground/80 block mb-1">
              {isAr ? "التحدي الرئيسي" : "Main Challenge"}
            </label>
            <select
              value={painPoint}
              onChange={(e) => setPainPoint(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              dir={isAr ? "rtl" : "ltr"}
            >
              <option value="">{isAr ? "اختر التحدي..." : "Choose challenge..."}</option>
              {painPoints.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <Button asChild size="lg" className="w-full" disabled={!formReady}>
            <Link href={diagnosticHref}>
              {isAr ? "ابدأ التشخيص المجاني ←" : "Start Free Diagnostic →"}
            </Link>
          </Button>
          <p className="text-xs text-muted-foreground text-center">
            {isAr
              ? "لا ائتمان مطلوب · لا إرسال آلي · النتائج خلال ٧ دقائق"
              : "No credit card · No automated outreach · Results in 7 minutes"}
          </p>
        </div>
      </Card>

      {/* Social Proof + Urgency */}
      <div className="grid gap-3 md:grid-cols-2">
        <Card className="p-4 border-orange-200 bg-orange-50 dark:bg-orange-950/20">
          <p className="text-xs font-semibold text-orange-700 dark:text-orange-400 uppercase tracking-wide mb-1">
            {isAr ? "إلزامي — ZATCA Wave 24" : "Mandatory — ZATCA Wave 24"}
          </p>
          <p className="text-sm text-foreground/80">
            {isAr
              ? "كل شركة بإيراد أكثر من ٣٧٥ ألف ر.س ملزمة بالفاتورة الإلكترونية قبل ٣٠ يونيو ٢٠٢٦."
              : "Every company above SAR 375K revenue must comply with e-invoicing by June 30, 2026."}
          </p>
        </Card>
        <Card className="p-4 border-blue-200 bg-blue-50 dark:bg-blue-950/20">
          <p className="text-xs font-semibold text-blue-700 dark:text-blue-400 uppercase tracking-wide mb-1">
            {isAr ? "سوق الذكاء الاصطناعي السعودي" : "Saudi AI Market"}
          </p>
          <p className="text-sm text-foreground/80">
            {isAr
              ? "$١٣.٣ مليار في ٢٠٢٦ (CAGR 32.87%). ٢٠٢٦ = عام الذكاء الاصطناعي (SDAIA)."
              : "$13.3B in 2026 (CAGR 32.87%). 2026 declared Year of AI by SDAIA."}
          </p>
        </Card>
      </div>

      {/* Secondary CTAs */}
      <div className="flex flex-wrap gap-3">
        <Button asChild variant="outline" size="sm">
          <Link href={`/${locale}/offer/lead-intelligence-sprint`}>
            {isAr ? "Sprint 499 ر.س — ابدأ الآن" : "Sprint 499 SAR — Start Now"}
          </Link>
        </Button>
        <Button asChild variant="ghost" size="sm">
          <Link href={`/${locale}/business-now`}>
            {isAr ? "ديمو مباشر" : "Live Demo"}
          </Link>
        </Button>
      </div>

      <p className="text-xs text-muted-foreground max-w-2xl">
        {isAr
          ? "لا إرسال خارجي آلي · لا ادّعاء إيراد قبل الدفع · امتثال PDPL كامل"
          : "No automated outbound · No revenue claims before payment · Full PDPL compliance"}
      </p>
    </div>
  );
}
