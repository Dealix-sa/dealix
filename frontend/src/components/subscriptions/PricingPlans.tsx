"use client";

import Link from "next/link";
import { useState } from "react";
import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CheckoutPanel } from "@/components/gtm/CheckoutPanel";
import { PRICING_TIERS, formatTierPrice, type PricingTier } from "@/content/pricing";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface FaqItem {
  questionAr: string;
  questionEn: string;
  answerAr: string;
  answerEn: string;
}

const FAQ_ITEMS: FaqItem[] = [
  {
    questionAr: "هل يمكنني الترقية لاحقاً؟",
    questionEn: "Can I upgrade later?",
    answerAr:
      "نعم، يمكنك الترقية في أي وقت. كل مستوى يبني على الإثبات من المستوى السابق — الانتقال إلى عمليات النمو يتطلب إتمام سبرنت أولاً.",
    answerEn:
      "Yes, you can upgrade at any time. Each tier builds on proof from the previous — moving to Growth Ops requires completing a Sprint first.",
  },
  {
    questionAr: "ما الفرق بين السبرنت وعمليات النمو؟",
    questionEn: "What is the difference between the Sprint and Growth Ops?",
    answerAr:
      "السبرنت تشخيص لمرة واحدة خلال ٧ أيام ينتهي بـ Proof Pack. عمليات النمو اشتراك شهري يشمل تشغيلاً مستمراً وتدقيقاً أسبوعياً وProof Pack شهري.",
    answerEn:
      "The Sprint is a one-time 7-day diagnostic ending with a Proof Pack. Growth Ops is a monthly subscription covering ongoing operations, weekly audits, and a monthly Proof Pack.",
  },
  {
    questionAr: "كيف تتم عملية الموافقة؟",
    questionEn: "How does the approval process work?",
    answerAr:
      "كل قرار حرج يمر عبر مركز الموافقات — لا يُنفَّذ أي إجراء خارجي بدون موافقة بشرية صريحة. هذا مبدأ غير قابل للتفاوض في جميع المستويات.",
    answerEn:
      "Every critical decision passes through the Approval Center — no external action is executed without explicit human approval. This is non-negotiable at all tiers.",
  },
  {
    questionAr: "ما وسائل الدفع المتاحة؟",
    questionEn: "What payment methods are available?",
    answerAr:
      "ندفع عبر Moyasar: مدى، Visa/Mastercard. فاتورة متوافقة مع ZATCA لكل معاملة.",
    answerEn:
      "We charge via Moyasar: Mada, Visa/Mastercard. A ZATCA-compliant invoice for every transaction.",
  },
];

// ---------------------------------------------------------------------------
// Animation variants
// ---------------------------------------------------------------------------

const FADE_UP = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.45, delay: i * 0.08, ease: "easeOut" },
  }),
};

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <polyline points="2.5 8 6 11.5 13.5 4.5" />
    </svg>
  );
}

function PlanCard({
  tier,
  isAr,
  index,
  locale,
}: {
  tier: PricingTier;
  isAr: boolean;
  index: number;
  locale: string;
}) {
  const [showCheckout, setShowCheckout] = useState(false);
  const featured = !!tier.featured;
  const deliverables = isAr ? tier.deliverablesAr : tier.deliverablesEn;
  const name = isAr ? tier.nameAr : tier.nameEn;
  const tagline = isAr ? tier.taglineAr : tier.taglineEn;
  const kpi = isAr ? tier.kpiAr : tier.kpiEn;
  const checkClass = featured ? "text-gold-500" : "text-[#001F3F] dark:text-gold-400";

  return (
    <motion.div
      custom={index}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={FADE_UP}
      className="flex"
    >
      <Card
        className={`relative flex w-full flex-col border-2 ${
          featured ? "border-gold-500/60 shadow-lg shadow-gold-500/10" : "border-border/60"
        }`}
      >
        {featured && (
          <div className="absolute -top-4 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-full bg-gold-500 px-4 py-1 text-xs font-bold text-[#001F3F] shadow-md">
            {isAr ? "الأكثر طلباً" : "Most Popular"}
          </div>
        )}

        <CardHeader
          className={`rounded-t-2xl pb-4 ${
            featured
              ? "bg-gradient-to-br from-gold-500/15 to-gold-500/5"
              : "bg-gradient-to-br from-[#001F3F]/10 to-transparent"
          }`}
        >
          <CardTitle className="text-lg">{name}</CardTitle>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-3xl font-bold">{formatTierPrice(tier, isAr)}</span>
          </div>
          <p className="mt-2 text-xs text-muted-foreground leading-relaxed">{tagline}</p>
        </CardHeader>

        <CardContent className="flex flex-1 flex-col pt-5">
          <ul className="flex-1 space-y-2.5">
            {deliverables.map((f) => (
              <li key={f} className="flex items-start gap-2.5 text-sm">
                <CheckIcon className={`mt-0.5 h-4 w-4 flex-shrink-0 ${checkClass}`} />
                <span>{f}</span>
              </li>
            ))}
          </ul>

          <p className="mt-4 rounded-lg bg-muted/40 px-3 py-2 text-xs text-muted-foreground leading-relaxed">
            {kpi}
          </p>

          <div className="mt-5">
            {tier.ctaKind === "checkout" ? (
              showCheckout ? (
                <CheckoutPanel
                  plan={tier.id}
                  planLabel={name}
                  priceHint={formatTierPrice(tier, isAr)}
                  isAr={isAr}
                />
              ) : (
                <Button
                  variant={featured ? "gold" : "default"}
                  size="lg"
                  className="w-full"
                  onClick={() => setShowCheckout(true)}
                >
                  {isAr ? "اختر هذه الباقة" : "Choose this plan"}
                </Button>
              )
            ) : (
              <Button variant={featured ? "gold" : "outline"} size="lg" className="w-full" asChild>
                <Link
                  href={`/${locale}${tier.ctaKind === "custom" ? "/custom" : "/dealix-diagnostic"}`}
                >
                  {tier.ctaKind === "custom"
                    ? isAr
                      ? "اطلب بناءً مخصّصاً"
                      : "Request a custom build"
                    : isAr
                      ? "ابدأ مجاناً"
                      : "Start free"}
                </Link>
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function FaqAccordion({ items, isAr }: { items: FaqItem[]; isAr: boolean }) {
  return (
    <div className="space-y-3">
      {items.map((item, i) => (
        <motion.details
          key={i}
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.07 }}
          className="group rounded-2xl border border-border/60 bg-card/80"
        >
          <summary className="flex cursor-pointer list-none items-center justify-between px-6 py-4 font-semibold text-sm hover:bg-muted/30 transition-colors rounded-2xl">
            <span>{isAr ? item.questionAr : item.questionEn}</span>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              className="h-4 w-4 flex-shrink-0 text-muted-foreground transition-transform group-open:rotate-180"
              aria-hidden="true"
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </summary>
          <div className="px-6 pb-5 pt-1 text-sm text-muted-foreground leading-relaxed">
            {isAr ? item.answerAr : item.answerEn}
          </div>
        </motion.details>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main exported component
// ---------------------------------------------------------------------------

export function PricingPlans() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div className="space-y-16" dir={isAr ? "rtl" : "ltr"}>
      <motion.header
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="text-center"
      >
        <Badge variant="gold" className="mb-4 text-xs uppercase tracking-wide">
          {isAr ? "خطط الأسعار" : "Pricing Plans"}
        </Badge>
        <h1 className="text-4xl font-bold leading-tight font-display">
          {isAr ? "ابدأ من حيث أنت — وسِّع بعد الإثبات" : "Start Where You Are — Expand After Proof"}
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-muted-foreground leading-relaxed">
          {isAr
            ? "كل خطة تبني على الإثبات من الخطة السابقة. لا توسع بدون Proof Pack مُسلَّم. كل الأسعار بالريال السعودي."
            : "Every plan builds on proof from the previous. No expansion without a delivered Proof Pack. All prices in SAR."}
        </p>
      </motion.header>

      <section className="grid gap-8 md:grid-cols-2 lg:grid-cols-3 items-start">
        {PRICING_TIERS.map((tier, i) => (
          <PlanCard key={tier.id} tier={tier} isAr={isAr} index={i} locale={locale} />
        ))}
      </section>

      {/* Money-back + payment methods */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4 }}
        className="flex flex-col items-center gap-6 rounded-2xl border border-emerald-500/30 bg-emerald-500/5 px-8 py-6 sm:flex-row sm:justify-between"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500/15 text-emerald-500">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="h-5 w-5" aria-hidden="true">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <div>
            <p className="font-semibold text-sm">
              {isAr ? "سياسة استرداد عادلة" : "Fair Refund Policy"}
            </p>
            <p className="text-xs text-muted-foreground">
              {isAr
                ? "السبرنت: استرداد ١٠٠٪ خلال ١٤ يوماً. تفاصيل كل باقة في الشروط."
                : "Sprint: 100% refund within 14 days. See each plan's terms for details."}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <p className="text-xs font-semibold text-muted-foreground">
            {isAr ? "وسائل الدفع:" : "Payment methods:"}
          </p>
          <div className="flex items-center gap-3">
            <span className="rounded-md border border-border/60 bg-card px-2.5 py-1 text-xs font-bold">Visa</span>
            <span className="rounded-md border border-border/60 bg-card px-2.5 py-1 text-xs font-bold">Mada</span>
            <span className="rounded-md border border-border/60 bg-card px-2.5 py-1 text-xs font-bold">Moyasar</span>
          </div>
        </div>
      </motion.section>

      {/* FAQ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-6 text-xl font-bold"
        >
          {isAr ? "الأسئلة الشائعة" : "Frequently Asked Questions"}
        </motion.h2>
        <FaqAccordion items={FAQ_ITEMS} isAr={isAr} />
      </section>

      {/* Bottom CTA */}
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4 }}
        className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#002f5f] p-8 text-center text-white"
      >
        <h2 className="text-2xl font-bold">
          {isAr ? "لا تزال غير متأكد؟ ابدأ بتشخيص مجاني" : "Still unsure? Start with a free diagnostic"}
        </h2>
        <p className="mx-auto mt-3 max-w-md text-white/70 text-sm">
          {isAr
            ? "تشخيص مجاني — لا بطاقة ائتمانية مطلوبة."
            : "Free diagnostic — no credit card required."}
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-4">
          <Button variant="gold" size="lg" asChild>
            <Link href={`/${locale}/dealix-diagnostic`}>
              {isAr ? "ابدأ التشخيص المجاني" : "Start the free diagnostic"}
            </Link>
          </Button>
          <Button variant="outline" size="lg" className="border-white/20 text-white hover:bg-white/10" asChild>
            <Link href={`/${locale}/contact`}>{isAr ? "احجز مكالمة" : "Book a call"}</Link>
          </Button>
        </div>
      </motion.section>
    </div>
  );
}
