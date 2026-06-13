"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

/* ─────────────────────────────────────────────────────────────────────────
   Founding-cohort honest stance. Dealix is pre-revenue: we do NOT publish
   invented testimonials, fabricated metrics, or false consent claims
   (non-negotiables #4/#5). Real, consented client quotes appear here only
   after a delivered Proof Pack. Until then we show our commitments.
   ───────────────────────────────────────────────────────────────────────── */

const PROMISES: {
  id: string;
  icon: string;
  title: { ar: string; en: string };
  body: { ar: string; en: string };
}[] = [
  {
    id: "evidence",
    icon: "✓",
    title: { ar: "دليل قبل الكلام", en: "Evidence before words" },
    body: {
      ar: "لن ترى هنا شهادة واحدة مُختلقة. ننشر اقتباسات العملاء فقط بعد Proof Pack مُسلَّم وبموافقتهم الكتابية.",
      en: "You will not see a single invented testimonial here. We publish client quotes only after a delivered Proof Pack and with written consent.",
    },
  },
  {
    id: "founder",
    icon: "★",
    title: { ar: "تسليم بإشراف المؤسس", en: "Founder-led delivery" },
    body: {
      ar: "عملاء الدفعة التأسيسية يعملون مباشرة مع المؤسس ويشكّلون المنتج — جودة عالية وانتباه شخصي.",
      en: "Founding-cohort clients work directly with the founder and shape the product — high quality, personal attention.",
    },
  },
  {
    id: "proof",
    icon: "▣",
    title: { ar: "نتيجتك هنا قريباً", en: "Your result here soon" },
    body: {
      ar: "كن أول قصة نجاح موثّقة لـ Dealix. ابدأ بتشخيص مجاني وحوّل بياناتك إلى دليل قابل للنشر.",
      en: "Be Dealix's first documented success story. Start with a free diagnostic and turn your data into publishable proof.",
    },
  },
];

interface TestimonialsSectionProps {
  limit?: number;
  className?: string;
}

export function TestimonialsSection({ limit, className = "" }: TestimonialsSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const displayed = limit ? PROMISES.slice(0, limit) : PROMISES;

  return (
    <section className={`space-y-8 ${className}`} dir={isAr ? "rtl" : "ltr"}>
      <div className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-2">
          {isAr ? "الدفعة التأسيسية 2026" : "Founding cohort 2026"}
        </p>
        <h2 className="text-3xl font-bold">
          {isAr ? "نتائج موثّقة فقط — لا شهادات مُختلقة" : "Verified results only — no invented testimonials"}
        </h2>
        <p className="mt-3 text-muted-foreground max-w-2xl leading-relaxed">
          {isAr
            ? "Dealix شركة سعودية حديثة. بدل اختلاق آراء عملاء، نعرض التزاماتنا — والشهادات الحقيقية تظهر هنا بعد أول Proof Pack مُسلَّم وبموافقة أصحابها."
            : "Dealix is a new Saudi venture. Instead of faking client quotes, we show our commitments — real testimonials appear here after the first delivered Proof Pack, with owner consent."}
        </p>
      </div>

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {displayed.map((p) => (
          <Card
            key={p.id}
            className={`flex flex-col border-border/60 bg-card/50 p-5 ${isAr ? "text-right" : "text-left"}`}
          >
            <div className="w-10 h-10 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold mb-3">
              {p.icon}
            </div>
            <h3 className="font-semibold text-base mb-1">{isAr ? p.title.ar : p.title.en}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed flex-1">{isAr ? p.body.ar : p.body.en}</p>
          </Card>
        ))}
      </div>

      <div className="text-center">
        <Button asChild size="sm" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-semibold">
          <Link href={`${base}/risk-score`}>{isAr ? "ابدأ تشخيصك المجاني" : "Start your free diagnostic"}</Link>
        </Button>
      </div>
    </section>
  );
}
