// from __future__ import annotations
"use client";

import Link from "next/link";
import { useLocale } from "next-intl";

import { ComparisonTable } from "@/components/gtm/ComparisonTable";
import { SocialProof } from "@/components/gtm/SocialProof";
import { ROICalculator } from "@/components/gtm/ROICalculator";
import { PricingCards } from "@/components/gtm/PricingCards";

// ---------------------------------------------------------------------------
// Copy
// ---------------------------------------------------------------------------

const COPY = {
  ar: {
    headerTitle: "لماذا Dealix؟",
    headerSubtitle:
      "نتائج قابلة للقياس، امتثال مدمج، وسعر شفاف — مصمم للسوق السعودي.",
    comparisonHeader: "مقارنة مع البدائل",
    comparisonSubheader:
      "شاهد كيف يختلف Dealix عن منصات CRM الدولية والاستشارات المحلية.",
    socialProofHeader: "ماذا يقول عملاؤنا",
    socialProofSubheader:
      "نتائج حقيقية من شركات سعودية تعمل مع Dealix.",
    roiHeader: "احسب عائد الاستثمار",
    roiSubheader:
      "أدخل أرقامك واكتشف العائد المتوقع خلال 90 يوماً.",
    pricingHeader: "الأسعار",
    pricingSubheader:
      "ابدأ بـ Sprint مجرّب — ادفع فقط عندما ترى النتائج.",
    ctaHeading: "ابدأ بـ Sprint مجاني — أثبت القيمة قبل الدفع",
    ctaSubheading:
      "لا التزامات. نشخّص وضعك ونعطيك خارطة طريق واضحة في 48 ساعة.",
    ctaButton: "ابدأ الآن",
  },
  en: {
    headerTitle: "Why Dealix?",
    headerSubtitle:
      "Measurable outcomes, built-in compliance, transparent pricing — designed for the Saudi market.",
    comparisonHeader: "How We Compare",
    comparisonSubheader:
      "See how Dealix differs from international CRM platforms and local consulting firms.",
    socialProofHeader: "What Our Clients Say",
    socialProofSubheader:
      "Real results from Saudi companies working with Dealix.",
    roiHeader: "Calculate Your ROI",
    roiSubheader:
      "Enter your numbers and see the expected return within 90 days.",
    pricingHeader: "Pricing",
    pricingSubheader:
      "Start with a proven Sprint — pay only when you see results.",
    ctaHeading: "Start with a Free Sprint — Prove Value Before You Pay",
    ctaSubheading:
      "No commitment. We diagnose your situation and deliver a clear roadmap in 48 hours.",
    ctaButton: "Get Started",
  },
};

// ---------------------------------------------------------------------------
// Section header helper
// ---------------------------------------------------------------------------

function SectionHeader({
  heading,
  subheading,
  isAr,
}: {
  heading: string;
  subheading: string;
  isAr: boolean;
}) {
  return (
    <div
      className={`mb-8 ${isAr ? "text-right" : "text-left"}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      <h2 className="text-2xl font-bold text-foreground mb-2">{heading}</h2>
      <p className="text-muted-foreground text-base max-w-2xl">{subheading}</p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page component
// ---------------------------------------------------------------------------

export function WhyDealixPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = isAr ? COPY.ar : COPY.en;

  return (
    <main
      className="min-h-screen bg-background text-foreground"
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Page header */}
      <section className="w-full bg-[var(--dealix-navy)] py-16 px-4">
        <div
          className={`max-w-4xl mx-auto ${isAr ? "text-right" : "text-left"}`}
        >
          <h1 className="text-4xl font-extrabold text-white mb-4">
            {t.headerTitle}
          </h1>
          <p className="text-lg text-white/80 max-w-2xl">{t.headerSubtitle}</p>
        </div>
      </section>

      {/* Comparison section */}
      <section className="w-full py-14 px-4 bg-background">
        <div className="max-w-5xl mx-auto">
          <SectionHeader
            heading={t.comparisonHeader}
            subheading={t.comparisonSubheader}
            isAr={isAr}
          />
          <ComparisonTable />
        </div>
      </section>

      {/* Social proof section */}
      <section className="w-full py-14 px-4 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <SectionHeader
            heading={t.socialProofHeader}
            subheading={t.socialProofSubheader}
            isAr={isAr}
          />
          <SocialProof />
        </div>
      </section>

      {/* ROI calculator section */}
      <section className="w-full py-14 px-4 bg-background">
        <div className="max-w-5xl mx-auto">
          <SectionHeader
            heading={t.roiHeader}
            subheading={t.roiSubheader}
            isAr={isAr}
          />
          <ROICalculator />
        </div>
      </section>

      {/* Pricing section */}
      <section className="w-full py-14 px-4 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <SectionHeader
            heading={t.pricingHeader}
            subheading={t.pricingSubheader}
            isAr={isAr}
          />
          <PricingCards />
        </div>
      </section>

      {/* Final CTA section */}
      <section className="w-full py-20 px-4 bg-[var(--dealix-navy)]">
        <div
          className={`max-w-3xl mx-auto ${isAr ? "text-right" : "text-center"}`}
        >
          <h2 className="text-3xl font-extrabold text-white mb-4">
            {t.ctaHeading}
          </h2>
          <p className="text-white/80 text-lg mb-8">{t.ctaSubheading}</p>
          <Link
            href={`/${locale}/risk-score`}
            className="inline-block bg-white text-[var(--dealix-navy)] font-bold px-8 py-4 rounded-lg text-lg hover:bg-white/90 transition-colors"
          >
            {t.ctaButton}
          </Link>
        </div>
      </section>
    </main>
  );
}
