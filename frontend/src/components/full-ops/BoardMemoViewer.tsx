"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { AlertTriangle, FileText, Play, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import type { BoardMemoResponse, BoardMemoSection } from "./types";

function defaultMonth(): string {
  const d = new Date();
  const yyyy = d.getUTCFullYear();
  const mm = String(d.getUTCMonth() + 1).padStart(2, "0");
  return `${yyyy}-${mm}`;
}

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

export function BoardMemoViewer() {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [month, setMonth] = useState<string>(defaultMonth());
  const [memo, setMemo] = useState<BoardMemoResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);

  const load = useCallback(
    async (target: string) => {
      setLoading(true);
      try {
        const res = await api.getFinancialBoardMemo(target);
        setMemo(unwrap<BoardMemoResponse>(res.data));
      } catch {
        setMemo(null);
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  useEffect(() => {
    void load(month);
  }, [load, month]);

  const handleRun = useCallback(async () => {
    setRunning(true);
    try {
      const res = await api.postFinancialBoardMemoRun(month);
      setMemo(unwrap<BoardMemoResponse>(res.data));
      toast.success(isAr ? "اكتملت مذكّرة المجلس" : "Board memo built");
    } catch {
      toast.error(
        isAr ? "فشل بناء مذكّرة المجلس" : "Board memo build failed",
      );
    } finally {
      setRunning(false);
    }
  }, [month, isAr]);

  const sections = memo?.sections ?? {};
  const orderedSlugs: string[] = Array.isArray(memo?.section_order)
    ? (memo!.section_order as string[])
    : Object.keys(sections);

  return (
    <div className="space-y-5">
      {/* Header — month picker + run */}
      <div className="flex flex-wrap items-end gap-3">
        <div className="flex flex-col gap-1">
          <label className="text-[11px] text-muted-foreground" htmlFor="memoMonth">
            {t("memo.monthLabel")}
          </label>
          <Input
            id="memoMonth"
            type="month"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
            className="w-44"
          />
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => void load(month)}
          disabled={loading}
        >
          <RefreshCw className={cn("w-3.5 h-3.5 me-1.5", loading && "animate-spin")} />
          {t("memo.reload")}
        </Button>
        <Button variant="gold" size="sm" onClick={handleRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("memo.build")}
        </Button>
      </div>

      {loading ? (
        <div className="h-40 rounded-xl border border-border bg-muted/30 animate-pulse" />
      ) : !memo || memo.empty ? (
        <div className="text-center py-10">
          <p className="text-sm text-muted-foreground inline-flex items-center gap-1.5">
            <FileText className="w-4 h-4" />
            {memo?.error === "month_must_be_yyyy_mm"
              ? t("memo.invalidMonth")
              : t("memo.emptyForMonth", { month })}
          </p>
        </div>
      ) : (
        <>
          {/* Memo header */}
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-foreground">
                {isAr ? memo.title_ar : memo.title_en}
              </p>
              <p className="text-xs text-muted-foreground mt-0.5">
                {memo.month}
                {memo.cycle_id ? (
                  <>
                    {" "}
                    · <span className="font-mono">{memo.cycle_id}</span>
                  </>
                ) : null}
              </p>
            </div>
            <div className="flex flex-wrap gap-1.5">
              <Badge
                variant={memo.sections_complete ? "emerald" : "gold"}
                className="text-[10px] px-1.5 py-0"
              >
                {memo.sections_complete
                  ? t("memo.complete")
                  : t("memo.incomplete")}
              </Badge>
              {memo.approval_id ? (
                <Badge variant="gold" className="text-[10px] px-1.5 py-0">
                  {t("memo.approvalQueued")}
                </Badge>
              ) : null}
            </div>
          </div>

          {/* Missing sections */}
          {memo.missing_sections && memo.missing_sections.length > 0 ? (
            <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 px-3 py-2">
              <p className="text-xs font-semibold text-amber-300 mb-1">
                {t("memo.missingSections")}
              </p>
              <p className="text-[11px] font-mono text-amber-200/90">
                {memo.missing_sections.join(", ")}
              </p>
            </div>
          ) : null}

          {/* Sections */}
          <ol className="space-y-3">
            {orderedSlugs.map((slug, idx) => {
              const block: BoardMemoSection = sections[slug] ?? {};
              const title = isAr ? block.title_ar : block.title_en;
              const body = isAr ? block.body_ar : block.body_en;
              return (
                <li
                  key={slug}
                  className="rounded-xl border border-border bg-muted/20 px-3 py-2.5"
                >
                  <p className="text-xs font-semibold text-foreground mb-1.5">
                    {idx + 1}. {title ?? slug}
                  </p>
                  {body ? (
                    <pre className="whitespace-pre-wrap text-[12px] leading-relaxed text-muted-foreground font-sans">
                      {body}
                    </pre>
                  ) : (
                    <p className="text-[11px] text-muted-foreground italic">
                      —
                    </p>
                  )}
                </li>
              );
            })}
          </ol>

          {/* Warnings */}
          {memo.warnings && memo.warnings.length > 0 ? (
            <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 px-3 py-2">
              <p className="text-xs font-semibold text-amber-300 mb-1 inline-flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                {t("memo.warnings")}
              </p>
              <ul className="text-[11px] text-amber-200/90 list-disc list-inside space-y-0.5">
                {memo.warnings.slice(0, 5).map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </>
      )}
    </div>
  );
}
