"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

/**
 * Custom AI Service intake — commercial ladder Rung 4 (5,000–25,000 SAR + 1,000/mo).
 * Captures a bespoke AI project request and posts it to the governed public
 * endpoint POST /api/v1/public/custom-ai-request, which stores it as a lead
 * for founder review. No external action happens without founder approval.
 */

type Option = { value: string; ar: string; en: string };

const SECTORS: Option[] = [
  { value: "real_estate", ar: "عقارات", en: "Real Estate" },
  { value: "b2b_services", ar: "خدمات B2B", en: "B2B Services" },
  { value: "agency", ar: "وكالة تسويق", en: "Marketing Agency" },
  { value: "consulting", ar: "استشارات", en: "Consulting" },
  { value: "retail", ar: "تجزئة / تجارة", en: "Retail / Commerce" },
  { value: "finance", ar: "تمويل / بنوك", en: "Finance / Banking" },
  { value: "healthcare", ar: "رعاية صحية", en: "Healthcare" },
  { value: "other", ar: "أخرى", en: "Other" },
];

const USE_CASES: { id: string; icon: string; ar: { t: string; d: string }; en: { t: string; d: string } }[] = [
  {
    id: "lead_intelligence",
    icon: "🎯",
    ar: { t: "ذكاء العملاء المحتملين", d: "تأهيل وترتيب وإثراء العملاء حسب ICP مع حوكمة PDPL" },
    en: { t: "Lead Intelligence", d: "ICP scoring, enrichment & qualification with PDPL governance" },
  },
  {
    id: "revenue_ops",
    icon: "📈",
    ar: { t: "أتمتة عمليات الإيراد", d: "Workflows حتمية للمتابعة والتسعير والقرارات بموافقة بشرية" },
    en: { t: "Revenue Ops Automation", d: "Deterministic follow-up, pricing & decision workflows with human approval" },
  },
  {
    id: "agent_copilot",
    icon: "🤖",
    ar: { t: "Copilot / وكيل مخصّص", d: "مساعد AI لفريقك يجيب من مصادرك فقط — لا إجابات بلا مصدر" },
    en: { t: "Custom Copilot / Agent", d: "An AI assistant grounded only in your sources — no source-less answers" },
  },
  {
    id: "doc_intelligence",
    icon: "📄",
    ar: { t: "ذكاء المستندات", d: "استخراج وتحليل العقود والفواتير والتقارير مع audit trail" },
    en: { t: "Document Intelligence", d: "Extract & analyze contracts, invoices & reports with an audit trail" },
  },
  {
    id: "compliance_engine",
    icon: "🛡️",
    ar: { t: "محرك امتثال", d: "فحوصات PDPL / ZATCA مدمجة في عملياتك مع أدلة لكل قرار" },
    en: { t: "Compliance Engine", d: "PDPL / ZATCA checks embedded in your ops with evidence per decision" },
  },
  {
    id: "other",
    icon: "✨",
    ar: { t: "شيء آخر", d: "صف فكرتك — نحوّلها إلى Scope موقَّع قبل أي تنفيذ" },
    en: { t: "Something else", d: "Describe your idea — we turn it into a signed Scope before any build" },
  },
];

const DATA_READINESS: Option[] = [
  { value: "structured", ar: "بيانات منظّمة جاهزة (CRM / CSV / قاعدة بيانات)", en: "Structured data ready (CRM / CSV / database)" },
  { value: "partial", ar: "بيانات جزئية / متفرّقة", en: "Partial / scattered data" },
  { value: "none_yet", ar: "لا توجد بيانات منظّمة بعد", en: "No structured data yet" },
  { value: "unsure", ar: "غير متأكد", en: "Not sure" },
];

const BUDGET_BANDS: Option[] = [
  { value: "5k_10k", ar: "5,000 – 10,000 ر.س", en: "5,000 – 10,000 SAR" },
  { value: "10k_25k", ar: "10,000 – 25,000 ر.س", en: "10,000 – 25,000 SAR" },
  { value: "25k_plus", ar: "أكثر من 25,000 ر.س (Enterprise)", en: "25,000+ SAR (Enterprise)" },
  { value: "exploring", ar: "ما زلت أستكشف", en: "Still exploring" },
];

const TIMELINES: Option[] = [
  { value: "asap", ar: "في أقرب وقت", en: "As soon as possible" },
  { value: "1_3_months", ar: "خلال 1 – 3 أشهر", en: "Within 1 – 3 months" },
  { value: "3_6_months", ar: "خلال 3 – 6 أشهر", en: "Within 3 – 6 months" },
  { value: "exploring", ar: "أستكشف فقط", en: "Just exploring" },
];

export function CustomAiRequestForm() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [form, setForm] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    sector: "",
    use_case: "lead_intelligence",
    data_readiness: "",
    budget_band: "",
    timeline: "",
    description: "",
    consent: false,
    website: "", // honeypot
  });
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [leadId, setLeadId] = useState("");

  function set<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة للمتابعة." : "Consent is required to proceed.");
      return;
    }
    setBusy(true);
    setStatus("");
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${base}/api/v1/public/custom-ai-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, source: "frontend.custom_ai_form" }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "failed");
      setLeadId(data.lead_id || "");
      setSubmitted(true);
      setStatus(
        isAr
          ? "تم استلام طلبك — سنتواصل خلال 4 ساعات عمل لتحديد الـ Scope."
          : "Request received — we will contact you within 4 business hours to define the Scope."
      );
    } catch {
      setStatus(
        isAr
          ? "تعذّر الإرسال — تحقق من الاتصال وحاول مجدداً، أو راسلنا مباشرة."
          : "Submission failed — check your connection and retry, or contact us directly."
      );
    } finally {
      setBusy(false);
    }
  }

  const useCases = USE_CASES;

  return (
    <div className={`space-y-14 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>
      {/* Hero */}
      <header className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8">
        <Badge className="mb-4 bg-amber-500/20 text-amber-300 border-amber-500/30">
          {isAr ? "مشروع AI مخصّص — الرتبة الرابعة" : "Custom AI Project — Rung 4"}
        </Badge>
        <h1 className="text-4xl font-bold leading-tight md:text-5xl">
          {isAr
            ? "قل لنا ماذا تريد أن نبني — نحوّله إلى نظام AI موثّق"
            : "Tell us what you want built — we turn it into a governed AI system"}
        </h1>
        <p className="mt-4 text-white/70 max-w-2xl leading-relaxed">
          {isAr
            ? "تطوير AI مخصّص لعملياتك، بـ Scope محدّد ومُوقَّع، وموافقة بشرية على كل خطوة، وProof Pack ختامي يثبت القيمة. مبني على نفس الحوكمة: لا scraping، لا إرسال آلي، أدلة لكل قرار."
            : "Bespoke AI development for your operations — a defined, signed Scope, human approval at every step, and a final Proof Pack that documents the value. Built on the same governance: no scraping, no automated sending, evidence for every decision."}
        </p>
        <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { v: isAr ? "5K–25K ر.س" : "5K–25K SAR", l: isAr ? "نطاق المشروع" : "Project range" },
            { v: isAr ? "4–12 أسبوع" : "4–12 weeks", l: isAr ? "مدة التنفيذ" : "Delivery time" },
            { v: isAr ? "موافقة" : "Approval", l: isAr ? "قبل كل خطوة" : "Before every step" },
            { v: "Proof Pack", l: isAr ? "تسليم موثّق" : "Documented delivery" },
          ].map((m) => (
            <div key={m.l} className="rounded-xl bg-white/5 border border-white/10 p-3 text-center">
              <p className="text-lg font-bold text-amber-300">{m.v}</p>
              <p className="text-xs text-white/50 mt-0.5">{m.l}</p>
            </div>
          ))}
        </div>
      </header>

      {/* What we build */}
      <section>
        <h2 className="text-2xl font-bold mb-2">{isAr ? "ماذا نبني لك؟" : "What we build for you"}</h2>
        <p className="text-muted-foreground mb-6">
          {isAr
            ? "اختر الأقرب لاحتياجك — وإن لم تجده، اختر «شيء آخر» وصف فكرتك."
            : "Pick the closest to your need — or choose “Something else” and describe your idea."}
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {useCases.map((u) => {
            const c = isAr ? u.ar : u.en;
            const active = form.use_case === u.id;
            return (
              <Card
                key={u.id}
                className={`p-5 cursor-pointer transition-all border-2 ${
                  active
                    ? "border-[#001F3F] dark:border-amber-500 shadow-md bg-primary/5"
                    : "border-border/40 bg-card/50 hover:border-border"
                }`}
                onClick={() => set("use_case", u.id)}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">{u.icon}</span>
                  <p className="font-semibold text-sm">{c.t}</p>
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">{c.d}</p>
              </Card>
            );
          })}
        </div>
      </section>

      {/* How it works */}
      <section>
        <h2 className="text-2xl font-bold mb-6">{isAr ? "كيف يعمل المشروع المخصّص" : "How a custom project works"}</h2>
        <div className="grid gap-4 sm:grid-cols-4">
          {(isAr
            ? [
                { n: "١", t: "Scope موقَّع", d: "نحوّل فكرتك إلى وثيقة نطاق محدّدة ومُوقَّعة — لا مفاجآت" },
                { n: "٢", t: "بناء بموافقة", d: "تطوير مع Approval Center لكل خطوة وaudit trail كامل" },
                { n: "٣", t: "Proof Pack", d: "تسليم موثّق بالأدلة يثبت ما تم إنجازه" },
                { n: "٤", t: "Hand-off وتدريب", d: "تسليم النظام مع تدريب فريقك وتوثيق PDPL كامل" },
              ]
            : [
                { n: "1", t: "Signed Scope", d: "We turn your idea into a defined, signed scope document — no surprises" },
                { n: "2", t: "Approved Build", d: "Development with an Approval Center at every step and a full audit trail" },
                { n: "3", t: "Proof Pack", d: "Evidence-backed delivery that documents exactly what was built" },
                { n: "4", t: "Hand-off & Training", d: "System hand-off with team training and full PDPL documentation" },
              ]
          ).map((s) => (
            <div key={s.n} className="flex flex-col items-center text-center p-5 rounded-xl border border-border/60 bg-card/50">
              <div className="w-10 h-10 rounded-full bg-[#001F3F] text-white flex items-center justify-center font-bold text-sm mb-3">
                {s.n}
              </div>
              <p className="font-semibold text-sm">{s.t}</p>
              <p className="text-xs text-muted-foreground mt-1">{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Intake form */}
      <section>
        <h2 className="text-2xl font-bold mb-2">{isAr ? "اطلب مشروعك المخصّص" : "Request your custom project"}</h2>
        <p className="text-muted-foreground mb-6 text-sm">
          {isAr
            ? "مراجعة يدوية من المؤسس — لا أتمتة. كل طلب يُدرس بجدية ونرد خلال 4 ساعات عمل."
            : "Manual review by the founder — no automation. Every request is taken seriously; we reply within 4 business hours."}
        </p>

        {submitted ? (
          <Card className="p-8 text-center border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20">
            <div className="text-4xl mb-3">✅</div>
            <h3 className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
              {isAr ? "تم استلام طلبك!" : "Request received!"}
            </h3>
            <p className="text-muted-foreground mt-2">{status}</p>
            {leadId ? <p className="text-xs text-muted-foreground mt-1">{isAr ? "رقم الطلب:" : "Request ID:"} {leadId}</p> : null}
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Button asChild variant="outline">
                <Link href={`/${locale}/proof-pack`}>{isAr ? "شاهد عيّنة Proof Pack" : "View Proof Pack Sample"}</Link>
              </Button>
              <Button asChild variant="outline">
                <Link href={`/${locale}/services`}>{isAr ? "كل الخدمات" : "All Services"}</Link>
              </Button>
            </div>
          </Card>
        ) : (
          <form onSubmit={submit} className="max-w-2xl space-y-5">
            {/* Honeypot — visually hidden */}
            <input
              type="text"
              name="website"
              tabIndex={-1}
              autoComplete="off"
              value={form.website}
              onChange={(e) => set("website", e.target.value)}
              className="absolute left-[-9999px] h-0 w-0 opacity-0"
              aria-hidden="true"
            />

            <div className="grid gap-5 sm:grid-cols-2">
              {([
                ["name", isAr ? "الاسم الكامل *" : "Full Name *", "text", true],
                ["company", isAr ? "اسم الشركة *" : "Company Name *", "text", true],
                ["email", isAr ? "البريد الإلكتروني *" : "Email Address *", "email", true],
                ["phone", isAr ? "رقم الجوال *" : "Phone Number *", "tel", true],
              ] as const).map(([k, label, type, required]) => (
                <div key={k}>
                  <Label htmlFor={k} className="text-sm font-medium">{label}</Label>
                  <Input
                    id={k}
                    type={type}
                    required={required}
                    value={form[k]}
                    onChange={(e) => set(k, e.target.value)}
                    className="mt-1"
                  />
                </div>
              ))}
            </div>

            <div className="grid gap-5 sm:grid-cols-2">
              <SelectField
                id="sector"
                label={isAr ? "القطاع" : "Sector"}
                isAr={isAr}
                value={form.sector}
                onChange={(v) => set("sector", v)}
                options={SECTORS}
                placeholder={isAr ? "اختر القطاع" : "Select sector"}
              />
              <SelectField
                id="data_readiness"
                label={isAr ? "جاهزية البيانات" : "Data Readiness"}
                isAr={isAr}
                value={form.data_readiness}
                onChange={(v) => set("data_readiness", v)}
                options={DATA_READINESS}
                placeholder={isAr ? "اختر الحالة" : "Select status"}
              />
              <SelectField
                id="budget_band"
                label={isAr ? "نطاق الميزانية" : "Budget Range"}
                isAr={isAr}
                value={form.budget_band}
                onChange={(v) => set("budget_band", v)}
                options={BUDGET_BANDS}
                placeholder={isAr ? "اختر النطاق" : "Select range"}
              />
              <SelectField
                id="timeline"
                label={isAr ? "الإطار الزمني" : "Timeline"}
                isAr={isAr}
                value={form.timeline}
                onChange={(v) => set("timeline", v)}
                options={TIMELINES}
                placeholder={isAr ? "اختر الإطار" : "Select timeline"}
              />
            </div>

            <div>
              <Label htmlFor="description" className="text-sm font-medium">
                {isAr ? "صف ما تريد بناءه *" : "Describe what you want built *"}
              </Label>
              <textarea
                id="description"
                rows={5}
                required
                value={form.description}
                onChange={(e) => set("description", e.target.value)}
                className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder={
                  isAr
                    ? "مثال: نريد نظاماً يقرأ عقود الإيجار، يستخرج بنود التجديد، ويبني قائمة متابعة بموافقة قبل أي تواصل..."
                    : "e.g. We want a system that reads lease contracts, extracts renewal terms, and builds an approval-gated follow-up list..."
                }
              />
            </div>

            <label className="flex items-start gap-2 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={form.consent}
                onChange={(e) => set("consent", e.target.checked)}
                className="mt-0.5 accent-primary"
              />
              <span>
                {isAr
                  ? "أوافق على مراجعة الطلب يدوياً والتواصل للمتابعة وفق نظام حماية البيانات (PDPL). لا outreach بارد آلي."
                  : "I consent to manual review and PDPL-compliant follow-up contact. No automated cold outreach."}
              </span>
            </label>

            <Button type="submit" disabled={busy} size="lg" className="w-full">
              {busy ? (isAr ? "جاري الإرسال..." : "Submitting...") : isAr ? "أرسل طلب المشروع المخصّص" : "Submit Custom Project Request"}
            </Button>

            {status && !submitted ? <p className="text-sm text-destructive">{status}</p> : null}

            <p className="text-xs text-muted-foreground">
              {isAr
                ? "تُخزَّن بياناتك بأمان لمراجعة المؤسس فقط. لا مشاركة، لا إرسال آلي، يمكنك طلب الحذف في أي وقت."
                : "Your data is stored securely for founder review only. No sharing, no automated sending; you may request deletion anytime."}
            </p>
          </form>
        )}
      </section>

      {/* Non-negotiables */}
      <section className="rounded-xl border border-border/60 bg-muted/20 p-6">
        <h2 className="font-semibold mb-4">{isAr ? "مبادئ غير قابلة للتفاوض" : "Non-negotiable principles"}</h2>
        <ul className="space-y-2">
          {(isAr
            ? [
                "Scope محدّد ومُوقَّع قبل أي تطوير — لا عمل بلا اتفاق واضح",
                "كل إجراء خارجي يمر بموافقة بشرية — لا أتمتة بلا مراجعة",
                "لا scraping ولا شراء قوائم — مصادر بيانات مشروعة فقط",
                "لا وعود بنتائج مضمونة — نلتزم بالمخرجات الموثّقة",
                "Proof Pack وتوثيق PDPL كامل مع كل تسليم",
              ]
            : [
                "Defined, signed Scope before any development — no work without a clear agreement",
                "Every external action passes human approval — no automation without review",
                "No scraping or list-buying — lawful data sources only",
                "No guaranteed-outcome promises — we commit to documented deliverables",
                "Proof Pack and full PDPL documentation with every hand-off",
              ]
          ).map((item) => (
            <li key={item} className="flex items-start gap-2 text-sm">
              <span className="text-[#001F3F] dark:text-amber-400 mt-0.5 flex-shrink-0">✓</span>
              {item}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

function SelectField({
  id,
  label,
  isAr,
  value,
  onChange,
  options,
  placeholder,
}: {
  id: string;
  label: string;
  isAr: boolean;
  value: string;
  onChange: (v: string) => void;
  options: Option[];
  placeholder: string;
}) {
  return (
    <div>
      <Label htmlFor={id} className="text-sm font-medium">{label}</Label>
      <select
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        <option value="">{placeholder}</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {isAr ? o.ar : o.en}
          </option>
        ))}
      </select>
    </div>
  );
}
