"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Mirrors os/03_OFFERS.yml — the real custom / high-ticket catalog.
const SYSTEMS = [
  { id: "workflow_audit", icon: "🔎", ar: "تدقيق Workflow بالـ AI", en: "AI Workflow Audit", priceAr: "من 5,000 ر.س · 7 أيام", priceEn: "From 5,000 SAR · 7 days" },
  { id: "maintenance_os", icon: "🔧", ar: "نظام ذكاء الصيانة", en: "Maintenance Intelligence OS", priceAr: "من 40,000 ر.س", priceEn: "From 40,000 SAR" },
  { id: "project_controls_os", icon: "📐", ar: "نظام التحكم بالمشاريع", en: "Project Controls AI OS", priceAr: "من 50,000 ر.س", priceEn: "From 50,000 SAR" },
  { id: "sovereign_rag", icon: "📚", ar: "المعرفة السيادية (RAG)", en: "Sovereign Knowledge / RAG", priceAr: "من 50,000 ر.س", priceEn: "From 50,000 SAR" },
  { id: "executive_command", icon: "🧭", ar: "مركز القيادة التنفيذي", en: "Executive Command Center", priceAr: "من 100,000 ر.س", priceEn: "From 100,000 SAR" },
  { id: "revenue_ai_os", icon: "🚀", ar: "نظام AI للإيرادات", en: "Revenue AI OS", priceAr: "من 40,000 ر.س", priceEn: "From 40,000 SAR" },
  { id: "governance_pack", icon: "⚖️", ar: "حزمة حوكمة الذكاء الاصطناعي", en: "AI Governance Pack", priceAr: "من 15,000 ر.س", priceEn: "From 15,000 SAR" },
  { id: "other", icon: "✨", ar: "حالة أخرى / غير متأكد", en: "Other / not sure", priceAr: "نحدّدها معاً", priceEn: "We'll scope it together" },
];

const BUDGETS = [
  { id: "lt_50k", ar: "أقل من 50 ألف", en: "Under 50k" },
  { id: "50_150k", ar: "50–150 ألف", en: "50k–150k" },
  { id: "150_500k", ar: "150–500 ألف", en: "150k–500k" },
  { id: "gt_500k", ar: "أكثر من 500 ألف", en: "500k+" },
  { id: "unsure", ar: "غير محدد", en: "Not sure yet" },
];

const TIMELINES = [
  { id: "urgent", ar: "عاجل (هذا الشهر)", en: "Urgent (this month)" },
  { id: "1_3m", ar: "1–3 أشهر", en: "1–3 months" },
  { id: "3_6m", ar: "3–6 أشهر", en: "3–6 months" },
  { id: "exploring", ar: "استكشاف مبدئي", en: "Just exploring" },
];

export function CustomSolutionForm() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [selected, setSelected] = useState<string[]>([]);
  const [form, setForm] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    sector: "",
    budget: "",
    timeline: "",
    challenge: "",
    consent: false,
    website: "", // honeypot
  });
  const [busy, setBusy] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [status, setStatus] = useState("");
  const [calendly, setCalendly] = useState("");

  function set<K extends keyof typeof form>(k: K, v: (typeof form)[K]) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  function toggleSystem(id: string) {
    setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  }

  function composeMessage(): string {
    const labels = selected
      .map((id) => SYSTEMS.find((s) => s.id === id))
      .filter(Boolean)
      .map((s) => (isAr ? s!.ar : s!.en));
    const budget = BUDGETS.find((b) => b.id === form.budget);
    const timeline = TIMELINES.find((t) => t.id === form.timeline);
    const lines = [
      "[Custom AI request]",
      `Systems: ${labels.length ? labels.join(", ") : "—"}`,
      `Budget: ${budget ? (isAr ? budget.ar : budget.en) : "—"}`,
      `Timeline: ${timeline ? (isAr ? timeline.ar : timeline.en) : "—"}`,
      `Challenge: ${form.challenge || "—"}`,
    ];
    return lines.join("\n");
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة للمتابعة." : "Consent is required to continue.");
      return;
    }
    if (selected.length === 0) {
      setStatus(isAr ? "اختر نظاماً واحداً على الأقل (أو «غير متأكد»)." : "Select at least one system (or 'not sure').");
      return;
    }
    setBusy(true);
    setStatus("");
    try {
      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          company: form.company,
          email: form.email,
          phone: form.phone,
          sector: form.sector,
          message: composeMessage(),
          consent: form.consent,
          website: form.website,
          source: "custom_page",
          systems: selected,
          budget: form.budget,
          timeline: form.timeline,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || data.ok === false) throw new Error(data.detail || "failed");
      setCalendly(data.calendly_url || "");
      setSubmitted(true);
    } catch (err) {
      const detail = err instanceof Error ? err.message : "failed";
      setStatus(
        detail === "missing_required_fields"
          ? isAr
            ? "يرجى تعبئة الاسم والشركة والبريد والجوال."
            : "Please fill name, company, email and phone."
          : isAr
            ? "تعذّر الإرسال — تحقق من الاتصال وحاول مجدداً."
            : "Couldn't submit — check your connection and try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  if (submitted) {
    return (
      <Card className="p-8 text-center border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20 max-w-lg mx-auto">
        <div className="text-4xl mb-3">✅</div>
        <h3 className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
          {isAr ? "وصلنا طلبك المخصّص!" : "Your custom request is in!"}
        </h3>
        <p className="text-muted-foreground mt-2 text-sm">
          {isAr
            ? "سنراجع حالتك ونعود لك بنطاق مبدئي وخطوة تالية. للرد الأسرع احجز مكالمة استكشاف."
            : "We'll review your case and reply with an initial scope and next step. For the fastest response, book a scoping call."}
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          {calendly && (
            <Button asChild variant="gold">
              <a href={calendly} target="_blank" rel="noopener noreferrer">
                {isAr ? "احجز مكالمة استكشاف" : "Book a scoping call"}
              </a>
            </Button>
          )}
          <Button asChild variant="outline">
            <Link href={`/${locale}/services`}>
              {isAr ? "تصفّح الخدمات" : "Browse services"}
            </Link>
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <form onSubmit={submit} className="space-y-10" dir={isAr ? "rtl" : "ltr"}>
      {/* honeypot */}
      <input
        type="text"
        tabIndex={-1}
        autoComplete="off"
        aria-hidden
        value={form.website}
        onChange={(e) => set("website", e.target.value)}
        className="hidden"
      />

      {/* System selection */}
      <section>
        <h2 className="text-xl font-bold mb-1">
          {isAr ? "1) أي نظام يهمّك؟" : "1) Which system interests you?"}
        </h2>
        <p className="text-sm text-muted-foreground mb-4">
          {isAr ? "اختر واحداً أو أكثر — تقدر تختار «غير متأكد»." : "Pick one or more — 'not sure' is fine."}
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {SYSTEMS.map((s) => {
            const active = selected.includes(s.id);
            return (
              <button
                type="button"
                key={s.id}
                onClick={() => toggleSystem(s.id)}
                className={`text-start rounded-xl border-2 p-4 transition-all ${
                  active
                    ? "border-[#001F3F] dark:border-amber-500 bg-primary/5 shadow-md"
                    : "border-border/40 bg-card/50 hover:border-border"
                }`}
              >
                <div className="text-2xl mb-2">{s.icon}</div>
                <p className="font-semibold text-sm leading-snug">{isAr ? s.ar : s.en}</p>
                <p className="text-xs text-muted-foreground mt-1">{isAr ? s.priceAr : s.priceEn}</p>
                {active && <span className="mt-2 inline-block text-emerald-500 text-xs">✓ {isAr ? "مختار" : "Selected"}</span>}
              </button>
            );
          })}
        </div>
      </section>

      {/* Budget + timeline */}
      <section className="grid sm:grid-cols-2 gap-6">
        <div>
          <h3 className="font-semibold mb-3">{isAr ? "2) الميزانية التقريبية (ر.س)" : "2) Approx. budget (SAR)"}</h3>
          <div className="flex flex-wrap gap-2">
            {BUDGETS.map((b) => (
              <button
                type="button"
                key={b.id}
                onClick={() => set("budget", b.id)}
                className={`rounded-lg border px-3 py-2 text-sm transition-colors ${
                  form.budget === b.id ? "border-primary bg-primary/10" : "border-border/50 hover:bg-muted/20"
                }`}
              >
                {isAr ? b.ar : b.en}
              </button>
            ))}
          </div>
        </div>
        <div>
          <h3 className="font-semibold mb-3">{isAr ? "3) الإطار الزمني" : "3) Timeline"}</h3>
          <div className="flex flex-wrap gap-2">
            {TIMELINES.map((t) => (
              <button
                type="button"
                key={t.id}
                onClick={() => set("timeline", t.id)}
                className={`rounded-lg border px-3 py-2 text-sm transition-colors ${
                  form.timeline === t.id ? "border-primary bg-primary/10" : "border-border/50 hover:bg-muted/20"
                }`}
              >
                {isAr ? t.ar : t.en}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Challenge */}
      <section>
        <h3 className="font-semibold mb-2">
          {isAr ? "4) اشرح التحدّي أو الـ workflow" : "4) Describe the challenge or workflow"}
        </h3>
        <textarea
          rows={4}
          value={form.challenge}
          onChange={(e) => set("challenge", e.target.value)}
          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          placeholder={
            isAr
              ? "مثال: عندنا 200 بلاغ صيانة شهرياً تُدار يدوياً بدون SLA واضح…"
              : "e.g. We handle 200 maintenance tickets/month manually with no clear SLA…"
          }
        />
      </section>

      {/* Contact details */}
      <section>
        <h3 className="font-semibold mb-3">{isAr ? "5) بيانات التواصل" : "5) Your details"}</h3>
        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="c-name" className="text-sm font-medium">{isAr ? "الاسم *" : "Name *"}</Label>
            <Input id="c-name" required value={form.name} onChange={(e) => set("name", e.target.value)} className="mt-1" />
          </div>
          <div>
            <Label htmlFor="c-company" className="text-sm font-medium">{isAr ? "الشركة *" : "Company *"}</Label>
            <Input id="c-company" required value={form.company} onChange={(e) => set("company", e.target.value)} className="mt-1" />
          </div>
          <div>
            <Label htmlFor="c-email" className="text-sm font-medium">{isAr ? "البريد *" : "Email *"}</Label>
            <Input id="c-email" type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} className="mt-1" />
          </div>
          <div>
            <Label htmlFor="c-phone" className="text-sm font-medium">{isAr ? "الجوال *" : "Phone *"}</Label>
            <Input id="c-phone" type="tel" required placeholder="+9665…" value={form.phone} onChange={(e) => set("phone", e.target.value)} className="mt-1" />
          </div>
          <div className="sm:col-span-2">
            <Label htmlFor="c-sector" className="text-sm font-medium">{isAr ? "القطاع" : "Sector"}</Label>
            <Input id="c-sector" value={form.sector} onChange={(e) => set("sector", e.target.value)} className="mt-1" placeholder={isAr ? "مثال: مقاولات، عقار، مرافق…" : "e.g. contracting, real estate, facilities…"} />
          </div>
        </div>
      </section>

      <label className="flex items-start gap-2 text-sm cursor-pointer">
        <input type="checkbox" checked={form.consent} onChange={(e) => set("consent", e.target.checked)} className="mt-0.5 accent-primary" />
        <span className="text-muted-foreground">
          {isAr
            ? "أوافق على التواصل معي لتحديد نطاق الحل. بياناتي تُعالَج وفق PDPL — لا إرسال آلي ولا مشاركة مع طرف ثالث دون إذن."
            : "I consent to be contacted to scope the solution. My data is processed under PDPL — no automated outreach, no third-party sharing without permission."}
        </span>
      </label>

      <div className="flex flex-col items-center gap-3">
        <Button type="submit" disabled={busy} size="lg" variant="gold" className="w-full sm:w-auto px-10">
          {busy ? (isAr ? "جارٍ الإرسال…" : "Submitting…") : isAr ? "أرسل طلب الحل المخصّص" : "Send custom request"}
        </Button>
        {status && <p className="text-sm text-destructive text-center">{status}</p>}
        <p className="text-xs text-muted-foreground text-center max-w-md">
          {isAr
            ? "مراجعة يدوية من الفريق. نعود لك بنطاق مبدئي وتقدير — لا التزام قبل اتفاق واضح."
            : "Manually reviewed by the team. We reply with an initial scope and estimate — no commitment before a clear agreement."}
        </p>
        <div className="flex flex-wrap justify-center gap-2 pt-1">
          {(isAr
            ? ["لا scraping", "موافقة قبل كل خطوة", "بيانات سيادية", "سجل تدقيق كامل"]
            : ["No scraping", "Approval before every step", "Sovereign data", "Full audit log"]
          ).map((b) => (
            <Badge key={b} variant="secondary" className="text-xs">{b}</Badge>
          ))}
        </div>
      </div>
    </form>
  );
}
