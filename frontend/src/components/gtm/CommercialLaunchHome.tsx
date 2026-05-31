"use client";
import Link from "next/link";
import { useLocale } from "next-intl";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckoutPanel } from "@/components/gtm/CheckoutPanel";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { usePublicLaunchStatus } from "@/lib/usePublicLaunchStatus";

/* ─── ZATCA Countdown ─────────────────────────────── */
function ZatcaCountdown({ isAr }: { isAr: boolean }) {
  const deadline = new Date("2026-06-30T23:59:59+03:00").getTime();
  const [diff, setDiff] = useState(deadline - Date.now());

  useEffect(() => {
    const id = setInterval(() => setDiff(deadline - Date.now()), 60_000);
    return () => clearInterval(id);
  }, [deadline]);

  const days = Math.max(0, Math.floor(diff / 86_400_000));
  return (
    <div className="inline-flex items-center gap-2 rounded-lg border border-amber-500/40 bg-amber-50/80 dark:bg-amber-950/30 px-4 py-2 text-sm font-medium text-amber-800 dark:text-amber-300">
      <span className="animate-pulse text-lg">⏰</span>
      {isAr
        ? `ZATCA Wave 24 — ${days} يوم متبقي · الموعد: ٣٠ يونيو ٢٠٢٦`
        : `ZATCA Wave 24 — ${days} days left · Deadline: June 30, 2026`}
    </div>
  );
}

/* ─── Trust Badges ─────────────────────────────────── */
const TRUST_BADGES = [
  { icon: "🛡️", ar: "PDPL أصيل", en: "PDPL Native" },
  { icon: "📋", ar: "ZATCA جاهز", en: "ZATCA Ready" },
  { icon: "✅", ar: "موافقة أولاً", en: "Approval-First" },
  { icon: "🇸🇦", ar: "عربي أولاً", en: "Arabic-First" },
  { icon: "🚫", ar: "لا outreach بارد", en: "No Cold Outreach" },
];

/* ─── 5-Tier Pricing Ladder ────────────────────────── */
const TIERS = [
  {
    id: "free",
    plan: null,
    icon: "🔍",
    ar: { label: "تشخيص مجاني", price: "مجاني", period: "", desc: "Risk Score وتحليل الجاهزية التشغيلية خلال 5 دقائق", cta: "احسب Risk Score" },
    en: { label: "Free Diagnostic", price: "Free", period: "", desc: "Risk Score & operational readiness check in 5 minutes", cta: "Calculate Risk Score" },
    href: "risk-score",
    highlight: false,
    badge: null,
  },
  {
    id: "sprint",
    plan: "pilot_managed",
    priceHint: "499 SAR",
    icon: "⚡",
    ar: { label: "10-Lead Audit Sprint", price: "499", period: "ر.س", desc: "مراجعة 10 leads حقيقية — مالك، أدلة، مسودة Proof، خطوة تالية. نتيجة خلال 48 ساعة.", cta: "ابدأ الآن" },
    en: { label: "10-Lead Audit Sprint", price: "499", period: "SAR", desc: "10 real leads reviewed — owner, evidence, Proof draft, next action. Results in 48 hours.", cta: "Start Now" },
    href: "dealix-diagnostic",
    highlight: false,
    badge: null,
  },
  {
    id: "proof",
    plan: null,
    icon: "📦",
    ar: { label: "Agency Proof Pack", price: "1,500", period: "ر.س", desc: "حزمة إثبات كاملة للوكالة — 4 أقسام، مستويات L0-L5، PDF ثنائي اللغة.", cta: "اطلب Proof Pack" },
    en: { label: "Agency Proof Pack", price: "1,500", period: "SAR", desc: "Full proof bundle for agencies — 4 sections, L0-L5 evidence levels, bilingual PDF.", cta: "Request Proof Pack" },
    href: "dealix-diagnostic",
    highlight: false,
    badge: null,
  },
  {
    id: "managed",
    plan: null,
    icon: "🏢",
    ar: { label: "Managed Ops Retainer", price: "2,999–4,999", period: "ر.س/شهر", desc: "تشغيل مُدار شهرياً — OKR أسبوعي، Proof Pack شهري، دعم أولوية. يبدأ بعد Proof Pack.", cta: "احجز استشارة" },
    en: { label: "Managed Ops Retainer", price: "2,999–4,999", period: "SAR/mo", desc: "Monthly managed ops — weekly OKR, monthly Proof Pack, priority support. Starts after Proof Pack.", cta: "Book Consultation" },
    href: "dealix-diagnostic",
    highlight: true,
    badge: { ar: "الأكثر طلباً", en: "Most Popular" },
  },
  {
    id: "custom",
    plan: null,
    icon: "🤖",
    ar: { label: "Custom AI Project", price: "5,000–25,000", period: "ر.س", desc: "تطوير AI مخصص لعملياتك — Scope محدد، نتائج موثّقة، Approval Center لكل خطوة.", cta: "ناقش مشروعك" },
    en: { label: "Custom AI Project", price: "5,000–25,000", period: "SAR", desc: "Custom AI for your operations — defined scope, documented outcomes, Approval Center at every step.", cta: "Discuss Project" },
    href: "dealix-diagnostic",
    highlight: false,
    badge: null,
  },
];

/* ─── Process Steps ────────────────────────────────── */
const PROCESS_STEPS = [
  { n: "١", nEn: "1", icon: "🔍", ar: { t: "تشخيص", d: "Risk Score أو Diagnostic محكوم يكشف الجاهزية" }, en: { t: "Diagnose", d: "Risk Score or governed Diagnostic reveals readiness" } },
  { n: "٢", nEn: "2", icon: "🛡️", ar: { t: "حوكمة", d: "مسودات وموافقة قبل أي إرسال خارجي" }, en: { t: "Govern", d: "Drafts + approval before any external send" } },
  { n: "٣", nEn: "3", icon: "📦", ar: { t: "تسليم", d: "Proof Pack بأقسام واضحة خلال 7 أيام" }, en: { t: "Deliver", d: "Proof Pack with clear sections in 7 days" } },
  { n: "٤", nEn: "4", icon: "📈", ar: { t: "توسّع", d: "Upsell فقط بعد إثبات القيمة" }, en: { t: "Expand", d: "Upsell only after proving value" } },
];

/* ─── Social Proof ─────────────────────────────────── */
const SOCIAL_PROOF = [
  { icon: "🚚", sector: { ar: "لوجستيات — الرياض", en: "Logistics — Riyadh" }, result: { ar: "كشف تسرّب إيراد 18% في 7 أيام", en: "18% revenue leakage detected in 7 days" } },
  { icon: "⚕️", sector: { ar: "رعاية صحية — جدة", en: "Healthcare — Jeddah" }, result: { ar: "جهوزية PDPL كاملة قبل الموعد النهائي", en: "Full PDPL readiness before deadline" } },
  { icon: "🏗️", sector: { ar: "مقاولات — الدمام", en: "Construction — Dammam" }, result: { ar: "ZATCA compliant قبل Wave 24", en: "ZATCA compliant before Wave 24" } },
];

/* ─── FAQs ─────────────────────────────────────────── */
const FAQS = [
  {
    ar: { q: "هل تستبدل Dealix الـ CRM الحالي؟", a: "لا. Dealix طبقة حوكمة وأدلة فوق CRM الحالي — تربط القرارات بالإثبات دون استبدال أي أداة." },
    en: { q: "Does Dealix replace my CRM?", a: "No. Dealix is a governance + evidence layer on top of your existing CRM — linking decisions to proof without replacing any tool." },
  },
  {
    ar: { q: "ما مدة التشخيص الأول؟", a: "7 أيام لـ Diagnostic كامل. 48 ساعة لـ 10-Lead Audit Sprint. Risk Score فوري." },
    en: { q: "How long does the first diagnostic take?", a: "7 days for a full Diagnostic. 48 hours for a 10-Lead Audit Sprint. Risk Score is instant." },
  },
  {
    ar: { q: "هل أحتاج تقنية أو مطوّر لتشغيل Dealix؟", a: "لا. الـ Diagnostic والـ Proof Pack يُسلَّمان كـ PDF ثنائي اللغة. لا setup تقني مطلوب في المرحلة الأولى." },
    en: { q: "Do I need a developer to use Dealix?", a: "No. The Diagnostic and Proof Pack are delivered as bilingual PDF. No technical setup needed in Phase 1." },
  },
  {
    ar: { q: "كيف تضمن عدم تسريب بيانات الشركة؟", a: "PDPL أصيل — لا scraping، لا مشاركة مع طرف ثالث بدون موافقة صريحة. سجل Audit Trail لكل عملية." },
    en: { q: "How do you protect my company data?", a: "PDPL native — no scraping, no third-party sharing without explicit consent. Audit trail for every operation." },
  },
  {
    ar: { q: "متى أبدأ Managed Ops Retainer؟", a: "بعد تسليم Proof Pack أول ناجح. لا upsell قبل إثبات القيمة. هذا مبدأ غير قابل للتفاوض." },
    en: { q: "When can I start a Managed Ops Retainer?", a: "After the first successful Proof Pack delivery. No upsell before proving value. This is non-negotiable." },
  },
];

/* ─── Component ────────────────────────────────────── */
export function CommercialLaunchHome() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const [payTier, setPayTier] = useState<string | null>(null);
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const { moyasarLive } = usePublicLaunchStatus();

  return (
    <PublicGtmShell>
      <div className={`mx-auto max-w-5xl px-6 py-12 space-y-20 ${isAr ? "text-right" : "text-left"}`}>

        {/* ── Hero ── */}
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[var(--dealix-navy)] to-[#0a2040] px-8 py-14 text-white shadow-xl">
          <div className="absolute inset-0 bg-dot-pattern opacity-20" />
          <div className="relative space-y-6">
            <div className="flex flex-wrap gap-2">
              <Badge className="bg-white/10 text-white border-white/20">
                {isAr ? "نظام تشغيل الإيرادات B2B · السعودية · رؤية 2030" : "B2B Revenue OS · Saudi Arabia · Vision 2030"}
              </Badge>
              <Badge className="bg-amber-500/20 text-amber-300 border-amber-500/30">v3.0.0</Badge>
            </div>
            <h1 className="text-4xl font-bold leading-tight md:text-5xl lg:text-6xl">
              {isAr
                ? <>وحّد قرار الإيراد.<br /><span className="text-[var(--dealix-gold)]">أثبت كل لمسة.</span><br />وسّع فقط بعد Proof.</>
                : <>Unify revenue decisions.<br /><span className="text-[var(--dealix-gold)]">Prove every touch.</span><br />Expand only after proof.</>}
            </h1>
            <p className="max-w-2xl text-lg text-white/80 leading-relaxed">
              {isAr
                ? "Dealix ليس CRM آخر — ذاكرة إيرادات + حوكمة + مسار تشخيص → Proof Pack. مبني لسوق يشتري بالثقة والامتثال."
                : "Dealix is not another CRM — revenue memory + governance + diagnostic → Proof Pack. Built for a market that buys on trust and compliance."}
            </p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Button asChild size="lg" className="bg-[var(--dealix-gold)] text-[var(--dealix-navy)] hover:bg-[var(--dealix-gold-hover)] font-bold shadow-lg">
                <Link href={`${base}/dealix-diagnostic`}>
                  {isAr ? "ابدأ التشخيص المحكوم ←" : "Start Governed Diagnostic →"}
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-white/30 text-white bg-white/10 hover:bg-white/20">
                <Link href={`${base}/risk-score`}>
                  {isAr ? "احسب Risk Score" : "Calculate Risk Score"}
                </Link>
              </Button>
              <Button asChild size="lg" variant="ghost" className="text-white/70 hover:text-white hover:bg-white/10">
                <Link href={`${base}/proof-pack`}>
                  {isAr ? "عيّنة Proof Pack" : "Sample Proof Pack"}
                </Link>
              </Button>
            </div>
            <div className="pt-2">
              <ZatcaCountdown isAr={isAr} />
            </div>
          </div>
        </section>

        {/* ── Trust Signals Bar ── */}
        <section>
          <p className="text-xs text-center text-muted-foreground mb-4 uppercase tracking-widest font-medium">
            {isAr ? "مبادئ غير قابلة للتفاوض" : "Non-negotiable principles"}
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            {TRUST_BADGES.map((b) => (
              <div key={b.en} className="flex items-center gap-2 rounded-full border border-border/60 bg-card/60 px-4 py-2 text-sm font-medium">
                <span>{b.icon}</span>
                <span>{isAr ? b.ar : b.en}</span>
              </div>
            ))}
          </div>
        </section>

        {/* ── Problem Section ── */}
        <section className="grid gap-8 lg:grid-cols-2 items-center">
          <div>
            <p className="text-sm font-semibold text-[var(--dealix-gold)] uppercase tracking-wide mb-3">
              {isAr ? "المشكلة" : "The Problem"}
            </p>
            <h2 className="text-3xl font-bold leading-snug">
              {isAr
                ? "فرقك تملك أدوات. القليل يملك سلسلة أدلة قابلة للتدقيق."
                : "Your team has tools. Few have an auditable evidence chain."}
            </h2>
            <ul className="mt-6 space-y-3">
              {(isAr ? [
                "إشارات السوق غير مربوطة بقرار إيراد",
                "عروض متعددة بلا حدود سطح واضحة",
                "إجراءات خارجية بلا موافقة مسجّلة",
                "أدلة مبعثرة أو مفقودة تماماً",
                "قصة الإيراد غير موحّدة للإدارة",
              ] : [
                "Market signals disconnected from revenue decisions",
                "Multiple offers without clear surface boundaries",
                "External actions without logged approval",
                "Evidence scattered or completely missing",
                "Revenue narrative not unified for leadership",
              ]).map((item) => (
                <li key={item} className="flex items-start gap-3 text-muted-foreground">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">✗</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <Card className="p-6 bg-gradient-to-br from-card to-card/50 border-[var(--dealix-gold)]/20">
            <p className="text-sm font-semibold text-[var(--dealix-gold)] uppercase tracking-wide mb-3">
              {isAr ? "الحل — SOAEN Framework" : "The Solution — SOAEN Framework"}
            </p>
            <div className="space-y-4">
              {[
                { letter: "S", ar: "Signal — إشارة السوق مربوطة بقرار", en: "Signal — market signal tied to a decision" },
                { letter: "O", ar: "Offer — عرض واحد على السطح بحد أقصى ٣", en: "Offer — one surface offer, max 3" },
                { letter: "A", ar: "Action — إجراء خارجي بموافقة مسجّلة", en: "Action — external action with logged approval" },
                { letter: "E", ar: "Evidence — دليل لكل لمسة مع العميل", en: "Evidence — proof for every customer touch" },
                { letter: "N", ar: "Narrative — قصة إيراد موحّدة للمؤسس", en: "Narrative — unified revenue story for founder" },
              ].map((s) => (
                <div key={s.letter} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-7 h-7 rounded-full bg-[var(--dealix-navy)] text-white flex items-center justify-center text-xs font-bold">{s.letter}</span>
                  <span className="text-sm">{isAr ? s.ar : s.en}</span>
                </div>
              ))}
            </div>
          </Card>
        </section>

        {/* ── Process Steps ── */}
        <section>
          <h2 className="text-2xl font-bold mb-8 text-center">
            {isAr ? "كيف يعمل Dealix" : "How Dealix Works"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PROCESS_STEPS.map((s) => (
              <div key={s.nEn} className="relative flex flex-col items-center text-center p-6 rounded-xl border border-border/60 bg-card/50">
                <div className="w-10 h-10 rounded-full bg-[var(--dealix-navy)] text-white flex items-center justify-center font-bold text-sm mb-3">
                  {isAr ? s.n : s.nEn}
                </div>
                <span className="text-2xl mb-2">{s.icon}</span>
                <p className="font-semibold">{isAr ? s.ar.t : s.en.t}</p>
                <p className="text-xs text-muted-foreground mt-1">{isAr ? s.ar.d : s.en.d}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── 5-Tier Pricing Ladder ── */}
        <section>
          <div className="flex items-center justify-between mb-2">
            <div>
              <p className="text-sm font-semibold text-[var(--dealix-gold)] uppercase tracking-wide">{isAr ? "سلم العروض" : "Offer Ladder"}</p>
              <h2 className="text-2xl font-bold mt-1">{isAr ? "خمسة مستويات — ابدأ من الجاهز" : "Five Tiers — Start Where You're Ready"}</h2>
            </div>
          </div>
          {!moyasarLive && (
            <p className="mb-4 text-sm text-amber-600 dark:text-amber-400 border border-amber-500/30 rounded-lg px-4 py-2 bg-amber-50/50 dark:bg-amber-950/20">
              {isAr ? "إطلاق ناعم — الدفع الإلكتروني لاحقاً. اطلب فاتورة أو احجز مراجعة." : "Soft launch — electronic payment coming soon. Request invoice or book a review."}
            </p>
          )}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {TIERS.map((tier) => {
              const content = isAr ? tier.ar : tier.en;
              const isHighlighted = tier.highlight;
              return (
                <Card
                  key={tier.id}
                  className={`relative p-5 flex flex-col transition-shadow hover:shadow-md ${
                    isHighlighted
                      ? "border-[var(--dealix-gold)] bg-gradient-to-b from-[var(--dealix-navy)]/5 to-card shadow-sm"
                      : "border-border/60 bg-card/50"
                  }`}
                >
                  {tier.badge && (
                    <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-[var(--dealix-gold)] text-[var(--dealix-navy)] text-xs font-bold px-3 py-0.5 whitespace-nowrap">
                      {isAr ? tier.badge.ar : tier.badge.en}
                    </span>
                  )}
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xl">{tier.icon}</span>
                    <p className="text-xs font-semibold text-muted-foreground uppercase">{content.label}</p>
                  </div>
                  <div className="mb-3">
                    <span className="text-2xl font-bold text-[var(--dealix-navy)] dark:text-white">{content.price}</span>
                    {content.period && <span className="text-sm text-muted-foreground ms-1">{content.period}</span>}
                  </div>
                  <p className="text-xs text-muted-foreground flex-1 leading-relaxed">{content.desc}</p>
                  <div className="mt-4 space-y-2">
                    {tier.plan && moyasarLive ? (
                      <>
                        <Button size="sm" className="w-full" onClick={() => setPayTier(payTier === tier.id ? null : tier.id)}>
                          {isAr ? "ادفع الآن" : "Pay Now"}
                        </Button>
                        {payTier === tier.id && (
                          <CheckoutPanel plan={tier.plan} planLabel={content.label} priceHint={tier.priceHint || ""} isAr={isAr} />
                        )}
                      </>
                    ) : (
                      <Button asChild size="sm" className={`w-full ${isHighlighted ? "bg-[var(--dealix-gold)] text-[var(--dealix-navy)] hover:bg-[var(--dealix-gold-hover)]" : ""}`}>
                        <Link href={`${base}/${tier.href}`}>{content.cta}</Link>
                      </Button>
                    )}
                  </div>
                </Card>
              );
            })}
          </div>
          <p className="mt-4 text-xs text-center text-muted-foreground">
            {isAr
              ? "* لا upsell بدون Proof Pack مسلّم · جميع الأسعار بالريال السعودي · موافقة بشرية على كل خطوة"
              : "* No upsell without delivered Proof Pack · All prices in SAR · Human approval at every step"}
          </p>
        </section>

        {/* ── Social Proof ── */}
        <section>
          <h2 className="text-xl font-semibold mb-6 text-center">
            {isAr ? "نتائج من شركات سعودية" : "Results from Saudi Companies"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-3">
            {SOCIAL_PROOF.map((p, i) => (
              <Card key={i} className="p-5 border-border/50 bg-muted/20">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">{p.icon}</span>
                  <p className="text-sm font-medium text-muted-foreground">{isAr ? p.sector.ar : p.sector.en}</p>
                </div>
                <p className="font-semibold text-foreground">{isAr ? p.result.ar : p.result.en}</p>
                <div className="mt-3 flex">
                  {[1,2,3,4,5].map((s) => <span key={s} className="text-[var(--dealix-gold)] text-sm">★</span>)}
                </div>
              </Card>
            ))}
          </div>
          <p className="mt-3 text-center text-xs text-muted-foreground">
            {isAr ? "* نتائج استرشادية — الأدلة الموثّقة تُسلَّم في Proof Pack" : "* Indicative results — documented evidence delivered in Proof Pack"}
          </p>
        </section>

        {/* ── CEO Quote / Authority ── */}
        <blockquote className="border-s-4 border-[var(--dealix-gold)] ps-6 py-4 bg-card/40 rounded-e-xl">
          <p className="text-lg font-medium italic">
            {isAr
              ? "«السوق السعودي يشتري بالثقة والامتثال — لا بالوعود. كل قرار إيراد يجب أن يكون قابلاً للتدقيق.»"
              : "«The Saudi market buys on trust and compliance — not promises. Every revenue decision must be auditable.»"}
          </p>
          <p className="mt-3 text-sm text-muted-foreground">— {isAr ? "المؤسس، Dealix" : "Founder, Dealix"}</p>
        </blockquote>

        {/* ── FAQ ── */}
        <section>
          <h2 className="text-2xl font-bold mb-6">{isAr ? "أسئلة شائعة" : "Frequently Asked Questions"}</h2>
          <div className="space-y-3">
            {FAQS.map((faq, i) => {
              const f = isAr ? faq.ar : faq.en;
              return (
                <div key={i} className="border border-border/60 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setOpenFaq(openFaq === i ? null : i)}
                    className="w-full flex items-center justify-between px-5 py-4 text-start font-medium hover:bg-muted/30 transition-colors"
                  >
                    <span>{f.q}</span>
                    <span className="text-muted-foreground text-lg">{openFaq === i ? "−" : "+"}</span>
                  </button>
                  {openFaq === i && (
                    <div className="px-5 pb-4 text-sm text-muted-foreground leading-relaxed border-t border-border/40">
                      {f.a}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* ── Final CTA ── */}
        <section className="rounded-2xl bg-gradient-to-br from-[var(--dealix-navy)] to-[#0a2040] text-white px-8 py-12 text-center shadow-xl">
          <h2 className="text-3xl font-bold">
            {isAr ? "جاهز لأول Proof Pack؟" : "Ready for your first Proof Pack?"}
          </h2>
          <p className="mt-3 text-white/70 max-w-xl mx-auto">
            {isAr
              ? "ابدأ بـ Risk Score مجاني، أو انتقل مباشرة للتشخيص المحكوم. لا التزام قبل رؤية النتائج."
              : "Start with a free Risk Score, or go directly to the governed Diagnostic. No commitment before seeing results."}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button asChild size="lg" className="bg-[var(--dealix-gold)] text-[var(--dealix-navy)] hover:bg-[var(--dealix-gold-hover)] font-bold">
              <Link href={`${base}/dealix-diagnostic`}>
                {isAr ? "ابدأ التشخيص ←" : "Start Diagnostic →"}
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 text-white bg-white/10 hover:bg-white/20">
              <Link href={`${base}/risk-score`}>
                {isAr ? "Risk Score مجاني" : "Free Risk Score"}
              </Link>
            </Button>
            <Button asChild size="lg" variant="ghost" className="text-white/70 hover:text-white hover:bg-white/10">
              <Link href={`${base}/proof-pack`}>
                {isAr ? "عيّنة Proof Pack" : "Sample Proof Pack"}
              </Link>
            </Button>
          </div>
          <p className="mt-4 text-xs text-white/40">
            {isAr
              ? "لا outreach بارد · لا scraping · PDPL أصيل · موافقة بشرية دائماً"
              : "No cold outreach · No scraping · PDPL native · Human approval always"}
          </p>
        </section>

      </div>
    </PublicGtmShell>
  );
}
