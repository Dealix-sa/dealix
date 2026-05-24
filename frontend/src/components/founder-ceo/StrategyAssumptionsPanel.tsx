"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface AssumptionRow {
  id?: string;
  assumption?: string;
  owner?: string;
  kill_trigger?: string;
  status?: string;
  last_reviewed?: string;
  notes?: string;
}

interface AssumptionsResponse {
  private_ops_enabled: boolean;
  private_ops_note: string | null;
  count: number;
  items: AssumptionRow[];
}

export function StrategyAssumptionsPanel() {
  const [data, setData] = useState<AssumptionsResponse | null>(null);

  useEffect(() => {
    fetch("/api/v1/founder/ceo-os/assumptions")
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
          <CardTitle>Strategic Assumptions Register</CardTitle>
          <CardDescription>
            Falsifiable bets with kill-triggers. Walk{" "}
            docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-sm">
          <div className="text-muted-foreground text-xs mb-3">
            Total: {data?.count ?? 0}
          </div>
          {data?.items?.length ? (
            <ul className="space-y-3">
              {data.items.map((row, i) => (
                <li key={row.id ?? i} className="border border-border rounded-xl p-3">
                  <div className="font-medium">{row.assumption}</div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Owner: {row.owner ?? "—"} · Status: {row.status ?? "—"} ·
                    Last reviewed: {row.last_reviewed ?? "—"}
                  </div>
                  {row.kill_trigger && (
                    <div className="text-xs mt-1">
                      <span className="font-medium">Kill trigger:</span> {row.kill_trigger}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-muted-foreground">
              No assumptions loaded. Add rows to PRIVATE_OPS ceo/strategic_assumptions.csv.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
