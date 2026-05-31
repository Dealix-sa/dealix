"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type IndustrySector =
  | "fintech"
  | "real_estate"
  | "healthcare_clinic"
  | "b2b_saas"
  | "logistics"
  | "engineering"
  | "agency"
  | "other";

type TeamSize = "1-10" | "11-50" | "51-200" | "200+";

type OnboardingProcess = "yes" | "partial" | "no";

type ReportTime = "< 1hr" | "1-4hrs" | "> 4hrs" | "we_dont_do_reports";

type ZatcaStatus = "yes" | "working_on_it" | "no" | "not_sure";

type RevenueRange = "< 25K SAR" | "25K-100K" | "100K-500K" | "500K+";

type Bottleneck =
  | "lead_generation"
  | "delivery_quality"
  | "client_retention"
  | "invoicing_compliance"
  | "team_capacity"
  | "data_reporting";

interface FunnelAnswers {
  company_name: string;
  industry: IndustrySector | "";
  team_size: TeamSize | "";
  onboarding_process: OnboardingProcess | "";
  report_time: ReportTime | "";
  zatca_status: ZatcaStatus | "";
  revenue_range: RevenueRange | "";
  bottleneck: Bottleneck | "";
}

interface RiskFinding {
  label_ar: string;
  label_en: string;
  severity: "high" | "medium" | "low";
}

// ---------------------------------------------------------------------------
// Score computation (client-side only — no PII leaves the browser)
// ---------------------------------------------------------------------------

function computeScore(answers: FunnelAnswers): number {
  let base = 50;
  if (answers.onboarding_process === "no") base += 15;
  else if (answers.onboarding_process === "partial") base += 7;
  if (answers.report_time === "> 4hrs") base += 15;
  else if (answers.report_time === "1-4hrs") base += 7;
  if (answers.zatca_status === "no") base += 20;
  else if (answers.zatca_status === "not_sure") base += 10;
  if (answers.revenue_range === "500K+") base += 10;
  if (answers.bottleneck === "delivery_quality") base += 10;
  return Math.min(base, 95);
}

function getRiskFindings(answers: FunnelAnswers): RiskFinding[] {
  const findings: RiskFinding[] = [];

  if (answers.onboarding_process === "no" || answers.onboarding_process === "partial") {
    findings.push({
      label_ar: "غياب عملية موثّقة لتأهيل العملاء يُعرّض رضا العملاء للخطر",
      label_en: "Undocumented onboarding process puts client satisfaction at risk",
      severity: answers.onboarding_process === "no" ? "high" : "medium",
    });
  }
  if (answers.report_time === "> 4hrs" || answers.report_time === "we_dont_do_reports") {
    findings.push({
      label_ar: "إعداد التقارير اليدوي يستنزف وقت الفريق ويقلّل جودة البيانات",
      label_en: "Manual reporting drains team time and degrades data quality",
      severity: answers.report_time === "we_dont_do_reports" ? "high" : "medium",
    });
  }
  if (answers.zatca_status === "no" || answers.zatca_status === "not_sure") {
    findings.push({
      label_ar: "عدم الامتثال لـ ZATCA Phase 2 يُعرّضك لغرامات تنظيمية",
      label_en: "Non-compliance with ZATCA Phase 2 exposes you to regulatory penalties",
      severity: answers.zatca_status === "no" ? "high" : "medium",
    });
  }
  if (answers.bottleneck === "delivery_quality") {
    findings.push({
      label_ar: "جودة التسليم هي العائق الرئيسي — يُقلّل من معدل الاحتفاظ بالعملاء",
      label_en: "Delivery quality bottleneck directly reduces client retention rate",
      severity: "high",
    });
  }
  if (answers.bottleneck === "lead_generation") {
    findings.push({
      label_ar: "ضعف توليد العملاء المحتملين يحدّ من نمو الإيرادات",
      label_en: "Weak lead generation caps revenue growth",
      severity: "medium",
    });
  }
  if (findings.length === 0) {
    findings.push({
      label_ar: "لا توجد مخاطر حرجة — فرصة للتحسين المستمر",
      label_en: "No critical risks detected — opportunity for continuous improvement",
      severity: "low",
    });
  }
  return findings.slice(0, 3);
}

function getRecommendedTier(score: number): { name_ar: string; name_en: string; description_ar: string; description_en: string } {
  if (score >= 66) {
    return {
      name_ar: "Managed Ops — إدارة كاملة",
      name_en: "Managed Ops — Full Management",
      description_ar: "مستوى المخاطر مرتفع — تحتاج إلى تدخّل عملياتي شامل وفوري",
      description_en: "High risk level — requires immediate comprehensive operational intervention",
    };
  }
  if (score >= 40) {
    return {
      name_ar: "Data Pack — حزمة البيانات",
      name_en: "Data Pack — Data Package",
      description_ar: "مستوى مخاطر متوسط — ابدأ بأتمتة التقارير وتنظيم البيانات",
      description_en: "Medium risk level — start with report automation and data organization",
    };
  }
  return {
    name_ar: "Sprint — حزمة الانطلاق",
    name_en: "Sprint — Starter Package",
    description_ar: "مخاطر منخفضة — Sprint سريع يرسّخ العمليات ويُعجّل النمو",
    description_en: "Low risk — a quick Sprint cements your processes and accelerates growth",
  };
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

const STEP_LABELS_AR = ["ملف الشركة", "نقاط الألم", "لقطة الإيراد", "النتائج"];
const STEP_LABELS_EN = ["Company Profile", "Current Pain", "Revenue Snapshot", "Results"];

function StepIndicator({ current, total, isAr }: { current: number; total: number; isAr: boolean }) {
  const labels = isAr ? STEP_LABELS_AR : STEP_LABELS_EN;
  const pct = ((current - 1) / (total - 1)) * 100;
  return (
    <div className="mb-8">
      <Progress value={pct} className="h-2 mb-4" />
      <div className="flex justify-between text-xs text-muted-foreground">
        {labels.map((l, i) => (
          <span
            key={l}
            className={i + 1 === current ? "text-[var(--dealix-deep-green)] font-semibold" : ""}
          >
            {l}
          </span>
        ))}
      </div>
    </div>
  );
}

function FieldGroup({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium">{label}</label>
      {children}
    </div>
  );
}

function SelectField({
  value,
  onChange,
  options,
  placeholder,
}: {
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
  placeholder: string;
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--dealix-deep-green)]"
    >
      <option value="">{placeholder}</option>
      {options.map((o) => (
        <option key={o.value} value={o.value}>
          {o.label}
        </option>
      ))}
    </select>
  );
}

function RadioGroup({
  value,
  onChange,
  options,
}: {
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label_ar: string; label_en: string }[];
}) {
  return (
    <div className="flex flex-col gap-2">
      {options.map((o) => (
        <label
          key={o.value}
          className={`flex items-center gap-3 rounded-lg border px-4 py-3 cursor-pointer transition-colors ${
            value === o.value
              ? "border-[var(--dealix-deep-green)] bg-[var(--dealix-deep-green)]/5"
              : "border-border hover:border-[var(--dealix-deep-green)]/40"
          }`}
        >
          <input
            type="radio"
            name={o.value}
            checked={value === o.value}
            onChange={() => onChange(o.value)}
            className="accent-[var(--dealix-deep-green)]"
          />
          <span className="text-sm">
            <span className="font-medium">{o.label_ar}</span>
            <span className="text-muted-foreground"> / {o.label_en}</span>
          </span>
        </label>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Animated score counter
// ---------------------------------------------------------------------------

function AnimatedScore({ target, isAr }: { target: number; isAr: boolean }) {
  const [displayed, setDisplayed] = useState(0);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    const start = performance.now();
    const duration = 1200;
    const animate = (now: number) => {
      const elapsed = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - elapsed, 3);
      setDisplayed(Math.round(eased * target));
      if (elapsed < 1) {
        rafRef.current = requestAnimationFrame(animate);
      }
    };
    rafRef.current = requestAnimationFrame(animate);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, [target]);

  const color =
    target < 40
      ? "text-green-600"
      : target <= 65
      ? "text-amber-600"
      : "text-red-600";

  const levelAr = target < 40 ? "منخفض" : target <= 65 ? "متوسط" : "مرتفع";
  const levelEn = target < 40 ? "Low" : target <= 65 ? "Medium" : "High";

  return (
    <div className="text-center py-6">
      <div className={`text-7xl font-black tabular-nums ${color}`}>{displayed}</div>
      <div className="text-muted-foreground text-sm mt-1">/100</div>
      <div className="mt-3">
        <Badge
          className={`text-sm px-4 py-1 ${
            target < 40
              ? "bg-green-100 text-green-800 border-green-300"
              : target <= 65
              ? "bg-amber-100 text-amber-800 border-amber-300"
              : "bg-red-100 text-red-800 border-red-300"
          }`}
          variant="outline"
        >
          {isAr ? `مستوى الخطر: ${levelAr}` : `Risk Level: ${levelEn}`}
        </Badge>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function DiagnosticFunnel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState<FunnelAnswers>({
    company_name: "",
    industry: "",
    team_size: "",
    onboarding_process: "",
    report_time: "",
    zatca_status: "",
    revenue_range: "",
    bottleneck: "",
  });

  const set = <K extends keyof FunnelAnswers>(key: K, value: FunnelAnswers[K]) =>
    setAnswers((prev) => ({ ...prev, [key]: value }));

  const canNext = () => {
    if (step === 1) return answers.company_name.trim() !== "" && answers.industry !== "" && answers.team_size !== "";
    if (step === 2) return answers.onboarding_process !== "" && answers.report_time !== "" && answers.zatca_status !== "";
    if (step === 3) return answers.revenue_range !== "" && answers.bottleneck !== "";
    return true;
  };

  const score = step === 4 ? computeScore(answers) : 0;
  const findings = step === 4 ? getRiskFindings(answers) : [];
  const tier = step === 4 ? getRecommendedTier(score) : null;

  const industrySectorOptions = [
    { value: "fintech", label: isAr ? "تقنية مالية (Fintech)" : "Fintech" },
    { value: "real_estate", label: isAr ? "عقارات" : "Real Estate" },
    { value: "healthcare_clinic", label: isAr ? "رعاية صحية / عيادة" : "Healthcare / Clinic" },
    { value: "b2b_saas", label: isAr ? "برمجيات B2B (SaaS)" : "B2B SaaS" },
    { value: "logistics", label: isAr ? "لوجستيات" : "Logistics" },
    { value: "engineering", label: isAr ? "هندسة / مقاولات" : "Engineering / Contracting" },
    { value: "agency", label: isAr ? "وكالة / استشارات" : "Agency / Consulting" },
    { value: "other", label: isAr ? "أخرى" : "Other" },
  ];

  const teamSizeOptions = [
    { value: "1-10", label: "1–10" },
    { value: "11-50", label: "11–50" },
    { value: "51-200", label: "51–200" },
    { value: "200+", label: "200+" },
  ];

  const bottleneckOptions = [
    { value: "lead_generation", label: isAr ? "توليد عملاء محتملين" : "Lead generation" },
    { value: "delivery_quality", label: isAr ? "جودة التسليم" : "Delivery quality" },
    { value: "client_retention", label: isAr ? "الاحتفاظ بالعملاء" : "Client retention" },
    { value: "invoicing_compliance", label: isAr ? "الفواتير / الامتثال" : "Invoicing / Compliance" },
    { value: "team_capacity", label: isAr ? "طاقة الفريق" : "Team capacity" },
    { value: "data_reporting", label: isAr ? "البيانات / التقارير" : "Data / Reporting" },
  ];

  return (
    <div className="max-w-2xl mx-auto" dir={isAr ? "rtl" : "ltr"}>
      <StepIndicator current={step} total={4} isAr={isAr} />

      {/* Step 1 — Company Profile */}
      {step === 1 && (
        <Card className="p-6 space-y-5">
          <div>
            <h2 className="text-xl font-bold text-[var(--dealix-deep-green)]">
              {isAr ? "ملف الشركة" : "Company Profile"}
            </h2>
            <p className="text-sm text-muted-foreground mt-1">
              {isAr ? "خطوة 1 من 3 — معلومات أساسية" : "Step 1 of 3 — Basic information"}
            </p>
          </div>

          <FieldGroup label={isAr ? "اسم الشركة" : "Company name"}>
            <input
              type="text"
              value={answers.company_name}
              onChange={(e) => set("company_name", e.target.value)}
              placeholder={isAr ? "مثال: شركة النخبة للتقنية" : "e.g. Acme Technology Co."}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--dealix-deep-green)]"
            />
          </FieldGroup>

          <FieldGroup label={isAr ? "القطاع" : "Industry sector"}>
            <SelectField
              value={answers.industry}
              onChange={(v) => set("industry", v as IndustrySector)}
              options={industrySectorOptions}
              placeholder={isAr ? "اختر القطاع..." : "Select sector..."}
            />
          </FieldGroup>

          <FieldGroup label={isAr ? "حجم الفريق" : "Team size"}>
            <SelectField
              value={answers.team_size}
              onChange={(v) => set("team_size", v as TeamSize)}
              options={teamSizeOptions}
              placeholder={isAr ? "اختر الحجم..." : "Select size..."}
            />
          </FieldGroup>

          <Button
            className="w-full bg-[var(--dealix-deep-green)] hover:bg-[var(--dealix-deep-green)]/90"
            disabled={!canNext()}
            onClick={() => setStep(2)}
          >
            {isAr ? "التالي ←" : "Next →"}
          </Button>
        </Card>
      )}

      {/* Step 2 — Current Pain */}
      {step === 2 && (
        <Card className="p-6 space-y-6">
          <div>
            <h2 className="text-xl font-bold text-[var(--dealix-deep-green)]">
              {isAr ? "نقاط الألم الحالية" : "Current Pain Points"}
            </h2>
            <p className="text-sm text-muted-foreground mt-1">
              {isAr ? "خطوة 2 من 3 — تقييم العمليات" : "Step 2 of 3 — Operations assessment"}
            </p>
          </div>

          <FieldGroup
            label={
              isAr
                ? "هل لديك عملية موثقة لتأهيل العملاء؟"
                : "Do you have a documented client onboarding process?"
            }
          >
            <RadioGroup
              value={answers.onboarding_process}
              onChange={(v) => set("onboarding_process", v as OnboardingProcess)}
              options={[
                { value: "yes", label_ar: "نعم، موثّقة ومطبّقة", label_en: "Yes, documented and applied" },
                { value: "partial", label_ar: "جزئياً — غير مكتملة", label_en: "Partial — not fully documented" },
                { value: "no", label_ar: "لا، تعتمد على الخبرة الشخصية", label_en: "No, relies on personal experience" },
              ]}
            />
          </FieldGroup>

          <FieldGroup
            label={
              isAr
                ? "كم وقت يستغرق إعداد تقرير أداء واحد؟"
                : "How long does one performance report take?"
            }
          >
            <RadioGroup
              value={answers.report_time}
              onChange={(v) => set("report_time", v as ReportTime)}
              options={[
                { value: "< 1hr", label_ar: "أقل من ساعة", label_en: "Less than 1 hour" },
                { value: "1-4hrs", label_ar: "1 إلى 4 ساعات", label_en: "1 to 4 hours" },
                { value: "> 4hrs", label_ar: "أكثر من 4 ساعات", label_en: "More than 4 hours" },
                { value: "we_dont_do_reports", label_ar: "لا نُعِدّ تقارير", label_en: "We don't do reports" },
              ]}
            />
          </FieldGroup>

          <FieldGroup
            label={
              isAr
                ? "هل تمتثل فواتيركم لمتطلبات ZATCA Phase 2؟"
                : "Are your invoices ZATCA Phase 2 compliant?"
            }
          >
            <RadioGroup
              value={answers.zatca_status}
              onChange={(v) => set("zatca_status", v as ZatcaStatus)}
              options={[
                { value: "yes", label_ar: "نعم، ممتثل بالكامل", label_en: "Yes, fully compliant" },
                { value: "working_on_it", label_ar: "نعمل على ذلك", label_en: "Working on it" },
                { value: "no", label_ar: "لا، غير ممتثل", label_en: "No, not compliant" },
                { value: "not_sure", label_ar: "غير متأكد", label_en: "Not sure" },
              ]}
            />
          </FieldGroup>

          <div className="flex gap-3">
            <Button variant="outline" className="flex-1" onClick={() => setStep(1)}>
              {isAr ? "→ السابق" : "← Back"}
            </Button>
            <Button
              className="flex-1 bg-[var(--dealix-deep-green)] hover:bg-[var(--dealix-deep-green)]/90"
              disabled={!canNext()}
              onClick={() => setStep(3)}
            >
              {isAr ? "التالي ←" : "Next →"}
            </Button>
          </div>
        </Card>
      )}

      {/* Step 3 — Revenue Snapshot */}
      {step === 3 && (
        <Card className="p-6 space-y-6">
          <div>
            <h2 className="text-xl font-bold text-[var(--dealix-deep-green)]">
              {isAr ? "لقطة الإيراد" : "Revenue Snapshot"}
            </h2>
            <p className="text-sm text-muted-foreground mt-1">
              {isAr ? "خطوة 3 من 3 — الوضع المالي" : "Step 3 of 3 — Financial picture"}
            </p>
          </div>

          <FieldGroup
            label={isAr ? "نطاق الإيرادات الشهرية المتكررة (MRR)" : "Monthly recurring revenue range (MRR)"}
          >
            <RadioGroup
              value={answers.revenue_range}
              onChange={(v) => set("revenue_range", v as RevenueRange)}
              options={[
                { value: "< 25K SAR", label_ar: "أقل من 25,000 ر.س", label_en: "Less than 25K SAR" },
                { value: "25K-100K", label_ar: "25,000 – 100,000 ر.س", label_en: "25K – 100K SAR" },
                { value: "100K-500K", label_ar: "100,000 – 500,000 ر.س", label_en: "100K – 500K SAR" },
                { value: "500K+", label_ar: "أكثر من 500,000 ر.س", label_en: "500K+ SAR" },
              ]}
            />
          </FieldGroup>

          <FieldGroup
            label={isAr ? "أكبر عائق حالي لديك" : "Current biggest bottleneck"}
          >
            <SelectField
              value={answers.bottleneck}
              onChange={(v) => set("bottleneck", v as Bottleneck)}
              options={bottleneckOptions}
              placeholder={isAr ? "اختر العائق..." : "Select bottleneck..."}
            />
          </FieldGroup>

          <div className="flex gap-3">
            <Button variant="outline" className="flex-1" onClick={() => setStep(2)}>
              {isAr ? "→ السابق" : "← Back"}
            </Button>
            <Button
              className="flex-1 bg-[var(--dealix-deep-green)] hover:bg-[var(--dealix-deep-green)]/90"
              disabled={!canNext()}
              onClick={() => setStep(4)}
            >
              {isAr ? "احسب النتيجة" : "Calculate Score"}
            </Button>
          </div>
        </Card>
      )}

      {/* Step 4 — Results */}
      {step === 4 && (
        <div className="space-y-6">
          <Card className="p-6">
            <h2 className="text-xl font-bold text-[var(--dealix-deep-green)] text-center mb-2">
              {isAr ? "درجة مخاطر الإيراد" : "Revenue Risk Score"}
            </h2>
            <p className="text-sm text-muted-foreground text-center mb-4">
              {isAr
                ? `تقييم لشركة: ${answers.company_name}`
                : `Assessment for: ${answers.company_name}`}
            </p>
            <AnimatedScore target={score} isAr={isAr} />
          </Card>

          <Card className="p-6 space-y-4">
            <h3 className="font-semibold text-[var(--dealix-deep-green)]">
              {isAr ? "أبرز النتائج" : "Key Findings"}
            </h3>
            <div className="space-y-3">
              {findings.map((f, i) => (
                <div
                  key={i}
                  className={`flex gap-3 p-3 rounded-lg border ${
                    f.severity === "high"
                      ? "border-red-200 bg-red-50 dark:bg-red-950/20"
                      : f.severity === "medium"
                      ? "border-amber-200 bg-amber-50 dark:bg-amber-950/20"
                      : "border-green-200 bg-green-50 dark:bg-green-950/20"
                  }`}
                >
                  <span
                    className={`flex-shrink-0 text-xs font-bold mt-0.5 ${
                      f.severity === "high"
                        ? "text-red-600"
                        : f.severity === "medium"
                        ? "text-amber-600"
                        : "text-green-600"
                    }`}
                  >
                    {f.severity === "high" ? (isAr ? "مرتفع" : "HIGH") : f.severity === "medium" ? (isAr ? "متوسط" : "MED") : (isAr ? "منخفض" : "LOW")}
                  </span>
                  <div className="text-sm">
                    <p className="font-medium">{f.label_ar}</p>
                    <p className="text-muted-foreground text-xs mt-0.5">{f.label_en}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {tier && (
            <Card className="p-6 border-[var(--dealix-deep-green)]/30 bg-[var(--dealix-deep-green)]/5">
              <h3 className="font-semibold text-[var(--dealix-deep-green)] mb-2">
                {isAr ? "الخدمة الموصى بها" : "Recommended Service"}
              </h3>
              <p className="text-lg font-bold">{isAr ? tier.name_ar : tier.name_en}</p>
              <p className="text-sm text-muted-foreground mt-1">
                {isAr ? tier.description_ar : tier.description_en}
              </p>
            </Card>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            <Button
              asChild
              className="flex-1 bg-[var(--dealix-deep-green)] hover:bg-[var(--dealix-deep-green)]/90 text-white font-semibold py-3"
            >
              <Link href={`/${locale}/dealix-diagnostic`}>
                {isAr ? "احجز استشارة مجانية 30 دقيقة" : "Book a Free 30-min Strategy Call"}
              </Link>
            </Button>
            <Button asChild variant="outline" className="flex-1 py-3 border-[var(--dealix-deep-green)] text-[var(--dealix-deep-green)]">
              <Link href={`/${locale}/dealix-diagnostic`}>
                {isAr ? "ابدأ بالتشخيص المجاني" : "Start Free Diagnostic"}
              </Link>
            </Button>
          </div>

          <div className="text-center">
            <button
              onClick={() => setStep(1)}
              className="text-xs text-muted-foreground underline"
            >
              {isAr ? "إعادة التقييم من البداية" : "Restart assessment"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
