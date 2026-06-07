"use client";

import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";

/* ─── Data ──────────────────────────────────────────────
 * Testimonials MUST be real, sourced, and consented before they appear here.
 * Doctrine (non-negotiables #4 / #5): no fake or un-sourced claims, no
 * guaranteed outcomes. This array stays EMPTY until a real customer has
 * given written consent to publish an (optionally abbreviated) quote.
 * Add entries only from a signed Proof Pack with a recorded source_ref.
 * ──────────────────────────────────────────────────────── */

type Testimonial = {
  id: string;
  initials: string;
  author: { ar: string; en: string };
  role: { ar: string; en: string };
  company: { ar: string; en: string };
  sector: { ar: string; en: string };
  quote: { ar: string; en: string };
  metric: { ar: string; en: string } | null;
  tier: string;
};

const TESTIMONIALS: Testimonial[] = [];

const TIER_COLORS: Record<string, string> = {
  "Sprint": "bg-orange-100 dark:bg-orange-950/30 text-orange-700 dark:text-orange-300",
  "Proof Pack": "bg-blue-100 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300",
  "Custom AI": "bg-purple-100 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300",
  "Managed Ops": "bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300",
};

/* ─── Component ─────────────────────────────────────── */

interface TestimonialsSectionProps {
  limit?: number;
  className?: string;
}

export function TestimonialsSection({ limit, className = "" }: TestimonialsSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const displayed = limit ? TESTIMONIALS.slice(0, limit) : TESTIMONIALS;

  return (
    <section className={`space-y-8 ${className}`} dir={isAr ? "rtl" : "ltr"}>
      {/* Header */}
      <div className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-[#D4AF37] uppercase tracking-wide mb-2">
          {isAr ? "شهادات العملاء" : "Client Testimonials"}
        </p>
        <h2 className="text-3xl font-bold">
          {isAr ? "ماذا قالوا عن Dealix" : "What Clients Say About Dealix"}
        </h2>
      </div>

      {displayed.length === 0 ? (
        /* Honest empty state — no fabricated social proof. */
        <Card className={`border-dashed border-border/60 bg-card/40 p-8 ${isAr ? "text-right" : "text-left"}`}>
          <p className="text-base font-semibold text-foreground">
            {isAr
              ? "نعرض هنا شهادات عملاء حقيقيين — بعد موافقتهم الموثّقة فقط."
              : "We publish real client testimonials here — only with documented consent."}
          </p>
          <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
            {isAr
              ? "لا نعرض شهادات أو شعارات ملفّقة. كل ادعاء مرتبط بـ Proof Pack موقّع ومصدر مسجّل. ابدأ بالتشخيص المجاني وكن أول قصة نجاح موثّقة."
              : "We do not display fabricated quotes or logos. Every claim is tied to a signed Proof Pack with a recorded source. Start with the free diagnostic and become our first documented success story."}
          </p>
        </Card>
      ) : (
        <>
          {/* Cards */}
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {displayed.map((t) => {
              const tierColor = TIER_COLORS[t.tier] ?? "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300";
              return (
                <Card
                  key={t.id}
                  className={`flex flex-col border-border/60 bg-card/50 p-5 ${isAr ? "text-right" : "text-left"}`}
                >
                  {/* Metric badge */}
                  {t.metric && (
                    <div className="mb-3">
                      <span className="text-2xl font-bold text-[#D4AF37]">
                        {isAr ? t.metric.ar : t.metric.en}
                      </span>
                    </div>
                  )}

                  {/* Quote */}
                  <blockquote className="flex-1 mb-4">
                    <p className="text-sm leading-relaxed text-foreground">
                      "{isAr ? t.quote.ar : t.quote.en}"
                    </p>
                  </blockquote>

                  {/* Author */}
                  <div className="flex items-center gap-3 pt-3 border-t border-border/40">
                    <div className="w-9 h-9 rounded-full bg-[#001F3F] text-[#D4AF37] flex items-center justify-center font-bold text-sm flex-shrink-0">
                      {t.initials}
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-semibold leading-none">
                        {isAr ? t.author.ar : t.author.en}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {isAr ? t.role.ar : t.role.en} — {isAr ? t.company.ar : t.company.en}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {isAr ? t.sector.ar : t.sector.en}
                      </p>
                    </div>
                    <span className={`ms-auto flex-shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${tierColor}`}>
                      {t.tier}
                    </span>
                  </div>
                </Card>
              );
            })}
          </div>

          <p className="text-xs text-center text-muted-foreground">
            {isAr
              ? "شهادات من عملاء حقيقيين بموافقة موثّقة. الأدلة في Proof Pack."
              : "Testimonials from real clients with documented consent. Evidence in Proof Pack."}
          </p>
        </>
      )}
    </section>
  );
}
