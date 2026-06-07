"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

const PROJECT_TYPES = [
  { id: "ai_agent", icon: "🤖", ar: "وكيل ذكاء اصطناعي", en: "AI agent" },
  { id: "automation", icon: "⚙️", ar: "أتمتة عملية", en: "Process automation" },
  { id: "integration", icon: "🔌", ar: "ربط مع أنظمتك", en: "System integration" },
  { id: "data", icon: "📊", ar: "بيانات وتقارير", en: "Data & reporting" },
  { id: "other", icon: "✨", ar: "شيء آخر", en: "Something else" },
];

const WHAT_WE_BUILD_AR = [
  { icon: "🤖", title: "وكلاء يردّون ويؤهّلون", desc: "وكيل عربي يردّ على leads الواتساب/الإيميل ويؤهّلها — بموافقة قبل أي إرسال." },
  { icon: "⚙️", title: "أتمتة تشغيل محكومة", desc: "أتمتة المتابعات والتقارير وخطوات التشغيل المتكررة دون فقدان السيطرة." },
  { icon: "🔌", title: "تكامل مع أدواتك", desc: "ربط مع CRM، Google، أنظمتك الداخلية — تدفّق بيانات نظيف وموثّق." },
  { icon: "🛡️", title: "حوكمة وامتثال", desc: "PDPL أصيل، سجل تدقيق، وموافقة بشرية على كل إجراء حسّاس." },
];

const WHAT_WE_BUILD_EN = [
  { icon: "🤖", title: "Agents that reply & qualify", desc: "An Arabic agent that replies to WhatsApp/email leads and qualifies them — approval before any send." },
  { icon: "⚙️", title: "Governed ops automation", desc: "Automate follow-ups, reports, and repetitive ops steps without losing control." },
  { icon: "🔌", title: "Integration with your tools", desc: "Connect CRM, Google, your internal systems — clean, documented data flow." },
  { icon: "🛡️", title: "Governance & compliance", desc: "PDPL-native, audit trail, and human approval on every sensitive action." },
];

export function CustomAIIntake() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const projectTypes = PROJECT_TYPES;
  const whatWeBuild = isAr ? WHAT_WE_BUILD_AR : WHAT_WE_BUILD_EN;

  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    phone: "",
    sector: "",
    project_type: "ai_agent",
    scope: "",
    budget_range: "",
    timeline: "",
    consent: false,
    website: "", // honeypot
  });
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.scope.trim()) {
      setStatus(isAr ? "اكتب لنا نطاق المشروع." : "Please describe the project scope.");
      return;
    }
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة." : "Consent is required.");
      return;
    }
    setBusy(true);
    setStatus("");
    try {
      const res = await api.postPublicCustomBrief(form);
      const data = res.data as { lead_id?: string; message_ar?: string; message_en?: string };
      setSubmitted(true);
      setStatus(
        (isAr ? data.message_ar : data.message_en) ||
          (isAr
            ? "وصلنا طلبك — سنعود إليك خلال يوم عمل."
            : "We received your brief — we'll get back within one business day."),
      );
    } catch {
      setStatus(
        isAr
          ? "تعذّر الإرسال — تحقّق من الاتصال وحاول مجدداً."
          : "Submit failed — check your connection and try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`space-y-14 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>
      {/* Hero */}
      <header className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8">
        <Badge className="mb-4 bg-amber-500/20 text-amber-300 border-amber-500/30">
          {isAr ? "بناء مخصّص — Dealix" : "Custom Build — Dealix"}
        </Badge>
        <h1 className="text-4xl font-bold leading-tight">
          {isAr
            ? "عندك شيء محدّد تبي نبنيه؟ قل لنا، ونرجع لك بخطة."
            : "Have a specific build in mind? Tell us, and we'll return a plan."}
        </h1>
        <p className="mt-4 text-white/70 max-w-xl leading-relaxed">
          {isAr
            ? "لكل حالة لا تناسبها الباقات الجاهزة — صف لنا ما تريد بناءه ونرجع لك بنطاق وتقدير مبدئي خلال يوم عمل. بلا أرقام مخترَعة، وبلا التزام قبل موافقتك."
            : "For anything the ready-made packages don't fit — describe what you want built and we return a scope and initial estimate within one business day. No invented numbers, no commitment before your approval."}
        </p>
        <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { ar: "يوم عمل", en: "1 business day", labelAr: "خطة وتقدير", labelEn: "Plan & estimate" },
            { ar: "PDPL", en: "PDPL", labelAr: "امتثال أصيل", labelEn: "Native compliance" },
            { ar: "موافقة", en: "Approval", labelAr: "قبل كل إرسال", labelEn: "Before every send" },
            { ar: "بلا scraping", en: "No scraping", labelAr: "بيانات مشروعة", labelEn: "Lawful data only" },
          ].map((m) => (
            <div key={m.en} className="rounded-xl bg-white/5 border border-white/10 p-3 text-center">
              <p className="text-lg font-bold text-amber-300">{isAr ? m.ar : m.en}</p>
              <p className="text-xs text-white/50 mt-0.5">{isAr ? m.labelAr : m.labelEn}</p>
            </div>
          ))}
        </div>
      </header>

      {/* What we can build */}
      <section>
        <h2 className="text-2xl font-bold mb-6">
          {isAr ? "أمثلة على ما نبنيه" : "Examples of what we build"}
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {whatWeBuild.map((w) => (
            <div key={w.title} className="flex items-start gap-4 rounded-xl border border-border/60 bg-card/50 p-5">
              <span className="text-3xl flex-shrink-0">{w.icon}</span>
              <div>
                <p className="font-semibold">{w.title}</p>
                <p className="text-sm text-muted-foreground mt-1">{w.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Intake form */}
      <section>
        <h2 className="text-2xl font-bold mb-2">
          {isAr ? "قل لنا وش تبي نسوي" : "Tell us what you want us to build"}
        </h2>
        <p className="text-muted-foreground mb-6 text-sm">
          {isAr
            ? "مراجعة يدوية من الفريق — لا أتمتة. كل طلب يُدرس بجدية ونرجع لك بنطاق وتقدير."
            : "Manual review by the team — no automation. Every brief is taken seriously; we return a scope and estimate."}
        </p>

        {submitted ? (
          <Card className="p-8 text-center border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20">
            <div className="text-4xl mb-3">✅</div>
            <h3 className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
              {isAr ? "وصلنا طلبك!" : "We got your brief!"}
            </h3>
            <p className="text-muted-foreground mt-2">{status}</p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Button asChild variant="outline">
                <Link href={`/${locale}/proof-pack`}>
                  {isAr ? "شاهد عيّنة Proof Pack" : "View Proof Pack Sample"}
                </Link>
              </Button>
              <Button asChild variant="outline">
                <Link href={`/${locale}/services`}>
                  {isAr ? "تصفّح الباقات الجاهزة" : "Browse ready packages"}
                </Link>
              </Button>
            </div>
          </Card>
        ) : (
          <form onSubmit={submit} className="max-w-lg space-y-5">
            {/* honeypot — visually hidden */}
            <input
              type="text"
              tabIndex={-1}
              autoComplete="off"
              value={form.website}
              onChange={(e) => setForm((f) => ({ ...f, website: e.target.value }))}
              className="hidden"
              aria-hidden="true"
            />

            {([
              ["name", isAr ? "الاسم الكامل *" : "Full Name *", "text", true],
              ["email", isAr ? "البريد الإلكتروني *" : "Email Address *", "email", true],
              ["company", isAr ? "اسم الشركة" : "Company Name", "text", false],
              ["phone", isAr ? "رقم الجوال (اختياري)" : "Phone (optional)", "tel", false],
              ["sector", isAr ? "القطاع" : "Sector", "text", false],
            ] as const).map(([k, label, type, required]) => (
              <div key={k}>
                <Label htmlFor={k} className="text-sm font-medium">{label}</Label>
                <Input
                  id={k}
                  type={type}
                  required={required}
                  value={form[k as keyof typeof form] as string}
                  onChange={(e) => setForm((f) => ({ ...f, [k]: e.target.value }))}
                  className="mt-1"
                />
              </div>
            ))}

            <div>
              <Label className="text-sm font-medium">{isAr ? "نوع المشروع *" : "Project Type *"}</Label>
              <div className="mt-2 grid grid-cols-2 sm:grid-cols-3 gap-2">
                {projectTypes.map((type) => (
                  <label
                    key={type.id}
                    className={`flex items-center gap-2 rounded-lg border p-2.5 cursor-pointer text-sm transition-colors ${
                      form.project_type === type.id
                        ? "border-[#001F3F] dark:border-amber-500 bg-primary/5"
                        : "border-border/50 hover:bg-muted/20"
                    }`}
                  >
                    <input
                      type="radio"
                      name="project_type"
                      value={type.id}
                      checked={form.project_type === type.id}
                      onChange={() => setForm((f) => ({ ...f, project_type: type.id }))}
                      className="accent-primary"
                    />
                    <span>{type.icon}</span>
                    <span>{isAr ? type.ar : type.en}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <Label htmlFor="scope" className="text-sm font-medium">
                {isAr ? "وش تبي نبني بالضبط؟ *" : "What exactly do you want built? *"}
              </Label>
              <textarea
                id="scope"
                rows={5}
                required
                value={form.scope}
                onChange={(e) => setForm((f) => ({ ...f, scope: e.target.value }))}
                className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder={
                  isAr
                    ? "مثال: نبي وكيل يردّ على رسائل العملاء على واتساب بالعربية، يؤهّلهم، ويحجز اجتماع — مع ربطه بـ CRM عندنا."
                    : "e.g. We want an agent that replies to customer WhatsApp messages in Arabic, qualifies them, and books a meeting — connected to our CRM."
                }
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="budget_range" className="text-sm font-medium">
                  {isAr ? "الميزانية التقريبية (اختياري)" : "Approx. budget (optional)"}
                </Label>
                <Input
                  id="budget_range"
                  type="text"
                  value={form.budget_range}
                  onChange={(e) => setForm((f) => ({ ...f, budget_range: e.target.value }))}
                  className="mt-1"
                  placeholder={isAr ? "مثال: ١٠٬٠٠٠ ر.س" : "e.g. 10,000 SAR"}
                />
              </div>
              <div>
                <Label htmlFor="timeline" className="text-sm font-medium">
                  {isAr ? "المدة المطلوبة (اختياري)" : "Desired timeline (optional)"}
                </Label>
                <Input
                  id="timeline"
                  type="text"
                  value={form.timeline}
                  onChange={(e) => setForm((f) => ({ ...f, timeline: e.target.value }))}
                  className="mt-1"
                  placeholder={isAr ? "مثال: خلال شهر" : "e.g. within a month"}
                />
              </div>
            </div>

            <label className="flex items-start gap-2 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={form.consent}
                onChange={(e) => setForm((f) => ({ ...f, consent: e.target.checked }))}
                className="mt-0.5 accent-primary"
              />
              <span>
                {isAr
                  ? "أوافق على مراجعة الطلب يدوياً والتواصل معي للمتابعة. لا outreach بارد آلي."
                  : "I consent to manual review and follow-up contact. No automated cold outreach."}
              </span>
            </label>

            <Button type="submit" disabled={busy} size="lg" className="w-full">
              {busy
                ? isAr
                  ? "جاري الإرسال..."
                  : "Submitting..."
                : isAr
                  ? "أرسل الطلب المخصّص"
                  : "Send custom brief"}
            </Button>

            {status && !submitted && <p className="text-sm text-destructive">{status}</p>}

            <p className="text-xs text-muted-foreground">
              {isAr
                ? "نراجع طلبك يدوياً ونعود إليك خلال يوم عمل بخطة وتقدير مبدئي. بياناتك تُعالَج وفق PDPL."
                : "We review manually and return within one business day with a plan and initial estimate. Your data is processed under PDPL."}
            </p>
          </form>
        )}
      </section>

      {/* Non-negotiables */}
      <section className="rounded-xl border border-border/60 bg-muted/20 p-6">
        <h2 className="font-semibold mb-4">
          {isAr ? "مبادئ غير قابلة للتفاوض" : "Non-negotiable principles"}
        </h2>
        <ul className="space-y-2">
          {(isAr
            ? [
                "لا scraping ولا شراء قوائم بيانات",
                "لا cold WhatsApp أو أتمتة LinkedIn",
                "كل إرسال خارجي يمرّ بموافقة بشرية",
                "لا أرقام أو نتائج مخترَعة — كل ادعاء له مصدر",
                "لا التزام مالي قبل موافقتك على النطاق",
              ]
            : [
                "No scraping or buying data lists",
                "No cold WhatsApp or LinkedIn automation",
                "Every external send passes human approval",
                "No invented numbers or results — every claim is sourced",
                "No financial commitment before you approve the scope",
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
