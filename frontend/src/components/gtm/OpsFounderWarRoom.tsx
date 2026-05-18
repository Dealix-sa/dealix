"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type ComprehensivePlan = {
  weekly_one_decision?: {
    verdict?: string;
    week_id?: string;
    one_decision?: string;
    supports_phase?: string | number;
    stop_list?: string[];
    latest_path?: string;
  };
  master_execution_phase?: {
    active_phase?: number;
    active_label_ar?: string;
    phases?: { phase: number; label_ar?: string; is_active?: boolean; is_complete?: boolean }[];
  };
  phase_0_1_gate?: {
    verdict?: string;
    no_build_until_closed?: boolean;
    blockers_ar?: string[];
  };
  max_ops_backlog?: {
    verdict?: string;
    percent_done?: number;
    done?: number;
    total?: number;
    doc?: string;
  };
  dogfooding?: {
    war_room_ready?: boolean;
    sync_script?: string;
    doc?: string;
  };
};

function MasterPhaseStrip({
  plan,
  isAr,
}: {
  plan: ComprehensivePlan;
  isAr: boolean;
}) {
  const phases = plan.master_execution_phase?.phases ?? [];
  const active = plan.master_execution_phase?.active_phase ?? 0;
  if (phases.length === 0) {
    return (
      <p className="text-xs text-muted-foreground">
        {isAr ? `المرحلة النشطة: ${active}` : `Active phase: ${active}`}
      </p>
    );
  }
  return (
    <div className="flex flex-wrap gap-1" role="list">
      {phases.map((p) => (
        <span
          key={p.phase}
          className={`text-xs px-2 py-0.5 rounded border ${
            p.is_active
              ? "border-primary bg-primary/20 font-semibold"
              : p.is_complete
                ? "border-emerald-500/40 text-emerald-700 dark:text-emerald-400"
                : "border-muted text-muted-foreground"
          }`}
          title={p.label_ar}
        >
          {p.phase}
        </span>
      ))}
    </div>
  );
}

function WeeklyDecisionBlock({
  plan,
  isAr,
}: {
  plan: ComprehensivePlan;
  isAr: boolean;
}) {
  const w = plan.weekly_one_decision;
  const decision = (w?.one_decision || "").trim();
  return (
    <div>
      <p className="text-xs text-muted-foreground mb-1">
        {isAr ? "قرار الأسبوع" : "Weekly decision"} · {w?.week_id ?? "—"} ·{" "}
        <span className="font-mono">{w?.verdict ?? "—"}</span>
      </p>
      <p className="text-sm">
        {decision ||
          (isAr ? "— املأ عبر founder_weekly_decision_init.py" : "— run founder_weekly_decision_init.py")}
      </p>
      {w?.supports_phase != null && w.supports_phase !== "" && (
        <p className="text-xs text-muted-foreground mt-1">
          {isAr ? "يدعم مرحلة" : "supports_phase"}: {String(w.supports_phase)}
        </p>
      )}
    </div>
  );
}

const CHECKLIST_90_AR = [
  "0–10: brief + digest",
  "10–25: War Room 10 لمسات",
  "25–40: موافقات",
  "40–55: LinkedIn يدوي",
  "55–70: ديمو / Calendly",
  "70–85: متابعات + شريك",
  "85–90: أدلة + KPI",
];

type WarRoomTarget = {
  company?: string;
  target?: string;
  status?: string;
  next_action?: string;
  segment?: string;
  outreach_draft_ar?: string;
};

type CockpitResponse = {
  comprehensive_plan?: ComprehensivePlan;
};

export function OpsFounderWarRoom() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [plan, setPlan] = useState<ComprehensivePlan | null>(null);
  const [targets, setTargets] = useState<WarRoomTarget[]>([]);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      setLoading(false);
      return;
    }
    const key = getAdminApiKey();
    setLoading(true);
    setErr("");
    Promise.all([
      api.getFounderCockpit(key, 10, "morning"),
      api.getWarRoom(key, { top_n: 6 }),
    ])
      .then(([cockpitRes, warRes]) => {
        setPlan((cockpitRes.data as CockpitResponse)?.comprehensive_plan ?? null);
        setTargets((warRes.data as { items?: WarRoomTarget[] })?.items ?? []);
      })
      .catch(() => setErr(isAr ? "تعذّر تحميل غرفة الحرب" : "Failed to load war room"))
      .finally(() => setLoading(false));
  }, [isAr]);

  return (
    <Card className="p-4 space-y-3">
      <div className="flex items-center justify-between gap-2">
        <h3 className="text-sm font-semibold">
          {isAr ? "غرفة حرب المؤسس" : "Founder war room"}
        </h3>
        <Button asChild variant="outline" size="sm">
          <Link href={`/${locale}/ops/war-room`}>
            {isAr ? "افتح غرفة الحرب" : "Open war room"}
          </Link>
        </Button>
      </div>

      {loading && (
        <p className="text-xs text-muted-foreground">
          {isAr ? "جارٍ التحميل…" : "Loading…"}
        </p>
      )}
      {err && <p className="text-xs text-destructive">{err}</p>}

      {!loading && !err && (
        <>
          {plan && (
            <div className="space-y-2">
              <MasterPhaseStrip plan={plan} isAr={isAr} />
              <WeeklyDecisionBlock plan={plan} isAr={isAr} />
            </div>
          )}

          <div>
            <p className="text-xs text-muted-foreground mb-1">
              {isAr ? "إيقاع الـ90 دقيقة" : "90-minute cadence"}
            </p>
            <ul className="text-xs space-y-0.5 list-disc ps-4">
              {CHECKLIST_90_AR.map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>
          </div>

          <div>
            <p className="text-xs text-muted-foreground mb-1">
              {isAr ? "أهداف اليوم" : "Today's targets"}
            </p>
            {targets.length === 0 ? (
              <p className="text-xs text-muted-foreground">
                {isAr
                  ? "لا أهداف — استورد قائمة في غرفة الحرب."
                  : "No targets — import a list in the war room."}
              </p>
            ) : (
              <ul className="space-y-1" role="list">
                {targets.map((tgt, i) => (
                  <li
                    key={`${tgt.company ?? tgt.target ?? "row"}-${i}`}
                    className="text-xs border rounded px-2 py-1"
                  >
                    <span className="font-medium">
                      {tgt.company ?? tgt.target ?? "—"}
                    </span>
                    {tgt.segment ? (
                      <span className="text-muted-foreground"> · {tgt.segment}</span>
                    ) : null}
                    {tgt.status ? (
                      <span className="text-muted-foreground"> · {tgt.status}</span>
                    ) : null}
                    {tgt.next_action ? (
                      <span className="block text-muted-foreground">
                        {tgt.next_action}
                      </span>
                    ) : null}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </>
      )}
    </Card>
  );
}

