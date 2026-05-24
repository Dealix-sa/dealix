"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface Dashboard {
  private_ops_enabled: boolean;
  private_ops_note: string | null;
  summary: {
    window_weeks: number;
    totals: Record<string, number>;
    ratio: Record<string, number>;
    rows_used: number;
  };
  bottlenecks_top3: string[];
}

export function FounderLeveragePanel() {
  const [data, setData] = useState<Dashboard | null>(null);

  useEffect(() => {
    fetch("/api/v1/founder/leverage/dashboard")
      .then((r) => (r.ok ? r.json() : null))
      .then(setData)
      .catch(() => setData(null));
  }, []);

  return (
    <div className="space-y-6">
      {data?.private_ops_note && (
        <Card>
          <CardContent className="p-4 text-sm text-muted-foreground">
            {data.private_ops_note}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Bucket mix — last {data?.summary?.window_weeks ?? 4} weeks</CardTitle>
          <CardDescription>
            Make / Manage / Move. Target Move ≥ 40%.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 text-sm">
            {(["make", "manage", "move"] as const).map((bucket) => {
              const ratio = data?.summary?.ratio?.[bucket] ?? 0;
              const hours = data?.summary?.totals?.[bucket] ?? 0;
              return (
                <div key={bucket} className="rounded-xl border border-border p-4">
                  <div className="text-xs uppercase text-muted-foreground">{bucket}</div>
                  <div className="text-2xl font-semibold">{Math.round(ratio * 100)}%</div>
                  <div className="text-xs text-muted-foreground">{hours} hrs</div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Bottlenecks tied to me</CardTitle>
          <CardDescription>Top 3 from bottleneck radar</CardDescription>
        </CardHeader>
        <CardContent className="text-sm">
          {data?.bottlenecks_top3?.length ? (
            <ul className="list-disc ml-5 space-y-1">
              {data.bottlenecks_top3.map((b, i) => (
                <li key={i}>{b}</li>
              ))}
            </ul>
          ) : (
            <p className="text-muted-foreground">
              No bottlenecks ranked. Walk docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
