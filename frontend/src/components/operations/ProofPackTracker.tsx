"use client";

import { useState } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type PackStatus = "draft" | "review" | "approved" | "delivered" | "archived";
type PackType =
  | "sprint_result"
  | "monthly_ops"
  | "annual_review"
  | "zatca_compliance";

interface Metric {
  metric_name_ar: string;
  metric_name_en: string;
  baseline_value: number;
  current_value: number;
  unit: string;
  improvement_pct: number;
  verified: boolean;
}

interface ProofPack {
  pack_id: string;
  client_id: string;
  company_ar: string;
  company_en: string;
  sprint_id: string | null;
  status: PackStatus;
  pack_type: PackType;
  generated_at: string;
  delivered_at: string | null;
  metrics: Metric[];
  proof_score: number;
  reviewer_notes: string | null;
  approved_by: string | null;
  delivery_channel: string | null;
}

interface ProofPackTrackerProps {
  locale: string;
}

// ---------------------------------------------------------------------------
// Static demo data — matches api/routers/proof_pack_ops.py exactly
// ---------------------------------------------------------------------------

const PACKS: ProofPack[] = [
  {
    pack_id: "PP-001",
    client_id: "CLT-001",
    company_ar: "شركة التقنية المتقدمة",
    company_en: "Advanced Technology Co.",
    sprint_id: "SPR-001",
    status: "delivered",
    pack_type: "sprint_result",
    generated_at: "2026-03-15T10:00:00+00:00",
    delivered_at: "2026-03-18T14:30:00+00:00",
    metrics: [
      {
        metric_name_ar: "درجة جودة البيانات",
        metric_name_en: "Data Quality Score",
        baseline_value: 48.0,
        current_value: 89.0,
        unit: "score",
        improvement_pct: 85.42,
        verified: true,
      },
      {
        metric_name_ar: "معدل التسليم في الوقت المحدد",
        metric_name_en: "On-Time Delivery Rate",
        baseline_value: 62.0,
        current_value: 91.0,
        unit: "%",
        improvement_pct: 46.77,
        verified: true,
      },
      {
        metric_name_ar: "وقت معالجة الفاتورة",
        metric_name_en: "Invoice Processing Time",
        baseline_value: 5.0,
        current_value: 1.5,
        unit: "days",
        improvement_pct: 70.0,
        verified: true,
      },
    ],
    proof_score: 82,
    reviewer_notes:
      "Excellent results across all KPIs. Ready for annual review expansion.",
    approved_by: "Bassam Al-Assiri",
    delivery_channel: "email",
  },
  {
    pack_id: "PP-002",
    client_id: "CLT-002",
    company_ar: "مجموعة الخدمات المالية الخليجية",
    company_en: "Gulf Financial Services Group",
    sprint_id: "SPR-002",
    status: "delivered",
    pack_type: "zatca_compliance",
    generated_at: "2026-04-01T09:00:00+00:00",
    delivered_at: "2026-04-04T11:00:00+00:00",
    metrics: [
      {
        metric_name_ar: "معدل الامتثال لهيئة الزكاة والضريبة",
        metric_name_en: "ZATCA Compliance Rate",
        baseline_value: 0.0,
        current_value: 100.0,
        unit: "%",
        improvement_pct: 100.0,
        verified: true,
      },
      {
        metric_name_ar: "نسبة الفواتير الإلكترونية المُرسلة",
        metric_name_en: "E-Invoice Submission Rate",
        baseline_value: 10.0,
        current_value: 98.0,
        unit: "%",
        improvement_pct: 880.0,
        verified: true,
      },
      {
        metric_name_ar: "وقت التحقق من الامتثال",
        metric_name_en: "Compliance Verification Time",
        baseline_value: 14.0,
        current_value: 2.0,
        unit: "days",
        improvement_pct: 85.71,
        verified: true,
      },
    ],
    proof_score: 94,
    reviewer_notes:
      "Full ZATCA Phase 2 compliance achieved. Delivered in-person at client HQ.",
    approved_by: "Bassam Al-Assiri",
    delivery_channel: "in_person",
  },
  {
    pack_id: "PP-003",
    client_id: "CLT-003",
    company_ar: "شركة العقارات السعودية الكبرى",
    company_en: "Major Saudi Real Estate Co.",
    sprint_id: null,
    status: "delivered",
    pack_type: "monthly_ops",
    generated_at: "2026-04-30T08:00:00+00:00",
    delivered_at: "2026-05-02T10:00:00+00:00",
    metrics: [
      {
        metric_name_ar: "تخفيض تسرب الإيرادات",
        metric_name_en: "Revenue Leakage Reduction",
        baseline_value: 85000.0,
        current_value: 12000.0,
        unit: "SAR",
        improvement_pct: 85.88,
        verified: true,
      },
      {
        metric_name_ar: "درجة رضا العملاء",
        metric_name_en: "Client Satisfaction Score",
        baseline_value: 3.1,
        current_value: 4.4,
        unit: "score/5",
        improvement_pct: 41.94,
        verified: false,
      },
      {
        metric_name_ar: "معدل التسليم في الوقت المحدد",
        metric_name_en: "On-Time Delivery Rate",
        baseline_value: 71.0,
        current_value: 88.0,
        unit: "%",
        improvement_pct: 23.94,
        verified: true,
      },
    ],
    proof_score: 58,
    reviewer_notes:
      "Good revenue leakage reduction. Client satisfaction metric awaiting verification.",
    approved_by: "Bassam Al-Assiri",
    delivery_channel: "email",
  },
  {
    pack_id: "PP-004",
    client_id: "CLT-004",
    company_ar: "شركة التجزئة الذكية",
    company_en: "Smart Retail Solutions",
    sprint_id: "SPR-004",
    status: "approved",
    pack_type: "sprint_result",
    generated_at: "2026-05-20T09:00:00+00:00",
    delivered_at: null,
    metrics: [
      {
        metric_name_ar: "درجة جودة البيانات",
        metric_name_en: "Data Quality Score",
        baseline_value: 52.0,
        current_value: 78.0,
        unit: "score",
        improvement_pct: 50.0,
        verified: true,
      },
      {
        metric_name_ar: "تخفيض وقت معالجة الطلبات",
        metric_name_en: "Order Processing Time Reduction",
        baseline_value: 4.0,
        current_value: 1.2,
        unit: "hours",
        improvement_pct: 70.0,
        verified: true,
      },
    ],
    proof_score: 60,
    reviewer_notes:
      "Solid improvement in data quality and processing. Approved for delivery.",
    approved_by: "Bassam Al-Assiri",
    delivery_channel: null,
  },
  {
    pack_id: "PP-005",
    client_id: "CLT-005",
    company_ar: "مستشفى الصحة المتكاملة",
    company_en: "Integrated Health Hospital",
    sprint_id: null,
    status: "approved",
    pack_type: "monthly_ops",
    generated_at: "2026-05-22T11:00:00+00:00",
    delivered_at: null,
    metrics: [
      {
        metric_name_ar: "معدل الامتثال لهيئة الزكاة والضريبة",
        metric_name_en: "ZATCA Compliance Rate",
        baseline_value: 45.0,
        current_value: 92.0,
        unit: "%",
        improvement_pct: 104.44,
        verified: true,
      },
      {
        metric_name_ar: "تخفيض تسرب الإيرادات",
        metric_name_en: "Revenue Leakage Reduction",
        baseline_value: 120000.0,
        current_value: 30000.0,
        unit: "SAR",
        improvement_pct: 75.0,
        verified: true,
      },
      {
        metric_name_ar: "وقت معالجة الفاتورة",
        metric_name_en: "Invoice Processing Time",
        baseline_value: 8.0,
        current_value: 2.0,
        unit: "days",
        improvement_pct: 75.0,
        verified: false,
      },
    ],
    proof_score: 72,
    reviewer_notes:
      "Strong compliance and revenue recovery. Invoice time pending audit verification.",
    approved_by: "Bassam Al-Assiri",
    delivery_channel: null,
  },
  {
    pack_id: "PP-006",
    client_id: "CLT-006",
    company_ar: "شركة الخدمات اللوجستية المتطورة",
    company_en: "Advanced Logistics Services Co.",
    sprint_id: "SPR-006",
    status: "draft",
    pack_type: "sprint_result",
    generated_at: "2026-05-28T13:00:00+00:00",
    delivered_at: null,
    metrics: [
      {
        metric_name_ar: "درجة جودة البيانات",
        metric_name_en: "Data Quality Score",
        baseline_value: 30.0,
        current_value: 55.0,
        unit: "score",
        improvement_pct: 83.33,
        verified: false,
      },
      {
        metric_name_ar: "معدل التسليم في الوقت المحدد",
        metric_name_en: "On-Time Delivery Rate",
        baseline_value: 55.0,
        current_value: 72.0,
        unit: "%",
        improvement_pct: 30.91,
        verified: false,
      },
    ],
    proof_score: 0,
    reviewer_notes: null,
    approved_by: null,
    delivery_channel: null,
  },
  {
    pack_id: "PP-007",
    client_id: "CLT-007",
    company_ar: "أكاديمية التعليم الرقمي",
    company_en: "Digital Education Academy",
    sprint_id: null,
    status: "draft",
    pack_type: "annual_review",
    generated_at: "2026-05-29T09:00:00+00:00",
    delivered_at: null,
    metrics: [
      {
        metric_name_ar: "نسبة الفواتير الإلكترونية المُرسلة",
        metric_name_en: "E-Invoice Submission Rate",
        baseline_value: 0.0,
        current_value: 60.0,
        unit: "%",
        improvement_pct: 100.0,
        verified: false,
      },
    ],
    proof_score: 0,
    reviewer_notes: null,
    approved_by: null,
    delivery_channel: null,
  },
  {
    pack_id: "PP-008",
    client_id: "CLT-008",
    company_ar: "شركة التصنيع الصناعي الخليجي",
    company_en: "Gulf Industrial Manufacturing Co.",
    sprint_id: "SPR-008",
    status: "review",
    pack_type: "zatca_compliance",
    generated_at: "2026-05-25T10:00:00+00:00",
    delivered_at: null,
    metrics: [
      {
        metric_name_ar: "معدل الامتثال لهيئة الزكاة والضريبة",
        metric_name_en: "ZATCA Compliance Rate",
        baseline_value: 20.0,
        current_value: 95.0,
        unit: "%",
        improvement_pct: 375.0,
        verified: true,
      },
      {
        metric_name_ar: "تخفيض تسرب الإيرادات",
        metric_name_en: "Revenue Leakage Reduction",
        baseline_value: 200000.0,
        current_value: 18000.0,
        unit: "SAR",
        improvement_pct: 91.0,
        verified: true,
      },
      {
        metric_name_ar: "درجة رضا العملاء",
        metric_name_en: "Client Satisfaction Score",
        baseline_value: 2.8,
        current_value: 4.6,
        unit: "score/5",
        improvement_pct: 64.29,
        verified: false,
      },
    ],
    proof_score: 67,
    reviewer_notes:
      "Pending founder sign-off. ZATCA gains are verified; satisfaction score still being audited.",
    approved_by: null,
    delivery_channel: null,
  },
];

// ---------------------------------------------------------------------------
// Status badge configuration
// ---------------------------------------------------------------------------

const STATUS_STYLES: Record<
  PackStatus,
  { bg: string; text: string; ar: string; en: string }
> = {
  draft: { bg: "bg-gray-100", text: "text-gray-600", ar: "مسودة", en: "Draft" },
  review: {
    bg: "bg-yellow-100",
    text: "text-yellow-800",
    ar: "قيد المراجعة",
    en: "Review",
  },
  approved: {
    bg: "bg-blue-100",
    text: "text-blue-700",
    ar: "معتمد",
    en: "Approved",
  },
  delivered: {
    bg: "bg-emerald-100",
    text: "text-emerald-700",
    ar: "مُسلَّم",
    en: "Delivered",
  },
  archived: {
    bg: "bg-gray-200",
    text: "text-gray-700",
    ar: "مؤرشف",
    en: "Archived",
  },
};

// ---------------------------------------------------------------------------
// Pack type badge configuration
// ---------------------------------------------------------------------------

const PACK_TYPE_STYLES: Record<
  PackType,
  { bg: string; text: string; ar: string; en: string }
> = {
  sprint_result: {
    bg: "bg-indigo-100",
    text: "text-indigo-700",
    ar: "نتيجة سبرينت",
    en: "Sprint Result",
  },
  monthly_ops: {
    bg: "bg-teal-100",
    text: "text-teal-700",
    ar: "العمليات الشهرية",
    en: "Monthly Ops",
  },
  annual_review: {
    bg: "bg-purple-100",
    text: "text-purple-700",
    ar: "المراجعة السنوية",
    en: "Annual Review",
  },
  zatca_compliance: {
    bg: "bg-orange-100",
    text: "text-orange-700",
    ar: "امتثال ZATCA",
    en: "ZATCA Compliance",
  },
};

// ---------------------------------------------------------------------------
// Pipeline stages
// ---------------------------------------------------------------------------

const PIPELINE_STAGES: PackStatus[] = [
  "draft",
  "review",
  "approved",
  "delivered",
  "archived",
];

// ---------------------------------------------------------------------------
// Proof score bar
// ---------------------------------------------------------------------------

function ProofScoreBar({ score }: { score: number }) {
  const pct = Math.min(100, Math.max(0, score));
  const barColor =
    pct >= 70
      ? "bg-emerald-500"
      : pct >= 40
      ? "bg-amber-500"
      : "bg-red-500";

  return (
    <div className="flex items-center gap-2 min-w-[100px]">
      <div className="flex-1 h-2 rounded-full bg-gray-100 overflow-hidden">
        <div
          className={`h-2 rounded-full ${barColor} transition-all`}
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
      <span className="text-xs font-semibold tabular-nums text-gray-700 w-7 text-end">
        {score}
      </span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// APPROVAL_FIRST modal
// ---------------------------------------------------------------------------

function ApprovalFirstModal({
  actionAr,
  actionEn,
  isAr,
  onClose,
}: {
  actionAr: string;
  actionEn: string;
  isAr: boolean;
  onClose: () => void;
}) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white rounded-xl shadow-xl border border-gray-200 p-6 max-w-md w-full mx-4">
        <h3 className="text-base font-bold text-gray-900 mb-2">
          {isAr ? "موافقة مطلوبة" : "Approval Required"}
        </h3>
        <p className="text-sm text-gray-700 mb-1">
          {isAr ? actionAr : actionEn}
        </p>
        <p className="text-sm font-semibold text-amber-700 bg-amber-50 border border-amber-200 rounded-lg p-3 mt-3">
          {isAr
            ? "هذا الإجراء يتطلب موافقة المؤسس قبل التنفيذ (APPROVAL_FIRST)."
            : "This action requires founder approval before execution (APPROVAL_FIRST)."}
        </p>
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

export default function ProofPackTracker({ locale }: ProofPackTrackerProps) {
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [modal, setModal] = useState<{
    actionAr: string;
    actionEn: string;
  } | null>(null);

  // Derived summary values
  const totalPacks = PACKS.length;
  const deliveredCount = PACKS.filter((p) => p.status === "delivered").length;
  const pendingDeliveryCount = PACKS.filter(
    (p) => p.status === "approved" && p.delivered_at === null
  ).length;
  const allScores = PACKS.map((p) => p.proof_score);
  const avgProofScore =
    allScores.length > 0
      ? Math.round(
          (allScores.reduce((a, b) => a + b, 0) / allScores.length) * 10
        ) / 10
      : 0;

  // Pipeline stage counts
  const stageCounts: Record<PackStatus, number> = {
    draft: 0,
    review: 0,
    approved: 0,
    delivered: 0,
    archived: 0,
  };
  for (const pack of PACKS) {
    stageCounts[pack.status] = (stageCounts[pack.status] ?? 0) + 1;
  }

  // Filtering
  const filtered = PACKS.filter(
    (p) => filterStatus === "all" || p.status === filterStatus
  );

  function formatDate(iso: string): string {
    return iso.slice(0, 10);
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6" dir={dir}>
      {/* Page heading */}
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900">
          {isAr ? "متتبع Proof Pack" : "Proof Pack Tracker"}
        </h1>
        <p className="text-sm text-gray-500 mt-0.5">
          {isAr
            ? "حزم الإثبات القابلة للتحقق — المراجعة والاعتماد والتسليم"
            : "Verifiable result packs — review, approval, and delivery"}
        </p>
      </div>

      {/* WhatsApp warning */}
      <div
        className="rounded-xl border border-red-200 bg-red-50 px-5 py-3"
        role="alert"
      >
        <p className="text-sm font-semibold text-red-700">
          {isAr
            ? "واتساب غير مسموح به لتسليم Proof Pack — استخدم البريد الإلكتروني أو اللقاء الشخصي"
            : "WhatsApp not permitted for Proof Pack delivery — use email or in-person"}
        </p>
      </div>

      {/* Summary bar */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "إجمالي الحزم" : "Total Packs"}
          </p>
          <p className="text-3xl font-extrabold text-gray-900 tabular-nums">
            {totalPacks}
          </p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "مُسلَّمة" : "Delivered"}
          </p>
          <p className="text-3xl font-extrabold text-emerald-700 tabular-nums">
            {deliveredCount}
          </p>
        </div>

        <div
          className={`rounded-xl border shadow-sm p-5 ${
            pendingDeliveryCount > 0
              ? "border-amber-200 bg-amber-50"
              : "border-gray-100 bg-white"
          }`}
        >
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "في انتظار التسليم" : "Pending Delivery"}
          </p>
          <p
            className={`text-3xl font-extrabold tabular-nums ${
              pendingDeliveryCount > 0 ? "text-amber-700" : "text-gray-900"
            }`}
          >
            {pendingDeliveryCount}
          </p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "متوسط درجة الإثبات" : "Avg Proof Score"}
          </p>
          <p className="text-3xl font-extrabold text-gray-900 tabular-nums">
            {avgProofScore}
          </p>
        </div>
      </div>

      {/* Status pipeline */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
        <p className="text-xs font-semibold text-gray-500 mb-4">
          {isAr ? "مسار الحالة" : "Status Pipeline"}
        </p>
        <div className="flex items-center gap-0 overflow-x-auto">
          {PIPELINE_STAGES.map((stage, idx) => {
            const style = STATUS_STYLES[stage];
            const count = stageCounts[stage];
            const isLast = idx === PIPELINE_STAGES.length - 1;
            return (
              <div key={stage} className="flex items-center">
                <div className="flex flex-col items-center min-w-[88px]">
                  <div
                    className={`flex items-center justify-center w-9 h-9 rounded-full font-extrabold text-sm tabular-nums ${style.bg} ${style.text} border-2 ${
                      count > 0 ? "border-current" : "border-transparent"
                    }`}
                  >
                    {count}
                  </div>
                  <span className="text-xs font-semibold text-gray-600 mt-1 text-center">
                    {isAr ? style.ar : style.en}
                  </span>
                </div>
                {!isLast && (
                  <div
                    className="flex-1 h-px bg-gray-200 mx-1 min-w-[16px]"
                    aria-hidden="true"
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Filter bar */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex flex-wrap gap-4 items-center">
        <div className="flex items-center gap-2">
          <label
            htmlFor="filter-status"
            className="text-sm font-semibold text-gray-700 whitespace-nowrap"
          >
            {isAr ? "الحالة" : "Status"}
          </label>
          <select
            id="filter-status"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">{isAr ? "الكل" : "All"}</option>
            {PIPELINE_STAGES.map((s) => (
              <option key={s} value={s}>
                {isAr ? STATUS_STYLES[s].ar : STATUS_STYLES[s].en}
              </option>
            ))}
          </select>
        </div>
        <p className="text-xs text-gray-400">
          {isAr
            ? `${filtered.length} نتيجة`
            : `${filtered.length} result${filtered.length !== 1 ? "s" : ""}`}
        </p>
      </div>

      {/* Pack table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
        <table className="w-full text-sm" dir={dir}>
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50">
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "معرّف الحزمة" : "Pack ID"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "العميل" : "Client"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "النوع" : "Type"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الحالة" : "Status"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "درجة الإثبات" : "Proof Score"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "تاريخ الإنشاء" : "Generated At"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "تاريخ التسليم" : "Delivered At"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الإجراءات" : "Actions"}
              </th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td
                  colSpan={8}
                  className="text-center text-gray-400 py-10 text-sm"
                >
                  {isAr ? "لا توجد نتائج" : "No results"}
                </td>
              </tr>
            ) : (
              filtered.map((pack, idx) => {
                const statusStyle = STATUS_STYLES[pack.status];
                const typeStyle = PACK_TYPE_STYLES[pack.pack_type];
                const isEven = idx % 2 === 0;

                return (
                  <tr
                    key={pack.pack_id}
                    className={`border-b border-gray-50 ${
                      isEven ? "bg-white" : "bg-gray-50/50"
                    } hover:bg-blue-50/30 transition-colors`}
                  >
                    {/* Pack ID */}
                    <td className="px-4 py-3">
                      <p className="font-mono text-xs font-semibold text-gray-700">
                        {pack.pack_id}
                      </p>
                      {pack.sprint_id && (
                        <p className="text-xs text-gray-400 font-mono">
                          {pack.sprint_id}
                        </p>
                      )}
                    </td>

                    {/* Client */}
                    <td className="px-4 py-3">
                      <p className="font-semibold text-gray-900 whitespace-nowrap">
                        {isAr ? pack.company_ar : pack.company_en}
                      </p>
                      <p className="text-xs text-gray-400">{pack.client_id}</p>
                    </td>

                    {/* Type badge */}
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span
                        className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full ${typeStyle.bg} ${typeStyle.text}`}
                      >
                        {isAr ? typeStyle.ar : typeStyle.en}
                      </span>
                    </td>

                    {/* Status badge */}
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span
                        className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full ${statusStyle.bg} ${statusStyle.text}`}
                      >
                        {isAr ? statusStyle.ar : statusStyle.en}
                      </span>
                    </td>

                    {/* Proof score bar */}
                    <td className="px-4 py-3">
                      <ProofScoreBar score={pack.proof_score} />
                    </td>

                    {/* Generated At */}
                    <td className="px-4 py-3 text-gray-600 font-mono text-xs whitespace-nowrap">
                      {formatDate(pack.generated_at)}
                    </td>

                    {/* Delivered At */}
                    <td className="px-4 py-3 text-gray-600 font-mono text-xs whitespace-nowrap">
                      {pack.delivered_at ? formatDate(pack.delivered_at) : (
                        <span className="text-gray-400">—</span>
                      )}
                    </td>

                    {/* Actions */}
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2 flex-wrap">
                        <button
                          type="button"
                          disabled={pack.status !== "review"}
                          onClick={() =>
                            setModal({
                              actionAr: `اعتماد ${pack.pack_id}`,
                              actionEn: `Approve ${pack.pack_id}`,
                            })
                          }
                          className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-blue-300 text-blue-700 bg-blue-50 hover:bg-blue-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
                        >
                          {isAr ? "اعتماد" : "Approve"}
                        </button>
                        <button
                          type="button"
                          disabled={pack.status !== "approved"}
                          onClick={() =>
                            setModal({
                              actionAr: `تسليم ${pack.pack_id}`,
                              actionEn: `Deliver ${pack.pack_id}`,
                            })
                          }
                          className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-emerald-300 text-emerald-700 bg-emerald-50 hover:bg-emerald-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
                        >
                          {isAr ? "تسليم" : "Deliver"}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* APPROVAL_FIRST modal */}
      {modal !== null && (
        <ApprovalFirstModal
          actionAr={modal.actionAr}
          actionEn={modal.actionEn}
          isAr={isAr}
          onClose={() => setModal(null)}
        />
      )}
    </div>
  );
}
