"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface DailyBrief {
  date: string;
  private_ops_enabled: boolean;
  private_ops_note: string | null;
  top_focus: string[];
  decisions_pending: { count: number; items: unknown[] };
  pipeline_signal?: { rows: number };
  evidence_signal?: { rows: number };
}

interface WeeklyReview {
  week_end: string;
  private_ops_enabled: boolean;
  questions: string[];
}

const LINK_TILES = [
  { href: "/founder-leverage", label: "Founder Leverage" },
  { href: "/capital-allocation", label: "Capital Allocation" },
  { href: "/strategy", label: "Strategy & Assumptions" },
  { href: "/deal-desk", label: "Deal Desk" },
  { href: "/enterprise-sales", label: "Enterprise Sales" },
  { href: "/metrics", label: "Hypergrowth Metrics" },
];

export function CeoOsHub() {
  const [brief, setBrief] = useState<DailyBrief | null>(null);
  const [weekly, setWeekly] = useState<WeeklyReview | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [b, w] = await Promise.all([
          fetch("/api/v1/founder/ceo-os/daily-brief").then((r) =>
            r.ok ? r.json() : null
          ),
          fetch("/api/v1/founder/ceo-os/weekly-review").then((r) =>
            r.ok ? r.json() : null
          ),
        ]);
        if (!cancelled) {
          setBrief(b);
          setWeekly(w);
        }
      } catch (e) {
        if (!cancelled) setError(String(e));
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-6">
      {brief?.private_ops_note && (
        <Card>
          <CardContent className="p-4 text-sm text-muted-foreground">
            {brief.private_ops_note}
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Daily Brief</CardTitle>
            <CardDescription>
              {brief?.date ?? "—"} ·{" "}
              <Badge variant={brief?.private_ops_enabled ? "default" : "outline"}>
                {brief?.private_ops_enabled ? "PRIVATE_OPS on" : "PRIVATE_OPS off"}
              </Badge>
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div>
              <div className="font-medium">Top focus</div>
              {brief?.top_focus?.length ? (
                <ul className="list-disc ml-5">
                  {brief.top_focus.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-muted-foreground">No pending decision.</p>
              )}
            </div>
            <div>
              <div className="font-medium">Decisions pending</div>
              <p>{brief?.decisions_pending?.count ?? 0}</p>
            </div>
            <div className="text-xs text-muted-foreground">
              Pipeline rows: {brief?.pipeline_signal?.rows ?? 0} · Evidence rows:{" "}
              {brief?.evidence_signal?.rows ?? 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Weekly Review Questions</CardTitle>
            <CardDescription>
              Source: dealix/execution_assurance/registry.yaml
            </CardDescription>
          </CardHeader>
          <CardContent className="text-sm">
            {weekly?.questions?.length ? (
              <ol className="list-decimal ml-5 space-y-1">
                {weekly.questions.slice(0, 8).map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ol>
            ) : (
              <p className="text-muted-foreground">
                No questions loaded. See docs/founder/CEO_WEEKLY_REVIEW.md.
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>CEO OS Navigation</CardTitle>
          <CardDescription>
            Jump to the focused panels of the Hypergrowth Layer.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {LINK_TILES.map((tile) => (
              <Link
                key={tile.href}
                href={tile.href}
                className="rounded-xl border border-border p-4 hover:bg-muted/40 transition"
              >
                <div className="font-medium text-sm">{tile.label}</div>
                <div className="text-xs text-muted-foreground mt-1">{tile.href}</div>
              </Link>
            ))}
          </div>
        </CardContent>
      </Card>

      {error && (
        <Card>
          <CardContent className="p-4 text-sm text-destructive">
            Load error: {error}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
