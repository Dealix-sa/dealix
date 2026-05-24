"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface DailyBrief {
  date: string;
  pipeline_signal?: { rows: number };
  evidence_signal?: { rows: number };
  decisions_pending?: { count: number };
  private_ops_enabled: boolean;
}

const TIERS = [
  { tier: "Tier 1 — North Star", source: "evidence_events_tracker.csv + proof ledger" },
  { tier: "Tier 2 — Leading", source: "evidence_events_tracker.csv + pipeline_tracker.csv" },
  { tier: "Tier 3 — Operating", source: "approval_center + friction_log + bottleneck_radar" },
];

export function HypergrowthMetricsPanel() {
  const [brief, setBrief] = useState<DailyBrief | null>(null);

  useEffect(() => {
    fetch("/api/v1/founder/ceo-os/daily-brief")
      .then((r) => (r.ok ? r.json() : null))
      .then(setBrief)
      .catch(() => setBrief(null));
  }, []);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Hypergrowth Metrics System</CardTitle>
          <CardDescription>
            Three-tier metric tree. Walk
            docs/metrics/HYPERGROWTH_METRICS_SYSTEM.md.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-sm space-y-3">
          {TIERS.map((t) => (
            <div key={t.tier} className="rounded-xl border border-border p-3">
              <div className="font-medium">{t.tier}</div>
              <div className="text-xs text-muted-foreground">Source: {t.source}</div>
            </div>
          ))}
          <div className="grid grid-cols-3 gap-3 mt-3">
            <div className="rounded-xl border border-border p-3">
              <div className="text-xs uppercase text-muted-foreground">Pipeline rows</div>
              <div className="text-xl font-semibold">{brief?.pipeline_signal?.rows ?? 0}</div>
            </div>
            <div className="rounded-xl border border-border p-3">
              <div className="text-xs uppercase text-muted-foreground">Evidence rows</div>
              <div className="text-xl font-semibold">{brief?.evidence_signal?.rows ?? 0}</div>
            </div>
            <div className="rounded-xl border border-border p-3">
              <div className="text-xs uppercase text-muted-foreground">Decisions pending</div>
              <div className="text-xl font-semibold">{brief?.decisions_pending?.count ?? 0}</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
