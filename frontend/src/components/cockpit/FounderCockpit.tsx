"use client";

import { type FC } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type Severity = "critical" | "high" | "medium";
type OnboardingStatus = "active" | "blocked";

interface KPICard {
  nameAr: string;
  nameEn: string;
  value: string;
  trendUp: boolean;
  trendPct: string;
  progress: number;
  targetLabel: string;
  accentColor: string;
}

interface Alert {
  id: string;
  severity: Severity;
  clientId: string;
  companyAr: string;
  companyEn: string;
  issueAr: string;
  issueEn: string;
}

interface PendingApproval {
  id: string;
  typeAr: string;
  typeEn: string;
  companyAr: string;
  companyEn: string;
  valueSar: number;
  tierAr: string;
  tierEn: string;
}

interface PipelineStat {
  labelAr: string;
  labelEn: string;
  value: string;
  accent: string;
}

interface ComplianceStat {
  labelAr: string;
  labelEn: string;
  value: string;
  sub?: string;
  accent: string;
}

interface OnboardingItem {
  id: string;
  companyAr: string;
  companyEn: string;
  tierAr: string;
  tierEn: string;
  step: number;
  totalSteps: number;
  progress: number;
  status: OnboardingStatus;
}

// ---------------------------------------------------------------------------
// Static data
// ---------------------------------------------------------------------------

const KPI_CARDS: KPICard[] = [
  {
    nameAr: "الإيراد الشهري المتكرر",
    nameEn: "MRR",
    value: "42,800 ر.س",
    trendUp: true,
    trendPct: "+6.2%",
    progress: 85.6,
    targetLabel: "50,000 ر.س",
    accentColor: "bg-emerald-500",
  },
  {
    nameAr: "العملاء النشطون",
    nameEn: "Active Clients",
    value: "12",
    trendUp: true,
    trendPct: "+2",
    progress: 60,
    targetLabel: "20 عميل",
    accentColor: "bg-blue-500",
  },
  {
    nameAr: "متوسط مؤشر الصحة",
    nameEn: "Avg Health Score",
    value: "67.3",
    trendUp: false,
    trendPct: "-1.4",
    progress: 89.7,
    targetLabel: "75 نقطة",
    accentColor: "bg-amber-500",
  },
  {
    nameAr: "معدل الإيراد الصافي",
    nameEn: "NRR",
    value: "108%",
    trendUp: true,
    trendPct: "+3%",
    progress: 93.9,
    targetLabel: "115%",
    accentColor: "bg-indigo-500",
  },
  {
    nameAr: "قيمة المسار التجاري",
    nameEn: "Pipeline Value",
    value: "94,200 ر.س",
    trendUp: true,
    trendPct: "+12.1%",
    progress: 47.1,
    targetLabel: "200,000 ر.س",
    accentColor: "bg-violet-500",
  },
  {
    nameAr: "موافقات معلّقة",
    nameEn: "Pending Approvals",
    value: "2",
    trendUp: false,
    trendPct: "none",
    progress: 0,
    targetLabel: "الهدف: صفر",
    accentColor: "bg-red-500",
  },
];

const ALERTS: Alert[] = [
  {
    id: "ALT-001",
    severity: "critical",
    clientId: "CLT-003",
    companyAr: "مجموعة الريادة للتجارة",
    companyEn: "Al Riyadah Trading Group",
    issueAr: "مؤشر الصحة أقل من 35 — يتطلب جلسة طارئة فورية",
    issueEn: "Health score < 35 — emergency session required",
  },
  {
    id: "ALT-002",
    severity: "high",
    clientId: "CLT-007",
    companyAr: "الوفاء للخدمات المالية",
    companyEn: "Al Wafa Financial Services",
    issueAr: "التجديد خلال 21 يوماً — حزمة الإثبات لم تُرسل بعد",
    issueEn: "Renewal in 21 days — Proof Pack not sent",
  },
  {
    id: "ALT-003",
    severity: "medium",
    clientId: "CLT-011",
    companyAr: "تمكين للرعاية الصحية",
    companyEn: "Tamkeen Health",
    issueAr: "انخفض مؤشر زاتكا 12 نقطة هذا الأسبوع",
    issueEn: "ZATCA score dropped 12 points this week",
  },
];

const PENDING_APPROVALS: PendingApproval[] = [
  {
    id: "APV-001",
    typeAr: "عرض سعر",
    typeEn: "Proposal",
    companyAr: "شركة المنفعة للتجارة",
    companyEn: "Al Manfaa Trading",
    valueSar: 14999,
    tierAr: "العمليات المُدارة",
    tierEn: "Managed Ops",
  },
  {
    id: "APV-002",
    typeAr: "ترقية",
    typeEn: "Upgrade",
    companyAr: "الوافي للخدمات المالية",
    companyEn: "Al Wafi Financial",
    valueSar: 4999,
    tierAr: "المستوى المؤسسي",
    tierEn: "Enterprise",
  },
];

const PIPELINE_STATS: PipelineStat[] = [
  {
    labelAr: "إجمالي الصفقات",
    labelEn: "Total deals in pipeline",
    value: "18",
    accent: "text-blue-700",
  },
  {
    labelAr: "المسار الموزون",
    labelEn: "Weighted pipeline",
    value: "94,200 ر.س",
    accent: "text-emerald-700",
  },
  {
    labelAr: "صفقات متوقفة",
    labelEn: "Stalled deals (>7 days)",
    value: "2",
    accent: "text-orange-700",
  },
];

const COMPLIANCE_STATS: ComplianceStat[] = [
  {
    labelAr: "ملتزمون بزاتكا",
    labelEn: "ZATCA compliant",
    value: "9/12",
    sub: "75% من العملاء",
    accent: "text-emerald-700",
  },
  {
    labelAr: "متوافقون مع PDPL",
    labelEn: "PDPL aligned",
    value: "8/12",
    sub: "67% من العملاء",
    accent: "text-blue-700",
  },
  {
    labelAr: "موجة زاتكا القادمة",
    labelEn: "Next ZATCA wave",
    value: "الموجة 8",
    sub: "أغسطس 2026",
    accent: "text-violet-700",
  },
  {
    labelAr: "متوسط درجة زاتكا",
    labelEn: "Avg ZATCA score",
    value: "72/100",
    sub: "من 100 نقطة",
    accent: "text-amber-700",
  },
];

const ONBOARDINGS: OnboardingItem[] = [
  {
    id: "ONB-001",
    companyAr: "شركة المنفعة للتقنية",
    companyEn: "Al Manfaa Technology",
    tierAr: "سبرينت",
    tierEn: "Sprint",
    step: 6,
    totalSteps: 12,
    progress: 50,
    status: "active",
  },
  {
    id: "ONB-002",
    companyAr: "صفا للخدمات اللوجستية",
    companyEn: "Safa Logistics",
    tierAr: "العمليات المُدارة",
    tierEn: "Managed Ops",
    step: 4,
    totalSteps: 12,
    progress: 33,
    status: "blocked",
  },
  {
    id: "ONB-003",
    companyAr: "تمكين للرعاية الصحية",
    companyEn: "Tamkeen Health",
    tierAr: "حزمة البيانات",
    tierEn: "Data Pack",
    step: 9,
    totalSteps: 12,
    progress: 75,
    status: "active",
  },
];

// ---------------------------------------------------------------------------
// Severity display config
// ---------------------------------------------------------------------------

const SEVERITY_CONFIG: Record<
  Severity,
  {
    badgeBg: string;
    badgeText: string;
    labelAr: string;
    labelEn: string;
    dotColor: string;
    cardBg: string;
    cardBorder: string;
  }
> = {
  critical: {
    badgeBg: "bg-red-100",
    badgeText: "text-red-700",
    labelAr: "حرج",
    labelEn: "Critical",
    dotColor: "bg-red-500",
    cardBg: "bg-red-50",
    cardBorder: "border-red-200",
  },
  high: {
    badgeBg: "bg-orange-100",
    badgeText: "text-orange-700",
    labelAr: "عالي",
    labelEn: "High",
    dotColor: "bg-orange-500",
    cardBg: "bg-orange-50",
    cardBorder: "border-orange-200",
  },
  medium: {
    badgeBg: "bg-yellow-100",
    badgeText: "text-yellow-700",
    labelAr: "متوسط",
    labelEn: "Medium",
    dotColor: "bg-yellow-500",
    cardBg: "bg-yellow-50",
    cardBorder: "border-yellow-200",
  },
};

// ---------------------------------------------------------------------------
// Shared sub-components
// ---------------------------------------------------------------------------

function SectionHeading({ ar, en }: { ar: string; en: string }) {
  return (
    <div className="mb-4">
      <h2 className="text-xl font-bold text-gray-900">{ar}</h2>
      <p className="text-xs text-gray-400 mt-0.5">{en}</p>
    </div>
  );
}

function TrendIndicator({ up, pct }: { up: boolean; pct: string }) {
  if (pct === "none") {
    return <span className="text-sm text-gray-300">—</span>;
  }
  return (
    <span
      className={`inline-flex items-center gap-0.5 text-sm font-semibold ${
        up ? "text-emerald-600" : "text-red-500"
      }`}
    >
      <span aria-hidden="true">{up ? "↑" : "↓"}</span>
      <span>{pct}</span>
    </span>
  );
}

function LinearProgress({
  progress,
  colorClass,
}: {
  progress: number;
  colorClass: string;
}) {
  const capped = Math.min(100, Math.max(0, progress));
  return (
    <div className="w-full bg-gray-100 rounded-full h-1.5 mt-2">
      <div
        className={`h-1.5 rounded-full transition-all duration-300 ${colorClass}`}
        style={{ width: `${capped}%` }}
        role="progressbar"
        aria-valuenow={capped}
        aria-valuemin={0}
        aria-valuemax={100}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// KPI Card
// ---------------------------------------------------------------------------

function KPICardItem({ card }: { card: KPICard }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 flex flex-col gap-2 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="text-base font-bold text-gray-900 leading-snug">{card.nameAr}</p>
          <p className="text-xs text-gray-400 mt-0.5 font-body">{card.nameEn}</p>
        </div>
        <TrendIndicator up={card.trendUp} pct={card.trendPct} />
      </div>
      <p className="text-3xl font-extrabold text-gray-900 tracking-tight">
        {card.value}
      </p>
      <LinearProgress progress={card.progress} colorClass={card.accentColor} />
      <div className="flex items-center justify-between mt-0.5">
        <span className="text-xs text-gray-400 font-body">
          {card.progress > 0 ? `${card.progress}%` : "—"}
        </span>
        <span className="text-xs text-gray-500">{card.targetLabel}</span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Alert Card
// ---------------------------------------------------------------------------

function AlertCardItem({ alert }: { alert: Alert }) {
  const cfg = SEVERITY_CONFIG[alert.severity];
  return (
    <div
      className={`rounded-xl border p-4 flex items-start justify-between gap-3 ${cfg.cardBg} ${cfg.cardBorder}`}
    >
      <div className="flex items-start gap-3 min-w-0 flex-1">
        <span
          className={`mt-2 flex-shrink-0 w-2 h-2 rounded-full ${cfg.dotColor}`}
          aria-hidden="true"
        />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2 mb-1.5">
            <span
              className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${cfg.badgeBg} ${cfg.badgeText}`}
            >
              {cfg.labelAr} | {cfg.labelEn}
            </span>
            <span className="text-xs text-gray-500 font-mono">{alert.clientId}</span>
          </div>
          <p className="text-sm font-bold text-gray-900">{alert.companyAr}</p>
          <p className="text-xs text-gray-500 font-body">{alert.companyEn}</p>
          <p className="text-sm text-gray-700 mt-1">{alert.issueAr}</p>
          <p className="text-xs text-gray-400 font-body">{alert.issueEn}</p>
        </div>
      </div>
      <button
        type="button"
        className="flex-shrink-0 text-xs font-semibold px-3 py-1.5 rounded-lg bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-colors whitespace-nowrap shadow-sm"
      >
        عرض | View
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Approval Card
// ---------------------------------------------------------------------------

function ApprovalCardItem({ item }: { item: PendingApproval }) {
  return (
    <div className="rounded-xl border border-blue-200 bg-blue-50 p-4 flex items-start justify-between gap-3">
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2 mb-1.5">
          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-700">
            {item.typeAr} | {item.typeEn}
          </span>
          <span className="text-xs text-gray-500 font-mono">{item.id}</span>
        </div>
        <p className="text-sm font-bold text-gray-900">{item.companyAr}</p>
        <p className="text-xs text-gray-500 font-body">{item.companyEn}</p>
        <div className="flex flex-wrap items-center gap-3 mt-2">
          <span className="text-lg font-extrabold text-blue-700">
            {item.valueSar.toLocaleString("ar-SA")} ر.س
          </span>
          <span className="text-xs text-gray-600">{item.tierAr}</span>
          <span className="text-xs text-gray-400 font-body">({item.tierEn})</span>
        </div>
      </div>
      <button
        type="button"
        className="flex-shrink-0 text-xs font-semibold px-3 py-1.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors whitespace-nowrap shadow-sm"
      >
        موافقة | Approve
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Onboarding Card
// ---------------------------------------------------------------------------

function OnboardingCardItem({ item }: { item: OnboardingItem }) {
  const isBlocked = item.status === "blocked";
  return (
    <div
      className={`rounded-xl border p-4 flex flex-col gap-2 shadow-sm ${
        isBlocked
          ? "border-red-200 bg-red-50"
          : "border-gray-100 bg-white hover:shadow-md transition-shadow"
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <span className="text-xs text-gray-400 font-mono">{item.id}</span>
            {isBlocked && (
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-700">
                متوقف | BLOCKED
              </span>
            )}
          </div>
          <p className="text-sm font-bold text-gray-900">{item.companyAr}</p>
          <p className="text-xs text-gray-400 font-body">{item.companyEn}</p>
        </div>
        <div className="text-right flex-shrink-0">
          <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
            {item.tierAr}
          </span>
          <p className="text-xs text-gray-400 font-body mt-0.5">{item.tierEn}</p>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs text-gray-500 mt-1">
        <span>
          الخطوة {item.step} من {item.totalSteps}
        </span>
        <span className="font-mono font-bold">{item.progress}%</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-300 ${
            isBlocked ? "bg-red-400" : "bg-emerald-500"
          }`}
          style={{ width: `${item.progress}%` }}
          role="progressbar"
          aria-valuenow={item.progress}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Root component
// ---------------------------------------------------------------------------

const FounderCockpit: FC = () => {
  return (
    <div
      className="max-w-7xl mx-auto px-4 py-6 space-y-8"
      dir="rtl"
      lang="ar"
    >
      {/* ------------------------------------------------------------------ */}
      {/* Row 1: Status Banner                                                */}
      {/* ------------------------------------------------------------------ */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 flex flex-wrap items-center justify-between gap-5">
        <div>
          <p className="text-xs text-gray-400 mb-1" dir="ltr">
            اليوم | Today — الأحد 31 مايو 2026
          </p>
          <div className="flex flex-wrap items-baseline gap-3">
            <h1 className="text-2xl font-extrabold text-gray-900">
              لوحة تحكم المؤسس
            </h1>
            <span className="text-sm font-medium text-gray-400">Founder Cockpit</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-5">
          <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-orange-100 border border-orange-200 text-orange-700 font-semibold text-sm">
            <span className="w-2 h-2 rounded-full bg-orange-500 flex-shrink-0" aria-hidden="true" />
            يحتاج انتباهاً | Needs Attention
          </span>

          <div className="flex items-center gap-5">
            <div className="text-center">
              <p className="text-2xl font-extrabold text-gray-900 leading-none tabular-nums">
                42,800
              </p>
              <p className="text-xs text-gray-400 mt-0.5">MRR (ر.س)</p>
            </div>
            <div className="w-px h-10 bg-gray-200" aria-hidden="true" />
            <div className="text-center">
              <p className="text-2xl font-extrabold text-gray-900 leading-none tabular-nums">
                12
              </p>
              <p className="text-xs text-gray-400 mt-0.5">عميل نشط</p>
            </div>
            <div className="w-px h-10 bg-gray-200" aria-hidden="true" />
            <div className="text-center">
              <p className="text-2xl font-extrabold text-red-600 leading-none tabular-nums">
                2
              </p>
              <p className="text-xs text-gray-400 mt-0.5">تنبيه حرج</p>
            </div>
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------------ */}
      {/* Row 2: KPI Grid                                                     */}
      {/* ------------------------------------------------------------------ */}
      <section aria-labelledby="kpi-heading">
        <SectionHeading ar="مؤشرات الأداء الرئيسية" en="Key Performance Indicators" />
        <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
          {KPI_CARDS.map((card) => (
            <KPICardItem key={card.nameEn} card={card} />
          ))}
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Row 3: Alerts + Pending Approvals (two-column)                     */}
      {/* ------------------------------------------------------------------ */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <section aria-labelledby="alerts-heading">
          <SectionHeading ar="التنبيهات النشطة" en="Active Alerts" />
          <div className="space-y-3">
            {ALERTS.map((alert) => (
              <AlertCardItem key={alert.id} alert={alert} />
            ))}
          </div>
        </section>

        <section aria-labelledby="approvals-heading">
          <SectionHeading ar="الموافقات المعلّقة" en="Pending Approvals" />
          <div className="space-y-3">
            {PENDING_APPROVALS.map((item) => (
              <ApprovalCardItem key={item.id} item={item} />
            ))}
          </div>
        </section>
      </div>

      {/* ------------------------------------------------------------------ */}
      {/* Row 4: Pipeline + Compliance strip                                  */}
      {/* ------------------------------------------------------------------ */}
      <section aria-labelledby="pipeline-compliance-heading">
        <SectionHeading ar="المسار التجاري والامتثال" en="Pipeline & Compliance" />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pipeline summary */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <p className="text-base font-bold text-gray-800 mb-4">
              ملخص المسار التجاري
            </p>
            <div className="grid grid-cols-3 gap-3">
              {PIPELINE_STATS.map((stat) => (
                <div
                  key={stat.labelEn}
                  className="rounded-xl bg-gray-50 border border-gray-100 p-4 text-center"
                >
                  <p className={`text-3xl font-extrabold tabular-nums ${stat.accent}`}>
                    {stat.value}
                  </p>
                  <p className="text-xs font-bold text-gray-700 mt-1 leading-snug">
                    {stat.labelAr}
                  </p>
                  <p className="text-xs text-gray-400 leading-snug">{stat.labelEn}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Compliance summary */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <p className="text-base font-bold text-gray-800 mb-4">
              ملخص الامتثال التنظيمي
            </p>
            <div className="grid grid-cols-2 gap-3">
              {COMPLIANCE_STATS.map((stat) => (
                <div
                  key={stat.labelEn}
                  className="rounded-xl bg-gray-50 border border-gray-100 p-4"
                >
                  <p className={`text-2xl font-extrabold tabular-nums ${stat.accent}`}>
                    {stat.value}
                  </p>
                  {stat.sub !== undefined && (
                    <p className="text-xs text-gray-400 mt-0.5">{stat.sub}</p>
                  )}
                  <p className="text-xs font-bold text-gray-700 mt-1 leading-snug">
                    {stat.labelAr}
                  </p>
                  <p className="text-xs text-gray-400 leading-snug">{stat.labelEn}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Row 5: Active Onboardings                                           */}
      {/* ------------------------------------------------------------------ */}
      <section aria-labelledby="onboarding-heading">
        <SectionHeading ar="حالة التأهيل النشط" en="Active Onboarding Status" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {ONBOARDINGS.map((item) => (
            <OnboardingCardItem key={item.id} item={item} />
          ))}
        </div>
      </section>
    </div>
  );
};

export default FounderCockpit;
