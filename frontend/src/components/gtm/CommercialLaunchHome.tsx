"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

import { motion, useInView, useAnimation, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Static data
// ---------------------------------------------------------------------------

const FEATURES = [
  {
    icon: "⚡",
    ar: "محرك الإيرادات الذكي",
    en: "AI Revenue Engine",
    descAr: "تحليل مسارات الإيراد وكشف التسرّب بالوقت الفعلي.",
    descEn: "Real-time revenue pathway analysis and leakage detection.",
  },
  {
    icon: "📊",
    ar: "لوحة تحكم تحليلية",
    en: "Analytics Dashboard",
    descAr: "رؤية موحّدة لكل مؤشرات الأداء في مكان واحد.",
    descEn: "Unified KPI visibility across every revenue motion.",
  },
  {
    icon: "🛡️",
    ar: "امتثال PDPL و ZATCA",
    en: "PDPL & ZATCA Compliance",
    descAr: "جاهزية تلقائية لمتطلبات الفوترة الإلكترونية وحماية البيانات.",
    descEn: "Automated readiness for e-invoicing and data protection.",
  },
  {
    icon: "🤝",
    ar: "إدارة العملاء (CRM)",
    en: "CRM Management",
    descAr: "CRM محكوم بالبيانات مع audit log كامل.",
    descEn: "Data-governed CRM with full audit trail.",
  },
  {
    icon: "📋",
    ar: "تقارير مخصصة",
    en: "Custom Reports",
    descAr: "تقارير ثنائية اللغة قابلة للتصدير بضغطة واحدة.",
    descEn: "One-click bilingual exportable reports.",
  },
  {
    icon: "🤝",
    ar: "دعم مباشر من المؤسِّس",
    en: "Direct Founder Support",
    descAr: "تواصل مباشر مع المؤسِّس خلال مرحلة التأسيس — لا مراكز اتصال.",
    descEn: "Direct line to the founder during the founding stage — no call centers.",
  },
];

// Saudi B2B sectors Dealix is built to serve (real ICP — not customer logos).
const SECTORS = [
  { initials: "RE", ar: "العقار والمقاولات", en: "Real Estate & Construction" },
  { initials: "TS", ar: "التقنية و SaaS", en: "Technology & SaaS" },
  { initials: "PS", ar: "الخدمات المهنية", en: "Professional Services" },
  { initials: "B2", ar: "خدمات B2B", en: "B2B Services" },
  { initials: "FA", ar: "المالية والمحاسبة", en: "Finance & Accounting" },
  { initials: "HE", ar: "الضيافة والفعاليات", en: "Hospitality & Events" },
];

// Honest operating facts — capability, not unverified outcome metrics.
const STATS = [
  { valueAr: "٥", valueEn: "5", labelAr: "مستويات خدمة — من المجاني إلى المخصّص", labelEn: "Service tiers — free to custom" },
  { valueAr: "L0–L5", valueEn: "L0–L5", labelAr: "مستويات أدلة لكل قرار", labelEn: "Evidence levels per decision" },
  { valueAr: "١٠٠٪", valueEn: "100%", labelAr: "ثنائي اللغة عربي / إنجليزي", labelEn: "Bilingual Arabic / English" },
  { valueAr: "٠", valueEn: "0", labelAr: "إرسال خارجي بدون موافقتك", labelEn: "External sends without your approval" },
];

const PRICING = [
  {
    tierAr: "المبدئي",
    tierEn: "Starter",
    priceAr: "٤٩٩ ر.س",
    priceEn: "499 SAR",
    periodAr: "دفعة واحدة",
    periodEn: "one-time",
    featuresAr: ["تشخيص ٧ أيام", "Proof Pack PDF", "خريطة الإيراد", "تقرير ثنائي اللغة"],
    featuresEn: ["7-day diagnostic", "Proof Pack PDF", "Revenue map", "Bilingual report"],
    popular: false,
    ctaAr: "ابدأ الآن",
    ctaEn: "Get started",
    href: "/offer/lead-intelligence-sprint",
  },
  {
    tierAr: "النمو",
    tierEn: "Growth",
    priceAr: "٢,٩٩٩ ر.س",
    priceEn: "2,999 SAR",
    periodAr: "شهرياً",
    periodEn: "per month",
    featuresAr: ["كل ميزات المبدئي", "CRM محكوم", "تقارير أسبوعية", "دعم أولوية", "لوحة تحليلية", "امتثال ZATCA"],
    featuresEn: ["Everything in Starter", "Governed CRM", "Weekly reports", "Priority support", "Analytics dashboard", "ZATCA compliance"],
    popular: true,
    ctaAr: "احجز مكالمة",
    ctaEn: "Book a call",
    href: "/contact",
  },
  {
    tierAr: "المؤسسي",
    tierEn: "Enterprise",
    priceAr: "مخصص",
    priceEn: "Custom",
    periodAr: "",
    periodEn: "",
    featuresAr: ["كل ميزات النمو", "تكامل API مخصص", "مدير حساب مخصص", "SLA مضمون", "تدريب الفريق", "audit log كامل"],
    featuresEn: ["Everything in Growth", "Custom API integration", "Dedicated account manager", "Guaranteed SLA", "Team training", "Full audit log"],
    popular: false,
    ctaAr: "تحدث مع فريقنا",
    ctaEn: "Talk to our team",
    href: "/contact",
  },
];

// Why teams trust Dealix — operating principles, not fabricated testimonials.
const WHY_DEALIX = [
  {
    icon: "✅",
    ar: "الموافقة أولاً",
    en: "Approval-first",
    descAr: "لا رسالة ولا إجراء خارجي يُرسَل بدون موافقتك الصريحة. الذكاء الاصطناعي يحلّل ويقترح، وأنت تقرّر.",
    descEn: "No external message or action goes out without your explicit approval. AI analyzes and recommends — you decide.",
  },
  {
    icon: "🧾",
    ar: "أدلة لا وعود",
    en: "Evidence, not promises",
    descAr: "كل توصية مرفقة بسلسلة أدلة L0–L5 ومصدر يمكن تتبّعه — لا أرقام بلا مصدر ولا ضمانات بيع.",
    descEn: "Every recommendation carries an L0–L5 evidence chain with a traceable source — no source-less numbers, no sales guarantees.",
  },
  {
    icon: "🛡️",
    ar: "بياناتك تبقى لك",
    en: "Your data stays yours",
    descAr: "مبني على نظام حماية البيانات الشخصية (PDPL) أصلاً، مع سجل تدقيق كامل وحوكمة سعودية.",
    descEn: "PDPL-native by design, with a full audit trail and Saudi-first governance.",
  },
];

const TRUST_BADGES = [
  { icon: "🔒", ar: "ملتزمون بـ PDPL", en: "PDPL Compliant" },
  { icon: "🧾", ar: "جاهز لـ ZATCA", en: "ZATCA Ready" },
  { icon: "🇸🇦", ar: "صنع في السعودية", en: "Saudi-First" },
  { icon: "🚫", ar: "لا تسويق بارد آلي", en: "No Cold Outreach" },
  { icon: "📋", ar: "audit log كامل", en: "Full Audit Log" },
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
// Sub-components
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function CommercialLaunchHome() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";
  const base = `/${locale}`;

  const [email, setEmail] = useState("");
  const [emailSubmitted, setEmailSubmitted] = useState(false);

  const heroControls = useAnimation();
  const heroRef = useRef<HTMLDivElement>(null);
  const heroInView = useInView(heroRef, { once: true });

  useEffect(() => {
    if (heroInView) heroControls.start("visible");
  }, [heroInView, heroControls]);

  function handleEmailSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim()) setEmailSubmitted(true);
  }

  return (
    <div dir={dir} className="min-h-screen bg-navy-500 text-white overflow-x-hidden">
      {/* ------------------------------------------------------------------ */}
      {/* HERO                                                                */}
      {/* ------------------------------------------------------------------ */}
      <section
        ref={heroRef}
        className="relative min-h-screen flex flex-col items-center justify-center px-4 overflow-hidden"
        style={{ background: "linear-gradient(135deg, #001F3F 0%, #001830 40%, #000d1a 70%, #001020 100%)" }}
      >
        {/* Animated gradient orbs */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 overflow-hidden"
        >
          <motion.div
            animate={{ scale: [1, 1.15, 1], opacity: [0.18, 0.28, 0.18] }}
            transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -top-32 -left-32 w-[520px] h-[520px] rounded-full"
            style={{ background: "radial-gradient(circle, rgba(212,175,55,0.25) 0%, transparent 70%)" }}
          />
          <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.12, 0.22, 0.12] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            className="absolute bottom-0 right-0 w-[600px] h-[600px] rounded-full"
            style={{ background: "radial-gradient(circle, rgba(16,185,129,0.18) 0%, transparent 70%)" }}
          />
          <motion.div
            animate={{ x: [0, 30, 0], y: [0, -20, 0], opacity: [0.08, 0.14, 0.08] }}
            transition={{ duration: 12, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] rounded-full"
            style={{ background: "radial-gradient(ellipse, rgba(0,31,63,0.6) 0%, transparent 70%)" }}
          />
          {/* Floating particles */}
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute rounded-full bg-gold-400/20"
              style={{
                width: 4 + (i % 3) * 4,
                height: 4 + (i % 3) * 4,
                top: `${15 + i * 13}%`,
                left: `${10 + i * 14}%`,
              }}
              animate={{ y: [0, -18, 0], opacity: [0.2, 0.5, 0.2] }}
              transition={{ duration: 4 + i, repeat: Infinity, ease: "easeInOut", delay: i * 0.7 }}
            />
          ))}
        </div>

        {/* ZATCA countdown badge */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="relative z-10 mb-6"
        >
          <Badge className="border-gold-500/40 bg-gold-500/10 text-gold-300 text-xs px-4 py-1.5 rounded-full backdrop-blur-sm">
            <span className="inline-block w-2 h-2 rounded-full bg-gold-400 me-2 animate-pulse" />
            {isAr ? "ZATCA Wave 24 — الموعد النهائي يونيو 2026" : "ZATCA Wave 24 — Deadline June 2026"}
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
                  محرّك الإيرادات{" "}
                  <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                    بالذكاء الاصطناعي
                  </span>{" "}
                  للشركات السعودية
                </>
              ) : (
                <>
                  The{" "}
                  <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                    AI Revenue Engine
                  </span>{" "}
                  for Saudi Enterprises
                </>
              )}
            </motion.h1>

            <motion.p
              variants={fadeUp}
              custom={2}
              className="mt-5 text-base md:text-lg text-white/70 max-w-xl mx-auto leading-relaxed"
            >
              {isAr
                ? "كشف تسرّب الإيراد · حوكمة الذكاء الاصطناعي · امتثال ZATCA & PDPL — كل شيء في منصة واحدة محكومة بالدليل."
                : "Revenue leakage detection · AI governance · ZATCA & PDPL compliance — all in one evidence-governed platform."}
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
                <Link href={`${base}/offer/lead-intelligence-sprint`}>
                  {isAr ? "ابدأ تشخيصك المجاني" : "Start Free Diagnostic"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-white/20 text-white hover:bg-white/10 backdrop-blur-sm text-base h-13 px-8"
              >
                <Link href={`${base}/demo`}>
                  {isAr ? "شاهد كيف يعمل" : "See How It Works"}
                </Link>
              </Button>
            </motion.div>

            <motion.p
              variants={fadeUp}
              custom={4}
              className="mt-5 text-xs text-white/40"
            >
              {isAr
                ? "لا إرسال آلي · لا ادّعاء إيراد قبل الدفع · PDPL compliant"
                : "No automated outbound · No revenue claims before payment · PDPL compliant"}
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
      {/* SECTORS STRIP (built-for, not customer logos)                       */}
      {/* ------------------------------------------------------------------ */}
      <section className="bg-navy-600 border-y border-white/5 py-10 overflow-hidden">
        <p className="text-center text-xs font-semibold text-white/40 uppercase tracking-widest mb-6">
          {isAr ? "مبني لقطاعات B2B السعودية" : "Built for Saudi B2B sectors"}
        </p>
        <div className="relative">
          <motion.div
            className="flex gap-10 items-center"
            animate={{ x: isAr ? [0, "50%"] : [0, "-50%"] }}
            transition={{ duration: 22, repeat: Infinity, ease: "linear" }}
          >
            {[...SECTORS, ...SECTORS].map((sector, i) => (
              <div
                key={i}
                className="flex-shrink-0 flex items-center gap-3 px-6 py-3 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm"
              >
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-gold-500/30 to-gold-400/10 border border-gold-500/20 flex items-center justify-center text-gold-400 font-bold text-sm">
                  {sector.initials}
                </div>
                <span className="text-white/60 text-sm whitespace-nowrap font-medium">{isAr ? sector.ar : sector.en}</span>
              </div>
            ))}
          </motion.div>
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
            {isAr ? "كل ما تحتاجه لتنمية إيراداتك" : "Everything you need to grow revenue"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-xl mx-auto">
            {isAr
              ? "ست أدوات متكاملة تعمل معاً لتحقيق نتائج قابلة للقياس."
              : "Six integrated tools working together for measurable results."}
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
              <div className="text-3xl mb-4">{f.icon}</div>
              <h3 className="font-bold text-lg mb-0.5">{isAr ? f.ar : f.en}</h3>
              <p className="text-xs text-white/50 font-medium mb-2">{isAr ? f.en : f.ar}</p>
              <p className="text-sm text-white/65 leading-relaxed">{isAr ? f.descAr : f.descEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* ANIMATED STATS                                                      */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-20 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 50%, #000d1a 100%)" }}
      >
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="max-w-4xl mx-auto text-center mb-12"
        >
          <motion.h2 variants={fadeUp} className="text-3xl md:text-4xl font-bold">
            {isAr ? "مبنيّ على الحوكمة، لا على الوعود" : "Built on governance, not hype"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-white/60 max-w-xl mx-auto">
            {isAr
              ? "لا نعرض أرقام عملاء قبل وجودهم. هذه حقائق تشغيلية يمكنك التحقق منها اليوم."
              : "We don't show customer numbers before customers exist. These are operating facts you can verify today."}
          </motion.p>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto"
        >
          {STATS.map((s, i) => (
            <motion.div
              key={s.labelEn}
              variants={fadeUp}
              custom={i}
              className="text-center rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm py-8 px-4"
            >
              <div className="text-4xl md:text-5xl font-bold bg-gradient-to-br from-gold-300 to-gold-500 bg-clip-text text-transparent leading-none mb-3">
                {isAr ? s.valueAr : s.valueEn}
              </div>
              <p className="text-white/70 text-sm font-medium">{isAr ? s.labelAr : s.labelEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* PRICING                                                             */}
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
            {isAr ? "الأسعار" : "Pricing"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "خطة مناسبة لكل مرحلة" : "A plan for every stage"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-lg mx-auto">
            {isAr ? "ابدأ بتشخيص واحد، ثم قرر." : "Start with one diagnostic, then decide."}
          </motion.p>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-6 md:grid-cols-3 items-start"
        >
          {PRICING.map((plan, i) => (
            <motion.div
              key={plan.tierEn}
              variants={fadeUp}
              custom={i}
              className={`relative rounded-2xl border p-8 flex flex-col gap-5 ${
                plan.popular
                  ? "border-gold-500/50 bg-gradient-to-b from-gold-500/8 to-transparent shadow-xl shadow-gold-500/10"
                  : "border-white/8 bg-white/4"
              } backdrop-blur-sm`}
              style={plan.popular ? { boxShadow: "0 0 40px rgba(212,175,55,0.12), inset 0 1px 0 rgba(255,255,255,0.07)" } : {}}
            >
              {plan.popular && (
                <div className={`absolute -top-3.5 ${isAr ? "left-6" : "right-6"}`}>
                  <Badge className="bg-gold-500 text-navy-500 border-0 font-bold px-3 py-1 text-xs">
                    {isAr ? "الأكثر شيوعاً" : "Most Popular"}
                  </Badge>
                </div>
              )}

              <div>
                <p className="text-white/50 text-sm font-medium mb-1">{isAr ? plan.tierAr : plan.tierEn}</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold">{isAr ? plan.priceAr : plan.priceEn}</span>
                  {plan.periodAr && (
                    <span className="text-white/50 text-sm">{isAr ? plan.periodAr : plan.periodEn}</span>
                  )}
                </div>
              </div>

              <ul className="space-y-2.5 flex-1">
                {(isAr ? plan.featuresAr : plan.featuresEn).map((feat) => (
                  <li key={feat} className="flex items-start gap-2 text-sm text-white/75">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0 text-base leading-none">✓</span>
                    {feat}
                  </li>
                ))}
              </ul>

              <Button
                asChild
                size="lg"
                className={`w-full font-semibold ${
                  plan.popular
                    ? "bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 hover:from-gold-400 hover:to-gold-300 shadow-md shadow-gold-500/20"
                    : "bg-white/8 border border-white/15 text-white hover:bg-white/14"
                }`}
              >
                <Link href={`${base}${plan.href}`}>
                  {isAr ? plan.ctaAr : plan.ctaEn}
                </Link>
              </Button>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* WHY DEALIX — operating principles + founding-customer band          */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-20 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 100%)" }}
      >
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          className="max-w-6xl mx-auto"
        >
          <motion.div variants={fadeUp} className="text-center mb-12">
            <p className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
              {isAr ? "لماذا Dealix" : "Why Dealix"}
            </p>
            <h2 className="text-3xl md:text-4xl font-bold">
              {isAr ? "الثقة مبنية على الحوكمة" : "Trust, built on governance"}
            </h2>
          </motion.div>

          <motion.div
            variants={stagger}
            className="grid gap-6 md:grid-cols-3"
          >
            {WHY_DEALIX.map((w, i) => (
              <motion.div
                key={w.en}
                variants={fadeUp}
                custom={i}
                className="rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-7 flex flex-col gap-3"
                style={{ boxShadow: "inset 0 1px 0 rgba(255,255,255,0.05)" }}
              >
                <div className="text-3xl">{w.icon}</div>
                <h3 className="font-bold text-lg leading-tight">{isAr ? w.ar : w.en}</h3>
                <p className="text-xs text-white/45 font-medium -mt-1.5">{isAr ? w.en : w.ar}</p>
                <p className="text-sm text-white/70 leading-relaxed">{isAr ? w.descAr : w.descEn}</p>
              </motion.div>
            ))}
          </motion.div>

          {/* Honest founding-customer band — no fabricated social proof */}
          <motion.div
            variants={fadeUp}
            custom={3}
            className="mt-10 rounded-2xl border border-gold-500/25 bg-gradient-to-b from-gold-500/8 to-transparent p-7 md:p-9 text-center"
          >
            <p className="text-gold-300 text-xs font-semibold uppercase tracking-widest mb-2">
              {isAr ? "عملاء التأسيس" : "Founding customers"}
            </p>
            <h3 className="text-xl md:text-2xl font-bold mb-2">
              {isAr ? "كن من أوائل من نوثّق نتائجهم" : "Be among the first results we document"}
            </h3>
            <p className="text-white/65 text-sm max-w-2xl mx-auto leading-relaxed mb-5">
              {isAr
                ? "نحن في مرحلة التأسيس ولا نعرض شهادات أو أرقام عملاء لا وجود لهم. ابدأ بتشخيص مجاني، واحصل على Proof Pack موثّق بالأدلة — ونحوّل نتيجتك إلى أول دراسة حالة (بموافقتك فقط)."
                : "We're at the founding stage and won't show testimonials or customer numbers that don't exist. Start with a free diagnostic, get an evidence-backed Proof Pack — and we turn your result into our first case study (only with your consent)."}
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Button
                asChild
                size="lg"
                className="w-full sm:w-auto bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300"
              >
                <Link href={`${base}/offer/lead-intelligence-sprint`}>
                  {isAr ? "ابدأ تشخيصك المجاني" : "Start free diagnostic"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-white/20 text-white hover:bg-white/10"
              >
                <Link href={`${base}/contact`}>
                  {isAr ? "تحدّث مع المؤسِّس" : "Talk to the founder"}
                </Link>
              </Button>
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* TRUST CENTER STRIP                                                  */}
      {/* ------------------------------------------------------------------ */}
      <section className="py-10 px-4 border-y border-white/5 bg-navy-600 overflow-x-auto">
        <div className="flex gap-4 justify-start md:justify-center min-w-max mx-auto px-2">
          {TRUST_BADGES.map((badge) => (
            <div
              key={badge.en}
              className="flex items-center gap-2 px-5 py-3 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm flex-shrink-0"
            >
              <span className="text-xl">{badge.icon}</span>
              <span className="text-sm font-medium text-white/80 whitespace-nowrap">
                {isAr ? badge.ar : badge.en}
              </span>
            </div>
          ))}
        </div>
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
                ابدأ رحلتك نحو{" "}
                <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                  إيراد أكثر
                </span>
              </>
            ) : (
              <>
                Start your journey to{" "}
                <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
                  more revenue
                </span>
              </>
            )}
          </motion.h2>

          <motion.p variants={fadeUp} custom={1} className="text-white/60 mb-8 text-lg">
            {isAr
              ? "أدخل بريدك الإلكتروني واحصل على تقرير تشخيصي مجاني خلال 48 ساعة."
              : "Enter your email and get a free diagnostic report within 48 hours."}
          </motion.p>

          <motion.form
            variants={fadeUp}
            custom={2}
            onSubmit={handleEmailSubmit}
            className={`flex flex-col sm:flex-row gap-3 max-w-md mx-auto ${isAr ? "sm:flex-row-reverse" : ""}`}
          >
            <AnimatePresence mode="wait">
              {!emailSubmitted ? (
                <motion.div
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col sm:flex-row gap-3 w-full"
                >
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder={isAr ? "البريد الإلكتروني للشركة" : "Work email address"}
                    className="flex-1 h-12 rounded-xl bg-white/8 border border-white/15 px-4 text-white placeholder-white/40 text-sm focus:outline-none focus:border-gold-500/60 focus:bg-white/12 transition-colors"
                  />
                  <Button
                    type="submit"
                    size="lg"
                    className="h-12 px-7 bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 whitespace-nowrap shadow-lg shadow-gold-500/25"
                  >
                    {isAr ? "ابدأ مجاناً" : "Start Free"}
                  </Button>
                </motion.div>
              ) : (
                <motion.div
                  key="thanks"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="w-full text-center py-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 font-medium text-sm"
                >
                  {isAr ? "تم الاستلام — سنتواصل معك خلال 48 ساعة." : "Received — we'll be in touch within 48 hours."}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.form>

          <motion.p variants={fadeUp} custom={3} className="mt-4 text-xs text-white/35">
            {isAr
              ? "لا بريد عشوائي. بياناتك محمية وفق PDPL. يمكنك إلغاء الاشتراك في أي وقت."
              : "No spam. Your data is protected under PDPL. Unsubscribe anytime."}
          </motion.p>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* FOOTER                                                              */}
      {/* ------------------------------------------------------------------ */}
      <footer
        className="py-12 px-4 border-t border-white/6"
        style={{ background: "#000d1a" }}
      >
        <div className="max-w-6xl mx-auto">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 mb-10">
            {/* Brand */}
            <div className="lg:col-span-2">
              <div className="text-xl font-bold bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent mb-3">
                Dealix
              </div>
              <p className="text-white/50 text-sm leading-relaxed max-w-xs">
                {isAr
                  ? "منصة الإيرادات بالذكاء الاصطناعي للشركات السعودية. محكومة بالدليل، ملتزمة بـ PDPL."
                  : "AI revenue platform for Saudi enterprises. Evidence-governed, PDPL compliant."}
              </p>
            </div>

            {/* Links */}
            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "المنتج" : "Product"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "التشخيص", en: "Diagnostic", href: "/dealix-diagnostic" },
                  { ar: "Proof Pack", en: "Proof Pack", href: "/proof-pack" },
                  { ar: "الأسعار", en: "Pricing", href: "#pricing" },
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

            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "الشركة" : "Company"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "من نحن", en: "About", href: "/about" },
                  { ar: "تواصل معنا", en: "Contact", href: "/contact" },
                  { ar: "سياسة الخصوصية", en: "Privacy", href: "/privacy" },
                  { ar: "الشروط والأحكام", en: "Terms", href: "/terms" },
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
