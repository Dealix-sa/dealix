"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";

/* ── Live countdown ─────────────────────────────────────── */
const DEADLINE = new Date("2026-06-30T23:59:59+03:00").getTime();

function useCountdown() {
  const [diff, setDiff] = useState(Math.max(0, DEADLINE - Date.now()));
  useEffect(() => {
    const id = setInterval(() => setDiff(Math.max(0, DEADLINE - Date.now())), 1000);
    return () => clearInterval(id);
  }, []);
  return {
    days: Math.floor(diff / 86_400_000),
    hours: Math.floor((diff % 86_400_000) / 3_600_000),
    minutes: Math.floor((diff % 3_600_000) / 60_000),
    seconds: Math.floor((diff % 60_000) / 1_000),
  };
}

/* ── Quiz data ──────────────────────────────────────────── */
const QUESTIONS_AR = [
  { id: "revenue", q: "إيراداتك السنوية تتجاوز 375,000 ريال؟", weight: 25 },
  { id: "einvoice", q: "تُصدر فواتير إلكترونية (Phase 1) حالياً؟", weight: 25 },
  { id: "erp", q: "نظام ERP أو محاسبي متوافق مع ZATCA API؟", weight: 20 },
  { id: "sandbox", q: "اختبرت الاتصال ببيئة ZATCA Sandbox؟", weight: 20 },
  { id: "qr", q: "فواتيرك تحتوي QR code معتمد ZATCA؟", weight: 10 },
];
const QUESTIONS_EN = [
  { id: "revenue", q: "Annual revenue exceeds 375,000 SAR?", weight: 25 },
  { id: "einvoice", q: "Currently issuing e-invoices (Phase 1)?", weight: 25 },
  { id: "erp", q: "ERP or accounting system with ZATCA API support?", weight: 20 },
  { id: "sandbox", q: "Tested connectivity to ZATCA Sandbox environment?", weight: 20 },
  { id: "qr", q: "Invoices include ZATCA-compliant QR codes?", weight: 10 },
];

const PENALTIES_AR = [
  { level: "تحذير", amount: "تحذير رسمي", trigger: "المخالفة الأولى", color: "amber" },
  { level: "غرامة خفيفة", amount: "حتى 5,000 ريال", trigger: "التأخير البسيط", color: "amber" },
  { level: "غرامة متوسطة", amount: "5,000 – 50,000 ريال", trigger: "الامتثال الجزئي", color: "orange" },
  { level: "غرامة كبيرة", amount: "حتى 100,000 ريال", trigger: "رفض الامتثال", color: "red" },
  { level: "إيقاف", amount: "إيقاف الترخيص", trigger: "المخالفات المتكررة", color: "red" },
];
const PENALTIES_EN = [
  { level: "Warning", amount: "Official warning", trigger: "First violation", color: "amber" },
  { level: "Light fine", amount: "Up to SAR 5,000", trigger: "Minor delay", color: "amber" },
  { level: "Medium fine", amount: "SAR 5,000 – 50,000", trigger: "Partial compliance", color: "orange" },
  { level: "Heavy fine", amount: "Up to SAR 100,000", trigger: "Refusing compliance", color: "red" },
  { level: "Suspension", amount: "License suspension", trigger: "Repeated violations", color: "red" },
];

const STEPS_AR = [
  { n: "1", title: "Phase 1 (2022)", desc: "فاتورة إلكترونية بصيغة XML — مُنجزة لمعظم الشركات", done: true },
  { n: "2", title: "Wave 24 — يونيو 2026", desc: "ربط مباشر مع ZATCA (Clearance + Reporting) — الآن", done: false },
  { n: "3", title: "بعد يونيو 2026", desc: "الامتثال إلزامي — الغرامات تبدأ فوراً", done: false },
];
const STEPS_EN = [
  { n: "1", title: "Phase 1 (2022)", desc: "E-invoice in XML format — done for most companies", done: true },
  { n: "2", title: "Wave 24 — June 2026", desc: "Direct ZATCA integration (Clearance + Reporting) — NOW", done: false },
  { n: "3", title: "After June 2026", desc: "Compliance mandatory — fines start immediately", done: false },
];

const FAQS_AR = [
  { q: "من يندرج ضمن Wave 24؟", a: "كل شركة إيراداتها تتجاوز 375,000 ريال سعودي سنوياً. إذا كنت ضمن هذا النطاق، الامتثال إلزامي قبل 30 يونيو 2026." },
  { q: "ما الفرق بين Phase 1 و Phase 2؟", a: "Phase 1: فواتير XML بدون اتصال بـ ZATCA. Phase 2 (Wave 24): كل فاتورة تُرسل مباشرة لـ ZATCA للمسح والموافقة قبل الإصدار." },
  { q: "ماذا يعني Clearance vs Reporting؟", a: "Clearance: ZATCA توافق على الفاتورة قبل إرسالها للعميل (B2B). Reporting: ترسل الفاتورة خلال 24 ساعة (B2C). معظم B2B يحتاج Clearance." },
  { q: "كيف يساعد Sprint 499 ريال في ZATCA؟", a: "يشمل Sprint check شامل: هل نظامك جاهز؟ ما الفجوات؟ ما الخطوات المطلوبة؟ مع توصية واضحة لأهل التقنية في شركتك." },
];
const FAQS_EN = [
  { q: "Who falls under Wave 24?", a: "Every company with annual revenue exceeding 375,000 SAR. If you're in this range, compliance is mandatory before June 30, 2026." },
  { q: "What's the difference between Phase 1 and Phase 2?", a: "Phase 1: XML invoices without ZATCA connection. Phase 2 (Wave 24): every invoice sent directly to ZATCA for clearance before issuing." },
  { q: "What does Clearance vs Reporting mean?", a: "Clearance: ZATCA approves the invoice before sending to client (B2B). Reporting: invoice sent within 24 hours (B2C). Most B2B needs Clearance." },
  { q: "How does the 499 SAR Sprint help with ZATCA?", a: "Includes a comprehensive check: is your system ready? What are the gaps? What steps are needed? With clear recommendations for your tech team." },
];

export default function ZatcaReadinessPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";
  const { days, hours, minutes, seconds } = useCountdown();
  const questions = isAr ? QUESTIONS_AR : QUESTIONS_EN;
  const penalties = isAr ? PENALTIES_AR : PENALTIES_EN;
  const steps = isAr ? STEPS_AR : STEPS_EN;
  const faqs = isAr ? FAQS_AR : FAQS_EN;

  const [answers, setAnswers] = useState<Record<string, boolean | null>>({});
  const [quizDone, setQuizDone] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const toggle = (id: string, val: boolean) =>
    setAnswers((p) => ({ ...p, [id]: val }));
  const answered = Object.keys(answers).length === questions.length;

  const score = questions.reduce((acc, q) =>
    answers[q.id] === true ? acc + q.weight : acc, 0);

  const tier =
    score >= 80 ? "ready"
    : score >= 50 ? "partial"
    : "critical";

  const tierConfig = {
    ready: {
      labelAr: "جاهز ✓", labelEn: "Ready ✓",
      color: "emerald", bgClass: "bg-emerald-50/30 dark:bg-emerald-950/10 border-emerald-500/20",
      textClass: "text-emerald-700 dark:text-emerald-300",
      msgAr: "شركتك في وضع جيد. راجع الـ sandbox testing وتأكد من API integration.",
      msgEn: "Your company is in good shape. Review sandbox testing and confirm API integration.",
    },
    partial: {
      labelAr: "يحتاج تجهيز ⚠", labelEn: "Needs Preparation ⚠",
      color: "amber", bgClass: "bg-amber-50/30 dark:bg-amber-950/10 border-amber-500/20",
      textClass: "text-amber-700 dark:text-amber-300",
      msgAr: "لديك بعض الجهوزية لكن فيه فجوات. Sprint 499 ريال يكشفها ويقدم خطة عمل واضحة.",
      msgEn: "You have some readiness but there are gaps. Sprint 499 SAR identifies them and provides a clear action plan.",
    },
    critical: {
      labelAr: "يحتاج تدخّل عاجل ✗", labelEn: "Urgent Action Needed ✗",
      color: "red", bgClass: "bg-red-50/30 dark:bg-red-950/10 border-red-500/20",
      textClass: "text-red-700 dark:text-red-400",
      msgAr: "مع بقاء 31 يوماً فقط، هذا وضع حرج. ابدأ Sprint 499 ريال اليوم لتجنب غرامات ZATCA.",
      msgEn: "With only 31 days left, this is a critical situation. Start Sprint 499 SAR today to avoid ZATCA fines.",
    },
  };
  const tc = tierConfig[tier];

  return (
    <div className="min-h-screen bg-background" dir={dir}>

      {/* Nav */}
      <header className="sticky top-0 z-20 border-b border-border/60 bg-background/95 backdrop-blur">
        <div className="mx-auto max-w-4xl px-6 py-3 flex items-center justify-between">
          <Link href={`/${locale}`} className="font-bold text-lg" style={{ color: "#001F3F" }}>Dealix</Link>
          <div className="flex items-center gap-3">
            <Link href={`/${locale}/risk-score`} className="text-sm text-muted-foreground hover:text-foreground hidden sm:block">
              {isAr ? "Risk Score" : "Risk Score"}
            </Link>
            <Link
              href={`/${locale}/offer/lead-intelligence-sprint`}
              className="rounded-lg px-4 py-2 text-sm font-semibold"
              style={{ backgroundColor: "#D4AF37", color: "#001F3F" }}
            >
              {isAr ? "Sprint — 499 ريال" : "Sprint — SAR 499"}
            </Link>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-10 space-y-14">

        {/* Hero + Countdown */}
        <section className="text-center space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-red-500/30 bg-red-50/50 dark:bg-red-950/20 px-4 py-1.5 text-sm font-medium text-red-700 dark:text-red-400">
            <span className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
            {isAr ? "الموعد النهائي الإلزامي" : "Mandatory deadline"}
          </div>
          <h1 className="text-4xl font-black md:text-5xl" style={{ color: "#001F3F" }}>
            {isAr ? "ZATCA Wave 24" : "ZATCA Wave 24"}
          </h1>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto">
            {isAr
              ? "كل شركة إيراداتها تتجاوز 375,000 ريال ملزمة بالفوترة الإلكترونية Phase 2. الموعد النهائي:"
              : "Every company with 375K+ SAR revenue must comply with Phase 2 e-invoicing. Deadline:"}
          </p>

          {/* Countdown */}
          <div className="flex justify-center gap-4 my-2">
            {[
              { val: days, labelAr: "يوم", labelEn: "days" },
              { val: hours, labelAr: "ساعة", labelEn: "hrs" },
              { val: minutes, labelAr: "دقيقة", labelEn: "min" },
              { val: seconds, labelAr: "ثانية", labelEn: "sec" },
            ].map(({ val, labelAr, labelEn }) => (
              <div key={labelEn} className="flex flex-col items-center">
                <div
                  className="flex h-16 w-16 items-center justify-center rounded-xl text-2xl font-black text-white md:h-20 md:w-20 md:text-3xl"
                  style={{ backgroundColor: "#001F3F" }}
                >
                  {String(val).padStart(2, "0")}
                </div>
                <span className="mt-1 text-xs text-muted-foreground">{isAr ? labelAr : labelEn}</span>
              </div>
            ))}
          </div>

          <div className="flex flex-wrap justify-center gap-3">
            <Link
              href={`/${locale}/offer/lead-intelligence-sprint`}
              className="rounded-xl px-8 py-3.5 text-base font-bold shadow-lg transition-all hover:-translate-y-0.5"
              style={{ backgroundColor: "#001F3F", color: "white" }}
            >
              {isAr ? "ابدأ Sprint 499 ريال ←" : "Start Sprint SAR 499 →"}
            </Link>
            <button
              onClick={() => document.getElementById("quiz")?.scrollIntoView({ behavior: "smooth" })}
              className="rounded-xl border border-border bg-card px-8 py-3.5 text-base font-medium hover:bg-muted/30 transition-colors"
            >
              {isAr ? "قيّم جاهزيتي الآن" : "Assess my readiness"}
            </button>
          </div>
        </section>

        {/* Timeline */}
        <section>
          <h2 className="text-xl font-bold mb-6 text-center">{isAr ? "المراحل الزمنية" : "Implementation Timeline"}</h2>
          <div className="flex flex-col sm:flex-row gap-4">
            {steps.map((s, i) => (
              <div
                key={i}
                className={`flex-1 rounded-xl border p-4 ${
                  s.done
                    ? "border-emerald-500/30 bg-emerald-50/20 dark:bg-emerald-950/10"
                    : i === 1
                    ? "border-red-500/40 bg-red-50/20 dark:bg-red-950/10"
                    : "border-border/60 bg-card/50"
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                    s.done ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
                    : i === 1 ? "bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300"
                    : "bg-muted text-muted-foreground"
                  }`}>
                    {s.n === "2" ? (isAr ? "أنت هنا" : "YOU ARE HERE") : s.n === "1" ? (isAr ? "مكتملة" : "Done") : (isAr ? "قادم" : "Upcoming")}
                  </span>
                </div>
                <p className="font-semibold text-sm">{s.title}</p>
                <p className="text-xs text-muted-foreground mt-1">{s.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Penalties */}
        <section>
          <h2 className="text-xl font-bold mb-2">{isAr ? "غرامات عدم الامتثال" : "Non-Compliance Penalties"}</h2>
          <p className="text-sm text-muted-foreground mb-6">
            {isAr
              ? "هيئة الزكاة والضريبة والجمارك تُطبّق غرامات تصاعدية بحسب حجم المخالفة"
              : "ZATCA applies escalating fines based on violation severity"}
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm min-w-[400px]">
              <thead>
                <tr className="border-b border-border">
                  <th className="pb-3 text-start font-semibold text-muted-foreground">{isAr ? "المستوى" : "Level"}</th>
                  <th className="pb-3 text-start font-semibold text-muted-foreground">{isAr ? "المبلغ" : "Amount"}</th>
                  <th className="pb-3 text-start font-semibold text-muted-foreground">{isAr ? "السبب" : "Trigger"}</th>
                </tr>
              </thead>
              <tbody>
                {penalties.map((p, i) => (
                  <tr key={i} className="border-b border-border/30">
                    <td className="py-2.5">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                        p.color === "red" ? "bg-red-100 text-red-700 dark:bg-red-950/50 dark:text-red-300"
                        : p.color === "orange" ? "bg-orange-100 text-orange-700 dark:bg-orange-950/50 dark:text-orange-300"
                        : "bg-amber-100 text-amber-700 dark:bg-amber-950/50 dark:text-amber-300"
                      }`}>
                        {p.level}
                      </span>
                    </td>
                    <td className="py-2.5 font-semibold text-xs">{p.amount}</td>
                    <td className="py-2.5 text-xs text-muted-foreground">{p.trigger}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            {isAr ? "* الأرقام تقديرية بناءً على لوائح ZATCA المعلنة. استشر محاسبك القانوني للتأكيد." : "* Figures estimated based on published ZATCA regulations. Consult your certified accountant for confirmation."}
          </p>
        </section>

        {/* What's required */}
        <section className="rounded-2xl border border-border/60 bg-card/30 p-6">
          <h2 className="text-xl font-bold mb-4">{isAr ? "ما المطلوب للامتثال؟" : "What's required for compliance?"}</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {(isAr ? [
              { icon: "🔗", title: "API Integration", desc: "ربط نظامك المحاسبي مباشرة بـ ZATCA Integration Layer" },
              { icon: "📋", title: "Clearance Model", desc: "الحصول على موافقة ZATCA قبل إرسال كل فاتورة B2B" },
              { icon: "🧾", title: "UBL 2.1 XML Format", desc: "تنسيق الفواتير وفق معيار UBL 2.1 المعتمد من ZATCA" },
              { icon: "🔐", title: "Digital Signature", desc: "توقيع كل فاتورة بشهادة رقمية معتمدة من ZATCA" },
            ] : [
              { icon: "🔗", title: "API Integration", desc: "Connect your accounting system directly to ZATCA Integration Layer" },
              { icon: "📋", title: "Clearance Model", desc: "Get ZATCA approval before sending every B2B invoice" },
              { icon: "🧾", title: "UBL 2.1 XML Format", desc: "Format invoices per ZATCA-approved UBL 2.1 standard" },
              { icon: "🔐", title: "Digital Signature", desc: "Sign every invoice with a ZATCA-approved digital certificate" },
            ]).map((item) => (
              <div key={item.title} className="flex gap-3 rounded-lg border border-border/40 bg-card/50 p-3">
                <span className="text-xl">{item.icon}</span>
                <div>
                  <p className="font-semibold text-sm">{item.title}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Quiz */}
        <section id="quiz">
          <h2 className="text-xl font-bold mb-2">{isAr ? "تحقق من جاهزيتك الآن — مجاناً" : "Check Your Readiness Now — Free"}</h2>
          <p className="text-sm text-muted-foreground mb-6">
            {isAr ? "5 أسئلة — نتيجة فورية — لا حاجة لإدخال بريد إلكتروني" : "5 questions — instant result — no email required"}
          </p>

          {!quizDone ? (
            <div className="space-y-4">
              {questions.map((q, i) => (
                <div key={q.id} className="rounded-xl border border-border/60 bg-card/50 p-4">
                  <p className="font-medium text-sm mb-3">
                    <span className="text-muted-foreground text-xs me-2">{i + 1}/{questions.length}</span>
                    {q.q}
                  </p>
                  <div className="flex gap-2">
                    {[true, false].map((val) => (
                      <button
                        key={String(val)}
                        onClick={() => toggle(q.id, val)}
                        className={`flex-1 py-2 rounded-lg border text-sm font-medium transition-all ${
                          answers[q.id] === val
                            ? val
                              ? "border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
                              : "border-red-400 bg-red-50/30 dark:bg-red-950/20 text-red-700 dark:text-red-400"
                            : "border-border bg-card hover:border-border/80"
                        }`}
                      >
                        {val ? (isAr ? "نعم ✓" : "Yes ✓") : (isAr ? "لا ✗" : "No ✗")}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
              <button
                disabled={!answered}
                onClick={() => setQuizDone(true)}
                className="w-full rounded-xl py-3.5 text-sm font-bold text-white transition-opacity disabled:opacity-40"
                style={{ backgroundColor: "#001F3F" }}
              >
                {isAr ? "احسب درجة جاهزيتي ←" : "Calculate my readiness score →"}
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div className={`rounded-2xl border p-8 text-center ${tc.bgClass}`}>
                <p className="text-6xl font-black mb-2">{score}<span className="text-2xl text-muted-foreground">/100</span></p>
                <span className={`inline-block rounded-full px-4 py-1 text-sm font-bold ${tc.textClass} ${tc.bgClass} border`}>
                  {isAr ? tc.labelAr : tc.labelEn}
                </span>
                <p className="mt-4 text-sm text-muted-foreground max-w-md mx-auto">
                  {isAr ? tc.msgAr : tc.msgEn}
                </p>
              </div>

              {/* Checklist */}
              <div className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-3">
                <p className="font-semibold text-sm">{isAr ? "تفاصيل الجاهزية" : "Readiness details"}</p>
                {questions.map((q) => (
                  <div key={q.id} className="flex items-start gap-3">
                    <span className={`text-base flex-shrink-0 ${answers[q.id] ? "text-emerald-500" : "text-red-400"}`}>
                      {answers[q.id] ? "✓" : "✗"}
                    </span>
                    <span className="text-sm">{q.q}</span>
                    <span className="ms-auto text-xs font-medium text-muted-foreground flex-shrink-0">+{answers[q.id] ? q.weight : 0}</span>
                  </div>
                ))}
              </div>

              <div className="flex flex-wrap gap-3">
                <Link
                  href={`/${locale}/offer/lead-intelligence-sprint`}
                  className="flex-1 text-center rounded-xl py-3 text-sm font-bold text-white"
                  style={{ backgroundColor: "#001F3F" }}
                >
                  {isAr ? "ابدأ Sprint 499 ريال ←" : "Start Sprint SAR 499 →"}
                </Link>
                <button
                  onClick={() => { setAnswers({}); setQuizDone(false); }}
                  className="rounded-xl border border-border bg-card px-4 py-3 text-sm font-medium hover:bg-muted/30 transition-colors"
                >
                  {isAr ? "أعد التقييم" : "Retake"}
                </button>
              </div>
            </div>
          )}
        </section>

        {/* FAQs */}
        <section>
          <h2 className="text-xl font-bold mb-6">{isAr ? "أسئلة شائعة عن ZATCA" : "ZATCA Frequently Asked Questions"}</h2>
          <div className="space-y-2">
            {faqs.map((f, i) => (
              <div key={i} className="rounded-xl border border-border/60 bg-card/50 overflow-hidden">
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full flex items-center justify-between px-5 py-4 text-sm font-medium hover:bg-muted/20 transition-colors"
                >
                  <span className={isAr ? "text-right" : "text-left"}>{f.q}</span>
                  <span className="flex-shrink-0 ms-3 text-muted-foreground text-lg">{openFaq === i ? "−" : "+"}</span>
                </button>
                {openFaq === i && (
                  <div className={`px-5 pb-4 text-sm text-muted-foreground leading-relaxed ${isAr ? "text-right" : ""}`}>{f.a}</div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Bottom CTA */}
        <section className="rounded-2xl text-white p-8 text-center" style={{ background: "linear-gradient(135deg, #001F3F 0%, #0a2040 100%)" }}>
          <p className="text-sm font-medium mb-1" style={{ color: "#D4AF37" }}>
            {isAr ? "ZATCA Wave 24 — الموعد النهائي" : "ZATCA Wave 24 — Final Deadline"}
          </p>
          <h2 className="text-2xl font-bold mb-2">
            {isAr
              ? `${days} يوم · ${hours} ساعة · ${minutes} دقيقة`
              : `${days} days · ${hours} hrs · ${minutes} min`}
          </h2>
          <p className="text-white/70 text-sm mb-6">
            {isAr
              ? "Sprint 7 أيام يشمل ZATCA check كامل مع Proof Pack — 499 ريال فقط"
              : "7-day Sprint includes full ZATCA check with Proof Pack — SAR 499 only"}
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Link
              href={`/${locale}/offer/lead-intelligence-sprint`}
              className="rounded-xl px-8 py-3 text-sm font-bold transition-all hover:-translate-y-0.5"
              style={{ backgroundColor: "#D4AF37", color: "#001F3F" }}
            >
              {isAr ? "ابدأ الآن ←" : "Start Now →"}
            </Link>
            <Link
              href={`/${locale}/learn/zatca-wave-24-guide`}
              className="rounded-xl border border-white/20 bg-white/10 px-8 py-3 text-sm font-medium text-white hover:bg-white/20 transition-colors"
            >
              {isAr ? "اقرأ الدليل الكامل" : "Read full guide"}
            </Link>
          </div>
        </section>

      </main>
    </div>
  );
}
