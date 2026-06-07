"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || ""
    : "";

type PoolData = {
  total?: number;
  csv_path?: string;
  by_segment?: Record<string, number>;
  by_status?: Record<string, number>;
};

type P0Row = {
  company?: string;
  contact?: string;
  segment?: string;
  priority?: string;
  next_action?: string;
  status?: string;
};

type UniverseItem = {
  company?: string;
  segment?: string;
  tier?: string;
  city?: string;
  offer_id?: string;
  why_now?: string;
  icp_score?: number;
  source_url?: string;
};

export function OpsTargetingPanel() {
  const locale = useLocale();
  const t = useTranslations("targeting");
  const isAr = locale === "ar";
  const [err, setErr] = useState("");
  const [pool, setPool] = useState<PoolData | null>(null);
  const [p0, setP0] = useState<P0Row[]>([]);
  const [universe, setUniverse] = useState<UniverseItem[]>([]);
  const [universeSize, setUniverseSize] = useState<number>(0);
  const [importing, setImporting] = useState(false);

  const load = useCallback(async () => {
    if (!ADMIN_KEY) {
      setErr(t("missingAdminKey"));
      return;
    }
    setErr("");
    try {
      const [poolRes, p0Res] = await Promise.all([
        api.getTargetingPool(ADMIN_KEY),
        api.getTargetingP0Today(ADMIN_KEY, 10),
      ]);
      setPool(poolRes.data as PoolData);
      const items = (p0Res.data as { items?: P0Row[] }).items ?? [];
      setP0(items);
    } catch {
      setErr(t("loadFailed"));
    }
    // Real sourced universe — optional, degrades gracefully on older backends.
    try {
      const uniRes = await api.getTargetingUniverseToday(ADMIN_KEY, 10);
      const data = uniRes.data as { selection?: UniverseItem[]; universe_size?: number };
      setUniverse(data.selection ?? []);
      setUniverseSize(data.universe_size ?? 0);
    } catch {
      /* universe endpoint optional */
    }
  }, [t]);

  useEffect(() => {
    load();
  }, [load]);

  const importCsv = async () => {
    if (!ADMIN_KEY) return;
    setImporting(true);
    try {
      await api.importWarRoomTargets(ADMIN_KEY, { use_default_csv: true });
      await load();
    } catch {
      setErr(t("importFailed"));
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">{t("subtitle")}</p>
      {err && <p className="text-destructive text-sm">{err}</p>}

      {universe.length > 0 && (
        <Card className="border-gold-500/40 bg-navy-500/5 p-4 space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h2 className="font-semibold text-navy-500">
                {isAr ? "العالم المستهدف الحقيقي — اليوم" : "Real Sourced Universe — Today"}
              </h2>
              <p className="text-xs text-muted-foreground">
                {isAr
                  ? `${universeSize} حساب مُصدَّر · معلومات عامة · مقدمة دافئة أولاً · لا PII`
                  : `${universeSize} sourced accounts · public info · warm-intro-first · no PII`}
              </p>
            </div>
            <span className="rounded-full border border-gold-500/50 px-3 py-1 text-xs text-gold-700">
              {isAr ? "كل صف بمصدر عام" : "every row sourced"}
            </span>
          </div>
          <div className="overflow-x-auto rounded border">
            <table className="w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="p-2 text-start">{isAr ? "الشركة" : "Company"}</th>
                  <th className="p-2 text-start">ICP</th>
                  <th className="p-2 text-start">{isAr ? "الشريحة" : "Segment"}</th>
                  <th className="p-2 text-start">{isAr ? "لماذا الآن" : "Why now"}</th>
                  <th className="p-2 text-start">{isAr ? "المصدر" : "Source"}</th>
                </tr>
              </thead>
              <tbody>
                {universe.map((row, i) => (
                  <tr key={`${row.company}-${i}`} className="border-t align-top">
                    <td className="p-2 font-medium">
                      {row.company}
                      <span className="block text-xs text-muted-foreground">
                        {row.tier} · {row.city}
                      </span>
                    </td>
                    <td className="p-2">
                      <span className="rounded bg-gold-500/15 px-1.5 py-0.5 font-semibold text-gold-700">
                        {row.icp_score ?? "-"}
                      </span>
                    </td>
                    <td className="p-2 text-xs">{row.segment}</td>
                    <td className="p-2 text-xs text-muted-foreground max-w-[18rem]">{row.why_now}</td>
                    <td className="p-2 text-xs">
                      {row.source_url && (
                        <a
                          href={row.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-navy-400 underline"
                          dir="ltr"
                        >
                          {isAr ? "رابط" : "link"}
                        </a>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-xs text-muted-foreground">
            {isAr
              ? "مسودات اليوم: python3 scripts/dealix_daily_draft_pack.py --top 10 (كلها بموافقة قبل الإرسال)"
              : "Today's drafts: python3 scripts/dealix_daily_draft_pack.py --top 10 (all approval-gated)"}
          </p>
        </Card>
      )}

      <div className="grid gap-3 sm:grid-cols-3">
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{t("poolTotal")}</p>
          <p className="text-2xl font-semibold">{pool?.total ?? 0}</p>
          {pool?.csv_path && (
            <p className="text-xs text-muted-foreground mt-1 truncate" dir="ltr">
              {pool.csv_path}
            </p>
          )}
        </Card>
        <Card className="p-3 sm:col-span-2">
          <p className="text-xs text-muted-foreground mb-2">{t("bySegment")}</p>
          <div className="flex flex-wrap gap-2 text-xs">
            {Object.entries(pool?.by_segment ?? {}).map(([seg, n]) => (
              <span key={seg} className="rounded border px-2 py-0.5">
                {seg}: {n}
              </span>
            ))}
          </div>
        </Card>
      </div>

      <Card className="p-4 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="font-semibold">{t("p0Title")}</h2>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={load}>
              {t("refresh")}
            </Button>
            <Button size="sm" onClick={importCsv} disabled={importing}>
              {t("importWarRoom")}
            </Button>
            <Link href={`/${locale}/ops/founder`}>
              <Button size="sm" variant="secondary">
                {t("openFounder")}
              </Button>
            </Link>
          </div>
        </div>
        <div className="overflow-x-auto rounded border">
          <table className="w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="p-2 text-start">{t("col.company")}</th>
                <th className="p-2 text-start">{t("col.segment")}</th>
                <th className="p-2 text-start">{t("col.priority")}</th>
                <th className="p-2 text-start">{t("col.next")}</th>
              </tr>
            </thead>
            <tbody>
              {p0.map((row, i) => (
                <tr key={`${row.company}-${i}`} className="border-t">
                  <td className="p-2 font-medium">{row.company}</td>
                  <td className="p-2">{row.segment}</td>
                  <td className="p-2">{row.priority}</td>
                  <td className="p-2 text-xs text-muted-foreground">{row.next_action}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {p0.length === 0 && (
            <p className="p-4 text-center text-muted-foreground text-sm">{t("empty")}</p>
          )}
        </div>
      </Card>
    </div>
  );
}
