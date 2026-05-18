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


