"use client";

import { useState } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type RiskBand = "critical" | "high" | "medium" | "low";
type Tier = "enterprise" | "professional" | "essential";

interface AtRiskClient {
  client_id: string;
  company_ar: string;
  company_en: string;
  tier: Tier;
  risk_score: number;
  risk_band: RiskBand;
  days_since_last_checkin: number;
  monthly_value_sar: number;
  churn_signals: string[];
  last_contact_ar: string;
  last_contact_en: string;
}

type ModalKind = "intervention" | "proof_pack";

interface ModalState {
  kind: ModalKind;
  client: AtRiskClient;
}

interface ChurnDashboardProps {
  locale: string;
}

// ---------------------------------------------------------------------------
// Risk score computation — mirrors _compute_risk_score in churn_prevention_ops.py
// ---------------------------------------------------------------------------

const WEIGHT_HEALTH_SCORE = 0.3;
const WEIGHT_DAYS_SINCE_CHECKIN = 0.1;
const WEIGHT_MISSED_CHECKINS = 0.2;
const WEIGHT_NPS_SCORE = 0.2;
const WEIGHT_CONTRACT_DAYS = 0.2;

interface RawClient extends Omit<AtRiskClient, "risk_score" | "risk_band"> {
  health_score: number;
  consecutive_missed_checkins: number;
  nps_score: number;
  contract_days_remaining: number;
}

function computeRiskScore(c: RawClient): { score: number; band: RiskBand } {
  const healthRisk = 100 - c.health_score;
  const checkinRisk = Math.min(c.days_since_last_checkin / 90, 1) * 100;
  const missedRisk = Math.min(c.consecutive_missed_checkins / 5, 1) * 100;
  const npsRisk = ((10 - c.nps_score) / 9) * 100;
  const contractRisk = (1 - Math.min(c.contract_days_remaining / 180, 1)) * 100;

  const raw =
    healthRisk * WEIGHT_HEALTH_SCORE +
    checkinRisk * WEIGHT_DAYS_SINCE_CHECKIN +
    missedRisk * WEIGHT_MISSED_CHECKINS +
    npsRisk * WEIGHT_NPS_SCORE +
    contractRisk * WEIGHT_CONTRACT_DAYS;

  const score = Math.round(Math.min(Math.max(raw, 0), 100) * 100) / 100;

  const band: RiskBand =
    score >= 70 ? "critical" : score >= 50 ? "high" : score >= 30 ? "medium" : "low";

  return { score, band };
}

// ---------------------------------------------------------------------------
// Demo data — ARC-001 through ARC-007, matching churn_prevention_ops.py exactly
// ---------------------------------------------------------------------------

const RAW_CLIENTS: RawClient[] = [
  {
    client_id: "ARC-001",
    company_ar: "شركة الخدمات اللوجستية السريعة",
    company_en: "Rapid Logistics Services Co.",
    tier: "enterprise",
    health_score: 18,
    days_since_last_checkin: 65,
    consecutive_missed_checkins: 4,
    nps_score: 2,
    contract_days_remaining: 12,
    monthly_value_sar: 4999,
    churn_signals: [
      "Health score critically low",
      "No contact in over 60 days",
      "Four consecutive missed checkins",
      "NPS at minimum threshold",
      "Contract expiring in under two weeks",
    ],
    last_contact_ar: "منذ 65 يوماً",
    last_contact_en: "65 days ago",
  },
  {
    client_id: "ARC-002",
    company_ar: "مجموعة التصنيع الصناعي المتقدم",
    company_en: "Advanced Industrial Manufacturing Group",
    tier: "professional",
    health_score: 22,
    days_since_last_checkin: 48,
    consecutive_missed_checkins: 3,
    nps_score: 3,
    contract_days_remaining: 18,
    monthly_value_sar: 3999,
    churn_signals: [
      "Health score below critical threshold",
      "Engagement dropped sharply over last 30 days",
      "Three consecutive missed checkins",
      "NPS score trending downward",
      "Contract renewal not yet confirmed",
    ],
    last_contact_ar: "منذ 48 يوماً",
    last_contact_en: "48 days ago",
  },
  {
    client_id: "ARC-003",
    company_ar: "شركة التجزئة الرقمية الموحدة",
    company_en: "Unified Digital Retail Co.",
    tier: "professional",
    health_score: 40,
    days_since_last_checkin: 32,
    consecutive_missed_checkins: 2,
    nps_score: 5,
    contract_days_remaining: 35,
    monthly_value_sar: 3999,
    churn_signals: [
      "Health score in lower range",
      "Two consecutive missed checkins",
      "NPS score below satisfaction benchmark",
      "Limited engagement with delivered outputs",
    ],
    last_contact_ar: "منذ 32 يوماً",
    last_contact_en: "32 days ago",
  },
  {
    client_id: "ARC-004",
    company_ar: "أكاديمية التطوير المهني",
    company_en: "Professional Development Academy",
    tier: "essential",
    health_score: 48,
    days_since_last_checkin: 28,
    consecutive_missed_checkins: 2,
    nps_score: 6,
    contract_days_remaining: 42,
    monthly_value_sar: 2999,
    churn_signals: [
      "Health score slightly below average",
      "Two missed checkins in current cycle",
      "Feature adoption lower than expected",
    ],
    last_contact_ar: "منذ 28 يوماً",
    last_contact_en: "28 days ago",
  },
  {
    client_id: "ARC-005",
    company_ar: "شركة الرعاية الصحية المتكاملة",
    company_en: "Integrated Healthcare Co.",
    tier: "enterprise",
    health_score: 55,
    days_since_last_checkin: 20,
    consecutive_missed_checkins: 1,
    nps_score: 6,
    contract_days_remaining: 55,
    monthly_value_sar: 4999,
    churn_signals: [
      "One missed checkin this period",
      "Below-average NPS relative to sector",
    ],
    last_contact_ar: "منذ 20 يوماً",
    last_contact_en: "20 days ago",
  },
  {
    client_id: "ARC-006",
    company_ar: "مجموعة الخدمات المالية الإقليمية",
    company_en: "Regional Financial Services Group",
    tier: "professional",
    health_score: 62,
    days_since_last_checkin: 14,
    consecutive_missed_checkins: 1,
    nps_score: 7,
    contract_days_remaining: 60,
    monthly_value_sar: 3999,
    churn_signals: [
      "One missed checkin this period",
      "Contract renewal conversation not initiated",
    ],
    last_contact_ar: "منذ 14 يوماً",
    last_contact_en: "14 days ago",
  },
  {
    client_id: "ARC-007",
    company_ar: "شركة التقنية والابتكار السعودية",
    company_en: "Saudi Technology and Innovation Co.",
    tier: "enterprise",
    health_score: 82,
    days_since_last_checkin: 7,
    consecutive_missed_checkins: 0,
    nps_score: 9,
    contract_days_remaining: 180,
    monthly_value_sar: 4999,
    churn_signals: ["Minor delay in last deliverable review"],
    last_contact_ar: "منذ 7 أيام",
    last_contact_en: "7 days ago",
  },
];

// Enrich with computed risk fields, sort by descending score
const CLIENTS: AtRiskClient[] = RAW_CLIENTS.map((r) => {
  const { score, band } = computeRiskScore(r);
  return { ...r, risk_score: score, risk_band: band };
}).sort((a, b) => b.risk_score - a.risk_score);

// ---------------------------------------------------------------------------
// Tier labels
// ---------------------------------------------------------------------------

const TIER_LABELS: Record<Tier, { ar: string; en: string }> = {
  enterprise: { ar: "مؤسسي", en: "Enterprise" },
  professional: { ar: "احترافي", en: "Professional" },
  essential: { ar: "أساسي", en: "Essential" },
};

// ---------------------------------------------------------------------------
// Risk band styling helpers
// ---------------------------------------------------------------------------

const BAND_STYLES: Record<
  RiskBand,
  { bg: string; text: string; border: string; bar: string; ar: string; en: string }
> = {
  critical: {
    bg: "bg-red-100",
    text: "text-red-800",
    border: "border-red-200",
    bar: "bg-red-500",
    ar: "حرج",
    en: "Critical",
  },
  high: {
    bg: "bg-amber-100",
    text: "text-amber-800",
    border: "border-amber-200",
    bar: "bg-amber-500",
    ar: "مرتفع",
    en: "High",
  },
  medium: {
    bg: "bg-yellow-100",
    text: "text-yellow-800",
    border: "border-yellow-200",
    bar: "bg-yellow-400",
    ar: "متوسط",
    en: "Medium",
  },
  low: {
    bg: "bg-green-100",
    text: "text-green-800",
    border: "border-green-200",
    bar: "bg-green-400",
    ar: "منخفض",
    en: "Low",
  },
};

function riskScoreBarColor(score: number): string {
  if (score >= 70) return "bg-red-500";
  if (score >= 50) return "bg-amber-500";
  if (score >= 30) return "bg-yellow-400";
  return "bg-green-400";
}

// ---------------------------------------------------------------------------
// Intervention modal
// ---------------------------------------------------------------------------

function InterventionModal({
  client,
  isAr,
  onClose,
}: {
  client: AtRiskClient;
  isAr: boolean;
  onClose: () => void;
}) {
  const companyName = isAr ? client.company_ar : client.company_en;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white rounded-xl shadow-xl border border-gray-200 p-6 max-w-md w-full mx-4">
        <h3 className="text-base font-bold text-gray-900 mb-1">
          {isAr ? "تسجيل تدخل" : "Log Intervention"}
        </h3>
        <p className="text-sm text-gray-500 mb-4 font-mono">{client.client_id}</p>
        <p className="text-sm text-gray-700 mb-3">
          {isAr ? `الشركة: ${companyName}` : `Company: ${companyName}`}
        </p>
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 space-y-2">
          <p className="text-sm font-bold text-amber-800">
            {isAr
              ? "هذا الإجراء يتطلب موافقة المؤسس قبل التنفيذ"
              : "This action requires founder approval before execution"}
          </p>
          <p className="text-xs text-amber-700 font-mono">
            governance_decision: APPROVAL_FIRST
          </p>
        </div>
        <div className="mt-5 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="text-sm font-semibold px-4 py-2 rounded-lg bg-gray-900 text-white hover:bg-gray-700 transition-colors"
          >
            {isAr ? "حسناً" : "OK"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Proof Pack modal
// ---------------------------------------------------------------------------

function ProofPackModal({
  client,
  isAr,
  onClose,
}: {
  client: AtRiskClient;
  isAr: boolean;
  onClose: () => void;
}) {
  const companyName = isAr ? client.company_ar : client.company_en;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white rounded-xl shadow-xl border border-gray-200 p-6 max-w-md w-full mx-4">
        <h3 className="text-base font-bold text-gray-900 mb-1">
          {isAr ? "إرسال Proof Pack" : "Send Proof Pack"}
        </h3>
        <p className="text-sm text-gray-500 mb-4 font-mono">{client.client_id}</p>
        <p className="text-sm text-gray-700 mb-3">
          {isAr ? `الشركة: ${companyName}` : `Company: ${companyName}`}
        </p>
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 mb-3">
          <p className="text-sm font-bold text-red-800">
            {isAr
              ? "واتساب محظور كقناة تسليم"
              : "WhatsApp not permitted — email or in-person only"}
          </p>
          <p className="text-xs text-red-700 mt-1">
            {isAr
              ? "يُخالف سياسة التواصل غير المرغوب فيه — استخدم البريد الإلكتروني أو اللقاء الشخصي"
              : "Violates no-unsolicited-outreach doctrine. Allowed channels: email, in_person."}
          </p>
        </div>
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
          <p className="text-sm font-bold text-amber-800">
            {isAr
              ? "يتطلب موافقة المؤسس قبل الإرسال"
              : "Requires founder approval before sending"}
          </p>
          <p className="text-xs text-amber-700 font-mono mt-1">
            governance_decision: APPROVAL_FIRST
          </p>
        </div>
        <div className="mt-5 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="text-sm font-semibold px-4 py-2 rounded-lg bg-gray-900 text-white hover:bg-gray-700 transition-colors"
          >
            {isAr ? "حسناً" : "OK"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Root component
// ---------------------------------------------------------------------------

export default function ChurnDashboard({ locale }: ChurnDashboardProps) {
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  const [modal, setModal] = useState<ModalState | null>(null);

  // ---------------------------------------------------------------------------
  // Derived summary counts
  // ---------------------------------------------------------------------------

  const criticalCount = CLIENTS.filter((c) => c.risk_band === "critical").length;
  const highCount = CLIENTS.filter((c) => c.risk_band === "high").length;
  const mediumCount = CLIENTS.filter((c) => c.risk_band === "medium").length;
  const lowCount = CLIENTS.filter((c) => c.risk_band === "low").length;
  const total = CLIENTS.length;

  const revenueAtRisk = CLIENTS.filter(
    (c) => c.risk_band === "critical" || c.risk_band === "high"
  ).reduce((sum, c) => sum + c.monthly_value_sar, 0);

  // Heat bar segment widths (percentage of total clients)
  function pct(count: number) {
    return total > 0 ? (count / total) * 100 : 0;
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6" dir={dir}>
      {/* Page heading */}
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900">
          {isAr ? "لوحة تحكم منع الاضطراب" : "Churn Prevention Dashboard"}
        </h1>
        <p className="text-sm text-gray-500 mt-0.5">
          {isAr
            ? "رصد مخاطر الاضطراب وإدارة التدخلات للعملاء النشطين"
            : "Monitor churn risk and manage interventions for active clients"}
        </p>
      </div>

      {/* Risk overview — 4 stat cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* Critical */}
        <div className="bg-white rounded-xl border border-red-100 shadow-sm p-5">
          <p className="text-xs font-medium text-gray-400 mb-1">
            {isAr ? "حرج" : "Critical"}
          </p>
          <p className="text-3xl font-extrabold text-red-600 tabular-nums">
            {criticalCount}
          </p>
          <p className="text-xs text-red-500 mt-1">
            {isAr ? "عملاء" : "clients"}
          </p>
        </div>

        {/* High */}
        <div className="bg-white rounded-xl border border-amber-100 shadow-sm p-5">
          <p className="text-xs font-medium text-gray-400 mb-1">
            {isAr ? "مرتفع" : "High"}
          </p>
          <p className="text-3xl font-extrabold text-amber-600 tabular-nums">
            {highCount}
          </p>
          <p className="text-xs text-amber-500 mt-1">
            {isAr ? "عملاء" : "clients"}
          </p>
        </div>

        {/* Medium */}
        <div className="bg-white rounded-xl border border-yellow-100 shadow-sm p-5">
          <p className="text-xs font-medium text-gray-400 mb-1">
            {isAr ? "متوسط" : "Medium"}
          </p>
          <p className="text-3xl font-extrabold text-yellow-600 tabular-nums">
            {mediumCount}
          </p>
          <p className="text-xs text-yellow-500 mt-1">
            {isAr ? "عملاء" : "clients"}
          </p>
        </div>

        {/* Revenue at risk */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs font-medium text-gray-400 mb-1">
            {isAr ? "الإيرادات المعرضة للخطر" : "Monthly Revenue at Risk"}
          </p>
          <p
            className={`text-2xl font-extrabold tabular-nums ${
              revenueAtRisk > 0 ? "text-red-600" : "text-gray-900"
            }`}
          >
            {revenueAtRisk.toLocaleString("ar-SA")}
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {isAr ? "ر.س / شهر" : "SAR / month"}
          </p>
        </div>
      </div>

      {/* Risk heat bar */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
        <p className="text-xs font-semibold text-gray-500 mb-3">
          {isAr ? "توزيع مستويات المخاطر" : "Risk Level Distribution"}
        </p>
        <div className="flex h-6 w-full rounded-full overflow-hidden gap-px">
          {criticalCount > 0 && (
            <div
              style={{ width: `${pct(criticalCount)}%` }}
              className="bg-red-500 flex items-center justify-center"
              title={isAr ? `حرج: ${criticalCount}` : `Critical: ${criticalCount}`}
            >
              {pct(criticalCount) >= 10 && (
                <span className="text-white text-xs font-bold">{criticalCount}</span>
              )}
            </div>
          )}
          {highCount > 0 && (
            <div
              style={{ width: `${pct(highCount)}%` }}
              className="bg-amber-500 flex items-center justify-center"
              title={isAr ? `مرتفع: ${highCount}` : `High: ${highCount}`}
            >
              {pct(highCount) >= 10 && (
                <span className="text-white text-xs font-bold">{highCount}</span>
              )}
            </div>
          )}
          {mediumCount > 0 && (
            <div
              style={{ width: `${pct(mediumCount)}%` }}
              className="bg-yellow-400 flex items-center justify-center"
              title={isAr ? `متوسط: ${mediumCount}` : `Medium: ${mediumCount}`}
            >
              {pct(mediumCount) >= 10 && (
                <span className="text-white text-xs font-bold">{mediumCount}</span>
              )}
            </div>
          )}
          {lowCount > 0 && (
            <div
              style={{ width: `${pct(lowCount)}%` }}
              className="bg-green-400 flex items-center justify-center"
              title={isAr ? `منخفض: ${lowCount}` : `Low: ${lowCount}`}
            >
              {pct(lowCount) >= 10 && (
                <span className="text-white text-xs font-bold">{lowCount}</span>
              )}
            </div>
          )}
        </div>
        {/* Legend */}
        <div className="flex flex-wrap gap-4 mt-3">
          {(
            [
              { band: "critical" as RiskBand, count: criticalCount },
              { band: "high" as RiskBand, count: highCount },
              { band: "medium" as RiskBand, count: mediumCount },
              { band: "low" as RiskBand, count: lowCount },
            ] as const
          ).map(({ band, count }) => {
            const s = BAND_STYLES[band];
            return (
              <div key={band} className="flex items-center gap-1.5">
                <span className={`inline-block w-3 h-3 rounded-sm ${s.bar}`} />
                <span className="text-xs text-gray-600">
                  {isAr ? s.ar : s.en}: {count}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* At-risk client table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
        <div className="px-5 py-4 border-b border-gray-100">
          <h2 className="text-sm font-bold text-gray-800">
            {isAr ? "العملاء المعرضون للمخاطر" : "At-Risk Clients"}
          </h2>
          <p className="text-xs text-gray-400 mt-0.5">
            {isAr
              ? `${CLIENTS.length} عميل مُراقَب — مرتب حسب درجة المخاطرة`
              : `${CLIENTS.length} monitored clients — sorted by risk score`}
          </p>
        </div>

        <table className="w-full text-sm" dir={dir}>
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50">
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الشركة" : "Company"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الباقة" : "Tier"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "درجة المخاطرة" : "Risk Score"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "مستوى المخاطرة" : "Risk Band"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "آخر تواصل" : "Days Since Contact"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "القيمة الشهرية" : "Monthly Value"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "إشارات الاضطراب" : "Churn Signals"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الإجراءات" : "Actions"}
              </th>
            </tr>
          </thead>
          <tbody>
            {CLIENTS.map((client, idx) => {
              const bandStyle = BAND_STYLES[client.risk_band];
              const tier = TIER_LABELS[client.tier];
              const isEven = idx % 2 === 0;

              return (
                <tr
                  key={client.client_id}
                  className={`border-b border-gray-50 ${
                    isEven ? "bg-white" : "bg-gray-50/50"
                  } hover:bg-blue-50/30 transition-colors`}
                >
                  {/* Company */}
                  <td className="px-4 py-3">
                    <p className="font-semibold text-gray-900 whitespace-nowrap">
                      {isAr ? client.company_ar : client.company_en}
                    </p>
                    <p className="text-xs text-gray-400 font-mono">
                      {client.client_id}
                    </p>
                  </td>

                  {/* Tier */}
                  <td className="px-4 py-3 whitespace-nowrap text-gray-700">
                    {isAr ? tier.ar : tier.en}
                  </td>

                  {/* Risk score bar */}
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2 min-w-[100px]">
                      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${riskScoreBarColor(client.risk_score)}`}
                          style={{ width: `${client.risk_score}%` }}
                        />
                      </div>
                      <span className="text-xs font-bold tabular-nums text-gray-700 w-8 text-end">
                        {Math.round(client.risk_score)}
                      </span>
                    </div>
                  </td>

                  {/* Risk band badge */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span
                      className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full border ${bandStyle.bg} ${bandStyle.text} ${bandStyle.border}`}
                    >
                      {isAr ? bandStyle.ar : bandStyle.en}
                    </span>
                  </td>

                  {/* Days since contact */}
                  <td className="px-4 py-3 whitespace-nowrap text-gray-700 text-xs">
                    {isAr ? client.last_contact_ar : client.last_contact_en}
                  </td>

                  {/* Monthly value */}
                  <td className="px-4 py-3 whitespace-nowrap tabular-nums font-semibold text-gray-800">
                    {client.monthly_value_sar.toLocaleString("ar-SA")}{" "}
                    <span className="font-normal text-gray-500">
                      {isAr ? "ر.س" : "SAR"}
                    </span>
                  </td>

                  {/* Churn signals */}
                  <td className="px-4 py-3 max-w-xs">
                    <p className="text-xs text-gray-600 leading-relaxed">
                      {client.churn_signals.join(", ")}
                    </p>
                  </td>

                  {/* Actions */}
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2 flex-wrap">
                      <button
                        type="button"
                        onClick={() => setModal({ kind: "intervention", client })}
                        className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-blue-300 text-blue-700 bg-blue-50 hover:bg-blue-100 transition-colors whitespace-nowrap"
                      >
                        {isAr ? "تسجيل تدخل" : "Log Intervention"}
                      </button>
                      <button
                        type="button"
                        onClick={() => setModal({ kind: "proof_pack", client })}
                        className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-purple-300 text-purple-700 bg-purple-50 hover:bg-purple-100 transition-colors whitespace-nowrap"
                      >
                        {isAr ? "إرسال Proof Pack" : "Send Proof Pack"}
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Modals */}
      {modal !== null && modal.kind === "intervention" && (
        <InterventionModal
          client={modal.client}
          isAr={isAr}
          onClose={() => setModal(null)}
        />
      )}
      {modal !== null && modal.kind === "proof_pack" && (
        <ProofPackModal
          client={modal.client}
          isAr={isAr}
          onClose={() => setModal(null)}
        />
      )}
    </div>
  );
}
