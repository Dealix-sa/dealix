"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? ""
    : "";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "https://api.dealix.me";

type RadarData = {
  targets_evaluated: number;
  total_pipeline_sar: number;
  avg_ebitda_multiple: number;
  sector_breakdown: Record<string, number>;
  recent_proposals: ProposalRow[];
};

type ProposalRow = {
  proposal_id: string;
  company_name: string;
  sector: string;
  proposed_offer_sar: number;
  ebitda_margin_pct: number;
  multiplier: number;
  is_estimate: boolean;
  created_at: string;
};

type EvaluateResult = {
  proposal_id: string;
  company_name: string;
  ebitda_sar: number;
  proposed_offer_sar: number;
  upfront_cash_sar: number;
  earnout_sar: number;
  earnout_months: number;
  multiplier: number;
  is_estimate: boolean;
};

function fmt(n: number) {
  return new Intl.NumberFormat("ar-SA", {
    style: "currency",
    currency: "SAR",
    maximumFractionDigits: 0,
  }).format(n);
}

export function OpsMandARadar() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [radar, setRadar] = useState<RadarData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Evaluate form
  const [companyName, setCompanyName] = useState("");
  const [revenue, setRevenue] = useState("");
  const [margin, setMargin] = useState("");
  const [sector, setSector] = useState("general");
  const [evaluating, setEvaluating] = useState(false);
  const [evalResult, setEvalResult] = useState<EvaluateResult | null>(null);
  const [evalError, setEvalError] = useState<string | null>(null);

  const fetchRadar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/m-and-a/radar`, {
        headers: { "X-Admin-API-Key": ADMIN_KEY },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setRadar(await res.json());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load radar");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchRadar(); }, [fetchRadar]);

  const handleEvaluate = async () => {
    if (!companyName || !revenue || !margin) return;
    setEvaluating(true);
    setEvalResult(null);
    setEvalError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/m-and-a/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Admin-API-Key": ADMIN_KEY,
        },
        body: JSON.stringify({
          company_name: companyName,
          annual_revenue_sar: parseFloat(revenue),
          ebitda_margin_pct: parseFloat(margin) / 100,
          sector,
        }),
      });
      if (!res.ok) {
        const d = await res.json();
        throw new Error(d?.detail?.message_ar ?? d?.detail?.message ?? "خطأ في التقييم");
      }
      setEvalResult(await res.json());
      fetchRadar();
    } catch (e: unknown) {
      setEvalError(e instanceof Error ? e.message : "حدث خطأ");
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      {/* KPI strip */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-zinc-900 border-zinc-800 p-5">
          <p className="text-xs text-zinc-400 mb-1">
            {isAr ? "الشركات المقيّمة" : "Targets Evaluated"}
          </p>
          <p className="text-3xl font-bold text-amber-400">
            {loading ? "—" : (radar?.targets_evaluated ?? 0)}
          </p>
        </Card>

        <Card className="bg-zinc-900 border-zinc-800 p-5">
          <p className="text-xs text-zinc-400 mb-1">
            {isAr ? "إجمالي خط الاستحواذ" : "Total Pipeline"}
          </p>
          <p className="text-3xl font-bold text-amber-400">
            {loading ? "—" : fmt(radar?.total_pipeline_sar ?? 0)}
          </p>
        </Card>

        <Card className="bg-zinc-900 border-zinc-800 p-5">
          <p className="text-xs text-zinc-400 mb-1">
            {isAr ? "متوسط مضاعف EBITDA" : "Avg EBITDA Multiple"}
          </p>
          <p className="text-3xl font-bold text-amber-400">
            {loading ? "—" : `${(radar?.avg_ebitda_multiple ?? 0).toFixed(1)}x`}
          </p>
        </Card>
      </div>

      {error && (
        <Card className="bg-red-950 border-red-800 p-4">
          <p className="text-red-300 text-sm">{error}</p>
        </Card>
      )}

      {/* Evaluate form */}
      <Card className="bg-zinc-900 border-zinc-800 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">
          {isAr ? "🎯 تقييم شركة مستهدفة" : "🎯 Evaluate a Target"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
          <div>
            <label className="text-xs text-zinc-400 block mb-1">
              {isAr ? "اسم الشركة" : "Company Name"}
            </label>
            <input
              className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm focus:outline-none focus:ring-1 focus:ring-amber-500"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder={isAr ? "مثال: شركة الرياض" : "e.g. Riyadh Co"}
            />
          </div>
          <div>
            <label className="text-xs text-zinc-400 block mb-1">
              {isAr ? "الإيرادات السنوية (ريال)" : "Annual Revenue (SAR)"}
            </label>
            <input
              type="number"
              className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm focus:outline-none focus:ring-1 focus:ring-amber-500"
              value={revenue}
              onChange={(e) => setRevenue(e.target.value)}
              placeholder="5000000"
            />
          </div>
          <div>
            <label className="text-xs text-zinc-400 block mb-1">
              {isAr ? "هامش EBITDA (%)" : "EBITDA Margin (%)"}
            </label>
            <input
              type="number"
              min={0}
              max={100}
              step={0.5}
              className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm focus:outline-none focus:ring-1 focus:ring-amber-500"
              value={margin}
              onChange={(e) => setMargin(e.target.value)}
              placeholder="20"
            />
          </div>
          <div>
            <label className="text-xs text-zinc-400 block mb-1">
              {isAr ? "القطاع" : "Sector"}
            </label>
            <select
              className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm focus:outline-none focus:ring-1 focus:ring-amber-500"
              value={sector}
              onChange={(e) => setSector(e.target.value)}
            >
              {["general", "retail", "technology", "healthcare", "logistics", "finance", "education"].map(
                (s) => <option key={s} value={s}>{s}</option>
              )}
            </select>
          </div>
        </div>
        <button
          onClick={handleEvaluate}
          disabled={evaluating || !companyName || !revenue || !margin}
          className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold px-5 py-2 rounded text-sm transition-colors"
        >
          {evaluating
            ? (isAr ? "جارٍ التقييم..." : "Evaluating...")
            : (isAr ? "احسب العرض" : "Calculate Offer")}
        </button>

        {evalError && (
          <p className="mt-3 text-red-400 text-sm">{evalError}</p>
        )}

        {evalResult && (
          <div className="mt-5 p-4 bg-zinc-800 rounded-lg border border-amber-500/30">
            <div className="flex items-center gap-2 mb-3">
              <h3 className="text-white font-semibold">
                {evalResult.company_name}
              </h3>
              <Badge className="bg-amber-500/20 text-amber-400 border-amber-500/30 text-xs">
                {isAr ? "تقدير" : "Estimate"} — {evalResult.proposal_id}
              </Badge>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
              <div>
                <p className="text-zinc-400 text-xs">{isAr ? "EBITDA" : "EBITDA"}</p>
                <p className="text-white font-medium">{fmt(evalResult.ebitda_sar)}</p>
              </div>
              <div>
                <p className="text-zinc-400 text-xs">{isAr ? "المضاعف" : "Multiple"}</p>
                <p className="text-white font-medium">{evalResult.multiplier}x</p>
              </div>
              <div>
                <p className="text-zinc-400 text-xs">{isAr ? "إجمالي العرض" : "Total Offer"}</p>
                <p className="text-amber-400 font-bold">{fmt(evalResult.proposed_offer_sar)}</p>
              </div>
              <div>
                <p className="text-zinc-400 text-xs">{isAr ? "دفعة فورية (60%)" : "Upfront (60%)"}</p>
                <p className="text-green-400 font-medium">{fmt(evalResult.upfront_cash_sar)}</p>
              </div>
            </div>
          </div>
        )}
      </Card>

      {/* Recent proposals */}
      {radar && radar.recent_proposals.length > 0 && (
        <Card className="bg-zinc-900 border-zinc-800 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">
            {isAr ? "📋 آخر المقترحات" : "📋 Recent Proposals"}
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="text-left text-zinc-400 pb-2 font-normal">
                    {isAr ? "الشركة" : "Company"}
                  </th>
                  <th className="text-left text-zinc-400 pb-2 font-normal">
                    {isAr ? "القطاع" : "Sector"}
                  </th>
                  <th className="text-right text-zinc-400 pb-2 font-normal">
                    {isAr ? "العرض المقترح" : "Proposed Offer"}
                  </th>
                  <th className="text-right text-zinc-400 pb-2 font-normal">
                    {isAr ? "المضاعف" : "Multiple"}
                  </th>
                </tr>
              </thead>
              <tbody>
                {radar.recent_proposals.map((p) => (
                  <tr key={p.proposal_id} className="border-b border-zinc-800/50">
                    <td className="py-2 text-white">{p.company_name}</td>
                    <td className="py-2 text-zinc-400">{p.sector}</td>
                    <td className="py-2 text-amber-400 text-right font-medium">
                      {fmt(p.proposed_offer_sar)}
                    </td>
                    <td className="py-2 text-zinc-300 text-right">{p.multiplier}x</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
