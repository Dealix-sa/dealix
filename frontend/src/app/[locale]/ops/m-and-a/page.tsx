"use client";

import { useLocale } from "next-intl";
import { useEffect, useState, useRef } from "react";
import { AppLayout } from "@/components/layout/AppLayout";

/* ─── Types ─────────────────────────────────────────────────────────── */

interface EvaluationResult {
  ebitda_sar: number;
  valuation_sar: number;
  upfront_cash_sar: number;
  earnout_sar: number;
  loi_arabic: string;
  loi_english: string;
  multiplier: number;
  risk_level: string;
}

interface ProposalRow {
  id: string;
  company_name: string;
  sector: string;
  annual_revenue_sar: number;
  valuation_sar: number;
  status: string;
  created_at: string;
}

/* ─── Helpers ─────────────────────────────────────────────────────────*/

function formatSAR(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return n.toLocaleString();
}

/* ─── Page component ─────────────────────────────────────────────────*/

export default function MAndAPage() {
  const locale = useLocale();
  const isAr = locale === "ar";

  /* Stats */
  const [stats, setStats] = useState({
    targets_tracked: 0,
    pipeline_value_sar: 0,
    avg_multiplier: 0,
    lois_drafted: 0,
  });

  /* Form state */
  const [form, setForm] = useState({
    company_name: "",
    sector: "logistics",
    annual_revenue_sar: "",
    net_profit_margin_pct: "",
    employees: "",
    years_in_business: "",
    has_real_estate: false,
    has_ip_assets: false,
  });

  /* UI state */
  const [evaluating, setEvaluating] = useState(false);
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [loiTab, setLoiTab] = useState<"ar" | "en">("ar");
  const [proposals, setProposals] = useState<ProposalRow[]>([]);
  const [error, setError] = useState("");
  const resultRef = useRef<HTMLDivElement>(null);

  /* Load stats + proposals on mount */
  useEffect(() => {
    fetch("/api/v1/m-and-a/stats")
      .then((r) => r.ok ? r.json() : Promise.reject())
      .then((d) => setStats(d))
      .catch(() => {/* silent — backend may not exist yet */});

    fetch("/api/v1/m-and-a/proposals?limit=20")
      .then((r) => r.ok ? r.json() : Promise.reject())
      .then((d) => setProposals(d.items ?? []))
      .catch(() => {/* silent */});
  }, []);

  /* Field change helper */
  function set(key: string, value: string | boolean) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  /* Submit evaluation */
  async function handleEvaluate() {
    setError("");
    if (!form.company_name.trim()) {
      setError(isAr ? "أدخل اسم الشركة" : "Enter company name");
      return;
    }
    if (!form.annual_revenue_sar || Number(form.annual_revenue_sar) <= 0) {
      setError(isAr ? "أدخل الإيراد السنوي" : "Enter annual revenue");
      return;
    }
    setEvaluating(true);
    try {
      const res = await fetch("/api/v1/m-and-a/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company_name: form.company_name.trim(),
          sector: form.sector,
          annual_revenue_sar: Number(form.annual_revenue_sar),
          net_profit_margin_pct: Number(form.net_profit_margin_pct) || 10,
          employees: Number(form.employees) || 0,
          years_in_business: Number(form.years_in_business) || 0,
          has_real_estate: form.has_real_estate,
          has_ip_assets: form.has_ip_assets,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data: EvaluationResult = await res.json();
      setResult(data);
      setStats((s) => ({
        ...s,
        targets_tracked: s.targets_tracked + 1,
        lois_drafted: s.lois_drafted + 1,
        pipeline_value_sar: s.pipeline_value_sar + data.valuation_sar,
      }));
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
    } catch {
      setError(isAr ? "فشل التقييم — تحقق من الاتصال." : "Evaluation failed — check connection.");
    } finally {
      setEvaluating(false);
    }
  }

  const sectors = [
    { value: "logistics", label: isAr ? "لوجستيات" : "Logistics" },
    { value: "retail", label: isAr ? "تجزئة" : "Retail" },
    { value: "tech", label: isAr ? "تقنية" : "Tech" },
    { value: "food", label: isAr ? "غذاء" : "Food" },
    { value: "manufacturing", label: isAr ? "تصنيع" : "Manufacturing" },
    { value: "services", label: isAr ? "خدمات" : "Services" },
  ];

  return (
    <AppLayout
      title={isAr ? "رادار الاستحواذ" : "M&A Radar"}
      subtitle={isAr ? "تقييم الأهداف وصياغة خطابات النية" : "Target evaluation & LOI drafting"}
    >
      <div className="space-y-8" dir={isAr ? "rtl" : "ltr"}>
        {/* ─── Hero Stats ─────────────────────────────────────────────── */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            {
              label: isAr ? "الأهداف المتتبعة" : "Targets Tracked",
              value: stats.targets_tracked,
              color: "from-violet-500/20 to-transparent",
            },
            {
              label: isAr ? "قيمة الخط (ريال)" : "Pipeline Value (SAR)",
              value: `${formatSAR(stats.pipeline_value_sar)} SAR`,
              color: "from-emerald-500/20 to-transparent",
            },
            {
              label: isAr ? "متوسط المضاعف" : "Avg Multiplier",
              value: `${stats.avg_multiplier.toFixed(1)}x`,
              color: "from-sky-500/20 to-transparent",
            },
            {
              label: isAr ? "خطابات نية صِيغت" : "LOIs Drafted",
              value: stats.lois_drafted,
              color: "from-amber-500/20 to-transparent",
            },
          ].map(({ label, value, color }) => (
            <div
              key={label}
              className={`bg-gradient-to-br ${color} bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6`}
            >
              <p className="text-xs text-muted-foreground uppercase tracking-wide">{label}</p>
              <p className="text-2xl font-bold mt-1 tabular-nums">{value}</p>
            </div>
          ))}
        </div>

        {/* ─── Evaluation Form ─────────────────────────────────────────── */}
        <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-semibold">
            {isAr ? "تقييم هدف جديد" : "Evaluate New Target"}
          </h2>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {/* Company name */}
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "اسم الشركة" : "Company Name"}
              </label>
              <input
                type="text"
                value={form.company_name}
                onChange={(e) => set("company_name", e.target.value)}
                placeholder={isAr ? "مثال: شركة الرياض للنقل" : "e.g. Riyadh Logistics Co."}
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>

            {/* Sector */}
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "القطاع" : "Sector"}
              </label>
              <select
                value={form.sector}
                onChange={(e) => set("sector", e.target.value)}
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              >
                {sectors.map((s) => (
                  <option key={s.value} value={s.value}>
                    {s.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Annual revenue */}
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "الإيراد السنوي (ريال)" : "Annual Revenue (SAR)"}
              </label>
              <input
                type="number"
                min="0"
                value={form.annual_revenue_sar}
                onChange={(e) => set("annual_revenue_sar", e.target.value)}
                placeholder="2,000,000"
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>

            {/* Net profit margin */}
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "هامش صافي الربح (%)" : "Net Profit Margin (%)"}
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={form.net_profit_margin_pct}
                onChange={(e) => set("net_profit_margin_pct", e.target.value)}
                placeholder="12"
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>

            {/* Employees */}
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "عدد الموظفين" : "Employees"}
              </label>
              <input
                type="number"
                min="0"
                value={form.employees}
                onChange={(e) => set("employees", e.target.value)}
                placeholder="45"
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>

            {/* Years in business */}
            <div className="space-y-1">
              <label className="text-xs text-muted-foreground">
                {isAr ? "سنوات في السوق" : "Years in Business"}
              </label>
              <input
                type="number"
                min="0"
                value={form.years_in_business}
                onChange={(e) => set("years_in_business", e.target.value)}
                placeholder="7"
                className="w-full rounded-lg bg-background/40 border border-white/10 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
              />
            </div>
          </div>

          {/* Checkboxes */}
          <div className="flex flex-wrap gap-6">
            <label className="flex items-center gap-2 cursor-pointer select-none text-sm">
              <input
                type="checkbox"
                checked={form.has_real_estate}
                onChange={(e) => set("has_real_estate", e.target.checked)}
                className="w-4 h-4 accent-primary"
              />
              {isAr ? "أصول عقارية" : "Real Estate Assets"}
            </label>
            <label className="flex items-center gap-2 cursor-pointer select-none text-sm">
              <input
                type="checkbox"
                checked={form.has_ip_assets}
                onChange={(e) => set("has_ip_assets", e.target.checked)}
                className="w-4 h-4 accent-primary"
              />
              {isAr ? "ملكية فكرية (براءات/علامات)" : "IP Assets (Patents / Trademarks)"}
            </label>
          </div>

          {error && <p className="text-sm text-destructive">{error}</p>}

          <button
            onClick={handleEvaluate}
            disabled={evaluating}
            className="rounded-xl bg-primary px-6 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            {evaluating
              ? isAr ? "جارٍ التقييم…" : "Evaluating…"
              : isAr ? "قيّم الآن" : "Evaluate Now"}
          </button>
        </div>

        {/* ─── Results Panel ────────────────────────────────────────────── */}
        {result && (
          <div
            ref={resultRef}
            className="bg-white/5 backdrop-blur border border-emerald-500/30 rounded-2xl p-6 space-y-6"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">
                {isAr ? "نتائج التقييم" : "Evaluation Results"}
              </h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  result.risk_level === "low"
                    ? "bg-emerald-500/20 text-emerald-400"
                    : result.risk_level === "medium"
                    ? "bg-amber-500/20 text-amber-400"
                    : "bg-red-500/20 text-red-400"
                }`}
              >
                {isAr
                  ? result.risk_level === "low" ? "مخاطر منخفضة" : result.risk_level === "medium" ? "مخاطر متوسطة" : "مخاطر عالية"
                  : `${result.risk_level.charAt(0).toUpperCase() + result.risk_level.slice(1)} Risk`}
              </span>
            </div>

            {/* Financial summary */}
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {[
                {
                  label: isAr ? "EBITDA (ريال)" : "EBITDA (SAR)",
                  value: `${formatSAR(result.ebitda_sar)} SAR`,
                },
                {
                  label: isAr ? "التقييم (ريال)" : "Valuation (SAR)",
                  value: `${formatSAR(result.valuation_sar)} SAR`,
                },
                {
                  label: isAr ? "نقد مقدم 60% (ريال)" : "Upfront Cash 60% (SAR)",
                  value: `${formatSAR(result.upfront_cash_sar)} SAR`,
                },
                {
                  label: isAr ? "استحقاق 40% (ريال)" : "Earnout 40% (SAR)",
                  value: `${formatSAR(result.earnout_sar)} SAR`,
                },
              ].map(({ label, value }) => (
                <div
                  key={label}
                  className="bg-background/30 rounded-xl p-4 border border-white/5"
                >
                  <p className="text-xs text-muted-foreground">{label}</p>
                  <p className="text-xl font-bold mt-1 tabular-nums">{value}</p>
                </div>
              ))}
            </div>

            {/* LOI Tabs */}
            <div className="space-y-2">
              <div className="flex gap-1 border border-white/10 rounded-lg w-fit p-0.5">
                {(["ar", "en"] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setLoiTab(tab)}
                    className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                      loiTab === tab
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {tab === "ar" ? "عربي" : "English"}
                  </button>
                ))}
              </div>
              <div className="bg-background/30 rounded-xl p-4 border border-white/10 text-sm leading-relaxed whitespace-pre-wrap max-h-72 overflow-auto">
                {loiTab === "ar" ? result.loi_arabic : result.loi_english}
              </div>
            </div>
          </div>
        )}

        {/* ─── Proposals History ─────────────────────────────────────────── */}
        <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-semibold">
            {isAr ? "سجل المقترحات" : "Proposals History"}
          </h2>
          <div className="overflow-x-auto rounded-xl border border-white/10">
            <table className="w-full text-sm">
              <thead className="bg-white/5">
                <tr>
                  <th className="p-3 text-start text-xs text-muted-foreground font-medium">
                    {isAr ? "الشركة" : "Company"}
                  </th>
                  <th className="p-3 text-start text-xs text-muted-foreground font-medium">
                    {isAr ? "القطاع" : "Sector"}
                  </th>
                  <th className="p-3 text-start text-xs text-muted-foreground font-medium">
                    {isAr ? "الإيراد (ريال)" : "Revenue (SAR)"}
                  </th>
                  <th className="p-3 text-start text-xs text-muted-foreground font-medium">
                    {isAr ? "التقييم (ريال)" : "Valuation (SAR)"}
                  </th>
                  <th className="p-3 text-start text-xs text-muted-foreground font-medium">
                    {isAr ? "الحالة" : "Status"}
                  </th>
                  <th className="p-3 text-start text-xs text-muted-foreground font-medium">
                    {isAr ? "التاريخ" : "Date"}
                  </th>
                </tr>
              </thead>
              <tbody>
                {proposals.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-6 text-center text-muted-foreground text-sm">
                      {isAr ? "لا توجد مقترحات بعد — قيّم هدفاً أعلاه." : "No proposals yet — evaluate a target above."}
                    </td>
                  </tr>
                ) : (
                  proposals.map((row) => (
                    <tr key={row.id} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                      <td className="p-3 font-medium">{row.company_name}</td>
                      <td className="p-3 text-muted-foreground capitalize">{row.sector}</td>
                      <td className="p-3 tabular-nums">{formatSAR(row.annual_revenue_sar)}</td>
                      <td className="p-3 tabular-nums">{formatSAR(row.valuation_sar)}</td>
                      <td className="p-3">
                        <span
                          className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                            row.status === "loi_sent"
                              ? "bg-emerald-500/20 text-emerald-400"
                              : row.status === "draft"
                              ? "bg-amber-500/20 text-amber-400"
                              : "bg-white/10 text-muted-foreground"
                          }`}
                        >
                          {row.status.replace(/_/g, " ")}
                        </span>
                      </td>
                      <td className="p-3 text-muted-foreground text-xs">
                        {new Date(row.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
