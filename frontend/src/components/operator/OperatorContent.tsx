"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

export function OperatorContent() {
  const t = useTranslations("operator");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [pack, setPack] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getDailySalesPack()
      .then((r) => setPack(r.data as Record<string, unknown>))
      .catch((e) => setError(String(e)));
  }, []);

  const brief = (pack?.daily_brief || {}) as Record<string, unknown>;
  const readiness = (pack?.launch_readiness || {}) as Record<string, unknown>;
  const pending = (pack?.pending_approvals || {}) as { count?: number };
  const decisions = (brief.top_decisions as string[]) || [];

  return (
    <div className="space-y-6 max-w-4xl">
      <Card className="border-gold-500/20">
        <CardHeader>
          <CardTitle>{t("governanceTitle")}</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground space-y-2">
          <p>{t("governanceNote")}</p>
          <div className="flex flex-wrap gap-2">
            <Badge variant="outline">{t("badgeDraftOnly")}</Badge>
            <Badge variant="outline">{t("badgeNoColdWhatsapp")}</Badge>
          </div>
        </CardContent>
      </Card>

      {error && (
        <p className="text-destructive text-sm">{error}</p>
      )}

      {pack && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>{t("briefTitle")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm">{String(brief.greeting || "")}</p>
              <ul className="list-disc ps-5 text-sm space-y-1">
                {decisions.map((d) => (
                  <li key={d}>{d}</li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>{t("readinessTitle")}</CardTitle>
              <Badge>{String(readiness.score ?? "—")}%</Badge>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              <p>{String(readiness.stage ?? "")}</p>
            </CardContent>
          </Card>

          <div className="flex flex-wrap gap-3">
            <Button asChild>
              <Link href={`/${locale}/approvals`}>
                {t("ctaApprovals")} ({pending.count ?? 0})
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href={`/${locale}/command-center`}>{t("ctaCommandCenter")}</Link>
            </Button>
          </div>
        </>
      )}

      {!pack && !error && (
        <p className="text-muted-foreground text-sm">
          {isAr ? "جاري التحميل…" : "Loading…"}
        </p>
      )}
    </div>
  );
}
