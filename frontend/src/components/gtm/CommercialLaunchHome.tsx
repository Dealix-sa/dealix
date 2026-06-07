"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

import { motion, useInView, useAnimation } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LocaleToggle } from "@/components/layout/LocaleToggle";

// ---------------------------------------------------------------------------
// Static data — honest, no fabricated clients / metrics / testimonials.
// Every claim here is true about the platform itself, not invented results.
// ---------------------------------------------------------------------------

const FEATURES = [
  {
    icon: "⚡",
    ar: "محرك الإيرادات الذكي",
    en: "AI Revenue Engine",
    descAr: "تحليل مسارات الإيراد وكشف نقاط التسرّب المحتملة بالأدلة.",
    descEn: "Evidence-based revenue pathway analysis and leakage detection.",
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
    descAr: "CRM محكوم بالبيانات مع سجل تدقيق كامل.",
    descEn: "Data-governed CRM with full audit trail.",
  },
  {
    icon: "📋",
    ar: "تقارير ثنائية اللغة",
    en: "Bilingual Reports",
    descAr: "تقارير عربية وإنجليزية قابلة للتصدير بضغطة واحدة.",
    descEn: "One-click exportable Arabic & English reports.",
  },
  {
    icon: "🔒",
    ar: "حوكمة بالموافقة أولاً",
    en: "Approval-First Governance",
    descAr: "لا إجراء خارجي بدون موافقة بشرية — كل خطوة موثّقة.",
    descEn: "No external action without human approval — every step logged.",
  },
];

// Replaces the previous fabricated "Trusted by" client logos.
// These are the Saudi B2B sectors Dealix is built for — a design fact,
// not a claim of existing customers.
const SECTORS = [
  { ar: "العقار والتطوير", en: "Real Estate & Development", icon: "🏗️" },
  { ar: "المقاولات وإدارة المشاريع", en: "Contracting & Project Mgmt", icon: "📐" },
  { ar: "إدارة المرافق والصيانة", en: "Facilities & Maintenance", icon: "🔧" },
  { ar: "الخدمات الاحترافية B2B", en: "Professional B2B Services", icon: "💼" },
  { ar: "التقنية و SaaS", en: "Technology & SaaS", icon: "💻" },
  { ar: "الضيافة والفعاليات", en: "Hospitality & Events", icon: "🏨" },
];

// Replaces the previous fabricated metrics (500 clients / 3.2x / 99.9%).
// Every figure below is a verifiable property of the product, not a result.
const STATS = [
  { kind: "num", value: 7, suffix: "", labelAr: "أيام للتشخيص", labelEn: "Days to diagnostic" },
  { kind: "num", value: 8, suffix: "", labelAr: "بوابات حوكمة صارمة", labelEn: "Immutable governance gates" },
  { kind: "text", textAr: "ع+إ", textEn: "AR+EN", labelAr: "تقارير ثنائية اللغة", labelEn: "Bilingual deliverables" },
  { kind: "text", textAr: "PDPL", textEn: "PDPL", labelAr: "أصلاً في التصميم", labelEn: "Native by design" },
];

// The custom / high-ticket systems (mirrors os/03_OFFERS.yml). This is the
// "عندي كوستم وش يبي نسوي" surface — a real catalog, not a teaser.
const CUSTOM_SYSTEMS = [
  { icon: "🔧", ar: "نظام ذكاء الصيانة", en: "Maintenance Intelligence OS", descAr: "بلاغات، SLA، فنيون، وتقارير تُولَّد تلقائياً.", descEn: "Tickets, SLA, technicians and auto-generated reports." },
  { icon: "📐", ar: "نظام التحكم بالمشاريع", en: "Project Controls AI OS", descAr: "متابعة المخاطر، التقدّم، الموافقات، وطلبات التغيير.", descEn: "Risk, progress, approvals and change-request tracking." },
  { icon: "📚", ar: "المعرفة السيادية (RAG)", en: "Sovereign Knowledge / RAG", descAr: "مساعد داخلي على وثائقكم — آمن ومتحكَّم به.", descEn: "Internal assistant over your docs — secure & controlled." },
  { icon: "🧭", ar: "مركز القيادة التنفيذي", en: "Executive Command Center", descAr: "لوحة واحدة للمخاطر والأداء والقرارات.", descEn: "One board for risk, performance and decisions." },
  { icon: "🚀", ar: "نظام AI للإيرادات", en: "Revenue AI OS", descAr: "بحث، تواصل مُسوّد، ومتابعة بموافقتكم.", descEn: "Research, drafted outreach and follow-up — you approve." },
  { icon: "⚖️", ar: "حزمة حوكمة الذكاء الاصطناعي", en: "AI Governance Pack", descAr: "سياسات، صلاحيات، وبوابات موافقة قابلة للتدقيق.", descEn: "Policies, permissions and auditable approval gates." },
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
    ctaAr: "تحدث معنا",
    ctaEn: "Talk to us",
    href: "/contact?plan=growth",
  },
  {
    tierAr: "المؤسسي / المخصص",
    tierEn: "Enterprise / Custom",
    priceAr: "مخصص",
    priceEn: "Custom",
    periodAr: "",
    periodEn: "",
    featuresAr: ["أنظمة AI مخصّصة بالكامل", "تكامل API مخصص", "مدير حساب مخصص", "SLA مضمون", "تدريب الفريق", "سجل تدقيق كامل"],
    featuresEn: ["Fully bespoke AI systems", "Custom API integration", "Dedicated account manager", "Guaranteed SLA", "Team training", "Full audit log"],
    popular: false,
    ctaAr: "صمّم نظامك",
    ctaEn: "Design your system",
    href: "/custom",
  },
];

const HOW_IT_WORKS = [
  {
    n: "1",
    ar: "تشخيص محكوم بالأدلة",
    en: "Evidence-governed diagnostic",
    descAr: "خلال ٧ أيام نكشف أين يتسرّب الإيراد ونحدّد فرص الـ AI العملية في سير عملكم.",
    descEn: "In 7 days we map where revenue leaks and pinpoint practical AI opportunities in your workflow.",
  },
  {
    n: "2",
    ar: "Proof Pack وخطة Pilot",
    en: "Proof Pack & pilot plan",
    descAr: "تسليم ثنائي اللغة مع عائد مُقدّر (تقدير صريح) وخطة تجربة واقعية محدّدة.",
    descEn: "A bilingual deliverable with clearly-flagged estimated ROI and a concrete, realistic pilot plan.",
  },
  {
    n: "3",
    ar: "تنفيذ بموافقتك",
    en: "Execute with your approval",
    descAr: "نبني ونشغّل النظام — وكل إجراء خارجي يمرّ بموافقة بشرية منكم. لا مفاجآت.",
    descEn: "We build and run the system — every external action passes your human approval. No surprises.",
  },
];

const TRUST_BADGES = [
  { icon: "🔒", ar: "ملتزمون بـ PDPL", en: "PDPL Compliant" },
  { icon: "🧾", ar: "جاهز لـ ZATCA", en: "ZATCA Ready" },
  { icon: "🇸🇦", ar: "صنع في السعودية", en: "Saudi-First" },
  { icon: "🚫", ar: "لا تسويق بارد آلي", en: "No Cold Outreach" },
  { icon: "📋", ar: "سجل تدقيق كامل", en: "Full Audit Log" },
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
    const duration = 1400;
    const steps = 40;
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

/** Real email capture — posts to the same-origin lead route, which forwards
 *  to the backend founder lead-inbox. Degrades to a Calendly fallback. */
function EmailCapture({ source, isAr, locale }: { source: string; isAr: boolean; locale: string }) {
  const [email, setEmail] = useState("");
  const [website, setWebsite] = useState(""); // honeypot
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const [calendly, setCalendly] = useState("");
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!email.trim()) return;
    setBusy(true);
    setError("");
    try {
      const res = await fetch("/api/early-access", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source, locale, website }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || data.ok === false) {
        throw new Error(data.detail || "failed");
      }
      setCalendly(data.calendly_url || "");
      setDone(true);
    } catch {
      setError(isAr ? "تعذّر الإرسال — حاول مجدداً." : "Couldn't submit — please try again.");
    } finally {
      setBusy(false);
    }
  }

  if (done) {
    return (
      <div className="w-full text-center py-4 px-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 text-sm">
        <p className="font-medium">
          {isAr ? "تم الاستلام — سنتواصل معك قريبًا." : "Received — we'll be in touch shortly."}
        </p>
        {calendly && (
          <a
            href={calendly}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-2 text-gold-300 underline underline-offset-4 hover:text-gold-200"
          >
            {isAr ? "أو احجز مكالمة الآن ←" : "Or book a call now →"}
          </a>
        )}
      </div>
    );
  }

  return (
    <form onSubmit={submit} className="flex flex-col sm:flex-row gap-3 w-full">
      {/* honeypot — visually hidden */}
      <input
        type="text"
        tabIndex={-1}
        autoComplete="off"
        value={website}
        onChange={(e) => setWebsite(e.target.value)}
        className="hidden"
        aria-hidden
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        placeholder={isAr ? "البريد الإلكتروني للعمل" : "Work email address"}
        className="flex-1 h-12 rounded-xl bg-white/8 border border-white/15 px-4 text-white placeholder-white/40 text-sm focus:outline-none focus:border-gold-500/60 focus:bg-white/12 transition-colors"
      />
      <Button
        type="submit"
        size="lg"
        disabled={busy}
        className="h-12 px-7 bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 whitespace-nowrap shadow-lg shadow-gold-500/25"
      >
        {busy ? (isAr ? "جارٍ..." : "...") : isAr ? "ابدأ مجاناً" : "Start Free"}
      </Button>
      {error && (
        <p className="w-full text-xs text-red-300 mt-1 sm:absolute sm:mt-14">{error}</p>
      )}
    </form>
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

  const navLinks = [
    { ar: "الخدمات", en: "Services", href: `${base}/services` },
    { ar: "الحلول المخصصة", en: "Custom AI", href: `${base}/custom` },
    { ar: "الأسعار", en: "Pricing", href: "#pricing" },
    { ar: "التشخيص", en: "Diagnostic", href: `${base}/dealix-diagnostic` },
    { ar: "تواصل", en: "Contact", href: `${base}/contact` },
  ];

  return (
    <div dir={dir} className="min-h-screen bg-navy-500 text-white overflow-x-hidden">
      {/* ------------------------------------------------------------------ */}
      {/* NAV                                                                 */}
      {/* ------------------------------------------------------------------ */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-navy-500/80 backdrop-blur-md">
        <div className="mx-auto max-w-6xl px-4 h-16 flex items-center justify-between gap-4">
          <Link
            href={base}
            className="text-xl font-bold bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent"
          >
            Dealix
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-sm">
            {navLinks.map((l) => (
              <Link
                key={l.en}
                href={l.href}
                className="text-white/70 hover:text-gold-300 transition-colors"
              >
                {isAr ? l.ar : l.en}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            <div className="text-white/80">
              <LocaleToggle />
            </div>
            <Button
              asChild
              size="sm"
              className="bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300"
            >
              <Link href={`${base}/offer/lead-intelligence-sprint`}>
                {isAr ? "ابدأ" : "Start"}
              </Link>
            </Button>
          </div>
        </div>
      </header>

      {/* ------------------------------------------------------------------ */}
      {/* HERO                                                                */}
      {/* ------------------------------------------------------------------ */}
      <section
        ref={heroRef}
        className="relative flex flex-col items-center justify-center px-4 py-24 md:py-32 overflow-hidden"
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
        </div>

        {/* Launch badge — honest positioning */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="relative z-10 mb-6"
        >
          <Badge className="border-gold-500/40 bg-gold-500/10 text-gold-300 text-xs px-4 py-1.5 rounded-full backdrop-blur-sm">
            <span className="inline-block w-2 h-2 rounded-full bg-gold-400 me-2 animate-pulse" />
            {isAr ? "مرحلة الإطلاق — انضم لأوائل العملاء" : "Now launching — join the founding cohort"}
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
            className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-lg px-8 py-12 md:px-16 md:py-14 shadow-2xl"
            style={{ boxShadow: "0 8px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.07)" }}
          >
            <motion.h1
              variants={fadeUp}
              custom={1}
              className="text-3xl sm:text-4xl md:text-5xl font-bold leading-tight tracking-tight"
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
                ? "كشف تسرّب الإيراد · حوكمة الذكاء الاصطناعي · امتثال ZATCA و PDPL — في منصة واحدة محكومة بالدليل."
                : "Revenue leakage detection · AI governance · ZATCA & PDPL compliance — in one evidence-governed platform."}
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
                  {isAr ? "ابدأ تشخيصك" : "Start Your Diagnostic"}
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-white/20 text-white hover:bg-white/10 backdrop-blur-sm text-base h-13 px-8"
              >
                <Link href={`${base}/custom`}>
                  {isAr ? "عندك حالة مخصّصة؟" : "Have a custom case?"}
                </Link>
              </Button>
            </motion.div>

            <motion.p variants={fadeUp} custom={4} className="mt-5 text-xs text-white/40">
              {isAr
                ? "لا إرسال آلي · لا ادّعاء إيراد قبل الإثبات · ملتزم بـ PDPL"
                : "No automated outbound · No revenue claims before proof · PDPL compliant"}
            </motion.p>
          </motion.div>
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* SECTORS STRIP (honest — built for these sectors)                    */}
      {/* ------------------------------------------------------------------ */}
      <section className="bg-navy-600 border-y border-white/5 py-10 overflow-hidden">
        <p className="text-center text-xs font-semibold text-white/40 uppercase tracking-widest mb-6">
          {isAr ? "مصمّم لقطاعات B2B السعودية" : "Built for Saudi B2B sectors"}
        </p>
        <div className="relative">
          <motion.div
            className="flex gap-6 items-center"
            animate={{ x: isAr ? [0, "50%"] : [0, "-50%"] }}
            transition={{ duration: 26, repeat: Infinity, ease: "linear" }}
          >
            {[...SECTORS, ...SECTORS].map((s, i) => (
              <div
                key={i}
                className="flex-shrink-0 flex items-center gap-3 px-6 py-3 rounded-xl border border-white/8 bg-white/4 backdrop-blur-sm"
              >
                <span className="text-xl">{s.icon}</span>
                <span className="text-white/65 text-sm whitespace-nowrap font-medium">
                  {isAr ? s.ar : s.en}
                </span>
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
              ? "ست قدرات متكاملة تعمل معاً لنتائج قابلة للقياس — بحوكمة في كل خطوة."
              : "Six integrated capabilities working together for measurable results — governed at every step."}
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
      {/* STATS — honest product facts                                        */}
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
            {isAr ? "مبني على مبادئ واضحة" : "Built on clear principles"}
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-3 text-white/55 max-w-lg mx-auto text-sm">
            {isAr ? "حقائق عن المنتج — لا أرقام عملاء مُختلقة." : "Product facts — not invented customer numbers."}
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
                {s.kind === "num" ? (
                  <AnimatedNumber target={s.value as number} suffix={s.suffix} />
                ) : (
                  <span>{isAr ? s.textAr : s.textEn}</span>
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
            {isAr ? "كيف نعمل" : "How it works"}
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
            {isAr ? "من التشخيص إلى التنفيذ — ثلاث خطوات" : "From diagnostic to execution — three steps"}
          </motion.h2>
        </motion.div>

        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-40px" }}
          className="grid gap-6 md:grid-cols-3"
        >
          {HOW_IT_WORKS.map((step, i) => (
            <motion.div
              key={step.n}
              variants={fadeUp}
              custom={i}
              className="rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-7"
              style={{ boxShadow: "inset 0 1px 0 rgba(255,255,255,0.05)" }}
            >
              <div className="w-11 h-11 rounded-full bg-gradient-to-br from-gold-500 to-gold-400 text-navy-500 font-bold text-lg flex items-center justify-center mb-4">
                {step.n}
              </div>
              <h3 className="font-bold text-lg mb-2">{isAr ? step.ar : step.en}</h3>
              <p className="text-sm text-white/65 leading-relaxed">{isAr ? step.descAr : step.descEn}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* CUSTOM AI SYSTEMS                                                    */}
      {/* ------------------------------------------------------------------ */}
      <section
        className="py-20 px-4"
        style={{ background: "linear-gradient(180deg, #000d1a 0%, #001528 100%)" }}
      >
        <div className="max-w-6xl mx-auto">
          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-60px" }}
            className="text-center mb-12"
          >
            <motion.p variants={fadeUp} className="text-gold-400 text-sm font-semibold uppercase tracking-widest mb-3">
              {isAr ? "الحلول المخصصة" : "Custom AI"}
            </motion.p>
            <motion.h2 variants={fadeUp} custom={1} className="text-3xl md:text-4xl font-bold">
              {isAr ? "عندك حالة مخصّصة؟ نبنيها لك" : "Have a custom case? We build it"}
            </motion.h2>
            <motion.p variants={fadeUp} custom={2} className="mt-3 text-white/60 max-w-2xl mx-auto">
              {isAr
                ? "أنظمة AI agentic كاملة لقطاعك — من الصيانة والمشاريع إلى المعرفة السيادية ومراكز القيادة."
                : "Full agentic AI systems for your sector — from maintenance and projects to sovereign knowledge and command centers."}
            </motion.p>
          </motion.div>

          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
          >
            {CUSTOM_SYSTEMS.map((c, i) => (
              <motion.div
                key={c.en}
                variants={fadeUp}
                custom={i}
                className="rounded-2xl border border-white/8 bg-white/4 backdrop-blur-sm p-6 hover:border-gold-500/30 transition-colors"
              >
                <div className="text-3xl mb-3">{c.icon}</div>
                <h3 className="font-bold text-base mb-1">{isAr ? c.ar : c.en}</h3>
                <p className="text-sm text-white/60 leading-relaxed">{isAr ? c.descAr : c.descEn}</p>
              </motion.div>
            ))}
          </motion.div>

          <div className="text-center mt-10">
            <Button
              asChild
              size="lg"
              className="bg-gradient-to-r from-gold-500 to-gold-400 text-navy-500 font-bold hover:from-gold-400 hover:to-gold-300 shadow-lg shadow-gold-500/25 px-8"
            >
              <Link href={`${base}/custom`}>
                {isAr ? "صمّم نظامك المخصّص ←" : "Design your custom system →"}
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* PRICING                                                             */}
      {/* ------------------------------------------------------------------ */}
      <section id="pricing" className="py-20 px-4 max-w-6xl mx-auto scroll-mt-20">
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
            {isAr ? "ابدأ بتشخيص واحد، ثم قرّر." : "Start with one diagnostic, then decide."}
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
                <Link href={`${base}${plan.href}`}>{isAr ? plan.ctaAr : plan.ctaEn}</Link>
              </Button>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* TRUST STRIP                                                         */}
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
      {/* CTA SECTION — real email capture                                    */}
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
              ? "اترك بريدك ونرسل لك خطوة البدء — أو احجز مكالمة مباشرة."
              : "Leave your email and we'll send your first step — or book a call directly."}
          </motion.p>

          <motion.div variants={fadeUp} custom={2} className="max-w-md mx-auto">
            <EmailCapture source="landing.cta_footer" isAr={isAr} locale={locale} />
          </motion.div>

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
      <footer className="py-12 px-4 border-t border-white/6" style={{ background: "#000d1a" }}>
        <div className="max-w-6xl mx-auto">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 mb-10">
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

            <div>
              <p className="text-white/30 text-xs uppercase tracking-widest font-semibold mb-3">
                {isAr ? "المنتج" : "Product"}
              </p>
              <ul className="space-y-2 text-sm text-white/55">
                {[
                  { ar: "الخدمات", en: "Services", href: "/services" },
                  { ar: "الحلول المخصصة", en: "Custom AI", href: "/custom" },
                  { ar: "التشخيص", en: "Diagnostic", href: "/dealix-diagnostic" },
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
                  { ar: "الثقة والامتثال", en: "Trust", href: "/trust" },
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
