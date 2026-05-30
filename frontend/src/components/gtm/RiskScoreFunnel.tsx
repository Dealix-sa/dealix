"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";

/* ── Local client-side scoring ──────────────────────────── */
type Answers = {
  sector: string;
  companySize: string;
  pains: string[];
  aiUsage: string;
  zatcaStatus: string;
  pdplStatus: string;
  urgency: string;
  name: string;
  email: string;
  company: string;
};

function computeScore(a: Answers): {
  total: number;
  breakdown: { label: string; labelAr: string; value: number; max: number }[];
  tier: "critical" | "medium" | "low";
} {
  const breakdown = [
    {
      label: "AI Governance",
      labelAr: "حوكمة AI",
      value:
        a.aiUsage === "ungoverned" ? 30
        : a.aiUsage === "partial" ? 18
        : a.aiUsage === "governed" ? 6
        : 3,
      max: 30,
    },
    {
      label: "ZATCA Readiness",
      labelAr: "جاهزية ZATCA",
      value:
        a.zatcaStatus === "not_ready" ? 28
        : a.zatcaStatus === "partial" ? 16
        : a.zatcaStatus === "ready" ? 4
        : 10,
      max: 28,
    },
    {
      label: "Revenue Leakage",
      labelAr: "تسرّب الإيراد",
      value: a.pains.includes("leakage") ? 18 : a.pains.includes("conversion") ? 12 : 4,
      max: 18,
    },
    {
      label: "Data & CRM Quality",
      labelAr: "جودة البيانات",
      value: a.pains.includes("crm") ? 14 : a.pains.includes("visibility") ? 8 : 2,
      max: 14,
    },
    {
      label: "PDPL Compliance",
      labelAr: "امتثال PDPL",
      value:
        a.pdplStatus === "not_started" ? 10
        : a.pdplStatus === "partial" ? 5
        : 1,
      max: 10,
    },
  ];
  const total = breakdown.reduce((s, b) => s + b.value, 0);
  const tier: "critical" | "medium" | "low" =
    total >= 60 ? "critical" : total >= 30 ? "medium" : "low";
  return { total, breakdown, tier };
}

/* ── Static data ─────────────────────────────────────────── */
const SECTORS_AR = [
  { value: "real_estate", label: "العقارات" },
  { value: "healthcare", label: "الرعاية الصحية" },
  { value: "logistics", label: "اللوجستيات والنقل" },
  { value: "technology", label: "تقنية المعلومات / SaaS" },
  { value: "b2b_services", label: "خدمات B2B" },
  { value: "engineering", label: "الهندسة والمقاولات" },
  { value: "finance", label: "المالية والاستشارات" },
  { value: "marketing_agency", label: "وكالات التسويق" },
  { value: "other", label: "أخرى" },
];
const SECTORS_EN = [
  { value: "real_estate", label: "Real Estate" },
  { value: "healthcare", label: "Healthcare" },
  { value: "logistics", label: "Logistics & Transport" },
  { value: "technology", label: "Technology / SaaS" },
  { value: "b2b_services", label: "B2B Services" },
  { value: "engineering", label: "Engineering & Construction" },
  { value: "finance", label: "Finance & Consulting" },
  { value: "marketing_agency", label: "Marketing Agency" },
  { value: "other", label: "Other" },
];

const PAINS_AR = [
  { value: "leakage", label: "تسرّب إيراد غير مُفسَّر" },
  { value: "conversion", label: "ضعف تحويل العروض إلى عملاء" },
  { value: "crm", label: "بيانات CRM غير موثوقة" },
  { value: "ai_risk", label: "AI غير محكوم بدون governance" },
  { value: "zatca", label: "ZATCA Wave 24 — الموعد قبل يونيو 2026" },
  { value: "pdpl", label: "PDPL — حماية البيانات الشخصية" },
  { value: "visibility", label: "غياب الرؤية على قرارات الإيراد" },
];
const PAINS_EN = [
  { value: "leakage", label: "Unexplained revenue leakage" },
  { value: "conversion", label: "Low proposal-to-customer conversion" },
  { value: "crm", label: "Unreliable CRM / data quality" },
  { value: "ai_risk", label: "Ungoverned AI without oversight" },
  { value: "zatca", label: "ZATCA Wave 24 — June 2026 deadline" },
  { value: "pdpl", label: "PDPL — personal data compliance" },
  { value: "visibility", label: "No visibility on revenue decisions" },
];

/* ── Sub-components ──────────────────────────────────────── */
function SelectCard({
  options,
  selected,
  onSelect,
}: {
  options: { value: string; label: string }[];
  selected: string;
  onSelect: (v: string) => void;
}) {
  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          onClick={() => onSelect(o.value)}
          className={`rounded-lg border px-3 py-2.5 text-sm text-start transition-all ${
            selected === o.value
              ? "border-[#D4AF37] bg-[#D4AF37]/10 font-medium text-[#001F3F] dark:text-amber-200"
              : "border-border bg-card/50 text-muted-foreground hover:border-border/80 hover:bg-card"
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

function CheckGroup({
  options,
  selected,
  onToggle,
}: {
  options: { value: string; label: string }[];
  selected: string[];
  onToggle: (v: string) => void;
}) {
  return (
    <div className="space-y-2">
      {options.map((o) => {
        const checked = selected.includes(o.value);
        return (
          <label
            key={o.value}
            className={`flex cursor-pointer items-center gap-3 rounded-lg border px-4 py-3 transition-all ${
              checked
                ? "border-[#D4AF37] bg-[#D4AF37]/10"
                : "border-border bg-card/50 hover:border-border/80"
            }`}
          >
            <span
              className={`flex h-4 w-4 flex-shrink-0 items-center justify-center rounded border text-xs font-bold transition-colors ${
                checked
                  ? "border-[#D4AF37] bg-[#D4AF37] text-white"
                  : "border-muted-foreground/40"
              }`}
            >
              {checked ? "✓" : ""}
            </span>
            <input
              type="checkbox"
              className="sr-only"
              checked={checked}
              onChange={() => onToggle(o.value)}
            />
            <span className="text-sm">{o.label}</span>
          </label>
        );
      })}
    </div>
  );
}

function ScoreRing({ score }: { score: number }) {
  const r = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(score, 100) / 100;
  const color =
    score >= 60 ? "#ef4444" : score >= 30 ? "#f59e0b" : "#10b981";
  return (
    <svg width="120" height="120" viewBox="0 0 120 120">
      <circle cx="60" cy="60" r={r} fill="none" stroke="#e5e7eb" strokeWidth="12" />
      <circle
        cx="60"
        cy="60"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="12"
        strokeLinecap="round"
        strokeDasharray={circ}
        strokeDashoffset={circ * (1 - pct)}
        transform="rotate(-90 60 60)"
        style={{ transition: "stroke-dashoffset 1s ease" }}
      />
      <text x="60" y="56" textAnchor="middle" fontSize="22" fontWeight="700" fill={color}>
        {score}
      </text>
      <text x="60" y="72" textAnchor="middle" fontSize="10" fill="#6b7280">
        /100
      </text>
    </svg>
  );
}

/* ── Main component ──────────────────────────────────────── */
const EMPTY: Answers = {
  sector: "",
  companySize: "",
  pains: [],
  aiUsage: "",
  zatcaStatus: "",
  pdplStatus: "",
  urgency: "",
  name: "",
  email: "",
  company: "",
};

export function RiskScoreFunnel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Answers>(EMPTY);
  const [result, setResult] = useState<ReturnType<typeof computeScore> | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [sendBusy, setSendBusy] = useState(false);

  const dir = isAr ? "rtl" : "ltr";
  const sectors = isAr ? SECTORS_AR : SECTORS_EN;
  const pains = isAr ? PAINS_AR : PAINS_EN;

  const setA = (k: keyof Answers, v: string | string[]) =>
    setAnswers((a) => ({ ...a, [k]: v }));

  const togglePain = (v: string) =>
    setA(
      "pains",
      answers.pains.includes(v)
        ? answers.pains.filter((p) => p !== v)
        : [...answers.pains, v]
    );

  function handleCompute() {
    const r = computeScore(answers);
    setResult(r);
    setStep(4);
    // fire-and-forget to backend — doesn't block
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "";
      if (base) {
        fetch(`${base}/api/v1/public/risk-score`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            industry: answers.sector,
            ai_usage: answers.aiUsage,
            urgency: answers.urgency,
            pain: answers.pains.join(", "),
            notes: `zatca:${answers.zatcaStatus} pdpl:${answers.pdplStatus}`,
          }),
        }).catch(() => {});
      }
    } catch {}
  }

  async function handleCapture(e: React.FormEvent) {
    e.preventDefault();
    if (!answers.name || !answers.email) return;
    setSendBusy(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "";
      if (base) {
        await fetch(`${base}/api/v1/public/lead`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: answers.name,
            email: answers.email,
            company: answers.company,
            industry: answers.sector,
            source: "risk_score_funnel",
            pain: answers.pains.join(", "),
          }),
        }).catch(() => {});
      }
    } finally {
      setSendBusy(false);
      setSubmitted(true);
    }
  }

  /* ── Step renderers ───── */
  const STEPS = [
    /* 0: sector */
    <div key="sector" className="space-y-5">
      <div>
        <h2 className="text-xl font-bold">
          {isAr ? "ما قطاع شركتك؟" : "What's your company sector?"}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          {isAr ? "اختر القطاع الأقرب لعملك" : "Select the closest to your business"}
        </p>
      </div>
      <SelectCard options={sectors} selected={answers.sector} onSelect={(v) => setA("sector", v)} />
      <button
        type="button"
        disabled={!answers.sector}
        onClick={() => setStep(1)}
        className="w-full rounded-lg bg-[#001F3F] py-3 text-sm font-semibold text-white transition-opacity disabled:opacity-40 hover:bg-[#000a1e]"
      >
        {isAr ? "التالي ←" : "Next →"}
      </button>
    </div>,

    /* 1: pain points */
    <div key="pains" className="space-y-5">
      <div>
        <h2 className="text-xl font-bold">
          {isAr ? "ما التحديات التشغيلية التي تواجهها؟" : "What operational challenges do you face?"}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          {isAr ? "اختر كل ما ينطبق" : "Select all that apply"}
        </p>
      </div>
      <CheckGroup options={pains} selected={answers.pains} onToggle={togglePain} />
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => setStep(0)}
          className="flex-1 rounded-lg border border-border py-3 text-sm font-medium hover:bg-muted/30"
        >
          {isAr ? "→ السابق" : "← Back"}
        </button>
        <button
          type="button"
          disabled={answers.pains.length === 0}
          onClick={() => setStep(2)}
          className="flex-[2] rounded-lg bg-[#001F3F] py-3 text-sm font-semibold text-white transition-opacity disabled:opacity-40 hover:bg-[#000a1e]"
        >
          {isAr ? "التالي ←" : "Next →"}
        </button>
      </div>
    </div>,

    /* 2: compliance status */
    <div key="compliance" className="space-y-6">
      <div>
        <h2 className="text-xl font-bold">
          {isAr ? "حالة الامتثال التنظيمي" : "Regulatory compliance status"}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          {isAr ? "ZATCA Wave 24 — الموعد النهائي 30 يونيو 2026" : "ZATCA Wave 24 — deadline June 30, 2026"}
        </p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-medium">{isAr ? "جاهزية ZATCA E-Invoicing" : "ZATCA E-Invoicing readiness"}</p>
        <SelectCard
          options={
            isAr
              ? [
                  { value: "not_ready", label: "غير جاهز" },
                  { value: "partial", label: "جزئي" },
                  { value: "ready", label: "جاهز" },
                  { value: "unsure", label: "غير متأكد" },
                ]
              : [
                  { value: "not_ready", label: "Not ready" },
                  { value: "partial", label: "Partially ready" },
                  { value: "ready", label: "Fully ready" },
                  { value: "unsure", label: "Not sure" },
                ]
          }
          selected={answers.zatcaStatus}
          onSelect={(v) => setA("zatcaStatus", v)}
        />
      </div>

      <div className="space-y-2">
        <p className="text-sm font-medium">{isAr ? "استخدام AI في شركتك" : "AI usage in your company"}</p>
        <SelectCard
          options={
            isAr
              ? [
                  { value: "ungoverned", label: "نستخدم AI بدون governance" },
                  { value: "partial", label: "بعض الضوابط" },
                  { value: "governed", label: "محكوم بالكامل" },
                  { value: "none", label: "لا نستخدم AI" },
                ]
              : [
                  { value: "ungoverned", label: "Using AI without governance" },
                  { value: "partial", label: "Some controls in place" },
                  { value: "governed", label: "Fully governed" },
                  { value: "none", label: "Not using AI" },
                ]
          }
          selected={answers.aiUsage}
          onSelect={(v) => setA("aiUsage", v)}
        />
      </div>

      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => setStep(1)}
          className="flex-1 rounded-lg border border-border py-3 text-sm font-medium hover:bg-muted/30"
        >
          {isAr ? "→ السابق" : "← Back"}
        </button>
        <button
          type="button"
          disabled={!answers.zatcaStatus || !answers.aiUsage}
          onClick={() => setStep(3)}
          className="flex-[2] rounded-lg bg-[#001F3F] py-3 text-sm font-semibold text-white transition-opacity disabled:opacity-40 hover:bg-[#000a1e]"
        >
          {isAr ? "احسب النتيجة ←" : "Calculate score →"}
        </button>
      </div>
    </div>,

    /* 3: contact + compute */
    <div key="contact" className="space-y-5">
      <div>
        <h2 className="text-xl font-bold">
          {isAr ? "أرسل لك نتيجتك مع تحليل مخصص" : "Send you your score with a custom analysis"}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          {isAr
            ? "ستظهر النتيجة فوراً — البريد اختياري للحصول على التحليل الكامل"
            : "Score shows immediately — email optional for the full analysis"}
        </p>
      </div>
      <div className="space-y-3">
        {(
          isAr
            ? [
                { key: "name", label: "الاسم", placeholder: "محمد العمر" },
                { key: "company", label: "الشركة", placeholder: "شركة الأفق" },
                { key: "email", label: "البريد الإلكتروني", placeholder: "m@company.com.sa" },
              ]
            : [
                { key: "name", label: "Name", placeholder: "John Smith" },
                { key: "company", label: "Company", placeholder: "Al Ufuq Co." },
                { key: "email", label: "Email", placeholder: "j@company.com" },
              ]
        ).map(({ key, label, placeholder }) => (
          <div key={key} className="space-y-1">
            <label className="text-sm font-medium">{label}</label>
            <input
              type={key === "email" ? "email" : "text"}
              placeholder={placeholder}
              value={String(answers[key as keyof Answers] ?? "")}
              onChange={(e) => setA(key as keyof Answers, e.target.value)}
              className="w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-[#D4AF37] focus:ring-1 focus:ring-[#D4AF37]"
            />
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => setStep(2)}
          className="flex-1 rounded-lg border border-border py-3 text-sm font-medium hover:bg-muted/30"
        >
          {isAr ? "→ السابق" : "← Back"}
        </button>
        <button
          type="button"
          onClick={handleCompute}
          className="flex-[2] rounded-lg bg-[#D4AF37] py-3 text-sm font-bold text-[#001F3F] hover:bg-[#c29d2e] transition-colors"
        >
          {isAr ? "أظهر نتيجتي ◀" : "Show my score ▶"}
        </button>
      </div>
    </div>,

    /* 4: result */
    result && (
      <div key="result" className="space-y-6">
        {/* Score header */}
        <div className="flex flex-col items-center gap-3 rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] py-8 text-white">
          <ScoreRing score={result.total} />
          <p className="text-lg font-bold">
            {result.tier === "critical"
              ? isAr ? "مستوى حرج — تدخّل فوري مطلوب" : "Critical — immediate action required"
              : result.tier === "medium"
              ? isAr ? "مخاطر متوسطة — راجع الأولويات" : "Medium risk — review priorities"
              : isAr ? "منخفض — استمر في المراقبة" : "Low risk — keep monitoring"}
          </p>
          <p className="text-xs text-white/60">
            {isAr
              ? "تقدير تشغيلي — ليس تأهيلاً نهائياً بدون مراجعة بشرية"
              : "Operational estimate — not final without human review"}
          </p>
        </div>

        {/* Breakdown */}
        <div className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {isAr ? "تفاصيل النتيجة" : "Score breakdown"}
          </p>
          {result.breakdown.map((b) => (
            <div key={b.label} className="flex items-center gap-3">
              <span className="w-36 flex-shrink-0 text-xs text-muted-foreground">
                {isAr ? b.labelAr : b.label}
              </span>
              <div className="flex-1 rounded-full bg-muted h-2 overflow-hidden">
                <div
                  className="h-full rounded-full bg-[#D4AF37] transition-all duration-700"
                  style={{ width: `${(b.value / b.max) * 100}%` }}
                />
              </div>
              <span className="w-10 text-right text-xs font-medium">{b.value}/{b.max}</span>
            </div>
          ))}
        </div>

        {/* CTA based on tier */}
        {result.tier === "critical" ? (
          <div className="rounded-xl border border-red-500/30 bg-red-50/30 dark:bg-red-950/10 p-5">
            <p className="font-bold text-red-700 dark:text-red-400">
              {isAr ? "الخطر عالٍ — ابدأ الآن" : "High risk — start now"}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {isAr
                ? "Sprint 7 أيام يكشف أبرز مصادر الخسارة ويقدم Proof Pack كامل قابل للعرض على إدارتك."
                : "7-day Sprint identifies your top loss drivers and delivers a full Proof Pack ready for your management."}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link
                href={`/${locale}/dealix-diagnostic`}
                className="rounded-lg bg-[#001F3F] text-white px-4 py-2 text-sm font-semibold hover:bg-[#000a1e] transition-colors"
              >
                {isAr ? "ابدأ Sprint — 499 ريال" : "Start Sprint — SAR 499"}
              </Link>
              <Link
                href={`/${locale}/services`}
                className="rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium hover:bg-muted/30 transition-colors"
              >
                {isAr ? "شاهد الخدمات" : "View services"}
              </Link>
            </div>
          </div>
        ) : result.tier === "medium" ? (
          <div className="rounded-xl border border-amber-500/30 bg-amber-50/30 dark:bg-amber-950/10 p-5">
            <p className="font-bold text-amber-700 dark:text-amber-400">
              {isAr ? "مخاطر يمكن معالجتها الآن" : "Manageable risks — act before they grow"}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {isAr
                ? "Diagnostic مجاني يحدد أولوياتك — ثم Sprint 499 ريال لحل 2-3 مشاكل محددة."
                : "Free diagnostic identifies your priorities — then Sprint SAR 499 to fix 2-3 specific issues."}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link
                href={`/${locale}/dealix-diagnostic`}
                className="rounded-lg bg-[#D4AF37] text-[#001F3F] px-4 py-2 text-sm font-semibold hover:bg-[#c29d2e] transition-colors"
              >
                {isAr ? "تشخيص مجاني" : "Free diagnostic"}
              </Link>
              <Link
                href={`/${locale}/learn`}
                className="rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium hover:bg-muted/30 transition-colors"
              >
                {isAr ? "اقرأ المكتبة" : "Read guides"}
              </Link>
            </div>
          </div>
        ) : (
          <div className="rounded-xl border border-emerald-500/30 bg-emerald-50/30 dark:bg-emerald-950/10 p-5">
            <p className="font-bold text-emerald-700 dark:text-emerald-400">
              {isAr ? "وضعك جيد — حافظ عليه" : "Your position is solid — keep it that way"}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {isAr
                ? "استمر في مراقبة ZATCA و PDPL — تواصل معنا إذا تغيّر أي شيء."
                : "Keep monitoring ZATCA & PDPL — reach out if anything changes."}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <Link
                href={`/${locale}/learn`}
                className="rounded-lg bg-[#001F3F] text-white px-4 py-2 text-sm font-semibold hover:bg-[#000a1e] transition-colors"
              >
                {isAr ? "مكتبة المعرفة" : "Knowledge library"}
              </Link>
            </div>
          </div>
        )}

        {/* Lead capture if not submitted */}
        {!submitted ? (
          <form onSubmit={handleCapture} className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-3">
            <p className="text-sm font-semibold">
              {isAr ? "احفظ نتيجتك واحصل على تحليل مخصص" : "Save your score and get a custom analysis"}
            </p>
            {answers.email ? (
              <p className="text-xs text-muted-foreground">
                {isAr ? `سنرسل التحليل إلى ${answers.email}` : `We'll send the analysis to ${answers.email}`}
              </p>
            ) : (
              <input
                type="email"
                required
                placeholder={isAr ? "بريدك الإلكتروني" : "Your email"}
                value={answers.email}
                onChange={(e) => setA("email", e.target.value)}
                className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm outline-none focus:border-[#D4AF37]"
              />
            )}
            <button
              type="submit"
              disabled={sendBusy || !answers.email}
              className="w-full rounded-lg bg-[#001F3F] py-2.5 text-sm font-semibold text-white transition-opacity disabled:opacity-40 hover:bg-[#000a1e]"
            >
              {sendBusy
                ? isAr ? "جارٍ الإرسال..." : "Sending..."
                : isAr ? "أرسل لي التحليل" : "Send me the analysis"}
            </button>
            <p className="text-xs text-muted-foreground">
              {isAr ? "لا رسائل تلقائية — موافقة مطلوبة قبل أي تواصل تجاري." : "No automation — approval required before any commercial outreach."}
            </p>
          </form>
        ) : (
          <div className="rounded-xl border border-emerald-500/30 bg-emerald-50/30 dark:bg-emerald-950/10 p-5 text-center">
            <p className="font-semibold text-emerald-700 dark:text-emerald-300">
              {isAr ? "تم الإرسال ✓" : "Sent ✓"}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {isAr ? "سنتواصل معك خلال 24 ساعة." : "We'll reach out within 24 hours."}
            </p>
          </div>
        )}

        <button
          type="button"
          onClick={() => { setStep(0); setAnswers(EMPTY); setResult(null); setSubmitted(false); }}
          className="text-xs text-muted-foreground underline underline-offset-2 hover:text-foreground"
        >
          {isAr ? "ابدأ من جديد" : "Start over"}
        </button>
      </div>
    ),
  ];

  /* ── Progress indicator ── */
  const totalSteps = 4;

  return (
    <div className="mx-auto max-w-xl px-4 py-10" dir={dir}>
      {/* Header */}
      <div className={`mb-8 ${isAr ? "text-right" : ""}`}>
        <span className="inline-block rounded-full bg-amber-100 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 text-xs font-medium px-3 py-1 mb-3">
          {isAr ? "مجاني — نتيجة فورية" : "Free — instant result"}
        </span>
        <h1 className="text-3xl font-bold">
          {isAr ? "Risk Score — AI & Revenue Ops" : "Risk Score — AI & Revenue Ops"}
        </h1>
        <p className="mt-2 text-muted-foreground">
          {isAr
            ? "3 خطوات فقط — نتيجتك جاهزة في أقل من دقيقة"
            : "3 steps only — your score ready in under a minute"}
        </p>

        {/* ZATCA urgency bar */}
        <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-500/20 bg-red-50/30 dark:bg-red-950/10 px-4 py-2">
          <span className="text-red-500 text-sm">⚠</span>
          <p className="text-xs text-red-700 dark:text-red-400 font-medium">
            {isAr
              ? "ZATCA Wave 24 — 31 يوماً متبقياً (30 يونيو 2026)"
              : "ZATCA Wave 24 — 31 days remaining (June 30, 2026)"}
          </p>
        </div>
      </div>

      {/* Progress bar */}
      {step < totalSteps && (
        <div className="mb-6 flex gap-1.5">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                i <= step ? "bg-[#D4AF37]" : "bg-muted"
              }`}
            />
          ))}
        </div>
      )}

      {/* Step content */}
      {STEPS[step]}
    </div>
  );
}
