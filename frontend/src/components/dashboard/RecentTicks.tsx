"use client";

import { useState, useEffect } from "react";
import { useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

interface TickEntry {
  tick_id: string | null;
  generated_at: string | null;
  work_items_sensed: number;
  approvals_created: number;
  internal_only_count: number;
  sends: number;
  charges: number;
}

function truncateTickId(id: string | null): string {
  if (!id) return "-";
  return id.length > 16 ? id.slice(0, 16) + "..." : id;
}

function formatTimestamp(ts: string | null, locale: string): string {
  if (!ts) return "-";
  try {
    return new Date(ts).toLocaleString(locale === "ar" ? "ar-SA" : "en-GB", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return ts;
  }
}

export function RecentTicks() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [ticks, setTicks] = useState<TickEntry[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchTicks() {
      try {
        const res = await api.getDailyCommandCenter();
        if (!cancelled) {
          const data = res.data?.data ?? res.data;
          const entries: unknown[] = Array.isArray(data?.recent_ticks)
            ? data.recent_ticks
            : [];
          setTicks(
            entries.map((raw: unknown) => {
              const e = raw as Record<string, unknown>;
              return {
                tick_id: (e.tick_id as string) ?? null,
                generated_at: (e.generated_at as string) ?? null,
                work_items_sensed: (e.work_items_sensed as number) ?? 0,
                approvals_created: (e.approvals_created as number) ?? 0,
                internal_only_count: (e.internal_only_count as number) ?? 0,
                sends: (e.sends as number) ?? 0,
                charges: (e.charges as number) ?? 0,
              };
            })
          );
        }
      } catch {
        if (!cancelled)
          setError(isAr ? "تعذّر تحميل سجل الدورات" : "Failed to load tick history");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchTicks();
    return () => {
      cancelled = true;
    };
  }, [isAr]);

  const titleAr = "آخر الدورات — للاستخدام الداخلي فقط";
  const titleEn = "Recent Ticks — internal use only";

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-base font-semibold">
          {isAr ? titleAr : titleEn}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {loading && (
          <div className="space-y-2">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="h-8 rounded bg-muted animate-pulse" />
            ))}
          </div>
        )}

        {!loading && error && (
          <p className="text-sm text-destructive">{error}</p>
        )}

        {!loading && !error && (!ticks || ticks.length === 0) && (
          <p className="text-sm text-muted-foreground">
            {isAr ? "لا توجد دورات مسجّلة بعد." : "No ticks recorded yet."}
          </p>
        )}

        {!loading && !error && ticks && ticks.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-muted-foreground border-b border-border">
                  <th className="text-start py-1 pe-3 font-medium">
                    {isAr ? "المعرف" : "Tick ID"}
                  </th>
                  <th className="text-start py-1 pe-3 font-medium">
                    {isAr ? "الوقت" : "Time"}
                  </th>
                  <th className="text-end py-1 pe-3 font-medium">
                    {isAr ? "مرصودة" : "Sensed"}
                  </th>
                  <th className="text-end py-1 pe-3 font-medium">
                    {isAr ? "موافقات" : "Approvals"}
                  </th>
                  <th className="text-end py-1 font-medium">
                    {isAr ? "محظورة" : "Blocked"}
                  </th>
                </tr>
              </thead>
              <tbody>
                {ticks.map((tick, i) => (
                  <tr
                    key={tick.tick_id ?? i}
                    className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors"
                  >
                    <td className="py-1.5 pe-3 font-mono text-[10px] text-muted-foreground">
                      {truncateTickId(tick.tick_id)}
                    </td>
                    <td className="py-1.5 pe-3 text-muted-foreground">
                      {formatTimestamp(tick.generated_at, locale)}
                    </td>
                    <td className="py-1.5 pe-3 text-end tabular-nums">
                      {tick.work_items_sensed}
                    </td>
                    <td className="py-1.5 pe-3 text-end tabular-nums">
                      {tick.approvals_created}
                    </td>
                    <td className="py-1.5 text-end tabular-nums">
                      {tick.internal_only_count}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
