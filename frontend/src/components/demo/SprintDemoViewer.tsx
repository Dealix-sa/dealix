"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type TopAccount = {
  company_name?: string;
  name?: string;
  sector?: string;
  city?: string;
  relationship_status?: string;
  score?: number;
  rank?: number;
  reasons?: string[];
};

type SprintSample = {
  engagement_id?: string;
  proof_score?: number;
  proof_tier?: string;
  retainer_eligible?: boolean;
  company_brain?: { workspace_id?: string; status?: string; top_accounts_indexed?: string[] };
  steps?: Array<{
    name: string;
    status: string;
    output?: Record<string, unknown>;
  }>;
  proof_pack?: {
    sections?: Record<string, string>;
    score?: number;
    tier?: string;
  };
};

function tierColor(tier?: string) {
  if (!tier) return "secondary";
  if (tier.includes("strong")) return "default";
  if (tier.includes("moderate")) return "outline";
  return "secondary";
}

export function SprintDemoViewer() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<SprintSample | null>(null);
  const [loading, setLoading] = useState(true);
  const [elapsed, setElapsed] = useState<number | null>(null);

  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const t0 = performance.now();
    fetch(`${base}/api/v1/sprint/sample`)
      .then((r) => r.json())
      .then((d) => {
        setData(d as SprintSample);
        setElapsed(Math.round(performance.now() - t0));
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  // Extract top accounts from scoring step
  const scoringStep = data?.steps?.find((s) => s.name === "account_scoring");
  const topAccounts: TopAccount[] = (scoringStep?.output?.top_10 as TopAccount[]) ?? [];

  // DQ score
  const dqStep = data?.steps?.find((s) => s.name === "data_quality");
  const dqScore = (dqStep?.output?.dq_overall as number) ?? null;

  // Proof Pack key sections
  const sections = data?.proof_pack?.sections ?? {};
  const keySections = [
    { key: "executive_summary", labelAr: "الملخص التنفيذي", labelEn: "Executive Summary" },
    { key: "outputs", labelAr: "المخرجات", labelEn: "Outputs" },
    { key: "recommended_next_step", labelAr: "الخطوة التالية", labelEn: "Next Step" },
  ];

  if (loading) {
    return (
      <div className="space-y-4 animate-pulse" dir={isAr ? "rtl" : "ltr"}>
        <div className="h-8 bg-muted rounded w-2/3" />
        <div className="h-4 bg-muted rounded w-full" />
        <div className="h-4 bg-muted rounded w-5/6" />
        <div className="grid grid-cols-3 gap-3">
          {[1, 2, 3].map((i) => <div key={i} className="h-24 bg-muted rounded" />)}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="rounded-lg border border-destructive/30 p-6 text-center" dir={isAr ? "rtl" : "ltr"}>
        <p className="text-sm text-muted-foreground">
          {isAr ? "لا يمكن تحميل البيانات الآن. جرّب لاحقاً." : "Unable to load demo data right now. Try again shortly."}
        </p>
      </div>
    );
  }

  const score = data.proof_score ?? data.proof_pack?.score ?? 0;
  const tier = data.proof_tier ?? data.proof_pack?.tier ?? "";

  return (
    <div className="space-y-8" dir={isAr ? "rtl" : "ltr"}>
      {/* Header metrics */}
      <div className="flex flex-wrap items-center gap-3">
        <Badge variant={tierColor(tier)} className="text-sm px-3 py-1">
          {isAr ? "درجة الإثبات" : "Proof Score"}: {score.toFixed(1)}
        </Badge>
        {tier && (
          <Badge variant="outline" className="text-xs">
            {tier.replace(/_/g, " ")}
          </Badge>
        )}
        {data.retainer_eligible && (
          <Badge className="text-xs bg-green-600 hover:bg-green-700">
            {isAr ? "مؤهّل للـ Retainer" : "Retainer Eligible"}
          </Badge>
        )}
        {dqScore !== null && (
          <Badge variant="outline" className="text-xs">
            DQ: {(dqScore * 100).toFixed(0)}%
          </Badge>
        )}
        {elapsed !== null && (
          <span className="text-xs text-muted-foreground">
            {elapsed < 200 ? "⚡ " : ""}{elapsed}ms
          </span>
        )}
      </div>

      {/* Top scored accounts */}
      {topAccounts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
            {isAr ? "أعلى الحسابات تقييماً" : "Top Scored Accounts"}
          </h3>
          <div className="space-y-2">
            {topAccounts.slice(0, 5).map((acc, i) => (
              <Card key={i} className="p-3 flex items-center gap-3 border-border/60">
                <span className="text-lg font-bold text-primary/60 w-6 shrink-0">
                  {acc.rank ?? i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">
                    {acc.company_name ?? acc.name ?? "—"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {[acc.sector, acc.city].filter(Boolean).join(" · ")}
                  </p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {acc.relationship_status === "warm" && (
                    <Badge variant="default" className="text-xs py-0">warm</Badge>
                  )}
                  {acc.score !== undefined && (
                    <span className="text-sm font-semibold text-primary">{acc.score}</span>
                  )}
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Proof Pack preview — first 3 sections */}
      {Object.keys(sections).length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
            {isAr ? "Proof Pack — مقتطف" : "Proof Pack — Preview"}
          </h3>
          <div className="space-y-3">
            {keySections.map(({ key, labelAr, labelEn }) => {
              const text = sections[key];
              if (!text) return null;
              return (
                <Card key={key} className="p-4 border-border/50">
                  <p className="text-xs font-semibold text-primary/70 uppercase tracking-wide mb-1">
                    {isAr ? labelAr : labelEn}
                  </p>
                  <p className="text-sm text-foreground/80 leading-relaxed line-clamp-3">{text}</p>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      {/* Company Brain status */}
      {data.company_brain?.status === "company_brain_v1_ready" && (
        <Card className="p-4 border-primary/20 bg-primary/5">
          <p className="text-xs font-semibold text-primary uppercase tracking-wide mb-1">
            Company Brain v1
          </p>
          <p className="text-sm text-foreground/70">
            {isAr
              ? `مساحة العمل جاهزة: ${data.company_brain.workspace_id ?? ""}. أُفهرست ${data.company_brain.top_accounts_indexed?.length ?? 0} شركات.`
              : `Workspace ready: ${data.company_brain.workspace_id ?? ""}. ${data.company_brain.top_accounts_indexed?.length ?? 0} companies indexed.`}
          </p>
        </Card>
      )}

      {/* CTAs */}
      <div className="flex flex-wrap gap-3 pt-2">
        <Button asChild size="lg">
          <Link href={`/${locale}/dealix-diagnostic`}>
            {isAr ? "ابدأ Diagnostic مجاني ←" : "Start Free Diagnostic →"}
          </Link>
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link href={`/${locale}/offer/lead-intelligence-sprint`}>
            {isAr ? "Sprint 499 ر.س — ابدأ الآن" : "Sprint 499 SAR — Start Now"}
          </Link>
        </Button>
      </div>
    </div>
  );
}
