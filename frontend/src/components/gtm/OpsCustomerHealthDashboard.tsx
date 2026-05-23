"use client";

import { useState, useCallback } from "react";
import { useLocale } from "next-intl";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? ""
    : "";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me";

const API_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_API_KEY ?? ""
    : "";

type ChurnBand = "safe" | "watch" | "at_risk" | "critical";

type ChurnResult = {
  customer_id: string;
  score: number;
  band: ChurnBand;
  drivers: string[];
  recommended_action_ar: string;
  confidence: number;
  is_estimate: boolean;
  governance_decision: string;
};

type PlaybookResult = {
  customer_id: string;
  playbook: {
    priority: string;
    actions_ar: string[];
    actions_en: string[];
    governance_decision: string;
  };
  is_estimate: boolean;
};

type ExpansionResult = {
  customer_id: string;
  expansion_score: number;
  band: string;
  expansion_hint_ar: string;
  governance_decision: string;
};

type FormData = {
  customer_id: string;
  days_since_last_login: number;
  monthly_engagement_drop_pct: number;
  support_tickets_open: number;
  billing_failures_last_90d: number;
  nps: number | null;
  months_as_customer: number;
};

const BAND_COLORS: Record<ChurnBand, string> = {
  safe: "text-green-400",
  watch: "text-yellow-400",
  at_risk: "text-orange-400",
  critical: "text-red-400",
};

const BAND_BG: Record<ChurnBand, string> = {
  safe: "bg-green-400/10 border-green-400/30 text-green-400",
  watch: "bg-yellow-400/10 border-yellow-400/30 text-yellow-400",
  at_risk: "bg-orange-400/10 border-orange-400/30 text-orange-400",
  critical: "bg-red-400/10 border-red-400/30 text-red-400",
};

const BAND_LABEL_AR: Record<ChurnBand, string> = {
  safe: "آمن",
  watch: "مراقبة",
  at_risk: "في خطر",
  critical: "حرج",
};

const PRIORITY_COLORS: Record<string, string> = {
  P0: "bg-red-500/20 border-red-500/40 text-red-300",
  P1: "bg-orange-500/20 border-orange-500/40 text-orange-300",
  P2: "bg-yellow-500/20 border-yellow-500/40 text-yellow-300",
  P3: "bg-blue-500/20 border-blue-500/40 text-blue-300",
};

export function OpsCustomerHealthDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [form, setForm] = useState<FormData>({
    customer_id: "",
    days_since_last_login: 0,
    monthly_engagement_drop_pct: 0.0,
    support_tickets_open: 0,
    billing_failures_last_90d: 0,
    nps: null,
    months_as_customer: 6,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [churnResult, setChurnResult] = useState<ChurnResult | null>(null);
  const [playbookResult, setPlaybookResult] = useState<PlaybookResult | null>(null);
  const [expansionResult, setExpansionResult] = useState<ExpansionResult | null>(null);

  const handleChange = useCallback(
    (field: keyof FormData, value: string | number | null) => {
      setForm((prev) => ({ ...prev, [field]: value }));
    },
    []
  );

  const handleAnalyze = useCallback(async () => {
    if (!form.customer_id.trim()) return;
    setLoading(true);
    setError(null);
    setChurnResult(null);
    setPlaybookResult(null);
    setExpansionResult(null);

    const payload = {
      customer_id: form.customer_id,
      days_since_last_login: form.days_since_last_login,
      monthly_engagement_drop_pct: form.monthly_engagement_drop_pct,
      support_tickets_open: form.support_tickets_open,
      billing_failures_last_90d: form.billing_failures_last_90d,
      nps: form.nps,
      months_as_customer: form.months_as_customer,
    };

    const headers = {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
      "X-Admin-API-Key": ADMIN_KEY,
    };

    try {
      const [churnRes, playbookRes, expansionRes] = await Promise.all([
        fetch(`${API_BASE}/api/v1/customer-health/churn-predict`, {
          method: "POST",
          headers,
          body: JSON.stringify(payload),
        }),
        fetch(`${API_BASE}/api/v1/customer-health/intervention-playbook`, {
          method: "POST",
          headers,
          body: JSON.stringify(payload),
        }),
        fetch(`${API_BASE}/api/v1/customer-health/expansion-signals`, {
          method: "POST",
          headers,
          body: JSON.stringify(payload),
        }),
      ]);

      if (!churnRes.ok) {
        const d = await churnRes.json().catch(() => ({}));
        throw new Error(
          d?.detail?.message_ar ?? d?.detail?.message ?? `HTTP ${churnRes.status}`
        );
      }

      const [churn, playbook, expansion] = await Promise.all([
        churnRes.json() as Promise<ChurnResult>,
        playbookRes.ok ? (playbookRes.json() as Promise<PlaybookResult>) : Promise.resolve(null),
        expansionRes.ok ? (expansionRes.json() as Promise<ExpansionResult>) : Promise.resolve(null),
      ]);

      setChurnResult(churn);
      if (playbook) setPlaybookResult(playbook);
      if (expansion) setExpansionResult(expansion);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : (isAr ? "حدث خطأ" : "An error occurred"));
    } finally {
      setLoading(false);
    }
  }, [form, isAr]);

  const inputCls =
    "w-full bg-gray-800/50 border border-gray-600/50 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-yellow-500/50";
  const labelCls = "block text-xs text-gray-400 mb-1";

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold text-yellow-400/80">
          {isAr ? "نظام صحة العملاء" : "Customer Health OS"}
        </h1>
      </div>

      {/* Churn Predict form */}
      <div className="bg-gray-900/50 border border-gray-700/50 rounded-xl p-6 backdrop-blur-sm">
        <h2 className="text-base font-semibold text-yellow-400/80 mb-4">
          {isAr ? "توقع التخبط" : "Churn Prediction"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
          <div>
            <label className={labelCls}>
              {isAr ? "معرف العميل" : "Customer ID"}
            </label>
            <input
              className={inputCls}
              value={form.customer_id}
              onChange={(e) => handleChange("customer_id", e.target.value)}
              placeholder={isAr ? "مثال: cust_001" : "e.g. cust_001"}
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "أيام منذ آخر دخول" : "Days Since Last Login"}
            </label>
            <input
              type="number"
              min={0}
              className={inputCls}
              value={form.days_since_last_login}
              onChange={(e) =>
                handleChange("days_since_last_login", parseInt(e.target.value, 10) || 0)
              }
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "انخفاض الاستخدام الشهري (0.0–1.0)" : "Monthly Engagement Drop (0.0–1.0)"}
            </label>
            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              className={inputCls}
              value={form.monthly_engagement_drop_pct}
              onChange={(e) =>
                handleChange(
                  "monthly_engagement_drop_pct",
                  parseFloat(e.target.value) || 0
                )
              }
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "تذاكر الدعم المفتوحة" : "Open Support Tickets"}
            </label>
            <input
              type="number"
              min={0}
              className={inputCls}
              value={form.support_tickets_open}
              onChange={(e) =>
                handleChange("support_tickets_open", parseInt(e.target.value, 10) || 0)
              }
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "فشل الدفع (آخر 90 يوم)" : "Billing Failures (Last 90d)"}
            </label>
            <input
              type="number"
              min={0}
              className={inputCls}
              value={form.billing_failures_last_90d}
              onChange={(e) =>
                handleChange(
                  "billing_failures_last_90d",
                  parseInt(e.target.value, 10) || 0
                )
              }
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "NPS (0–10، اختياري)" : "NPS (0–10, optional)"}
            </label>
            <input
              type="number"
              min={0}
              max={10}
              className={inputCls}
              value={form.nps ?? ""}
              placeholder={isAr ? "اتركه فارغاً إذا غير معروف" : "Leave blank if unknown"}
              onChange={(e) => {
                const v = e.target.value;
                handleChange("nps", v === "" ? null : parseInt(v, 10));
              }}
            />
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "مدة العميل (أشهر)" : "Months as Customer"}
            </label>
            <input
              type="number"
              min={0}
              className={inputCls}
              value={form.months_as_customer}
              onChange={(e) =>
                handleChange("months_as_customer", parseInt(e.target.value, 10) || 6)
              }
            />
          </div>
        </div>
        <button
          onClick={handleAnalyze}
          disabled={loading || !form.customer_id.trim()}
          className="bg-yellow-500 text-black font-semibold px-4 py-2 rounded-lg hover:bg-yellow-400 transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading
            ? (isAr ? "جارٍ التحليل..." : "Analyzing...")
            : (isAr ? "تحليل الصحة" : "Analyze Health")}
        </button>

        {error && (
          <p className="mt-3 text-red-400 text-sm">{error}</p>
        )}
      </div>

      {/* Results panel */}
      {churnResult && (
        <div className="bg-gray-900/50 border border-gray-700/50 rounded-xl p-6 backdrop-blur-sm">
          <h2 className="text-base font-semibold text-yellow-400/80 mb-4">
            {isAr ? "نسبة خطر التخبط" : "Churn Risk Score"}
          </h2>
          <div className="flex items-center gap-4 mb-4">
            <span
              className={`text-4xl font-bold ${BAND_COLORS[churnResult.band as ChurnBand] ?? "text-white"}`}
            >
              {Math.round(churnResult.score * 100)}%
            </span>
            <span
              className={`px-3 py-1 rounded-full border text-sm font-medium ${
                BAND_BG[churnResult.band as ChurnBand] ?? "bg-gray-800 text-gray-300"
              }`}
            >
              {isAr
                ? BAND_LABEL_AR[churnResult.band as ChurnBand] ?? churnResult.band
                : churnResult.band}
            </span>
          </div>

          {churnResult.drivers.length > 0 && (
            <div className="mb-4">
              <p className="text-xs text-gray-400 mb-2">
                {isAr ? "العوامل المؤثرة" : "Drivers"}
              </p>
              <ul className="space-y-1">
                {churnResult.drivers.map((d, i) => (
                  <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                    <span className="text-yellow-400 mt-0.5">-</span>
                    <span>{d}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {churnResult.recommended_action_ar && (
            <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-600/30">
              <p className="text-xs text-gray-400 mb-1">
                {isAr ? "الإجراء الموصى به" : "Recommended Action"}
              </p>
              <p className="text-sm text-white">{churnResult.recommended_action_ar}</p>
            </div>
          )}
        </div>
      )}

      {/* Intervention Playbook */}
      {playbookResult && (
        <div className="bg-gray-900/50 border border-gray-700/50 rounded-xl p-6 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-base font-semibold text-yellow-400/80">
              {isAr ? "خطة التدخل" : "Intervention Playbook"}
            </h2>
            <span
              className={`px-2 py-0.5 rounded border text-xs font-bold ${
                PRIORITY_COLORS[playbookResult.playbook?.priority] ?? "bg-gray-700 text-gray-300"
              }`}
            >
              {playbookResult.playbook?.priority}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(playbookResult.playbook?.actions_ar?.length ?? 0) > 0 && (
              <div>
                <p className="text-xs text-gray-400 mb-2">
                  {isAr ? "الإجراءات (عربي)" : "Actions (AR)"}
                </p>
                <ul className="space-y-1">
                  {playbookResult.playbook?.actions_ar.map((a, i) => (
                    <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                      <span className="text-yellow-400 shrink-0">{i + 1}.</span>
                      <span>{a}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {(playbookResult.playbook?.actions_en?.length ?? 0) > 0 && (
              <div>
                <p className="text-xs text-gray-400 mb-2">
                  {isAr ? "الإجراءات (إنجليزي)" : "Actions (EN)"}
                </p>
                <ul className="space-y-1">
                  {playbookResult.playbook?.actions_en.map((a, i) => (
                    <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                      <span className="text-yellow-400 shrink-0">{i + 1}.</span>
                      <span>{a}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Expansion Signals */}
      {expansionResult &&
        (expansionResult.band === "expand_now" ||
          expansionResult.band === "potential") && (
          <div className="bg-gray-900/50 border border-green-700/30 rounded-xl p-6 backdrop-blur-sm">
            <h2 className="text-base font-semibold text-green-400/80 mb-3">
              {isAr ? "فرصة التوسع" : "Expansion Opportunity"}
            </h2>
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl font-bold text-green-400">
                {Math.round(expansionResult.expansion_score * 100)}%
              </span>
              <span className="px-2 py-0.5 rounded border bg-green-400/10 border-green-400/30 text-green-400 text-xs">
                {expansionResult.band}
              </span>
            </div>
            {expansionResult.expansion_hint_ar && (
              <p className="text-sm text-gray-300">{expansionResult.expansion_hint_ar}</p>
            )}
          </div>
        )}

      {/* Estimate disclaimer */}
      <p className="text-xs text-gray-500 border-t border-gray-800 pt-3">
        {isAr
          ? "is_estimate=True — جميع النتائج تقديرية وتستلزم مراجعة بشرية قبل أي إجراء خارجي."
          : "is_estimate=True — All results are estimates and require human review before any external action."}
      </p>
    </div>
  );
}
