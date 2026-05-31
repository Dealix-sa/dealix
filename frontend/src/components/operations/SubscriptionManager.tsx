"use client";

import { useState } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type SubState = "trial" | "active" | "paused" | "cancelled" | "reactivated";
type TierKey =
  | "sprint"
  | "data_pack"
  | "managed_ops_essential"
  | "managed_ops_professional"
  | "managed_ops_enterprise"
  | "custom_ai";

interface Subscription {
  sub_id: string;
  client_id: string;
  company_ar: string;
  company_en: string;
  tier: TierKey;
  state: SubState;
  monthly_value_sar: number;
  renewal_date: string;
  days_until_renewal: number;
  auto_renew: boolean;
}

interface SubscriptionManagerProps {
  locale: string;
}

// ---------------------------------------------------------------------------
// Static demo data — matches api/routers/subscription_ops.py exactly
// ---------------------------------------------------------------------------

const SUBSCRIPTIONS: Subscription[] = [
  {
    sub_id: "SUB-001",
    client_id: "CLT-001",
    company_ar: "شركة الرياض للتقنية",
    company_en: "Riyadh Tech Co",
    tier: "managed_ops_professional",
    state: "active",
    monthly_value_sar: 3999,
    renewal_date: "2026-07-01",
    days_until_renewal: 31,
    auto_renew: true,
  },
  {
    sub_id: "SUB-002",
    client_id: "CLT-002",
    company_ar: "مجموعة الخليج للخدمات المالية",
    company_en: "Gulf Financial Services Group",
    tier: "managed_ops_enterprise",
    state: "active",
    monthly_value_sar: 4999,
    renewal_date: "2026-06-15",
    days_until_renewal: 15,
    auto_renew: true,
  },
  {
    sub_id: "SUB-003",
    client_id: "CLT-003",
    company_ar: "شركة سفا للخدمات اللوجستية",
    company_en: "Safa Logistics Co",
    tier: "managed_ops_essential",
    state: "active",
    monthly_value_sar: 2999,
    renewal_date: "2026-06-20",
    days_until_renewal: 20,
    auto_renew: false,
  },
  {
    sub_id: "SUB-004",
    client_id: "CLT-004",
    company_ar: "تمكين الصحية",
    company_en: "Tamkeen Health Tech",
    tier: "data_pack",
    state: "active",
    monthly_value_sar: 1500,
    renewal_date: "2026-07-01",
    days_until_renewal: 31,
    auto_renew: true,
  },
  {
    sub_id: "SUB-005",
    client_id: "CLT-005",
    company_ar: "شركة جازان للتصنيع",
    company_en: "Jazan Manufacturing Co",
    tier: "managed_ops_professional",
    state: "paused",
    monthly_value_sar: 3999,
    renewal_date: "2026-08-01",
    days_until_renewal: 62,
    auto_renew: false,
  },
  {
    sub_id: "SUB-006",
    client_id: "CLT-006",
    company_ar: "الوافي للتمويل",
    company_en: "Al-Wafi Finance",
    tier: "sprint",
    state: "cancelled",
    monthly_value_sar: 499,
    renewal_date: "2026-03-15",
    days_until_renewal: 0,
    auto_renew: false,
  },
];

// ---------------------------------------------------------------------------
// Tier display labels
// ---------------------------------------------------------------------------

const TIER_LABELS: Record<TierKey, { ar: string; en: string }> = {
  sprint: { ar: "سبرينت", en: "Sprint" },
  data_pack: { ar: "حزمة البيانات", en: "Data Pack" },
  managed_ops_essential: { ar: "العمليات المُدارة — أساسي", en: "Managed Ops Essential" },
  managed_ops_professional: { ar: "العمليات المُدارة — احترافي", en: "Managed Ops Pro" },
  managed_ops_enterprise: { ar: "العمليات المُدارة — مؤسسي", en: "Managed Ops Enterprise" },
  custom_ai: { ar: "ذكاء اصطناعي مخصص", en: "Custom AI" },
};

// ---------------------------------------------------------------------------
// State badge styling
// ---------------------------------------------------------------------------

const STATE_STYLES: Record<SubState, { bg: string; text: string; ar: string; en: string }> = {
  active: { bg: "bg-emerald-100", text: "text-emerald-800", ar: "نشط", en: "Active" },
  paused: { bg: "bg-amber-100", text: "text-amber-800", ar: "موقوف مؤقتاً", en: "Paused" },
  cancelled: { bg: "bg-red-100", text: "text-red-800", ar: "ملغى", en: "Cancelled" },
  reactivated: { bg: "bg-blue-100", text: "text-blue-800", ar: "مُعاد تفعيله", en: "Reactivated" },
  trial: { bg: "bg-gray-100", text: "text-gray-700", ar: "تجريبي", en: "Trial" },
};

// ---------------------------------------------------------------------------
// Modal component
// ---------------------------------------------------------------------------

function ConfirmModal({
  action,
  companyAr,
  companyEn,
  onClose,
  isAr,
}: {
  action: string;
  companyAr: string;
  companyEn: string;
  onClose: () => void;
  isAr: boolean;
}) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white rounded-xl shadow-xl border border-gray-200 p-6 max-w-md w-full mx-4">
        <h3 className="text-base font-bold text-gray-900 mb-2">
          {isAr ? "تأكيد الإجراء" : "Action Confirmation"}
        </h3>
        <p className="text-sm text-gray-700 mb-1">
          {isAr
            ? `${action} — ${companyAr}`
            : `${action} — ${companyEn}`}
        </p>
        <p className="text-sm font-semibold text-amber-700 bg-amber-50 border border-amber-200 rounded-lg p-3 mt-3">
          {isAr
            ? "هذا الإجراء يتطلب موافقة المؤسس قبل التنفيذ."
            : "This action requires founder approval before execution."}
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

export default function SubscriptionManager({ locale }: SubscriptionManagerProps) {
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  const [filterTier, setFilterTier] = useState<string>("all");
  const [filterState, setFilterState] = useState<string>("all");
  const [modal, setModal] = useState<{
    action: string;
    companyAr: string;
    companyEn: string;
  } | null>(null);

  // Derived summary values
  const activeSubs = SUBSCRIPTIONS.filter((s) => s.state === "active");
  const totalMrr = activeSubs.reduce((sum, s) => sum + s.monthly_value_sar, 0);
  const expiringIn30 = activeSubs.filter((s) => s.days_until_renewal <= 30).length;

  // Filtering
  const filtered = SUBSCRIPTIONS.filter((s) => {
    const tierMatch = filterTier === "all" || s.tier === filterTier;
    const stateMatch = filterState === "all" || s.state === filterState;
    return tierMatch && stateMatch;
  });

  // Tier options for filter dropdown
  const tierOptions: TierKey[] = [
    "sprint",
    "data_pack",
    "managed_ops_essential",
    "managed_ops_professional",
    "managed_ops_enterprise",
    "custom_ai",
  ];
  const stateOptions: SubState[] = ["active", "paused", "cancelled", "reactivated", "trial"];

  function openModal(action: string, sub: Subscription) {
    setModal({ action, companyAr: sub.company_ar, companyEn: sub.company_en });
  }

  function canPause(state: SubState) {
    return state === "active";
  }
  function canCancel(state: SubState) {
    return state !== "cancelled";
  }
  function canReactivate(state: SubState) {
    return state === "paused" || state === "cancelled";
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6" dir={dir}>
      {/* Page heading */}
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900">
          {isAr ? "إدارة الاشتراكات" : "Subscription Manager"}
        </h1>
        <p className="text-sm text-gray-500 mt-0.5">
          {isAr
            ? "دورة حياة الاشتراكات — الحالة والتجديد والإجراءات"
            : "Subscription lifecycle — state, renewal, and actions"}
        </p>
      </div>

      {/* Summary bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "الاشتراكات النشطة" : "Active Subscriptions"}
          </p>
          <p className="text-3xl font-extrabold text-gray-900 tabular-nums">
            {activeSubs.length}
          </p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "الإيراد الشهري المتكرر" : "Monthly Recurring Revenue"}
          </p>
          <p className="text-3xl font-extrabold text-emerald-700 tabular-nums">
            {totalMrr.toLocaleString("ar-SA")}{" "}
            <span className="text-base font-semibold text-gray-500">
              {isAr ? "ر.س" : "SAR"}
            </span>
          </p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "تنتهي خلال 30 يوماً" : "Expiring in 30 Days"}
          </p>
          <p
            className={`text-3xl font-extrabold tabular-nums ${
              expiringIn30 > 0 ? "text-amber-600" : "text-gray-900"
            }`}
          >
            {expiringIn30}
          </p>
        </div>
      </div>

      {/* Filter bar */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex flex-wrap gap-4 items-center">
        <div className="flex items-center gap-2">
          <label
            htmlFor="filter-tier"
            className="text-sm font-semibold text-gray-700 whitespace-nowrap"
          >
            {isAr ? "الباقة" : "Tier"}
          </label>
          <select
            id="filter-tier"
            value={filterTier}
            onChange={(e) => setFilterTier(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">{isAr ? "الكل" : "All"}</option>
            {tierOptions.map((t) => (
              <option key={t} value={t}>
                {isAr ? TIER_LABELS[t].ar : TIER_LABELS[t].en}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-2">
          <label
            htmlFor="filter-state"
            className="text-sm font-semibold text-gray-700 whitespace-nowrap"
          >
            {isAr ? "الحالة" : "State"}
          </label>
          <select
            id="filter-state"
            value={filterState}
            onChange={(e) => setFilterState(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">{isAr ? "الكل" : "All"}</option>
            {stateOptions.map((s) => (
              <option key={s} value={s}>
                {isAr ? STATE_STYLES[s].ar : STATE_STYLES[s].en}
              </option>
            ))}
          </select>
        </div>
        <p className="text-xs text-gray-400 ms-auto">
          {isAr
            ? `${filtered.length} نتيجة`
            : `${filtered.length} result${filtered.length !== 1 ? "s" : ""}`}
        </p>
      </div>

      {/* Subscription table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
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
                {isAr ? "الحالة" : "State"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "القيمة الشهرية" : "Monthly Value"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "تاريخ التجديد" : "Renewal Date"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "أيام حتى التجديد" : "Days Until Renewal"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "تجديد تلقائي" : "Auto-Renew"}
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
              filtered.map((sub, idx) => {
                const stateStyle = STATE_STYLES[sub.state];
                const tier = TIER_LABELS[sub.tier];
                const isEven = idx % 2 === 0;
                return (
                  <tr
                    key={sub.sub_id}
                    className={`border-b border-gray-50 ${isEven ? "bg-white" : "bg-gray-50/50"} hover:bg-blue-50/30 transition-colors`}
                  >
                    <td className="px-4 py-3">
                      <p className="font-semibold text-gray-900">
                        {isAr ? sub.company_ar : sub.company_en}
                      </p>
                      <p className="text-xs text-gray-400 font-mono">
                        {sub.sub_id}
                      </p>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-gray-700">
                      {isAr ? tier.ar : tier.en}
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full ${stateStyle.bg} ${stateStyle.text}`}
                      >
                        {isAr ? stateStyle.ar : stateStyle.en}
                      </span>
                    </td>
                    <td className="px-4 py-3 tabular-nums font-semibold text-gray-800 whitespace-nowrap">
                      {sub.monthly_value_sar.toLocaleString("ar-SA")}{" "}
                      <span className="font-normal text-gray-500">
                        {isAr ? "ر.س" : "SAR"}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-700 whitespace-nowrap font-mono text-xs">
                      {sub.renewal_date}
                    </td>
                    <td className="px-4 py-3 tabular-nums text-center">
                      <span
                        className={`font-bold ${
                          sub.days_until_renewal <= 30 && sub.state === "active"
                            ? "text-amber-600"
                            : "text-gray-700"
                        }`}
                      >
                        {sub.state === "cancelled" ? "—" : sub.days_until_renewal}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      {sub.auto_renew ? (
                        <span className="text-emerald-600 font-semibold text-xs">
                          {isAr ? "نعم" : "Yes"}
                        </span>
                      ) : (
                        <span className="text-gray-400 text-xs">
                          {isAr ? "لا" : "No"}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2 flex-wrap">
                        <button
                          type="button"
                          disabled={!canPause(sub.state)}
                          onClick={() =>
                            openModal(isAr ? "إيقاف مؤقت" : "Pause", sub)
                          }
                          className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-amber-300 text-amber-700 bg-amber-50 hover:bg-amber-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
                        >
                          {isAr ? "إيقاف" : "Pause"}
                        </button>
                        <button
                          type="button"
                          disabled={!canCancel(sub.state)}
                          onClick={() =>
                            openModal(isAr ? "إلغاء" : "Cancel", sub)
                          }
                          className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-red-300 text-red-700 bg-red-50 hover:bg-red-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
                        >
                          {isAr ? "إلغاء" : "Cancel"}
                        </button>
                        <button
                          type="button"
                          disabled={!canReactivate(sub.state)}
                          onClick={() =>
                            openModal(isAr ? "إعادة تفعيل" : "Reactivate", sub)
                          }
                          className="text-xs font-semibold px-2.5 py-1 rounded-lg border border-blue-300 text-blue-700 bg-blue-50 hover:bg-blue-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
                        >
                          {isAr ? "إعادة تفعيل" : "Reactivate"}
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

      {/* Confirmation modal */}
      {modal !== null && (
        <ConfirmModal
          action={modal.action}
          companyAr={modal.companyAr}
          companyEn={modal.companyEn}
          onClose={() => setModal(null)}
          isAr={isAr}
        />
      )}
    </div>
  );
}
