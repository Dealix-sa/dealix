"use client";

import { useEffect, useState } from "react";

type ServiceState = {
  name_ar: string;
  name_en: string;
  status: "ok" | "degraded" | "down" | "unknown";
  latency_ms?: number;
  detail?: string;
};

export function StatusBoard({ isAr }: { isAr: boolean }) {
  const [services, setServices] = useState<ServiceState[]>([]);
  const [lastCheck, setLastCheck] = useState<string | null>(null);

  useEffect(() => {
    const check = async () => {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const probes: { url: string; service: ServiceState }[] = [
        {
          url: `${base}/health`,
          service: {
            name_ar: "واجهة API الأساسية",
            name_en: "Core API",
            status: "unknown",
          },
        },
        {
          url: `${base}/api/v1/founder-summary`,
          service: {
            name_ar: "موجز الفاوندر",
            name_en: "Founder summary",
            status: "unknown",
          },
        },
        {
          url: `${base}/api/v1/commercial-map`,
          service: {
            name_ar: "خريطة التجارة",
            name_en: "Commercial map",
            status: "unknown",
          },
        },
      ];

      const results: ServiceState[] = await Promise.all(
        probes.map(async (p) => {
          const start = performance.now();
          try {
            const res = await fetch(p.url, { cache: "no-store" });
            const latency = Math.round(performance.now() - start);
            return {
              ...p.service,
              status: res.ok ? "ok" : res.status >= 500 ? "down" : "degraded",
              latency_ms: latency,
              detail: res.ok ? undefined : `HTTP ${res.status}`,
            };
          } catch (e) {
            return {
              ...p.service,
              status: "down",
              detail: isAr ? "لا يستجيب" : "Not reachable",
            };
          }
        }),
      );

      setServices(results);
      setLastCheck(new Date().toISOString());
    };

    check();
    const id = setInterval(check, 60000);
    return () => clearInterval(id);
  }, [isAr]);

  const overall = services.length
    ? services.every((s) => s.status === "ok")
      ? "ok"
      : services.some((s) => s.status === "down")
        ? "down"
        : "degraded"
    : "unknown";

  const overallColor = {
    ok: "bg-emerald-50 border-emerald-300 text-emerald-900",
    degraded: "bg-amber-50 border-amber-300 text-amber-900",
    down: "bg-red-50 border-red-300 text-red-900",
    unknown: "bg-slate-50 border-slate-300 text-slate-900",
  }[overall];

  const overallLabel = {
    ok: isAr ? "كل الخدمات تعمل" : "All systems operational",
    degraded: isAr ? "بعض الخدمات تتأثر" : "Some services degraded",
    down: isAr ? "هناك خدمة معطلة" : "Outage in progress",
    unknown: isAr ? "جاري الفحص..." : "Probing...",
  }[overall];

  return (
    <div className="space-y-6">
      <div className={`rounded-lg border p-6 ${overallColor}`}>
        <h2 className="text-lg font-semibold">{overallLabel}</h2>
        {lastCheck && (
          <p className="mt-1 text-xs opacity-80">
            {isAr ? "آخر فحص: " : "Last check: "}
            {lastCheck}
          </p>
        )}
      </div>

      <div className="rounded-lg border bg-card">
        <table className="w-full text-sm">
          <thead className="border-b text-xs uppercase text-muted-foreground">
            <tr>
              <th className="px-4 py-2 text-start">
                {isAr ? "الخدمة" : "Service"}
              </th>
              <th className="px-4 py-2 text-start">
                {isAr ? "الحالة" : "Status"}
              </th>
              <th className="px-4 py-2 text-start">
                {isAr ? "زمن الاستجابة" : "Latency"}
              </th>
            </tr>
          </thead>
          <tbody>
            {services.map((s) => (
              <tr key={s.name_en} className="border-b last:border-0">
                <td className="px-4 py-3">{isAr ? s.name_ar : s.name_en}</td>
                <td className="px-4 py-3">
                  <span
                    className={`inline-block rounded px-2 py-0.5 text-xs ${
                      s.status === "ok"
                        ? "bg-emerald-100 text-emerald-800"
                        : s.status === "degraded"
                          ? "bg-amber-100 text-amber-800"
                          : s.status === "down"
                            ? "bg-red-100 text-red-800"
                            : "bg-slate-100 text-slate-800"
                    }`}
                  >
                    {s.status}
                  </span>
                  {s.detail && (
                    <span className="ms-2 text-xs text-muted-foreground">
                      {s.detail}
                    </span>
                  )}
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {s.latency_ms ? `${s.latency_ms} ms` : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border bg-slate-50 p-4 text-xs text-slate-700">
        <p className="font-medium">
          {isAr ? "تعليمات في حالة العطل: " : "If you see an outage: "}
        </p>
        <ol className="mt-2 list-decimal space-y-1 ps-5">
          <li>
            {isAr
              ? "تحقق من /health بشكل مباشر للتأكد."
              : "Cross-check by hitting /health directly."}
          </li>
          <li>
            {isAr
              ? "ابلغ عبر support@dealix.me — رد خلال ٣٠ دقيقة في ساعات العمل."
              : "Report at support@dealix.me — 30-min response in business hours."}
          </li>
          <li>
            {isAr
              ? "نشر post-mortem خلال ٤٨ ساعة من أي outage > ٣٠ دقيقة."
              : "Post-mortem published within 48h of any outage > 30 min."}
          </li>
        </ol>
      </div>
    </div>
  );
}
