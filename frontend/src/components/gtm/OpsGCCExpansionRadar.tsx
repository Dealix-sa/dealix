"use client";

import { useState, useCallback, useEffect } from "react";
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

type CountryCode = "SA" | "AE" | "KW" | "BH" | "QA" | "OM";

type CountryCard = {
  country_code: CountryCode;
  country_name_ar: string;
  country_name_en: string;
  top_sector: string | null;
  heat_score: number;
};

type GCCOverview = {
  countries: CountryCard[];
  generated_at: string;
  is_estimate: boolean;
};

type SignalDetectResult = {
  detected: boolean;
  confidence: number;
  signal_type: string;
  metadata: Record<string, unknown>;
  governance_decision: string;
  is_estimate: boolean;
};

type CityCard = {
  city: string;
  heat_score: number;
  top_sector: string | null;
};

type HotCitiesResult = {
  country: CountryCode;
  cities: CityCard[];
  is_estimate: boolean;
};

type OpportunityCard = {
  company_name: string;
  urgency_score: number;
  why_now_ar: string;
  why_now_en: string;
  sector_ar: string;
  sector_en: string;
};

type OpportunityFeedResult = {
  country: CountryCode;
  opportunities: OpportunityCard[];
  is_estimate: boolean;
  governance_decision: string;
};

const COUNTRY_NAMES_AR: Record<CountryCode, string> = {
  SA: "السعودية",
  AE: "الإمارات",
  KW: "الكويت",
  BH: "البحرين",
  QA: "قطر",
  OM: "عُمان",
};

const COUNTRY_NAMES_EN: Record<CountryCode, string> = {
  SA: "Saudi Arabia",
  AE: "UAE",
  KW: "Kuwait",
  BH: "Bahrain",
  QA: "Qatar",
  OM: "Oman",
};

const SIGNAL_TYPES = ["hiring", "website", "ads", "funding", "tender"] as const;
type SignalType = (typeof SIGNAL_TYPES)[number];

const COUNTRY_CODES: CountryCode[] = ["SA", "AE", "KW", "BH", "QA", "OM"];

function heatColor(score: number): string {
  if (score > 70) return "text-green-400";
  if (score >= 40) return "text-yellow-400";
  return "text-zinc-400";
}

function heatBorder(score: number): string {
  if (score > 70) return "border-green-500/40 shadow-green-500/10 shadow-sm";
  if (score >= 40) return "border-yellow-500/30";
  return "border-zinc-700";
}

export function OpsGCCExpansionRadar() {
  const locale = useLocale();
  const isAr = locale === "ar";

  // GCC Overview
  const [overview, setOverview] = useState<GCCOverview | null>(null);
  const [overviewLoading, setOverviewLoading] = useState(true);
  const [overviewError, setOverviewError] = useState<string | null>(null);

  // Signal Detector
  const [signalType, setSignalType] = useState<SignalType>("hiring");
  const [rawData, setRawData] = useState('{"company": "شركة ما", "jobs_count": 5}');
  const [signalLoading, setSignalLoading] = useState(false);
  const [signalResult, setSignalResult] = useState<SignalDetectResult | null>(null);
  const [signalError, setSignalError] = useState<string | null>(null);

  // Hot Cities
  const [citiesCountry, setCitiesCountry] = useState<CountryCode>("SA");
  const [topN, setTopN] = useState(5);
  const [citiesResult, setCitiesResult] = useState<HotCitiesResult | null>(null);
  const [citiesLoading, setCitiesLoading] = useState(false);
  const [citiesError, setCitiesError] = useState<string | null>(null);

  // Opportunity Feed
  const [oppCountry, setOppCountry] = useState<CountryCode>("SA");
  const [oppResult, setOppResult] = useState<OpportunityFeedResult | null>(null);
  const [oppLoading, setOppLoading] = useState(false);
  const [oppError, setOppError] = useState<string | null>(null);

  const fetchOverview = useCallback(async () => {
    setOverviewLoading(true);
    setOverviewError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/gcc-expansion/gcc-overview`, {
        headers: { "X-API-Key": API_KEY, "X-Admin-API-Key": ADMIN_KEY },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setOverview(await res.json());
    } catch (e: unknown) {
      setOverviewError(e instanceof Error ? e.message : (isAr ? "تعذّر تحميل نظرة عامة" : "Failed to load overview"));
    } finally {
      setOverviewLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    fetchOverview();
  }, [fetchOverview]);

  const handleSignalDetect = useCallback(async () => {
    setSignalLoading(true);
    setSignalResult(null);
    setSignalError(null);
    let parsed: unknown;
    try {
      parsed = JSON.parse(rawData);
    } catch {
      setSignalError(isAr ? "بيانات JSON غير صالحة" : "Invalid JSON data");
      setSignalLoading(false);
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/v1/gcc-expansion/signal-detect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": API_KEY,
          "X-Admin-API-Key": ADMIN_KEY,
        },
        body: JSON.stringify({ signal_type: signalType, raw_data: parsed }),
      });
      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(d?.detail?.message_ar ?? d?.detail?.message ?? `HTTP ${res.status}`);
      }
      setSignalResult(await res.json());
    } catch (e: unknown) {
      setSignalError(e instanceof Error ? e.message : (isAr ? "حدث خطأ" : "An error occurred"));
    } finally {
      setSignalLoading(false);
    }
  }, [signalType, rawData, isAr]);

  const fetchHotCities = useCallback(async () => {
    setCitiesLoading(true);
    setCitiesError(null);
    try {
      const res = await fetch(
        `${API_BASE}/api/v1/gcc-expansion/hot-cities?country=${citiesCountry}&top_n=${topN}`,
        { headers: { "X-API-Key": API_KEY, "X-Admin-API-Key": ADMIN_KEY } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setCitiesResult(await res.json());
    } catch (e: unknown) {
      setCitiesError(e instanceof Error ? e.message : (isAr ? "تعذّر تحميل المدن" : "Failed to load cities"));
    } finally {
      setCitiesLoading(false);
    }
  }, [citiesCountry, topN, isAr]);

  const fetchOpportunities = useCallback(async () => {
    setOppLoading(true);
    setOppError(null);
    try {
      const res = await fetch(
        `${API_BASE}/api/v1/gcc-expansion/opportunity-feed?country=${oppCountry}`,
        { headers: { "X-API-Key": API_KEY, "X-Admin-API-Key": ADMIN_KEY } }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setOppResult(await res.json());
    } catch (e: unknown) {
      setOppError(e instanceof Error ? e.message : (isAr ? "تعذّر تحميل الفرص" : "Failed to load opportunities"));
    } finally {
      setOppLoading(false);
    }
  }, [oppCountry, isAr]);

  const inputCls =
    "w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-white text-sm focus:outline-none focus:ring-1 focus:ring-amber-500";
  const labelCls = "block text-xs text-zinc-400 mb-1";

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <div>
        <h1 className="text-xl font-bold text-amber-400">
          {isAr ? "رادار التوسع الخليجي" : "GCC Expansion Radar"}
        </h1>
      </div>

      {/* GCC Overview */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-amber-400">
            {isAr ? "نظرة عامة على دول الخليج" : "GCC Country Overview"}
          </h2>
          <button
            onClick={fetchOverview}
            disabled={overviewLoading}
            className="text-xs text-zinc-400 hover:text-amber-400 transition-colors disabled:opacity-50"
          >
            {isAr ? "تحديث" : "Refresh"}
          </button>
        </div>

        {overviewError && (
          <div className="bg-red-950 border border-red-800 rounded-lg p-3 mb-4">
            <p className="text-red-300 text-sm">{overviewError}</p>
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {overviewLoading
            ? COUNTRY_CODES.map((code) => (
                <div
                  key={code}
                  className="bg-zinc-800/60 border border-zinc-700 rounded-lg p-4 animate-pulse"
                >
                  <div className="h-4 bg-zinc-700 rounded w-1/2 mb-2" />
                  <div className="h-6 bg-zinc-700 rounded w-1/3" />
                </div>
              ))
            : (
                overview?.countries.length
                  ? overview.countries
                  : COUNTRY_CODES.map((code) => ({
                      country_code: code,
                      country_name_ar: COUNTRY_NAMES_AR[code],
                      country_name_en: COUNTRY_NAMES_EN[code],
                      top_sector: null,
                      heat_score: 0,
                    }))
              ).map((card) => (
                <div
                  key={card.country_code}
                  className={`bg-zinc-800/60 border rounded-lg p-4 ${heatBorder(card.heat_score)}`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-white font-medium text-sm">
                      {isAr ? card.country_name_ar : card.country_name_en}
                    </span>
                    <span className="text-xs text-zinc-500">{card.country_code}</span>
                  </div>
                  {card.top_sector && (
                    <p className="text-xs text-zinc-400 mb-2">
                      {card.top_sector}
                    </p>
                  )}
                  <div className="flex items-center gap-2">
                    <span className={`text-lg font-bold ${heatColor(card.heat_score)}`}>
                      {card.heat_score}%
                    </span>
                    <span className="text-xs text-zinc-500">
                      {isAr ? "حرارة السوق" : "heat"}
                    </span>
                  </div>
                  <div className="mt-2 h-1.5 bg-zinc-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        card.heat_score > 70
                          ? "bg-green-400"
                          : card.heat_score >= 40
                          ? "bg-yellow-400"
                          : "bg-zinc-500"
                      }`}
                      style={{ width: `${card.heat_score}%` }}
                    />
                  </div>
                </div>
              ))}
        </div>
      </div>

      {/* Signal Detector */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <h2 className="text-base font-semibold text-amber-400 mb-4">
          {isAr ? "كاشف الإشارات" : "Signal Detector"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className={labelCls}>
              {isAr ? "نوع الإشارة" : "Signal Type"}
            </label>
            <select
              className={inputCls}
              value={signalType}
              onChange={(e) => setSignalType(e.target.value as SignalType)}
            >
              {SIGNAL_TYPES.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "البيانات الخام (JSON)" : "Raw Data (JSON)"}
            </label>
            <textarea
              className={`${inputCls} h-24 resize-none font-mono text-xs`}
              value={rawData}
              onChange={(e) => setRawData(e.target.value)}
              placeholder='{"company": "شركة ما", "jobs_count": 5}'
            />
          </div>
        </div>
        <button
          onClick={handleSignalDetect}
          disabled={signalLoading || !rawData.trim()}
          className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold px-5 py-2 rounded text-sm transition-colors"
        >
          {signalLoading
            ? (isAr ? "جارٍ الكشف..." : "Detecting...")
            : (isAr ? "كشف الإشارة" : "Detect Signal")}
        </button>

        {signalError && (
          <p className="mt-3 text-red-400 text-sm">{signalError}</p>
        )}

        {signalResult && (
          <div className="mt-4 p-4 bg-zinc-800 rounded-lg border border-amber-500/30">
            <div className="flex items-center gap-3 mb-3">
              <span
                className={`px-2 py-0.5 rounded border text-xs font-bold ${
                  signalResult.detected
                    ? "bg-green-400/10 border-green-400/30 text-green-400"
                    : "bg-zinc-700 border-zinc-600 text-zinc-400"
                }`}
              >
                {signalResult.detected
                  ? (isAr ? "مكتشف" : "Detected")
                  : (isAr ? "غير مكتشف" : "Not detected")}
              </span>
              <span className="text-sm text-zinc-300">
                {isAr ? "الثقة:" : "Confidence:"}{" "}
                <span className="text-amber-400 font-semibold">
                  {Math.round(signalResult.confidence * 100)}%
                </span>
              </span>
            </div>
            {Object.keys(signalResult.metadata).length > 0 && (
              <pre className="text-xs text-zinc-400 bg-zinc-900 rounded p-2 overflow-x-auto">
                {JSON.stringify(signalResult.metadata, null, 2)}
              </pre>
            )}
          </div>
        )}
      </div>

      {/* Hot Cities */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <h2 className="text-base font-semibold text-amber-400 mb-4">
          {isAr ? "المدن الأكثر نشاطاً" : "Hot Cities"}
        </h2>
        <div className="flex flex-wrap gap-3 mb-4 items-end">
          <div>
            <label className={labelCls}>
              {isAr ? "الدولة" : "Country"}
            </label>
            <select
              className={inputCls}
              value={citiesCountry}
              onChange={(e) => setCitiesCountry(e.target.value as CountryCode)}
            >
              {COUNTRY_CODES.map((c) => (
                <option key={c} value={c}>
                  {isAr ? COUNTRY_NAMES_AR[c] : COUNTRY_NAMES_EN[c]}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className={labelCls}>
              {isAr ? "عدد المدن (3-10)" : "Top N (3-10)"}
            </label>
            <input
              type="range"
              min={3}
              max={10}
              value={topN}
              onChange={(e) => setTopN(parseInt(e.target.value, 10))}
              className="block mt-2 accent-amber-500"
            />
            <span className="text-xs text-amber-400">{topN}</span>
          </div>
          <button
            onClick={fetchHotCities}
            disabled={citiesLoading}
            className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold px-5 py-2 rounded text-sm transition-colors"
          >
            {citiesLoading
              ? (isAr ? "جارٍ التحميل..." : "Loading...")
              : (isAr ? "عرض المدن" : "Show Cities")}
          </button>
        </div>

        {citiesError && (
          <p className="text-red-400 text-sm">{citiesError}</p>
        )}

        {citiesResult && citiesResult.cities.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {citiesResult.cities.map((city, i) => (
              <div
                key={i}
                className={`bg-zinc-800/60 border rounded-lg p-3 ${heatBorder(city.heat_score)}`}
              >
                <p className="text-white font-medium text-sm">
                  {city.city}
                </p>
                {city.top_sector && (
                  <p className="text-xs text-zinc-400 mb-2">
                    {city.top_sector}
                  </p>
                )}
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1.5 bg-zinc-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        city.heat_score > 70
                          ? "bg-green-400"
                          : city.heat_score >= 40
                          ? "bg-yellow-400"
                          : "bg-zinc-500"
                      }`}
                      style={{ width: `${city.heat_score}%` }}
                    />
                  </div>
                  <span className={`text-xs font-bold ${heatColor(city.heat_score)}`}>
                    {city.heat_score}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Opportunity Feed */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
        <h2 className="text-base font-semibold text-amber-400 mb-4">
          {isAr ? "تغذية الفرص" : "Opportunity Feed"}
        </h2>
        <div className="flex flex-wrap gap-3 mb-4 items-end">
          <div>
            <label className={labelCls}>
              {isAr ? "الدولة" : "Country"}
            </label>
            <select
              className={inputCls}
              value={oppCountry}
              onChange={(e) => setOppCountry(e.target.value as CountryCode)}
            >
              {COUNTRY_CODES.map((c) => (
                <option key={c} value={c}>
                  {isAr ? COUNTRY_NAMES_AR[c] : COUNTRY_NAMES_EN[c]}
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={fetchOpportunities}
            disabled={oppLoading}
            className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-semibold px-5 py-2 rounded text-sm transition-colors"
          >
            {oppLoading
              ? (isAr ? "جارٍ التحميل..." : "Loading...")
              : (isAr ? "تحميل الفرص" : "Load Opportunities")}
          </button>
        </div>

        {oppError && (
          <p className="text-red-400 text-sm">{oppError}</p>
        )}

        {oppResult && oppResult.opportunities.length > 0 && (
          <div className="space-y-3">
            {oppResult.opportunities.map((opp, i) => (
              <div
                key={i}
                className="bg-zinc-800/60 border border-zinc-700 rounded-lg p-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium text-sm truncate">
                      {opp.company_name}
                    </p>
                    <p className="text-xs text-zinc-400 mt-0.5">
                      {isAr ? opp.sector_ar : opp.sector_en}
                    </p>
                    <p className="text-sm text-zinc-300 mt-2">
                      {isAr ? opp.why_now_ar : opp.why_now_en}
                    </p>
                  </div>
                  <div className="shrink-0 text-right">
                    <p className="text-xs text-zinc-500 mb-0.5">
                      {isAr ? "الإلحاح" : "Urgency"}
                    </p>
                    <span
                      className={`text-lg font-bold ${heatColor(opp.urgency_score)}`}
                    >
                      {opp.urgency_score}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {oppResult && oppResult.opportunities.length === 0 && (
          <p className="text-zinc-500 text-sm">
            {isAr ? "لا فرص متاحة لهذه الدولة" : "No opportunities for this country"}
          </p>
        )}
      </div>

      <p className="text-xs text-zinc-500 border-t border-zinc-800 pt-3">
        {isAr
          ? "is_estimate=True — جميع النتائج تقديرية وتستلزم مراجعة بشرية قبل أي إجراء خارجي."
          : "is_estimate=True — All results are estimates and require human review before any external action."}
      </p>
    </div>
  );
}
