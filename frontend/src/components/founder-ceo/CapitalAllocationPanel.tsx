"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface Bucket {
  bucket: string;
  allocated_sar: number;
  actual_sar: number;
  roi_estimate: number;
  count: number;
}

interface Quarterly {
  private_ops_enabled: boolean;
  private_ops_note: string | null;
  quarter: string;
  buckets: Bucket[];
  total_allocated_sar: number;
  total_actual_sar: number;
}

export function CapitalAllocationPanel() {
  const [data, setData] = useState<Quarterly | null>(null);

  useEffect(() => {
    fetch("/api/v1/founder/capital-allocation/quarterly")
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
          <CardTitle>Capital Allocation — {data?.quarter ?? "—"}</CardTitle>
          <CardDescription>
            This layer records intent only; money movement flows through
            docs/revenue/INVOICE_FLOW.md + Moyasar verifier.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-border p-4">
              <div className="text-xs uppercase text-muted-foreground">Allocated</div>
              <div className="text-2xl font-semibold">
                {(data?.total_allocated_sar ?? 0).toLocaleString()} SAR
              </div>
            </div>
            <div className="rounded-xl border border-border p-4">
              <div className="text-xs uppercase text-muted-foreground">Actual</div>
              <div className="text-2xl font-semibold">
                {(data?.total_actual_sar ?? 0).toLocaleString()} SAR
              </div>
            </div>
          </div>

          <div>
            <div className="font-medium mb-2">Buckets</div>
            {data?.buckets?.length ? (
              <ul className="space-y-1">
                {data.buckets.map((b) => (
                  <li key={b.bucket} className="text-xs">
                    <span className="font-medium">{b.bucket}</span> — allocated:{" "}
                    {b.allocated_sar.toLocaleString()} · actual:{" "}
                    {b.actual_sar.toLocaleString()} · ROI: {b.roi_estimate}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-muted-foreground text-xs">
                No bucket rows. Walk docs/finance/CAPITAL_ALLOCATION_SYSTEM.md.
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
