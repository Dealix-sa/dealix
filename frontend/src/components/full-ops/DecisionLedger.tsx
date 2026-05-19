"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { ClipboardList } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import type {
  StrategicDecisionItem,
  StrategicDecisionsResponse,
} from "./types";

function unwrap<T>(payload: unknown): T {
  if (
    payload &&
    typeof payload === "object" &&
    "data" in (payload as Record<string, unknown>)
  ) {
    return (payload as { data: T }).data;
  }
  return payload as T;
}

const DECISION_TYPES = [
  "SCALE",
  "BUILD",
  "KILL",
  "HOLD",
  "RAISE_PRICE",
  "OFFER_RETAINER",
  "HIRE",
  "CREATE_BUSINESS_UNIT",
  "CREATE_VENTURE_CANDIDATE",
] as const;

const STATUSES = [
  "recommended",
  "pending_approval",
  "approved",
  "rejected",
  "delegated",
] as const;

const ALL = "__all__";

export function decisionTypeVariant(
  type: string,
): "emerald" | "blue" | "red" | "gold" {
  switch (type) {
    case "SCALE":
    case "BUILD":
    case "HIRE":
    case "CREATE_BUSINESS_UNIT":
    case "CREATE_VENTURE_CANDIDATE":
      return "emerald";
    case "KILL":
      return "red";
    case "RAISE_PRICE":
    case "OFFER_RETAINER":
      return "gold";
    default:
      return "blue";
  }
}

export function statusVariant(
  status: string,
): "emerald" | "blue" | "red" | "gold" {
  switch (status) {
    case "approved":
      return "emerald";
    case "rejected":
      return "red";
    case "pending_approval":
      return "gold";
    case "delegated":
      return "blue";
    default:
      return "blue";
  }
}

export function DecisionLedger() {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [decisions, setDecisions] = useState<StrategicDecisionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [decisionType, setDecisionType] = useState<string>(ALL);
  const [status, setStatus] = useState<string>(ALL);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.getStrategicDecisions({
        decision_type: decisionType === ALL ? undefined : decisionType,
        status: status === ALL ? undefined : status,
        limit: 100,
      });
      const data = unwrap<StrategicDecisionsResponse>(res.data);
      setDecisions(Array.isArray(data?.decisions) ? data.decisions : []);
    } catch {
      setDecisions([]);
    } finally {
      setLoading(false);
    }
  }, [decisionType, status]);

  useEffect(() => {
    void load();
  }, [load]);

  const statusLabel = useMemo(
    () => (s: string) =>
      t(`strategy.ledger.status.${s}` as "strategy.ledger.status.recommended"),
    [t],
  );

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <Select value={decisionType} onValueChange={setDecisionType}>
          <SelectTrigger className="h-9 w-auto min-w-[180px] text-xs">
            <SelectValue placeholder={t("strategy.ledger.filterType")} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>
              {t("strategy.ledger.allTypes")}
            </SelectItem>
            {DECISION_TYPES.map((dt) => (
              <SelectItem key={dt} value={dt}>
                {dt}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={status} onValueChange={setStatus}>
          <SelectTrigger className="h-9 w-auto min-w-[180px] text-xs">
            <SelectValue placeholder={t("strategy.ledger.filterStatus")} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>
              {t("strategy.ledger.allStatuses")}
            </SelectItem>
            {STATUSES.map((s) => (
              <SelectItem key={s} value={s}>
                {statusLabel(s)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {loading ? (
        <div className="space-y-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div
              key={i}
              className="h-14 rounded-xl border border-border bg-muted/30 animate-pulse"
            />
          ))}
        </div>
      ) : decisions.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          <ClipboardList className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">{t("strategy.ledger.empty")}</p>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-border">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-border bg-muted/30 text-muted-foreground">
                <th className="px-3 py-2 text-start font-semibold">
                  {t("strategy.ledger.col.type")}
                </th>
                <th className="px-3 py-2 text-start font-semibold">
                  {t("strategy.ledger.col.target")}
                </th>
                <th className="px-3 py-2 text-start font-semibold">
                  {t("strategy.ledger.col.rationale")}
                </th>
                <th className="px-3 py-2 text-end font-semibold">
                  {t("strategy.ledger.col.score")}
                </th>
                <th className="px-3 py-2 text-start font-semibold">
                  {t("strategy.ledger.col.band")}
                </th>
                <th className="px-3 py-2 text-start font-semibold">
                  {t("strategy.ledger.col.status")}
                </th>
              </tr>
            </thead>
            <tbody>
              {decisions.map((d) => (
                <tr
                  key={d.decision_id}
                  className="border-b border-border last:border-0 hover:bg-muted/20"
                >
                  <td className="px-3 py-2">
                    <Badge
                      variant={decisionTypeVariant(d.decision_type)}
                      className="text-[10px] px-1.5 py-0"
                    >
                      {d.decision_type}
                    </Badge>
                  </td>
                  <td className="px-3 py-2 text-foreground">{d.target}</td>
                  <td className="px-3 py-2 text-muted-foreground max-w-xs truncate">
                    {isAr ? d.rationale_ar : d.rationale_en}
                  </td>
                  <td className="px-3 py-2 text-end tabular-nums text-foreground">
                    {d.score}
                  </td>
                  <td className="px-3 py-2 text-muted-foreground">
                    {d.decision_band}
                  </td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap items-center gap-1">
                      <Badge
                        variant={statusVariant(d.status)}
                        className="text-[10px] px-1.5 py-0"
                      >
                        {statusLabel(d.status)}
                      </Badge>
                      {d.irreversible && (
                        <span
                          className={cn(
                            "rounded-md bg-red-500/10 px-1.5 py-0.5 text-[10px] text-red-400",
                          )}
                        >
                          {t("strategy.ledger.irreversible")}
                        </span>
                      )}
                      {d.requires_approval && (
                        <span className="rounded-md bg-gold-500/10 px-1.5 py-0.5 text-[10px] text-gold-400">
                          {t("strategy.ledger.requiresApproval")}
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
