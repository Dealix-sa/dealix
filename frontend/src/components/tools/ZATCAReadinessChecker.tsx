// from __future__ import annotations
"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ChecklistItem {
  id: string;
  labelAr: string;
  labelEn: string;
  weight: number;
  critical: boolean;
  penaltyExposureSar: number;
}

type ChecklistState = Record<string, boolean | null>;

type ScoreTier = "non_compliant" | "at_risk" | "moderate" | "compliant";

interface TierConfig {
  labelAr: string;
  labelEn: string;
  colorClass: string;
  bgClass: string;
  borderClass: string;
  textClass: string;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const CHECKLIST_ITEMS: ChecklistItem[] = [
  {
    id: "csid",
    labelAr: "شهادة CSID من بوابة ZATCA",
    labelEn: "CSID from ZATCA portal",
    weight: 15,
    critical: true,
    penaltyExposureSar: 10000,
  },
  {
    id: "ubl_xml",
    labelAr: "تنسيق XML وفق معيار UBL 2.1",
    labelEn: "XML UBL 2.1 format",
    weight: 12,
    critical: true,
    penaltyExposureSar: 8000,
  },
  {
    id: "qr_code",
    labelAr: "توليد رمز QR المعتمد",
    labelEn: "QR code generation",
    weight: 10,
    critical: false,
    penaltyExposureSar: 5000,
  },
  {
    id: "digital_stamp",
    labelAr: "الختم الرقمي (Cryptographic Stamp)",
    labelEn: "Digital stamp",
    weight: 12,
    critical: true,
    penaltyExposureSar: 8000,
  },
  {
    id: "fatoora_api",
    labelAr: "التكامل مع Fatoora API",
    labelEn: "Fatoora API integration",
    weight: 12,
    critical: true,
    penaltyExposureSar: 10000,
  },
  {
    id: "realtime_submission",
    labelAr: "الإرسال الآني للفواتير",
    labelEn: "Real-time submission",
    weight: 10,
    critical: false,
    penaltyExposureSar: 5000,
  },
  {
    id: "trn",
    labelAr: "رقم التسجيل الضريبي (TRN) صحيح",
    labelEn: "Correct TRN",
    weight: 8,
    critical: true,
    penaltyExposureSar: 5000,
  },
  {
    id: "invoice_data",
    labelAr: "بيانات الفاتورة مكتملة (كل الحقول الإلزامية)",
    labelEn: "Complete invoice data",
    weight: 8,
    critical: false,
    penaltyExposureSar: 3000,
  },
  {
    id: "rejection_process",
    labelAr: "إجراء معالجة الرفض والإخطارات",
    labelEn: "Rejection process handling",
    weight: 7,
    critical: false,
    penaltyExposureSar: 3000,
  },
  {
    id: "team_training",
    labelAr: "تدريب الفريق على متطلبات ZATCA",
    labelEn: "Team training",
    weight: 6,
    critical: false,
    penaltyExposureSar: 2000,
  },
];

const TIER_CONFIGS: Record<ScoreTier, TierConfig> = {
  non_compliant: {
    labelAr: "غير ممتثل",
    labelEn: "Non-Compliant",
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
  moderate: {
    labelAr: "امتثال جزئي",
    labelEn: "Moderate",
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
  const total = CHECKLIST_ITEMS.reduce((acc, item) => acc + item.weight, 0);
  const earned = CHECKLIST_ITEMS.reduce((acc, item) => {
    return state[item.id] === true ? acc + item.weight : acc;
  }, 0);
  return total > 0 ? Math.round((earned / total) * 100) : 0;
}

function computeTier(score: number): ScoreTier {
  if (score >= 80) return "compliant";
  if (score >= 60) return "moderate";
  if (score >= 40) return "at_risk";
  return "non_compliant";
}

function computePenaltyExposure(state: ChecklistState): number {
  return CHECKLIST_ITEMS.reduce((acc, item) => {
    return state[item.id] !== true ? acc + item.penaltyExposureSar : acc;
  }, 0);
}

function getGaps(state: ChecklistState, isAr: boolean): string[] {
  return CHECKLIST_ITEMS.filter((item) => state[item.id] !== true).map((item) =>
    isAr ? item.labelAr : item.labelEn
  );
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
  const config = TIER_CONFIGS[tier];
  const barColorMap: Record<ScoreTier, string> = {
    non_compliant: "bg-red-500",
    at_risk: "bg-orange-500",
    moderate: "bg-yellow-500",
    compliant: "bg-emerald-500",
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center text-sm">
        <span className={`font-semibold ${config.colorClass}`}>
          {score}/100
        </span>
      </div>
      <div className="h-3 w-full rounded-full bg-muted overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${barColorMap[tier]}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Wizard step (checklist form)
// ---------------------------------------------------------------------------

interface WizardStepProps {
  currentStep: number;
  totalSteps: number;
  item: ChecklistItem;
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

  return (
    <div className="space-y-6">
      {/* Progress indicator */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{isAr ? `السؤال ${currentStep} من ${totalSteps}` : `Question ${currentStep} of ${totalSteps}`}</span>
          <span>{Math.round((currentStep / totalSteps) * 100)}%</span>
        </div>
        <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-[var(--dealix-navy)] transition-all duration-300"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      {/* Question */}
      <div className="space-y-2">
        {item.critical && (
          <span className="inline-block text-xs font-semibold px-2 py-0.5 rounded-full bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300 border border-red-300 dark:border-red-700">
            {isAr ? "عنصر حرج" : "Critical Item"}
          </span>
        )}
        <p className="text-lg font-semibold leading-relaxed">{label}</p>
      </div>

      {/* Answer buttons */}
      <div className="flex gap-4">
        <button
          onClick={() => onSelect(true)}
          className={`flex-1 py-3 rounded-xl border-2 font-semibold text-sm transition-all ${
            value === true
              ? "bg-emerald-500 border-emerald-500 text-white"
              : "border-border hover:border-emerald-400 text-muted-foreground hover:text-foreground"
          }`}
        >
          {isAr ? "نعم، جاهز" : "Yes, done"} &#10003;
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
          className="bg-[var(--dealix-navy)] text-white hover:bg-[var(--dealix-navy-hover)]"
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
  gaps: string[];
  penaltyExposure: number;
  isAr: boolean;
  onRetake: () => void;
  locale: string;
}

function ResultsView({
  score,
  tier,
  gaps,
  penaltyExposure,
  isAr,
  onRetake,
  locale,
}: ResultsViewProps) {
  const config = TIER_CONFIGS[tier];

  const tierDescriptions: Record<ScoreTier, { ar: string; en: string }> = {
    non_compliant: {
      ar: "شركتك في خطر كبير من الغرامات. تحتاج إلى تدخل عاجل قبل موعد التطبيق.",
      en: "Your company faces significant penalty risk. Urgent intervention required before the compliance deadline.",
    },
    at_risk: {
      ar: "هناك ثغرات جوهرية تحتاج معالجة سريعة لتجنب الغرامات والتوقف عن العمل.",
      en: "There are critical gaps that need rapid remediation to avoid penalties and operational disruption.",
    },
    moderate: {
      ar: "تقدم جيد، لكن لا تزال هناك نقاط ناقصة تعرضك للمخاطر التشغيلية.",
      en: "Good progress, but remaining gaps still expose you to operational and compliance risk.",
    },
    compliant: {
      ar: "شركتك في وضع جيد للامتثال. راجع مع محاسبك للتأكد من آخر التفاصيل.",
      en: "Your company is well-positioned for compliance. Verify final details with your accountant.",
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
          <div>
            <span
              className={`inline-block px-4 py-1.5 rounded-full text-sm font-bold border ${config.bgClass} ${config.borderClass} ${config.textClass}`}
            >
              {isAr ? config.labelAr : config.labelEn}
            </span>
          </div>
          <ScoreBar score={score} tier={tier} />
          <p className="text-sm text-muted-foreground max-w-md mx-auto">
            {isAr ? tierDescriptions[tier].ar : tierDescriptions[tier].en}
          </p>
        </div>
      </Card>

      {/* Penalty exposure callout */}
      {penaltyExposure > 0 && (
        <Card className="p-5 border-2 border-red-300 dark:border-red-700 bg-red-50 dark:bg-red-950/30">
          <div className={`${isAr ? "text-right" : "text-left"}`}>
            <p className="text-xs font-semibold uppercase tracking-wide text-red-600 dark:text-red-400 mb-1">
              {isAr ? "التعرض المالي المحتمل للغرامات" : "Estimated Penalty Exposure"}
            </p>
            <p className="text-3xl font-black text-red-700 dark:text-red-300 tabular-nums">
              {isAr
                ? `ريال ${formatSar(penaltyExposure)}`
                : `SAR ${formatSar(penaltyExposure)}`}
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              {isAr
                ? "* تقدير بناءً على العناصر غير المكتملة — راجع محاسبك للتقييم الدقيق"
                : "* Estimate based on incomplete items — consult your accountant for precise assessment"}
            </p>
          </div>
        </Card>
      )}

      {/* Gaps */}
      {gaps.length > 0 && (
        <Card className="p-5">
          <h3 className="font-semibold mb-3 text-sm uppercase tracking-wide text-muted-foreground">
            {isAr ? "الفجوات المحددة" : "Identified Gaps"}
          </h3>
          <ul className="space-y-2">
            {gaps.map((gap, i) => (
              <li key={i} className="flex items-start gap-2 text-sm">
                <span className="mt-0.5 text-red-500 shrink-0">&#10007;</span>
                <span>{gap}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {/* CTA */}
      <Card className="p-6 bg-gradient-to-br from-[var(--dealix-navy)]/5 to-[var(--dealix-gold)]/5 border-[var(--dealix-navy)]/20">
        <h3 className="font-bold text-base mb-2">
          {isAr
            ? "احصل على Sprint جاهزية ZATCA مجاناً"
            : "Get a free ZATCA readiness sprint"}
        </h3>
        <p className="text-sm text-muted-foreground mb-4">
          {isAr
            ? "فريق Dealix يرافقك في كل خطوة: الإعداد التقني، التكامل مع ZATCA، وتدريب الفريق — خلال أسبوع واحد."
            : "Dealix walks you through every step: technical setup, ZATCA integration, and team training — within one week."}
        </p>
        <div className="flex flex-wrap gap-3">
          <Button
            asChild
            className="bg-[var(--dealix-navy)] text-white hover:bg-[var(--dealix-navy-hover)] font-semibold"
          >
            <Link href={`/${locale}/dealix-diagnostic`}>
              {isAr ? "ابدأ التشخيص المجاني" : "Start free diagnostic"}
            </Link>
          </Button>
          <Button variant="outline" onClick={onRetake}>
            {isAr ? "أعد التقييم" : "Retake assessment"}
          </Button>
        </div>
      </Card>

      {/* Share button (UI only) */}
      <div className={`${isAr ? "text-right" : "text-left"}`}>
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

export default function ZATCAReadinessChecker() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [step, setStep] = useState<number>(1);
  const [answers, setAnswers] = useState<ChecklistState>({});
  const [submitted, setSubmitted] = useState<boolean>(false);

  const totalSteps = CHECKLIST_ITEMS.length;
  const currentItem = CHECKLIST_ITEMS[step - 1];
  const currentAnswer = answers[currentItem?.id] ?? null;

  const score = computeScore(answers);
  const tier = computeTier(score);
  const penaltyExposure = computePenaltyExposure(answers);
  const gaps = getGaps(answers, isAr);

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
            <span className="badge-zatca text-xs font-semibold px-2.5 py-1 rounded-full">
              ZATCA Phase 2
            </span>
            <span className="badge-proof text-xs font-semibold px-2.5 py-1 rounded-full">
              {isAr ? "تقييم مجاني" : "Free Assessment"}
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--dealix-navy)] dark:text-foreground">
            {isAr
              ? "مدقق جاهزية ZATCA التفاعلي"
              : "ZATCA Readiness Checker"}
          </h1>
          <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
            {isAr
              ? "أجب على ١٠ أسئلة للحصول على تقييم فوري لمدى امتثالك مع متطلبات الفاتورة الإلكترونية في المرحلة الثانية."
              : "Answer 10 questions for an instant assessment of your Phase 2 e-invoicing compliance readiness."}
          </p>
        </header>

        {/* Live score strip — visible during wizard */}
        {!submitted && (
          <Card className="p-4">
            <div className="flex items-center justify-between gap-4">
              <span className="text-sm text-muted-foreground">
                {isAr ? "الدرجة الحالية" : "Current score"}
              </span>
              <div className="flex-1 max-w-xs">
                <ScoreBar score={score} tier={tier} />
              </div>
              <span className="text-sm font-bold tabular-nums">{score}/100</span>
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
            penaltyExposure={penaltyExposure}
            isAr={isAr}
            onRetake={handleRetake}
            locale={locale}
          />
        )}

        {/* Footer disclaimer */}
        <p className="text-xs text-muted-foreground border border-border/40 rounded-lg p-3 bg-muted/20">
          {isAr
            ? "* هذا تقييم تقديري لأغراض التوعية فقط. لا بيانات شخصية تُرسل أو تُحفظ. استشر محاسبك المعتمد لأي قرارات ضريبية."
            : "* This is an indicative self-assessment for awareness purposes only. No personal data is sent or stored. Consult your certified accountant for tax decisions."}
        </p>
      </div>
    </div>
  );
}
