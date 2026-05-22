"use client";

import { useState, useCallback } from "react";
import { useLocale } from "next-intl";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";
const ADMIN_KEY = process.env.NEXT_PUBLIC_ADMIN_API_KEY || "";

const HEADERS = {
  "Content-Type": "application/json",
  "X-Admin-API-Key": ADMIN_KEY,
};

const SIGNAL_COLORS: Record<string, string> = {
  strong_signal: "text-green-400 bg-green-400/10 border-green-400/30",
  potential: "text-yellow-400 bg-yellow-400/10 border-yellow-400/30",
  no_signal: "text-gray-400 bg-gray-400/10 border-gray-400/30",
  blocked: "text-red-400 bg-red-400/10 border-red-400/30",
};

const SIGNAL_LABELS_AR: Record<string, string> = {
  strong_signal: "إشارة قوية",
  potential: "محتمل",
  no_signal: "لا إشارة",
  blocked: "محجوب — لا دليل",
};

interface EligibilityResult {
  customer_id: string;
  eligible: boolean;
  signal: string;
  recommended_retainer_sar?: number;
  proof_gate_passed: boolean;
  months_as_customer: number;
  churn_band: string;
  is_estimate: boolean;
}

interface DraftResult {
  customer_id: string;
  eligible: boolean;
  draft_ar?: string;
  draft_en?: string;
  retainer_sar?: number;
  draft_only: boolean;
  approval_required: boolean;
  reason?: string;
}

export function OpsRetainerConversionEngine() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [form, setForm] = useState({
    customer_id: "",
    current_tier: "sprint_499",
    months_as_customer: 2,
    proof_events_completed: 1,
    monthly_engagement_drop_pct: 0.1,
    nps: 8,
    pipeline_added_drop_pct: 0.05,
    churn_band: "safe",
    arr_so_far_sar: 1000,
  });

  const [result, setResult] = useState<EligibilityResult | null>(null);
  const [draft, setDraft] = useState<DraftResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkEligibility = useCallback(async () => {
    if (!form.customer_id.trim()) {
      setError(isAr ? "معرف العميل مطلوب" : "Customer ID required");
      return;
    }
    setLoading(true);
    setError(null);
    setDraft(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/retainer-conversion/check-eligibility`, {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify(form),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(isAr ? "فشل الاتصال بالخادم" : "Failed to connect to server");
    } finally {
      setLoading(false);
    }
  }, [form, isAr]);

  const generateDraft = useCallback(async () => {
    if (!result?.eligible) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/retainer-conversion/draft-outreach`, {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify({ ...form, retainer_tier_sar: result.recommended_retainer_sar || 2999 }),
      });
      const data = await res.json();
      setDraft(data);
    } catch (e) {
      setError(isAr ? "فشل توليد المسودة" : "Failed to generate draft");
    } finally {
      setLoading(false);
    }
  }, [form, result, isAr]);

  const inputClass =
    "bg-gray-800/50 border border-gray-600/50 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-yellow-500/50 w-full";
  const labelClass = "text-gray-400 text-xs mb-1 block";

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-yellow-400/80 text-lg font-semibold">
          {isAr ? "محرك تحويل العقود الشهرية" : "Retainer Conversion Engine"}
        </h2>
        <p className="text-gray-500 text-sm mt-1">
          {isAr
            ? "تحديد العملاء الجاهزين للترقية — مع تطبيق قاعدة لا ترقية بدون دليل"
            : "Identify upgrade-ready customers — no_upsell_without_proof gate enforced"}
        </p>
      </div>

      {/* Governance notice */}
      <div className="bg-yellow-500/5 border border-yellow-500/20 rounded-lg p-3 text-xs text-yellow-300/70">
        {isAr
          ? "⚖️ جميع مسودات التواصل تتطلب موافقة المؤسس — لا يتم الإرسال تلقائياً أبداً"
          : "⚖️ All outreach drafts require founder approval — never auto-sent"}
      </div>

      {/* Form */}
      <div className="bg-gray-900/50 border border-gray-700/50 rounded-xl p-6 backdrop-blur-sm">
        <h3 className="text-white font-medium mb-4">
          {isAr ? "بيانات العميل" : "Customer Data"}
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="col-span-2 md:col-span-1">
            <label className={labelClass}>{isAr ? "معرف العميل" : "Customer ID"}</label>
            <input
              className={inputClass}
              value={form.customer_id}
              onChange={(e) => setForm((p) => ({ ...p, customer_id: e.target.value }))}
              placeholder="cust_001"
            />
          </div>
          <div>
            <label className={labelClass}>{isAr ? "المستوى الحالي" : "Current Tier"}</label>
            <select
              className={inputClass}
              value={form.current_tier}
              onChange={(e) => setForm((p) => ({ ...p, current_tier: e.target.value }))}
            >
              <option value="sprint_499">Sprint 499 SAR</option>
              <option value="data_pack_1500">Data Pack 1,500 SAR</option>
            </select>
          </div>
          <div>
            <label className={labelClass}>{isAr ? "أشهر كعميل" : "Months as Customer"}</label>
            <input
              type="number"
              className={inputClass}
              value={form.months_as_customer}
              onChange={(e) => setForm((p) => ({ ...p, months_as_customer: +e.target.value }))}
              min={0}
            />
          </div>
          <div>
            <label className={labelClass}>{isAr ? "أحداث الإثبات المكتملة" : "Proof Events Completed"}</label>
            <input
              type="number"
              className={inputClass}
              value={form.proof_events_completed}
              onChange={(e) => setForm((p) => ({ ...p, proof_events_completed: +e.target.value }))}
              min={0}
            />
          </div>
          <div>
            <label className={labelClass}>NPS (0-10)</label>
            <input
              type="number"
              className={inputClass}
              value={form.nps}
              onChange={(e) => setForm((p) => ({ ...p, nps: +e.target.value }))}
              min={0}
              max={10}
            />
          </div>
          <div>
            <label className={labelClass}>{isAr ? "انخفاض الاستخدام (0-1)" : "Engagement Drop (0-1)"}</label>
            <input
              type="number"
              className={inputClass}
              value={form.monthly_engagement_drop_pct}
              onChange={(e) => setForm((p) => ({ ...p, monthly_engagement_drop_pct: +e.target.value }))}
              min={0}
              max={1}
              step={0.05}
            />
          </div>
          <div>
            <label className={labelClass}>{isAr ? "مستوى المخاطر" : "Churn Band"}</label>
            <select
              className={inputClass}
              value={form.churn_band}
              onChange={(e) => setForm((p) => ({ ...p, churn_band: e.target.value }))}
            >
              <option value="safe">Safe / آمن</option>
              <option value="watch">Watch / مراقبة</option>
              <option value="at_risk">At Risk / في خطر</option>
              <option value="critical">Critical / حرج</option>
            </select>
          </div>
          <div>
            <label className={labelClass}>{isAr ? "الإيرادات حتى الآن (ر.س)" : "ARR So Far (SAR)"}</label>
            <input
              type="number"
              className={inputClass}
              value={form.arr_so_far_sar}
              onChange={(e) => setForm((p) => ({ ...p, arr_so_far_sar: +e.target.value }))}
              min={0}
            />
          </div>
        </div>
        <button
          onClick={checkEligibility}
          disabled={loading}
          className="mt-4 bg-yellow-500 text-black font-semibold px-6 py-2 rounded-lg hover:bg-yellow-400 transition-colors text-sm disabled:opacity-50"
        >
          {loading ? "..." : isAr ? "فحص الأهلية" : "Check Eligibility"}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Eligibility Result */}
      {result && (
        <div className="bg-gray-900/50 border border-gray-700/50 rounded-xl p-6 backdrop-blur-sm">
          <h3 className="text-white font-medium mb-4">
            {isAr ? "نتيجة الأهلية" : "Eligibility Result"}
          </h3>
          <div className="flex items-center gap-4 mb-4">
            <div className={`px-3 py-1 rounded-full border text-sm font-medium ${SIGNAL_COLORS[result.signal] || SIGNAL_COLORS.no_signal}`}>
              {isAr ? SIGNAL_LABELS_AR[result.signal] : result.signal.replace(/_/g, " ")}
            </div>
            {result.eligible && result.recommended_retainer_sar && (
              <div className="text-green-400 text-sm">
                {isAr ? `الخطة الموصى بها: ${result.recommended_retainer_sar.toLocaleString()} ر.س/شهر` : `Recommended: SAR ${result.recommended_retainer_sar.toLocaleString()}/mo`}
              </div>
            )}
          </div>
          <div className="grid grid-cols-3 gap-3 text-sm">
            <div className="bg-gray-800/50 rounded-lg p-3">
              <div className="text-gray-400 text-xs mb-1">{isAr ? "بوابة الدليل" : "Proof Gate"}</div>
              <div className={result.proof_gate_passed ? "text-green-400" : "text-red-400"}>
                {result.proof_gate_passed ? "✅ Passed" : "❌ Blocked"}
              </div>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-3">
              <div className="text-gray-400 text-xs mb-1">{isAr ? "الأشهر كعميل" : "Months"}</div>
              <div className="text-white">{result.months_as_customer}</div>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-3">
              <div className="text-gray-400 text-xs mb-1">{isAr ? "مستوى المخاطر" : "Churn Band"}</div>
              <div className="text-white">{result.churn_band}</div>
            </div>
          </div>

          {result.eligible && (
            <button
              onClick={generateDraft}
              disabled={loading}
              className="mt-4 bg-gray-700 text-white font-medium px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors text-sm disabled:opacity-50 border border-gray-600"
            >
              {loading ? "..." : isAr ? "توليد مسودة التواصل" : "Generate Outreach Draft"}
            </button>
          )}
        </div>
      )}

      {/* Draft Outreach */}
      {draft && draft.eligible && (
        <div className="bg-gray-900/50 border border-yellow-500/20 rounded-xl p-6 backdrop-blur-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-yellow-400/80 font-medium">
              {isAr ? "مسودة التواصل" : "Outreach Draft"}
            </h3>
            <span className="text-xs text-yellow-300/60 bg-yellow-500/10 border border-yellow-500/20 px-2 py-1 rounded">
              {isAr ? "مسودة — موافقة المؤسس مطلوبة" : "Draft — Founder Approval Required"}
            </span>
          </div>
          {draft.retainer_sar && (
            <div className="text-gray-400 text-sm mb-4">
              {isAr ? `العقد المقترح: ${draft.retainer_sar.toLocaleString()} ر.س/شهر` : `Proposed retainer: SAR ${draft.retainer_sar.toLocaleString()}/mo`}
            </div>
          )}
          <div className="space-y-4">
            {draft.draft_ar && (
              <div>
                <div className="text-xs text-gray-500 mb-2">🇸🇦 Arabic</div>
                <pre className="bg-gray-800/50 border border-gray-700/50 rounded-lg p-4 text-gray-300 text-sm whitespace-pre-wrap font-sans leading-relaxed">
                  {draft.draft_ar}
                </pre>
              </div>
            )}
            {draft.draft_en && (
              <div>
                <div className="text-xs text-gray-500 mb-2">🇬🇧 English</div>
                <pre className="bg-gray-800/50 border border-gray-700/50 rounded-lg p-4 text-gray-300 text-sm whitespace-pre-wrap font-sans leading-relaxed">
                  {draft.draft_en}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Estimate disclaimer */}
      <div className="text-gray-600 text-xs text-center">
        is_estimate=True · no_auto_execute_offer · approval_required_for_external_actions
      </div>
    </div>
  );
}
