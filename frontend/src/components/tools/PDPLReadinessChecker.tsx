// from __future__ import annotations
"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PDPLItem {
  id: string;
  labelAr: string;
  labelEn: string;
  descriptionAr: string;
  descriptionEn: string;
  weight: number;
  critical: boolean;
  actionAr: string;
  actionEn: string;
  maxPenaltySar: number;
}

type ChecklistState = Record<string, boolean | null>;

type ScoreTier = "critical" | "at_risk" | "partial" | "compliant";

interface TierConfig {
  labelAr: string;
  labelEn: string;
  colorClass: string;
  bgClass: string;
  borderClass: string;
  textClass: string;
}

// ---------------------------------------------------------------------------
// Constants — 10 PDPL checklist items
// ---------------------------------------------------------------------------

const PDPL_ITEMS: PDPLItem[] = [
  {
    id: "privacy_notice",
    labelAr: "إشعار الخصوصية منشور",
    labelEn: "Privacy notice published",
    descriptionAr: "نشر سياسة خصوصية واضحة تشرح كيف تُجمع البيانات وتُستخدم",
    descriptionEn: "A clear privacy policy published explaining how data is collected and used",
    weight: 12,
    critical: true,
    actionAr: "أنشر سياسة خصوصية متوافقة مع نظام PDPL على موقعك الإلكتروني",
    actionEn: "Publish a PDPL-compliant privacy policy on your website",
    maxPenaltySar: 500000,
  },
  {
    id: "data_inventory",
    labelAr: "سجل معالجة البيانات محدّث",
    labelEn: "Data processing inventory maintained",
    descriptionAr: "سجل شامل بجميع عمليات معالجة البيانات الشخصية داخل المنظمة",
    descriptionEn: "Comprehensive record of all personal data processing activities within the organization",
    weight: 10,
    critical: true,
    actionAr: "أنشئ سجلاً وثائقياً لجميع تدفقات البيانات الشخصية",
    actionEn: "Create a documented record of all personal data flows",
    maxPenaltySar: 1000000,
  },
  {
    id: "dpo",
    labelAr: "تعيين مسؤول حماية البيانات (DPO)",
    labelEn: "DPO appointed or designated",
    descriptionAr: "تعيين شخص مسؤول عن الامتثال لنظام حماية البيانات الشخصية",
    descriptionEn: "Designating a person responsible for personal data protection compliance",
    weight: 10,
    critical: false,
    actionAr: "عيّن مسؤول حماية بيانات داخلياً أو استعن بمزود خارجي",
    actionEn: "Appoint an internal DPO or engage an external provider",
    maxPenaltySar: 500000,
  },
  {
    id: "dsar",
    labelAr: "إجراء تلبية طلبات أصحاب البيانات (DSAR)",
    labelEn: "Data subject request process (DSAR)",
    descriptionAr: "آلية واضحة لتلقي ومعالجة طلبات الوصول والتصحيح والحذف",
    descriptionEn: "Clear mechanism to receive and handle access, rectification, and deletion requests",
    weight: 10,
    critical: true,
    actionAr: "طوّر إجراء رسمي للرد على طلبات أصحاب البيانات خلال المهلة النظامية",
    actionEn: "Develop a formal procedure to respond to data subject requests within the legal timeframe",
    maxPenaltySar: 1000000,
  },
  {
    id: "cross_border",
    labelAr: "ضوابط نقل البيانات عبر الحدود",
    labelEn: "Cross-border transfer controls",
    descriptionAr: "ضمان نقل البيانات الشخصية خارج المملكة وفق الاشتراطات النظامية فقط",
    descriptionEn: "Ensuring personal data is only transferred outside the Kingdom per regulatory requirements",
    weight: 8,
    critical: true,
    actionAr: "حدد وتحقق من جميع عمليات نقل البيانات الدولية وضع ضمانات مناسبة",
    actionEn: "Identify and verify all international data transfers and put appropriate safeguards in place",
    maxPenaltySar: 5000000,
  },
  {
    id: "processor_agreements",
    labelAr: "اتفاقيات معالجة البيانات مع الأطراف الثالثة",
    labelEn: "Third-party processor agreements",
    descriptionAr: "عقود معالجة بيانات مع جميع المزودين الذين يتعاملون مع بيانات شخصية",
    descriptionEn: "Data processing agreements with all vendors that handle personal data",
    weight: 8,
    critical: false,
    actionAr: "أبرم اتفاقيات معالجة بيانات مع جميع الموردين المؤهلين",
    actionEn: "Execute data processing agreements with all qualifying vendors",
    maxPenaltySar: 500000,
  },
  {
    id: "breach_notification",
    labelAr: "إجراء إخطار الاختراق خلال ٧٢ ساعة",
    labelEn: "Breach notification procedure (72-hour)",
    descriptionAr: "إجراء موثق للكشف عن الاختراقات والإخطار بها خلال ٧٢ ساعة",
    descriptionEn: "Documented procedure for detecting breaches and notifying within 72 hours",
    weight: 12,
    critical: true,
    actionAr: "ضع خطة استجابة لحوادث الاختراق تتضمن إجراء الإخطار في ٧٢ ساعة",
    actionEn: "Develop a breach response plan including the 72-hour notification procedure",
    maxPenaltySar: 5000000,
  },
  {
    id: "data_minimization",
    labelAr: "سياسة تقليل البيانات المجمّعة",
    labelEn: "Data minimization policy",
    descriptionAr: "سياسة تضمن جمع البيانات الشخصية الضرورية فقط لأغراض محددة",
    descriptionEn: "Policy ensuring only necessary personal data is collected for defined purposes",
    weight: 10,
    critical: false,
    actionAr: "راجع ووثّق مبررات جمع كل نوع من البيانات الشخصية لديك",
    actionEn: "Review and document justifications for collecting each type of personal data",
    maxPenaltySar: 500000,
  },
  {
    id: "retention_schedule",
    labelAr: "جدول الاحتفاظ والحذف المجدول",
    labelEn: "Retention and deletion schedule",
    descriptionAr: "جداول احتفاظ واضحة وعمليات حذف آمن عند انتهاء مدة الاحتفاظ",
    descriptionEn: "Clear retention schedules and secure deletion processes when retention periods expire",
    weight: 10,
    critical: false,
    actionAr: "حدد مدد الاحتفاظ بكل فئة من البيانات وفعّل آلية الحذف الآمن",
    actionEn: "Define retention periods for each data category and activate secure deletion mechanisms",
    maxPenaltySar: 500000,
  },
  {
    id: "employee_training",
    labelAr: "تدريب الموظفين على نظام PDPL",
    labelEn: "Employee training on PDPL",
    descriptionAr: "برامج تدريبية منتظمة للموظفين على متطلبات حماية البيانات الشخصية",
    descriptionEn: "Regular training programs for employees on personal data protection requirements",
    weight: 10,
    critical: false,
    actionAr: "نفّذ برنامجاً تدريبياً لجميع الموظفين الذين يتعاملون مع بيانات شخصية",
    actionEn: "Implement a training program for all employees handling personal data",
    maxPenaltySar: 250000,
  },
];

const TIER_CONFIGS: Record<ScoreTier, TierConfig> = {
  critical: {
    labelAr: "حرج — تدخل عاجل",
    labelEn: "Critical — Urgent Action",
    colorClass: "text-red-600",
    bgClass: "bg-red-50 dark:bg-red-950/30",
    borderClass: "border-red-300 dark:border-red-700",
    textClass: "text-red-700 dark:text-red-300",
  },
  at_risk: {
    labelAr: "في خطر",
    labelEn: "At Risk",
    colorClass: "text-orange-600",
    bgClass: "bg-orange-50 dark:bg-orange-950/30",
    borderClass: "border-orange-300 dark:border-orange-700",
    textClass: "text-orange-700 dark:text-orange-300",
  },
  partial: {
    labelAr: "امتثال جزئي",
    labelEn: "Partial Compliance",
    colorClass: "text-yellow-600",
    bgClass: "bg-yellow-50 dark:bg-yellow-950/30",
    borderClass: "border-yellow-300 dark:border-yellow-700",
    textClass: "text-yellow-700 dark:text-yellow-300",
  },
  compliant: {
    labelAr: "ممتثل",
    labelEn: "Compliant",
    colorClass: "text-emerald-600",
    bgClass: "bg-emerald-50 dark:bg-emerald-950/30",
    borderClass: "border-emerald-300 dark:border-emerald-700",
    textClass: "text-emerald-700 dark:text-emerald-300",
  },
};

// ---------------------------------------------------------------------------
// Pure helpers
// ---------------------------------------------------------------------------

function computeScore(state: ChecklistState): number {
  const total = PDPL_ITEMS.reduce((acc, item) => acc + item.weight, 0);
  const earned = PDPL_ITEMS.reduce((acc, item) => {
    return state[item.id] === true ? acc + item.weight : acc;
  }, 0);
  return total > 0 ? Math.round((earned / total) * 100) : 0;
}

function computeTier(score: number): ScoreTier {
  if (score >= 80) return "compliant";
  if (score >= 60) return "partial";
  if (score >= 40) return "at_risk";
  return "critical";
}

function computeMaxViolationCost(state: ChecklistState): number {
  return PDPL_ITEMS.reduce((acc, item) => {
    return state[item.id] !== true ? acc + item.maxPenaltySar : acc;
  }, 0);
}

interface Gap {
  labelAr: string;
  labelEn: string;
  actionAr: string;
  actionEn: string;
  critical: boolean;
}

function getGaps(state: ChecklistState): Gap[] {
  return PDPL_ITEMS.filter((item) => state[item.id] !== true).map((item) => ({
    labelAr: item.labelAr,
    labelEn: item.labelEn,
    actionAr: item.actionAr,
    actionEn: item.actionEn,
    critical: item.critical,
  }));
}

function formatSar(value: number): string {
  return new Intl.NumberFormat("en-SA", {
    style: "decimal",
    maximumFractionDigits: 0,
  }).format(value);
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface ScoreBarProps {
  score: number;
  tier: ScoreTier;
}

function ScoreBar({ score, tier }: ScoreBarProps) {
  const barColorMap: Record<ScoreTier, string> = {
    critical: "bg-red-500",
    at_risk: "bg-orange-500",
    partial: "bg-yellow-500",
    compliant: "bg-emerald-500",
  };
  return (
    <div className="h-3 w-full rounded-full bg-muted overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-500 ${barColorMap[tier]}`}
        style={{ width: `${score}%` }}
      />
    </div>
  );
}

interface WizardStepProps {
  currentStep: number;
  totalSteps: number;
  item: PDPLItem;
  value: boolean | null;
  isAr: boolean;
  onSelect: (val: boolean) => void;
  onNext: () => void;
  onPrev: () => void;
}

function WizardStep({
  currentStep,
  totalSteps,
  item,
  value,
  isAr,
  onSelect,
  onNext,
  onPrev,
}: WizardStepProps) {
  const label = isAr ? item.labelAr : item.labelEn;
  const description = isAr ? item.descriptionAr : item.descriptionEn;

  return (
    <div className="space-y-6">
      {/* Progress */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>
            {isAr
              ? `${currentStep} من ${totalSteps}`
              : `${currentStep} of ${totalSteps}`}
          </span>
          <span>{Math.round((currentStep / totalSteps) * 100)}%</span>
        </div>
        <div className="h-1.5 w-full rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-blue-600 transition-all duration-300"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      {/* Question */}
      <div className="space-y-2">
        {item.critical && (
          <span className="inline-block text-xs font-semibold px-2 py-0.5 rounded-full bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300 border border-red-300 dark:border-red-700">
            {isAr ? "متطلب حرج" : "Critical Requirement"}
          </span>
        )}
        <p className="text-lg font-semibold leading-relaxed">{label}</p>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>

      {/* Answers */}
      <div className="flex gap-4">
        <button
          onClick={() => onSelect(true)}
          className={`flex-1 py-3 rounded-xl border-2 font-semibold text-sm transition-all ${
            value === true
              ? "bg-emerald-500 border-emerald-500 text-white"
              : "border-border hover:border-emerald-400 text-muted-foreground hover:text-foreground"
          }`}
        >
          {isAr ? "نعم، مكتمل" : "Yes, completed"} &#10003;
        </button>
        <button
          onClick={() => onSelect(false)}
          className={`flex-1 py-3 rounded-xl border-2 font-semibold text-sm transition-all ${
            value === false
              ? "bg-red-100 border-red-400 text-red-700 dark:bg-red-950 dark:text-red-300"
              : "border-border hover:border-red-300 text-muted-foreground hover:text-foreground"
          }`}
        >
          {isAr ? "لا، لم يكتمل" : "No, not yet"} &#10007;
        </button>
      </div>

      {/* Navigation */}
      <div className="flex justify-between gap-3 pt-2">
        {currentStep > 1 ? (
          <Button variant="outline" onClick={onPrev} size="sm">
            {isAr ? "السابق" : "Previous"}
          </Button>
        ) : (
          <div />
        )}
        <Button
          onClick={onNext}
          disabled={value === null}
          size="sm"
          className="bg-blue-700 text-white hover:bg-blue-800"
        >
          {currentStep === totalSteps
            ? (isAr ? "عرض النتائج" : "Show Results")
            : (isAr ? "التالي" : "Next")}
        </Button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Results view
// ---------------------------------------------------------------------------

interface ResultsViewProps {
  score: number;
  tier: ScoreTier;
  gaps: Gap[];
  maxViolationCost: number;
  isAr: boolean;
  onRetake: () => void;
  locale: string;
}

function ResultsView({
  score,
  tier,
  gaps,
  maxViolationCost,
  isAr,
  onRetake,
  locale,
}: ResultsViewProps) {
  const config = TIER_CONFIGS[tier];

  const tierMessages: Record<ScoreTier, { ar: string; en: string }> = {
    critical: {
      ar: "شركتك تواجه مخاطر قانونية جسيمة وفق نظام PDPL. يجب اتخاذ إجراءات فورية قبل أن تصل الجهات الرقابية.",
      en: "Your organization faces significant legal risk under PDPL. Immediate action is required before regulators reach out.",
    },
    at_risk: {
      ar: "هناك ثغرات مهمة في امتثالك لنظام PDPL تعرضك للعقوبات المالية والإشعارات التنظيمية.",
      en: "There are significant PDPL compliance gaps that expose you to financial penalties and regulatory notices.",
    },
    partial: {
      ar: "تقدم ملحوظ في الامتثال، لكن لا تزال بعض المتطلبات الأساسية غير مكتملة.",
      en: "Noticeable compliance progress, but some key requirements remain incomplete.",
    },
    compliant: {
      ar: "شركتك في وضع امتثال جيد لنظام PDPL. استمر في مراجعة الممارسات بشكل دوري.",
      en: "Your organization is in a good PDPL compliance position. Continue periodic practice reviews.",
    },
  };

  return (
    <div className="space-y-6">
      {/* Score card */}
      <Card className={`p-8 ${config.bgClass} ${config.borderClass} border-2`}>
        <div className="text-center space-y-4">
          <p className="text-6xl font-black tabular-nums">
            {score}
            <span className="text-2xl font-normal text-muted-foreground">/100</span>
          </p>
          <span
            className={`inline-block px-4 py-1.5 rounded-full text-sm font-bold border ${config.bgClass} ${config.borderClass} ${config.textClass}`}
          >
            {isAr ? config.labelAr : config.labelEn}
          </span>
          <div className="max-w-xs mx-auto">
            <ScoreBar score={score} tier={tier} />
          </div>
          <p className="text-sm text-muted-foreground max-w-md mx-auto">
            {isAr ? tierMessages[tier].ar : tierMessages[tier].en}
          </p>
        </div>
      </Card>

      {/* Violation cost callout */}
      {maxViolationCost > 0 && (
        <Card className="p-5 border-2 border-red-300 dark:border-red-700 bg-red-50 dark:bg-red-950/30">
          <div className={isAr ? "text-right" : "text-left"}>
            <p className="text-xs font-semibold uppercase tracking-wide text-red-600 dark:text-red-400 mb-1">
              {isAr
                ? "كلفة المخالفة المحتملة (المادة ٣٥)"
                : "Potential Violation Cost (Article 35)"}
            </p>
            <p className="text-3xl font-black text-red-700 dark:text-red-300 tabular-nums">
              {isAr
                ? `ريال ${formatSar(maxViolationCost)}`
                : `SAR ${formatSar(maxViolationCost)}`}
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              {isAr
                ? "* تقدير تراكمي للغرامات القصوى — الحد الأقصى للمادة ٣٥ يصل إلى ٥ مليون ريال لكل مخالفة"
                : "* Cumulative estimate of maximum fines — Article 35 caps at SAR 5M per violation"}
            </p>
          </div>
        </Card>
      )}

      {/* Gaps with recommended actions */}
      {gaps.length > 0 && (
        <Card className="p-5">
          <h3 className="font-semibold mb-4 text-sm uppercase tracking-wide text-muted-foreground">
            {isAr ? "الفجوات والإجراءات الموصى بها" : "Gaps and Recommended Actions"}
          </h3>
          <ul className="space-y-4">
            {gaps.map((gap, i) => (
              <li key={i} className="space-y-1">
                <div className="flex items-start gap-2">
                  {gap.critical ? (
                    <span className="mt-0.5 text-red-500 shrink-0 font-bold">!</span>
                  ) : (
                    <span className="mt-0.5 text-orange-400 shrink-0">&#10007;</span>
                  )}
                  <div>
                    <p className="text-sm font-semibold">
                      {isAr ? gap.labelAr : gap.labelEn}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {isAr
                        ? `الإجراء الموصى به: ${gap.actionAr}`
                        : `Recommended action: ${gap.actionEn}`}
                    </p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {/* CTA */}
      <Card className="p-6 border border-blue-200 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-950/20">
        <h3 className="font-bold text-base mb-2">
          {isAr
            ? "احجز Sprint جاهزية PDPL مجاناً"
            : "Book a free PDPL readiness sprint"}
        </h3>
        <p className="text-sm text-muted-foreground mb-4">
          {isAr
            ? "فريق Dealix يراجع وضعك الحالي ويساعدك على سد الفجوات تدريجياً — قبل وصول الجهات الرقابية."
            : "Dealix reviews your current posture and helps you close gaps incrementally — before regulators reach out."}
        </p>
        <div className="flex flex-wrap gap-3">
          <Button
            asChild
            className="bg-blue-700 hover:bg-blue-800 text-white font-semibold"
          >
            <Link href={`/${locale}/dealix-diagnostic`}>
              {isAr ? "احجز الجلسة التشخيصية" : "Book diagnostic session"}
            </Link>
          </Button>
          <Button variant="outline" onClick={onRetake}>
            {isAr ? "أعد التقييم" : "Retake assessment"}
          </Button>
        </div>
      </Card>

      {/* Share */}
      <div className={isAr ? "text-right" : "text-left"}>
        <button
          onClick={() => {
            /* share UI placeholder */
          }}
          className="text-sm text-muted-foreground hover:text-foreground underline underline-offset-2 transition-colors"
        >
          {isAr ? "مشاركة النتائج" : "Share results"}
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function PDPLReadinessChecker() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [step, setStep] = useState<number>(1);
  const [answers, setAnswers] = useState<ChecklistState>({});
  const [submitted, setSubmitted] = useState<boolean>(false);

  const totalSteps = PDPL_ITEMS.length;
  const currentItem = PDPL_ITEMS[step - 1];
  const currentAnswer = answers[currentItem?.id] ?? null;

  const score = computeScore(answers);
  const tier = computeTier(score);
  const maxViolationCost = computeMaxViolationCost(answers);
  const gaps = getGaps(answers);

  function handleSelect(val: boolean) {
    setAnswers((prev) => ({ ...prev, [currentItem.id]: val }));
  }

  function handleNext() {
    if (step < totalSteps) {
      setStep((s) => s + 1);
    } else {
      setSubmitted(true);
    }
  }

  function handlePrev() {
    if (step > 1) setStep((s) => s - 1);
  }

  function handleRetake() {
    setAnswers({});
    setStep(1);
    setSubmitted(false);
  }

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-8">
        {/* Header */}
        <header className={isAr ? "text-right" : "text-left"}>
          <div className="flex gap-2 mb-3 flex-wrap">
            <span className="badge-pdpl text-xs font-semibold px-2.5 py-1 rounded-full">
              PDPL
            </span>
            <span className="badge-proof text-xs font-semibold px-2.5 py-1 rounded-full">
              {isAr ? "تقييم مجاني" : "Free Assessment"}
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--dealix-navy)] dark:text-foreground">
            {isAr
              ? "مدقق جاهزية نظام حماية البيانات الشخصية (PDPL)"
              : "PDPL Readiness Checker"}
          </h1>
          <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
            {isAr
              ? "تقييم تفاعلي في ١٠ خطوات لقياس مدى التزام شركتك بنظام حماية البيانات الشخصية السعودي."
              : "A 10-step interactive assessment to measure your organization's compliance with Saudi PDPL."}
          </p>
        </header>

        {/* Live score strip */}
        {!submitted && (
          <Card className="p-4">
            <div className="flex items-center justify-between gap-4">
              <span className="text-sm text-muted-foreground shrink-0">
                {isAr ? "الدرجة الحالية" : "Current score"}
              </span>
              <div className="flex-1 max-w-xs">
                <ScoreBar score={score} tier={tier} />
              </div>
              <span className="text-sm font-bold tabular-nums shrink-0">
                {score}/100
              </span>
            </div>
          </Card>
        )}

        {/* Wizard / Results */}
        {!submitted ? (
          <Card className="p-8">
            <WizardStep
              currentStep={step}
              totalSteps={totalSteps}
              item={currentItem}
              value={currentAnswer}
              isAr={isAr}
              onSelect={handleSelect}
              onNext={handleNext}
              onPrev={handlePrev}
            />
          </Card>
        ) : (
          <ResultsView
            score={score}
            tier={tier}
            gaps={gaps}
            maxViolationCost={maxViolationCost}
            isAr={isAr}
            onRetake={handleRetake}
            locale={locale}
          />
        )}

        {/* Footer */}
        <p className="text-xs text-muted-foreground border border-border/40 rounded-lg p-3 bg-muted/20">
          {isAr
            ? "* هذا تقييم تقديري لأغراض التوعية فقط. لا بيانات شخصية تُرسل أو تُحفظ. استشر مستشارك القانوني للتقييم الرسمي."
            : "* This is an indicative self-assessment for awareness purposes only. No personal data is sent or stored. Consult your legal counsel for a formal assessment."}
        </p>
      </div>
    </div>
  );
}
