"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

import { motion, useInView, useAnimation } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Static data — HONEST by design.
// Dealix is pre-revenue / founding-cohort. We never display invented client
// logos, fabricated metrics, or un-sourced testimonials (doctrine #4/#5).
// Everything below is a true capability, a stated promise, or a sector focus.
// ---------------------------------------------------------------------------

const FEATURES = [
  {
    icon: "⚡",
    ar: "محرك الإيرادات الذكي",
    en: "AI Revenue Engine",
    descAr: "تحليل مسارات الإيراد وكشف التسرّب — كل إشارة لها مصدر موثّق.",
    descEn: "Revenue pathway analysis and leakage detection — every signal sourced.",
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
    descAr: "جاهزية مدمجة لمتطلبات الفوترة الإلكترونية وحماية البيانات.",
    descEn: "Built-in readiness for e-invoicing and data protection.",
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
    ar: "Proof Pack بالأدلة",
    en: "Evidence Proof Pack",
    descAr: "تقارير ثنائية اللغة بمستويات أدلة L0–L5 قابلة للتصدير.",
    descEn: "Bilingual reports with L0–L5 evidence levels, exportable.",
  },
  {
    icon: "✅",
    ar: "موافقة بشرية أولاً",
    en: "Human Approval First",
    descAr: "لا إجراء خارجي بدون موافقة — لا أتمتة عمياء.",
    descEn: "No external action without approval — no blind automation.",
  },
];

// Sector focus (ICP) — these are the markets we build for, NOT a client list.
const SECTORS = [
  { code: "AG", ar: "وكالات تسويق وإعلان", en: "Marketing & ad agencies" },
  { code: "CN", ar: "المقاولات والإنشاءات", en: "Contracting & construction" },
  { code: "PS", ar: "الخدمات المهنية", en: "Professional services" },
  { code: "TR", ar: "التجارة والتوزيع", en: "Trade & distribution" },
  { code: "TC", ar: "التقنية و SaaS", en: "Tech & SaaS" },
  { code: "LG", ar: "اللوجستيات", en: "Logistics" },
];

// Honest capability stats — promises and true capabilities, not customer metrics.
const STATS = [
  { numeric: 5, suffix: "", labelAr: "مستويات خدمة واضحة", labelEn: "Clear service tiers" },
  { numeric: 48, suffix: "h", labelAr: "تسليم أول تشخيص", labelEn: "First diagnostic turnaround" },
  { text: "AR+EN", labelAr: "ثنائي اللغة بالكامل", labelEn: "Fully bilingual" },
  { numeric: 100, suffix: "%", labelAr: "إجراءات بموافقة بشرية", labelEn: "Human-approved actions" },
];

// How it works — the real methodology (replaces fabricated testimonials).
const STEPS = [
  {
    n: "1",
    ar: { t: "شخّص", d: "Risk Score مجاني في 5 دقائق، ثم تشخيص محكوم خلال 48 ساعة يكشف أين تتسرّب الفرص." },
    en: { t: "Diagnose", d: "Free 5-minute Risk Score, then a governed 48-hour diagnostic that shows where opportunities leak." },
  },
  {
    n: "2",
    ar: { t: "أثبت", d: "Proof Pack ثنائي اللغة بمستويات أدلة L0–L5 — كل رقم له مصدر، لا ادعاءات بلا دليل." },
    en: { t: "Prove", d: "Bilingual Proof Pack with L0–L5 evidence levels — every number sourced, no un-evidenced claims." },
  },
  {
    n: "3",
    ar: { t: "شغّل", d: "تشغيل مُدار شهري يبدأ فقط بعد إثبات القيمة — وموافقة بشرية على كل خطوة." },
    en: { t: "Operate", d: "Monthly managed ops that starts only after value is proven — human approval at every step." },
  },
];

const PRICING = [
  {
    tierAr: "المبدئي",
    tierEn: "Starter",
    priceAr: "٤٩٩ ر.س",
    priceEn: "499 SAR",
    periodAr: "دفعة واحدة",
    periodEn: "one-time",
    featuresAr: ["تشخيص Revenue Intelligence", "مراجعة 10 leads حقيقية", "مسودة Proof Pack", "تقرير ثنائي اللغة"],
    featuresEn: ["Revenue Intelligence diagnostic", "10 real leads reviewed", "Proof Pack draft", "Bilingual report"],
    popular: false,
    ctaAr: "ابدأ Sprint",
    ctaEn: "Start Sprint",
    href: "/offer/lead-intelligence-sprint",
  },
  {
    tierAr: "التشغيل المُدار",
    tierEn: "Managed Ops",
    priceAr: "من ٢,٩٩٩ ر.س",
    priceEn: "from 2,999 SAR",
    periodAr: "شهرياً",
    periodEn: "per month",
    featuresAr: ["كل ما في المبدئي", "OKR أسبوعي محكوم", "Proof Pack شهري", "دعم أولوية SLA 48س", "Approval Center", "امتثال ZATCA و PDPL"],
    featuresEn: ["Everything in Starter", "Governed weekly OKR", "Monthly Proof Pack", "Priority 48h SLA support", "Approval Center", "ZATCA & PDPL compliance"],
    popular: true,
    ctaAr: "شاهد المستويات",
    ctaEn: "See the tiers",
    href: "/services",
  },
  {
    tierAr: "AI مخصص",
    tierEn: "Custom AI",
    priceAr: "٥٬٠٠٠ – ٢٥٬٠٠٠ ر.س",
    priceEn: "5,000 – 25,000 SAR",
    periodAr: "حسب النطاق",
    periodEn: "by scope",
    featuresAr: ["Scope مُحدَّد ومُوقَّع", "تطوير AI مخصص مع audit trail", "Approval Center لكل خطوة", "Proof Pack ختامي", "SLA واضح", "تدريب الفريق"],
    featuresEn: ["Defined, signed scope", "Custom AI build with audit trail", "Approval Center at each step", "Final Proof Pack", "Defined SLA", "Team training"],
    popular: false,
    ctaAr: "ناقش مشروعك",
    ctaEn: "Discuss your project",
    href: "/custom-ai",
  },
];

const TRUST_BADGES = [
  { icon: "✅", ar: "نتائج موثّقة فقط", en: "Verified results only" },
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

function AnimatedNumber({ target, suffix = "" }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  useEffect(() => {
    if (!inView) return;
    const duration = 1600;
    const steps = 48;
    const increment = target / steps;
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + increment, target);
      setCount(Math.round(current * 10) / 10);
      if (current >= target) clearInterval(timer);
    }, duration / steps);
    return () => clearInterval(timer);
  }, [inView, target]);

  return (
    <span ref={ref}>
      {count % 1 === 0 ? count.toFixed(0) : count.toFixed(1)}
      {suffix}
    </span>
  );
}

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
      {/* TOP NAV                                                             */}
      {/* ------------------------------------------------------------------ */}
      <header className="absolute top-0 inset-x-0 z-30">
        <div className="mx-auto max-w-6xl px-5 py-4 flex items-center justify-between">
          <Link href={base} className="text-lg font-bold bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
            Dealix
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-sm text-white/70">
            <Link href={`${base}/services`} className="hover:text-gold-300 transition-colors">{isAr ? "الخدمات" : "Services"}</Link>
            <Link href={`${base}/pricing`} className="hover:text-gold-300 transition-colors">{isAr ? "الأسعار" : "Pricing"}</Link>
            <Link href={`${base}/trust-center`} className="hover:text-gold-300 transition-colors">{isAr ? "الثقة" : "Trust"}</Link>
            <Link href={`${base}/about`} className="hover:text-gold-300 transition-colors">{isAr ? "من نحن" : "About"}</Link>
          </nav>
          <Link
            href={`${base}/risk-score`}
            className="rounded-full bg-white/10 border border-white/15 px-4 py-1.5 text-sm font-medium hover:bg-white/15 transition-colors"
          >
            {isAr ? "تشخيص مجاني" : "Free diagnostic"}
          </Link>
        </div>
      </header>

      {/* ------------------------------------------------------------------ */}
      {/* HERO                                                                */}
      {/* ------------------------------------------------------------------ */}
      <section
        ref={heroRef}
        className="relative min-h-screen flex flex-col items-center justify-center px-4 overflow-hidden"
        style={{ background: "linear-gradient(135deg, #001F3F 0%, #001830 40%, #000d1a 70%, #001020 100%)" }}
      >
        {/* Animated gradient orbs */}
        <div aria-hidden className="pointer-events-none absolute inset-0 overflow-hidden">
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
                ? "كشف تسرّب الإيراد · حوكمة الذكاء الاصطناعي · امتثال ZATCA و PDPL — كل شيء في منصة واحدة محكومة بالدليل."
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
                <Link href={`${base}/risk-score`}>
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

            <motion.p variants={fadeUp} custom={4} className="mt-5 text-xs text-white/40">
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
      {/* SECTOR FOCUS STRIP (built for — NOT a client list)                  */}
      {/* ------------------------------------------------------------------ */}
      <section className="bg-navy-600 border-y border-white/5 py-10 overflow-hidden">
        <p className="text-center text-xs font-semibold text-white/40 uppercase tracking-widest mb-6">
          {isAr ? "مبني لقطاعات B2B السعودية" : "Built for Saudi B2B sectors"}
        </p>
        <div className="relative">
          <motion.div
            className="flex gap-10 items-center"
            animate={{ x: isAr ? [0, "50%"] : [0, "-50%"] }}
            transition={{ duration: 26, repeat: Infinity, ease: "linear" }}
          >
            {[...SECTORS, ...SECTORS].map((s, i) => (
              <div
                key={i}
                className="flex-shrink-0 flex items-center gap-3 px-6 py-3 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm"
              >
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-gold-500/30 to-gold-400/10 border border-gold-500/20 flex items-center justify-center text-gold-400 font-bold text-sm">
                  {s.code}
                </div>
                <span className="text-white/60 text-sm whitespace-nowrap font-medium">{isAr ? s.ar : s.en}</span>
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
              ? "ست قدرات متكاملة تعمل معاً لتحقيق نتائج قابلة للقياس والتدقيق."
              : "Six integrated capabilities working together for measurable, auditable results."}
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
      {/* CAPABILITY STATS (honest — promises & capabilities, not metrics)    */}
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
            {isAr ? "بُني على الحوكمة لا على الوعود" : "Built on governance, not promises"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-white/60 max-w-xl mx-auto">
            {isAr
              ? "لا نعرض أرقام عملاء مُختلقة. هذه قدراتنا والتزاماتنا الحقيقية."
              : "We don't show invented customer metrics. These are our real capabilities and commitments."}
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
                {typeof s.numeric === "number" ? (
                  <AnimatedNumber target={s.numeric} suffix={s.suffix} />
                ) : (
                  <span>{s.text}</span>
                )}
              </div>
              <p className="text-white/70 text-sm font-medium">{isAr ? s.labelAr : s.labelEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* HOW IT WORKS (replaces fabricated testimonials)                     */}
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
            {isAr ? "كيف يعمل" : "How it works"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "شخّص · أثبت · شغّل" : "Diagnose · Prove · Operate"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-xl mx-auto">
            {isAr
              ? "كل درجة تفتح فقط بعد دليل حقيقي من الدرجة السابقة. لا توسّع قبل الإثبات."
              : "Each rung unlocks only after real evidence from the one below. No expansion before proof."}
          </motion.p>
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
              key={step.n}
              variants={fadeUp}
              custom={i}
              className="rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-7"
              style={{ boxShadow: "inset 0 1px 0 rgba(255,255,255,0.05)" }}
            >
              <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-gold-500/30 to-gold-400/10 border border-gold-500/20 flex items-center justify-center text-gold-300 font-bold text-lg mb-4">
                {step.n}
              </div>
              <h3 className="font-bold text-lg mb-2">{isAr ? step.ar.t : step.en.t}</h3>
              <p className="text-sm text-white/65 leading-relaxed">{isAr ? step.ar.d : step.en.d}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* FOUNDING COHORT (honest scarcity — replaces fake social proof)      */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-16 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 100%)" }}
      >
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5 }}
          className="max-w-3xl mx-auto rounded-2xl border border-gold-500/20 bg-gradient-to-b from-gold-500/8 to-transparent p-8 text-center"
        >
          <Badge className="border-gold-500/40 bg-gold-500/10 text-gold-300 text-xs px-4 py-1.5 rounded-full mb-4">
            {isAr ? "الدفعة التأسيسية 2026" : "Founding cohort 2026"}
          </Badge>
          <h2 className="text-2xl md:text-3xl font-bold mb-4">
            {isAr ? "كن من أوائل عملائنا في السعودية" : "Be among our first clients in Saudi Arabia"}
          </h2>
          <p className="text-white/65 leading-relaxed max-w-2xl mx-auto">
            {isAr
              ? "Dealix شركة سعودية حديثة. نحن صريحون: لا نعرض شعارات عملاء وهمية ولا أرقاماً مُختلقة. عملاء الدفعة التأسيسية يحصلون على تسليم بإشراف المؤسس مباشرة، ويساعدون في تشكيل المنتج — وننشر نتائجهم فقط بعد توثيقها وبموافقتهم."
              : "Dealix is a new Saudi venture. We're transparent: no invented client logos, no fabricated numbers. Founding-cohort clients get founder-led delivery, help shape the product — and we publish their results only once documented and with their consent."}
          </p>
          <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
            <Button asChild size="lg" className="bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 shadow-lg shadow-gold-500/25">
              <Link href={`${base}/risk-score`}>{isAr ? "ابدأ بتشخيص مجاني" : "Start with a free diagnostic"}</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <Link href={`${base}/contact`}>{isAr ? "تحدّث مع المؤسس" : "Talk to the founder"}</Link>
            </Button>
          </div>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* PRICING                                                             */}
      {/* ------------------------------------------------------------------ */}
      <section id="pricing" className="py-20 px-4 max-w-6xl mx-auto">
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
            {isAr ? "ابدأ بتشخيص واحد، ثم قرر — لا upsell بدون Proof Pack مُسلَّم." : "Start with one diagnostic, then decide — no upsell without a delivered Proof Pack."}
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
                    {isAr ? "الأكثر طلباً" : "Most Popular"}
                  </Badge>
                </div>
              )}

              <div>
                <p className="text-white/50 text-sm font-medium mb-1">{isAr ? plan.tierAr : plan.tierEn}</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold">{isAr ? plan.priceAr : plan.priceEn}</span>
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

        <p className="mt-8 text-center text-sm text-white/50">
          <Link href={`${base}/services`} className="text-gold-400 hover:underline font-medium">
            {isAr ? "شاهد كل المستويات الخمسة ←" : "See all five service tiers →"}
          </Link>
        </p>
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
              ? "ابدأ بـ Risk Score مجاني خلال 5 دقائق — أو تحدّث معنا مباشرة."
              : "Start with a free 5-minute Risk Score — or talk to us directly."}
          </motion.p>

          <motion.div variants={fadeUp} custom={2} className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button
              asChild
              size="lg"
              className="h-12 px-7 bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 shadow-lg shadow-gold-500/25"
            >
              <Link href={`${base}/risk-score`}>{isAr ? "احسب Risk Score مجاناً" : "Get my free Risk Score"}</Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="h-12 px-7 border-white/20 text-white hover:bg-white/10"
            >
              <Link href={`${base}/contact`}>{isAr ? "تواصل معنا" : "Contact us"}</Link>
            </Button>
          </motion.div>

          <motion.p variants={fadeUp} custom={3} className="mt-4 text-xs text-white/35">
            {isAr
              ? "لا بطاقة ائتمان. بياناتك محمية وفق PDPL."
              : "No credit card. Your data is protected under PDPL."}
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
                  ? "منصة الإيرادات بالذكاء الاصطناعي للشركات السعودية. محكومة بالدليل، ملتزمة بـ PDPL."
                  : "AI revenue platform for Saudi enterprises. Evidence-governed, PDPL compliant."}
              </p>
            </div>

            {/* Product links */}
            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "المنتج" : "Product"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "الخدمات", en: "Services", href: "/services" },
                  { ar: "التشخيص", en: "Diagnostic", href: "/dealix-diagnostic" },
                  { ar: "Proof Pack", en: "Proof Pack", href: "/proof-pack" },
                  { ar: "AI مخصص", en: "Custom AI", href: "/custom-ai" },
                  { ar: "الأسعار", en: "Pricing", href: "/pricing" },
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

            {/* Company links */}
            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "الشركة" : "Company"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "من نحن", en: "About", href: "/about" },
                  { ar: "مركز الثقة", en: "Trust Center", href: "/trust-center" },
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
