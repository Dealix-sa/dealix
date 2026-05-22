"use client";

import { useState, useCallback, useEffect } from "react";
import { useLocale } from "next-intl";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? ""
    : "";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "https://api.dealix.me";

type DealStage =
  | "prospect"
  | "qualified"
  | "proposal"
  | "negotiation"
  | "verbal";

const DEAL_STAGES: DealStage[] = [
  "prospect",
  "qualified",
  "proposal",
  "negotiation",
  "verbal",
];

const STAGE_LABELS_AR: Record<DealStage, string> = {
  prospect: "عميل محتمل",
  qualified: "مؤهل",
  proposal: "عرض",
  negotiation: "تفاوض",
  verbal: "موافقة شفهية",
};

const STAGE_LABELS_EN: Record<DealStage, string> = {
  prospect: "Prospect",
  qualified: "Qualified",
  proposal: "Proposal",
  negotiation: "Negotiation",
  verbal: "Verbal Commit",
};

type DealRow = {
  company_name: string;
  stage: DealStage;
  value_sar: number;
  days_in_stage: number;
};

type ForecastBand = {
  worst_sar: number;
  likely_sar: number;
  best_sar: number;
  confidence: number;
};

type ForecastResult = {
  customer_id: string;
  horizon_days: number;
  forecast: ForecastBand;
  deal_count: number;
  is_estimate: boolean;
  governance_decision: string;
};

type StageHealth = {
  stage: DealStage;
  win_probability: number;
  deal_count: number;
  total_value_sar: number;
};

type PipelineHealthResult = {
  stages: StageHealth[];
  total_pipeline_sar: number;
  weighted_pipeline_sar: number;
  is_estimate: boolean;
  governance_decision: string;
};

type ScenarioResult = {
  horizon_days: number;
  likely_sar: number;
  best_sar: number;
  worst_sar: number;
  confidence: number;
};

type ScenariosResult = {
  customer_id: string;
  scenarios: ScenarioResult[];
  is_estimate: boolean;
  governance_decision: string;
};

function fmt(n: number): string {
  return new Intl.NumberFormat("ar-SA", {
    style: "currency",
    currency: "SAR",
    maximumFractionDigits: 0,
  }).format(n);
}

function probColor(p: number): string {
  if (p >= 0.6) return "text-green-400";
  if (p >= 0.3) return "text-yellow-400";
  return "text-red-400";
}

function probBg(p: number): string {
  if (p >= 0.6) return "bg-green-400/10 border-green-400/30 text-green-400";
  if (p >= 0.3) return "bg-yellow-400/10 border-yellow-400/30 text-yellow-400";
  return "bg-red-400/10 border-red-400/30 text-red-400";
}

const HORIZON_OPTIONS = [30, 60, 90] as const;
type Horizon = (typeof HORIZON_OPTIONS)[number];

export function OpsRevenueForecastDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";

  // Forecast form state
  const [customerId, setCustomerId] = useState("");
  const [horizon, setHorizon] = useState<Horizon>(90);
  const [deals, setDeals] = useState<DealRow[]>([
    { company_name: "", stage: "qualified", value_sar: 0, days_in_stage: 0 },
  ]);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [forecastResult, setForecastResult] = useState<ForecastResult | null>(null);
  const [forecastError, setForecastError] = useState<string | null>(null);

  // Pipeline health state
  const [healthResult, setHealthResult] = useState<PipelineHealthResult | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState<string | null>(null);

  // Scenarios state
  const [scenariosLoading, setScenariosLoading] = useState(false);
  const [scenariosResult, setScenariosResult] = useState<ScenariosResult | null>(null);
  const [scenariosError, setScenariosError] = useState<string | null>(null);

  const fetchPipelineHealth = useCallback(async () => {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const res = await fetch(
        `${API_BASE}/api/v1/revenue-forecast/pipeline-health`,
        { headers: { "X-Admin-API-Key": ADMIN_KEY } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setHealthResult(await res.json());
    } catch (e: unknown) {
      setHealthError(
        e instanceof Error
          ? e.message
          : isAr
          ? "تعذّر تحميل صحة الخط"
          : "Failed to load pipeline health"
      );
    } finally {
      setHealthLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    fetchPipelineHealth();
  }, [fetchPipelineHealth]);

  const addDealRow = useCallback(() => {
    setDeals((prev) => [
      ...prev,
      { company_name: "", stage: "qualified", value_sar: 0, days_in_stage: 0 },
    ]);
  }, []);

  const removeDealRow = useCallback((index: number) => {
    setDeals((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const updateDealRow = useCallback(
    (index: number, field: keyof DealRow, value: string | number) => {
      setDeals((prev) =>
        prev.map((row, i) =>
          i === index ? { ...row, [field]: value } : row
        )
      );
    },
    []
  );

  const handleForecast = useCallback(async () => {
    if (!customerId.trim() || deals.length === 0) return;
    setForecastLoading(true);
    setForecastResult(null);
    setForecastError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/revenue-forecast/forecast`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Admin-API-Key": ADMIN_KEY,
        },
        body: JSON.stringify({
          customer_id: customerId,
          horizon_days: horizon,
          deals: deals.filter((d) => d.company_name.trim() && d.value_sar > 0),
        }),
      });
      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(
          d?.detail?.message_ar ??
            d?.detail?.message ??
            `HTTP ${res.status}`
        );
      }
      setForecastResult(await res.json());
    } catch (e: unknown) {
      setForecastError(
        e instanceof Error ? e.message : isAr ? "حدث خطأ" : "An error occurred"
      );
    } finally {
      setForecastLoading(false);
    }
  }, [customerId, horizon, deals, isAr]);

  const handleRunScenarios = useCallback(async () => {
    if (!customerId.trim()) return;
    setScenariosLoading(true);
    setScenariosResult(null);
    setScenariosError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/revenue-forecast/scenarios`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Admin-API-Key": ADMIN_KEY,
        },
        body: JSON.stringify({
          customer_id: customerId,
          deals: deals.filter((d) => d.company_name.trim() && d.value_sar > 0),
        }),
      });
      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(
          d?.detail?.message_ar ??
            d?.detail?.message ??
            `HTTP ${res.status}`
        );
      }
      setScenariosResult(await res.json());
    } catch (e: unknown) {
      setScenariosError(
        e instanceof Error ? e.message : isAr ? "حدث خطأ" : "An error occurred"
      );
    } finally {
      setScenariosLoading(false);
    }
  }, [customerId, deals, isAr]);

  const inputCls =
    "bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm focus:outline-none focus:ring-1 focus:ring-amber-500";
  const labelCls = "block text-xs text-zinc-400 mb-1";

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <div>
        <h1 className="text-xl font-bold text-amber-400">
          {isAr ? "توقعات الإيرادات" : "Revenue Forecast OS"}
        </h1>
      </div>

      {/* Forecast Scenarios */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <h2 className="text-base font-semibold text-amber-400 mb-4">
          {isAr ? "توقع السيناريوهات" : "Forecast Scenarios"}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className={labelCls}>
              {isAr ? "معرف العميل" : "Customer ID"}
            </label>
            <input
              className={`${inputCls} w-full`}
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
              placeholder={isAr ? "مثال: cust_001" : "e.g. cust_001"}
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "الأفق الزمني (يوم)" : "Horizon (days)"}
            </label>
            <select
              className={`${inputCls} w-full`}
              value={horizon}
              onChange={(e) => setHorizon(parseInt(e.target.value, 10) as Horizon)}
            >
              {HORIZON_OPTIONS.map((h) => (
                <option key={h} value={h}>
                  {h} {isAr ? "يوم" : "days"}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Deal rows */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs text-zinc-400">
              {isAr ? "صفوف الصفقات" : "Deal rows"}
            </p>
            <button
              onClick={addDealRow}
              className="text-xs text-amber-400 hover:text-amber-300 transition-colors"
            >
              + {isAr ? "إضافة صفقة" : "Add deal"}
            </button>
          </div>
          <div className="space-y-2">
            {deals.map((row, i) => (
              <div
                key={i}
                className="grid grid-cols-1 sm:grid-cols-4 gap-2 bg-zinc-800/50 rounded-lg p-3"
              >
                <div>
                  <label className={labelCls}>
                    {isAr ? "اسم الشركة" : "Company"}
                  </label>
                  <input
                    className={`${inputCls} w-full`}
                    value={row.company_name}
                    onChange={(e) =>
                      updateDealRow(i, "company_name", e.target.value)
                    }
                    placeholder={isAr ? "الشركة" : "Company name"}
                  />
                </div>
                <div>
                  <label className={labelCls}>
                    {isAr ? "المرحلة" : "Stage"}
                  </label>
                  <select
                    className={`${inputCls} w-full`}
                    value={row.stage}
                    onChange={(e) =>
                      updateDealRow(i, "stage", e.target.value as DealStage)
                    }
                  >
                    {DEAL_STAGES.map((s) => (
                      <option key={s} value={s}>
                        {isAr ? STAGE_LABELS_AR[s] : STAGE_LABELS_EN[s]}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className={labelCls}>
                    {isAr ? "القيمة (ريال)" : "Value (SAR)"}
                  </label>
                  <input
                    type="number"
                    min={0}
                    className={`${inputCls} w-full`}
                    value={row.value_sar || ""}
                    onChange={(e) =>
                      updateDealRow(
                        i,
                        "value_sar",
                        parseFloat(e.target.value) || 0
                      )
                    }
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className={labelCls}>
                    {isAr ? "أيام في المرحلة" : "Days in stage"}
                  </label>
                  <div className="flex gap-1">
                    <input
                      type="number"
                      min={0}
                      className={`${inputCls} flex-1`}
                      value={row.days_in_stage || ""}
                      onChange={(e) =>
                        updateDealRow(
                          i,
                          "days_in_stage",
                          parseInt(e.target.value, 10) || 0
                        )
                      }
                      placeholder="0"
                    />
                    {deals.length > 1 && (
                      <button
                        onClick={() => removeDealRow(i)}
                        className="text-zinc-500 hover:text-red-400 text-xs px-2 transition-colors"
                        title={isAr ? "حذف" : "Remove"}
                      >
                        x
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={handleForecast}
          disabled={forecastLoading || !customerId.trim()}
          className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold px-5 py-2 rounded text-sm transition-colors"
        >
          {forecastLoading
            ? isAr
              ? "جارٍ التوقع..."
              : "Forecasting..."
            : isAr
            ? "احسب التوقع"
            : "Run Forecast"}
        </button>

        {forecastError && (
          <p className="mt-3 text-red-400 text-sm">{forecastError}</p>
        )}

        {forecastResult && (
          <div className="mt-5 p-4 bg-zinc-800 rounded-lg border border-amber-500/30">
            <div className="flex items-center gap-2 mb-4">
              <h3 className="text-white font-semibold text-sm">
                {isAr
                  ? `توقع ${forecastResult.horizon_days} يوم`
                  : `${forecastResult.horizon_days}-day forecast`}
              </h3>
              <span className="px-2 py-0.5 rounded border bg-amber-500/10 border-amber-500/30 text-amber-400 text-xs">
                {isAr ? "تقدير" : "Estimate"} —{" "}
                {Math.round(forecastResult.forecast.confidence * 100)}%{" "}
                {isAr ? "ثقة" : "confidence"}
              </span>
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-zinc-900 rounded-lg p-3 border border-red-500/20">
                <p className="text-xs text-zinc-400 mb-1">
                  {isAr ? "الأسوأ" : "Worst"}
                </p>
                <p className="text-lg font-bold text-red-400">
                  {fmt(forecastResult.forecast.worst_sar)}
                </p>
              </div>
              <div className="bg-zinc-900 rounded-lg p-3 border border-amber-500/30">
                <p className="text-xs text-zinc-400 mb-1">
                  {isAr ? "المتوقع" : "Likely"}
                </p>
                <p className="text-lg font-bold text-amber-400">
                  {fmt(forecastResult.forecast.likely_sar)}
                </p>
              </div>
              <div className="bg-zinc-900 rounded-lg p-3 border border-green-500/20">
                <p className="text-xs text-zinc-400 mb-1">
                  {isAr ? "الأفضل" : "Best"}
                </p>
                <p className="text-lg font-bold text-green-400">
                  {fmt(forecastResult.forecast.best_sar)}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Pipeline Health */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-amber-400">
            {isAr ? "صحة خط الصفقات" : "Pipeline Health"}
          </h2>
          <button
            onClick={fetchPipelineHealth}
            disabled={healthLoading}
            className="text-xs text-zinc-400 hover:text-amber-400 transition-colors disabled:opacity-50"
          >
            {isAr ? "تحديث" : "Refresh"}
          </button>
        </div>

        {healthError && (
          <div className="bg-red-950 border border-red-800 rounded-lg p-3 mb-4">
            <p className="text-red-300 text-sm">{healthError}</p>
          </div>
        )}

        {healthLoading ? (
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="h-10 bg-zinc-800 rounded-lg animate-pulse"
              />
            ))}
          </div>
        ) : healthResult ? (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-zinc-800">
                    <th className="text-left text-zinc-400 pb-2 font-normal">
                      {isAr ? "المرحلة" : "Stage"}
                    </th>
                    <th className="text-right text-zinc-400 pb-2 font-normal">
                      {isAr ? "احتمالية الفوز" : "Win Probability"}
                    </th>
                    <th className="text-right text-zinc-400 pb-2 font-normal">
                      {isAr ? "عدد الصفقات" : "Deals"}
                    </th>
                    <th className="text-right text-zinc-400 pb-2 font-normal">
                      {isAr ? "القيمة الإجمالية" : "Total Value"}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {healthResult.stages.map((s) => (
                    <tr
                      key={s.stage}
                      className="border-b border-zinc-800/50"
                    >
                      <td className="py-2 text-white">
                        {isAr
                          ? STAGE_LABELS_AR[s.stage] ?? s.stage
                          : STAGE_LABELS_EN[s.stage] ?? s.stage}
                      </td>
                      <td className="py-2 text-right">
                        <span
                          className={`px-2 py-0.5 rounded border text-xs font-semibold ${probBg(s.win_probability)}`}
                        >
                          {Math.round(s.win_probability * 100)}%
                        </span>
                      </td>
                      <td className="py-2 text-right text-zinc-300">
                        {s.deal_count}
                      </td>
                      <td
                        className={`py-2 text-right font-medium ${probColor(s.win_probability)}`}
                      >
                        {fmt(s.total_value_sar)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-3">
              <div className="bg-zinc-800/50 rounded-lg p-3">
                <p className="text-xs text-zinc-400 mb-1">
                  {isAr ? "إجمالي الخط" : "Total Pipeline"}
                </p>
                <p className="text-lg font-bold text-amber-400">
                  {fmt(healthResult.total_pipeline_sar)}
                </p>
              </div>
              <div className="bg-zinc-800/50 rounded-lg p-3">
                <p className="text-xs text-zinc-400 mb-1">
                  {isAr ? "الخط المرجّح" : "Weighted Pipeline"}
                </p>
                <p className="text-lg font-bold text-green-400">
                  {fmt(healthResult.weighted_pipeline_sar)}
                </p>
              </div>
            </div>
          </>
        ) : null}
      </div>

      {/* 3-Horizon Comparison */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <h2 className="text-base font-semibold text-amber-400 mb-4">
          {isAr ? "مقارنة الأفق الثلاثي" : "3-Horizon Comparison"}
        </h2>

        <button
          onClick={handleRunScenarios}
          disabled={scenariosLoading || !customerId.trim()}
          className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold px-5 py-2 rounded text-sm transition-colors mb-4"
        >
          {scenariosLoading
            ? isAr
              ? "جارٍ الحساب..."
              : "Computing..."
            : isAr
            ? "تشغيل كل السيناريوهات"
            : "Run All Scenarios"}
        </button>

        {!customerId.trim() && (
          <p className="text-xs text-zinc-500 mb-3">
            {isAr
              ? "أدخل معرف العميل أولاً"
              : "Enter a customer ID above first"}
          </p>
        )}

        {scenariosError && (
          <p className="text-red-400 text-sm mb-3">{scenariosError}</p>
        )}

        {scenariosResult && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {scenariosResult.scenarios.map((sc) => (
              <div
                key={sc.horizon_days}
                className="bg-zinc-800/50 border border-zinc-700 rounded-xl p-4"
              >
                <p className="text-xs text-zinc-400 mb-3">
                  {sc.horizon_days} {isAr ? "يوم" : "days"}
                </p>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-zinc-500">
                      {isAr ? "الأسوأ" : "Worst"}
                    </span>
                    <span className="text-sm font-medium text-red-400">
                      {fmt(sc.worst_sar)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-zinc-500">
                      {isAr ? "المتوقع" : "Likely"}
                    </span>
                    <span className="text-base font-bold text-amber-400">
                      {fmt(sc.likely_sar)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-zinc-500">
                      {isAr ? "الأفضل" : "Best"}
                    </span>
                    <span className="text-sm font-medium text-green-400">
                      {fmt(sc.best_sar)}
                    </span>
                  </div>
                </div>
                <div className="mt-3 pt-2 border-t border-zinc-700">
                  <span className="text-xs text-zinc-500">
                    {isAr ? "الثقة:" : "Confidence:"}{" "}
                    <span className="text-amber-400">
                      {Math.round(sc.confidence * 100)}%
                    </span>
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-4 bg-zinc-800/30 border border-zinc-700/50 rounded-lg p-3">
          <p className="text-xs text-zinc-500">
            {isAr
              ? "is_estimate=True — تقديرات مرجّحة باحتمالية. تتطلب مراجعة بشرية قبل أي قرار تجاري."
              : "is_estimate=True — probability-weighted estimates. Require human review before any commercial decision."}
          </p>
        </div>
      </div>

      <p className="text-xs text-zinc-500 border-t border-zinc-800 pt-3">
        {isAr
          ? "is_estimate=True — جميع النتائج تقديرية وتستلزم مراجعة بشرية قبل أي إجراء خارجي."
          : "is_estimate=True — All results are estimates and require human review before any external action."}
      </p>
    </div>
  );
}
