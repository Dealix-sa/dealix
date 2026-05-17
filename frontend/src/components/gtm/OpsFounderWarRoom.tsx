"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

const CHECKLIST_90_AR = [
  "0–10: brief + digest",
  "10–25: War Room 10 لمسات",
  "25–40: موافقات",
  "40–55: LinkedIn يدوي",
  "55–70: ديمو / Calendly",
  "70–85: متابعات + شريك",
  "85–90: أدلة + KPI",
];

type SocialPost = {
  title_ar?: string;
  pillar?: string;
  status?: string;
  cta_ar?: string;
  calendar_date?: string;
};

type WarRoomTarget = {
  company?: string;
  target?: string;
  status?: string;
  next_action?: string;
  segment?: string;
  outreach_draft_ar?: string;
};

type Dashboard = {
  tiles?: Record<string, number | Record<string, unknown>>;
  today_focus_ar?: string[];
  no_build_warnings?: string[];
  links?: Record<string, string>;
  policy_ar?: string;
  sovereign_gtm?: {
    social_post_due_today?: SocialPost | null;
    war_room_top_targets?: WarRoomTarget[];
    sample_proof_pack_path?: string;
    master_plan_path?: string;
    sovereign_gtm_path?: string;
  };
};

export function OpsFounderWarRoom() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<Dashboard | null>(null);
  const [todayTargets, setTodayTargets] = useState<WarRoomTarget[]>([]);
  const [health, setHealth] = useState<Record<string, unknown> | null>(null);
  const [err, setErr] = useState("");
  const [copiedCo, setCopiedCo] = useState("");
  const adminKey = getAdminApiKey();

  useEffect(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    const key = adminKey || "";
    Promise.all([
      api.getOpsFounderDashboard(key),
      api.getWarRoomTodayPack(key),
      api.getFullOpsHealth(key),
    ])
      .then(([dashRes, packRes, healthRes]) => {
        setData(dashRes.data as Dashboard);
        const pack = packRes.data as {
          targets?: { items?: WarRoomTarget[] };
        };
        setTodayTargets(pack.targets?.items ?? []);
        setHealth(healthRes.data as Record<string, unknown>);
      })
      .catch(() =>
        setErr(isAr ? "تعذّر تحميل لوحة المؤسس." : "Failed to load founder dashboard."),
      );
  }, [isAr, adminKey]);

  const copyOutreach = async (row: WarRoomTarget) => {
    const text = row.outreach_draft_ar || "";
    if (!text) return;
    await navigator.clipboard.writeText(text);
    setCopiedCo(row.company || row.target || "");
    setTimeout(() => setCopiedCo(""), 2000);
  };

  const tiles = data?.tiles ?? {};

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "غرفة إيراد يومية — ٩٠ دقيقة: موافقات · مبيعات · شركاء · دعم · محتوى."
          : "Daily revenue war room — 90 min: approvals · sales · partners · support · content."}
      </p>

      {err && <p className="text-destructive text-sm">{err}</p>}

      <Card className="p-4 border-primary/20 bg-muted/30">
        <h2 className="font-semibold mb-2">
          {isAr ? "صباح اليوم — أمر واحد" : "Morning — single command"}
        </h2>
        <pre className="text-xs bg-background/80 p-2 rounded border overflow-x-auto mb-2" dir="ltr">
          bash scripts/run_founder_commercial_day.sh
        </pre>
        <p className="text-xs text-muted-foreground mb-3">
          {isAr
            ? "مخرجات: data/founder_briefs/ · data/war_room_today.json"
            : "Outputs: data/founder_briefs/ · data/war_room_today.json"}
        </p>
        <div className="flex flex-wrap gap-2 text-sm">
          <Link href={`/${locale}/ops`} className="text-primary hover:underline">
            {isAr ? "مركز Ops" : "Ops hub"}
          </Link>
          <Link href={`/${locale}/ops/war-room`} className="text-primary hover:underline">
            War Room
          </Link>
          <Link href={`/${locale}/ops/marketing`} className="text-primary hover:underline">
            {isAr ? "تسويق" : "Marketing"}
          </Link>
          <Link href={`/${locale}/ops/approvals`} className="text-primary hover:underline">
            {isAr ? "موافقات" : "Approvals"}
          </Link>
          <Link href={`/${locale}/business-now`} className="text-primary hover:underline">
            Business NOW
          </Link>
        </div>
      </Card>

      <Card className="p-4">
        <h2 className="font-semibold mb-2">{isAr ? "خطة 90 دقيقة" : "90-min plan"}</h2>
        <ul className="text-sm space-y-1 list-disc mr-5">
          {CHECKLIST_90_AR.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </Card>

      {health && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">{isAr ? "صحة التشغيل" : "Ops health"}</h2>
          <p className="text-xs font-mono text-muted-foreground">
            {String((health as { verdict?: string }).verdict ?? "ok")}
          </p>
        </Card>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Object.entries(tiles).map(([k, v]) => (
          <Card key={k} className="p-4">
            <p className="text-xs text-muted-foreground uppercase">{k}</p>
            <p className="text-2xl font-semibold mt-1">
              {typeof v === "object" ? JSON.stringify(v) : String(v)}
            </p>
          </Card>
        ))}
      </div>

      {data?.today_focus_ar && isAr && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">تركيز اليوم</h2>
          <ul className="list-disc mr-5 space-y-1 text-sm">
            {data.today_focus_ar.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </Card>
      )}

      {data?.no_build_warnings && data.no_build_warnings.length > 0 && (
        <Card className="p-4 border-amber-500/40">
          <h2 className="font-semibold text-amber-600 mb-2">no-build</h2>
          <ul className="text-sm space-y-1">
            {data.no_build_warnings.map((w) => (
              <li key={w}>{w}</li>
            ))}
          </ul>
        </Card>
      )}

      {data?.sovereign_gtm?.social_post_due_today && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">
            {isAr ? "منشور LinkedIn اليوم (مسودة)" : "Today's LinkedIn draft"}
          </h2>
          <p className="text-sm font-medium">{data.sovereign_gtm.social_post_due_today.title_ar}</p>
          <p className="text-xs text-muted-foreground mt-1">
            {data.sovereign_gtm.social_post_due_today.pillar} ·{" "}
            {data.sovereign_gtm.social_post_due_today.status}
          </p>
          <p className="text-sm mt-2">{data.sovereign_gtm.social_post_due_today.cta_ar}</p>
        </Card>
      )}

      {todayTargets.length > 0 && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">
            {isAr ? "مسودات لمسة اليوم (P0)" : "Today's outreach drafts (P0)"}
          </h2>
          <ul className="text-sm space-y-3">
            {todayTargets.slice(0, 10).map((t) => (
              <li key={`${t.company}-${t.status}`} className="border-b pb-2">
                <span className="font-medium">{t.company ?? t.target}</span>
                <span className="text-muted-foreground text-xs"> · {t.status}</span>
                {t.outreach_draft_ar && (
                  <div className="mt-1 flex flex-wrap gap-2 items-start">
                    <p className="text-xs text-muted-foreground flex-1 line-clamp-2">
                      {t.outreach_draft_ar.slice(0, 160)}…
                    </p>
                    <Button size="sm" variant="outline" onClick={() => copyOutreach(t)}>
                      {copiedCo === (t.company || t.target)
                        ? isAr
                          ? "نُسخ"
                          : "Copied"
                        : isAr
                          ? "نسخ"
                          : "Copy"}
                    </Button>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </Card>
      )}

      {(data?.sovereign_gtm?.war_room_top_targets?.length ?? 0) > 0 && (
        <Card className="p-4">
          <h2 className="font-semibold mb-2">
            {isAr ? "أعلى أهداف War Room" : "Top War Room targets"}
          </h2>
          <ul className="text-sm space-y-2">
            {data!.sovereign_gtm!.war_room_top_targets!.slice(0, 10).map((t) => (
              <li key={`${t.company ?? t.target}-${t.status}`}>
                <span className="font-medium">{t.company ?? t.target}</span>
                <span className="text-muted-foreground"> · {t.status}</span>
                {t.next_action && (
                  <span className="block text-xs text-muted-foreground">{t.next_action}</span>
                )}
              </li>
            ))}
          </ul>
        </Card>
      )}

      {data?.policy_ar && isAr && (
        <p className="text-xs text-muted-foreground">{data.policy_ar}</p>
      )}

      <div className="flex flex-wrap gap-2 text-sm">
        <Link href={`/${locale}/approvals`} className="text-primary hover:underline">
          {isAr ? "مركز الموافقات" : "Approvals"}
        </Link>
        <Link href={`/${locale}/ops/war-room`} className="text-primary hover:underline">
          {isAr ? "غرفة الإيراد (7 أعمدة)" : "Revenue War Room"}
        </Link>
        <Link href={`/${locale}/ops/marketing`} className="text-primary hover:underline">
          {isAr ? "تسويق / سوشال" : "Marketing"}
        </Link>
        <Link href={`/${locale}/ops/partners`} className="text-primary hover:underline">
          {isAr ? "شركاء" : "Partners"}
        </Link>
        <Link href={`/${locale}/ops/sales`} className="text-primary hover:underline">
          {isAr ? "خط المبيعات" : "Sales pipeline"}
        </Link>
        <Link href={`/${locale}/ops/evidence`} className="text-primary hover:underline">
          {isAr ? "سجل الأدلة" : "Evidence ledger"}
        </Link>
        <Link href={`/${locale}/business-now#strategy`} className="text-primary hover:underline">
          {isAr ? "ديمو" : "Demo"}
        </Link>
      </div>
    </div>
  );
}
