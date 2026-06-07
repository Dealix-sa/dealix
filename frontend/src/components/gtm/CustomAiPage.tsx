"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const CONTACT_EMAIL = "hello@dealix.me";

/* Process — mirrors the Custom AI tier on /services (honest, audit-first). */
const PROCESS = [
  {
    ar: { t: "نطاق موقّع", d: "نتفق على Scope محدّد ومُوقَّع قبل أي بناء — لا مفاجآت، لا التزام مفتوح." },
    en: { t: "Signed scope", d: "We agree on a defined, signed scope before any build — no surprises, no open-ended commitment." },
  },
  {
    ar: { t: "بناء محكوم", d: "تطوير مخصص مع audit trail كامل وموافقة بشرية على كل خطوة حرجة." },
    en: { t: "Governed build", d: "Custom development with a full audit trail and human approval at every critical step." },
  },
  {
    ar: { t: "Proof Pack ختامي", d: "تسليم موثّق بمستويات أدلة L0–L5 + توثيق PDPL كامل." },
    en: { t: "Final Proof Pack", d: "Documented hand-off with L0–L5 evidence levels + full PDPL documentation." },
  },
  {
    ar: { t: "تسليم وتدريب", d: "Hand-off مع تدريب فريقك حتى تصبح القدرة داخلية ومستدامة." },
    en: { t: "Hand-off & training", d: "Hand-off with team training so the capability becomes internal and sustainable." },
  },
];

/* Example build types — framed as capabilities we can build, NOT client claims. */
const EXAMPLES = [
  { icon: "🎯", ar: "تأهيل العملاء المحتملين آلياً (محكوم)", en: "Governed lead-qualification automation" },
  { icon: "💬", ar: "مساعد مبيعات بالعربية على بياناتك", en: "Arabic sales assistant on your data" },
  { icon: "🔎", ar: "تحليل CRM وكشف تسرّب الإيراد", en: "CRM analysis & revenue-leakage detection" },
  { icon: "🛟", ar: "وكيل دعم محكوم بموافقة", en: "Approval-gated support agent" },
  { icon: "📑", ar: "تقارير تنفيذية ثنائية اللغة تلقائية", en: "Automated bilingual executive reports" },
  { icon: "🧾", ar: "تكامل ZATCA وأنظمتك الداخلية", en: "ZATCA & internal-systems integration" },
];

export function CustomAiPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  const [form, setForm] = useState({
    company: "",
    sector: "",
    build: "",
    tools: "",
    timeline: "",
    budget: "",
    email: "",
  });
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<"ok" | "fallback" | null>(null);

  function update(field: keyof typeof form, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    setResult(null);
    const payload = {
      name: form.company || "Custom AI inquiry",
      company: form.company,
      email: form.email,
      sector: form.sector,
      source: "custom-ai-intake",
      message:
        `Custom AI scoping request\n` +
        `What to build: ${form.build}\n` +
        `Current tools: ${form.tools}\n` +
        `Timeline: ${form.timeline}\n` +
        `Budget: ${form.budget}`,
    };
    try {
      const res = await fetch(`${API_BASE}/api/v1/public/demo-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setResult(res.ok ? "ok" : "fallback");
    } catch {
      setResult("fallback");
    } finally {
      setBusy(false);
    }
  }

  const field = "w-full rounded-lg border border-border/60 bg-background px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#C9974B]/40";

  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-4xl px-6 py-12 space-y-16 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >
        {/* Hero */}
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] px-8 py-14 text-white shadow-xl">
          <div className="relative space-y-5">
            <Badge className="bg-white/10 text-white border-white/20 text-xs">
              {isAr ? "AI مخصص — المستوى الخامس" : "Custom AI — Tier 5"}
            </Badge>
            <h1 className="text-4xl font-bold leading-tight md:text-5xl">
              {isAr ? (
                <>قل لنا ماذا تريد أن<br /><span className="text-[#C9974B]">نبنيه لك</span></>
              ) : (
                <>Tell us what you want<br /><span className="text-[#C9974B]">us to build</span></>
              )}
            </h1>
            <p className="max-w-2xl text-lg text-white/80 leading-relaxed">
              {isAr
                ? "تطوير ذكاء اصطناعي مخصص لعملياتك — بنطاق موقّع، وموافقة بشرية على كل خطوة، وProof Pack ختامي. من 5,000 إلى 25,000 ر.س حسب النطاق."
                : "Bespoke AI built for your operations — signed scope, human approval at every step, and a final Proof Pack. From 5,000 to 25,000 SAR by scope."}
            </p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Button asChild size="lg" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold shadow-lg">
                <a href="#scope">{isAr ? "ابدأ تحديد النطاق ↓" : "Start scoping ↓"}</a>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-white/30 text-white bg-white/10 hover:bg-white/20">
                <Link href={`${base}/services`}>{isAr ? "كل المستويات الخمسة" : "All five tiers"}</Link>
              </Button>
            </div>
          </div>
        </section>

        {/* How custom works */}
        <section>
          <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-1">
            {isAr ? "كيف يعمل المخصص" : "How custom works"}
          </p>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "نطاق موقّع · بناء محكوم · دليل ختامي" : "Signed scope · Governed build · Final evidence"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PROCESS.map((p, i) => {
              const c = isAr ? p.ar : p.en;
              return (
                <div key={i} className="rounded-xl border border-border/60 bg-card/50 p-5">
                  <div className="w-8 h-8 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold text-sm mb-3">
                    {i + 1}
                  </div>
                  <p className="font-semibold text-sm">{c.t}</p>
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{c.d}</p>
                </div>
              );
            })}
          </div>
        </section>

        {/* Examples */}
        <section>
          <h2 className="text-2xl font-bold mb-2">
            {isAr ? "أمثلة على ما يمكننا بناؤه" : "Examples of what we can build"}
          </h2>
          <p className="text-sm text-muted-foreground mb-6">
            {isAr
              ? "أمثلة على القدرات — وليست ادعاءات نتائج. نطاقك يُحدَّد معك."
              : "Capability examples — not result claims. Your scope is defined with you."}
          </p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {EXAMPLES.map((ex, i) => (
              <div key={i} className="flex items-start gap-3 rounded-xl border border-border/60 bg-card/50 p-4">
                <span className="text-2xl">{ex.icon}</span>
                <span className="text-sm font-medium">{isAr ? ex.ar : ex.en}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Scoping form */}
        <section id="scope" className="rounded-2xl border border-[#C9974B]/30 bg-gradient-to-b from-[#C9974B]/5 to-card p-8 scroll-mt-24">
          <h2 className="text-2xl font-bold mb-2">
            {isAr ? "موجز المشروع المخصص" : "Custom project brief"}
          </h2>
          <p className="text-sm text-muted-foreground mb-6">
            {isAr
              ? "املأ الموجز وسنعود إليك خلال 48 ساعة بخطوة تالية واضحة (مكالمة نطاق أو أسئلة). لا التزام."
              : "Fill in the brief and we'll come back within 48 hours with a clear next step (scoping call or questions). No commitment."}
          </p>

          {result === "ok" ? (
            <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-6 text-center">
              <p className="font-semibold text-emerald-600 dark:text-emerald-400">
                {isAr ? "تم استلام موجزك ✓" : "Your brief was received ✓"}
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                {isAr ? "سنرد خلال 48 ساعة عمل." : "We'll reply within 48 business hours."}
              </p>
            </div>
          ) : (
            <form onSubmit={submit} className="grid gap-4 sm:grid-cols-2">
              <input className={field} placeholder={isAr ? "اسم الشركة" : "Company name"} value={form.company} onChange={(e) => update("company", e.target.value)} required />
              <input className={field} placeholder={isAr ? "القطاع" : "Sector"} value={form.sector} onChange={(e) => update("sector", e.target.value)} />
              <textarea className={`${field} sm:col-span-2 min-h-[96px]`} placeholder={isAr ? "ماذا تريد أن نبني؟ صف المشكلة أو الفكرة." : "What do you want us to build? Describe the problem or idea."} value={form.build} onChange={(e) => update("build", e.target.value)} required />
              <input className={field} placeholder={isAr ? "الأنظمة الحالية (CRM، إلخ)" : "Current tools (CRM, etc.)"} value={form.tools} onChange={(e) => update("tools", e.target.value)} />
              <input className={field} placeholder={isAr ? "الإطار الزمني المرغوب" : "Desired timeline"} value={form.timeline} onChange={(e) => update("timeline", e.target.value)} />
              <input className={field} placeholder={isAr ? "نطاق الميزانية (ر.س)" : "Budget range (SAR)"} value={form.budget} onChange={(e) => update("budget", e.target.value)} />
              <input type="email" className={field} placeholder={isAr ? "بريدك الإلكتروني" : "Your email"} value={form.email} onChange={(e) => update("email", e.target.value)} required />
              <div className="sm:col-span-2 flex flex-col gap-3">
                <Button type="submit" size="lg" disabled={busy} className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold w-full sm:w-auto">
                  {busy ? (isAr ? "جارٍ الإرسال…" : "Sending…") : isAr ? "أرسل الموجز" : "Send brief"}
                </Button>
                {result === "fallback" && (
                  <p className="text-sm text-amber-600 dark:text-amber-400">
                    {isAr
                      ? <>تعذّر الإرسال التلقائي. راسلنا مباشرة على <a className="underline font-medium" href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a> ونسعد بخدمتك.</>
                      : <>Automatic submit failed. Email us directly at <a className="underline font-medium" href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a> and we'll take it from there.</>}
                  </p>
                )}
              </div>
            </form>
          )}
          <p className="mt-6 text-xs text-muted-foreground">
            {isAr
              ? "القيمة التقديرية ليست قيمة مُتحقَّقة · لا أتمتة بلا موافقة · بياناتك محمية وفق PDPL"
              : "Estimated value is not Verified value · No automation without approval · Your data is protected under PDPL"}
          </p>
        </section>
      </div>
    </PublicGtmShell>
  );
}
