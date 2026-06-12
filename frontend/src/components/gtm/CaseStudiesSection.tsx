"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

/* ─── Data ──────────────────────────────────────────────
 * Case studies MUST be real and consented before they appear here.
 * Doctrine (non-negotiables #4 / #5 / #10): no fake or un-sourced claims,
 * no guaranteed outcomes, every project carries a Proof Pack. This array
 * stays EMPTY until a delivered engagement with a signed Proof Pack and
 * recorded source_ref exists and the customer consents to publish.
 * ──────────────────────────────────────────────────────── */

type CaseStudy = {
  id: string;
  sector: { ar: string; en: string };
  sectorTag: { ar: string; en: string };
  challenge: { ar: string; en: string };
  solution: { ar: string; en: string };
  metric: { ar: string; en: string };
  metricLabel: { ar: string; en: string };
  quote: { ar: string; en: string };
  author: { ar: string; en: string };
  tagColor: string;
};

const CASE_STUDIES: CaseStudy[] = [];

/* ─── Component ─────────────────────────────────────── */

interface CaseStudiesSectionProps {
  className?: string;
}

export function CaseStudiesSection({ className = "" }: CaseStudiesSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <section
      className={`space-y-10 ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Header */}
      <div className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-[#D4AF37] uppercase tracking-wide mb-2">
          {isAr ? "قصص نجاح" : "Success Stories"}
        </p>
        <h2 className="text-3xl font-bold">
          {isAr ? "نتائج موثّقة من شركات سعودية" : "Documented Results from Saudi Companies"}
        </h2>
      </div>

      {CASE_STUDIES.length === 0 ? (
        /* Honest empty state — no fabricated case studies. */
        <Card className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-dashed border-border/60 bg-card/40 px-6 py-6">
          <div className={isAr ? "text-right" : "text-left"}>
            <p className="text-base font-semibold text-foreground">
              {isAr
                ? "قصص النجاح الموثّقة قيد الإنشاء."
                : "Documented success stories are in the making."}
            </p>
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed max-w-xl">
              {isAr
                ? "لا نعرض نتائج ملفّقة. كل قصة هنا ستكون من مشروع فعلي مع Proof Pack موقّع ومصدر مسجّل وبموافقة العميل. ابدأ بالتشخيص المجاني وكن أول قصة."
                : "We do not display fabricated results. Each story here will come from a real engagement with a signed Proof Pack, recorded source, and customer consent. Start with the free diagnostic and be the first story."}
            </p>
          </div>
          <Button asChild size="sm" className="bg-[#D4AF37] text-[#001F3F] hover:bg-[#c4a032] font-semibold whitespace-nowrap">
            <Link href={`${base}/dealix-diagnostic`}>
              {isAr ? "ابدأ التشخيص" : "Start Diagnostic"}
            </Link>
          </Button>
        </Card>
      ) : (
        <>
          {/* Case Study Cards */}
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {CASE_STUDIES.map((cs) => (
              <Card
                key={cs.id}
                className="flex flex-col border-border/60 bg-card/50 overflow-hidden hover:shadow-md transition-shadow"
              >
                {/* Sector header */}
                <div className="bg-[#001F3F] px-5 py-4">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-white/80 text-sm font-medium">
                      {isAr ? cs.sector.ar : cs.sector.en}
                    </p>
                    <Badge className={`text-xs ${cs.tagColor}`}>
                      {isAr ? cs.sectorTag.ar : cs.sectorTag.en}
                    </Badge>
                  </div>
                  {/* Metric highlight */}
                  <div className="mt-3 flex items-baseline gap-2">
                    <span className="text-4xl font-bold text-[#D4AF37]">
                      {isAr ? cs.metric.ar : cs.metric.en}
                    </span>
                    <span className="text-white/60 text-sm">
                      {isAr ? cs.metricLabel.ar : cs.metricLabel.en}
                    </span>
                  </div>
                </div>

                {/* Body */}
                <div className={`flex flex-col flex-1 p-5 space-y-4 ${isAr ? "text-right" : "text-left"}`}>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">
                      {isAr ? "التحدي" : "Challenge"}
                    </p>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {isAr ? cs.challenge.ar : cs.challenge.en}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">
                      {isAr ? "الحل" : "Solution"}
                    </p>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {isAr ? cs.solution.ar : cs.solution.en}
                    </p>
                  </div>

                  {/* Quote */}
                  <blockquote className="border-s-2 border-[#D4AF37] ps-3 flex-1">
                    <p className="text-sm italic text-foreground leading-relaxed">
                      "{isAr ? cs.quote.ar : cs.quote.en}"
                    </p>
                    <p className="mt-2 text-xs text-muted-foreground">
                      — {isAr ? cs.author.ar : cs.author.en}
                    </p>
                  </blockquote>
                </div>
              </Card>
            ))}
          </div>

          {/* Disclaimer + CTA */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-xl border border-border/60 bg-card/30 px-6 py-4">
            <p className="text-xs text-muted-foreground max-w-lg">
              {isAr
                ? "نتائج من مشاريع حقيقية. الأدلة تُسلَّم في Proof Pack. الأسماء مُخفاة بموافقة أصحابها."
                : "Results from real projects. Evidence delivered in Proof Pack. Names anonymized with owner consent."}
            </p>
            <Button asChild size="sm" className="bg-[#D4AF37] text-[#001F3F] hover:bg-[#c4a032] font-semibold whitespace-nowrap">
              <Link href={`${base}/dealix-diagnostic`}>
                {isAr ? "ابدأ التشخيص" : "Start Diagnostic"}
              </Link>
            </Button>
          </div>
        </>
      )}
    </section>
  );
}
