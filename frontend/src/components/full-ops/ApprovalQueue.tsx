"use client";

import { useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Check, CheckCheck, X } from "lucide-react";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn, getRiskColor, formatRelativeTime } from "@/lib/utils";
import { api } from "@/lib/api";
import type { ApprovalCardItem } from "./types";

const APPROVAL_WHO = process.env.NEXT_PUBLIC_APPROVAL_ACTOR?.trim() || "sami";

function normalizeRisk(raw: string | undefined): "high" | "medium" | "low" {
  const r = (raw || "low").toLowerCase();
  if (r === "high" || r === "critical") return "high";
  if (r === "medium") return "medium";
  return "low";
}

function approvalId(item: ApprovalCardItem): string {
  return String(item.approval_id || item.id || "unknown");
}

function QueueCard({
  item,
  isAr,
  busy,
  onApprove,
  onReject,
}: {
  item: ApprovalCardItem;
  isAr: boolean;
  busy: boolean;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const id = approvalId(item);
  const risk = normalizeRisk(item.risk_level);
  const summary =
    (isAr ? item.summary_ar : item.summary_en) ||
    item.summary_en ||
    item.summary_ar ||
    item.action_type ||
    id;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="rounded-2xl border border-border bg-card overflow-hidden"
    >
      <div
        className={cn(
          "h-1",
          risk === "high"
            ? "bg-red-500"
            : risk === "medium"
              ? "bg-gold-500"
              : "bg-emerald-500",
        )}
      />
      <div className="p-4">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="min-w-0">
            <p className="text-[11px] text-muted-foreground">
              {item.action_type || item.object_type || "—"}
            </p>
            <h4 className="text-sm font-semibold text-foreground leading-tight mt-0.5">
              {summary}
            </h4>
          </div>
          <Badge
            variant="outline"
            className={cn("text-[10px] flex-shrink-0", getRiskColor(risk))}
          >
            {t(`queue.risk.${risk}` as "queue.risk.low")}
          </Badge>
        </div>

        <div className="grid gap-1.5 mb-3 rounded-xl bg-muted/40 p-2.5">
          <Row label={isAr ? "القناة" : "Channel"} value={item.channel || "—"} />
          <Row
            label={isAr ? "الكائن" : "Object"}
            value={`${item.object_type || "—"} · ${item.object_id || "—"}`}
          />
          {item.proof_impact && (
            <Row
              label={isAr ? "أثر الإثبات" : "Proof impact"}
              value={item.proof_impact}
              accent
            />
          )}
          {item.created_at && (
            <Row
              label={isAr ? "وقت الطلب" : "Requested"}
              value={formatRelativeTime(item.created_at, locale)}
            />
          )}
        </div>

        <div className="flex gap-2">
          <Button
            variant="emerald"
            size="sm"
            className="flex-1"
            disabled={busy}
            onClick={() => onApprove(id)}
          >
            <Check className="w-3.5 h-3.5 me-1.5" />
            {t("queue.approve")}
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="flex-1 text-destructive border-destructive/30 hover:bg-destructive/10"
            disabled={busy}
            onClick={() => onReject(id)}
          >
            <X className="w-3.5 h-3.5 me-1.5" />
            {t("queue.reject")}
          </Button>
        </div>
      </div>
    </motion.div>
  );
}

function Row({
  label,
  value,
  accent,
}: {
  label: string;
  value: string;
  accent?: boolean;
}) {
  return (
    <div className="flex items-center justify-between text-xs">
      <span className="text-muted-foreground">{label}</span>
      <span
        className={cn(
          "font-medium truncate ms-2",
          accent ? "text-emerald-400" : "text-foreground",
        )}
      >
        {value}
      </span>
    </div>
  );
}

export function ApprovalQueue({
  items,
  loading,
  onChanged,
}: {
  items: ApprovalCardItem[];
  loading: boolean;
  onChanged: () => void;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [busy, setBusy] = useState(false);

  const handleApprove = async (id: string) => {
    setBusy(true);
    try {
      await api.postApprovalApprove(id, APPROVAL_WHO);
      toast.success(isAr ? "تمت الموافقة" : "Approved");
      onChanged();
    } catch {
      toast.error(isAr ? "فشلت الموافقة" : "Approve failed");
    } finally {
      setBusy(false);
    }
  };

  const handleReject = async (id: string) => {
    setBusy(true);
    const reason = isAr
      ? "مرفوض من لوحة العمليات الكاملة"
      : "Rejected from Full Ops console";
    try {
      await api.postApprovalReject(id, APPROVAL_WHO, reason);
      toast.success(isAr ? "تم الرفض" : "Rejected");
      onChanged();
    } catch {
      toast.error(isAr ? "فشل الرفض" : "Reject failed");
    } finally {
      setBusy(false);
    }
  };

  const handleBulkApprove = async () => {
    if (items.length === 0) return;
    setBusy(true);
    try {
      await api.postApprovalsBulkApprove({
        who: APPROVAL_WHO,
        approval_ids: items.map((i) => approvalId(i)),
      });
      toast.success(isAr ? "تمت الموافقة الجماعية" : "Bulk approved");
      onChanged();
    } catch {
      toast.error(isAr ? "فشلت الموافقة الجماعية" : "Bulk approve failed");
    } finally {
      setBusy(false);
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        {Array.from({ length: 2 }).map((_, i) => (
          <div
            key={i}
            className="h-44 rounded-2xl border border-border bg-muted/30 animate-pulse"
          />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <p className="text-xs text-muted-foreground">
          {t("queue.count", { count: items.length })}
        </p>
        <Button
          variant="gold"
          size="sm"
          disabled={busy || items.length === 0}
          onClick={handleBulkApprove}
        >
          <CheckCheck className="w-3.5 h-3.5 me-1.5" />
          {t("queue.bulkApprove")}
        </Button>
      </div>

      {items.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          <Check className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">{t("queue.empty")}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
          <AnimatePresence>
            {items.map((item) => (
              <QueueCard
                key={approvalId(item)}
                item={item}
                isAr={isAr}
                busy={busy}
                onApprove={handleApprove}
                onReject={handleReject}
              />
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
