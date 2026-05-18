"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import Link from "next/link";
import { AlertTriangle, CheckCircle2, Loader2, Rocket } from "lucide-react";
import { fetchLaunchStatusPublic, fetchHealthz, fetchVersion } from "@/lib/public-api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function FounderLaunchBoard() {
  const t = useTranslations("founder");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [loading, setLoading] = useState(true);
  const [launch, setLaunch] = useState<Record<string, unknown> | null>(null);
  const [healthOk, setHealthOk] = useState(false);
  const [versionOk, setVersionOk] = useState(false);

  useEffect(() => {
    void (async () => {
      const [ls, hz, ver] = await Promise.all([
        fetchLaunchStatusPublic(),
        fetchHealthz(),
        fetchVersion(),
      ]);
      if (ls.ok && ls.data) setLaunch(ls.data);
      setHealthOk(Boolean(hz.ok && hz.data?.status === "ok"));
      setVersionOk(Boolean(ver.ok));
      setLoading(false);
    })();
  }, []);

  const verdict =
    launch && typeof launch.verdict === "string"
      ? launch.verdict
      : launch && typeof launch.status === "string"
        ? launch.status
        : null;

  return (
    <div className="space-y-8" dir={isAr ? "rtl" : "ltr"}>
      <div className={cn("max-w-3xl", isAr ? "text-right" : "text-left")}>
        <p className="text-sm font-medium text-primary uppercase tracking-wide">
          {t("eyebrow")}
        </p>
        <h1 className="mt-2 text-3xl md:text-4xl font-bold font-display">{t("title")}</h1>
        <p className="mt-3 text-muted-foreground leading-relaxed">{t("subtitle")}</p>
      </div>

      {loading ? (
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="w-5 h-5 animate-spin" />
          {t("loading")}
        </div>
      ) : (
        <div className="grid md:grid-cols-3 gap-4">
          <Card className="card-glass">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                {healthOk ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-destructive" />
                )}
                {t("apiHealth")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{healthOk ? "200" : "—"}</p>
              <p className="text-xs text-muted-foreground mt-1">/healthz</p>
            </CardContent>
          </Card>

          <Card className="card-glass">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                {versionOk ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-amber-500" />
                )}
                {t("apiVersion")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm font-medium">
                {versionOk ? t("versionLive") : t("versionDeploy")}
              </p>
              <p className="text-xs text-muted-foreground mt-1">/version</p>
            </CardContent>
          </Card>

          <Card className="card-glass border-primary/30">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Rocket className="w-4 h-4 text-primary" />
                {t("launchVerdict")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg font-semibold capitalize">{verdict ?? t("unknown")}</p>
            </CardContent>
          </Card>
        </div>
      )}

      {launch && (
        <Card className="card-glass">
          <CardHeader>
            <CardTitle className="text-base">{t("rawStatus")}</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="text-xs font-mono bg-muted/40 rounded-xl p-4 overflow-auto max-h-[420px]">
              {JSON.stringify(launch, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}

      <div className="flex flex-wrap gap-3">
        <Button variant="gold" asChild>
          <Link href={`/${locale}/dashboard`}>{t("openDashboard")}</Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href={`/${locale}/trust-check`}>{t("trustCheck")}</Link>
        </Button>
        <Button variant="outline" asChild>
          <Link href={`/${locale}/approvals`}>{t("approvals")}</Link>
        </Button>
      </div>
    </div>
  );
}
