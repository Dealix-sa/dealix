"use client";

import { useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type StepStatus = "done" | "active" | "pending";

interface SprintStep {
  day: number;
  title_ar: string;
  title_en: string;
  description_ar: string;
  description_en: string;
  status: StepStatus;
}

interface Deliverable {
  label_ar: string;
  label_en: string;
  completed: boolean;
}

interface ProofSection {
  title_ar: string;
  title_en: string;
  status_ar: string;
  status_en: string;
  ready: boolean;
}

interface SprintData {
  client_name: string;
  current_day: number;
  total_days: number;
  steps: SprintStep[];
  deliverables: Deliverable[];
  proof_sections: ProofSection[];
}

// ---------------------------------------------------------------------------
// Static demo data
// ---------------------------------------------------------------------------

const DEMO_SPRINT: SprintData = {
  client_name: "شركة التقنية المتقدمة",
  current_day: 5,
  total_days: 7,
  steps: [
    {
      day: 1,
      title_ar: "جمع البيانات وجواز المصدر",
      title_en: "Data Collection & Source Passport",
      description_ar:
        "تحديد مصادر البيانات وتوثيق جواز المصدر لكل مصدر بيانات مشمول في النطاق.",
      description_en:
        "Identify data sources and document the Source Passport for each in-scope data source.",
      status: "done",
    },
    {
      day: 2,
      title_ar: "تسجيل جودة البيانات",
      title_en: "Data Quality Scoring — DQ Score 0-100",
      description_ar:
        "احتساب درجة DQ لكل مجموعة بيانات وتحديد الفجوات بناءً على معايير الاكتمال والدقة.",
      description_en:
        "Compute DQ score per dataset and flag gaps based on completeness and accuracy criteria.",
      status: "done",
    },
    {
      day: 3,
      title_ar: "تسجيل الحسابات ومطابقة ICP",
      title_en: "Account Scoring & ICP Fit",
      description_ar:
        "تسجيل الحسابات مقابل ملف ICP ودرجة الملاءمة لتحديد أفضل الحسابات للمتابعة.",
      description_en:
        "Score accounts against the ICP profile and fit score to identify the best accounts for follow-up.",
      status: "done",
    },
    {
      day: 4,
      title_ar: "تجميع حزمة المسودة",
      title_en: "Draft Pack Assembly",
      description_ar:
        "تجميع كل نتائج الأيام الثلاثة في مسودة حزمة الأدلة الأولية للمراجعة الداخلية.",
      description_en:
        "Assemble all findings from the first three days into an initial draft evidence pack for internal review.",
      status: "done",
    },
    {
      day: 5,
      title_ar: "مراجعة الحوكمة — APPROVAL_FIRST",
      title_en: "Governance Review — APPROVAL_FIRST",
      description_ar:
        "مراجعة المسودة وفق بروتوكول الحوكمة APPROVAL_FIRST وضمان الامتثال قبل المتابعة.",
      description_en:
        "Review the draft under the APPROVAL_FIRST governance protocol and ensure compliance before proceeding.",
      status: "active",
    },
    {
      day: 6,
      title_ar: "بناء Proof Pack",
      title_en: "Proof Pack Build",
      description_ar:
        "بناء حزمة الإثبات النهائية المكونة من 14 قسماً مع الدرجة والمستوى.",
      description_en:
        "Build the final 14-section Proof Pack with score and tier classification.",
      status: "pending",
    },
    {
      day: 7,
      title_ar: "تسجيل الأصول وعرض الاحتفاظ",
      title_en: "Capital Asset Registration + Retainer Pitch",
      description_ar:
        "تسجيل المخرجات كأصول رأسمالية وتقديم عرض الانتقال إلى خدمة Managed Ops الشهرية.",
      description_en:
        "Register outputs as capital assets and deliver the pitch for transitioning to the monthly Managed Ops retainer.",
      status: "pending",
    },
  ],
  deliverables: [
    {
      label_ar: "جواز مصدر موثّق لكل مصدر بيانات",
      label_en: "Documented Source Passport per data source",
      completed: true,
    },
    {
      label_ar: "تقرير DQ Score مفصّل",
      label_en: "Detailed DQ Score report",
      completed: true,
    },
    {
      label_ar: "قائمة الحسابات المُسجَّلة مع درجة ICP",
      label_en: "Scored account list with ICP fit",
      completed: true,
    },
    {
      label_ar: "مسودة حزمة الأدلة الأولية",
      label_en: "Initial draft evidence pack",
      completed: true,
    },
    {
      label_ar: "سجل قرار الحوكمة",
      label_en: "Governance decision log",
      completed: false,
    },
    {
      label_ar: "حزمة الإثبات النهائية (14 قسماً)",
      label_en: "Final Proof Pack (14 sections)",
      completed: false,
    },
    {
      label_ar: "تسجيل الأصول الرأسمالية",
      label_en: "Capital asset registration",
      completed: false,
    },
    {
      label_ar: "ملخص عرض Managed Ops",
      label_en: "Managed Ops pitch summary",
      completed: false,
    },
  ],
  proof_sections: [
    {
      title_ar: "تدقيق البيانات",
      title_en: "Data Audit",
      status_ar: "مكتمل",
      status_en: "Complete",
      ready: true,
    },
    {
      title_ar: "تحليل الإيرادات",
      title_en: "Revenue Analysis",
      status_ar: "مكتمل",
      status_en: "Complete",
      ready: true,
    },
    {
      title_ar: "سجل الحوكمة",
      title_en: "Governance Log",
      status_ar: "جارٍ",
      status_en: "In Progress",
      ready: false,
    },
    {
      title_ar: "خطة العمل",
      title_en: "Action Plan",
      status_ar: "معلّق",
      status_en: "Pending",
      ready: false,
    },
  ],
};

// ---------------------------------------------------------------------------
// Step status helpers
// ---------------------------------------------------------------------------

function statusBadgeProps(status: StepStatus, isAr: boolean) {
  if (status === "done") {
    return {
      variant: "emerald" as const,
      label: isAr ? "مكتمل" : "Done",
    };
  }
  if (status === "active") {
    return {
      variant: "gold" as const,
      label: isAr ? "نشط" : "Active",
    };
  }
  return {
    variant: "outline" as const,
    label: isAr ? "معلّق" : "Pending",
  };
}

function stepBorderClass(status: StepStatus): string {
  if (status === "done") return "border-emerald-500/40 bg-emerald-500/5";
  if (status === "active")
    return "border-[var(--dealix-gold)]/60 bg-[var(--dealix-gold)]/5";
  return "border-border bg-muted/10";
}

function dayCircleClass(status: StepStatus): string {
  if (status === "done")
    return "bg-emerald-500 text-white";
  if (status === "active")
    return "bg-[var(--dealix-gold)] text-[var(--dealix-navy)]";
  return "bg-muted text-muted-foreground";
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface HeroSectionProps {
  sprint: SprintData;
  isAr: boolean;
}

function HeroSection({ sprint, isAr }: HeroSectionProps) {
  const progressPct = (sprint.current_day / sprint.total_days) * 100;

  return (
    <Card className="p-6 border-[var(--dealix-navy)]/20 bg-gradient-to-br from-[var(--dealix-navy)]/5 to-transparent">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--dealix-navy)]">
            {isAr ? "Revenue Intelligence Sprint" : "Revenue Intelligence Sprint"}
          </h1>
          <p className="text-muted-foreground text-sm mt-1">
            {sprint.client_name}
          </p>
        </div>
        <Badge
          variant="gold"
          className="self-start sm:self-auto text-base px-4 py-2"
        >
          {isAr
            ? `اليوم ${sprint.current_day} من ${sprint.total_days}`
            : `Day ${sprint.current_day} of ${sprint.total_days}`}
        </Badge>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{isAr ? "التقدم الإجمالي" : "Overall progress"}</span>
          <span>{Math.round(progressPct)}%</span>
        </div>
        <Progress value={progressPct} className="h-3" />
      </div>

      <div className="mt-4 flex flex-wrap gap-4 text-sm">
        <div>
          <span className="text-muted-foreground">
            {isAr ? "السعر: " : "Price: "}
          </span>
          <span className="font-semibold text-[var(--dealix-gold)]">
            499 {isAr ? "ر.س" : "SAR"}
          </span>
        </div>
        <div>
          <span className="text-muted-foreground">
            {isAr ? "المدة: " : "Duration: "}
          </span>
          <span className="font-semibold">
            {isAr ? "7 أيام" : "7 days"}
          </span>
        </div>
      </div>
    </Card>
  );
}

interface SprintTimelineProps {
  steps: SprintStep[];
  isAr: boolean;
}

function SprintTimeline({ steps, isAr }: SprintTimelineProps) {
  return (
    <div className="space-y-1">
      <h2 className="text-lg font-bold text-[var(--dealix-navy)] mb-4">
        {isAr ? "جدول السبرينت — 7 أيام" : "7-Day Sprint Timeline"}
      </h2>
      <div className="relative">
        {/* Vertical connector line */}
        <div className="absolute top-0 bottom-0 left-[19px] w-px bg-border rtl:left-auto rtl:right-[19px]" />

        <div className="space-y-3">
          {steps.map((step) => {
            const { variant, label } = statusBadgeProps(step.status, isAr);
            return (
              <div
                key={step.day}
                className={`relative flex gap-4 rounded-xl border p-4 transition-colors ${stepBorderClass(step.status)}`}
              >
                {/* Day circle */}
                <div
                  className={`relative z-10 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full text-sm font-bold ${dayCircleClass(step.status)}`}
                >
                  {step.day}
                </div>

                {/* Content */}
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-start justify-between gap-2">
                    <div>
                      <p className="font-semibold text-sm">
                        {isAr ? step.title_ar : step.title_en}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {isAr ? step.title_en : step.title_ar}
                      </p>
                    </div>
                    <Badge variant={variant}>{label}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                    {isAr ? step.description_ar : step.description_en}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

interface DeliverablesChecklistProps {
  deliverables: Deliverable[];
  isAr: boolean;
}

function DeliverablesChecklist({ deliverables, isAr }: DeliverablesChecklistProps) {
  const completedCount = deliverables.filter((d) => d.completed).length;

  return (
    <Card className="p-6">
      <CardHeader className="p-0 pb-4">
        <CardTitle className="text-[var(--dealix-navy)] flex items-center justify-between">
          <span>{isAr ? "قائمة المخرجات" : "Deliverables Checklist"}</span>
          <Badge variant="outline" className="text-xs font-normal">
            {completedCount}/{deliverables.length}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="space-y-2">
          {deliverables.map((item, i) => (
            <div
              key={i}
              className={`flex items-start gap-3 rounded-lg px-3 py-2.5 ${
                item.completed
                  ? "bg-emerald-500/5 border border-emerald-500/20"
                  : "bg-muted/30 border border-border"
              }`}
            >
              <div
                className={`mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded border text-xs font-bold ${
                  item.completed
                    ? "border-emerald-500 bg-emerald-500 text-white"
                    : "border-muted-foreground/30 bg-background text-transparent"
                }`}
              >
                {item.completed ? "+" : ""}
              </div>
              <div className="min-w-0">
                <p
                  className={`text-sm ${
                    item.completed
                      ? "text-foreground"
                      : "text-muted-foreground"
                  }`}
                >
                  {isAr ? item.label_ar : item.label_en}
                </p>
                <p className="text-xs text-muted-foreground/60 mt-0.5">
                  {isAr ? item.label_en : item.label_ar}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

interface ProofPackPreviewProps {
  sections: ProofSection[];
  isAr: boolean;
}

function ProofPackPreview({ sections, isAr }: ProofPackPreviewProps) {
  return (
    <Card className="p-6 border-[var(--dealix-navy)]/20">
      <CardHeader className="p-0 pb-4">
        <CardTitle className="text-[var(--dealix-navy)]">
          {isAr ? "معاينة Proof Pack" : "Proof Pack Preview"}
        </CardTitle>
        <p className="text-xs text-muted-foreground mt-1">
          {isAr
            ? "الحزمة النهائية تشتمل على 14 قسماً — يظهر هنا ملخص الأقسام الرئيسية"
            : "Final pack contains 14 sections — key sections summary shown here"}
        </p>
      </CardHeader>
      <CardContent className="p-0">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {sections.map((sec, i) => (
            <div
              key={i}
              className={`rounded-xl border p-4 ${
                sec.ready
                  ? "border-emerald-500/30 bg-emerald-500/5"
                  : "border-border bg-muted/10"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-semibold">
                  {isAr ? sec.title_ar : sec.title_en}
                </p>
                <Badge
                  variant={sec.ready ? "emerald" : "outline"}
                  className="text-xs"
                >
                  {isAr ? sec.status_ar : sec.status_en}
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {isAr ? sec.title_en : sec.title_ar}
              </p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

interface UpgradeBannerProps {
  isAr: boolean;
  sprintComplete: boolean;
}

function UpgradeBanner({ isAr, sprintComplete }: UpgradeBannerProps) {
  if (!sprintComplete) return null;

  return (
    <Card className="p-6 border-[var(--dealix-gold)]/40 bg-gradient-to-br from-[var(--dealix-gold)]/10 to-transparent">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <Badge variant="gold" className="mb-2">
            {isAr ? "السبرينت مكتمل" : "Sprint Complete"}
          </Badge>
          <h3 className="text-lg font-bold text-[var(--dealix-navy)]">
            {isAr
              ? "جاهز للانتقال إلى Managed Ops"
              : "Ready for Managed Ops"}
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            {isAr
              ? "استمر في بناء الزخم مع إدارة كاملة شهرية للعمليات وتحسين مستمر للإيراد."
              : "Continue building momentum with full monthly operations management and continuous revenue improvement."}
          </p>
          <p className="text-lg font-bold text-[var(--dealix-gold)] mt-2">
            2,999 {isAr ? "ر.س / شهرياً" : "SAR / mo"}
          </p>
        </div>
        <Button className="bg-[var(--dealix-navy)] hover:bg-[var(--dealix-navy-hover)] text-white shrink-0 px-6 py-3">
          {isAr ? "ابدأ Managed Ops" : "Start Managed Ops"}
        </Button>
      </div>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Main export
// ---------------------------------------------------------------------------

export function SprintPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const sprint = DEMO_SPRINT;
  const sprintComplete = sprint.current_day >= sprint.total_days;

  return (
    <div className="max-w-3xl mx-auto space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <HeroSection sprint={sprint} isAr={isAr} />
      <SprintTimeline steps={sprint.steps} isAr={isAr} />
      <DeliverablesChecklist deliverables={sprint.deliverables} isAr={isAr} />
      <ProofPackPreview sections={sprint.proof_sections} isAr={isAr} />
      <UpgradeBanner isAr={isAr} sprintComplete={sprintComplete} />
    </div>
  );
}
