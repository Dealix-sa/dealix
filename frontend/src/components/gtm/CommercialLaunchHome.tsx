"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

import { motion, useInView, useAnimation } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Static data — product capabilities only. No customer names, no outcome
// metrics, no guaranteed-results language. Every claim maps to a shipped
// capability or a non-negotiable governance principle.
// ---------------------------------------------------------------------------

const FEATURES = [
  {
    icon: "01",
    ar: "تشخيص الإيراد بالأدلة",
    en: "Evidence-Based Revenue Diagnostic",
    descAr: "مراجعة محكومة لمسار الإيراد وملفات العملاء مع تحديد فجوات الأدلة.",
    descEn: "Governed review of your revenue pipeline and account records with evidence-gap detection.",
  },
  {
    icon: "02",
    ar: "حزمة إثبات Proof Pack",
    en: "Proof Pack",
    descAr: "حزمة أدلة بأربعة أقسام ومستويات L0-L5، تُسلَّم كـ PDF ثنائي اللغة.",
    descEn: "Four-section evidence bundle with L0-L5 levels, delivered as a bilingual PDF.",
  },
  {
    icon: "03",
    ar: "حوكمة قبل كل إرسال",
    en: "Approval-First Governance",
    descAr: "كل إجراء خارجي يمر بموافقة بشرية. لا أتمتة بلا مراجعة، مع سجل تدقيق كامل.",
    descEn: "Every external action passes human approval. No automation without review, full audit trail.",
  },
  {
    icon: "04",
    ar: "جاهزية PDPL و ZATCA",
    en: "PDPL & ZATCA Readiness",
    descAr: "تشخيص جاهزية حماية البيانات والفوترة الإلكترونية مدمج في كل Proof Pack.",
    descEn: "Data-protection and e-invoicing readiness diagnostics built into every Proof Pack.",
  },
  {
    icon: "05",
    ar: "OKR أسبوعي محكوم",
    en: "Governed Weekly OKR",
    descAr: "أهداف ونتائج أسبوعية موثّقة ضمن خطة التشغيل المُدار.",
    descEn: "Documented weekly objectives and key results inside the managed-ops plan.",
  },
  {
    icon: "06",
    ar: "طبقة فوق الـ CRM الحالي",
    en: "Layer Over Your CRM",
    descAr: "طبقة حوكمة وأدلة تعمل فوق الـ CRM الحالي — لا تستبدله.",
    descEn: "A governance and evidence layer that works on top of your existing CRM, not a replacement.",
  },
];

// The five productized offers (the commercial ladder). Prices are list prices;
// no outcome promises. Each rung links into the public funnel.
const LADDER = [
  {
    rung: "0",
    ar: "التشخيص المجاني",
    en: "Free Diagnostic",
    priceAr: "مجاني",
    priceEn: "Free",
    periodAr: "",
    periodEn: "",
    valueAr: "Risk Score تشغيلي وتحليل جاهزية في دقائق — بدون بطاقة أو حساب.",
    valueEn: "Operational Risk Score and readiness analysis in minutes — no card, no account.",
    proofAr: "نتيجة فورية + 3 فجوات رئيسية",
    proofEn: "Instant score + 3 key gaps",
    ctaAr: "ابدأ مجاناً",
    ctaEn: "Start free",
    href: "/risk-score",
    highlight: false,
  },
  {
    rung: "1",
    ar: "سبرنت ذكاء الإيرادات (7 أيام)",
    en: "7-Day Revenue Intelligence Sprint",
    priceAr: "499 ر.س",
    priceEn: "499 SAR",
    periodAr: "دفعة واحدة",
    periodEn: "one-time",
    valueAr: "مراجعة عميقة لـ 10 leads حقيقية: مالك واضح، فجوات أدلة، مسودة Proof، خطوة تالية.",
    valueEn: "Deep review of 10 real leads: clear owner, evidence gaps, Proof draft, next action.",
    proofAr: "مسودة Proof لأفضل 3 leads",
    proofEn: "Proof draft for top 3 leads",
    ctaAr: "ابدأ السبرنت",
    ctaEn: "Start the sprint",
    href: "/dealix-diagnostic",
    highlight: false,
  },
  {
    rung: "2",
    ar: "حزمة البيانات إلى إيراد",
    en: "Data-to-Revenue Pack",
    priceAr: "1,500 ر.س",
    priceEn: "1,500 SAR",
    periodAr: "دفعة واحدة",
    periodEn: "one-time",
    valueAr: "حزمة إثبات كاملة بأربعة أقسام ومستويات L0-L5، جاهزة لتقديمها للعميل.",
    valueEn: "Full four-section evidence bundle with L0-L5 levels, ready to present to your client.",
    proofAr: "Proof Pack PDF ثنائي اللغة",
    proofEn: "Bilingual Proof Pack PDF",
    ctaAr: "اطلب الحزمة",
    ctaEn: "Request the pack",
    href: "/proof-pack",
    highlight: false,
  },
  {
    rung: "3",
    ar: "إدارة عمليات الإيراد",
    en: "Managed Revenue Ops",
    priceAr: "2,999 – 4,999 ر.س",
    priceEn: "2,999 – 4,999 SAR",
    periodAr: "شهرياً",
    periodEn: "per month",
    valueAr: "تشغيل مُدار شهرياً: OKR أسبوعي، Proof Pack شهري، دعم أولوية، Approval Center.",
    valueEn: "Monthly managed ops: weekly OKR, monthly Proof Pack, priority support, Approval Center.",
    proofAr: "يبدأ بعد Proof Pack مُسلَّم",
    proofEn: "Starts after a delivered Proof Pack",
    ctaAr: "احجز استشارة",
    ctaEn: "Book a consultation",
    href: "/services",
    highlight: true,
    badgeAr: "الأكثر طلباً",
    badgeEn: "Most popular",
  },
  {
    rung: "4",
    ar: "إعداد خدمة AI مخصّصة",
    en: "Custom AI Service Setup",
    priceAr: "5,000 – 25,000 ر.س",
    priceEn: "5,000 – 25,000 SAR",
    periodAr: "+ 1,000 ر.س/شهر",
    periodEn: "+ 1,000 SAR/mo",
    valueAr: "تطوير AI مخصص بـ Scope موقّع، Approval Center لكل خطوة، وProof Pack ختامي.",
    valueEn: "Custom AI build with a signed scope, Approval Center at every step, and a final Proof Pack.",
    proofAr: "Scope موقّع + audit trail",
    proofEn: "Signed scope + audit trail",
    ctaAr: "ناقش مشروعك",
    ctaEn: "Discuss your project",
    href: "/services",
    highlight: false,
  },
];

const ENTERPRISE = {
  ar: "مراجعة حوكمة الذكاء الاصطناعي",
  en: "AI Governance Review",
  priceAr: "25,000 – 50,000 ر.س",
  priceEn: "25,000 – 50,000 SAR",
  valueAr: "مراجعة مستقلة لحوكمة الذكاء الاصطناعي والامتثال للمؤسسات الكبيرة.",
  valueEn: "Independent AI governance and compliance review for larger organizations.",
  ctaAr: "تواصل مع الفريق",
  ctaEn: "Contact the team",
  href: "/services",
};

// Governance principles — the non-negotiables, stated as guardrails not claims.
const TRUST_BADGES = [
  { ar: "PDPL أصيل", en: "PDPL-native" },
  { ar: "موافقة بشرية أولاً", en: "Human approval first" },
  { ar: "لا تواصل بارد آلي", en: "No cold outreach" },
  { ar: "لا scraping", en: "No scraping" },
  { ar: "سجل تدقيق كامل", en: "Full audit trail" },
];

// How it works — the proof-before-expansion path.
const STEPS = [
  {
    ar: "ابدأ بالتشخيص المجاني",
    en: "Start with the free diagnostic",
    descAr: "اعرف وضعك التشغيلي وفجواتك قبل أي التزام.",
    descEn: "Understand your operational position and gaps before any commitment.",
  },
  {
    ar: "احصل على Proof Pack",
    en: "Get a Proof Pack",
    descAr: "أدلة موثّقة بأربعة أقسام تثبت القيمة قبل التوسع.",
    descEn: "Documented four-section evidence that proves value before you scale.",
  },
  {
    ar: "وسّع بعد الإثبات",
    en: "Expand after proof",
    descAr: "انتقل إلى التشغيل المُدار فقط بعد Proof Pack مُسلَّم.",
    descEn: "Move to managed ops only after a delivered Proof Pack.",
  },
];

// ---------------------------------------------------------------------------
// Animation variants
// ---------------------------------------------------------------------------

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.08, ease: "easeOut" },
  }),
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.09 } },
};

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function CommercialLaunchHome() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";
  const base = `/${locale}`;

  const heroControls = useAnimation();
  const heroRef = useRef<HTMLDivElement>(null);
  const heroInView = useInView(heroRef, { once: true });

  useEffect(() => {
    if (heroInView) heroControls.start("visible");
  }, [heroInView, heroControls]);

  return (
    <div dir={dir} className="min-h-screen bg-navy-500 text-white overflow-x-hidden">
      {/* ------------------------------------------------------------------ */}
      {/* HERO                                                                */}
      {/* ------------------------------------------------------------------ */}
      <section
        ref={heroRef}
        className="relative min-h-[88vh] flex flex-col items-center justify-center px-4 overflow-hidden"
        style={{ background: "linear-gradient(135deg, #001F3F 0%, #001830 40%, #000d1a 70%, #001020 100%)" }}
      >
        {/* Brand gradient orbs (navy + gold) */}
        <div aria-hidden className="pointer-events-none absolute inset-0 overflow-hidden">
          <motion.div
            animate={{ scale: [1, 1.15, 1], opacity: [0.18, 0.28, 0.18] }}
            transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -top-32 -left-32 w-[520px] h-[520px] rounded-full"
            style={{ background: "radial-gradient(circle, rgba(212,175,55,0.22) 0%, transparent 70%)" }}
          />
          <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.1, 0.18, 0.1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            className="absolute bottom-0 right-0 w-[600px] h-[600px] rounded-full"
            style={{ background: "radial-gradient(circle, rgba(0,102,255,0.14) 0%, transparent 70%)" }}
          />
        </div>

        {/* PDPL / approval-first badge */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="relative z-10 mb-6"
        >
          <Badge className="border-gold-500/40 bg-gold-500/10 text-gold-300 text-xs px-4 py-1.5 rounded-full backdrop-blur-sm">
            <span className="inline-block w-2 h-2 rounded-full bg-gold-400 me-2 animate-pulse" />
            {isAr ? "مبني للسوق السعودي — PDPL أصيل · ZATCA جاهز" : "Built for Saudi market — PDPL-native · ZATCA-ready"}
          </Badge>
        </motion.div>

        {/* Glassmorphism hero card */}
        <motion.div
          variants={stagger}
          initial="hidden"
          animate={heroControls}
          className="relative z-10 w-full max-w-3xl text-center"
        >
          <motion.div
            variants={fadeUp}
            className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-lg px-8 py-12 md:px-16 md:py-16 shadow-2xl"
            style={{ boxShadow: "0 8px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.07)" }}
          >
            <motion.h1
              variants={fadeUp}
              custom={1}
              className="font-arabic text-3xl sm:text-4xl md:text-5xl font-bold leading-tight tracking-tight"
              style={{ fontFamily: "'Noto Sans Arabic', 'IBM Plex Arabic', sans-serif" }}
            >
              {isAr ? (
                <>
                  وحّد قرار الإيراد.{" "}
                  <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                    أثبت كل لمسة.
                  </span>{" "}
                  وسّع بعد الإثبات.
                </>
              ) : (
                <>
                  Unify revenue decisions.{" "}
                  <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                    Prove every touch.
                  </span>{" "}
                  Expand after proof.
                </>
              )}
            </motion.h1>

            <motion.p
              variants={fadeUp}
              custom={2}
              className="mt-5 text-base md:text-lg text-white/70 max-w-xl mx-auto leading-relaxed"
            >
              {isAr
                ? "نظام تشغيل الإيرادات B2B للشركات السعودية — تشخيص محكوم، Proof Pack بالأدلة، وحوكمة قبل كل إرسال."
                : "The B2B revenue operating system for Saudi enterprises — governed diagnostics, evidence-based Proof Packs, and approval before every send."}
            </motion.p>

            <motion.div
              variants={fadeUp}
              custom={3}
              className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3"
            >
              <Button
                asChild
                size="lg"
                className="w-full sm:w-auto bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 shadow-lg shadow-gold-500/25 text-base h-13 px-8"
              >
                <Link href={`${base}/risk-score`}>
                  {isAr ? "ابدأ تشخيصك المجاني" : "Start your free diagnostic"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-white/20 text-white hover:bg-white/10 backdrop-blur-sm text-base h-13 px-8"
              >
                <Link href={`${base}/services`}>
                  {isAr ? "استعرض العروض الخمسة" : "See the five offers"}
                </Link>
              </Button>
            </motion.div>

            <motion.p variants={fadeUp} custom={4} className="mt-5 text-xs text-white/40">
              {isAr
                ? "لا تواصل بارد آلي · لا ادّعاء نتائج · موافقة بشرية دائماً"
                : "No automated cold outreach · No results claims · Always human approval"}
            </motion.p>
          </motion.div>
        </motion.div>

        {/* Scroll cue */}
        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="w-5 h-8 rounded-full border border-white/20 flex items-start justify-center pt-1.5">
            <div className="w-1 h-2 rounded-full bg-white/40" />
          </div>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* TRUST / GOVERNANCE STRIP                                            */}
      {/* ------------------------------------------------------------------ */}
      <section className="bg-navy-600 border-y border-white/5 py-8 px-4">
        <p className="text-center text-xs font-semibold text-white/40 uppercase tracking-widest mb-5">
          {isAr ? "مبادئ غير قابلة للتفاوض" : "Non-negotiable principles"}
        </p>
        <div className="flex flex-wrap gap-3 justify-center max-w-4xl mx-auto">
          {TRUST_BADGES.map((badge) => (
            <div
              key={badge.en}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm"
            >
              <span className="text-gold-400 text-sm leading-none">◆</span>
              <span className="text-sm font-medium text-white/80 whitespace-nowrap">
                {isAr ? badge.ar : badge.en}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* FEATURES GRID                                                       */}
      {/* ------------------------------------------------------------------ */}
      <section className="py-20 px-4 max-w-6xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="text-center mb-12"
        >
          <motion.p variants={fadeUp} className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "المنصة" : "Platform"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "ما الذي تحصل عليه فعلياً" : "What you actually get"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-xl mx-auto">
            {isAr
              ? "قدرات مُنتَجة تعمل معاً — كل واحدة منها قابلة للتسليم والتوثيق."
              : "Productized capabilities that work together — each one deliverable and documented."}
          </motion.p>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.en}
              variants={fadeUp}
              custom={i}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="group rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-6 hover:border-gold-500/30 hover:bg-white/7 transition-colors cursor-default"
              style={{ boxShadow: "inset 0 1px 0 rgba(255,255,255,0.05)" }}
            >
              <div className="text-gold-400/70 font-mono text-sm mb-4 tracking-widest">{f.icon}</div>
              <h3 className="font-bold text-lg mb-0.5">{isAr ? f.ar : f.en}</h3>
              <p className="text-xs text-white/50 font-medium mb-2">{isAr ? f.en : f.ar}</p>
              <p className="text-sm text-white/65 leading-relaxed">{isAr ? f.descAr : f.descEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* THE FIVE-OFFER LADDER                                               */}
      {/* ------------------------------------------------------------------ */}
      <section
        id="offers"
        className="py-20 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 50%, #000d1a 100%)" }}
      >
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="text-center mb-12 max-w-2xl mx-auto"
        >
          <motion.p variants={fadeUp} className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "سلم العروض" : "The offer ladder"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "خمسة عروض تبني على الإثبات" : "Five offers that build on proof"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60">
            {isAr
              ? "ابدأ من حيث أنت. لا توسّع بدون Proof Pack مُسلَّم. جميع الأسعار بالريال السعودي."
              : "Start where you are. No expansion without a delivered Proof Pack. All prices in SAR."}
          </motion.p>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-5 md:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto items-stretch"
        >
          {LADDER.map((offer, i) => (
            <motion.div
              key={offer.rung}
              variants={fadeUp}
              custom={i}
              className={`relative rounded-2xl border p-7 flex flex-col gap-4 ${
                offer.highlight
                  ? "border-gold-500/50 bg-gradient-to-b from-gold-500/8 to-transparent shadow-xl shadow-gold-500/10"
                  : "border-white/8 bg-white/4"
              } backdrop-blur-sm`}
              style={offer.highlight ? { boxShadow: "0 0 40px rgba(212,175,55,0.12), inset 0 1px 0 rgba(255,255,255,0.07)" } : {}}
            >
              {offer.highlight && offer.badgeAr && (
                <div className={`absolute -top-3.5 ${isAr ? "left-6" : "right-6"}`}>
                  <Badge className="bg-gold-500 text-navy-500 border-0 font-bold px-3 py-1 text-xs">
                    {isAr ? offer.badgeAr : offer.badgeEn}
                  </Badge>
                </div>
              )}

              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg border border-gold-500/30 bg-gold-500/10 text-gold-400 font-bold text-sm">
                  {offer.rung}
                </span>
                <h3 className="font-bold text-lg leading-tight">{isAr ? offer.ar : offer.en}</h3>
              </div>

              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold">{isAr ? offer.priceAr : offer.priceEn}</span>
                {offer.periodAr && (
                  <span className="text-white/50 text-sm">{isAr ? offer.periodAr : offer.periodEn}</span>
                )}
              </div>

              <p className="text-sm text-white/70 leading-relaxed flex-1">{isAr ? offer.valueAr : offer.valueEn}</p>

              <div className="flex items-start gap-2 text-xs text-emerald-300/90 border-t border-white/8 pt-3">
                <span className="text-emerald-400 mt-0.5 flex-shrink-0 leading-none">✓</span>
                <span>{isAr ? offer.proofAr : offer.proofEn}</span>
              </div>

              <Button
                asChild
                size="lg"
                className={`w-full font-semibold ${
                  offer.highlight
                    ? "bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 hover:from-gold-400 hover:to-gold-300 shadow-md shadow-gold-500/20"
                    : "bg-white/8 border border-white/15 text-white hover:bg-white/14"
                }`}
              >
                <Link href={`${base}${offer.href}`}>{isAr ? offer.ctaAr : offer.ctaEn}</Link>
              </Button>
            </motion.div>
          ))}

          {/* Enterprise rung */}
          <motion.div
            variants={fadeUp}
            custom={LADDER.length}
            className="relative rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-7 flex flex-col gap-4 lg:col-span-2"
          >
            <div className="flex items-center gap-3">
              <span className="flex h-9 px-3 flex-shrink-0 items-center justify-center rounded-lg border border-gold-500/30 bg-gold-500/10 text-gold-400 font-bold text-xs uppercase tracking-wide">
                {isAr ? "مؤسسي" : "Enterprise"}
              </span>
              <h3 className="font-bold text-lg leading-tight">{isAr ? ENTERPRISE.ar : ENTERPRISE.en}</h3>
            </div>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <span className="text-2xl font-bold">{isAr ? ENTERPRISE.priceAr : ENTERPRISE.priceEn}</span>
                <p className="text-sm text-white/70 leading-relaxed mt-1 max-w-md">
                  {isAr ? ENTERPRISE.valueAr : ENTERPRISE.valueEn}
                </p>
              </div>
              <Button
                asChild
                size="lg"
                className="bg-white/8 border border-white/15 text-white hover:bg-white/14 font-semibold whitespace-nowrap"
              >
                <Link href={`${base}${ENTERPRISE.href}`}>{isAr ? ENTERPRISE.ctaAr : ENTERPRISE.ctaEn}</Link>
              </Button>
            </div>
          </motion.div>
        </motion.div>

        <div className="text-center mt-10">
          <Link
            href={`${base}/pricing`}
            className="text-sm text-gold-400 hover:text-gold-300 font-medium transition-colors"
          >
            {isAr ? "قارن الخطط بالتفصيل ←" : "Compare plans in detail →"}
          </Link>
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* HOW IT WORKS — proof before expansion                               */}
      {/* ------------------------------------------------------------------ */}
      <section className="py-20 px-4 max-w-5xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="text-center mb-12"
        >
          <motion.p variants={fadeUp} className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
            {isAr ? "كيف يعمل" : "How it works"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "الإثبات قبل التوسع" : "Proof before expansion"}
          </motion.h2>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-6 md:grid-cols-3"
        >
          {STEPS.map((step, i) => (
            <motion.div
              key={step.en}
              variants={fadeUp}
              custom={i}
              className="rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-7"
            >
              <div className="text-4xl font-bold bg-gradient-to-br from-gold-300 to-gold-500 bg-clip-text text-transparent leading-none mb-4">
                {i + 1}
              </div>
              <h3 className="font-bold text-lg mb-2">{isAr ? step.ar : step.en}</h3>
              <p className="text-sm text-white/65 leading-relaxed">{isAr ? step.descAr : step.descEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* CTA SECTION                                                         */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-24 px-4 relative overflow-hidden"
        style={{ background: "linear-gradient(135deg, #001830 0%, #002040 50%, #001830 100%)" }}
      >
        <div
          aria-hidden
          className="absolute inset-0 pointer-events-none"
          style={{ background: "radial-gradient(ellipse 80% 60% at 50% 50%, rgba(212,175,55,0.08) 0%, transparent 70%)" }}
        />
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="relative z-10 max-w-2xl mx-auto text-center"
        >
          <motion.h2
            variants={fadeUp}
            className="text-3xl md:text-5xl font-bold leading-tight mb-5"
            style={{ fontFamily: "'Noto Sans Arabic', 'IBM Plex Arabic', sans-serif" }}
          >
            {isAr ? (
              <>
                ابدأ بالتشخيص{" "}
                <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                  المجاني
                </span>
              </>
            ) : (
              <>
                Start with the{" "}
                <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                  free diagnostic
                </span>
              </>
            )}
          </motion.h2>

          <motion.p variants={fadeUp} custom={1} className="text-white/60 mb-8 text-lg">
            {isAr
              ? "Risk Score تشغيلي في دقائق — بدون بطاقة ائتمان وبدون تسجيل. اعرف أين أنت وما هي أولوياتك."
              : "An operational Risk Score in minutes — no credit card, no sign-up. Know where you are and what to prioritize."}
          </motion.p>

          <motion.div
            variants={fadeUp}
            custom={2}
            className="flex flex-col sm:flex-row items-center justify-center gap-3"
          >
            <Button
              asChild
              size="lg"
              className="w-full sm:w-auto h-12 px-7 bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 shadow-lg shadow-gold-500/25"
            >
              <Link href={`${base}/risk-score`}>{isAr ? "احسب Risk Score مجاناً" : "Calculate Risk Score free"}</Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="w-full sm:w-auto h-12 px-7 border-white/20 text-white hover:bg-white/10"
            >
              <Link href={`${base}/dealix-diagnostic`}>{isAr ? "تشخيص محكوم" : "Governed diagnostic"}</Link>
            </Button>
          </motion.div>

          <motion.p variants={fadeUp} custom={3} className="mt-4 text-xs text-white/35">
            {isAr
              ? "بياناتك محمية وفق PDPL. لا upsell قبل Proof Pack. لا outreach بارد."
              : "Your data is protected under PDPL. No upsell before a Proof Pack. No cold outreach."}
          </motion.p>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* FOOTER                                                              */}
      {/* ------------------------------------------------------------------ */}
      <footer className="py-12 px-4 border-t border-white/6" style={{ background: "#000d1a" }}>
        <div className="max-w-6xl mx-auto">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 mb-10">
            {/* Brand */}
            <div className="lg:col-span-2">
              <div className="text-xl font-bold bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent mb-3">
                Dealix
              </div>
              <p className="text-white/50 text-sm leading-relaxed max-w-xs">
                {isAr
                  ? "نظام تشغيل الإيرادات B2B للشركات السعودية. محكوم بالأدلة، PDPL أصيل."
                  : "The B2B revenue operating system for Saudi enterprises. Evidence-governed, PDPL-native."}
              </p>
            </div>

            {/* Product */}
            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "المنتج" : "Product"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "الخدمات", en: "Services", href: "/services" },
                  { ar: "التسعير", en: "Pricing", href: "/pricing" },
                  { ar: "Proof Pack", en: "Proof Pack", href: "/proof-pack" },
                  { ar: "الشركاء", en: "Partners", href: "/partners" },
                ].map((link) => (
                  <li key={link.href}>
                    <Link href={`${base}${link.href}`} className="hover:text-gold-400 transition-colors">
                      {isAr ? link.ar : link.en}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Company */}
            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "الشركة" : "Company"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "من نحن", en: "About", href: "/about" },
                  { ar: "مركز الثقة", en: "Trust Center", href: "/trust-center" },
                  { ar: "سياسة الخصوصية", en: "Privacy", href: "/privacy" },
                  { ar: "تعلّم", en: "Learn", href: "/learn" },
                ].map((link) => (
                  <li key={link.href}>
                    <Link href={`${base}${link.href}`} className="hover:text-gold-400 transition-colors">
                      {isAr ? link.ar : link.en}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-white/6 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-white/30">
            <p>
              {isAr
                ? `© ${new Date().getFullYear()} Dealix. جميع الحقوق محفوظة.`
                : `© ${new Date().getFullYear()} Dealix. All rights reserved.`}
            </p>
            <div className="flex gap-4">
              <span className="text-emerald-500/70">PDPL</span>
              <span className="text-gold-500/70">ZATCA Ready</span>
              <span className="text-white/40">Saudi-First</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
